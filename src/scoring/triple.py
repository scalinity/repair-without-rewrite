"""Integer all-optimal pair lattices and compatible joint DAG, v1.2 IV.4-9.

This implementation is deliberately separate from oracle.py's path enumeration
and dense lexicographic recurrence. No alignment routine is shared.
"""
from array import array
from dataclasses import dataclass
import hashlib
import heapq
import json

MOVES = ((1,1,1),(1,1,0),(1,0,1),(0,1,1),(1,0,0),(0,1,0),(0,0,1))
_UNSET = object()


@dataclass(frozen=True)
class Limits:
    pair_cells: int = 4_000_000
    joint_states: int = 250_000
    joint_moves: int = 1_750_000


def distance(x, y):
    row=list(range(len(y)+1))
    for i,a in enumerate(x,1):
        nxt=[i]
        for j,b in enumerate(y,1):
            nxt.append(min(nxt[j-1]+1,row[j]+1,row[j-1]+(a!=b)))
        row=nxt
    return row[-1]


def lattice(x, y, budget=4_000_000):
    n,m=len(x),len(y)
    if (n+1)*(m+1)>budget:
        return None
    width=m+1
    f=array('I',[0])*((n+1)*width)
    back=array('I',[0])*((n+1)*width)
    for i in range(n+1):
        f[i*width]=i
    for j in range(m+1):
        f[j]=j
    for i in range(1,n+1):
        for j in range(1,m+1):
            idx=i*width+j
            f[idx]=min(f[idx-width]+1,f[idx-1]+1,f[idx-width-1]+(x[i-1]!=y[j-1]))
    for i in range(n+1):
        back[i*width+m]=n-i
    for j in range(m+1):
        back[n*width+j]=m-j
    for i in range(n-1,-1,-1):
        for j in range(m-1,-1,-1):
            idx=i*width+j
            back[idx]=min(back[idx+width]+1,back[idx+1]+1,
                          back[idx+width+1]+(x[i]!=y[j]))
    total=f[-1]
    edges={}
    counts={(0,0):1}
    for i in range(n+1):
        for j in range(m+1):
            idx=i*width+j
            if f[idx]+back[idx]!=total:
                continue
            destinations=[]
            for a,b in ((1,1),(1,0),(0,1)):
                if i+a>n or j+b>m:
                    continue
                cost=(x[i]!=y[j]) if a and b else 1
                if f[idx]+cost+back[(i+a)*width+j+b]==total:
                    dst=(i+a,j+b)
                    destinations.append(dst)
                    counts[dst]=min(2,counts.get(dst,0)+counts.get((i,j),0))
            edges[i,j]=tuple(destinations)
    return {'distance':total,'edges':edges,'path_count_saturated':counts.get((n,m),0),
            'cells':(n+1)*(m+1)}


def source_masks(r, s, rs):
    if rs is None:
        return {'status':'computationally_unavailable','reference':None,'source':None,
                'gap_sequences':None}
    reference=[set() for _ in r]
    source=[set() for _ in s]
    for (i,j),destinations in rs['edges'].items():
        for ii,jj in destinations:
            if ii>i:
                reference[i].add(j if jj>j else None)
            if jj>j:
                source[j].add(('reference',i) if ii>i else ('gap',i))
    labels=[]
    for i,mappings in enumerate(reference):
        correct={j for j in mappings if j is not None and r[i]==s[j]}
        labels.append('certain_correct' if len(mappings)==1 and correct else
                      'certain_error' if not correct else 'ambiguous')
    gaps=[]
    for i in range(len(r)+1):
        uncertain=any(('gap',i) in v and len(v)>1 for v in source)
        gaps.append(None if uncertain else tuple(j for j,v in enumerate(source) if v=={('gap',i)}))
    return {'status':'available','reference':tuple(tuple(sorted(v,key=lambda z:-1 if z is None else z)) for v in reference),
            'reference_labels':tuple(labels),'source':tuple(tuple(sorted(v)) for v in source),
            'gap_sequences':tuple(gaps),'pair_unique':rs['path_count_saturated']==1}


def _fallback(eS,eO,reason,states,moves):
    return {'repair':(max(0,eS-eO),eS),'introduced':(max(0,eO-eS),eO),
            'h':None,'reference_events':None,'source_events':None,'witness':None,
            'reference_damage':(0,eO),'insertion_damage':(0,eO),
            'edited_unresolved':(0,min(eS,eO)),
            'fixed_correct_damage':None,'fixed_error_repair':None,
            'status':'resource_envelope','fallback_reason':reason,
            'joint_states':states,'joint_moves':moves,'joint_edges':None}


def _known_totals_on_fallback(r,s,o,base,result):
    # Resource limits can remove local correspondence evidence, never a proved
    # identity/perfect-reference total. These conditions are candidate-independent
    # identities of the normalized triple, not an approximate alignment rescue.
    eS,eO=base['eS'],base['eO']
    if o==s:
        result.update(repair=(0,0),introduced=(0,0),h=0,status='closed_form_point')
    elif o==r:
        result.update(repair=(eS,eS),introduced=(0,0),h=eS,status='closed_form_point')
    elif s==r:
        result.update(repair=(0,0),introduced=(eO,eO),h=eO,status='closed_form_point')
    return base|result


def score_tokens(reference, source, output, limits=Limits(), prepared_lattice=_UNSET):
    r,s,o=tuple(reference),tuple(source),tuple(output)
    if any(v is None for seq in (r,s,o) for v in seq):
        raise ValueError('None is reserved as the tagged gap')
    eS,eO=distance(r,s),distance(r,o)
    rs=lattice(r,s,limits.pair_cells) if prepared_lattice is _UNSET else prepared_lattice
    ro=lattice(r,o,limits.pair_cells)
    masks=source_masks(r,s,rs)
    base={'eS':eS,'eO':eO,'eSO':distance(s,o),'source_masks':masks,
          'reference_words':len(r),'source_words':len(s),'output_words':len(o)}
    if rs is None or ro is None:
        return _known_totals_on_fallback(r,s,o,base,_fallback(eS,eO,'pair_lattice_cap',0,0))
    start=(0,0,0); final=(len(r),len(s),len(o))
    if limits.joint_states<1:
        return _known_totals_on_fallback(r,s,o,base,_fallback(eS,eO,'joint_state_cap',0,0))
    forward={start:0}; adjacency={}; heap=[(0,*start)]; moves=0
    ordered=[]
    while heap:
        _,i,j,k=heapq.heappop(heap)
        u=(i,j,k);ordered.append(u);out=[]
        for a,b,c in MOVES:
            if moves==limits.joint_moves:
                return _known_totals_on_fallback(r,s,o,base,_fallback(eS,eO,'joint_move_cap',len(forward),moves))
            moves+=1
            v=(i+a,j+b,k+c)
            if v[0]>len(r) or v[1]>len(s) or v[2]>len(o):
                continue
            if (a or b) and v[:2] not in rs['edges'].get((i,j),()):
                continue
            if (a or c) and (v[0],v[2]) not in ro['edges'].get((i,k),()):
                continue
            x,y,z=r[i] if a else None,s[j] if b else None,o[k] if c else None
            es,eo=int(x!=y),int(x!=z)
            cost=int(y!=z)
            label='repair' if es>eo else 'introduced' if eo>es else 'unresolved' if es else 'preserved'
            rewards=(max(es-eo,0),max(eo-es,0),int(a and eo>es),
                     int(not a and eo>es),int(es and eo and y!=z),
                     int(a and masks['reference_labels'][i]=='certain_correct' and eo>es),
                     int(es>eo and ((a and masks['reference_labels'][i]=='certain_error') or
                         (not a and b and len(masks['source'][j])==1 and masks['source'][j][0][0]=='gap'))))
            if v not in forward:
                if len(forward)==limits.joint_states:
                    return _known_totals_on_fallback(r,s,o,base,_fallback(eS,eO,'joint_state_cap',len(forward),moves))
                forward[v]=forward[u]+cost
                heapq.heappush(heap,(sum(v),*v))
            else:
                forward[v]=min(forward[v],forward[u]+cost)
            out.append((v,cost,rewards,label,k if c else None,a,b))
        adjacency[u]=out
    if final not in forward:
        raise AssertionError('compatible triple existence failed')
    backward={final:0}
    for u in reversed(ordered):
        for v,cost,*_ in adjacency[u]:
            if v in backward:
                backward[u]=min(backward.get(u,10**18),cost+backward[v])
    optimal=forward[final]
    lo={start:(0,)*7};hi={start:(0,)*7};retained={}
    events=[set() for _ in r];source_events=[set() for _ in s]
    for u in ordered:
        good=[]
        for edge in adjacency[u]:
            v,cost,rewards,label,mapping,a,b=edge
            if v not in backward or forward[u]+cost+backward[v]!=optimal:
                continue
            good.append(edge)
            candidate_lo=tuple(x+y for x,y in zip(lo[u],rewards))
            candidate_hi=tuple(x+y for x,y in zip(hi[u],rewards))
            lo[v]=tuple(min(x,y) for x,y in zip(lo.get(v,candidate_lo),candidate_lo))
            hi[v]=tuple(max(x,y) for x,y in zip(hi.get(v,candidate_hi),candidate_hi))
            if a:
                events[u[0]].add((label,mapping))
            if b:
                source_events[u[1]].add((label,'reference' if a else 'gap',u[0],mapping))
        retained[u]=good
    witness=[];u=start
    while u!=final:
        edge=retained[u][0]
        v=edge[0];witness.append(tuple(y-x for x,y in zip(u,v)));u=v
    repairs=(lo[final][0],hi[final][0]);introduced=(lo[final][1],hi[final][1])
    assert tuple(x-eS+eO for x in repairs)==introduced
    return base|{'repair':repairs,'introduced':introduced,'h':optimal,
                 'reference_events':events,'source_events':source_events,'witness':witness,
                 'reference_damage':(lo[final][2],hi[final][2]),
                 'insertion_damage':(lo[final][3],hi[final][3]),
                 'edited_unresolved':(lo[final][4],hi[final][4]),
                 'fixed_correct_damage':(lo[final][5],hi[final][5]),
                 'fixed_error_repair':(lo[final][6],hi[final][6]),
                 'status':'exact_point' if repairs[0]==repairs[1] else 'exact_interval',
                 'fallback_reason':None,'joint_states':len(forward),'joint_moves':moves,
                 'joint_edges':sum(len(v) for v in adjacency.values())}


def serialize(value):
    def safe(x):
        if isinstance(x,dict):
            return {k:safe(v) for k,v in x.items()}
        if isinstance(x,set):
            return sorted((safe(v) for v in x),key=lambda v:json.dumps(v,sort_keys=True))
        if isinstance(x,(tuple,list)):
            return [safe(v) for v in x]
        return x
    return json.dumps(safe(value),sort_keys=True,separators=(',',':'),ensure_ascii=False)


def seal(value):
    return hashlib.sha256(serialize(value).encode('utf-8')).hexdigest()
