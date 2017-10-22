rASE - Rosen revision to the Atomic Simulation Environment
=============================

ASE is a set of tools and Python modules for setting up, manipulating,
running, visualizing and analyzing atomistic simulations. 
The rASE repository contains all changes made by A.S. Rosen.

The major changes are listed below. Only the mandatory arguments are shown. Please refer to the corresponding
sections of the program for more details.

*New module*: **ase.vibrations.vib_util**

``vib_util.freq_to_energy(vib_freq)``:

Converts a list of vibrational frequencies in cm^(-1) to eV

``vib_util.energy_to_freq(vib_energies)``:

Converts a list of vibrational energies in eV to cm^(-1)

*New module*: **ase.calculators.vasp.vib**

``vib.get_vibrational_frequencies(atoms)``:

Adopted from J.Kitchin. Takes an atoms object and gets the vibrational
frequencies from an OUTCAR file

``vib.get_vibrational_modes(atoms)``:

Adopted from J.Kitchin. Takes an atoms object and gets the vibrational
modes from an OUTCAR file

*Modification*: **ase.thermochemistry**

Changed the reference pressure from 1 atm to 1 bar, per IUPAC standards.

*Modification*: **ase.calculators.vasp.create_input**

Changed the default pseudopotentials to be those recommended in the VASP manual

Requirements
------------

* Python 2.7, 3.4-3.6
* NumPy

Optional:

* SciPy
* Matplotlib


Installation
------------

Add ``~/rASE`` to your $PYTHONPATH environment variable and add
``~/rASE/bin`` to $PATH (assuming ``~/rASE`` is where your rASE folder is).

