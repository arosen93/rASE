.. module:: ase.calculators.gamess_us

=========
GAMESS-US
=========

`GAMESS-US <https://www.msg.chem.iastate.edu/gamess/index.html>`_ is a
computational chemistry software package based on gaussian basis functions.


Setup
=====

.. highlight:: bash

Ask your systems administrator to install GAMESS-US for you, or obtain
it yourself from the
`GAMESS-US download page <https://www.msg.chem.iastate.edu/gamess/download.html>`_.
Note that while GAMESS-US is available at no cost (including its source code),
it is not distributed under an open source license, thus you are not permitted
to redistribute copies of GAMESS-US or its source code.

GAMESS-US is distributed with a ``rungms`` script to run calculations. This
script must be customized for your computer or cluster. ASE expects that a
properly customized version of this ``rungms`` script will be present in your
``$PATH``. The default argument to run GAMESS-US in ASE is::

  rungms PREFIX.inp > PREFIX.log 2> PREFIX.err

The default ``rungms`` script can be instructed to run across a number of CPU
cores through the following syntax::

  rungms PREFIX.inp <VERSION> <NUMBER_OF_CORES> <CORES_PER_NODE> [<NUMBER_OF_NODES>]

For example, if you want to run a calculation on 8 cores, you might set the
``ASE_GAMESSUS_COMMAND`` environment variable to the following::

  rungms PREFIX.inp 00 8 > PREFIX.log 2> PREFIX.err

Alternatively, this command can be passed as a string directly to the
``GAMESSUS`` Calculator with the ``command`` keyword argument.

Examples
========

Here is a command line example of how to optimize the geometry of a
water molecule using the PBE density functional::

  $ ase build H2O | ase run gamess_us -p xc=PBE -f 0.02
  $ ase gui stdin.traj@-1 -tg "a(1,0,2),d(0,1)"
  102.59049267228833 1.0079388022627982

.. highlight:: python

An example of creating a GAMESS-US calculator using the python interface is::

  from ase.calculators.gamess_us import GAMESSUS

  calc = GAMESSUS(contrl=dict(scftyp='rhf', dfttyp='b3lyp', ispher=1),
                  dft=dict(dc=True, idcver=3),
                  basis=dict(gbasis='ccd'))

This will run a B3LYP/cc-pVDZ calculation with Stefan Grimme's DFT-D3
empirical dispersion correction.

Parameters
==========

.. highlight:: none

GAMESS-US organized keywords into blocks delimited by ``$<BLOCKNAME>`` and
``$END``. The ``GAMESSUS`` calculator represents these blocks as dictionaries.
For example, consider the following block of input::

   $CONTRL SCFTYP=RHF DFTTYP=M06 $END
   $SYSTEM MWORDS=4 $END
   $BASIS
     GBASIS=N31
     NGAUSS=6
     NDFUNC=1
   $END
   $DFT NRAD=96 NLEB=1202 $END

.. highlight:: python

Note that keywords within a block can be on the same or different lines.
Equivalent input will be generated by invoking the ``GAMESSUS`` calculator
with the following arguments::

  calc = GAMESSUS(contrl=dict(scftyp='rhf', dfttyp='m06'),
                  system=dict(mwords=4),
                  basis=dict(gbasis='n31', ngauss=6, ndfunc=1),
                  dft=dict(nrad=96, nleb=1202))

.. highlight:: none


Note that though GAMESS-US is case insensitive, Python is case sensitive.
The ``GAMESSUS`` calculator expects lowercase keywords.

Most input files can be constructed in this way. The ``GAMESSUS`` calculator also
has several special keywords, which are described in the table below

============== ======== ================ ==================================================
keyword        type     default value    description
============== ======== ================ ==================================================
``label``      ``str``  ``'gamess_us'``  Used to name input and output files.
``userscr``    ``str``  ``None``         The ``USERSCR`` directory defined in ``rungms``.
                                         If not provided, ASE will attempt to automatically
                                         determine the correct value from your ``rungms``
                                         script. This is not guaranteed to work, in which case
                                         you will need to manually provide the proper location.
``basis``      ``dict``  See description Specifies the arguments that go into the ``$BASIS``
                                         block in the GAMESS-US input file. Defaults to
                                         ``{'gbasis': 'n21', 'ngauss': 3}``, i.e. 3-21G.
                                         Alternately, ``basis`` accepts a dictionary of
                                         literal basis set definitions where the keys
                                         correspond to element type or atom index.
``ecp``        ``dict``  ``None``        A dictionary of literal ECP definitions. Keys should
                                         be either an element symbol or an atom index.
============== ======== ================ ==================================================

.. autoclass:: GAMESSUS
