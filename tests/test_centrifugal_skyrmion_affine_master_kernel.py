from fractions import Fraction
from math import cos, sin, sqrt

import pytest

from qgtoy.centrifugal_skyrmion_affine_master_kernel import (
    centrifugal_background_wall_stress_generic,
    centrifugal_completed_master_source_affine_kernel,
    centrifugal_completed_master_source_generic,
    centrifugal_completed_stress_affine_kernel,
    centrifugal_completed_stress_generic,
    centrifugal_moving_wall_master_affine_kernel,
    centrifugal_moving_wall_master_contribution_generic,
)
from qgtoy.centrifugal_skyrmion_completed_stress import (
    centrifugal_quadrupole_stress_amplitudes,
)
from qgtoy.static_patch_l2_master_source import static_l2_master_source_density
from qgtoy.centrifugal_skyrmion_membrane_stress import (
    moving_interface_singular_amplitudes,
)
from qgtoy.static_patch_l2_master_source import (
    canonical_l2_master_source_distribution,
)
from qgtoy.static_patch_l2_response import (
    l2_center_regular_solution,
    l2_center_regular_solution_derivative,
)
from qgtoy.validated_centrifugal_liouville_taylor import _CenteredTaylorModel
from qgtoy.validated_interval import RationalInterval, RationalPolynomial


def _stress_values(stress):
    return (
        stress.energy_density,
        stress.radial_pressure,
        stress.tangential_pressure,
        stress.radial_angular_shear,
        stress.angular_tracefree_stress,
    )


def _wall_values(contribution):
    singular = contribution.singular_stress
    source = contribution.master_source
    return (
        contribution.wall_displacement,
        contribution.bulk_energy_density_at_wall,
        singular.energy_density_delta,
        singular.energy_density_delta_prime,
        singular.radial_pressure_delta,
        singular.radial_pressure_delta_prime,
        singular.tangential_pressure_delta,
        singular.tangential_pressure_delta_prime,
        singular.radial_angular_shear_delta,
        singular.radial_angular_shear_delta_prime,
        singular.angular_tracefree_stress_delta,
        singular.angular_tracefree_stress_delta_prime,
        source.delta_second,
        source.delta_prime,
        source.delta,
        source.master_field_contact_delta,
        source.contact_free_delta_prime,
        source.contact_free_delta,
        source.contact_free_delta_without_bulk_endpoint,
        contribution.raw_contact_free_exterior_amplitude,
        contribution.bulk_energy_endpoint_amplitude,
        contribution.effective_wall_amplitude,
    )


def test_generic_float_stress_matches_existing_completed_formula() -> None:
    profile = 0.91
    values = {
        "radius": 1.37,
        "metric_factor": 0.942,
        "sine_profile": sin(profile),
        "cosine_profile": cos(profile),
        "profile_derivative": -0.48,
        "radial_field": 0.13,
        "radial_field_derivative": -0.07,
        "tangential_field": -0.04,
        "tangential_field_derivative": 0.09,
        "pion_mass_squared": 1.21,
    }
    generic = centrifugal_completed_stress_generic(**values)
    existing = centrifugal_quadrupole_stress_amplitudes(
        radius=values["radius"],
        metric_factor=values["metric_factor"],
        profile=profile,
        profile_derivative=values["profile_derivative"],
        radial_field=values["radial_field"],
        radial_field_derivative=values["radial_field_derivative"],
        tangential_field=values["tangential_field"],
        tangential_field_derivative=values["tangential_field_derivative"],
        pion_mass=1.1,
    )
    for name, value in zip(
        (
            "energy_density",
            "radial_pressure",
            "tangential_pressure",
            "radial_angular_shear",
            "angular_tracefree_stress",
        ),
        _stress_values(generic.total),
        strict=True,
    ):
        assert value == pytest.approx(existing[f"total_{name}"], abs=2.0e-15)


def test_affine_stress_coefficients_equal_exact_rational_basis_evaluations() -> None:
    background = {
        "radius": Fraction(7, 5),
        "metric_factor": Fraction(19, 20),
        "sine_profile": Fraction(3, 5),
        "cosine_profile": Fraction(4, 5),
        "profile_derivative": Fraction(-2, 5),
        "pion_mass_squared": Fraction(6, 5),
    }
    kernel = centrifugal_completed_stress_affine_kernel(**background)
    zero = Fraction(0)
    rigid_direct = centrifugal_completed_stress_generic(
        **background,
        radial_field=zero,
        radial_field_derivative=zero,
        tangential_field=zero,
        tangential_field_derivative=zero,
    ).total
    assert _stress_values(kernel.rigid) == _stress_values(rigid_direct)

    coefficient_blocks = (
        kernel.radial_field,
        kernel.radial_field_derivative,
        kernel.tangential_field,
        kernel.tangential_field_derivative,
    )
    for index, coefficient in enumerate(coefficient_blocks):
        basis = [zero] * 4
        basis[index] = Fraction(1)
        direct = centrifugal_completed_stress_generic(
            **background,
            radial_field=basis[0],
            radial_field_derivative=basis[1],
            tangential_field=basis[2],
            tangential_field_derivative=basis[3],
        ).total
        assert _stress_values(coefficient) == tuple(
            value - rigid
            for value, rigid in zip(
                _stress_values(direct), _stress_values(rigid_direct), strict=True
            )
        )

    arguments = (Fraction(2, 13), Fraction(-3, 17), Fraction(5, 19), Fraction(7, 23))
    evaluated = kernel.evaluate(
        radial_field=arguments[0],
        radial_field_derivative=arguments[1],
        tangential_field=arguments[2],
        tangential_field_derivative=arguments[3],
    )
    direct = centrifugal_completed_stress_generic(
        **background,
        radial_field=arguments[0],
        radial_field_derivative=arguments[1],
        tangential_field=arguments[2],
        tangential_field_derivative=arguments[3],
    ).total
    assert _stress_values(evaluated) == _stress_values(direct)
    assert kernel.l0 == (kernel.radial_field, kernel.tangential_field)
    assert kernel.l1 == (
        kernel.radial_field_derivative,
        kernel.tangential_field_derivative,
    )


def test_master_source_coefficients_equal_exact_rational_basis_evaluations() -> None:
    background = {
        "radius": Fraction(7, 5),
        "metric_factor": Fraction(19, 20),
        "metric_factor_derivative": Fraction(-7, 1000),
        "inverse_patch_radius_squared": Fraction(1, 400),
        "sine_profile": Fraction(3, 5),
        "cosine_profile": Fraction(4, 5),
        "profile_derivative": Fraction(-2, 5),
        "profile_second_derivative": Fraction(1, 7),
        "pion_mass_squared": Fraction(6, 5),
        "gravitational_coupling": Fraction(3, 2),
    }
    kernel = centrifugal_completed_master_source_affine_kernel(**background)
    names = (
        "radial_field",
        "radial_field_derivative",
        "radial_field_second_derivative",
        "tangential_field",
        "tangential_field_derivative",
    )
    zero_fields = {name: Fraction(0) for name in names}
    rigid_direct = centrifugal_completed_master_source_generic(
        **background, **zero_fields
    )
    assert kernel.rigid == rigid_direct
    for name in names:
        basis = dict(zero_fields)
        basis[name] = Fraction(1)
        direct = centrifugal_completed_master_source_generic(**background, **basis)
        assert getattr(kernel, name) == direct - rigid_direct

    fields = {
        "radial_field": Fraction(2, 13),
        "radial_field_derivative": Fraction(-3, 17),
        "radial_field_second_derivative": Fraction(11, 29),
        "tangential_field": Fraction(5, 19),
        "tangential_field_derivative": Fraction(7, 23),
    }
    assert kernel.evaluate(**fields) == centrifugal_completed_master_source_generic(
        **background, **fields
    )


def test_generic_master_jet_matches_independent_completed_stress_derivative() -> None:
    radius = 1.37
    patch_radius = 20.0
    inverse_patch_radius_squared = 1.0 / patch_radius**2
    profile = 0.91
    profile_derivative = -0.48
    profile_second_derivative = 0.17
    radial_field = 0.13
    radial_field_derivative = -0.07
    radial_field_second_derivative = 0.11
    tangential_field = -0.04
    tangential_field_derivative = 0.09
    pion_mass = 1.1
    coupling = 1.7

    def data(at_radius: float) -> tuple[float, dict[str, float]]:
        displacement = at_radius - radius
        local_profile = (
            profile
            + profile_derivative * displacement
            + profile_second_derivative * displacement**2 / 2.0
        )
        local_profile_derivative = (
            profile_derivative + profile_second_derivative * displacement
        )
        local_radial = (
            radial_field
            + radial_field_derivative * displacement
            + radial_field_second_derivative * displacement**2 / 2.0
        )
        local_radial_derivative = (
            radial_field_derivative + radial_field_second_derivative * displacement
        )
        local_tangential = tangential_field + tangential_field_derivative * displacement
        stress = centrifugal_quadrupole_stress_amplitudes(
            radius=at_radius,
            metric_factor=1.0 - at_radius**2 / patch_radius**2,
            profile=local_profile,
            profile_derivative=local_profile_derivative,
            radial_field=local_radial,
            radial_field_derivative=local_radial_derivative,
            tangential_field=local_tangential,
            tangential_field_derivative=tangential_field_derivative,
            pion_mass=pion_mass,
        )
        return local_profile, stress

    _, center = data(radius)
    step = 1.0e-5
    _, left = data(radius - step)
    _, right = data(radius + step)
    energy_derivative = (
        right["total_energy_density"] - left["total_energy_density"]
    ) / (2.0 * step)
    independent = static_l2_master_source_density(
        radius=radius,
        static_patch_radius=patch_radius,
        energy_density=center["total_energy_density"],
        energy_density_derivative=energy_derivative,
        radial_pressure=center["total_radial_pressure"],
        radial_angular_shear=center["total_radial_angular_shear"],
        angular_tracefree_stress=center["total_angular_tracefree_stress"],
        gravitational_coupling=coupling,
    )
    generic = centrifugal_completed_master_source_generic(
        radius=radius,
        metric_factor=1.0 - radius**2 / patch_radius**2,
        metric_factor_derivative=-2.0 * radius / patch_radius**2,
        inverse_patch_radius_squared=inverse_patch_radius_squared,
        sine_profile=sin(profile),
        cosine_profile=cos(profile),
        profile_derivative=profile_derivative,
        profile_second_derivative=profile_second_derivative,
        radial_field=radial_field,
        radial_field_derivative=radial_field_derivative,
        radial_field_second_derivative=radial_field_second_derivative,
        tangential_field=tangential_field,
        tangential_field_derivative=tangential_field_derivative,
        pion_mass_squared=pion_mass**2,
        gravitational_coupling=coupling,
    )
    assert generic == pytest.approx(independent, rel=2.0e-10, abs=2.0e-11)


def test_interval_and_centered_taylor_arithmetic_remain_supported() -> None:
    point = lambda value: RationalInterval.point(Fraction(value))  # noqa: E731
    interval_kernel = centrifugal_completed_stress_affine_kernel(
        radius=RationalInterval(Fraction(13, 10), Fraction(7, 5)),
        metric_factor=RationalInterval(Fraction(9, 10), Fraction(19, 20)),
        sine_profile=RationalInterval(Fraction(1, 2), Fraction(3, 5)),
        cosine_profile=RationalInterval(Fraction(4, 5), Fraction(9, 10)),
        profile_derivative=RationalInterval(Fraction(-1, 2), Fraction(-2, 5)),
        pion_mass_squared=point(1),
    )
    assert isinstance(interval_kernel.rigid.energy_density, RationalInterval)
    assert isinstance(interval_kernel.radial_field.energy_density, RationalInterval)
    interval_master = centrifugal_completed_master_source_affine_kernel(
        radius=RationalInterval(Fraction(13, 10), Fraction(7, 5)),
        metric_factor=RationalInterval(Fraction(9, 10), Fraction(19, 20)),
        metric_factor_derivative=RationalInterval(Fraction(-1, 100), Fraction(0)),
        inverse_patch_radius_squared=point(Fraction(1, 400)),
        sine_profile=RationalInterval(Fraction(1, 2), Fraction(3, 5)),
        cosine_profile=RationalInterval(Fraction(4, 5), Fraction(9, 10)),
        profile_derivative=RationalInterval(Fraction(-1, 2), Fraction(-2, 5)),
        profile_second_derivative=RationalInterval(Fraction(0), Fraction(1, 5)),
        pion_mass_squared=point(1),
        gravitational_coupling=point(1),
    )
    assert isinstance(interval_master.rigid, RationalInterval)
    assert isinstance(interval_master.radial_field_second_derivative, RationalInterval)

    model = _CenteredTaylorModel.from_polynomial(
        RationalPolynomial((Fraction(7, 5), Fraction(1, 100))),
        degree_limit=8,
    )
    constant = lambda value: _CenteredTaylorModel.constant(  # noqa: E731
        Fraction(value), degree_limit=8
    )
    model_kernel = centrifugal_completed_stress_affine_kernel(
        radius=model,
        metric_factor=constant(Fraction(19, 20)),
        sine_profile=constant(Fraction(3, 5)),
        cosine_profile=constant(Fraction(4, 5)),
        profile_derivative=constant(Fraction(-2, 5)),
        pion_mass_squared=constant(1),
    )
    assert isinstance(model_kernel.rigid.energy_density, _CenteredTaylorModel)
    assert model_kernel.rigid.energy_density.range().lower < 0


def test_generic_moving_wall_pipeline_matches_existing_float_modules() -> None:
    wall_radius = 4.0
    patch_radius = 20.0
    inverse_patch_radius_squared = 1.0 / patch_radius**2
    lapse = 1.0 - wall_radius**2 * inverse_patch_radius_squared
    lapse_p = -2.0 * wall_radius * inverse_patch_radius_squared
    profile = 0.0
    profile_derivative = -0.0878758
    radial_field = 0.023
    radial_field_derivative = -0.014
    tangential_field = -0.008
    tangential_field_derivative = 0.005
    pion_mass_squared = 1.0
    tension = 0.031
    displacement_per_f = -1.0 / profile_derivative
    ratio = wall_radius / patch_radius
    weight = (
        2.0 * patch_radius * l2_center_regular_solution(ratio) / 15.0
    )
    weight_p = 2.0 * l2_center_regular_solution_derivative(ratio) / 15.0
    generic = centrifugal_moving_wall_master_contribution_generic(
        wall_radius=wall_radius,
        wall_metric_factor=lapse,
        wall_metric_factor_derivative=lapse_p,
        sqrt_wall_metric_factor=lapse**0.5,
        inverse_patch_radius_squared=inverse_patch_radius_squared,
        sine_profile=sin(profile),
        cosine_profile=cos(profile),
        profile_derivative=profile_derivative,
        radial_field=radial_field,
        radial_field_derivative=radial_field_derivative,
        tangential_field=tangential_field,
        tangential_field_derivative=tangential_field_derivative,
        pion_mass_squared=pion_mass_squared,
        membrane_tension=tension,
        wall_displacement_per_radial_field=displacement_per_f,
        wall_green_weight=weight,
        wall_green_weight_derivative=weight_p,
        gravitational_coupling=1.0,
    )
    background = centrifugal_background_wall_stress_generic(
        radius=wall_radius,
        metric_factor=lapse,
        sine_profile=sin(profile),
        cosine_profile=cos(profile),
        profile_derivative=profile_derivative,
        pion_mass_squared=pion_mass_squared,
    )
    displacement = displacement_per_f * radial_field
    singular = moving_interface_singular_amplitudes(
        wall_radius=wall_radius,
        wall_metric_factor=lapse,
        wall_metric_factor_derivative=lapse_p,
        membrane_tension=tension,
        wall_displacement_coefficient=displacement,
        background_energy_density=background.energy_density,
        background_radial_pressure=background.radial_pressure,
        background_tangential_pressure=background.tangential_pressure,
    )
    distribution = canonical_l2_master_source_distribution(
        wall_radius=wall_radius,
        static_patch_radius=patch_radius,
        bulk_energy_density_at_wall=generic.bulk_energy_density_at_wall,
        energy_density_delta=singular["energy_density_delta"],
        energy_density_delta_prime=singular["energy_density_delta_prime"],
        radial_pressure_delta=singular["radial_pressure_delta"],
        radial_angular_shear_delta=singular["radial_angular_shear_delta"],
    )
    assert generic.wall_displacement == pytest.approx(displacement)
    assert generic.master_source.delta_second == pytest.approx(
        distribution["master_source_delta_second_coefficient"]
    )
    assert generic.master_source.delta_prime == pytest.approx(
        distribution["master_source_delta_prime_coefficient"]
    )
    assert generic.master_source.delta == pytest.approx(
        distribution["master_source_delta_coefficient"]
    )
    assert generic.master_source.contact_free_delta_prime == pytest.approx(
        distribution["contact_free_delta_prime_coefficient"]
    )
    assert generic.master_source.contact_free_delta == pytest.approx(
        distribution["contact_free_delta_coefficient"]
    )


def test_affine_wall_coefficients_and_gamma_b_are_exact_rational_identities() -> None:
    background = {
        "wall_radius": Fraction(3),
        "wall_metric_factor": Fraction(16, 25),
        "wall_metric_factor_derivative": Fraction(-6, 25),
        "sqrt_wall_metric_factor": Fraction(4, 5),
        "inverse_patch_radius_squared": Fraction(1, 25),
        "sine_profile": Fraction(3, 5),
        "cosine_profile": Fraction(4, 5),
        "profile_derivative": Fraction(-2, 5),
        "pion_mass_squared": Fraction(6, 5),
        "membrane_tension": Fraction(7, 13),
        "wall_displacement_per_radial_field": Fraction(5, 2),
        "wall_green_weight": Fraction(11, 17),
        "wall_green_weight_derivative": Fraction(-7, 19),
        "gravitational_coupling": Fraction(3, 2),
    }
    kernel = centrifugal_moving_wall_master_affine_kernel(**background)
    names = (
        "radial_field",
        "radial_field_derivative",
        "tangential_field",
        "tangential_field_derivative",
    )
    zero_fields = {name: Fraction(0) for name in names}
    rigid_direct = centrifugal_moving_wall_master_contribution_generic(
        **background, **zero_fields
    )
    assert _wall_values(kernel.rigid) == _wall_values(rigid_direct)
    for name in names:
        fields = dict(zero_fields)
        fields[name] = Fraction(1)
        direct = centrifugal_moving_wall_master_contribution_generic(
            **background, **fields
        )
        expected = tuple(
            value - rigid
            for value, rigid in zip(
                _wall_values(direct), _wall_values(rigid_direct), strict=True
            )
        )
        assert _wall_values(getattr(kernel, name)) == expected

    zero = Fraction(0)
    assert kernel.rigid.effective_wall_amplitude == zero
    assert kernel.radial_field_derivative.effective_wall_amplitude == zero
    assert kernel.tangential_field.effective_wall_amplitude == zero
    assert kernel.tangential_field_derivative.effective_wall_amplitude == zero
    assert kernel.response_wall_trace_gamma_b == (
        kernel.radial_field.raw_contact_free_exterior_amplitude
        - kernel.radial_field.bulk_energy_endpoint_amplitude
    )
    assert kernel.wall_displacement_per_radial_field == Fraction(5, 2)
    assert kernel.response_wall_trace_gamma_b != (
        kernel.wall_displacement_per_radial_field
    )


def test_exact_rational_wall_formula_matches_independent_manual_algebra() -> None:
    r = Fraction(3)
    lapse = Fraction(16, 25)
    lapse_p = Fraction(-6, 25)
    root_lapse = Fraction(4, 5)
    inverse_patch_squared = Fraction(1, 25)
    sine = Fraction(3, 5)
    cosine = Fraction(4, 5)
    profile_p = Fraction(-2, 5)
    mass_squared = Fraction(6, 5)
    tension = Fraction(7, 13)
    displacement_per_f = Fraction(5, 2)
    weight = Fraction(11, 17)
    weight_p = Fraction(-7, 19)
    coupling = Fraction(3, 2)
    f = Fraction(2, 11)
    f_p = Fraction(-3, 13)
    g = Fraction(5, 17)
    g_p = Fraction(7, 19)

    result = centrifugal_moving_wall_master_contribution_generic(
        wall_radius=r,
        wall_metric_factor=lapse,
        wall_metric_factor_derivative=lapse_p,
        sqrt_wall_metric_factor=root_lapse,
        inverse_patch_radius_squared=inverse_patch_squared,
        sine_profile=sine,
        cosine_profile=cosine,
        profile_derivative=profile_p,
        radial_field=f,
        radial_field_derivative=f_p,
        tangential_field=g,
        tangential_field_derivative=g_p,
        pion_mass_squared=mass_squared,
        membrane_tension=tension,
        wall_displacement_per_radial_field=displacement_per_f,
        wall_green_weight=weight,
        wall_green_weight_derivative=weight_p,
        gravitational_coupling=coupling,
    )

    radial_strain = lapse * profile_p**2
    tangential_strain = sine**2 / r**2
    potential_energy = mass_squared * (1 - cosine) / 4
    background_energy = (
        radial_strain / 8
        + tangential_strain / 4
        + radial_strain * tangential_strain
        + tangential_strain**2 / 2
        + potential_energy
    )
    background_radial = (
        radial_strain / 8
        - tangential_strain / 4
        + radial_strain * tangential_strain
        - tangential_strain**2 / 2
        - potential_energy
    )
    background_tangential = (
        -radial_strain / 8 + tangential_strain**2 / 2 - potential_energy
    )
    sigma_rotation = sine**2 / (8 * lapse)
    skyrme_rotation = sine**2 / (2 * lapse)
    rigid_energy = -sigma_rotation - skyrme_rotation * (
        radial_strain + tangential_strain
    )
    radial_variation = 2 * lapse * profile_p * f_p
    angular_variation = 2 * sine * (2 * f * cosine - 3 * g) / r**2
    deformation_energy = (
        (radial_variation + angular_variation) / 8
        + tangential_strain * radial_variation
        + (radial_strain + tangential_strain) * angular_variation / 2
        + mass_squared * f * sine / 4
    )
    bulk_energy = rigid_energy + deformation_energy

    displacement = displacement_per_f * f
    shell_rho = tension * displacement * lapse_p / (2 * root_lapse)
    shell_rho_p = -tension * displacement * root_lapse
    rho_delta = displacement * background_energy + shell_rho
    radial_delta = displacement * background_radial
    tangential_delta = displacement * background_tangential - shell_rho
    shear_delta = shell_rho_p
    assert result.singular_stress.energy_density_delta == rho_delta
    assert result.singular_stress.energy_density_delta_prime == shell_rho_p
    assert result.singular_stress.radial_pressure_delta == radial_delta
    assert result.singular_stress.tangential_pressure_delta == tangential_delta
    assert result.singular_stress.radial_angular_shear_delta == shear_delta

    coefficient_a = r**2 * lapse / 6
    coefficient_a_p = r * lapse / 3 + r**2 * lapse_p / 6
    lapse_pp = -2 * inverse_patch_squared
    coefficient_a_pp = (
        lapse / 3 + 2 * r * lapse_p / 3 + r**2 * lapse_pp / 6
    )
    coefficient_b = r * (1 + 4 * r**2 * inverse_patch_squared) / 6
    coefficient_b_p = (1 + 12 * r**2 * inverse_patch_squared) / 6
    delta_second = coupling * (-coefficient_a * shell_rho_p)
    delta_prime = coupling * (
        -coefficient_a * rho_delta
        + 2 * coefficient_a_p * shell_rho_p
        + coefficient_b * shell_rho_p
    )
    delta_without_bulk = coupling * (
        coefficient_a_p * rho_delta
        - coefficient_a_pp * shell_rho_p
        + coefficient_b * rho_delta
        - coefficient_b_p * shell_rho_p
        - r * radial_delta / 2
        - shear_delta
    )
    delta = coupling * coefficient_a * bulk_energy + delta_without_bulk
    off_prime = delta_prime + delta_second * lapse_p / lapse
    off_without_bulk = delta_without_bulk + 6 * delta_second / (r**2 * lapse)
    off_delta = coupling * coefficient_a * bulk_energy + off_without_bulk
    raw = weight * off_delta - weight_p * off_prime
    endpoint = coupling * weight * coefficient_a * bulk_energy
    effective = weight * off_without_bulk - weight_p * off_prime
    assert result.bulk_energy_density_at_wall == bulk_energy
    assert result.master_source.delta_second == delta_second
    assert result.master_source.delta_prime == delta_prime
    assert result.master_source.delta == delta
    assert result.master_source.contact_free_delta_prime == off_prime
    assert result.master_source.contact_free_delta == off_delta
    assert (
        result.master_source.contact_free_delta_without_bulk_endpoint
        == off_without_bulk
    )
    assert result.raw_contact_free_exterior_amplitude == raw
    assert result.bulk_energy_endpoint_amplitude == endpoint
    assert result.effective_wall_amplitude == effective
    assert raw - endpoint == effective


def test_wall_kernel_supports_interval_and_centered_taylor_scalars() -> None:
    point = lambda value: RationalInterval.point(Fraction(value))  # noqa: E731
    interval_kernel = centrifugal_moving_wall_master_affine_kernel(
        wall_radius=point(3),
        wall_metric_factor=RationalInterval(Fraction(63, 100), Fraction(13, 20)),
        wall_metric_factor_derivative=RationalInterval(
            Fraction(-1, 4), Fraction(-23, 100)
        ),
        sqrt_wall_metric_factor=RationalInterval(
            Fraction(79, 100), Fraction(81, 100)
        ),
        inverse_patch_radius_squared=point(Fraction(1, 25)),
        sine_profile=RationalInterval(Fraction(1, 2), Fraction(3, 5)),
        cosine_profile=RationalInterval(Fraction(4, 5), Fraction(9, 10)),
        profile_derivative=RationalInterval(Fraction(-1, 2), Fraction(-2, 5)),
        pion_mass_squared=point(1),
        membrane_tension=point(Fraction(1, 20)),
        wall_displacement_per_radial_field=RationalInterval(
            Fraction(2), Fraction(5, 2)
        ),
        wall_green_weight=point(Fraction(3, 10)),
        wall_green_weight_derivative=point(Fraction(1, 5)),
        gravitational_coupling=point(1),
    )
    assert isinstance(
        interval_kernel.response_wall_trace_gamma_b, RationalInterval
    )
    assert isinstance(
        interval_kernel.radial_field.master_source.contact_free_delta,
        RationalInterval,
    )
    interval_zero = point(0)
    assert (
        interval_kernel.radial_field_derivative.effective_wall_amplitude
        == interval_zero
    )
    assert interval_kernel.tangential_field.effective_wall_amplitude == interval_zero
    assert (
        interval_kernel.tangential_field_derivative.effective_wall_amplitude
        == interval_zero
    )

    model = _CenteredTaylorModel.from_polynomial(
        RationalPolynomial((Fraction(3), Fraction(1, 100))),
        degree_limit=8,
    )
    constant = lambda value: _CenteredTaylorModel.constant(  # noqa: E731
        Fraction(value), degree_limit=8
    )
    model_kernel = centrifugal_moving_wall_master_affine_kernel(
        wall_radius=model,
        wall_metric_factor=constant(Fraction(16, 25)),
        wall_metric_factor_derivative=constant(Fraction(-6, 25)),
        sqrt_wall_metric_factor=constant(Fraction(4, 5)),
        inverse_patch_radius_squared=constant(Fraction(1, 25)),
        sine_profile=constant(Fraction(3, 5)),
        cosine_profile=constant(Fraction(4, 5)),
        profile_derivative=constant(Fraction(-2, 5)),
        pion_mass_squared=constant(1),
        membrane_tension=constant(Fraction(1, 20)),
        wall_displacement_per_radial_field=constant(Fraction(5, 2)),
        wall_green_weight=constant(Fraction(3, 10)),
        wall_green_weight_derivative=constant(Fraction(1, 5)),
        gravitational_coupling=constant(1),
    )
    gamma_range = model_kernel.response_wall_trace_gamma_b.range()
    assert gamma_range.lower <= gamma_range.upper


def test_default_wall_trace_is_not_the_wall_displacement_multiplier() -> None:
    wall_radius = 4.0
    inverse_patch_radius_squared = 0.0025
    patch_radius = 1.0 / sqrt(inverse_patch_radius_squared)
    lapse = 1.0 - wall_radius**2 * inverse_patch_radius_squared
    profile_derivative = -0.08787579978871057
    ratio = wall_radius / patch_radius
    kernel = centrifugal_moving_wall_master_affine_kernel(
        wall_radius=wall_radius,
        wall_metric_factor=lapse,
        wall_metric_factor_derivative=(
            -2.0 * inverse_patch_radius_squared * wall_radius
        ),
        sqrt_wall_metric_factor=sqrt(lapse),
        inverse_patch_radius_squared=inverse_patch_radius_squared,
        sine_profile=0.0,
        cosine_profile=1.0,
        profile_derivative=profile_derivative,
        pion_mass_squared=1.0,
        membrane_tension=0.001931779647,
        wall_displacement_per_radial_field=-1.0 / profile_derivative,
        wall_green_weight=(
            2.0 * patch_radius * l2_center_regular_solution(ratio) / 15.0
        ),
        wall_green_weight_derivative=(
            2.0 * l2_center_regular_solution_derivative(ratio) / 15.0
        ),
        gravitational_coupling=1.0,
    )
    assert kernel.wall_displacement_per_radial_field == pytest.approx(
        11.3796972819
    )
    assert kernel.response_wall_trace_gamma_b == pytest.approx(
        0.00282575297583
    )
    assert abs(kernel.response_wall_trace_gamma_b) < (
        abs(kernel.wall_displacement_per_radial_field) / 1000.0
    )
