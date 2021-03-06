.. _framework_design:

.. index:: Particle, Bond, Angle, Dihedral, Simulation, Structure, Class, Improper, MPI, Boost, mpi4py, parameters, periodic table, units


*********************************************
STREAMM code description
*********************************************

StructureContainer Class
============================

Object-oriented design is used throughout STREAMM to enable ease of
use and the ability to update and extend its functionality. 
The StructureContainer class is a data structure for describing a
collection of discrete particles. These particles have unique integer
IDs and spatial positions and can have user specified attributes such
as mass, charge and type. These particles can have 2-body (bond),
3-body (angle) and 4-body (dihedral) interactions, which are
implemented by the python classes Particle, Bond, Angle and Dihedral.
Impropers are special dihedral 4-body interactions.

Each of these classes has an associated container. For example,
multiple Particle objects are held in an instance of a
ParticleContainer class. These containers are essentially modified
dictionaries that map a unique integer ID to an object.
All IDs referred to by the subcontainers are consistent.
The embedded docstrings for the modules containing the classes above
and their related containers are:

- :mod:`particles`
- :mod:`bonds`
- :mod:`angles`
- :mod:`dihedrals`
- :mod:`impropers`

Finally, a StructureContainer object is a container for the Particle, Bond,
Angle Dihedral and Improper containers. This class is in the module
:mod:`structureContainer`

.. figure:: figures/strucC.png
   :align: center
   :scale: 40%

The StructureContainer must contain a ParticleContainer at a minimum
(eg for setting Gaussian runs when no connectivity information is requested).
StructureContainer objects can be created without Bonds, Angles,
Dihedrals and/or Impropers, with the default empty containers being set automatically.


MPI Wrapper Class
============================

.. toctree::
   :maxdepth: 1

   mpi_interface.rst


Molecular Building-Block Assembler
========================================

.. toctree::
   :maxdepth: 1

   donoracceptorsystems.rst



Simulation Classes
===========================================

These classes make use of the StructureContainer to organize data needed to run specific simulations.
The `Simulation` class is an interface to the derived classes `simulationLAMMPS1` and `simulationGaussian1`.
The derived classes have specific methods for input/output that are specific to particular applications
and projects. The intent is for users to be able to design additional derived classes for other projects
and/or additional simulation packages. There is one example in the `tools-tests` (see :mod:`test_dumpLammps`)
illustrating the LAMMPS simulation derived class.

- :mod:`simulation`
- :mod:`simulationLAMMPS1`
- :mod:`simulationGaussian1`



External Utilities
===========================================

A number of utility classes are included in STREAMM that use the core functionality described above.
These utility classes are used in a number of :ref:`examples` included in the documentation.
The embedded docstrings for these are listed below.

- :mod:`parameters`
- :mod:`periodictable`
- :mod:`units`



Class APIs
======================================

.. toctree::
   :maxdepth: 1

   docstr_particles.rst
   docstr_bonds.rst
   docstr_angles.rst
   docstr_dihedrals.rst
   docstr_impropers.rst
   docstr_structureContainer.rst
   docstr_simulation.rst
   docstr_simulationLAMMPS1.rst
   docstr_simulationGaussian1.rst
   docstr_mpiBase.rst
   docstr_extras.rst
