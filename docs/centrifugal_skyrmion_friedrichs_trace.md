# Local Friedrichs-Admissible Origin Trace

The exact indicial theorem gives four homogeneous powers for the centrifugal
two-channel weak form:

```text
p in {1,3,-2,-4}.
```

This note classifies which solution germs have finite local quadratic-form
energy and attaches the admissible germs to the certified physical endpoint
tubes.

## Energy Scaling

The regular weak-form blocks obey

```text
C=Cbar(x^2),  M=x Mbar(x^2),  P=x^2 Pbar(x^2).
```

For a solution branch

```text
y=x^p(v+O(x^2)),
```

the density therefore has the form

```text
H[y]=Q_p(b)x^(2p)+O(x^(2p+2)).
```

The audit inserts an exact nullvector of the indicial pencil for each power
and computes `Q_p(b)` as a polynomial in the origin slope. Every `Q_p` is a
strictly positive even polynomial for all real slopes. Hence no leading
branch coefficient is accidentally null in the quadratic form.

The local energy integral is finite exactly when

```text
integral_0^epsilon x^(2p) dx < infinity
iff p > -1/2.
```

Consequently

```text
finite energy: p=1,3,
excluded:      p=-2,-4.
```

If a `p=-4` coefficient is nonzero, its positive `x^-8` square is the first
singular term and cannot be cancelled by cross terms with `p=-2`. Once the
`p=-4` coefficient vanishes, a nonzero `p=-2` coefficient has a positive
`x^-4` square. Thus a mixed singular solution cannot evade the classification.

## Trace Space

Within the local solution-germ space, the finite-energy homogeneous trace is
two-dimensional and is spanned by the `p=1` and `p=3` columns. The rotational
forced particular column begins at `p=3` and is also finite energy. The
admissible affine germ is therefore

```text
alpha y_(p=1)+beta y_(p=3)+sigma y_(forced,p=3).
```

The physical transfer certificate maps exactly these columns to direct
`(f,g,f',g')` tubes at `x=1/16`.

## Reproduce

```bash
PYTHONPATH=. python experiments/centrifugal_skyrmion_friedrichs_trace_audit.py
python -m pytest -q tests/test_centrifugal_skyrmion_friedrichs_trace.py tests/test_centrifugal_skyrmion_friedrichs_trace_audit.py
```

## Claim Boundary

This theorem classifies local solution germs of the symmetric weak-form
equation. It does not classify the entire form domain, prove global
semiboundedness, or by itself construct the global Friedrichs realization.
