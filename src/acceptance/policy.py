"""NONSCIENTIFIC fixed ridge mathematics, independently supplied artificial FIT."""
import numpy as np
from .records import FitRecord, Normalizer, Policy, FEATURE_ORDER, width


class NumericalFailure(ValueError):
    pass


def fit_support(records: tuple[FitRecord, ...]):
    valid = [r for r in records if r.valid and r.changed]
    beneficial = [r for r in valid if r.beneficial]
    return len(valid) >= 200 and len(beneficial) >= 40 and len({r.group for r in beneficial}) >= 20


def _matrix(values, n):
    try:
        supplied = np.asarray(values)
        if supplied.dtype.kind not in "fiu":
            raise ValueError("numeric values required; no string/bool coercion")
        result = supplied.astype(np.float64)
    except (ValueError, TypeError, OverflowError) as exc: raise NumericalFailure("malformed features") from exc
    if result.ndim != 2 or result.shape[1] != n or result.shape[0] == 0 or not np.isfinite(result).all():
        raise NumericalFailure("nonempty finite feature matrix required")
    return result


def transform(normalizer: Normalizer, values):
    normalizer.__post_init__()
    matrix = _matrix(values, width(normalizer.form))
    means = np.asarray(normalizer.means, dtype=np.float64)
    sd = np.asarray(normalizer.standard_deviations, dtype=np.float64)
    result = np.zeros_like(matrix)
    variable = sd != 0
    with np.errstate(over="raise", invalid="raise", divide="raise"):
        try: result[:, variable] = (matrix[:, variable]-means[variable])/sd[variable]
        except FloatingPointError as exc: raise NumericalFailure("normalization failed") from exc
    return result


def fit_policy(records: tuple[FitRecord, ...], form):
    """Synthetic solver tests are mathematical fixtures, not population admission."""
    n = width(form)
    if not records: raise NumericalFailure("empty FIT")
    for row in records:
        row.__post_init__()
        if not row.valid or not row.changed: raise ValueError("FIT must be valid and lexically changed")
    x = _matrix([r.values for r in records], n)
    y = np.asarray([r.completed_repair_lower - 4*r.introduced_error_upper for r in records], dtype=np.float64)
    with np.errstate(over="raise", invalid="raise", divide="raise"):
        try:
            means = np.mean(x, axis=0)
            sd = np.sqrt(np.mean((x-means)**2, axis=0))
            constant = np.all(x == x[0], axis=0)
            if np.any((~constant) & (sd == 0)):
                raise FloatingPointError("nonconstant FIT standard deviation collapsed to zero")
            means[constant] = x[0, constant]
            sd[constant] = 0
            normalizer = Normalizer(form, tuple(float(v) for v in means),
                tuple(float(v) for v in sd), len(records), FEATURE_ORDER[:n])
            z = transform(normalizer, x)
            design = np.column_stack((np.ones(len(records), dtype=np.float64), z))
            penalty = np.diag([0.0] + [0.01*len(records)]*n)
            beta = np.linalg.solve(design.T@design + penalty, design.T@y)
        except (np.linalg.LinAlgError, FloatingPointError, ValueError) as exc:
            raise NumericalFailure("fixed ridge arithmetic failed; no rescue") from exc
    if not np.isfinite(beta).all(): raise NumericalFailure("nonfinite coefficients")
    return Policy(form, normalizer, float(beta[0]), tuple(float(v) for v in beta[1:]))


def predict(policy: Policy, values):
    policy.__post_init__()
    with np.errstate(over="raise", invalid="raise"):
        try: result = policy.intercept + transform(policy.normalizer, values) @ np.asarray(policy.coefficients, dtype=np.float64)
        except FloatingPointError as exc: raise NumericalFailure("prediction failed") from exc
    if not np.isfinite(result).all(): raise NumericalFailure("nonfinite predictions")
    return tuple(float(v) for v in result)
