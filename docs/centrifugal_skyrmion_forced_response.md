# Nonzero Centrifugal Weak Response

Status: exact nonzero-response theorem for the declared fixed-background weak
matter model.

## Source Theorem

Let `b=-F'(0)` be the authenticated shooting slope. In the regular source
kernels, the tangential coordinate coefficient has the origin expansion

```text
s_g(x)=c(b)x^3+O(x^5),
c(b)=b(4b^2-1)/30.
```

The authenticated interval is

```text
546684696508091/347185136818875
<= b <=
550388004634159/347185136818875.
```

It lies strictly above `1/2`, and monotonicity of `c` on that interval gives

```text
c(b) >=
587641827616063254469055059652310004726318409
/
1255465053148813676361431823453150360410156250
> 0.4680670530.
```

Thus the rotational source functional is not zero. Its derivative coefficient
is `O(x^4)` at the origin and contains `sin(F)^2`, so it vanishes both at the
origin and at the `F(a)=0` wall. Exact integration by parts introduces no
endpoint load and gives

```text
s=s_0-s_1' in L2.
```

The source is therefore also a continuous element of the form dual `V*`, and
the certified `L2` inverse constant applies directly.

## Response Theorem

Let `q` be the closed coercive form from the global Friedrichs theorem and
let `ell` be this source. Lax-Milgram gives a unique `y in V` such that

```text
q(y,z)=ell(z)  for every z in V.
```

Since `ell` is nonzero, `y` is nonzero. Testing with `z=y` gives the strict
source-conjugate susceptibility statement

```text
chi_rot = ell(y)=q(y)>0.
```

This is a nonperturbative sign statement within the linear forced problem; it
does not depend on the floating finite-difference solution.

## Evidence And Boundary

The source-hashed artifact is
`experiments/centrifugal_skyrmion_forced_response_certificate.json`, SHA256
`9edc2bc479534fab3f527ce535a373da1373b45085c6fbf4602f4ee9cdd32db7`.

The theorem proves a nonzero matter deformation and positive conjugate
susceptibility, but not a numerical field norm or a nonzero off-wall
Zerilli/electric-Weyl functional. The latter still needs a quantitative
primal-adjoint residual enclosure and an observable interval excluding zero.
