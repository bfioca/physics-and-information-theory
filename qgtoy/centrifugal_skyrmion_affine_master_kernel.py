"""Generic-scalar affine completed-stress and bulk master-source kernels.

The floating response code differentiates sampled energy densities.  This
module instead propagates a first radial jet through the exact same-action
stress algebra.  It therefore exposes the pointwise affine maps

``T = T_rigid + L0 (f,g) + L1 (f',g')``

and

``F = F_rigid + b_f f + b_fp f' + b_fpp f'' + b_g g + b_gp g'``

without finite differences.  Transcendental evaluation is intentionally left
to the caller: supplying ``sin(F)`` and ``cos(F)`` makes the arithmetic usable
with floats, exact rational intervals, and centered Taylor models.

The moving-wall part uses a caller-supplied square root of the wall lapse and
Green weight.  This keeps transcendental and square-root enclosure policy out
of the algebra while still supporting floats, exact rationals, intervals, and
Taylor models.

This is a local algebraic kernel.  It does not validate the profile enclosure,
the radial integral, the origin limit, or any continuum residual bound.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar


Scalar = TypeVar("Scalar")


@dataclass(frozen=True)
class StressAmplitudes(Generic[Scalar]):
    """The five static-even quadrupole stress amplitudes."""

    energy_density: Scalar
    radial_pressure: Scalar
    tangential_pressure: Scalar
    radial_angular_shear: Scalar
    angular_tracefree_stress: Scalar

    def __add__(self, other: StressAmplitudes[Scalar]) -> StressAmplitudes[Scalar]:
        return StressAmplitudes(
            self.energy_density + other.energy_density,  # type: ignore[operator]
            self.radial_pressure + other.radial_pressure,  # type: ignore[operator]
            self.tangential_pressure + other.tangential_pressure,  # type: ignore[operator]
            self.radial_angular_shear + other.radial_angular_shear,  # type: ignore[operator]
            self.angular_tracefree_stress
            + other.angular_tracefree_stress,  # type: ignore[operator]
        )

    def scale(self, factor: Scalar) -> StressAmplitudes[Scalar]:
        return StressAmplitudes(
            self.energy_density * factor,  # type: ignore[operator]
            self.radial_pressure * factor,  # type: ignore[operator]
            self.tangential_pressure * factor,  # type: ignore[operator]
            self.radial_angular_shear * factor,  # type: ignore[operator]
            self.angular_tracefree_stress * factor,  # type: ignore[operator]
        )


@dataclass(frozen=True)
class CompletedStress(Generic[Scalar]):
    """Rigid, deformation, and total stress amplitudes."""

    rigid: StressAmplitudes[Scalar]
    deformation: StressAmplitudes[Scalar]
    total: StressAmplitudes[Scalar]


@dataclass(frozen=True)
class _FirstRadialJet(Generic[Scalar]):
    value: Scalar
    derivative: Scalar

    @classmethod
    def constant(cls, value: Scalar) -> _FirstRadialJet[Scalar]:
        return cls(value, value - value)  # type: ignore[operator]

    def _coerce(self, other: _FirstRadialJet[Scalar] | Scalar) -> _FirstRadialJet[Scalar]:
        return other if isinstance(other, _FirstRadialJet) else self.constant(other)

    def __add__(
        self, other: _FirstRadialJet[Scalar] | Scalar
    ) -> _FirstRadialJet[Scalar]:
        right = self._coerce(other)
        return _FirstRadialJet(
            self.value + right.value,  # type: ignore[operator]
            self.derivative + right.derivative,  # type: ignore[operator]
        )

    __radd__ = __add__

    def __neg__(self) -> _FirstRadialJet[Scalar]:
        return _FirstRadialJet(-self.value, -self.derivative)  # type: ignore[operator]

    def __sub__(
        self, other: _FirstRadialJet[Scalar] | Scalar
    ) -> _FirstRadialJet[Scalar]:
        return self + (-self._coerce(other))

    def __rsub__(
        self, other: _FirstRadialJet[Scalar] | Scalar
    ) -> _FirstRadialJet[Scalar]:
        return self._coerce(other) - self

    def __mul__(
        self, other: _FirstRadialJet[Scalar] | Scalar
    ) -> _FirstRadialJet[Scalar]:
        right = self._coerce(other)
        return _FirstRadialJet(
            self.value * right.value,  # type: ignore[operator]
            self.derivative * right.value
            + self.value * right.derivative,  # type: ignore[operator]
        )

    __rmul__ = __mul__

    def __truediv__(
        self, other: _FirstRadialJet[Scalar] | Scalar
    ) -> _FirstRadialJet[Scalar]:
        right = self._coerce(other)
        denominator = right.value * right.value  # type: ignore[operator]
        return _FirstRadialJet(
            self.value / right.value,  # type: ignore[operator]
            (
                self.derivative * right.value
                - self.value * right.derivative  # type: ignore[operator]
            )
            / denominator,  # type: ignore[operator]
        )

    def __rtruediv__(
        self, other: _FirstRadialJet[Scalar] | Scalar
    ) -> _FirstRadialJet[Scalar]:
        return self._coerce(other) / self


@dataclass(frozen=True)
class _AffineScalar(Generic[Scalar]):
    constant: Scalar
    coefficients: tuple[Scalar, ...]
    variable: bool

    @classmethod
    def lifted(cls, value: Scalar, dimension: int) -> _AffineScalar[Scalar]:
        zero = value - value  # type: ignore[operator]
        return cls(value, (zero,) * dimension, False)

    @classmethod
    def basis(
        cls, template: Scalar, dimension: int, index: int
    ) -> _AffineScalar[Scalar]:
        zero = template - template  # type: ignore[operator]
        one = zero + 1  # type: ignore[operator]
        coefficients = [zero] * dimension
        coefficients[index] = one
        return cls(zero, tuple(coefficients), True)

    def _coerce(self, other: _AffineScalar[Scalar] | Scalar) -> _AffineScalar[Scalar]:
        return (
            other
            if isinstance(other, _AffineScalar)
            else self.lifted(other, len(self.coefficients))
        )

    def __add__(
        self, other: _AffineScalar[Scalar] | Scalar
    ) -> _AffineScalar[Scalar]:
        right = self._coerce(other)
        return _AffineScalar(
            self.constant + right.constant,  # type: ignore[operator]
            tuple(
                left + right_value  # type: ignore[operator]
                for left, right_value in zip(
                    self.coefficients, right.coefficients, strict=True
                )
            ),
            self.variable or right.variable,
        )

    __radd__ = __add__

    def __neg__(self) -> _AffineScalar[Scalar]:
        return _AffineScalar(
            -self.constant,  # type: ignore[operator]
            tuple(-value for value in self.coefficients),  # type: ignore[operator]
            self.variable,
        )

    def __sub__(
        self, other: _AffineScalar[Scalar] | Scalar
    ) -> _AffineScalar[Scalar]:
        return self + (-self._coerce(other))

    def __rsub__(
        self, other: _AffineScalar[Scalar] | Scalar
    ) -> _AffineScalar[Scalar]:
        return self._coerce(other) - self

    def __mul__(
        self, other: _AffineScalar[Scalar] | Scalar
    ) -> _AffineScalar[Scalar]:
        right = self._coerce(other)
        if self.variable and right.variable:
            raise ValueError("affine kernel encountered a nonlinear field product")
        return _AffineScalar(
            self.constant * right.constant,  # type: ignore[operator]
            tuple(
                left * right.constant + self.constant * right_value  # type: ignore[operator]
                for left, right_value in zip(
                    self.coefficients, right.coefficients, strict=True
                )
            ),
            self.variable or right.variable,
        )

    __rmul__ = __mul__

    def __truediv__(
        self, other: _AffineScalar[Scalar] | Scalar
    ) -> _AffineScalar[Scalar]:
        right = self._coerce(other)
        if right.variable:
            raise ValueError("affine kernel encountered a field-dependent denominator")
        return _AffineScalar(
            self.constant / right.constant,  # type: ignore[operator]
            tuple(
                value / right.constant  # type: ignore[operator]
                for value in self.coefficients
            ),
            self.variable,
        )

    def __rtruediv__(
        self, other: _AffineScalar[Scalar] | Scalar
    ) -> _AffineScalar[Scalar]:
        return self._coerce(other) / self

    def evaluate(self, arguments: tuple[Scalar, ...]) -> Scalar:
        if len(arguments) != len(self.coefficients):
            raise ValueError("affine argument count does not match kernel dimension")
        result = self.constant
        for coefficient, argument in zip(self.coefficients, arguments, strict=True):
            result = result + coefficient * argument  # type: ignore[operator]
        return result


def centrifugal_completed_stress_generic(
    *,
    radius: Scalar,
    metric_factor: Scalar,
    sine_profile: Scalar,
    cosine_profile: Scalar,
    profile_derivative: Scalar,
    radial_field: Scalar,
    radial_field_derivative: Scalar,
    tangential_field: Scalar,
    tangential_field_derivative: Scalar,
    pion_mass_squared: Scalar,
) -> CompletedStress[Scalar]:
    """Evaluate the exact completed stress using only scalar arithmetic."""
    radius_squared = radius * radius  # type: ignore[operator]
    sine_squared = sine_profile * sine_profile  # type: ignore[operator]
    profile_derivative_squared = profile_derivative * profile_derivative  # type: ignore[operator]
    radial_strain_squared = metric_factor * profile_derivative_squared  # type: ignore[operator]
    tangential_strain_squared = sine_squared / radius_squared  # type: ignore[operator]
    sigma_rotation = sine_squared / (metric_factor * 8)  # type: ignore[operator]
    skyrme_rotation = sine_squared / (metric_factor * 2)  # type: ignore[operator]

    rigid_energy = -(
        sigma_rotation
        + skyrme_rotation * (radial_strain_squared + tangential_strain_squared)  # type: ignore[operator]
    )
    rigid_radial = -(
        sigma_rotation
        + skyrme_rotation * (tangential_strain_squared - radial_strain_squared)  # type: ignore[operator]
    )
    rigid_tangential = -(
        sigma_rotation + skyrme_rotation * radial_strain_squared  # type: ignore[operator]
    )
    rigid_tracefree = -(skyrme_rotation * tangential_strain_squared)  # type: ignore[operator]
    zero = radius - radius  # type: ignore[operator]
    quarter = (zero + 1) / 4  # type: ignore[operator]

    radial_strain_variation = (
        metric_factor * profile_derivative * radial_field_derivative * 2  # type: ignore[operator]
    )
    angular_strain_trace_variation = (
        sine_profile
        * (radial_field * cosine_profile * 2 - tangential_field * 3)  # type: ignore[operator]
        * 2
        / radius_squared  # type: ignore[operator]
    )
    total_strain_trace_variation = (
        radial_strain_variation + angular_strain_trace_variation  # type: ignore[operator]
    )
    deformation_energy = (
        total_strain_trace_variation / 8  # type: ignore[operator]
        + tangential_strain_squared * radial_strain_variation
        + (radial_strain_squared + tangential_strain_squared)  # type: ignore[operator]
        * angular_strain_trace_variation
        / 2
        + pion_mass_squared * radial_field * sine_profile / 4  # type: ignore[operator]
    )
    deformation_radial = (
        radial_strain_variation
        * (
            quarter
            - radial_strain_squared  # type: ignore[operator]
            + tangential_strain_squared * 2
        )
        + radial_strain_squared * total_strain_trace_variation
        - deformation_energy
    )
    angular_isotropic_strain_variation = (
        sine_profile
        * (radial_field * cosine_profile * 2 - tangential_field * 3)  # type: ignore[operator]
        / radius_squared  # type: ignore[operator]
    )
    deformation_tangential = (
        (quarter + radial_strain_squared)  # type: ignore[operator]
        * angular_isotropic_strain_variation
        + tangential_strain_squared * total_strain_trace_variation
        - deformation_energy
    )
    deformation_tracefree = (
        (quarter + radial_strain_squared)  # type: ignore[operator]
        * sine_profile
        * tangential_field
        / radius_squared  # type: ignore[operator]
    )
    radial_angular_strain = (
        sine_profile * tangential_field_derivative
        + profile_derivative
        * (radial_field * 2 - cosine_profile * tangential_field)  # type: ignore[operator]
    )
    deformation_shear = (
        metric_factor
        * radial_angular_strain
        * (quarter + tangential_strain_squared)  # type: ignore[operator]
        / 2
    )

    rigid = StressAmplitudes(
        rigid_energy,
        rigid_radial,
        rigid_tangential,
        zero,
        rigid_tracefree,
    )
    deformation = StressAmplitudes(
        deformation_energy,
        deformation_radial,
        deformation_tangential,
        deformation_shear,
        deformation_tracefree,
    )
    return CompletedStress(rigid, deformation, rigid + deformation)


@dataclass(frozen=True)
class AffineCompletedStressKernel(Generic[Scalar]):
    """Pointwise ``T_rigid``, ``L0``, and ``L1`` coefficients."""

    rigid: StressAmplitudes[Scalar]
    radial_field: StressAmplitudes[Scalar]
    radial_field_derivative: StressAmplitudes[Scalar]
    tangential_field: StressAmplitudes[Scalar]
    tangential_field_derivative: StressAmplitudes[Scalar]

    @property
    def l0(self) -> tuple[StressAmplitudes[Scalar], StressAmplitudes[Scalar]]:
        return self.radial_field, self.tangential_field

    @property
    def l1(self) -> tuple[StressAmplitudes[Scalar], StressAmplitudes[Scalar]]:
        return self.radial_field_derivative, self.tangential_field_derivative

    def evaluate(
        self,
        *,
        radial_field: Scalar,
        radial_field_derivative: Scalar,
        tangential_field: Scalar,
        tangential_field_derivative: Scalar,
    ) -> StressAmplitudes[Scalar]:
        return (
            self.rigid
            + self.radial_field.scale(radial_field)
            + self.radial_field_derivative.scale(radial_field_derivative)
            + self.tangential_field.scale(tangential_field)
            + self.tangential_field_derivative.scale(tangential_field_derivative)
        )


def _stress_from_affine(
    stress: StressAmplitudes[_AffineScalar[Scalar]], index: int | None
) -> StressAmplitudes[Scalar]:
    def select(value: _AffineScalar[Scalar]) -> Scalar:
        return value.constant if index is None else value.coefficients[index]

    return StressAmplitudes(
        select(stress.energy_density),
        select(stress.radial_pressure),
        select(stress.tangential_pressure),
        select(stress.radial_angular_shear),
        select(stress.angular_tracefree_stress),
    )


def centrifugal_completed_stress_affine_kernel(
    *,
    radius: Scalar,
    metric_factor: Scalar,
    sine_profile: Scalar,
    cosine_profile: Scalar,
    profile_derivative: Scalar,
    pion_mass_squared: Scalar,
) -> AffineCompletedStressKernel[Scalar]:
    """Extract the exact four-field affine stress coefficients."""
    dimension = 4
    lift = lambda value: _AffineScalar.lifted(value, dimension)  # noqa: E731
    fields = tuple(_AffineScalar.basis(radius, dimension, index) for index in range(4))
    result = centrifugal_completed_stress_generic(
        radius=lift(radius),
        metric_factor=lift(metric_factor),
        sine_profile=lift(sine_profile),
        cosine_profile=lift(cosine_profile),
        profile_derivative=lift(profile_derivative),
        radial_field=fields[0],
        radial_field_derivative=fields[1],
        tangential_field=fields[2],
        tangential_field_derivative=fields[3],
        pion_mass_squared=lift(pion_mass_squared),
    )
    total = result.total
    return AffineCompletedStressKernel(
        _stress_from_affine(total, None),
        *(_stress_from_affine(total, index) for index in range(dimension)),
    )


def static_l2_master_source_density_generic(
    *,
    radius: Scalar,
    metric_factor: Scalar,
    inverse_patch_radius_squared: Scalar,
    energy_density: Scalar,
    energy_density_derivative: Scalar,
    radial_pressure: Scalar,
    radial_angular_shear: Scalar,
    angular_tracefree_stress: Scalar,
    gravitational_coupling: Scalar,
) -> Scalar:
    """Generic-scalar form of the smooth ``ell=2`` master source."""
    radius_squared = radius * radius  # type: ignore[operator]
    return gravitational_coupling * (  # type: ignore[operator]
        -(radius_squared * metric_factor * energy_density_derivative) / 6  # type: ignore[operator]
        + radius
        * (radius_squared * inverse_patch_radius_squared * 4 + 1)  # type: ignore[operator]
        * energy_density
        / 6
        - radius * radial_pressure / 2  # type: ignore[operator]
        - radial_angular_shear
        + radius * angular_tracefree_stress * 2
    )


def centrifugal_completed_master_source_generic(
    *,
    radius: Scalar,
    metric_factor: Scalar,
    metric_factor_derivative: Scalar,
    inverse_patch_radius_squared: Scalar,
    sine_profile: Scalar,
    cosine_profile: Scalar,
    profile_derivative: Scalar,
    profile_second_derivative: Scalar,
    radial_field: Scalar,
    radial_field_derivative: Scalar,
    radial_field_second_derivative: Scalar,
    tangential_field: Scalar,
    tangential_field_derivative: Scalar,
    pion_mass_squared: Scalar,
    gravitational_coupling: Scalar,
) -> Scalar:
    """Evaluate the bulk master source with an exact radial energy jet."""
    zero = radius - radius  # type: ignore[operator]
    one = zero + 1  # type: ignore[operator]
    radius_jet = _FirstRadialJet(radius, one)
    metric_jet = _FirstRadialJet(metric_factor, metric_factor_derivative)
    sine_jet = _FirstRadialJet(
        sine_profile, cosine_profile * profile_derivative  # type: ignore[operator]
    )
    cosine_jet = _FirstRadialJet(
        cosine_profile, -(sine_profile * profile_derivative)  # type: ignore[operator]
    )
    profile_derivative_jet = _FirstRadialJet(
        profile_derivative, profile_second_derivative
    )
    radial_field_jet = _FirstRadialJet(radial_field, radial_field_derivative)
    radial_derivative_jet = _FirstRadialJet(
        radial_field_derivative, radial_field_second_derivative
    )
    tangential_field_jet = _FirstRadialJet(
        tangential_field, tangential_field_derivative
    )
    tangential_derivative_jet = _FirstRadialJet(tangential_field_derivative, zero)
    mass_jet = _FirstRadialJet.constant(pion_mass_squared)
    stress = centrifugal_completed_stress_generic(
        radius=radius_jet,
        metric_factor=metric_jet,
        sine_profile=sine_jet,
        cosine_profile=cosine_jet,
        profile_derivative=profile_derivative_jet,
        radial_field=radial_field_jet,
        radial_field_derivative=radial_derivative_jet,
        tangential_field=tangential_field_jet,
        tangential_field_derivative=tangential_derivative_jet,
        pion_mass_squared=mass_jet,
    ).total
    return static_l2_master_source_density_generic(
        radius=radius,
        metric_factor=metric_factor,
        inverse_patch_radius_squared=inverse_patch_radius_squared,
        energy_density=stress.energy_density.value,
        energy_density_derivative=stress.energy_density.derivative,
        radial_pressure=stress.radial_pressure.value,
        radial_angular_shear=stress.radial_angular_shear.value,
        angular_tracefree_stress=stress.angular_tracefree_stress.value,
        gravitational_coupling=gravitational_coupling,
    )


@dataclass(frozen=True)
class AffineMasterSourceKernel(Generic[Scalar]):
    """Pointwise affine coefficients of the smooth bulk master source."""

    rigid: Scalar
    radial_field: Scalar
    radial_field_derivative: Scalar
    radial_field_second_derivative: Scalar
    tangential_field: Scalar
    tangential_field_derivative: Scalar

    def evaluate(
        self,
        *,
        radial_field: Scalar,
        radial_field_derivative: Scalar,
        radial_field_second_derivative: Scalar,
        tangential_field: Scalar,
        tangential_field_derivative: Scalar,
    ) -> Scalar:
        return (  # type: ignore[return-value]
            self.rigid
            + self.radial_field * radial_field  # type: ignore[operator]
            + self.radial_field_derivative * radial_field_derivative
            + self.radial_field_second_derivative * radial_field_second_derivative
            + self.tangential_field * tangential_field
            + self.tangential_field_derivative * tangential_field_derivative
        )


def centrifugal_completed_master_source_affine_kernel(
    *,
    radius: Scalar,
    metric_factor: Scalar,
    metric_factor_derivative: Scalar,
    inverse_patch_radius_squared: Scalar,
    sine_profile: Scalar,
    cosine_profile: Scalar,
    profile_derivative: Scalar,
    profile_second_derivative: Scalar,
    pion_mass_squared: Scalar,
    gravitational_coupling: Scalar,
) -> AffineMasterSourceKernel[Scalar]:
    """Extract the exact five-field affine bulk-source coefficients."""
    dimension = 5
    lift = lambda value: _AffineScalar.lifted(value, dimension)  # noqa: E731
    fields = tuple(_AffineScalar.basis(radius, dimension, index) for index in range(5))
    result = centrifugal_completed_master_source_generic(
        radius=lift(radius),
        metric_factor=lift(metric_factor),
        metric_factor_derivative=lift(metric_factor_derivative),
        inverse_patch_radius_squared=lift(inverse_patch_radius_squared),
        sine_profile=lift(sine_profile),
        cosine_profile=lift(cosine_profile),
        profile_derivative=lift(profile_derivative),
        profile_second_derivative=lift(profile_second_derivative),
        radial_field=fields[0],
        radial_field_derivative=fields[1],
        radial_field_second_derivative=fields[2],
        tangential_field=fields[3],
        tangential_field_derivative=fields[4],
        pion_mass_squared=lift(pion_mass_squared),
        gravitational_coupling=lift(gravitational_coupling),
    )
    return AffineMasterSourceKernel(result.constant, *result.coefficients)


@dataclass(frozen=True)
class BackgroundWallStress(Generic[Scalar]):
    """Spherical background stress evaluated on the inner side of the wall."""

    energy_density: Scalar
    radial_pressure: Scalar
    tangential_pressure: Scalar


def centrifugal_background_wall_stress_generic(
    *,
    radius: Scalar,
    metric_factor: Scalar,
    sine_profile: Scalar,
    cosine_profile: Scalar,
    profile_derivative: Scalar,
    pion_mass_squared: Scalar,
) -> BackgroundWallStress[Scalar]:
    """Return the same-action spherical wall stress using scalar arithmetic."""
    zero = radius - radius  # type: ignore[operator]
    one = zero + 1  # type: ignore[operator]
    radius_squared = radius * radius  # type: ignore[operator]
    radial_strain = (  # type: ignore[operator]
        metric_factor * profile_derivative * profile_derivative
    )
    tangential_strain = (  # type: ignore[operator]
        sine_profile * sine_profile / radius_squared
    )
    potential = (  # type: ignore[operator]
        pion_mass_squared * (one - cosine_profile) / 4
    )
    energy = (  # type: ignore[operator]
        radial_strain / 8
        + tangential_strain / 4
        + radial_strain * tangential_strain
        + tangential_strain * tangential_strain / 2
        + potential
    )
    radial = (  # type: ignore[operator]
        radial_strain / 8
        - tangential_strain / 4
        + radial_strain * tangential_strain
        - tangential_strain * tangential_strain / 2
        - potential
    )
    tangential = (  # type: ignore[operator]
        -radial_strain / 8
        + tangential_strain * tangential_strain / 2
        - potential
    )
    return BackgroundWallStress(energy, radial, tangential)


@dataclass(frozen=True)
class MovingInterfaceStressJet(Generic[Scalar]):
    """Canonical delta jets of the displaced bulk plus pure-tension wall."""

    energy_density_delta: Scalar
    energy_density_delta_prime: Scalar
    radial_pressure_delta: Scalar
    radial_pressure_delta_prime: Scalar
    tangential_pressure_delta: Scalar
    tangential_pressure_delta_prime: Scalar
    radial_angular_shear_delta: Scalar
    radial_angular_shear_delta_prime: Scalar
    angular_tracefree_stress_delta: Scalar
    angular_tracefree_stress_delta_prime: Scalar


def moving_interface_singular_amplitudes_generic(
    *,
    wall_metric_factor_derivative: Scalar,
    sqrt_wall_metric_factor: Scalar,
    membrane_tension: Scalar,
    wall_displacement: Scalar,
    background_energy_density: Scalar,
    background_radial_pressure: Scalar,
    background_tangential_pressure: Scalar,
) -> MovingInterfaceStressJet[Scalar]:
    """Generic-scalar version of the moving-interface stress distribution."""
    zero = wall_displacement - wall_displacement  # type: ignore[operator]
    lapse_shape = (  # type: ignore[operator]
        wall_metric_factor_derivative / (sqrt_wall_metric_factor * 2)
    )
    shell_energy_delta = (  # type: ignore[operator]
        membrane_tension * wall_displacement * lapse_shape
    )
    shell_energy_delta_prime = -(  # type: ignore[operator]
        membrane_tension * wall_displacement * sqrt_wall_metric_factor
    )
    shell_shear_delta = shell_energy_delta_prime
    return MovingInterfaceStressJet(
        wall_displacement * background_energy_density + shell_energy_delta,  # type: ignore[operator]
        shell_energy_delta_prime,
        wall_displacement * background_radial_pressure,  # type: ignore[operator]
        zero,
        wall_displacement * background_tangential_pressure  # type: ignore[operator]
        - shell_energy_delta,
        -shell_energy_delta_prime,
        shell_shear_delta,
        zero,
        zero,
        zero,
    )


@dataclass(frozen=True)
class ContactFreeMasterSourceJet(Generic[Scalar]):
    """Literal master delta jet and its contact-free representative."""

    delta_second: Scalar
    delta_prime: Scalar
    delta: Scalar
    master_field_contact_delta: Scalar
    contact_free_delta_prime: Scalar
    contact_free_delta: Scalar
    contact_free_delta_without_bulk_endpoint: Scalar


def canonical_l2_master_source_distribution_generic(
    *,
    wall_radius: Scalar,
    wall_metric_factor: Scalar,
    wall_metric_factor_derivative: Scalar,
    inverse_patch_radius_squared: Scalar,
    bulk_energy_density_at_wall: Scalar,
    singular_stress: MovingInterfaceStressJet[Scalar],
    gravitational_coupling: Scalar,
) -> ContactFreeMasterSourceJet[Scalar]:
    """Map canonical stress jets to the literal and contact-free source."""
    radius = wall_radius
    zero = radius - radius  # type: ignore[operator]
    one = zero + 1  # type: ignore[operator]
    radius_squared = radius * radius  # type: ignore[operator]
    lapse = wall_metric_factor
    lapse_p = wall_metric_factor_derivative
    lapse_pp = -(inverse_patch_radius_squared * 2)  # type: ignore[operator]
    coefficient_a = radius_squared * lapse / 6  # type: ignore[operator]
    coefficient_a_p = (  # type: ignore[operator]
        radius * lapse / 3 + radius_squared * lapse_p / 6
    )
    coefficient_a_pp = (  # type: ignore[operator]
        lapse / 3 + radius * lapse_p * 2 / 3 + radius_squared * lapse_pp / 6
    )
    coefficient_b = (  # type: ignore[operator]
        radius * (one + radius_squared * inverse_patch_radius_squared * 4) / 6
    )
    coefficient_b_p = (  # type: ignore[operator]
        (one + radius_squared * inverse_patch_radius_squared * 12) / 6
    )
    stress = singular_stress
    delta_second = gravitational_coupling * (  # type: ignore[operator]
        -coefficient_a * stress.energy_density_delta_prime
    )
    delta_prime = gravitational_coupling * (  # type: ignore[operator]
        -coefficient_a * stress.energy_density_delta
        + coefficient_a_p * stress.energy_density_delta_prime * 2
        + coefficient_b * stress.energy_density_delta_prime
        - radius * stress.radial_pressure_delta_prime / 2
        - stress.radial_angular_shear_delta_prime
        + radius * stress.angular_tracefree_stress_delta_prime * 2
    )
    delta_without_bulk_endpoint = gravitational_coupling * (  # type: ignore[operator]
        coefficient_a_p * stress.energy_density_delta
        - coefficient_a_pp * stress.energy_density_delta_prime
        + coefficient_b * stress.energy_density_delta
        - coefficient_b_p * stress.energy_density_delta_prime
        - radius * stress.radial_pressure_delta / 2
        + stress.radial_pressure_delta_prime / 2
        - stress.radial_angular_shear_delta
        + radius * stress.angular_tracefree_stress_delta * 2
        - stress.angular_tracefree_stress_delta_prime * 2
    )
    bulk_endpoint_source = (  # type: ignore[operator]
        gravitational_coupling * coefficient_a * bulk_energy_density_at_wall
    )
    delta = bulk_endpoint_source + delta_without_bulk_endpoint  # type: ignore[operator]
    potential = (zero + 6) / radius_squared  # type: ignore[operator]
    contact = -delta_second / lapse  # type: ignore[operator]
    contact_free_delta_prime = (  # type: ignore[operator]
        delta_prime + delta_second * lapse_p / lapse
    )
    contact_without_bulk_endpoint = (  # type: ignore[operator]
        delta_without_bulk_endpoint + potential * delta_second / lapse
    )
    contact_free_delta = (  # type: ignore[operator]
        bulk_endpoint_source + contact_without_bulk_endpoint
    )
    return ContactFreeMasterSourceJet(
        delta_second,
        delta_prime,
        delta,
        contact,
        contact_free_delta_prime,
        contact_free_delta,
        contact_without_bulk_endpoint,
    )


@dataclass(frozen=True)
class MovingWallMasterContribution(Generic[Scalar]):
    """All wall-local quantities entering the exterior master amplitude."""

    wall_displacement: Scalar
    bulk_energy_density_at_wall: Scalar
    singular_stress: MovingInterfaceStressJet[Scalar]
    master_source: ContactFreeMasterSourceJet[Scalar]
    raw_contact_free_exterior_amplitude: Scalar
    bulk_energy_endpoint_amplitude: Scalar
    effective_wall_amplitude: Scalar


def centrifugal_moving_wall_master_contribution_generic(
    *,
    wall_radius: Scalar,
    wall_metric_factor: Scalar,
    wall_metric_factor_derivative: Scalar,
    sqrt_wall_metric_factor: Scalar,
    inverse_patch_radius_squared: Scalar,
    sine_profile: Scalar,
    cosine_profile: Scalar,
    profile_derivative: Scalar,
    radial_field: Scalar,
    radial_field_derivative: Scalar,
    tangential_field: Scalar,
    tangential_field_derivative: Scalar,
    pion_mass_squared: Scalar,
    membrane_tension: Scalar,
    wall_displacement_per_radial_field: Scalar,
    wall_green_weight: Scalar,
    wall_green_weight_derivative: Scalar,
    gravitational_coupling: Scalar,
) -> MovingWallMasterContribution[Scalar]:
    """Evaluate the moving-wall/contact-free response using scalar arithmetic.

    ``wall_green_weight`` is ``w(a)`` and its derivative is ``w'(a)`` for the
    factorized exterior Green kernel.  The effective amplitude subtracts the
    bulk integration-by-parts endpoint and is the quantity whose coefficient
    of ``radial_field`` is the physical response trace ``gamma_B``.
    """
    completed = centrifugal_completed_stress_generic(
        radius=wall_radius,
        metric_factor=wall_metric_factor,
        sine_profile=sine_profile,
        cosine_profile=cosine_profile,
        profile_derivative=profile_derivative,
        radial_field=radial_field,
        radial_field_derivative=radial_field_derivative,
        tangential_field=tangential_field,
        tangential_field_derivative=tangential_field_derivative,
        pion_mass_squared=pion_mass_squared,
    ).total
    background = centrifugal_background_wall_stress_generic(
        radius=wall_radius,
        metric_factor=wall_metric_factor,
        sine_profile=sine_profile,
        cosine_profile=cosine_profile,
        profile_derivative=profile_derivative,
        pion_mass_squared=pion_mass_squared,
    )
    displacement = (  # type: ignore[operator]
        wall_displacement_per_radial_field * radial_field
    )
    singular = moving_interface_singular_amplitudes_generic(
        wall_metric_factor_derivative=wall_metric_factor_derivative,
        sqrt_wall_metric_factor=sqrt_wall_metric_factor,
        membrane_tension=membrane_tension,
        wall_displacement=displacement,
        background_energy_density=background.energy_density,
        background_radial_pressure=background.radial_pressure,
        background_tangential_pressure=background.tangential_pressure,
    )
    source = canonical_l2_master_source_distribution_generic(
        wall_radius=wall_radius,
        wall_metric_factor=wall_metric_factor,
        wall_metric_factor_derivative=wall_metric_factor_derivative,
        inverse_patch_radius_squared=inverse_patch_radius_squared,
        bulk_energy_density_at_wall=completed.energy_density,
        singular_stress=singular,
        gravitational_coupling=gravitational_coupling,
    )
    raw_amplitude = (  # type: ignore[operator]
        wall_green_weight * source.contact_free_delta
        - wall_green_weight_derivative * source.contact_free_delta_prime
    )
    coefficient_a = (  # type: ignore[operator]
        wall_radius * wall_radius * wall_metric_factor / 6
    )
    endpoint_amplitude = (  # type: ignore[operator]
        gravitational_coupling
        * wall_green_weight
        * coefficient_a
        * completed.energy_density
    )
    effective_amplitude = (  # type: ignore[operator]
        wall_green_weight * source.contact_free_delta_without_bulk_endpoint
        - wall_green_weight_derivative * source.contact_free_delta_prime
    )
    return MovingWallMasterContribution(
        displacement,
        completed.energy_density,
        singular,
        source,
        raw_amplitude,
        endpoint_amplitude,
        effective_amplitude,
    )


@dataclass(frozen=True)
class AffineMovingWallMasterKernel(Generic[Scalar]):
    """Exact affine coefficients of all moving-wall response quantities."""

    rigid: MovingWallMasterContribution[Scalar]
    radial_field: MovingWallMasterContribution[Scalar]
    radial_field_derivative: MovingWallMasterContribution[Scalar]
    tangential_field: MovingWallMasterContribution[Scalar]
    tangential_field_derivative: MovingWallMasterContribution[Scalar]
    wall_displacement_per_radial_field: Scalar

    @property
    def response_wall_trace_gamma_b(self) -> Scalar:
        """Coefficient of ``f(a)`` after the bulk endpoint cancellation."""
        return self.radial_field.effective_wall_amplitude


def _wall_contribution_from_affine(
    contribution: MovingWallMasterContribution[_AffineScalar[Scalar]],
    index: int | None,
) -> MovingWallMasterContribution[Scalar]:
    def select(value: _AffineScalar[Scalar]) -> Scalar:
        return value.constant if index is None else value.coefficients[index]

    stress = contribution.singular_stress
    selected_stress = MovingInterfaceStressJet(
        select(stress.energy_density_delta),
        select(stress.energy_density_delta_prime),
        select(stress.radial_pressure_delta),
        select(stress.radial_pressure_delta_prime),
        select(stress.tangential_pressure_delta),
        select(stress.tangential_pressure_delta_prime),
        select(stress.radial_angular_shear_delta),
        select(stress.radial_angular_shear_delta_prime),
        select(stress.angular_tracefree_stress_delta),
        select(stress.angular_tracefree_stress_delta_prime),
    )
    source = contribution.master_source
    selected_source = ContactFreeMasterSourceJet(
        select(source.delta_second),
        select(source.delta_prime),
        select(source.delta),
        select(source.master_field_contact_delta),
        select(source.contact_free_delta_prime),
        select(source.contact_free_delta),
        select(source.contact_free_delta_without_bulk_endpoint),
    )
    return MovingWallMasterContribution(
        select(contribution.wall_displacement),
        select(contribution.bulk_energy_density_at_wall),
        selected_stress,
        selected_source,
        select(contribution.raw_contact_free_exterior_amplitude),
        select(contribution.bulk_energy_endpoint_amplitude),
        select(contribution.effective_wall_amplitude),
    )


def centrifugal_moving_wall_master_affine_kernel(
    *,
    wall_radius: Scalar,
    wall_metric_factor: Scalar,
    wall_metric_factor_derivative: Scalar,
    sqrt_wall_metric_factor: Scalar,
    inverse_patch_radius_squared: Scalar,
    sine_profile: Scalar,
    cosine_profile: Scalar,
    profile_derivative: Scalar,
    pion_mass_squared: Scalar,
    membrane_tension: Scalar,
    wall_displacement_per_radial_field: Scalar,
    wall_green_weight: Scalar,
    wall_green_weight_derivative: Scalar,
    gravitational_coupling: Scalar,
) -> AffineMovingWallMasterKernel[Scalar]:
    """Extract the exact four-field affine moving-wall response kernel."""
    dimension = 4
    lift = lambda value: _AffineScalar.lifted(value, dimension)  # noqa: E731
    fields = tuple(
        _AffineScalar.basis(wall_radius, dimension, index)
        for index in range(dimension)
    )
    result = centrifugal_moving_wall_master_contribution_generic(
        wall_radius=lift(wall_radius),
        wall_metric_factor=lift(wall_metric_factor),
        wall_metric_factor_derivative=lift(wall_metric_factor_derivative),
        sqrt_wall_metric_factor=lift(sqrt_wall_metric_factor),
        inverse_patch_radius_squared=lift(inverse_patch_radius_squared),
        sine_profile=lift(sine_profile),
        cosine_profile=lift(cosine_profile),
        profile_derivative=lift(profile_derivative),
        radial_field=fields[0],
        radial_field_derivative=fields[1],
        tangential_field=fields[2],
        tangential_field_derivative=fields[3],
        pion_mass_squared=lift(pion_mass_squared),
        membrane_tension=lift(membrane_tension),
        wall_displacement_per_radial_field=lift(
            wall_displacement_per_radial_field
        ),
        wall_green_weight=lift(wall_green_weight),
        wall_green_weight_derivative=lift(wall_green_weight_derivative),
        gravitational_coupling=lift(gravitational_coupling),
    )
    return AffineMovingWallMasterKernel(
        _wall_contribution_from_affine(result, None),
        *(
            _wall_contribution_from_affine(result, index)
            for index in range(dimension)
        ),
        wall_displacement_per_radial_field,
    )
