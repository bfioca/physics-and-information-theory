import math

import pytest

from qgtoy.global_so3_reference_risk import (
    hard_cutoff_orientation_risk_lower_bound,
)
from qgtoy.locality_reference_leakage import (
    collective_mode_leakage_from_casimir,
    compression_commutator_budget,
    locality_reference_leakage_certificate,
    minimum_integer_spin_from_risk,
    operational_collective_mode_leakage_bound,
    operational_locality_leakage_bound,
    pairwise_state_weighted_collective_mode_bound,
    required_mean_casimir_for_risk,
    self_adjoint_locality_reference_leakage_bound,
    disjoint_block_ferromagnetic_code_record,
    three_cell_ferromagnetic_state_record,
)


def _matrix_product(left, right):
    return tuple(
        tuple(
            sum(left[row][inner] * right[inner][column] for inner in range(3))
            for column in range(3)
        )
        for row in range(3)
    )


def _matrix_difference(left, right):
    return tuple(
        tuple(left[row][column] - right[row][column] for column in range(3))
        for row in range(3)
    )


def _matrix_sum(*matrices):
    return tuple(
        tuple(sum(matrix[row][column] for matrix in matrices) for column in range(3))
        for row in range(3)
    )


def _matrix_scale(scale, matrix):
    return tuple(
        tuple(scale * matrix[row][column] for column in range(3))
        for row in range(3)
    )


def _commutator(left, right):
    return _matrix_difference(
        _matrix_product(left, right),
        _matrix_product(right, left),
    )


def _outer(vector):
    return tuple(
        tuple(vector[row] * vector[column] for column in range(3))
        for row in range(3)
    )


def _assert_matrices_close(left, right, tolerance=1.0e-13):
    for row in range(3):
        for column in range(3):
            assert abs(left[row][column] - right[row][column]) <= tolerance


def _dense_product(left, right):
    return tuple(
        tuple(
            sum(
                left[row][inner] * right[inner][column]
                for inner in range(len(right))
            )
            for column in range(len(right[0]))
        )
        for row in range(len(left))
    )


def _dense_adjoint(matrix):
    return tuple(
        tuple(matrix[row][column].conjugate() for row in range(len(matrix)))
        for column in range(len(matrix[0]))
    )


def _dense_sum(*matrices):
    return tuple(
        tuple(
            sum(matrix[row][column] for matrix in matrices)
            for column in range(len(matrices[0][0]))
        )
        for row in range(len(matrices[0]))
    )


def _dense_scale(scale, matrix):
    return tuple(
        tuple(scale * value for value in row)
        for row in matrix
    )


def _dense_difference(left, right):
    return _dense_sum(left, _dense_scale(-1.0, right))


def _dense_identity(dimension):
    return tuple(
        tuple(1.0 if row == column else 0.0 for column in range(dimension))
        for row in range(dimension)
    )


def _dense_kron(left, right):
    return tuple(
        tuple(
            left[left_row][left_column] * right[right_row][right_column]
            for left_column in range(len(left[0]))
            for right_column in range(len(right[0]))
        )
        for left_row in range(len(left))
        for right_row in range(len(right))
    )


def _site_operator(single_site, site, site_count):
    result = ((1.0,),)
    identity = _dense_identity(2)
    for current_site in range(site_count):
        result = _dense_kron(
            result,
            single_site if current_site == site else identity,
        )
    return result


def _dicke_isometry(site_count):
    rows = []
    for basis_index in range(2**site_count):
        down_count = basis_index.bit_count()
        row = [0.0] * (site_count + 1)
        row[down_count] = 1.0 / math.sqrt(
            math.comb(site_count, down_count)
        )
        rows.append(tuple(row))
    return tuple(rows)


def _spin_matrices(site_count):
    dimension = site_count + 1
    spin = site_count / 2.0
    jx = [[0j] * dimension for _ in range(dimension)]
    jy = [[0j] * dimension for _ in range(dimension)]
    jz = [[0j] * dimension for _ in range(dimension)]
    for down_count in range(dimension):
        jz[down_count][down_count] = spin - down_count
        if down_count + 1 < dimension:
            coefficient = 0.5 * math.sqrt(
                (down_count + 1) * (site_count - down_count)
            )
            jx[down_count + 1][down_count] = coefficient
            jx[down_count][down_count + 1] = coefficient
            jy[down_count + 1][down_count] = 1j * coefficient
            jy[down_count][down_count + 1] = -1j * coefficient
    return tuple(map(tuple, jx)), tuple(map(tuple, jy)), tuple(map(tuple, jz))


def _assert_dense_close(left, right, tolerance=1.0e-11):
    assert len(left) == len(right)
    assert len(left[0]) == len(right[0])
    for row in range(len(left)):
        for column in range(len(left[0])):
            assert abs(left[row][column] - right[row][column]) <= tolerance


def test_exact_compression_identity_for_commuting_ambient_observables():
    inverse_root_three = 1.0 / math.sqrt(3.0)
    normal = (inverse_root_three,) * 3
    identity = (
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, 1.0),
    )
    q = _outer(normal)
    p = _matrix_difference(identity, q)
    a = (
        (1.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (0.0, 0.0, -1.0),
    )
    b = (
        (0.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, -1.0),
    )
    assert _commutator(a, b) == (
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
    )

    pap = _matrix_product(_matrix_product(p, a), p)
    pbp = _matrix_product(_matrix_product(p, b), p)
    left = _commutator(pap, pbp)
    right = _matrix_sum(
        _matrix_product(_matrix_product(p, _commutator(a, b)), p),
        _matrix_product(
            _matrix_product(_matrix_product(_matrix_product(p, b), q), a),
            p,
        ),
        _matrix_scale(
            -1.0,
            _matrix_product(
                _matrix_product(_matrix_product(_matrix_product(p, a), q), b),
                p,
            ),
        ),
    )
    _assert_matrices_close(left, right)
    assert any(
        abs(left[row][column]) > 1.0e-6
        for row in range(3)
        for column in range(3)
    )


def test_directed_and_self_adjoint_bounds_have_explicit_constants():
    directed = compression_commutator_budget(
        generator_commutator_norm=1.0,
        generator_norm_a=1.0,
        generator_norm_b=1.0,
        gain_a=1.0,
        gain_b=1.0,
        leakage_a_out=1.0,
        leakage_a_in=1.0,
        leakage_b_out=1.0,
        leakage_b_in=1.0,
    )
    assert directed["nonabelian_signal"] == 1.0
    assert directed["directed_leakage_budget"] == 2.0
    assert directed["supplied_bounds_satisfy_theorem"] is True

    approximate = self_adjoint_locality_reference_leakage_bound(
        maximum_spin=4.0,
        gain_a=0.5,
        gain_b=0.5,
        locality_defect=0.1,
        compression_error_a=0.01,
        compression_error_b=0.02,
    )
    expected_approximation = 2.0 * 4.0 * (0.5 * 0.01 + 0.5 * 0.02)
    expected_approximation += 2.0 * 0.01 * 0.02
    assert approximate["nonabelian_signal"] == 1.0
    assert math.isclose(
        approximate["compression_approximation_budget"],
        expected_approximation,
    )
    assert approximate["positive_tradeoff"] is True


def test_pairwise_state_weighted_bound_can_be_saturated_by_supplied_data():
    record = pairwise_state_weighted_collective_mode_bound(
        generator_second_moment=4.0,
        maximum_spin=2.0,
        gain_a=1.0,
        gain_b=1.0,
        local_operator_norm_a=2.0,
        local_operator_norm_b=2.0,
        leakage_weight_a=0.25,
        leakage_weight_b=0.25,
    )
    assert record["target_commutator_rms"] == 2.0
    assert record["leakage_rms_budget"] == 2.0
    assert abs(record["inequality_slack"]) < 1.0e-15


def test_three_cell_exact_and_robust_state_weighted_bounds():
    exact = collective_mode_leakage_from_casimir(
        mean_casimir=6.0,
        response_gain=1.0,
        local_operator_norm=2.0,
    )
    assert exact["exact_case_uses_direct_factor_four"] is True
    assert exact["minimum_total_off_code_weight"] == 0.375
    assert exact["minimum_normalized_total_off_code_weight"] == 0.09375
    assert math.isclose(
        exact["minimum_uniform_leakage_amplitude_from_consistency"],
        (6.0 / 12.0) ** 0.25,
    )

    robust = collective_mode_leakage_from_casimir(
        mean_casimir=6.0,
        response_gain=1.0,
        local_operator_norm=2.0,
        maximum_spin=2.0,
        locality_defect=0.01,
        compression_error=0.001,
        young_parameter=0.25,
    )
    assert robust["exact_case_uses_direct_factor_four"] is False
    assert 0.0 < robust["minimum_total_off_code_weight"] < 0.375

    certified_cap = collective_mode_leakage_from_casimir(
        mean_casimir=6.0,
        response_gain=1.0,
        local_operator_norm=2.0,
        leakage_amplitude_cap=1.0,
    )
    assert certified_cap["minimum_total_off_code_weight"] == 1.5
    assert certified_cap[
        "certified_cap_is_consistent_with_required_weight"
    ] is True

    inconsistent_cap = collective_mode_leakage_from_casimir(
        mean_casimir=100.0,
        response_gain=1.0,
        local_operator_norm=2.0,
        leakage_amplitude_cap=0.1,
    )
    assert inconsistent_cap[
        "certified_cap_is_consistent_with_required_weight"
    ] is False


def test_global_risk_compositions_use_existing_w3_bounds():
    assert required_mean_casimir_for_risk(0.01) == 5.75
    resource = minimum_integer_spin_from_risk(0.375)
    assert resource["hard_cutoff_integer_spin_requirement"] == 1
    for cutoff in (0, 1, 2, 4, 8):
        risk = hard_cutoff_orientation_risk_lower_bound(cutoff)
        record = minimum_integer_spin_from_risk(risk)
        assert record["hard_cutoff_integer_spin_requirement"] == cutoff

    norm_bound = operational_locality_leakage_bound(
        risk_budget=0.01,
        gain_a=1.0,
        gain_b=1.0,
    )
    assert norm_bound["risk_resource_requirement"][
        "binding_integer_spin_requirement"
    ] > 0
    assert norm_bound["locality_reference_leakage_tradeoff"][
        "minimum_maximum_leakage_amplitude"
    ] > 0.0

    state_bound = operational_collective_mode_leakage_bound(
        risk_budget=0.01,
        response_gain=1.0 / 15.0,
        local_operator_norm=1.0,
        maximum_spin=15.0,
    )
    expected = ((1.0 / 15.0) ** 4) * 5.75 / 4.0
    assert math.isclose(
        state_bound["state_weighted_leakage"][
            "minimum_total_off_code_weight"
        ],
        expected,
    )
    assert state_bound["declared_parameters_are_not_ruled_out"] is True

    vacuous_calibration = operational_collective_mode_leakage_bound(
        risk_budget=0.01,
        response_gain=0.25,
        local_operator_norm=1.0,
        maximum_spin=15.0,
    )
    assert vacuous_calibration[
        "calibration_allows_minimum_required_spin"
    ] is False
    assert vacuous_calibration["declared_parameters_are_not_ruled_out"] is False


def test_disjoint_block_ferromagnetic_family_is_distributed_and_near_sharp():
    two_sites = disjoint_block_ferromagnetic_code_record(2)
    assert two_sites["code_spin_exact"] == "1"
    assert two_sites["leakage_squared_exact"] == "1"
    assert two_sites["sharpness_ratio_exact"] == "2"
    assert two_sites["microscopic_commutator_is_zero"] is True

    four_sites = disjoint_block_ferromagnetic_code_record(4)
    assert four_sites["leakage_squared_exact"] == "4/3"
    assert four_sites["sharpness_ratio_exact"] == "4/3"

    large = disjoint_block_ferromagnetic_code_record(128)
    assert large["sharpness_ratio_exact"] == "128/127"
    assert large["relative_leakage_squared_exact"] == "1/127"
    assert large["sharpness_ratio"] < 1.01

    buffered = disjoint_block_ferromagnetic_code_record(128, buffer_sites=2)
    assert buffered["buffer_sites"] == 2
    assert buffered["sharpness_ratio"] < 1.05


@pytest.mark.parametrize(
    ("site_count", "buffer_sites"),
    ((2, 0), (4, 0), (4, 2), (6, 2)),
)
def test_disjoint_block_formulas_against_dicke_matrices(
    site_count,
    buffer_sites,
):
    sigma_x_over_two = (
        (0.0, 0.5),
        (0.5, 0.0),
    )
    sigma_y_over_two = (
        (0.0, -0.5j),
        (0.5j, 0.0),
    )
    block_size = (site_count - buffer_sites) // 2
    block_scale = site_count / block_size
    ambient_dimension = 2**site_count
    zero = tuple(
        tuple(0j for _ in range(ambient_dimension))
        for _ in range(ambient_dimension)
    )
    a = zero
    b = zero
    for site in range(block_size):
        a = _dense_sum(
            a,
            _dense_scale(
                block_scale,
                _site_operator(sigma_x_over_two, site, site_count),
            ),
        )
    for site in range(site_count - block_size, site_count):
        b = _dense_sum(
            b,
            _dense_scale(
                block_scale,
                _site_operator(sigma_y_over_two, site, site_count),
            ),
        )

    _assert_dense_close(
        _dense_product(a, b),
        _dense_product(b, a),
    )
    v = _dicke_isometry(site_count)
    v_adjoint = _dense_adjoint(v)
    jx, jy, jz = _spin_matrices(site_count)
    compressed_a = _dense_product(_dense_product(v_adjoint, a), v)
    compressed_b = _dense_product(_dense_product(v_adjoint, b), v)
    _assert_dense_close(compressed_a, jx)
    _assert_dense_close(compressed_b, jy)

    a_v = _dense_product(a, v)
    b_v = _dense_product(b, v)
    q_a_v = _dense_difference(a_v, _dense_product(v, compressed_a))
    q_b_v = _dense_difference(b_v, _dense_product(v, compressed_b))
    leakage_gram = _dense_product(_dense_adjoint(q_a_v), q_a_v)
    spin = site_count / 2.0
    coefficient = (site_count - block_size) / (
        block_size * (site_count - 1)
    )
    predicted_gram = _dense_scale(
        coefficient,
        _dense_difference(
            _dense_scale(spin * spin, _dense_identity(site_count + 1)),
            _dense_product(jx, jx),
        ),
    )
    _assert_dense_close(leakage_gram, predicted_gram)

    cross = _dense_product(
        _dense_product(v_adjoint, b),
        q_a_v,
    )
    anticommutator = _dense_sum(
        _dense_product(jx, jy),
        _dense_product(jy, jx),
    )
    predicted_cross = _dense_sum(
        _dense_scale(1.0 / (2.0 * (site_count - 1)), anticommutator),
        _dense_scale(0.5j, jz),
    )
    _assert_dense_close(cross, predicted_cross)

    reverse_cross = _dense_product(
        _dense_product(v_adjoint, a),
        q_b_v,
    )
    predicted_reverse = _dense_sum(
        _dense_scale(1.0 / (2.0 * (site_count - 1)), anticommutator),
        _dense_scale(-0.5j, jz),
    )
    _assert_dense_close(reverse_cross, predicted_reverse)


def test_three_cell_ferromagnet_checks_state_weighted_scaling():
    six_sites = three_cell_ferromagnetic_state_record(6)
    assert six_sites["code_spin_exact"] == "3"
    assert six_sites["leakage_amplitude_squared_exact"] == "18/5"
    assert six_sites["isotropic_state_leakage_weight_each_exact"] == "2"
    assert six_sites["total_leakage_weight_exact"] == "6"
    assert six_sites["state_bound_with_leakage_cap_exact"] == "5/6"
    assert six_sites["actual_to_leakage_cap_bound_ratio_exact"] == "36/5"

    large = three_cell_ferromagnetic_state_record(120)
    assert 7.0 < large["actual_to_leakage_cap_bound_ratio"] < 9.0
    assert large["asymptotic_ratio"] == 8.0
    assert "Only the sum" in large["claim_boundary"]


def test_three_cell_formulas_against_six_site_dicke_matrices():
    site_count = 6
    block_size = site_count // 3
    block_scale = site_count / block_size
    sigma_x_over_two = (
        (0.0, 0.5),
        (0.5, 0.0),
    )
    sigma_y_over_two = (
        (0.0, -0.5j),
        (0.5j, 0.0),
    )
    sigma_z_over_two = (
        (0.5, 0.0),
        (0.0, -0.5),
    )
    ambient_dimension = 2**site_count
    zero = tuple(
        tuple(0j for _ in range(ambient_dimension))
        for _ in range(ambient_dimension)
    )
    observables = []
    for block, single_site in enumerate(
        (sigma_x_over_two, sigma_y_over_two, sigma_z_over_two)
    ):
        observable = zero
        for site in range(block * block_size, (block + 1) * block_size):
            observable = _dense_sum(
                observable,
                _dense_scale(
                    block_scale,
                    _site_operator(single_site, site, site_count),
                ),
            )
        observables.append(observable)

    for left in range(3):
        for right in range(left + 1, 3):
            _assert_dense_close(
                _dense_product(observables[left], observables[right]),
                _dense_product(observables[right], observables[left]),
            )

    v = _dicke_isometry(site_count)
    v_adjoint = _dense_adjoint(v)
    generators = _spin_matrices(site_count)
    leakage_grams = []
    spin = site_count / 2.0
    coefficient = 2.0 / (site_count - 1)
    identity = _dense_identity(site_count + 1)
    for observable, generator in zip(observables, generators):
        compressed = _dense_product(_dense_product(v_adjoint, observable), v)
        _assert_dense_close(compressed, generator)
        observable_v = _dense_product(observable, v)
        q_observable_v = _dense_difference(
            observable_v,
            _dense_product(v, compressed),
        )
        gram = _dense_product(
            _dense_adjoint(q_observable_v),
            q_observable_v,
        )
        predicted = _dense_scale(
            coefficient,
            _dense_difference(
                _dense_scale(spin * spin, identity),
                _dense_product(generator, generator),
            ),
        )
        _assert_dense_close(gram, predicted)
        leakage_grams.append(gram)

    highest_weight_weights = tuple(
        gram[0][0].real for gram in leakage_grams
    )
    assert math.isclose(highest_weight_weights[0], site_count / 2.0)
    assert math.isclose(highest_weight_weights[1], site_count / 2.0)
    assert math.isclose(highest_weight_weights[2], 0.0)
    assert math.isclose(sum(highest_weight_weights), float(site_count))

    isotropic_weights = tuple(
        sum(gram[index][index].real for index in range(site_count + 1))
        / (site_count + 1)
        for gram in leakage_grams
    )
    assert all(
        math.isclose(weight, site_count / 3.0)
        for weight in isotropic_weights
    )


def test_certificate_passes_with_explicit_claim_boundary():
    certificate = locality_reference_leakage_certificate()
    assert certificate["status"] == "pass"
    assert all(certificate["certified_claims"].values())
    assert "state-weighted" in certificate["claim_boundary"]
    assert "no QFT" in certificate["claim_boundary"]


@pytest.mark.parametrize(
    "call",
    (
        lambda: required_mean_casimir_for_risk(0.0),
        lambda: minimum_integer_spin_from_risk(1.1),
        lambda: disjoint_block_ferromagnetic_code_record(3),
        lambda: disjoint_block_ferromagnetic_code_record(8, buffer_sites=3),
        lambda: three_cell_ferromagnetic_state_record(8),
        lambda: collective_mode_leakage_from_casimir(
            mean_casimir=1.0,
            response_gain=1.0,
            local_operator_norm=1.0,
            leakage_amplitude_cap=2.0,
        ),
        lambda: collective_mode_leakage_from_casimir(
            mean_casimir=1.0,
            response_gain=1.0,
            local_operator_norm=1.0,
            compression_error=0.1,
        ),
    ),
)
def test_invalid_inputs_are_rejected(call):
    with pytest.raises(ValueError):
        call()
