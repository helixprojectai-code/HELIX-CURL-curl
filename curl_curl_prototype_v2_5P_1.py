import numpy as np
import matplotlib.pyplot as plt

# --- Fundamental Constants ---
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
    return np.cos(theta / 2) * np.eye(2, dtype=complex) - 1j * np.sin(theta / 2) * n_dot_sigma

def R_matrix(p, q, gamma=0.0):
    Op, Oq = O_p(p, gamma), O_p(q, gamma)
    SWAP = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], dtype=complex)
    phase = np.exp(1j * np.pi / 4 * (1 + gamma))
    U = np.kron(Op, Oq)
    return U @ (phase * SWAP) @ U.conj().T

def braid_matrix(crossings, gamma=0.0):
    M = np.eye(8, dtype=complex)
    for si, sj, p, q in crossings:
        R = R_matrix(p, q, gamma)
        if si == 0 and sj == 1: R_full = np.kron(R, np.eye(2, dtype=complex))
        elif si == 1 and sj == 2: R_full = np.kron(np.eye(2, dtype=complex), R)
        M = R_full @ M
    return M

def main():
    print("=" * 70)
    print("CURL curl v2.5P -- THE PULSE INVESTIGATION")
    print("=" * 70)

    # The missing line fixed here:
    gamma_vals = np.linspace(0, 1.0, 1000)

    # Defining the powers
    TREFOIL = [(0, 1, 2, 3), (1, 2, 3, 5), (0, 1, 2, 3)]
    braids = {
        'Trefoil^1': TREFOIL,
        'Trefoil^2': TREFOIL * 2,
        'Trefoil^3': TREFOIL * 3,
        'Trefoil^4': TREFOIL * 4, # THE 8-HUNTER
    }

    print(f"{'Braid':<15} {'|Tr| Mean':<15} {'Phase Slope':<15} {'Var':<10}")
    print("-" * 70)

    for name, crossings in braids.items():
        traces = np.array([np.trace(braid_matrix(crossings, g)) for g in gamma_vals])
        mags = np.abs(traces)
        phases = np.unwrap(np.angle(traces))
        slope = np.polyfit(gamma_vals, phases, 1)[0] / np.pi
        variation = (np.max(mags) - np.min(mags)) / np.mean(mags)
        
        print(f"{name:<15} {np.mean(mags):<15.8f} {slope:<15.4f} {variation:<10.2e}")
        # === THE RESET PROBE ===
    print("\n" + "="*40)
    print("THE TREFOIL^4 RESET PROBE (gamma=1/3)")
    print("="*40)
    
    # Just multiply the list directly to be safe
    M_quad = braid_matrix(TREFOIL * 4, 1/3)
    eigenvals = np.linalg.eigvals(M_quad)
    
    print(f"{'Eigenvalue (Rounded)':<30} {'Magnitude':<15}")
    print("-" * 45)
    for ev in eigenvals:
        # Rounding to 10 decimal places to clear the floating point noise
        ev_rounded = np.round(ev, 10)
        print(f"{str(ev_rounded):<30} {abs(ev):<15.8f}")
        
    print(f"\nTrace (Sum of Evals): {np.sum(eigenvals):.8f}")
    
    # Check 1/3 Alignment
    idx_third = np.argmin(np.abs(gamma_vals - 1/3))
    print("\n--- Alignment at Gamma = 1/3 ---")
    for name, crossings in braids.items():
        tr = np.trace(braid_matrix(crossings, 1/3))
        print(f"{name:<15}: Tr = {tr.real:+.4f} {tr.imag:+.4f}j")

if __name__ == "__main__":
    main()
