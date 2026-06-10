# Finite Clock Crossed-Product Gate

Status: exact finite order-of-limits obstruction implemented

Every automorphism of a finite matrix algebra `M_d` is inner. For a cyclic
clock group `Z_q` acting by `alpha_g=Ad(U_g)`, the elements

```text
W_g = U_g^* lambda_g
```

commute with `M_d` and generate the group algebra. Therefore

```text
M_d crossed_alpha Z_q
  isomorphic to M_d tensor C*(Z_q)
  isomorphic to direct_sum_{r=1}^q M_d.
```

For `q>1` the center has dimension `q`. At every finite cutoff this is a finite
Type-I algebra, not a Type-II factor.

Adjoining a finite clock to a finite fuzzy-sphere or finite Fock-space matrix
algebra therefore cannot derive the gravitational Type-II observer algebra. A
large matrix dimension, a normalized trace, or a clock label is insufficient.

The required order of work is:

1. construct a many-body or local-QFT regulator whose limiting local algebra is
   not Type I;
2. prove convergence of the state and modular dynamics;
3. show that modular flow becomes outer in the limit;
4. form the clock crossed product at the limiting or jointly controlled level;
5. derive the semifinite trace and compare it with generalized entropy.

The theorem does not say that a sequence of finite algebras cannot converge to
a Type-II or Type-III algebra under suitable embeddings. It says that the type
does not follow from performing an inner finite crossed product at each cutoff.

Reproduce with:

```bash
PYTHONPATH=. python3 -m qgtoy finite-clock-crossed-product --max-level 8
PYTHONPATH=. python3 -m unittest tests.test_finite_clock_crossed_product
```
