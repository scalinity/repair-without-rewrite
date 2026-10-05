"""Pinned lexical_eval_v1 and conservative, explicit raw-span provenance."""
from dataclasses import dataclass
from pathlib import Path
import hashlib
import unicodedata2 as ud

TABLE_ROOT=Path(__file__).resolve().parents[2]/'docs/design-inputs/unicode-15.1.0'
assert ud.unidata_version=='15.1.0'
FOLD={}
for line in (TABLE_ROOT/'CaseFolding.txt').read_text().splitlines():
    content=line.split('#',1)[0].strip()
    if not content:
        continue
    cp,status,target,*_=map(str.strip,content.split(';'))
    if status in ('C','F'):
        FOLD[chr(int(cp,16))]=''.join(chr(int(v,16)) for v in target.split())
WHITE=set()
for line in (TABLE_ROOT/'PropList.txt').read_text().splitlines():
    content=line.split('#',1)[0].strip()
    if not content:
        continue
    span,prop=map(str.strip,content.split(';'))
    if prop=='White_Space':
        first,*last=span.split('..')
        WHITE.update(chr(v) for v in range(int(first,16),int(last[0] if last else first,16)+1))
POLICY_HASH=hashlib.sha256(('lexical_eval_v1:15.1.0:'+''.join(
    hashlib.sha256((TABLE_ROOT/name).read_bytes()).hexdigest()
    for name in ('CaseFolding.txt','PropList.txt'))+
    hashlib.sha256(Path(ud.__file__).read_bytes()).hexdigest()).encode()).hexdigest()


def strict_text(value):
    if isinstance(value,bytes):
        return value.decode('utf-8',errors='strict')
    if isinstance(value,str):
        value.encode('utf-8',errors='strict')
        return value
    raise ValueError('Text must be present bytes/string; empty is allowed, null is not')


def _nfc_with_origins(items):
    decomposed=[]
    for char,origin in items:
        for scalar in ud.normalize('NFD',char):
            decomposed.append((scalar,origin))
            c=ud.combining(scalar)
            pos=len(decomposed)-1
            while c and pos>0 and ud.combining(decomposed[pos-1][0])>c:
                decomposed[pos-1],decomposed[pos]=decomposed[pos],decomposed[pos-1]
                pos-=1
    composed=[];starter=None;last_class=0
    for scalar,origin in decomposed:
        c=ud.combining(scalar)
        combined=ud.normalize('NFC',composed[starter][0]+scalar) if starter is not None else ''
        if starter is not None and (last_class<c or last_class==0) and len(combined)==1:
            composed[starter]=(combined,composed[starter][1]|origin)
        else:
            if c==0:
                starter=len(composed)
            composed.append((scalar,origin));last_class=c
    return composed


@dataclass(frozen=True)
class Token:
    value: str
    normalized_span: tuple
    raw_byte_intervals: tuple
    raw_scalar_intervals: tuple
    raw_byte_span: tuple | None


def _intervals(indices,offsets):
    result=[]
    for i in sorted(indices):
        interval=(offsets[i],offsets[i+1])
        if result and result[-1][1]==interval[0]:
            result[-1]=(result[-1][0],interval[1])
        else:
            result.append(interval)
    return tuple(result)


def normalize_tokens(value):
    raw=strict_text(value)
    byte_offsets=[0]
    for char in raw:
        byte_offsets.append(byte_offsets[-1]+len(char.encode('utf-8')))
    items=_nfc_with_origins([(c,frozenset({i})) for i,c in enumerate(raw)])
    folded=[(c,origin) for char,origin in items for c in FOLD.get(char,char)]
    items=_nfc_with_origins(folded)
    lookalikes={'\u2018':"'",'\u2019':"'",'\u2010':'-','\u2011':'-'}
    items=[(lookalikes.get(c,c),origin) for c,origin in items]
    normalized=''.join(c for c,_ in items)
    def word(c):
        return ud.category(c)[0] in 'LMN'
    tokens=[];i=0
    while i<len(items):
        c=items[i][0];start=i
        if word(c):
            i+=1
            while i<len(items):
                char=items[i][0]
                if word(char) or (char in "'-" and i+1<len(items) and
                                 word(items[i-1][0]) and word(items[i+1][0])):
                    i+=1
                else:
                    break
        elif c in WHITE or (ud.category(c)[0]=='P' and c not in '-%'):
            i+=1
            continue
        else:
            i+=1
        origins=frozenset().union(*(origin for _,origin in items[start:i]))
        intervals=_intervals(origins,byte_offsets)
        scalar_intervals=_intervals(origins,list(range(len(raw)+1)))
        unique=(len(intervals)==1 and not any(origin&origins for _,origin in items[:start]+items[i:]))
        tokens.append(Token(normalized[start:i],(start,i),intervals,scalar_intervals,
                            intervals[0] if unique else None))
    return normalized,tuple(tokens)


def lexical(value):
    return tuple(token.value for token in normalize_tokens(value)[1])
