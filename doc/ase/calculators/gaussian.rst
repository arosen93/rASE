.. module:: ase.calculators.gaussian

Introduction
============

Gaussian_ is a computational chemistry code for electronic structure
calculations. Gaussian's density functional theory calculations are
based on Gaussian basis functions.


.. _Gaussian: http://gaussian.com/



Setup
=====================

By default, the gaussian calculator assumes that the Gaussian executable
is given by ``g09``. If this is not the executable of choice, you must
define the executable in an environment variable named ``GAUSSIAN_EXE``.

For instance, if you wish to run Gaussian 16, you can set 
``export GAUSSIAN_EXE='g16'`` somewhere in your submission script
or ``.bashrc``.

Parameters
==========

The list of default parameters are shown below. The ``method`` keyword can be
used to specify the electronic structure method. For density functional theory
calculations, ``method`` should be set to the desired functional using the
appropriate Gaussian keyword. Like normal Gaussian keywords, all Link 0 commands
should be set as arguments in the gaussian calculator (e.g. ``nprocshared=8``).
This holds true for the charge and spin multiplicity as well.

By default, the ``force`` keyword is set so that ASE optimizers can be used
with the gaussian calculator.

================  ========  ==============================   ============================
keyword           type      default value                    description
================  ========  ==============================   ============================
``method``        ``str``   ``'hf'``                         Electronic structure method
``charge``        ``int``   ``0``                            Net charge on the system
``multiplicity``  ``int``   Sum of the initial magmoms + 1   Net spin multiplicity
``basis``         ``str``   ``'6-31g*'``                     Basis set
``force``         ``str``   ``'force'``                      Request force calculation
================  ========  ==============================   ============================

Minimal Examples
=================

A minimal example is shown below for the optimization of H2
using the PBE functional::

    from ase import Atoms
    from ase.optimize import BFGS
    from ase.calculators.gaussian import Gaussian
    from ase.io import write
    h2 = Atoms('H2',positions=[[0, 0, 0],[0, 0, 0.7]])
    h2.calc = Gaussian(method='PBEPBE')
    opt = BFGS(h2)
    opt.run(fmax=0.02)
    write('h2.xyz', h2)
    h2.get_potential_energy()

An example is shown below for the optimization of triplet
O2 using the PBE functional and def2-SVP basis set. Link 0
commands involving the number of CPUs and allocated memory
are also set.
::

    from ase import Atoms
    from ase.optimize import BFGS
    from ase.calculators.gaussian import Gaussian
    from ase.io import write
    o2 = Atoms('O2',positions=[[0, 0, 0],[0, 0, 1.24]])
    o2.calc = Gaussian(method='PBEPBE',
      basis='def2svp',
      multiplicity=3,
      nprocshared=4,
      mem='8GB')
    opt = BFGS(h2)
    opt.run(fmax=0.02)
    write('o2.xyz', o2)
    o2.get_potential_energy()

.. highlight:: python