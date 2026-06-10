"""Directed spherical-constraint replay for the certified Skyrmion source.

The authenticated sharp profile supplies pointwise interval boxes for the
fixed-de-Sitter Skyrmion energy density.  This module integrates those boxes
cumulatively and bounds

``H = sup_x c_m(x)/(x (1-lambda x^2))``

including the Nambu-Goto wall mass at ``x=x_w``.  For
``alpha=2G/(e^2 R^2 lambda)``, the spherical Hamiltonian-constraint ratio obeys
``q(x)<=alpha H_upper``.  This is a directed test-source constraint response,
not a self-consistent Einstein-Skyrme solution.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .validated_interval import (
    RationalInterval,
    cos_center_lipschitz_interval,
    pi_machin_interval,
    sin_center_lipschitz_interval,
)
from .validated_skyrmion_origin import (
    ValidatedSkyrmionOriginFamily,
    _entire_even_kernel_interval,
)
from .validated_skyrmion_sharp_profile import (
    ValidatedSkyrmionSharpProfileTube,
    build_validated_skyrmion_sharp_worldtube_constants,
)


def _positive_integer(name: str, value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


@dataclass(frozen=True)
class ValidatedSkyrmionEnergyCell:
    region: str
    source_cell_index: int
    radius: RationalInterval
    reduced_density: RationalInterval
    reduced_integral: RationalInterval


@dataclass(frozen=True)
class ValidatedSkyrmionConstraintShape:
    certificate_id: str
    curvature: Fraction
    wall_radius: Fraction
    interior_mass: RationalInterval
    shell_mass: RationalInterval
    total_mass: RationalInterval
    origin_cells: tuple[ValidatedSkyrmionEnergyCell, ...]
    positive_radius_cells: tuple[ValidatedSkyrmionEnergyCell, ...]
    fixed_background_exterior_shape_lower: Fraction
    sufficient_bulk_shape_upper: Fraction
    sufficient_test_source_global_shape_upper: Fraction
    maximum_upper_region: str
    maximum_upper_source_cell_index: int
    claim_boundary: str

    def to_record(self) -> dict[str, object]:
        return {
            "certificate_id": self.certificate_id,
            "curvature_lambda": str(self.curvature),
            "wall_radius_x_w": str(self.wall_radius),
            "interior_mass_enclosure": _interval_record(self.interior_mass),
            "shell_mass_enclosure": _interval_record(self.shell_mass),
            "total_mass_enclosure": _interval_record(self.total_mass),
            "origin_cell_count": len(self.origin_cells),
            "positive_radius_cell_count": len(self.positive_radius_cells),
            "fixed_background_exterior_shape_lower_exact": str(
                self.fixed_background_exterior_shape_lower
            ),
            "fixed_background_exterior_shape_lower_float": float(
                self.fixed_background_exterior_shape_lower
            ),
            "sufficient_bulk_shape_upper_exact": str(
                self.sufficient_bulk_shape_upper
            ),
            "sufficient_bulk_shape_upper_float": float(
                self.sufficient_bulk_shape_upper
            ),
            "sufficient_test_source_global_shape_upper_exact": str(
                self.sufficient_test_source_global_shape_upper
            ),
            "sufficient_test_source_global_shape_upper_float": float(
                self.sufficient_test_source_global_shape_upper
            ),
            "upper_to_lower_shape_ratio": float(
                self.sufficient_test_source_global_shape_upper
                / self.fixed_background_exterior_shape_lower
            ),
            "maximum_upper_region": self.maximum_upper_region,
            "maximum_upper_source_cell_index": (
                self.maximum_upper_source_cell_index
            ),
            "claim_boundary": self.claim_boundary,
        }


def _interval_record(value: RationalInterval) -> dict[str, str]:
    return {"lower": str(value.lower), "upper": str(value.upper)}


def _positive_radius_density(
    profile: ValidatedSkyrmionSharpProfileTube,
    cell_index: int,
    *,
    trigonometric_terms: int,
) -> RationalInterval:
    cell = profile.cells[cell_index]
    radius_squared = cell.radius.power(2)
    lapse = RationalInterval.point(1) - radius_squared.scale(profile.curvature)
    sine = sin_center_lipschitz_interval(
        cell.solution_profile,
        terms=trigonometric_terms,
    )
    cosine = cos_center_lipschitz_interval(
        cell.solution_profile,
        terms=trigonometric_terms,
    )
    sine_squared = sine.power(2)
    derivative_squared = cell.solution_derivative.power(2)
    density = (
        lapse * (radius_squared + sine_squared.scale(8)) * derivative_squared
    ).scale(Fraction(1, 8))
    density += sine_squared.scale(Fraction(1, 4))
    density += sine_squared.power(2) / radius_squared.scale(2)
    density += (
        radius_squared * (RationalInterval.point(1) - cosine)
    ).scale(profile.pion_mass_squared / 4)
    if density.lower < 0:
        raise AssertionError("positive-radius energy density became negative")
    return density


def _origin_density_over_radius_squared(
    profile: ValidatedSkyrmionSharpProfileTube,
    origin_family: ValidatedSkyrmionOriginFamily,
    radius: RationalInterval,
    *,
    trigonometric_terms: int,
    origin_kernel_terms: int,
) -> RationalInterval:
    time = radius.power(2)
    time_squared = time.power(2)
    remainder_box = RationalInterval(
        -origin_family.remainder_radius,
        origin_family.remainder_radius,
    )
    u = (
        origin_family.shooting_slopes
        - origin_family.cubic_coefficient * time
        + (remainder_box * time_squared).scale(Fraction(1, 5))
    )
    momentum = (
        origin_family.shooting_slopes
        - (origin_family.cubic_coefficient * time).scale(3)
        + remainder_box * time_squared
    )
    argument = radius * u
    argument_squared = time * u.power(2)
    sinc = _entire_even_kernel_interval(
        argument_squared,
        scale_squared=1,
        derivative_order=0,
        terms=origin_kernel_terms,
    )
    cosine = cos_center_lipschitz_interval(
        argument,
        terms=trigonometric_terms,
    )
    sine_over_radius_squared = (u * sinc).power(2)
    lapse = RationalInterval.point(1) - time.scale(profile.curvature)
    density_over_radius_squared = (
        lapse
        * (RationalInterval.point(1) + sine_over_radius_squared.scale(8))
        * momentum.power(2)
    ).scale(Fraction(1, 8))
    density_over_radius_squared += sine_over_radius_squared.scale(Fraction(1, 4))
    density_over_radius_squared += sine_over_radius_squared.power(2).scale(
        Fraction(1, 2)
    )
    density_over_radius_squared += (
        RationalInterval.point(1) + cosine
    ).scale(profile.pion_mass_squared / 4)
    if density_over_radius_squared.lower < 0:
        raise AssertionError("origin energy coefficient became negative")
    return density_over_radius_squared


def build_validated_skyrmion_constraint_shape(
    profile: ValidatedSkyrmionSharpProfileTube,
    origin_family: ValidatedSkyrmionOriginFamily,
    *,
    origin_subdivisions: int = 32,
    trigonometric_terms: int = 24,
    origin_kernel_terms: int = 20,
    pi_terms: int = 80,
) -> ValidatedSkyrmionConstraintShape:
    """Certify the local spherical-constraint shape coefficient."""
    origin_parts = _positive_integer("origin_subdivisions", origin_subdivisions)
    _positive_integer("trigonometric_terms", trigonometric_terms)
    _positive_integer("origin_kernel_terms", origin_kernel_terms)
    _positive_integer("pi_terms", pi_terms)
    if (
        origin_family.cutoff != profile.origin_cutoff
        or origin_family.curvature != profile.curvature
        or origin_family.pion_mass_squared != profile.pion_mass_squared
        or origin_family.shooting_slopes != profile.shooting_slope_interval
    ):
        raise ValueError("origin family does not match the sharp profile")
    if 3 * profile.curvature * profile.wall_radius**2 >= 1:
        raise ValueError("x(1-lambda x^2) must increase across the worldtube")

    constants = build_validated_skyrmion_sharp_worldtube_constants(
        profile,
        origin_family,
        origin_subdivisions=origin_parts,
        trigonometric_terms=trigonometric_terms,
        origin_kernel_terms=origin_kernel_terms,
        pi_terms=pi_terms,
    )
    pi_interval = pi_machin_interval(terms=pi_terms)
    four_pi = pi_interval.scale(4)
    cumulative = RationalInterval.point(0)
    candidates: list[tuple[Fraction, str, int]] = []
    origin_cells = []
    origin_step = profile.origin_cutoff / origin_parts
    for index in range(origin_parts):
        radius = RationalInterval(index * origin_step, (index + 1) * origin_step)
        coefficient = _origin_density_over_radius_squared(
            profile,
            origin_family,
            radius,
            trigonometric_terms=trigonometric_terms,
            origin_kernel_terms=origin_kernel_terms,
        )
        density = radius.power(2) * coefficient
        integral = density.scale(radius.width)
        cumulative += integral
        origin_cells.append(
            ValidatedSkyrmionEnergyCell(
                region="origin",
                source_cell_index=index,
                radius=radius,
                reduced_density=density,
                reduced_integral=integral,
            )
        )
        if radius.lower == 0:
            upper = radius.upper
            lapse = 1 - profile.curvature * upper**2
            shape_upper = (
                four_pi.upper * coefficient.upper * upper**2 / (3 * lapse)
            )
        else:
            lower = radius.lower
            denominator = lower * (1 - profile.curvature * lower**2)
            shape_upper = (four_pi * cumulative).upper / denominator
        candidates.append((shape_upper, "origin", index))

    positive_cells = []
    for index, cell in enumerate(profile.cells):
        density = _positive_radius_density(
            profile,
            index,
            trigonometric_terms=trigonometric_terms,
        )
        integral = density.scale(cell.radius.width)
        cumulative += integral
        positive_cells.append(
            ValidatedSkyrmionEnergyCell(
                region="positive_radius",
                source_cell_index=index,
                radius=cell.radius,
                reduced_density=density,
                reduced_integral=integral,
            )
        )
        lower = cell.radius.lower
        denominator = lower * (1 - profile.curvature * lower**2)
        candidates.append(
            (
                (four_pi * cumulative).upper / denominator,
                "positive_radius",
                index,
            )
        )

    replayed_interior_mass = four_pi * cumulative
    if replayed_interior_mass != constants.interior_mass:
        raise AssertionError("cumulative energy replay disagrees with worldtube mass")
    wall_lapse = 1 - profile.curvature * profile.wall_radius**2
    fixed_background_exterior = (
        constants.total_mass.lower / (profile.wall_radius * wall_lapse)
    )
    bulk_upper = max(candidates)[0]
    candidates.append(
        (
            constants.total_mass.upper / (profile.wall_radius * wall_lapse),
            "exterior_wall",
            -1,
        )
    )
    maximum_upper, maximum_region, maximum_index = max(candidates)
    return ValidatedSkyrmionConstraintShape(
        certificate_id=profile.certificate_id,
        curvature=profile.curvature,
        wall_radius=profile.wall_radius,
        interior_mass=constants.interior_mass,
        shell_mass=constants.shell_mass,
        total_mass=constants.total_mass,
        origin_cells=tuple(origin_cells),
        positive_radius_cells=tuple(positive_cells),
        fixed_background_exterior_shape_lower=fixed_background_exterior,
        sufficient_bulk_shape_upper=bulk_upper,
        sufficient_test_source_global_shape_upper=maximum_upper,
        maximum_upper_region=maximum_region,
        maximum_upper_source_cell_index=maximum_index,
        claim_boundary=(
            "The bulk coefficient is a directed fixed-background supersolution "
            "bound for the self-consistent spherical Hamiltonian mass equation "
            "with the certified field held fixed. The global test-source value "
            "also includes the centered fixed-background Nambu-Goto wall mass. "
            "It does not solve the lapse equation, field equation, or Israel "
            "junction conditions."
        ),
    )


def validated_constraint_coupling_record(
    shape: ValidatedSkyrmionConstraintShape,
    *,
    control_budget: Fraction,
    static_patch_radius_squared_over_newton: Fraction,
) -> dict[str, object]:
    """Return necessary and sufficient ``e^2`` floors for ``q<=beta``."""
    for name, value in (
        ("control_budget", control_budget),
        (
            "static_patch_radius_squared_over_newton",
            static_patch_radius_squared_over_newton,
        ),
    ):
        if not isinstance(value, Fraction) or value <= 0:
            raise ValueError(f"{name} must be a positive Fraction")
    if control_budget >= 1:
        raise ValueError("control_budget must be smaller than one")
    common = Fraction(2) / (
        shape.curvature
        * control_budget
        * static_patch_radius_squared_over_newton
    )
    exterior_test_source = common * shape.fixed_background_exterior_shape_lower
    sufficient_bulk = common * shape.sufficient_bulk_shape_upper
    sufficient_global_test_source = (
        common * shape.sufficient_test_source_global_shape_upper
    )
    return {
        "control_budget_beta": str(control_budget),
        "static_patch_radius_squared_over_newton": str(
            static_patch_radius_squared_over_newton
        ),
        "fixed_background_exterior_coupling_squared_floor_exact": str(
            exterior_test_source
        ),
        "fixed_background_exterior_coupling_squared_floor_float": float(
            exterior_test_source
        ),
        "sufficient_bulk_coupling_squared_lower_bound_exact": str(sufficient_bulk),
        "sufficient_bulk_coupling_squared_lower_bound_float": float(sufficient_bulk),
        "sufficient_global_test_source_coupling_squared_lower_bound_exact": str(
            sufficient_global_test_source
        ),
        "sufficient_global_test_source_coupling_squared_lower_bound_float": float(
            sufficient_global_test_source
        ),
        "interpretation": (
            "The directed bulk mass-function replay gives a sufficient e^2 "
            "floor for the self-consistent radial Hamiltonian-constraint metric "
            "budget with the certified field held fixed. The exterior and global "
            "values treat the fixed-background membrane mass as a test source."
        ),
    }
