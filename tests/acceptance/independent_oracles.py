"""NONSCIENTIFIC separate expected-result paths. No production imports."""
from functools import lru_cache
from fractions import Fraction
import hashlib
import json
import math


def tiny_alignments(source, proposal):
    """Exhaustively enumerate paths; terminal-priority sequence determines witness."""
    paths = []
    def visit(i, j, operations, cost):
        if i == len(source) and j == len(proposal):
            paths.append((cost, tuple(reversed(operations)), operations))
            return
        if i < len(source) and j < len(proposal):
            match = source[i] == proposal[j]
            visit(i+1, j+1, operations+(0 if match else 1,), cost+(not match))
        if i < len(source): visit(i+1, j, operations+(2,), cost+1)
        if j < len(proposal): visit(i, j+1, operations+(3,), cost+1)
    visit(0, 0, (), 0)
    cost, _, operations = min(paths)
    return operations.count(3), operations.count(2), operations.count(1), cost


def recursive_distance(source, proposal):
    @lru_cache(None)
    def visit(i, j):
        if i == len(source): return len(proposal)-j
        if j == len(proposal): return len(source)-i
        return min(1+visit(i+1,j), 1+visit(i,j+1),
                   (source[i] != proposal[j])+visit(i+1,j+1))
    return visit(0, 0)


def rational_standard_deviation(variance):
    """Keep exact zero separate from a positive variance lost by float conversion."""
    if variance == 0:
        return Fraction(0)
    numerator, denominator = math.isqrt(variance.numerator), math.isqrt(variance.denominator)
    if numerator**2 == variance.numerator and denominator**2 == variance.denominator:
        return Fraction(numerator, denominator)
    converted = float(variance)
    if converted == 0:
        raise ArithmeticError("positive exact variance cannot use a collapsed float square root")
    return math.sqrt(converted)


def rational_ridge(matrix, utilities):
    """Exact Fraction Gaussian elimination; no NumPy or production normalizer."""
    n, p = len(matrix), len(matrix[0])
    columns = list(zip(*matrix))
    means = [sum(map(Fraction, c))/n for c in columns]
    variances = [sum((Fraction(v)-m)**2 for v in c)/n for c,m in zip(columns,means)]
    # Solve in centered original units: standardized penalty translates to variance.
    x = [[Fraction(1), *(Fraction(v)-m for v,m in zip(row, means))] for row in matrix]
    a = [[sum(row[i]*row[j] for row in x)+(Fraction(n,100)*variances[i-1] if i==j and i>0 else 0)
          for j in range(p+1)] for i in range(p+1)]
    b = [sum(row[i]*Fraction(y) for row,y in zip(x,utilities)) for i in range(p+1)]
    # Omit mathematically constant columns; their standardized coefficients are zero.
    keep = [0]+[i+1 for i,v in enumerate(variances) if v]
    rows = [[a[i][j] for j in keep]+[b[i]] for i in keep]
    for k in range(len(keep)):
        pivot = next(i for i in range(k,len(keep)) if rows[i][k])
        rows[k],rows[pivot] = rows[pivot],rows[k]
        divisor = rows[k][k]; rows[k] = [v/divisor for v in rows[k]]
        for i in range(len(keep)):
            if i != k:
                factor = rows[i][k]; rows[i] = [v-factor*w for v,w in zip(rows[i],rows[k])]
    coefficients = [Fraction(0)]*(p+1)
    for index,row in zip(keep,rows): coefficients[index] = row[-1]
    deviations = [rational_standard_deviation(v) for v in variances]
    standard = [float(coefficients[i+1]*sd) if isinstance(sd, Fraction) else float(coefficients[i+1])*sd
                for i,sd in enumerate(deviations)]
    return tuple(float(m) for m in means), tuple(float(sd) for sd in deviations), float(coefficients[0]), tuple(standard)


def identity_bytes(path):
    # Independent literal namespace, built without production serializer/constants.
    escaped = path.replace(chr(92), chr(92)*2).replace('"', chr(92)+'"')
    return ('["RWR_CV26_BRITISH_CASE_V1","cmrt6zrob000zmm07yqwjlpwi",'
            '"cv-corpus-26.0-2026-06-12","en","' + escaped + '"]').encode("utf-8")


def independent_component(members):
    payload = b"RWR_CV26_BRITISH_COMPONENT_V1\n" + b"\n".join(x.encode() for x in sorted(members))
    return hashlib.sha256(payload).hexdigest()


def graph_components(ids, edges):
    """Set expansion, separate from production union-find."""
    remaining = set(ids); groups = []
    while remaining:
        group = {min(remaining)}
        while True:
            expanded = group | {v for a,b in edges if a in group or b in group for v in (a,b)}
            if expanded == group: break
            group = expanded
        remaining -= group; groups.append(tuple(sorted(group)))
    return sorted(groups)


def independent_allocation(groups, eligible, excluded):
    pools = {"FIT":[], "SELECT":[], "EVAL":[]}; owner = {}
    for members in groups:
        if set(members) & set(excluded): continue
        component = independent_component(members)
        remainder = int(hashlib.sha256(("POST_FEASIBILITY_ACCEPTANCE_V1|"+component).encode()).hexdigest(),16)%6
        role = "FIT" if remainder in (0,1) else "SELECT" if remainder==2 else "EVAL"
        rank = lambda m: hashlib.sha256(("POST_FEASIBILITY_CASE_V1|"+m).encode()).hexdigest()
        admitted = sorted(set(members)&set(eligible),key=rank)[:60]
        pools[role].extend(admitted); owner.update({m:component for m in admitted})
    result = {}
    for role,quota,minimum in (("FIT",4000,80),("SELECT",2000,40),("EVAL",6000,100)):
        candidates = sorted(pools[role],key=lambda m:hashlib.sha256(("POST_FEASIBILITY_CASE_V1|"+m).encode()).hexdigest())
        selected = tuple(candidates[:quota]); count = len({owner[m] for m in selected})
        result[role] = selected,count,len(candidates),len(selected)==quota and count>=minimum
    return result


def independent_select(rows):
    result = []
    for threshold in (0,.25,.5,1,2,4):
        taken = [r for r in rows if r.eligible_proposal and r.predicted_utility>threshold]
        errors = sum(r.proposal_errors if r in taken else r.raw_errors for r in rows)
        repairs = sum(r.completed_repair_lower for r in taken)
        intro = sum(r.introduced_error_upper for r in taken)
        support = len({r.group for r in taken if r.completed_repair_lower})
        zero = sum(r.raw_errors==0 for r in rows)
        damaged = sum(r.raw_errors==0 and r.proposal_errors>0 for r in taken)
        if zero and errors < sum(r.raw_errors for r in rows) and repairs>=10 and support>=5 and Fraction(intro)<=Fraction(repairs,4) and Fraction(damaged,zero)<=Fraction(1,200):
            result.append((repairs-4*intro,threshold))
    return max(result)[1] if result else None
