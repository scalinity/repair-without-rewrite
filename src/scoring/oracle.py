"""Independent exhaustive path enumerator. No optimized scorer imports.

The tiny domain deliberately visits every monotone triple path; the separate
dense lexicographic DP supports bounded development parity without lattices.
"""
from functools import lru_cache
from itertools import product

GAP = None
MOVES = tuple(x for x in product((0, 1), repeat=3) if any(x))


def distance(x, y):
    @lru_cache(None)
    def suffix(i, j):
        if i == len(x):
            return len(y) - j
        if j == len(y):
            return len(x) - i
        return min(1 + suffix(i + 1, j), 1 + suffix(i, j + 1),
                   (x[i] != y[j]) + suffix(i + 1, j + 1))
    return suffix(0, 0)


def pair_oracle(x, y):
    best, edges, mappings, paths = float('inf'), set(), [set() for _ in x], 0

    def visit(i, j, cost, path, mapping):
        nonlocal best, edges, mappings, paths
        if (i, j) == (len(x), len(y)):
            if cost < best:
                best, edges, mappings, paths = cost, set(), [set() for _ in x], 0
            if cost == best:
                edges.update(path)
                for k, v in enumerate(mapping):
                    mappings[k].add(v)
                paths += 1
            return
        if i < len(x):
            visit(i+1, j, cost+1, path+[((i,j),(i+1,j))], mapping+[None])
        if j < len(y):
            visit(i, j+1, cost+1, path+[((i,j),(i,j+1))], mapping)
        if i < len(x) and j < len(y):
            visit(i+1, j+1, cost+(x[i]!=y[j]), path+[((i,j),(i+1,j+1))], mapping+[j])
    visit(0, 0, 0, [], [])
    return {'distance':best, 'edges':edges, 'reference_mappings':mappings, 'paths':paths}


def enumerate_triple(r, s, o):
    """Enumerate all paths, with no pair-lattice/shortest-path pruning."""
    best = None
    minimum, maximum, imin, imax = 0, 0, 0, 0
    consensus = [set() for _ in r]
    paths_visited = 0

    def visit(i, j, k, rs, ro, so, repair, introduced, local):
        nonlocal best, minimum, maximum, imin, imax, consensus, paths_visited
        if (i, j, k) == (len(r), len(s), len(o)):
            paths_visited += 1
            key = (rs + ro, so)
            if best is None or key < best:
                best = key
                minimum = maximum = repair
                imin = imax = introduced
                consensus = [{v} for v in local]
            elif key == best:
                minimum, maximum = min(minimum,repair), max(maximum,repair)
                imin, imax = min(imin,introduced), max(imax,introduced)
                for idx, v in enumerate(local):
                    consensus[idx].add(v)
            return
        for a,b,c in MOVES:
            if i+a>len(r) or j+b>len(s) or k+c>len(o):
                continue
            x,y,z = r[i] if a else GAP, s[j] if b else GAP, o[k] if c else GAP
            es,eo = int(x!=y), int(x!=z)
            label = 'repair' if es>eo else 'introduced' if eo>es else 'unresolved' if es else 'preserved'
            visit(i+a,j+b,k+c,rs+es,ro+eo,so+(y!=z),repair+max(es-eo,0),
                  introduced+max(eo-es,0),local+[(label,k if c else None)] if a else local)
    visit(0,0,0,0,0,0,0,0,[])
    return {'eS':distance(r,s),'eO':distance(r,o),'h':best[1],
            'repair':(minimum,maximum),'introduced':(imin,imax),
            'reference_events':consensus,'paths_visited':paths_visited}


def dense_triple(r, s, o):
    """Independent dense prefix recurrence: lexicographic (RS+RO, SO).

    No lattice, graph edges, source masks or optimized traceback is reused.
    Directly tracks both reward extrema on every tied prefix optimum.
    """
    cells = {(0,0,0): ((0,0),0,0,0,0)}
    for i in range(len(r)+1):
        for j in range(len(s)+1):
            for k in range(len(o)+1):
                if (i,j,k)==(0,0,0):
                    continue
                best, rrlo, rrhi, iilo, iihi = None, 0, 0, 0, 0
                for a,b,c in MOVES:
                    if i<a or j<b or k<c:
                        continue
                    prev=cells[i-a,j-b,k-c]
                    x,y,z=r[i-1] if a else GAP,s[j-1] if b else GAP,o[k-1] if c else GAP
                    es,eo=int(x!=y),int(x!=z)
                    key=(prev[0][0]+es+eo,prev[0][1]+(y!=z))
                    values=(prev[1]+max(es-eo,0),prev[2]+max(es-eo,0),
                            prev[3]+max(eo-es,0),prev[4]+max(eo-es,0))
                    if best is None or key<best:
                        best=key
                        rrlo,rrhi,iilo,iihi=values
                    elif key==best:
                        rrlo,rrhi=min(rrlo,values[0]),max(rrhi,values[1])
                        iilo,iihi=min(iilo,values[2]),max(iihi,values[3])
                cells[i,j,k]=(best,rrlo,rrhi,iilo,iihi)
    final=cells[len(r),len(s),len(o)]
    return {'eS':distance(r,s),'eO':distance(r,o),'h':final[0][1],
            'repair':(final[1],final[2]),'introduced':(final[3],final[4])}
