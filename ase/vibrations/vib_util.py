from ase import units
def freq_to_energy(vib_freq):
    vib_energies = [units._hplanck*(1/units._e) * units._c*100.0 * nu for nu in vib_freq]
    return vib_energies

def energy_to_freq(vib_energies):
    vib_freq = [units._e/units._hplanck * 100.0/units._c * E for E in vib_energies]
    return vib_freq
