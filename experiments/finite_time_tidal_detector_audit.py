"""Write the source-hashed finite-time tidal-detector transfer audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from qgtoy.finite_time_tidal_detector import finite_time_tidal_readout_record


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "experiments/finite_time_tidal_detector_certificate.json"
SOURCES = (
    "qgtoy/finite_time_tidal_detector.py",
    "experiments/finite_time_tidal_detector_audit.py",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_record() -> dict[str, object]:
    noiseless_heat = finite_time_tidal_readout_record(
        initial_fractional_acceleration_contrast=0.02,
        physical_proof_mass_separation=0.4,
        interrogation_time=3.0,
        diffusion_rate=0.0,
        displacement_readout_standard_deviation=0.002,
    )
    diffusing = finite_time_tidal_readout_record(
        initial_fractional_acceleration_contrast=0.02,
        physical_proof_mass_separation=0.4,
        interrogation_time=3.0,
        diffusion_rate=0.1,
        displacement_readout_standard_deviation=0.002,
    )
    zero_signal = finite_time_tidal_readout_record(
        initial_fractional_acceleration_contrast=0.0,
        physical_proof_mass_separation=0.4,
        interrogation_time=3.0,
        diffusion_rate=0.1,
        displacement_readout_standard_deviation=0.002,
    )
    claims = {
        "zero_rate_kernel_is_T_squared_over_two": noiseless_heat[
            "integrated_rank_two_jacobi_kernel"
        ]
        == 4.5,
        "rank_two_multiplier_is_rank_one_cubed": abs(
            diffusing["rank_two_equals_rank_one_cubed_error"]
        )
        < 1.0e-15,
        "jacobi_kernel_obeys_endpoint_bounds": diffusing["kernel_bounds_hold"],
        "diffusion_reduces_integrated_tidal_signal": abs(
            diffusing["mean_displacement_contrast"]
        )
        < abs(noiseless_heat["mean_displacement_contrast"]),
        "zero_signal_has_coin_flip_error": zero_signal[
            "equal_prior_optimal_gaussian_error_probability"
        ]
        == 0.5,
    }
    return {
        "goal": "Finite-Time Noisy Tidal Detector Transfer",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "rank_two_heat_jacobi_gaussian_readout_composition",
        "certified_claims": claims,
        "zero_rate_case": noiseless_heat,
        "diffusing_case": diffusing,
        "zero_signal_case": zero_signal,
        "source_sha256": {relative: _sha256(ROOT / relative) for relative in SOURCES},
        "claim_boundary": (
            "Exact within the declared heat/Jacobi/Gaussian model. The audit "
            "does not derive the Weyl amplitude, diffusion rate, readout noise, "
            "or detector backreaction from the Skyrmion action."
        ),
    }


def main() -> None:
    record = build_record()
    OUTPUT.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="ascii"
    )
    print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
