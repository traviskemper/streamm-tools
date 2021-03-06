.. _thiophene:


Thiophene
-------------------------------------------------------

*Generate structure and quantum input*

Generate a .xyz file, a `Gaussian <http://www.gaussian.com/>`_  .com input file and a submission
script ".pbs"  for thiophene by running ::

   donoracceptorsystems.py  "thiophene" -b BuildingBlocks  -r 1 

this creates the file::

   mols/thiophene/acc1_thiophene_n1.xyz

which is just a file containing the Cartesian coordinates of a
thiophene molecule.  You can view with your favorite viewer. The -r option is set to 1 to generate a single molecule rather than an oligomer.  The
`Gaussian <http://www.gaussian.com/>`_  input file based on
"donoracceptor.com.template" is::

   mols/thiophene/acc1_thiophene_n1.com

And the pbs submission script file  based on `donoracceptor.pbs.template` is::

   mols/thiophene/acc1_thiophene_n1.pbs

*Generate topology  files*

The .xyz file is read in to get the atomic positions and
atom types, and a `.itp
<http://www.gromacs.org/Documentation/File_Formats/.itp_File>`_ file
"conj.itp"  is read in to get a set of reference Force Field
parameters. The conj.itp file contains parameters from the OPLSaa
force-field that is included in the `GROMACS release
<http://www.gromacs.org/Downloads>`_.  

For `LAMMPS <http://lammps.sandia.gov/>`_ input generation run `xyz2data.py`::

  xyz2data.py  --in_itp conj.itp 
    --in_xyz  mols/thiophene/acc1_thiophene_n1.xyz 
    --out_data  mols/thiophene/acc1_thiophene_n1.data

This creates the `.data <http://lammps.sandia.gov/doc/2001/data_format.html>`_  formated `LAMMPS <http://lammps.sandia.gov/>`_ input file::

    mols/thiophene/acc1_thiophene_n1.data

And input files for a `GROMACS <http://www.gromacs.org>`_ run are
generated `xyz2gromacs.py`::

   xyz2gromacs.py --in_itp conj.itp 
      --in_xyz  mols/thiophene/acc1_thiophene_n1.xyz 
      --out_gro mols/thiophene/acc1_thiophene_n1.gro 
      --out_top mols/thiophene/acc1_thiophene_n1.top
      --out_itp  acc1_thiophene_n1.itp 

This creates the `GROMACS <http://www.gromacs.org>`_ input files::

      mols/thiophene/acc1_thiophene_n1.gro 
      mols/thiophene/acc1_thiophene_n1.top
      acc1_thiophene_n1.itp 

where the `.gro <http://manual.gromacs.org/current/online/gro.html>`_ file includes the structural information, the `.top <http://manual.gromacs.org/current/online/top.html>`_ file is the connectivity file and the new `.itp <http://www.gromacs.org/Documentation/File_Formats/.itp_File>`_ file contains the Force-field parameters for the molecule.  

.. note::

   This entire example can be executed by running::

      thiophene.sh

   in `tools/examples`. Needed files and scripts are 

   *  donoracceptor.com.template
   *  donoracceptor.pbs.template 
   *  conj.itp      
   *  xyz2data.py
   *  xyz2gromacs.py
