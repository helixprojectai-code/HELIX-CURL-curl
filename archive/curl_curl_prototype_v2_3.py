#!/usr/bin/env python3
"""
CURL curl Prototype v2.3 -- Extremum Verification
Constitutional Unitary Resonant Lattice (CURL)

High-resolution zoom on:
  A) Double-triangle (6 crossings): extremum +1.0 at gamma=1/3?
  B) Double-trefoil (6 crossings): extremum +1.0 at gamma=1/3?
  C) 5-crossing braids: extremum +1/2 at gamma~0.6? Is 0.6 = 2/3?
  D) Composition law: if trefoil^1 -> -1/2, trefoil^2 -> +1, what is trefoil^3?
"""

import numpy as np
import matplotlib.pyplot as plt

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
    dim = 8
    M = np.eye(dim, dtype=complex)
    for si, sj, p, q in crossings:
        R = R_matrix(p, q, gamma)
        if si == 0 and sj == 1:
            R_full = np.kron(R, np.eye(2, dtype=complex))
        elif si == 1 and sj == 2:
            R_full = np.kron(np.eye(2, dtype=complex), R)
        elif si == 0 and sj == 2:
            SWAP12 = np.kron(np.eye(2, dtype=complex),
                             np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]], dtype=complex))
            R_on_01 = np.kron(R, np.eye(2, dtype=complex))
            R_full = SWAP12 @ R_on_01 @ SWAP12
        else:
            continue
        M = R_full @ M
    return M


def trace_invariant(crossings, gamma=0.0):
    return np.trace(braid_matrix(crossings, gamma)).real / 8.0


# === Braid definitions ===

TREFOIL = [
    (0, 1, 2, 3), (1, 2, 3, 5), (0, 1, 2, 3),
]

DBL_TRIANGLE = [
    (0, 1, 2, 3), (1, 2, 3, 5), (0, 2, 2, 5),
    (0, 1, 2, 3), (1, 2, 3, 5), (0, 2, 2, 5),
]

DBL_TREFOIL = [
    (0, 1, 2, 3), (1, 2, 3, 5), (0, 1, 2, 3),
    (0, 1, 2, 3), (1, 2, 3, 5), (0, 1, 2, 3),
]

CYCLE_5 = [
    (0, 1, 2, 3), (1, 2, 3, 5), (0, 2, 2, 5),
    (0, 1, 2, 3), (1, 2, 3, 5),
]

# Trefoil^3: 9 crossings
TRIPLE_TREFOIL = [
    (0, 1, 2, 3), (1, 2, 3, 5), (0, 1, 2, 3),
    (0, 1, 2, 3), (1, 2, 3, 5), (0, 1, 2, 3),
    (0, 1, 2, 3), (1, 2, 3, 5), (0, 1, 2, 3),
]


def zoom_extremum(name, braid, search_center, search_width=0.05):
    """High-res zoom to find exact extremum."""
    # Coarse pass
    gamma_c = np.linspace(max(0, search_center - search_width),
                          search_center + search_width, 500)
    inv_c = np.array([trace_invariant(braid, g) for g in gamma_c])

    # Find if it's a min or max
    min_idx = np.argmin(inv_c)
    max_idx = np.argmax(inv_c)
    if abs(inv_c[max_idx]) > abs(inv_c[min_idx]):
        coarse_idx = max_idx
    else:
        coarse_idx = min_idx

    center = gamma_c[coarse_idx]

    # Ultra-fine pass
    gamma_f = np.linspace(max(0, center - 0.003), center + 0.003, 5000)
    inv_f = np.array([trace_invariant(braid, g) for g in gamma_f])

    # Find extremum (furthest from zero)
    abs_inv = np.abs(inv_f)
    fine_idx = np.argmax(abs_inv)
    gamma_ext = gamma_f[fine_idx]
    inv_ext = inv_f[fine_idx]

    # Derivatives
    d1 = np.gradient(inv_f, gamma_f)
    d2 = np.gradient(d1, gamma_f)

    # Symmetry check
    left = inv_f[:fine_idx]
    right = inv_f[fine_idx:]
    min_len = min(len(left), len(right))
    if min_len > 10:
        asymmetry = np.mean(np.abs(left[-min_len:][::-1] - right[:min_len]))
    else:
        asymmetry = float('nan')

    return gamma_ext, inv_ext, d2[fine_idx], asymmetry, gamma_f, inv_f, d1, d2


def main():
    print("=" * 70)
    print("CURL curl v2.3 -- Extremum Verification")
    print("=" * 70)

    # === A) Double-triangle at gamma=1/3 ===
    print("\n--- A) Double-Triangle (6 crossings) ---")
    g, inv, d2, asym, gf, invf, d1f, d2f = zoom_extremum(
        "dbl-triangle", DBL_TRIANGLE, 1/3)
    print(f"  Extremum gamma:      {g:.8f}")
    print(f"  Theoretical 1/3:     {1/3:.8f}")
    print(f"  Difference:          {abs(g - 1/3):.2e}")
    print(f"  Extremum invariant:  {inv:.10f}")
    print(f"  Theoretical +1:      {1.0:.10f}")
    print(f"  Difference:          {abs(inv - 1.0):.2e}")
    print(f"  d2 at extremum:      {d2:.6f}")
    print(f"  Symmetry:            {asym:.2e} ({'SYMMETRIC' if asym < 1e-4 else 'ASYMMETRIC'})")
    dbl_tri_zoom = (gf, invf, d1f, d2f, g, inv)

    # === B) Double-trefoil at gamma=1/3 ===
    print("\n--- B) Double-Trefoil (6 crossings) ---")
    g, inv, d2, asym, gf, invf, d1f, d2f = zoom_extremum(
        "dbl-trefoil", DBL_TREFOIL, 1/3)
    print(f"  Extremum gamma:      {g:.8f}")
    print(f"  Theoretical 1/3:     {1/3:.8f}")
    print(f"  Difference:          {abs(g - 1/3):.2e}")
    print(f"  Extremum invariant:  {inv:.10f}")
    print(f"  Theoretical +1:      {1.0:.10f}")
    print(f"  Difference:          {abs(inv - 1.0):.2e}")
    print(f"  d2 at extremum:      {d2:.6f}")
    print(f"  Symmetry:            {asym:.2e} ({'SYMMETRIC' if asym < 1e-4 else 'ASYMMETRIC'})")
    dbl_tre_zoom = (gf, invf, d1f, d2f, g, inv)

    # === C) 5-crossing at gamma~0.6 -- is it 2/3? ===
    print("\n--- C) 5-Crossing Cycle ---")
    g, inv, d2, asym, gf, invf, d1f, d2f = zoom_extremum(
        "cycle-5", CYCLE_5, 0.6, search_width=0.05)
    print(f"  Extremum gamma:      {g:.8f}")
    print(f"  Theoretical 2/3:     {2/3:.8f}")
    print(f"  Difference from 2/3: {abs(g - 2/3):.2e}")
    print(f"  Difference from 3/5: {abs(g - 3/5):.2e}")
    print(f"  Extremum invariant:  {inv:.10f}")
    print(f"  Theoretical +1/2:    {0.5:.10f}")
    print(f"  Difference:          {abs(inv - 0.5):.2e}")
    print(f"  d2 at extremum:      {d2:.6f}")
    print(f"  Symmetry:            {asym:.2e} ({'SYMMETRIC' if asym < 1e-4 else 'ASYMMETRIC'})")
    cyc5_zoom = (gf, invf, d1f, d2f, g, inv)

    # === D) Triple-trefoil (9 crossings) -- the composition law ===
    print("\n--- D) Triple-Trefoil (9 crossings) -- Composition Law ---")
    # First find where the extremum is with a wide sweep
    gamma_wide = np.linspace(0, 1.5, 1000)
    inv_wide = np.array([trace_invariant(TRIPLE_TREFOIL, g) for g in gamma_wide])
    baseline_triple = inv_wide[0]
    print(f"  Baseline (gamma=0):  {baseline_triple:.10f}")

    # Check candidate algebraic values
    for candidate, label in [(-1/(2*np.sqrt(2)), "-1/(2sqrt2)"),
                             (-0.5, "-1/2"), (0.5, "+1/2"),
                             (1.0, "+1"), (-1.0, "-1"),
                             (0.0, "0"),
                             (1/(2*np.sqrt(2)), "+1/(2sqrt2)")]:
        if abs(baseline_triple - candidate) < 0.001:
            print(f"  Baseline matches:    {label}")

    # Find extremum
    ext_idx = np.argmax(np.abs(inv_wide))
    print(f"  Peak at gamma:       {gamma_wide[ext_idx]:.4f}")
    print(f"  Peak invariant:      {inv_wide[ext_idx]:.8f}")

    # High-res zoom on triple
    g, inv, d2, asym, gf, invf, d1f, d2f = zoom_extremum(
        "triple-trefoil", TRIPLE_TREFOIL, gamma_wide[ext_idx], search_width=0.05)
    print(f"\n  Zoomed extremum gamma:     {g:.8f}")
    print(f"  Zoomed extremum invariant: {inv:.10f}")
    print(f"  Is gamma = 1/3?            diff = {abs(g - 1/3):.2e}")
    print(f"  Is gamma = 1/9?            diff = {abs(g - 1/9):.2e}")
    print(f"  Is inv = -1/2?             diff = {abs(inv - (-0.5)):.2e}")
    print(f"  Is inv = +1/2?             diff = {abs(inv - 0.5):.2e}")
    print(f"  Is inv = -1?               diff = {abs(inv - (-1.0)):.2e}")
    print(f"  Is inv = +1?               diff = {abs(inv - 1.0):.2e}")
    print(f"  Is inv = -1/(2sqrt2)?      diff = {abs(inv - (-1/(2*np.sqrt(2)))):.2e}")
    print(f"  Is inv = +1/(2sqrt2)?      diff = {abs(inv - (1/(2*np.sqrt(2)))):.2e}")
    print(f"  d2 at extremum:            {d2:.6f}")
    print(f"  Symmetry:                  {asym:.2e}")
    triple_zoom = (gf, invf, d1f, d2f, g, inv)

    # === COMPOSITION LAW SUMMARY ===
    print(f"\n{'=' * 70}")
    print("COMPOSITION LAW")
    print(f"{'=' * 70}")
    print(f"  Trefoil^1 (3 crossings):  baseline = {trace_invariant(TREFOIL, 0):.6f}  "
          f"extremum = {trace_invariant(TREFOIL, 1/3):.6f} at gamma=1/3")
    print(f"  Trefoil^2 (6 crossings):  baseline = {trace_invariant(DBL_TREFOIL, 0):.6f}  "
          f"extremum = {trace_invariant(DBL_TREFOIL, 1/3):.6f} at gamma=1/3")
    print(f"  Trefoil^3 (9 crossings):  baseline = {baseline_triple:.6f}  "
          f"extremum = {inv:.6f} at gamma={g:.4f}")

    # === Visualization ===
    fig, axes = plt.subplots(2, 2, figsize=(15, 11))

    # A) Double-triangle zoom
    ax = axes[0, 0]
    gf, invf, d1f, d2f, ge, ie = dbl_tri_zoom
    ax.plot(gf, invf, 'b-', linewidth=2)
    ax.axvline(x=1/3, color='red', linestyle='--', linewidth=1.5, label='gamma=1/3')
    ax.axhline(y=1.0, color='orange', linestyle='--', linewidth=1.5, label='inv=+1')
    ax.plot(ge, ie, 'ro', markersize=10, zorder=5)
    ax.set_title(f'Double-Triangle: extremum at ({ge:.6f}, {ie:.8f})')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('gamma')
    ax.set_ylabel('Trace Invariant')

    # B) 5-crossing zoom
    ax = axes[0, 1]
    gf, invf, d1f, d2f, ge, ie = cyc5_zoom
    ax.plot(gf, invf, 'g-', linewidth=2)
    ax.axvline(x=2/3, color='red', linestyle='--', linewidth=1.5, label='gamma=2/3')
    ax.axhline(y=0.5, color='orange', linestyle='--', linewidth=1.5, label='inv=+1/2')
    ax.plot(ge, ie, 'ro', markersize=10, zorder=5)
    ax.set_title(f'5-Crossing Cycle: extremum at ({ge:.6f}, {ie:.8f})')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('gamma')
    ax.set_ylabel('Trace Invariant')

    # C) Triple-trefoil zoom
    ax = axes[1, 0]
    gf, invf, d1f, d2f, ge, ie = triple_zoom
    ax.plot(gf, invf, 'purple', linewidth=2)
    ax.axvline(x=1/3, color='red', linestyle='--', linewidth=1.5, alpha=0.5, label='gamma=1/3')
    ax.plot(ge, ie, 'ro', markersize=10, zorder=5)
    ax.set_title(f'Triple-Trefoil: extremum at ({ge:.6f}, {ie:.8f})')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('gamma')
    ax.set_ylabel('Trace Invariant')

    # D) Full composition: all three trefoil powers on one plot
    ax = axes[1, 1]
    gamma_sweep = np.linspace(0, 0.8, 500)
    inv1 = [trace_invariant(TREFOIL, g) for g in gamma_sweep]
    inv2 = [trace_invariant(DBL_TREFOIL, g) for g in gamma_sweep]
    inv3 = [trace_invariant(TRIPLE_TREFOIL, g) for g in gamma_sweep]
    ax.plot(gamma_sweep, inv1, 'b-', linewidth=2, label='Trefoil^1 (3)')
    ax.plot(gamma_sweep, inv2, 'r-', linewidth=2, label='Trefoil^2 (6)')
    ax.plot(gamma_sweep, inv3, 'purple', linewidth=2, label='Trefoil^3 (9)')
    ax.axvline(x=1/3, color='gray', linestyle='--', alpha=0.7, label='gamma=1/3')
    ax.axhline(y=-0.5, color='blue', linestyle=':', alpha=0.4)
    ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    ax.axhline(y=1.0, color='red', linestyle=':', alpha=0.4)
    ax.set_title('Composition Law: Trefoil^1, ^2, ^3')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('gamma')
    ax.set_ylabel('Trace Invariant')

    plt.suptitle('CURL curl v2.3: Extremum Verification + Composition Law\n'
                 'Trefoil powers and the algebraic sequence',
                 fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig('curl_curl_v2_3_output.png', dpi=150, bbox_inches='tight')
    print(f"\nPlot saved to: curl_curl_v2_3_output.png")
    plt.show()


if __name__ == "__main__":
    main()
