"""Exact state-sensitive transfer of a certified Paper-R response interval.

The module has two deliberately separate jobs:

* verify the spin-two cat and second-order-anticoherent state data with exact
  finite-dimensional algebra; and
* transfer a directed interval for the leading exterior amplitude ``A_ext``
  to the normalized annular Weyl coefficient and the two state footprints.

All public interval endpoints are exact :class:`fractions.Fraction` values.
The result is conditional on the supplied amplitude interval: the cat-state
footprint is certified nonzero exactly when that interval excludes zero.  No
finite-rotation remainder, self-gravity, detector dynamics, or Israel
matching is inferred.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .validated_interval import RationalInterval, sqrt_fraction_interval


ExactMatrix3 = tuple[tuple[Fraction, Fraction, Fraction], ...]


def _reduce_radicand(value: int) -> tuple[int, int]:
    """Return ``(outside, square_free)`` for ``sqrt(value)``."""
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError("radicand must be a positive integer")
    outside = 1
    square_free = 1
    remainder = value
    divisor = 2
    while divisor * divisor <= remainder:
        exponent = 0
        while remainder % divisor == 0:
            remainder //= divisor
            exponent += 1
        outside *= divisor ** (exponent // 2)
        if exponent % 2:
            square_free *= divisor
        divisor += 1
    if remainder > 1:
        square_free *= remainder
    return outside, square_free


@dataclass(frozen=True)
class _Radical:
    """A finite exact sum ``sum coefficient[r] sqrt(r)``."""

    terms: tuple[tuple[int, Fraction], ...]

    @classmethod
    def from_mapping(cls, values: dict[int, Fraction]) -> _Radical:
        reduced: dict[int, Fraction] = {}
        for radicand, coefficient in values.items():
            if not coefficient:
                continue
            outside, square_free = _reduce_radicand(radicand)
            reduced[square_free] = (
                reduced.get(square_free, Fraction(0)) + coefficient * outside
            )
        return cls(
            tuple(
                (radicand, coefficient)
                for radicand, coefficient in sorted(reduced.items())
                if coefficient
            )
        )

    @classmethod
    def rational(cls, value: int | Fraction) -> _Radical:
        return cls.from_mapping({1: Fraction(value)})

    @classmethod
    def square_root(cls, value: int) -> _Radical:
        return cls.from_mapping({value: Fraction(1)})

    def __add__(self, other: _Radical) -> _Radical:
        values = dict(self.terms)
        for radicand, coefficient in other.terms:
            values[radicand] = values.get(radicand, Fraction(0)) + coefficient
        return _Radical.from_mapping(values)

    def __neg__(self) -> _Radical:
        return _Radical(tuple((radicand, -value) for radicand, value in self.terms))

    def __sub__(self, other: _Radical) -> _Radical:
        return self + (-other)

    def __mul__(self, other: _Radical) -> _Radical:
        values: dict[int, Fraction] = {}
        for left_radicand, left_coefficient in self.terms:
            for right_radicand, right_coefficient in other.terms:
                radicand = left_radicand * right_radicand
                values[radicand] = (
                    values.get(radicand, Fraction(0))
                    + left_coefficient * right_coefficient
                )
        return _Radical.from_mapping(values)

    def scale(self, value: int | Fraction) -> _Radical:
        factor = Fraction(value)
        return _Radical(
            tuple(
                (radicand, factor * coefficient) for radicand, coefficient in self.terms
            )
        )

    def as_fraction(self) -> Fraction:
        if not self.terms:
            return Fraction(0)
        if len(self.terms) != 1 or self.terms[0][0] != 1:
            raise AssertionError(f"expected a rational value, got {self.terms!r}")
        return self.terms[0][1]


_RADICAL_ZERO = _Radical(())


@dataclass(frozen=True)
class _ComplexRadical:
    real: _Radical
    imaginary: _Radical

    @classmethod
    def rational(cls, value: int | Fraction) -> _ComplexRadical:
        return cls(_Radical.rational(value), _RADICAL_ZERO)

    def __add__(self, other: _ComplexRadical) -> _ComplexRadical:
        return _ComplexRadical(
            self.real + other.real,
            self.imaginary + other.imaginary,
        )

    def __neg__(self) -> _ComplexRadical:
        return _ComplexRadical(-self.real, -self.imaginary)

    def __sub__(self, other: _ComplexRadical) -> _ComplexRadical:
        return self + (-other)

    def __mul__(self, other: _ComplexRadical) -> _ComplexRadical:
        return _ComplexRadical(
            self.real * other.real - self.imaginary * other.imaginary,
            self.real * other.imaginary + self.imaginary * other.real,
        )

    def scale(self, value: int | Fraction) -> _ComplexRadical:
        return _ComplexRadical(
            self.real.scale(value),
            self.imaginary.scale(value),
        )

    def conjugate(self) -> _ComplexRadical:
        return _ComplexRadical(self.real, -self.imaginary)


_COMPLEX_ZERO = _ComplexRadical(_RADICAL_ZERO, _RADICAL_ZERO)
_ComplexMatrix = tuple[tuple[_ComplexRadical, ...], ...]
_ExactState = tuple[_ComplexRadical, ...]


def _matrix_add(left: _ComplexMatrix, right: _ComplexMatrix) -> _ComplexMatrix:
    return tuple(
        tuple(left[row][column] + right[row][column] for column in range(5))
        for row in range(5)
    )


def _matrix_scale(matrix: _ComplexMatrix, scalar: _ComplexRadical) -> _ComplexMatrix:
    return tuple(
        tuple(matrix[row][column] * scalar for column in range(5)) for row in range(5)
    )


def _matrix_multiply(left: _ComplexMatrix, right: _ComplexMatrix) -> _ComplexMatrix:
    return tuple(
        tuple(
            sum(
                (left[row][index] * right[index][column] for index in range(5)),
                start=_COMPLEX_ZERO,
            )
            for column in range(5)
        )
        for row in range(5)
    )


def _expectation(state: _ExactState, operator: _ComplexMatrix) -> Fraction:
    value = sum(
        (
            state[row].conjugate() * operator[row][column] * state[column]
            for row in range(5)
            for column in range(5)
        ),
        start=_COMPLEX_ZERO,
    )
    if value.imaginary != _RADICAL_ZERO:
        raise AssertionError(f"Hermitian expectation is not real: {value!r}")
    return value.real.as_fraction()


def _spin_two_generators() -> tuple[_ComplexMatrix, _ComplexMatrix, _ComplexMatrix]:
    basis = (2, 1, 0, -1, -2)
    index_by_m = {value: index for index, value in enumerate(basis)}
    raising = [[_COMPLEX_ZERO for _ in range(5)] for _ in range(5)]
    for column, magnetic in enumerate(basis):
        if magnetic == 2:
            continue
        coefficient = _Radical.square_root(6 - magnetic * (magnetic + 1))
        row = index_by_m[magnetic + 1]
        raising[row][column] = _ComplexRadical(coefficient, _RADICAL_ZERO)
    j_plus = tuple(tuple(row) for row in raising)
    j_minus = tuple(
        tuple(j_plus[column][row].conjugate() for column in range(5))
        for row in range(5)
    )
    half = _ComplexRadical.rational(Fraction(1, 2))
    minus_i_half = _ComplexRadical(_RADICAL_ZERO, _Radical.rational(Fraction(-1, 2)))
    j_x = _matrix_scale(_matrix_add(j_plus, j_minus), half)
    j_y = _matrix_scale(
        _matrix_add(j_plus, _matrix_scale(j_minus, _ComplexRadical.rational(-1))),
        minus_i_half,
    )
    j_z = tuple(
        tuple(
            _ComplexRadical.rational(basis[row]) if row == column else _COMPLEX_ZERO
            for column in range(5)
        )
        for row in range(5)
    )
    return j_x, j_y, j_z


def _identity_matrix() -> _ComplexMatrix:
    return tuple(
        tuple(
            _ComplexRadical.rational(1) if row == column else _COMPLEX_ZERO
            for column in range(5)
        )
        for row in range(5)
    )


def _state_second_moment(
    state: _ExactState,
) -> tuple[Fraction, ExactMatrix3, Fraction]:
    normalization = _expectation(state, _identity_matrix())
    generators = _spin_two_generators()
    second_rows: list[tuple[Fraction, Fraction, Fraction]] = []
    for left in generators:
        entries: list[Fraction] = []
        for right in generators:
            symmetrized = _matrix_scale(
                _matrix_add(
                    _matrix_multiply(left, right),
                    _matrix_multiply(right, left),
                ),
                _ComplexRadical.rational(Fraction(1, 2)),
            )
            entries.append(_expectation(state, symmetrized))
        second_rows.append(tuple(entries))
    second = tuple(second_rows)
    casimir = sum(second[index][index] for index in range(3))
    return normalization, second, casimir


@dataclass(frozen=True)
class ExactSpinTwoStateData:
    name: str
    normalization: Fraction
    casimir: Fraction
    leading_rotor_energy_coefficient: Fraction
    quadrupole_qj: ExactMatrix3
    quadrupole_frobenius_norm_squared: Fraction
    quadrupole_frobenius_norm_symbolic: str


def _spin_two_state_data(name: str, state: _ExactState) -> ExactSpinTwoStateData:
    normalization, second, casimir = _state_second_moment(state)
    quadrupole = tuple(
        tuple(
            second[row][column] - (casimir / 3 if row == column else Fraction(0))
            for column in range(3)
        )
        for row in range(3)
    )
    norm_squared = sum(value * value for row in quadrupole for value in row)
    norm_symbolic = "0" if norm_squared == 0 else f"sqrt({norm_squared})"
    return ExactSpinTwoStateData(
        name=name,
        normalization=normalization,
        casimir=casimir,
        leading_rotor_energy_coefficient=casimir / 2,
        quadrupole_qj=quadrupole,
        quadrupole_frobenius_norm_squared=norm_squared,
        quadrupole_frobenius_norm_symbolic=norm_symbolic,
    )


def exact_spin_two_state_data() -> tuple[ExactSpinTwoStateData, ExactSpinTwoStateData]:
    """Return exact algebraic records for the Paper-R spin-two states.

    The leading rotor energy is the returned coefficient divided by the
    common physical inertia, namely ``E_rot=coefficient/I``.
    """
    inverse_sqrt_two = _Radical.square_root(2).scale(Fraction(1, 2))
    zero = _COMPLEX_ZERO
    cat_state = (
        _ComplexRadical(inverse_sqrt_two, _RADICAL_ZERO),
        zero,
        zero,
        zero,
        _ComplexRadical(inverse_sqrt_two, _RADICAL_ZERO),
    )
    anticoherent_state = (
        _ComplexRadical.rational(Fraction(1, 2)),
        zero,
        _ComplexRadical(_RADICAL_ZERO, inverse_sqrt_two),
        zero,
        _ComplexRadical.rational(Fraction(1, 2)),
    )
    return (
        _spin_two_state_data("spin_two_cat", cat_state),
        _spin_two_state_data("spin_two_anticoherent_T", anticoherent_state),
    )


@dataclass(frozen=True)
class PaperRStateTransferCertificate:
    exterior_amplitude: RationalInterval
    exterior_amplitude_excludes_zero: bool
    exterior_amplitude_sign: int
    annular_rms_factor: Fraction
    unit_tensor_weyl_footprint: RationalInterval
    cat_weyl_footprint: RationalInterval
    cat_weyl_footprint_squared: RationalInterval
    anticoherent_weyl_footprint: RationalInterval
    equal_casimir_and_leading_energy: bool
    cat_quadrupole_nonzero: bool
    anticoherent_quadrupole_zero: bool
    state_sensitive_nonzero_conclusion: bool
    conclusion: str
    claim_scope: str


def certify_paper_r_state_transfer(
    *,
    exterior_amplitude: RationalInterval,
    annular_rms_factor: Fraction = Fraction(25, 2),
    sqrt_bisection_steps: int = 160,
) -> PaperRStateTransferCertificate:
    """Transfer a certified ``A_ext`` interval to the two spin-state footprints.

    ``annular_rms_factor=25/2`` is the exact Paper-R value for ``R=20`` and
    ``5<=x<=10``.  The unit-tensor footprint is
    ``B_W=(25/2)|A_ext|``.  The cat footprint has the additional exact state
    factor ``||QJ_cat||_F=sqrt(6)``, while the anticoherent leading
    quadrupolar footprint is identically zero.
    """
    if not isinstance(exterior_amplitude, RationalInterval):
        raise TypeError("exterior_amplitude must be a RationalInterval")
    if not isinstance(annular_rms_factor, Fraction):
        raise TypeError("annular_rms_factor must be an exact Fraction")
    if annular_rms_factor <= 0:
        raise ValueError("annular_rms_factor must be positive")

    excludes_zero = not exterior_amplitude.contains_zero()
    sign = (
        1 if exterior_amplitude.lower > 0 else -1 if exterior_amplitude.upper < 0 else 0
    )
    absolute_lower = (
        min(abs(exterior_amplitude.lower), abs(exterior_amplitude.upper))
        if excludes_zero
        else Fraction(0)
    )
    absolute_upper = max(abs(exterior_amplitude.lower), abs(exterior_amplitude.upper))
    unit_footprint = RationalInterval(
        annular_rms_factor * absolute_lower,
        annular_rms_factor * absolute_upper,
    )

    cat, anticoherent = exact_spin_two_state_data()
    equal_energy = (
        cat.normalization == anticoherent.normalization == 1
        and cat.casimir == anticoherent.casimir
        and cat.leading_rotor_energy_coefficient
        == anticoherent.leading_rotor_energy_coefficient
    )
    cat_nonzero = cat.quadrupole_frobenius_norm_squared > 0
    anticoherent_zero = anticoherent.quadrupole_frobenius_norm_squared == 0
    sqrt_cat_norm = sqrt_fraction_interval(
        cat.quadrupole_frobenius_norm_squared,
        bisection_steps=sqrt_bisection_steps,
    )
    cat_footprint = unit_footprint * sqrt_cat_norm
    cat_footprint_squared = unit_footprint.power(2).scale(
        cat.quadrupole_frobenius_norm_squared
    )
    zero_interval = RationalInterval.point(0)
    conclusion_holds = (
        excludes_zero and equal_energy and cat_nonzero and anticoherent_zero
    )
    conclusion = (
        "certified: equal-leading-energy states have nonzero versus zero "
        "leading mean Weyl footprints"
        if conclusion_holds
        else "not certified: the supplied exterior-amplitude interval does not "
        "establish a nonzero cat-state footprint"
    )
    return PaperRStateTransferCertificate(
        exterior_amplitude=exterior_amplitude,
        exterior_amplitude_excludes_zero=excludes_zero,
        exterior_amplitude_sign=sign,
        annular_rms_factor=annular_rms_factor,
        unit_tensor_weyl_footprint=unit_footprint,
        cat_weyl_footprint=cat_footprint,
        cat_weyl_footprint_squared=cat_footprint_squared,
        anticoherent_weyl_footprint=zero_interval,
        equal_casimir_and_leading_energy=equal_energy,
        cat_quadrupole_nonzero=cat_nonzero,
        anticoherent_quadrupole_zero=anticoherent_zero,
        state_sensitive_nonzero_conclusion=conclusion_holds,
        conclusion=conclusion,
        claim_scope=(
            "Leading O(Omega^2) semiclassical mean electric-Weyl coefficient "
            "on the fixed de Sitter background only; no finite-Omega "
            "remainder, self-gravity, detector dynamics, fluctuations, or "
            "tensorial Israel matching."
        ),
    )
