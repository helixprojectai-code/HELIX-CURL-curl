#!/usr/bin/env python3
"""
CURL curl Prototype v2.4 -- Loose Ends
Constitutional Unitary Resonant Lattice (CURL)

Four investigations:
  1. Imaginary part of trace -- zero, or carrying hidden structure?
  2. Phase factor sweep -- is pi/4 special, or do algebraic values appear elsewhere?
  3. Raw trace analysis -- what are the unnormalized values?
  4. SWAP embedding verification -- does the (0,2) crossing convention matter?
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


def R_matrix(p, q, gamma=0.0, phase_angle=np.pi/4):
    Op = O_p(p, gamma)
    Oq = O_p(q, gamma)
    SWAP = np.array([[1, 0, 0, 0],
                     [0, 0, 1, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 1]], dtype=complex)
    phase = np.exp(1j * phase_angle * (1 + gamma))
    U = np.kron(Op, Oq)
    U_dag = U.conj().T
    return U @ (phase * SWAP) @ U_dag


def braid_matrix(crossings, gamma=0.0, phase_angle=np.pi/4):
    dim = 8
    M = np.eye(dim, dtype=complex)
    for si, sj, p, q in crossings:
        R = R_matrix(p, q, gamma, phase_angle)
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


def braid_matrix_alt_swap(crossings, gamma=0.0, phase_angle=np.pi/4):
    """Alternative (0,2) embedding: swap strands 0<->1 instead of 1<->2."""
    dim = 8
    M = np.eye(dim, dtype=complex)
    for si, sj, p, q in crossings:
        R = R_matrix(p, q, gamma, phase_angle)
        if si == 0 and sj == 1:
            R_full = np.kron(R, np.eye(2, dtype=complex))
        elif si == 1 and sj == 2:
            R_full = np.kron(np.eye(2, dtype=complex), R)
        elif si == 0 and sj == 2:
            # Alt convention: swap strands 0<->1, apply R on (1,2), swap back
            SWAP01 = np.kron(
                np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]], dtype=complex),
                np.eye(2, dtype=complex))
            R_on_12 = np.kron(np.eye(2, dtype=complex), R)
            R_full = SWAP01 @ R_on_12 @ SWAP01
        else:
            continue
        M = R_full @ M
    return M


TREFOIL = [
    (0, 1, 2, 3), (1, 2, 3, 5), (0, 1, 2, 3),
]

TRIANGLE = [
    (0, 1, 2, 3), (1, 2, 3, 5), (0, 2, 2, 5),
]

DBL_TREFOIL = [
    (0, 1, 2, 3), (1, 2, 3, 5), (0, 1, 2, 3),
    (0, 1, 2, 3), (1, 2, 3, 5), (0, 1, 2, 3),
]


def investigation_1_imaginary():
    """Check the imaginary part of the trace across gamma sweep."""
    print("=" * 70)
    print("INVESTIGATION 1: Imaginary Part of Trace")
    print("=" * 70)

    gamma_vals = np.linspace(0, 0.5, 500)
    braids = {
        'Trefoil': TREFOIL,
        'Triangle': TRIANGLE,
        'Dbl-Trefoil': DBL_TREFOIL,
    }

    results = {}
    for name, braid in braids.items():
        reals = []
        imags = []
        for g in gamma_vals:
            M = braid_matrix(braid, g)
            tr = np.trace(M)
            reals.append(tr.real)
            imags.append(tr.imag)
        reals = np.array(reals)
        imags = np.array(imags)
        results[name] = (reals, imags)

        print(f"\n  {name}:")
        print(f"    Im(Tr) at gamma=0:     {imags[0]:.2e}")
        print(f"    Im(Tr) at gamma=1/3:   {imags[np.argmin(np.abs(gamma_vals - 1/3))]:.2e}")
        print(f"    Max |Im(Tr)|:          {np.max(np.abs(imags)):.2e}")
        print(f"    Mean |Im(Tr)|:         {np.mean(np.abs(imags)):.2e}")

        if np.max(np.abs(imags)) < 1e-10:
            print(f"    VERDICT: Imaginary part is ZERO (machine epsilon)")
        else:
            print(f"    VERDICT: Imaginary part is NONZERO -- carries information!")
            # Check if imaginary part has algebraic values
            im_at_0 = imags[0] / 8.0
            im_at_third = imags[np.argmin(np.abs(gamma_vals - 1/3))] / 8.0
            print(f"    Normalized Im at gamma=0:   {im_at_0:.8f}")
            print(f"    Normalized Im at gamma=1/3: {im_at_third:.8f}")

            # Test against known algebraic values
            for val, label in [(0, "0"), (1/(2*np.sqrt(2)), "1/(2sqrt2)"),
                               (0.5, "1/2"), (1.0, "1"),
                               (np.sqrt(2)/2, "sqrt2/2"), (np.sqrt(3)/2, "sqrt3/2"),
                               (1/np.sqrt(2), "1/sqrt2")]:
                if abs(abs(im_at_0) - val) < 0.001:
                    print(f"    |Im| at gamma=0 matches: {label}")
                if abs(abs(im_at_third) - val) < 0.001:
                    print(f"    |Im| at gamma=1/3 matches: {label}")

    return gamma_vals, results


def investigation_2_phase_sweep():
    """Sweep the phase angle to see if pi/4 is special."""
    print("\n" + "=" * 70)
    print("INVESTIGATION 2: Phase Factor Sweep")
    print("=" * 70)

    phase_angles = np.linspace(0, np.pi, 500)
    gamma_test_points = [0.0, 1/3]

    results = {}
    for g in gamma_test_points:
        reals = []
        imags = []
        for phi in phase_angles:
            M = braid_matrix(TREFOIL, g, phase_angle=phi)
            tr = np.trace(M) / 8.0
            reals.append(tr.real)
            imags.append(tr.imag)
        results[g] = (np.array(reals), np.array(imags))

    # Find where algebraic values appear
    print(f"\n  Scanning for algebraic values in Re(Tr/8) at gamma=0:")
    reals_0 = results[0.0][0]
    targets = [
        (-1/(2*np.sqrt(2)), "-1/(2sqrt2)"),
        (-0.5, "-1/2"),
        (-0.25, "-1/4"),
        (0.0, "0"),
        (0.25, "+1/4"),
        (0.5, "+1/2"),
        (1/(2*np.sqrt(2)), "+1/(2sqrt2)"),
        (1.0, "+1"),
        (-1.0, "-1"),
    ]
    for val, label in targets:
        matches = np.where(np.abs(reals_0 - val) < 0.002)[0]
        if len(matches) > 0:
            for idx in matches[:3]:  # Show up to 3 matches
                phi = phase_angles[idx]
                # Check if phi is a nice fraction of pi
                phi_over_pi = phi / np.pi
                print(f"    {label} appears at phase = {phi:.6f} = {phi_over_pi:.6f}*pi")
                for num, den in [(1,6),(1,5),(1,4),(1,3),(2,5),(1,2),(3,5),(2,3),(3,4),(4,5),(5,6)]:
                    if abs(phi_over_pi - num/den) < 0.005:
                        print(f"      -> phase = pi*{num}/{den}")

    print(f"\n  Scanning for algebraic values in Re(Tr/8) at gamma=1/3:")
    reals_third = results[1/3][0]
    for val, label in targets:
        matches = np.where(np.abs(reals_third - val) < 0.002)[0]
        if len(matches) > 0:
            for idx in matches[:3]:
                phi = phase_angles[idx]
                phi_over_pi = phi / np.pi
                print(f"    {label} appears at phase = {phi:.6f} = {phi_over_pi:.6f}*pi")
                for num, den in [(1,6),(1,5),(1,4),(1,3),(2,5),(1,2),(3,5),(2,3),(3,4),(4,5),(5,6)]:
                    if abs(phi_over_pi - num/den) < 0.005:
                        print(f"      -> phase = pi*{num}/{den}")

    # Is pi/4 the ONLY angle that gives -1/(2sqrt2) at gamma=0?
    target_val = -1/(2*np.sqrt(2))
    close_to_target = np.abs(reals_0 - target_val) < 0.0001
    matching_phases = phase_angles[close_to_target]
    print(f"\n  Phases giving -1/(2sqrt2) at gamma=0:")
    for phi in matching_phases:
        print(f"    phase = {phi:.6f} = {phi/np.pi:.6f}*pi")

    return phase_angles, results


def investigation_3_raw_trace():
    """Look at unnormalized trace values."""
    print("\n" + "=" * 70)
    print("INVESTIGATION 3: Raw (Unnormalized) Trace")
    print("=" * 70)

    braids = {
        'Trefoil': TREFOIL,
        'Dbl-Trefoil': DBL_TREFOIL,
    }

    key_gammas = [0.0, 1/3]

    for name, braid in braids.items():
        print(f"\n  {name}:")
        for g in key_gammas:
            M = braid_matrix(braid, g)
            tr = np.trace(M)
            print(f"    gamma={g:.4f}:")
            print(f"      Raw Tr     = {tr.real:+.8f} {tr.imag:+.8f}j")
            print(f"      |Tr|       = {abs(tr):.8f}")
            print(f"      Tr/8       = {tr.real/8:+.8f} {tr.imag/8:+.8f}j")
            print(f"      Tr/dim     = {tr.real/8:+.8f}  (dim=8=2^3)")

            # Check raw trace against algebraic values
            raw_re = tr.real
            for val, label in [(-8*1/(2*np.sqrt(2)), "-8/(2sqrt2) = -2sqrt2"),
                               (-4.0, "-4"), (-2*np.sqrt(2), "-2sqrt2"),
                               (-2.0, "-2"), (-np.sqrt(2), "-sqrt2"),
                               (0.0, "0"), (2.0, "2"), (4.0, "4"),
                               (2*np.sqrt(2), "2sqrt2"), (8.0, "8"),
                               (-8.0, "-8")]:
                if abs(raw_re - val) < 0.001:
                    print(f"      Raw Re matches: {label} = {val:.6f}")

            # Eigenvalue analysis
            eigenvalues = np.linalg.eigvals(M)
            unique_mags = np.unique(np.round(np.abs(eigenvalues), 6))
            print(f"      Eigenvalue magnitudes: {unique_mags}")
            # Check if all eigenvalues are on unit circle (unitary)
            all_unit = np.allclose(np.abs(eigenvalues), 1.0, atol=1e-10)
            print(f"      All on unit circle: {all_unit}")


def investigation_4_swap_verify():
    """Verify (0,2) crossing embedding convention doesn't affect results."""
    print("\n" + "=" * 70)
    print("INVESTIGATION 4: SWAP Embedding Verification")
    print("=" * 70)

    # Only braids with (0,2) crossings are affected
    gamma_vals = np.linspace(0, 0.5, 200)

    inv_original = []
    inv_alt = []
    for g in gamma_vals:
        M1 = braid_matrix(TRIANGLE, g)
        M2 = braid_matrix_alt_swap(TRIANGLE, g)
        inv_original.append(np.trace(M1).real / 8.0)
        inv_alt.append(np.trace(M2).real / 8.0)

    inv_original = np.array(inv_original)
    inv_alt = np.array(inv_alt)
    diff = np.abs(inv_original - inv_alt)

    print(f"\n  Triangle braid with (0,2) crossing:")
    print(f"    Max |difference|:     {np.max(diff):.2e}")
    print(f"    Mean |difference|:    {np.mean(diff):.2e}")

    if np.max(diff) < 1e-10:
        print(f"    VERDICT: Conventions are IDENTICAL")
    else:
        print(f"    VERDICT: Conventions DIFFER -- embedding matters!")
        print(f"\n    Original baseline:    {inv_original[0]:.8f}")
        print(f"    Alt baseline:         {inv_alt[0]:.8f}")

        # Find extrema for both
        ext1 = np.argmin(inv_original)
        ext2 = np.argmin(inv_alt)
        print(f"    Original extremum:    {inv_original[ext1]:.8f} at gamma={gamma_vals[ext1]:.4f}")
        print(f"    Alt extremum:         {inv_alt[ext2]:.8f} at gamma={gamma_vals[ext2]:.4f}")

        # Check if alt also produces algebraic values
        print(f"\n    Alt at gamma=0:       {inv_alt[0]:.8f}")
        print(f"    Alt at gamma=1/3:     {inv_alt[np.argmin(np.abs(gamma_vals - 1/3))]:.8f}")

        for val, label in [(-1/(2*np.sqrt(2)), "-1/(2sqrt2)"), (-0.5, "-1/2"),
                           (-0.25, "-1/4"), (0.0, "0"), (0.5, "+1/2"), (1.0, "+1")]:
            if abs(inv_alt[0] - val) < 0.001:
                print(f"    Alt baseline matches: {label}")

    return gamma_vals, inv_original, inv_alt


def plot_all(imag_data, phase_data, swap_data):
    gamma_vals_im, imag_results = imag_data
    phase_angles, phase_results = phase_data
    gamma_vals_sw, inv_orig, inv_alt = swap_data

    fig, axes = plt.subplots(2, 2, figsize=(15, 11))

    # 1) Imaginary part
    ax = axes[0, 0]
    for name, (re, im) in imag_results.items():
        ax.plot(gamma_vals_im, im, linewidth=1.5, label=f'{name} Im(Tr)')
    ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    ax.axvline(x=1/3, color='red', linestyle='--', alpha=0.5, label='gamma=1/3')
    ax.set_xlabel('gamma')
    ax.set_ylabel('Im(Tr)')
    ax.set_title('Investigation 1: Imaginary Part of Trace')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # 2) Phase sweep
    ax = axes[0, 1]
    for g, (re, im) in phase_results.items():
        ax.plot(phase_angles / np.pi, re, linewidth=1.5, label=f'Re(Tr/8) at gamma={g:.3f}')
    ax.axvline(x=0.25, color='red', linestyle='--', linewidth=2, label='pi/4')
    # Mark algebraic values
    for val, label in [(-1/(2*np.sqrt(2)), '-1/(2sqrt2)'), (-0.5, '-1/2'),
                       (0.0, '0'), (0.5, '+1/2'), (1.0, '+1')]:
        ax.axhline(y=val, color='gray', linestyle=':', alpha=0.4)
    ax.set_xlabel('Phase angle / pi')
    ax.set_ylabel('Re(Tr/8)')
    ax.set_title('Investigation 2: Phase Factor Sweep\n(Is pi/4 special?)')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # 3) Raw trace -- show eigenvalue phases at gamma=0 and gamma=1/3
    ax = axes[1, 0]
    for g, color, label in [(0.0, 'blue', 'gamma=0'), (1/3, 'red', 'gamma=1/3')]:
        M = braid_matrix(TREFOIL, g)
        eigs = np.linalg.eigvals(M)
        phases = np.angle(eigs)
        mags = np.abs(eigs)
        ax.scatter(phases / np.pi, mags, s=80, color=color, label=label, zorder=5)
    ax.set_xlabel('Eigenvalue phase / pi')
    ax.set_ylabel('Eigenvalue magnitude')
    ax.set_title('Investigation 3: Eigenvalue Structure\n(Trefoil braid matrix)')
    ax.axhline(y=1.0, color='gray', linestyle=':', alpha=0.5, label='Unit circle')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # 4) SWAP verification
    ax = axes[1, 1]
    ax.plot(gamma_vals_sw, inv_orig, 'b-', linewidth=2, label='Original (swap 1<->2)')
    ax.plot(gamma_vals_sw, inv_alt, 'r--', linewidth=2, label='Alt (swap 0<->1)')
    ax.axvline(x=1/3, color='gray', linestyle='--', alpha=0.5)
    ax.set_xlabel('gamma')
    ax.set_ylabel('Trace Invariant')
    ax.set_title('Investigation 4: SWAP Convention\n(Triangle braid with (0,2) crossing)')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    plt.suptitle('CURL curl v2.4: Loose Ends\n'
                 'Imaginary part | Phase factor | Raw trace | SWAP convention',
                 fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig('curl_curl_v2_4_output.png', dpi=150, bbox_inches='tight')
    print(f"\nPlot saved to: curl_curl_v2_4_output.png")
    plt.show()


if __name__ == "__main__":
    print("=" * 70)
    print("CURL curl v2.4 -- Loose Ends Investigation")
    print("=" * 70)

    imag_data = investigation_1_imaginary()
    phase_data = investigation_2_phase_sweep()
    investigation_3_raw_trace()
    swap_data = investigation_4_swap_verify()
    plot_all(imag_data, phase_data, swap_data)

    print("\n" + "=" * 70)
    print("v2.4 COMPLETE")
    print("=" * 70)
