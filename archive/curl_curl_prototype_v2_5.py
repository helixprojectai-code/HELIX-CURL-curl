#!/usr/bin/env python3
"""
CURL curl Prototype v2.5 -- The Complex Plane
Constitutional Unitary Resonant Lattice (CURL)

The Scooby Snack: the gamma sweep doesn't degrade the invariant.
It ROTATES the trace through the complex plane.
gamma=1/3 is where the trace hits the real axis.

Investigations:
  1. |Tr| constancy across full gamma sweep (all braids)
  2. Complex plane trajectory of Tr(M) as gamma sweeps
  3. Phase angle of Tr vs gamma -- is the rotation linear?
  4. The definitive figure: trefoil trace spiral in C
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


def complex_trace(crossings, gamma=0.0):
    """Return full complex trace (unnormalized)."""
    return np.trace(braid_matrix(crossings, gamma))


TREFOIL = [(0, 1, 2, 3), (1, 2, 3, 5), (0, 1, 2, 3)]
DBL_TREFOIL = TREFOIL + TREFOIL
TRIPLE_TREFOIL = TREFOIL + TREFOIL + TREFOIL


def main():
    print("=" * 70)
    print("CURL curl v2.5 -- The Complex Plane")
    print("=" * 70)

    gamma_vals = np.linspace(0, 1.0, 2000)

    braids = {
        'Trefoil (3)': TREFOIL,
        'Trefoil^2 (6)': DBL_TREFOIL,
        'Trefoil^3 (9)': TRIPLE_TREFOIL,
    }

    all_traces = {}
    for name, braid in braids.items():
        traces = np.array([complex_trace(braid, g) for g in gamma_vals])
        all_traces[name] = traces

    # === 1. Magnitude constancy ===
    print("\n--- 1. Trace Magnitude Constancy ---")
    print(f"{'Braid':<20} {'|Tr| min':<14} {'|Tr| max':<14} {'|Tr| mean':<14} {'Variation':<14}")
    print("-" * 70)
    for name, traces in all_traces.items():
        mags = np.abs(traces)
        variation = (np.max(mags) - np.min(mags)) / np.mean(mags)
        print(f"{name:<20} {np.min(mags):<14.8f} {np.max(mags):<14.8f} "
              f"{np.mean(mags):<14.8f} {variation:<14.2e}")

    # === 2. Phase angle analysis ===
    print("\n--- 2. Phase Angle of Tr(M) ---")
    for name, traces in all_traces.items():
        phases = np.angle(traces)
        print(f"\n  {name}:")
        # Key gamma points
        for g_target, g_label in [(0, "0"), (1/3, "1/3"), (2/3, "2/3"), (1.0, "1")]:
            idx = np.argmin(np.abs(gamma_vals - g_target))
            tr = traces[idx]
            ph = np.angle(tr)
            print(f"    gamma={g_label:<6} Tr = {tr.real:+.4f}{tr.imag:+.4f}j  "
                  f"|Tr|={abs(tr):.4f}  phase={ph:.6f} = {ph/np.pi:.6f}*pi")
            # Check if phase is a nice fraction of pi
            for num, den in [(0,1),(1,6),(1,4),(1,3),(1,2),(2,3),(3,4),(5,6),
                             (1,1),(-1,6),(-1,4),(-1,3),(-1,2),(-2,3),(-3,4),(-5,6),(-1,1)]:
                if abs(ph/np.pi - num/den) < 0.005:
                    print(f"             -> phase = {num}/{den} * pi")

    # === 3. Is the rotation linear in gamma? ===
    print("\n--- 3. Phase Rotation Rate ---")
    for name, traces in all_traces.items():
        phases = np.unwrap(np.angle(traces))
        # Linear fit
        coeffs = np.polyfit(gamma_vals, phases, 1)
        residuals = phases - np.polyval(coeffs, gamma_vals)
        max_residual = np.max(np.abs(residuals))
        print(f"\n  {name}:")
        print(f"    Linear fit: phase = {coeffs[0]:.6f}*gamma + {coeffs[1]:.6f}")
        print(f"    Slope = {coeffs[0]:.6f} = {coeffs[0]/np.pi:.6f}*pi")
        print(f"    Max residual from linear: {max_residual:.6f} rad = {max_residual/np.pi:.6f}*pi")
        if max_residual < 0.1:
            print(f"    VERDICT: Rotation is LINEAR in gamma")
        else:
            print(f"    VERDICT: Rotation is NONLINEAR")
            # Try quadratic
            coeffs2 = np.polyfit(gamma_vals, phases, 2)
            residuals2 = phases - np.polyval(coeffs2, gamma_vals)
            max_res2 = np.max(np.abs(residuals2))
            print(f"    Quadratic fit residual: {max_res2:.6f}")
            print(f"    Quadratic coeffs: {coeffs2[0]:.4f}*g^2 + {coeffs2[1]:.4f}*g + {coeffs2[2]:.4f}")

    # === 4. Where does each braid cross the real axis? ===
    print("\n--- 4. Real Axis Crossings (Im(Tr) = 0) ---")
    for name, traces in all_traces.items():
        imag = traces.imag
        # Find zero crossings
        crossings_idx = []
        for i in range(len(imag) - 1):
            if imag[i] * imag[i+1] < 0:
                # Linear interpolation
                g_cross = gamma_vals[i] - imag[i] * (gamma_vals[i+1] - gamma_vals[i]) / (imag[i+1] - imag[i])
                tr_at_cross = traces[i].real  # approximately
                crossings_idx.append((g_cross, tr_at_cross))

        print(f"\n  {name}:")
        for g_cross, re_at_cross in crossings_idx:
            print(f"    Im(Tr)=0 at gamma = {g_cross:.6f}, Re(Tr) = {re_at_cross:.4f}")
            # Check if gamma is algebraic
            for num, den, label in [(1,3,"1/3"), (2,3,"2/3"), (1,2,"1/2"),
                                     (1,1,"1"), (3,5,"3/5"), (1,6,"1/6")]:
                if abs(g_cross - num/den) < 0.005:
                    print(f"      -> gamma = {label}")

    # === DEFINITIVE FIGURE ===
    fig = plt.figure(figsize=(18, 14))

    # Layout: 2x3 grid
    # Top row: complex plane trajectories for each braid
    # Bottom row: magnitude, phase angle, and the combined view

    # Top-left: Trefoil in complex plane
    ax = fig.add_subplot(2, 3, 1)
    tr = all_traces['Trefoil (3)']
    re, im = tr.real, tr.imag
    scatter = ax.scatter(re, im, c=gamma_vals, cmap='coolwarm', s=3, zorder=3)
    # Mark key points
    idx_0 = 0
    idx_third = np.argmin(np.abs(gamma_vals - 1/3))
    ax.plot(re[idx_0], im[idx_0], 'go', markersize=12, label='gamma=0', zorder=5)
    ax.plot(re[idx_third], im[idx_third], 'r*', markersize=15, label='gamma=1/3', zorder=5)
    # Draw circle of constant |Tr|
    theta_circle = np.linspace(0, 2*np.pi, 200)
    r_circle = np.abs(tr[0])
    ax.plot(r_circle * np.cos(theta_circle), r_circle * np.sin(theta_circle),
            'gray', linestyle=':', alpha=0.4)
    ax.axhline(y=0, color='black', linewidth=0.5, alpha=0.3)
    ax.axvline(x=0, color='black', linewidth=0.5, alpha=0.3)
    ax.set_xlabel('Re(Tr)')
    ax.set_ylabel('Im(Tr)')
    ax.set_title('Trefoil: Trace in Complex Plane')
    ax.legend(fontsize=8)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.2)
    plt.colorbar(scatter, ax=ax, label='gamma', shrink=0.8)

    # Top-center: Double-trefoil in complex plane
    ax = fig.add_subplot(2, 3, 2)
    tr = all_traces['Trefoil^2 (6)']
    re, im = tr.real, tr.imag
    scatter = ax.scatter(re, im, c=gamma_vals, cmap='coolwarm', s=3, zorder=3)
    ax.plot(re[idx_0], im[idx_0], 'go', markersize=12, label='gamma=0', zorder=5)
    ax.plot(re[idx_third], im[idx_third], 'r*', markersize=15, label='gamma=1/3', zorder=5)
    r_circle = np.abs(tr[0])
    ax.plot(r_circle * np.cos(theta_circle), r_circle * np.sin(theta_circle),
            'gray', linestyle=':', alpha=0.4)
    ax.axhline(y=0, color='black', linewidth=0.5, alpha=0.3)
    ax.axvline(x=0, color='black', linewidth=0.5, alpha=0.3)
    ax.set_xlabel('Re(Tr)')
    ax.set_ylabel('Im(Tr)')
    ax.set_title('Trefoil^2: Trace in Complex Plane')
    ax.legend(fontsize=8)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.2)
    plt.colorbar(scatter, ax=ax, label='gamma', shrink=0.8)

    # Top-right: Triple-trefoil in complex plane
    ax = fig.add_subplot(2, 3, 3)
    tr = all_traces['Trefoil^3 (9)']
    re, im = tr.real, tr.imag
    scatter = ax.scatter(re, im, c=gamma_vals, cmap='coolwarm', s=3, zorder=3)
    ax.plot(re[idx_0], im[idx_0], 'go', markersize=12, label='gamma=0', zorder=5)
    ax.plot(re[idx_third], im[idx_third], 'r*', markersize=15, label='gamma=1/3', zorder=5)
    r_circle = np.abs(tr[0])
    ax.plot(r_circle * np.cos(theta_circle), r_circle * np.sin(theta_circle),
            'gray', linestyle=':', alpha=0.4)
    ax.axhline(y=0, color='black', linewidth=0.5, alpha=0.3)
    ax.axvline(x=0, color='black', linewidth=0.5, alpha=0.3)
    ax.set_xlabel('Re(Tr)')
    ax.set_ylabel('Im(Tr)')
    ax.set_title('Trefoil^3: Trace in Complex Plane')
    ax.legend(fontsize=8)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.2)
    plt.colorbar(scatter, ax=ax, label='gamma', shrink=0.8)

    # Bottom-left: |Tr| vs gamma for all braids
    ax = fig.add_subplot(2, 3, 4)
    for name, traces in all_traces.items():
        ax.plot(gamma_vals, np.abs(traces), linewidth=2, label=name)
    ax.axvline(x=1/3, color='red', linestyle='--', alpha=0.5, label='gamma=1/3')
    ax.set_xlabel('gamma')
    ax.set_ylabel('|Tr(M)|')
    ax.set_title('Trace Magnitude vs Shear')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Bottom-center: Phase angle vs gamma
    ax = fig.add_subplot(2, 3, 5)
    for name, traces in all_traces.items():
        phases = np.unwrap(np.angle(traces))
        ax.plot(gamma_vals, phases / np.pi, linewidth=2, label=name)
    ax.axvline(x=1/3, color='red', linestyle='--', alpha=0.5, label='gamma=1/3')
    ax.axhline(y=-1, color='gray', linestyle=':', alpha=0.4, label='phase = -pi (real neg)')
    ax.axhline(y=0, color='gray', linestyle=':', alpha=0.4, label='phase = 0 (real pos)')
    ax.set_xlabel('gamma')
    ax.set_ylabel('Phase(Tr) / pi')
    ax.set_title('Trace Phase Angle vs Shear')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    # Bottom-right: All three braids overlaid in complex plane
    ax = fig.add_subplot(2, 3, 6)
    colors_map = {'Trefoil (3)': 'blue', 'Trefoil^2 (6)': 'red', 'Trefoil^3 (9)': 'purple'}
    for name, traces in all_traces.items():
        # Normalize to unit circle for comparison
        normalized = traces / np.abs(traces[0])
        re, im = normalized.real, normalized.imag
        ax.plot(re, im, color=colors_map[name], linewidth=1.5, label=name, alpha=0.7)
        ax.plot(re[idx_0], im[idx_0], 'o', color=colors_map[name], markersize=10, zorder=5)
        ax.plot(re[idx_third], im[idx_third], '*', color=colors_map[name], markersize=14, zorder=5)
    # Unit circle
    ax.plot(np.cos(theta_circle), np.sin(theta_circle), 'gray', linestyle=':', alpha=0.4)
    ax.axhline(y=0, color='black', linewidth=0.5, alpha=0.3)
    ax.axvline(x=0, color='black', linewidth=0.5, alpha=0.3)
    ax.set_xlabel('Re(Tr) normalized')
    ax.set_ylabel('Im(Tr) normalized')
    ax.set_title('All Braids Normalized\n(circles = gamma=0, stars = gamma=1/3)')
    ax.legend(fontsize=8)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.2)

    plt.suptitle('CURL curl v2.5: The Complex Plane\n'
                 'The gamma sweep ROTATES the trace. gamma=1/3 is where it hits the real axis.',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('curl_curl_v2_5_output.png', dpi=150, bbox_inches='tight')
    print(f"\nPlot saved to: curl_curl_v2_5_output.png")
    plt.show()


if __name__ == "__main__":
    main()
