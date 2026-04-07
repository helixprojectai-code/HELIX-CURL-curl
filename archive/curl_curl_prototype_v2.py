#!/usr/bin/env python3
"""
CURL curl Prototype v2 -- Three-Body Shortcut
Constitutional Unitary Resonant Lattice (CURL)

v2 changes from v1:
  - Strand-aware R-matrix: sigma_1 uses primes (2,3), sigma_2 uses primes (3,5)
  - Uniform gamma scaling: theta_p = ln(p) * (1 + gamma) everywhere
  - Emergent threshold detection via second derivative (inflection point)
  - Commutator norm analysis: ||[O_p, O_q]|| across all three prime pairs
"""

import numpy as np
import matplotlib.pyplot as plt

# Pauli matrices
sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)


def n_hat_p(p):
    """Unit vector for prime p: orientation from ln p."""
    ln_p = np.log(p)
    v = np.array([np.sin(ln_p), np.cos(ln_p), np.tanh(ln_p)], dtype=float)
    return v / np.linalg.norm(v)


def O_p(p, gamma=0.0):
    """SU(2) unitary rotation for prime p -- the 'curl' operator."""
    ln_p = np.log(p)
    theta = ln_p * (1 + gamma)  # v2: uniform gamma scaling
    nx, ny, nz = n_hat_p(p)
    n_dot_sigma = nx * sigma_x + ny * sigma_y + nz * sigma_z
    I2 = np.eye(2, dtype=complex)
    return np.cos(theta / 2) * I2 - 1j * np.sin(theta / 2) * n_dot_sigma


def R_matrix(p, q, gamma=0.0):
    """Strand-aware R-matrix: crossing between primes p and q."""
    Op = O_p(p, gamma)
    Oq = O_p(q, gamma)

    SWAP = np.array([[1, 0, 0, 0],
                     [0, 0, 1, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 1]], dtype=complex)

    phase = np.exp(1j * np.pi / 4 * (1 + gamma))

    U = np.kron(Op, Oq)
    U_dag = U.conj().T
    R_basic = phase * SWAP
    return U @ R_basic @ U_dag


def trefoil_braid_matrix(gamma=0.0):
    """
    Trefoil braid word: sigma_1 sigma_2 sigma_1
    v2: each generator uses the correct prime pair for its strand position.
      sigma_1 (strands 0,1) -> primes (2, 3)
      sigma_2 (strands 1,2) -> primes (3, 5)
    """
    dim = 8
    M = np.eye(dim, dtype=complex)

    crossings = [
        (0, 1, 2, 3),  # sigma_1: strands 0,1 -> primes 2,3
        (1, 2, 3, 5),  # sigma_2: strands 1,2 -> primes 3,5
        (0, 1, 2, 3),  # sigma_1: strands 0,1 -> primes 2,3
    ]

    for si, sj, p, q in crossings:
        R = R_matrix(p, q, gamma)
        if si == 0 and sj == 1:
            R_full = np.kron(R, np.eye(2, dtype=complex))
        elif si == 1 and sj == 2:
            R_full = np.kron(np.eye(2, dtype=complex), R)
        else:
            continue
        M = R_full @ M

    return M


def compute_invariant(gamma=0.0):
    """Compute trace invariant for trefoil at shear gamma."""
    M = trefoil_braid_matrix(gamma)
    trace = np.trace(M)
    return trace.real / 8.0


def commutator_norm(p, q, gamma=0.0):
    """Frobenius norm of [O_p, O_q] = O_p O_q - O_q O_p."""
    Op = O_p(p, gamma)
    Oq = O_p(q, gamma)
    comm = Op @ Oq - Oq @ Op
    return np.linalg.norm(comm, 'fro')


def simulate_threshold():
    """Sweep gamma, detect emergent threshold, analyze commutators."""
    gamma_vals = np.linspace(0, 0.50, 500)
    invariants = np.array([compute_invariant(g) for g in gamma_vals])
    baseline = invariants[0]

    # Second derivative to find inflection point
    d1 = np.gradient(invariants, gamma_vals)
    d2 = np.gradient(d1, gamma_vals)

    # Inflection = where |d2| is maximized (sharpest curvature change)
    inflection_idx = np.argmax(np.abs(d2))
    gamma_inflection = gamma_vals[inflection_idx]

    # Commutator norms across all three prime pairs
    comm_23 = [commutator_norm(2, 3, g) for g in gamma_vals]
    comm_35 = [commutator_norm(3, 5, g) for g in gamma_vals]
    comm_25 = [commutator_norm(2, 5, g) for g in gamma_vals]
    # Total non-commutativity
    comm_total = np.array(comm_23) + np.array(comm_35) + np.array(comm_25)

    # Print results
    print("Computing v2 trefoil invariant (strand-aware, uniform gamma)...")
    print(f"{'gamma':<10} {'Invariant':<16} {'d2(inv)':<14} {'CommTotal':<12} {'Status':<10}")
    print("-" * 65)

    for i, g in enumerate(gamma_vals):
        if i == 0 or abs(g - gamma_inflection) < 0.003 or abs(g - 0.17) < 0.003 \
                or g % 0.1 < 0.003:
            status = "LOCKED" if g < gamma_inflection else "UNSTABLE"
            marker = " <<< INFLECTION" if abs(g - gamma_inflection) < 0.003 else ""
            print(f"{g:<10.4f} {invariants[i]:<16.6f} {d2[i]:<14.6f} "
                  f"{comm_total[i]:<12.6f} {status:<10}{marker}")

    # Analysis
    pre = invariants[gamma_vals < gamma_inflection]
    post = invariants[gamma_vals >= gamma_inflection]

    print(f"\n{'=' * 65}")
    print("CURL curl v2 ANALYSIS")
    print(f"{'=' * 65}")
    print(f"\nBaseline invariant (gamma=0):       {baseline:.6f}")
    print(f"Theoretical:                        {-1/(2*np.sqrt(2)):.6f}")
    print(f"\nEMERGENT INFLECTION POINT:          gamma = {gamma_inflection:.4f}")
    print(f"  (v1 hardcoded threshold was:      gamma = 0.1700)")
    print(f"\nPre-inflection  mean:               {np.mean(pre):.6f} +/- {np.std(pre):.6f}")
    print(f"Post-inflection mean:               {np.mean(post):.6f} +/- {np.std(post):.6f}")
    print(f"Pre-inflection  RSD:                {np.std(pre)/(abs(np.mean(pre))+1e-10)*100:.2f}%")
    print(f"Post-inflection RSD:                {np.std(post)/(abs(np.mean(post))+1e-10)*100:.2f}%")
    print(f"\nCommutator norms at gamma=0:")
    print(f"  ||[O_2, O_3]||:                   {comm_23[0]:.6f}")
    print(f"  ||[O_3, O_5]||:                   {comm_35[0]:.6f}")
    print(f"  ||[O_2, O_5]||:                   {comm_25[0]:.6f}")
    print(f"  Total:                            {comm_total[0]:.6f}")
    print(f"\nCommutator norms at inflection (gamma={gamma_inflection:.4f}):")
    print(f"  ||[O_2, O_3]||:                   {comm_23[inflection_idx]:.6f}")
    print(f"  ||[O_3, O_5]||:                   {comm_35[inflection_idx]:.6f}")
    print(f"  ||[O_2, O_5]||:                   {comm_25[inflection_idx]:.6f}")
    print(f"  Total:                            {comm_total[inflection_idx]:.6f}")

    # --- Visualization ---
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Top-left: Trace invariant with emergent threshold
    ax = axes[0, 0]
    ax.plot(gamma_vals, invariants, 'b-', linewidth=2, label='Trace invariant')
    ax.axvline(x=gamma_inflection, color='red', linestyle='--', linewidth=2,
               label=f'Emergent inflection ({gamma_inflection:.4f})')
    ax.axvline(x=0.17, color='orange', linestyle=':', linewidth=1.5,
               alpha=0.7, label='v1 threshold (0.17)')
    ax.axhline(y=baseline, color='gray', linestyle=':', alpha=0.5)
    ax.axvspan(0, gamma_inflection, alpha=0.08, color='green')
    ax.axvspan(gamma_inflection, gamma_vals[-1], alpha=0.08, color='red')
    ax.set_xlabel('Shear gamma')
    ax.set_ylabel('Normalized Trace Invariant')
    ax.set_title('v2: Strand-Aware Trefoil Invariant')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Top-right: Second derivative (curvature)
    ax = axes[0, 1]
    ax.plot(gamma_vals, d2, 'purple', linewidth=1.5)
    ax.axvline(x=gamma_inflection, color='red', linestyle='--', linewidth=2,
               label=f'Max |d2| at {gamma_inflection:.4f}')
    ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    ax.set_xlabel('Shear gamma')
    ax.set_ylabel('d2(invariant)/d(gamma)2')
    ax.set_title('Second Derivative (Inflection Detection)')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Bottom-left: Commutator norms
    ax = axes[1, 0]
    ax.plot(gamma_vals, comm_23, label='||[O_2, O_3]||', linewidth=1.5)
    ax.plot(gamma_vals, comm_35, label='||[O_3, O_5]||', linewidth=1.5)
    ax.plot(gamma_vals, comm_25, label='||[O_2, O_5]||', linewidth=1.5)
    ax.plot(gamma_vals, comm_total, 'k--', label='Total', linewidth=2)
    ax.axvline(x=gamma_inflection, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    ax.set_xlabel('Shear gamma')
    ax.set_ylabel('Frobenius Norm')
    ax.set_title('Commutator Norms: Non-Commutativity of Prime Pairs')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Bottom-right: Deviation % with emergent threshold
    ax = axes[1, 1]
    deviations = np.abs(invariants - baseline) / (np.abs(baseline) + 1e-10) * 100
    ax.plot(gamma_vals, deviations, 'green', linewidth=2)
    ax.axvline(x=gamma_inflection, color='red', linestyle='--', linewidth=2,
               label=f'Inflection ({gamma_inflection:.4f})')
    ax.axhline(y=17, color='orange', linestyle=':', alpha=0.7, label='17% deviation')
    ax.fill_between(gamma_vals, 0, deviations,
                    where=(gamma_vals >= gamma_inflection),
                    alpha=0.2, color='red')
    ax.set_xlabel('Shear gamma')
    ax.set_ylabel('Deviation from baseline (%)')
    ax.set_title('Stability Deviation')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    plt.suptitle('CURL curl v2: Strand-Aware Prime-Indexed Trefoil\n'
                 'Primes [2,3,5] | Braid: sigma_1(2,3) sigma_2(3,5) sigma_1(2,3)',
                 fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig('curl_curl_v2_output.png', dpi=150, bbox_inches='tight')
    print(f"\nPlot saved to: curl_curl_v2_output.png")
    plt.show()


if __name__ == "__main__":
    print("=" * 65)
    print("CURL curl Prototype v2 -- Three-Body Shortcut")
    print("Strand-Aware | Uniform Gamma | Emergent Threshold")
    print("=" * 65)
    print("""
v2 changes:
  - sigma_1 uses primes (2, 3), sigma_2 uses primes (3, 5)
  - gamma scaling uniform: theta_p = ln(p) * (1 + gamma)
  - Threshold detected from inflection point, not hardcoded
  - Commutator norms computed for all three prime pairs
""")
    simulate_threshold()
