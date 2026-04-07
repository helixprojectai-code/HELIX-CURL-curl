#!/usr/bin/env python3
"""
CURL curl Prototype v2.1 -- Zoom + (2,5) Diagonal Branch
Constitutional Unitary Resonant Lattice (CURL)

Two experiments in parallel:
  A) High-resolution zoom around gamma=1/3 to characterize the reversal
     - Cusp, smooth inflection, or true discontinuity?
  B) (2,5) diagonal braid: sigma_1(2,3) sigma_2(3,5) sigma_3(2,5)
     - Does the full prime triangle change the threshold?
     - Does -1/2 survive?

v2 baseline preserved. This is a branch, not a replacement.
"""

import numpy as np
import matplotlib.pyplot as plt

# Pauli matrices
sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)


def n_hat_p(p):
    ln_p = np.log(p)
    v = np.array([np.sin(ln_p), np.cos(ln_p), np.tanh(ln_p)], dtype=float)
    return v / np.linalg.norm(v)


def O_p(p, gamma=0.0):
    ln_p = np.log(p)
    theta = ln_p * (1 + gamma)
    nx, ny, nz = n_hat_p(p)
    n_dot_sigma = nx * sigma_x + ny * sigma_y + nz * sigma_z
    I2 = np.eye(2, dtype=complex)
    return np.cos(theta / 2) * I2 - 1j * np.sin(theta / 2) * n_dot_sigma


def R_matrix(p, q, gamma=0.0):
    Op = O_p(p, gamma)
    Oq = O_p(q, gamma)
    SWAP = np.array([[1, 0, 0, 0],
                     [0, 0, 1, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 1]], dtype=complex)
    phase = np.exp(1j * np.pi / 4 * (1 + gamma))
    U = np.kron(Op, Oq)
    U_dag = U.conj().T
    return U @ (phase * SWAP) @ U_dag


def braid_matrix(crossings, gamma=0.0):
    """Generic braid matrix builder. crossings = [(strand_i, strand_j, prime_p, prime_q), ...]"""
    dim = 8
    M = np.eye(dim, dtype=complex)
    for si, sj, p, q in crossings:
        R = R_matrix(p, q, gamma)
        if si == 0 and sj == 1:
            R_full = np.kron(R, np.eye(2, dtype=complex))
        elif si == 1 and sj == 2:
            R_full = np.kron(np.eye(2, dtype=complex), R)
        elif si == 0 and sj == 2:
            # (2,5) diagonal: acts on strands 0 and 2, identity on strand 1
            # Need to permute strand order: swap 1<->2, apply R on (0,1), swap back
            SWAP12 = np.kron(np.eye(2, dtype=complex),
                             np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]], dtype=complex))
            R_on_01 = np.kron(R, np.eye(2, dtype=complex))
            R_full = SWAP12 @ R_on_01 @ SWAP12
        else:
            continue
        M = R_full @ M
    return M


def trace_invariant(crossings, gamma=0.0):
    M = braid_matrix(crossings, gamma)
    return np.trace(M).real / 8.0


def commutator_norm(p, q, gamma=0.0):
    Op = O_p(p, gamma)
    Oq = O_p(q, gamma)
    return np.linalg.norm(Op @ Oq - Oq @ Op, 'fro')


# === Braid definitions ===

# v2 trefoil: sigma_1(2,3) sigma_2(3,5) sigma_1(2,3)
TREFOIL_V2 = [
    (0, 1, 2, 3),
    (1, 2, 3, 5),
    (0, 1, 2, 3),
]

# v2.1 full triangle: sigma_1(2,3) sigma_2(3,5) sigma_3(2,5)
TRIANGLE = [
    (0, 1, 2, 3),
    (1, 2, 3, 5),
    (0, 2, 2, 5),
]

# v2.1 extended: all three pairs then repeat first (4 crossings)
TRIANGLE_PLUS = [
    (0, 1, 2, 3),
    (1, 2, 3, 5),
    (0, 2, 2, 5),
    (0, 1, 2, 3),
]


def experiment_a_zoom():
    """High-resolution zoom around gamma=1/3."""
    print("=" * 65)
    print("EXPERIMENT A: Zoom around gamma = 1/3")
    print("=" * 65)

    # Coarse sweep to confirm location
    gamma_coarse = np.linspace(0.30, 0.37, 500)
    inv_coarse = np.array([trace_invariant(TREFOIL_V2, g) for g in gamma_coarse])

    # Find exact extremum
    extremum_idx = np.argmin(inv_coarse)
    gamma_ext = gamma_coarse[extremum_idx]
    inv_ext = inv_coarse[extremum_idx]

    # Ultra-fine zoom around extremum
    gamma_fine = np.linspace(gamma_ext - 0.005, gamma_ext + 0.005, 2000)
    inv_fine = np.array([trace_invariant(TREFOIL_V2, g) for g in gamma_fine])

    fine_ext_idx = np.argmin(inv_fine)
    gamma_precise = gamma_fine[fine_ext_idx]
    inv_precise = inv_fine[fine_ext_idx]

    # Derivatives around extremum
    d1 = np.gradient(inv_fine, gamma_fine)
    d2 = np.gradient(d1, gamma_fine)
    d2_at_ext = d2[fine_ext_idx]

    # Check symmetry around extremum (cusp vs smooth)
    left_half = inv_fine[:fine_ext_idx]
    right_half = inv_fine[fine_ext_idx:]
    min_len = min(len(left_half), len(right_half))
    if min_len > 10:
        left_mirror = left_half[-min_len:][::-1]
        right_mirror = right_half[:min_len]
        asymmetry = np.mean(np.abs(left_mirror - right_mirror))
    else:
        asymmetry = float('nan')

    print(f"\nExtremum location:     gamma = {gamma_precise:.8f}")
    print(f"Theoretical 1/3:       gamma = {1/3:.8f}")
    print(f"Difference:            {abs(gamma_precise - 1/3):.8f}")
    print(f"\nInvariant at extremum: {inv_precise:.10f}")
    print(f"Theoretical -1/2:      {-0.5:.10f}")
    print(f"Difference:            {abs(inv_precise - (-0.5)):.2e}")
    print(f"\nd2(inv)/d(gamma)2:     {d2_at_ext:.6f}")
    print(f"  -> {'SMOOTH TURNING POINT (d2 > 0)' if d2_at_ext > 0 else 'CUSP or DISCONTINUITY'}")
    print(f"\nAsymmetry measure:     {asymmetry:.2e}")
    print(f"  -> {'SYMMETRIC (smooth inflection)' if asymmetry < 1e-4 else 'ASYMMETRIC (cusp-like)'}")

    return gamma_fine, inv_fine, d1, d2, gamma_precise, inv_precise


def experiment_b_triangle():
    """Test (2,5) diagonal braid variants."""
    print("\n" + "=" * 65)
    print("EXPERIMENT B: (2,5) Diagonal -- Full Prime Triangle")
    print("=" * 65)

    gamma_vals = np.linspace(0, 0.50, 500)

    inv_v2 = np.array([trace_invariant(TREFOIL_V2, g) for g in gamma_vals])
    inv_tri = np.array([trace_invariant(TRIANGLE, g) for g in gamma_vals])
    inv_tri_plus = np.array([trace_invariant(TRIANGLE_PLUS, g) for g in gamma_vals])

    # Find extrema for each
    results = {}
    for name, inv in [("v2 trefoil", inv_v2), ("triangle", inv_tri), ("triangle+", inv_tri_plus)]:
        ext_idx = np.argmin(inv)
        gamma_ext = gamma_vals[ext_idx]
        inv_ext = inv[ext_idx]

        d1 = np.gradient(inv, gamma_vals)
        d2 = np.gradient(d1, gamma_vals)
        inflection_idx = np.argmax(np.abs(d2))

        results[name] = {
            'extremum_gamma': gamma_ext,
            'extremum_inv': inv_ext,
            'inflection_gamma': gamma_vals[inflection_idx],
            'baseline': inv[0],
        }

    print(f"\n{'Braid':<16} {'Baseline':<12} {'Extremum':<12} {'at gamma':<12} {'Has reversal'}")
    print("-" * 65)
    for name, r in results.items():
        has_reversal = r['extremum_gamma'] < gamma_vals[-1] - 0.02
        print(f"{name:<16} {r['baseline']:<12.6f} {r['extremum_inv']:<12.6f} "
              f"{r['extremum_gamma']:<12.4f} {'YES' if has_reversal else 'NO (monotonic)'}")

    # Commutator comparison at key points
    print(f"\nCommutator norms at gamma=0 vs gamma=1/3:")
    print(f"{'Pair':<12} {'gamma=0':<12} {'gamma=1/3':<12} {'Ratio':<10}")
    print("-" * 46)
    for p, q, label in [(2, 3, "[O2,O3]"), (3, 5, "[O3,O5]"), (2, 5, "[O2,O5]")]:
        c0 = commutator_norm(p, q, 0.0)
        c3 = commutator_norm(p, q, 1/3)
        print(f"{label:<12} {c0:<12.6f} {c3:<12.6f} {c3/c0:<10.4f}")

    return gamma_vals, inv_v2, inv_tri, inv_tri_plus, results


def plot_all(zoom_data, triangle_data):
    gamma_fine, inv_fine, d1, d2, gamma_precise, inv_precise = zoom_data
    gamma_vals, inv_v2, inv_tri, inv_tri_plus, results = triangle_data

    fig, axes = plt.subplots(2, 2, figsize=(15, 11))

    # Top-left: Zoom on the turning point
    ax = axes[0, 0]
    ax.plot(gamma_fine, inv_fine, 'b-', linewidth=2)
    ax.axvline(x=1/3, color='red', linestyle='--', linewidth=1.5, label='gamma = 1/3')
    ax.axhline(y=-0.5, color='orange', linestyle='--', linewidth=1.5, label='inv = -1/2')
    ax.plot(gamma_precise, inv_precise, 'ro', markersize=10, zorder=5,
            label=f'Extremum ({gamma_precise:.6f}, {inv_precise:.8f})')
    ax.set_xlabel('gamma')
    ax.set_ylabel('Trace Invariant')
    ax.set_title(f'ZOOM: Turning Point at gamma ~ 1/3\n'
                 f'Extremum: gamma={gamma_precise:.6f}, inv={inv_precise:.8f}')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Top-right: Derivatives at zoom
    ax = axes[0, 1]
    ax.plot(gamma_fine, d1, 'green', linewidth=1.5, label="d(inv)/d(gamma)")
    ax.plot(gamma_fine, d2, 'purple', linewidth=1.5, label="d2(inv)/d(gamma)2")
    ax.axvline(x=1/3, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    ax.set_xlabel('gamma')
    ax.set_ylabel('Derivative value')
    ax.set_title('Derivatives at Turning Point\n(d1 crosses zero = confirmed extremum)')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Bottom-left: Three braid variants compared
    ax = axes[1, 0]
    ax.plot(gamma_vals, inv_v2, 'b-', linewidth=2, label='v2: s1(2,3) s2(3,5) s1(2,3)')
    ax.plot(gamma_vals, inv_tri, 'r-', linewidth=2, label='Triangle: s1(2,3) s2(3,5) s3(2,5)')
    ax.plot(gamma_vals, inv_tri_plus, 'g--', linewidth=2, label='Tri+: s1(2,3) s2(3,5) s3(2,5) s1(2,3)')
    ax.axvline(x=1/3, color='gray', linestyle=':', alpha=0.7, label='gamma = 1/3')
    ax.axhline(y=-0.5, color='orange', linestyle=':', alpha=0.5)
    ax.set_xlabel('gamma')
    ax.set_ylabel('Trace Invariant')
    ax.set_title('Braid Variant Comparison\n(2,5) diagonal vs v2 trefoil')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    # Bottom-right: Commutator evolution for all three pairs
    ax = axes[1, 1]
    c23 = [commutator_norm(2, 3, g) for g in gamma_vals]
    c35 = [commutator_norm(3, 5, g) for g in gamma_vals]
    c25 = [commutator_norm(2, 5, g) for g in gamma_vals]
    ax.plot(gamma_vals, c23, label='||[O2,O3]||', linewidth=1.5)
    ax.plot(gamma_vals, c35, label='||[O3,O5]||', linewidth=1.5)
    ax.plot(gamma_vals, c25, label='||[O2,O5]||', linewidth=1.5)
    ax.axvline(x=1/3, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='gamma=1/3')
    # Mark the ratio at 1/3
    c25_at_third = commutator_norm(2, 5, 1/3)
    c23_at_third = commutator_norm(2, 3, 1/3)
    ax.annotate(f'ratio [O2,O5]/[O2,O3] = {c25_at_third/c23_at_third:.3f}',
                xy=(1/3, c25_at_third), xytext=(0.38, c25_at_third * 0.85),
                arrowprops=dict(arrowstyle='->', color='black'),
                fontsize=8)
    ax.set_xlabel('gamma')
    ax.set_ylabel('Frobenius Norm')
    ax.set_title('Commutator Norms: All Three Prime Pairs')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    plt.suptitle('CURL curl v2.1: Zoom + (2,5) Diagonal Analysis\n'
                 'Primes [2,3,5] | Full Triangle Test',
                 fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig('curl_curl_v2_1_output.png', dpi=150, bbox_inches='tight')
    print(f"\nPlot saved to: curl_curl_v2_1_output.png")
    plt.show()


if __name__ == "__main__":
    print("=" * 65)
    print("CURL curl v2.1 -- Zoom + (2,5) Diagonal Branch")
    print("=" * 65)

    zoom_data = experiment_a_zoom()
    triangle_data = experiment_b_triangle()
    plot_all(zoom_data, triangle_data)

    print("\n" + "=" * 65)
    print("v2.1 COMPLETE")
    print("=" * 65)
