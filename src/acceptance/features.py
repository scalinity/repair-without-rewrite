"""NONSCIENTIFIC source-to-proposal features; no reference interface."""
import hashlib
import math
from src.scoring.text import lexical, strict_text
from .records import FeatureRecord


def raw_bytes(text):
    return strict_text(text).encode("utf-8", "strict")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def edit_counts(source, proposal):
    """Unit-cost prefix DP, terminal traceback: match, substitute, delete, insert."""
    table = [list(range(len(proposal) + 1))]
    for i, a in enumerate(source, 1):
        row = [i]
        for j, b in enumerate(proposal, 1):
            row.append(min(table[-1][j] + 1, row[j-1] + 1,
                           table[-1][j-1] + (a != b)))
        table.append(row)
    i, j = len(source), len(proposal)
    insertions = deletions = substitutions = 0
    while i or j:
        here = table[i][j]
        if i and j and source[i-1] == proposal[j-1] and here == table[i-1][j-1]:
            i -= 1; j -= 1
        elif i and j and here == table[i-1][j-1] + 1:
            substitutions += 1; i -= 1; j -= 1
        elif i and here == table[i-1][j] + 1:
            deletions += 1; i -= 1
        else:
            insertions += 1; j -= 1
    return insertions, deletions, substitutions


def distance(source, proposal):
    row = list(range(len(proposal) + 1))
    for i, a in enumerate(source, 1):
        nxt = [i]
        for j, b in enumerate(proposal, 1):
            nxt.append(min(nxt[j-1]+1, row[j]+1, row[j-1]+(a != b)))
        row = nxt
    return row[-1]


def structural_features(source, proposal):
    sb, ob = raw_bytes(source), raw_bytes(proposal)
    s, o = lexical(sb), lexical(ob)
    ins, delete, sub = edit_counts(s, o)
    values = (math.log1p(len(s)), math.log1p(len(o)), math.log1p(len(sb)),
              math.log1p(len(ob)), ins/max(1, len(s)), delete/max(1, len(s)),
              sub/max(1, len(s)), distance(sb, ob)/max(1, len(sb)))
    return FeatureRecord(digest(sb), digest(ob), len(sb), len(ob), values)
