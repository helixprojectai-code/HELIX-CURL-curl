#!/usr/bin/env python3
"""
CURL curl Prototype v2.2 -- The Sequence Hunter
Constitutional Unitary Resonant Lattice (CURL)

Questions:
  1. Does Triangle+ (4 crossings) have its own threshold?
  2. Does it hit -1/2 at some gamma?
  3. Hypothesis: gamma_n = 1/n for n crossings?
  4. What's the 5-crossing and 6-crossing baseline? Does -2^(-3) = -1/8 appear?
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
    M = braid_matrix(crossings, gamma)
    return np.trace(M).real / 8.0


# === Braid Zoo ===

# 3 crossings: trefoil
BRAID_3 = [
    (0, 1, 2, 3),
    (1, 2, 3, 5),
    (0, 1, 2, 3),
]

# 4 crossings: triangle+
BRAID_4 = [
    (0, 1, 2, 3),
    (1, 2, 3, 5),
    (0, 2, 2, 5),
    (0, 1, 2, 3),
]

# 5 crossings: full cycle + repeat
BRAID_5 = [
    (0, 1, 2, 3),
    (1, 2, 3, 5),
    (0, 2, 2, 5),
    (0, 1, 2, 3),
    (1, 2, 3, 5),
]

# 6 crossings: double triangle
BRAID_6 = [
    (0, 1, 2, 3),
    (1, 2, 3, 5),
    (0, 2, 2, 5),
    (0, 1, 2, 3),
    (1, 2, 3, 5),
    (0, 2, 2, 5),
]

# Alternative 5: trefoil squared (sigma1 sigma2 sigma1 sigma1 sigma2)
BRAID_5_ALT = [
    (0, 1, 2, 3),
    (1, 2, 3, 5),
    (0, 1, 2, 3),
    (0, 1, 2, 3),
    (1, 2, 3, 5),
]

# Alternative 6: double trefoil
BRAID_6_ALT = [
    (0, 1, 2, 3),
    (1, 2, 3, 5),
    (0, 1, 2, 3),
    (0, 1, 2, 3),
    (1, 2, 3, 5),
    (0, 1, 2, 3),
]

ALL_BRAIDS = {
    '3 (trefoil)':     BRAID_3,
    '4 (tri+)':        BRAID_4,
    '5 (cycle)':       BRAID_5,
    '6 (dbl-tri)':     BRAID_6,
    '5 (trefoil-ext)': BRAID_5_ALT,
    '6 (dbl-trefoil)': BRAID_6_ALT,
}


def sweep_braid(name, crossings, gamma_vals):
    """Sweep gamma for a braid, find extremum and threshold."""
    inv = np.array([trace_invariant(crossings, g) for g in gamma_vals])
    baseline = inv[0]

    # Find extremum (minimum)
    ext_idx = np.argmin(inv)
    # Also check maximum in case curve goes the other way
    max_idx = np.argmax(np.abs(inv))

    # Use whichever is furthest from baseline
    if abs(inv[ext_idx] - baseline) >= abs(inv[max_idx] - baseline):
        peak_idx = ext_idx
    else:
        peak_idx = max_idx

    gamma_peak = gamma_vals[peak_idx]
    inv_peak = inv[peak_idx]
    has_reversal = peak_idx > 5 and peak_idx < len(gamma_vals) - 5

    return {
        'name': name,
        'inv': inv,
        'baseline': baseline,
        'peak_gamma': gamma_peak,
        'peak_inv': inv_peak,
        'has_reversal': has_reversal,
    }


def main():
    gamma_vals = np.linspace(0, 1.0, 1000)

    print("=" * 75)
    print("CURL curl v2.2 -- The Sequence Hunter")
    print("=" * 75)

    # Sweep all braids
    results = {}
    for name, braid in ALL_BRAIDS.items():
        results[name] = sweep_braid(name, braid, gamma_vals)

    # Summary table
    print(f"\n{'Braid':<20} {'Crossings':<10} {'Baseline':<12} {'Extremum':<12} "
          f"{'at gamma':<10} {'Reversal':<10}")
    print("-" * 75)
    for name, r in results.items():
        n = name.split()[0]
        print(f"{name:<20} {n:<10} {r['baseline']:<12.6f} {r['peak_inv']:<12.6f} "
              f"{r['peak_gamma']:<10.4f} {'YES' if r['has_reversal'] else 'NO'}")

    # Check hypothesis: gamma_n = 1/n
    print(f"\n{'=' * 75}")
    print("HYPOTHESIS TEST: gamma_n = 1/n")
    print(f"{'=' * 75}")
    for name, braid in ALL_BRAIDS.items():
        n_crossings = len(braid)
        predicted_gamma = 1.0 / n_crossings
        inv_at_predicted = trace_invariant(braid, predicted_gamma)
        r = results[name]
        print(f"\n{name}:")
        print(f"  Predicted gamma = 1/{n_crossings} = {predicted_gamma:.6f}")
        print(f"  Actual extremum gamma     = {r['peak_gamma']:.6f}")
        print(f"  Invariant at 1/{n_crossings}          = {inv_at_predicted:.8f}")
        print(f"  Invariant at extremum     = {r['peak_inv']:.8f}")
        print(f"  Is -1/2 at predicted?     {abs(inv_at_predicted - (-0.5)) < 0.001}")

    # Check power-of-two pattern in baselines
    print(f"\n{'=' * 75}")
    print("BASELINE PATTERN: Powers of 2?")
    print(f"{'=' * 75}")
    for name, r in results.items():
        b = r['baseline']
        if abs(b) > 1e-10:
            log2_val = np.log2(abs(b))
            print(f"  {name:<20} baseline = {b:<12.6f}  |b| = 2^({log2_val:.4f})  "
                  f"nearest: -2^({round(log2_val)}) = {-2**round(log2_val):.6f}")

    # High-res zoom on Triangle+ around its extremum
    print(f"\n{'=' * 75}")
    print("TRIANGLE+ HIGH-RES ZOOM")
    print(f"{'=' * 75}")
    r4 = results['4 (tri+)']
    if r4['has_reversal']:
        center = r4['peak_gamma']
        gamma_zoom = np.linspace(max(0, center - 0.02), center + 0.02, 2000)
        inv_zoom = np.array([trace_invariant(BRAID_4, g) for g in gamma_zoom])
        fine_idx = np.argmin(inv_zoom)
        print(f"  Extremum gamma:    {gamma_zoom[fine_idx]:.8f}")
        print(f"  Extremum inv:      {inv_zoom[fine_idx]:.10f}")
        print(f"  Is gamma = 1/4?    diff = {abs(gamma_zoom[fine_idx] - 0.25):.8f}")
        print(f"  Is inv = -1/2?     diff = {abs(inv_zoom[fine_idx] - (-0.5)):.2e}")
        print(f"  Is inv = -1/4?     diff = {abs(inv_zoom[fine_idx] - (-0.25)):.2e}")
        print(f"  Is inv = -1/8?     diff = {abs(inv_zoom[fine_idx] - (-0.125)):.2e}")
    else:
        # Monotonic -- check if it ever reaches -1/2
        gamma_wide = np.linspace(0, 2.0, 2000)
        inv_wide = np.array([trace_invariant(BRAID_4, g) for g in gamma_wide])
        closest_to_half = np.argmin(np.abs(inv_wide - (-0.5)))
        print(f"  Triangle+ is monotonic in [0, 1.0]")
        print(f"  Closest to -1/2:   gamma={gamma_wide[closest_to_half]:.4f}, "
              f"inv={inv_wide[closest_to_half]:.6f}")
        ext_idx = np.argmin(inv_wide)
        print(f"  Global extremum:   gamma={gamma_wide[ext_idx]:.4f}, "
              f"inv={inv_wide[ext_idx]:.8f}")

    # === Visualization ===
    fig, axes = plt.subplots(2, 2, figsize=(15, 11))

    # Top-left: All braids overlaid
    ax = axes[0, 0]
    colors = ['blue', 'red', 'green', 'purple', 'orange', 'brown']
    for (name, r), c in zip(results.items(), colors):
        ax.plot(gamma_vals, r['inv'], color=c, linewidth=1.8, label=name)
        if r['has_reversal']:
            ax.plot(r['peak_gamma'], r['peak_inv'], 'o', color=c, markersize=8)
    ax.axhline(y=-0.5, color='gray', linestyle=':', alpha=0.5, label='-1/2')
    ax.axhline(y=-0.25, color='gray', linestyle='--', alpha=0.5, label='-1/4')
    ax.axhline(y=-0.125, color='gray', linestyle='-.', alpha=0.5, label='-1/8')
    ax.set_xlabel('gamma')
    ax.set_ylabel('Trace Invariant')
    ax.set_title('All Braid Variants: Invariant vs Shear')
    ax.legend(fontsize=7, loc='best')
    ax.grid(True, alpha=0.3)

    # Top-right: Baselines vs crossing count
    ax = axes[0, 1]
    crossing_counts = []
    baselines = []
    labels = []
    for name, r in results.items():
        n = len(ALL_BRAIDS[name])
        crossing_counts.append(n)
        baselines.append(r['baseline'])
        labels.append(name)
    ax.scatter(crossing_counts, baselines, s=100, zorder=5)
    for x, y, l in zip(crossing_counts, baselines, labels):
        ax.annotate(l, (x, y), textcoords="offset points", xytext=(5, 5), fontsize=7)
    # Power of 2 reference
    ns = np.array([3, 4, 5, 6])
    ax.plot(ns, -2.0**(-ns/2), 'r--', alpha=0.5, label='-2^(-n/2)')
    ax.plot(ns, -1.0/ns, 'g--', alpha=0.5, label='-1/n')
    ax.set_xlabel('Number of crossings')
    ax.set_ylabel('Baseline invariant (gamma=0)')
    ax.set_title('Baseline vs Crossing Count')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Bottom-left: Extremum gamma vs crossing count
    ax = axes[1, 0]
    peak_gammas = []
    for name, r in results.items():
        n = len(ALL_BRAIDS[name])
        if r['has_reversal']:
            ax.scatter(n, r['peak_gamma'], s=100, zorder=5, color='red')
            peak_gammas.append((n, r['peak_gamma']))
        else:
            ax.scatter(n, r['peak_gamma'], s=100, zorder=5, color='gray', marker='x')
    # 1/n reference
    ax.plot(ns, 1.0/ns, 'b--', alpha=0.5, label='gamma = 1/n')
    ax.set_xlabel('Number of crossings')
    ax.set_ylabel('Extremum gamma')
    ax.set_title('Threshold gamma vs Crossing Count\n(red = reversal, gray x = monotonic)')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Bottom-right: Extremum invariant vs crossing count
    ax = axes[1, 1]
    for name, r in results.items():
        n = len(ALL_BRAIDS[name])
        color = 'red' if r['has_reversal'] else 'gray'
        marker = 'o' if r['has_reversal'] else 'x'
        ax.scatter(n, r['peak_inv'], s=100, zorder=5, color=color, marker=marker)
        ax.annotate(f"{r['peak_inv']:.4f}", (n, r['peak_inv']),
                    textcoords="offset points", xytext=(5, 5), fontsize=8)
    ax.axhline(y=-0.5, color='orange', linestyle=':', alpha=0.7, label='-1/2')
    ax.set_xlabel('Number of crossings')
    ax.set_ylabel('Extremum invariant')
    ax.set_title('Extremum Value vs Crossing Count')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    plt.suptitle('CURL curl v2.2: The Sequence Hunter\n'
                 'Braids from 3 to 6 crossings | Prime triad [2,3,5]',
                 fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig('curl_curl_v2_2_output.png', dpi=150, bbox_inches='tight')
    print(f"\nPlot saved to: curl_curl_v2_2_output.png")
    plt.show()


if __name__ == "__main__":
    main()
