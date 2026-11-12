<!-- Source: https://dci.dci-gitlab.cines.fr/webextranet/software_stack/cines_software_stack/spack_products_catalog.html -->
<!-- Title: CINES’ Spack module catalog -->

<a id="cines-spack-module-catalog"></a>

<a id="adastra-software-stack-spack-product-catalog"></a>

# CINES’ Spack module catalog

CINES provides tools, libraries and simulation softwares built using Spack. A list is given below. We explain how to use these modules in [this document](spack.md#adastra-software-stack-cines-software-stack-spack-using).

**Note**

CINES provide more variants in older environment but they are not shown here. You may enquire about these using `module spider`.

<a id="currently-in-production-or-deprecated-products"></a>

## Currently in production or deprecated products

| Software name | CINES Spack modules (environment) | Variant/version | Description |
| --- | --- | --- | --- |
| adios2 | `GCC-CPU-4.0.0` | `2.10.2-mpi` | The Adaptable Input Output System version 2, developed in the Exascale Computing Program |
| `GCC-CPU-5.0.0` | `2.10.2-mpi` |
| `GCC-GPU-5.0.0` | `2.10.2-mpi` |
| amber | `GCC-CPU-4.0.0` | `24-cpu` | Amber is a suite of biomolecular simulation programs together with Amber tools. |
| autoconf | `GCC-CPU-5.0.0` | `2.72` | Autoconf – system configuration part of autotools |
| `GCC-GPU-5.0.0` | `2.72` |
| boost | `CCE-CPU-4.0.0` | `1.86.0-mpi` | Boost provides free peer-reviewed portable C++ source libraries, emphasizing libraries that work well with the C++ Standard Library. |
| `CCE-CPU-5.0.0` | `1.88.0-mpi` |
| `CCE-GPU-4.0.0` | `1.86.0-mpi` |
| `CCE-GPU-5.0.0` | `1.88.0-mpi` |
| `GCC-CPU-4.0.0` | `1.86.0-mpi` |
| `GCC-CPU-5.0.0` | `1.88.0-mpi` |
| `GCC-GPU-4.0.0` | `1.86.0-mpi` |
| `GCC-GPU-5.0.0` | `1.88.0-mpi` |
| bzip2 | `GCC-CPU-5.0.0` | `1.0.8` | bzip2 is a freely available, patent free high-quality data compressor. It typically compresses files to within 10% to 15% of the best available techniques (the PPM family of statistical compressors), whilst being around twice as fast at compression and six times faster at decompression. |
| `GCC-GPU-5.0.0` | `1.0.8` |
| cdo | `CCE-CPU-5.0.0` | `2.5.2-omp-mpi` | CDO is a collection of command line Operators to manipulate and analyse Climate and NWP model Data. |
| `GCC-CPU-4.0.0` | `2.4.4-omp-mpi` |
| `GCC-GPU-5.0.0` | `2.5.2-omp-mpi` |
| cgns | `GCC-CPU-4.0.0` | `4.4.0-int64-mpi` | The CFD General Notation System (CGNS) provides a general, portable, and extensible standard for the storage and retrieval of computational fluid dynamics (CFD) analysis data. |
| `GCC-CPU-5.0.0` | `4.5.0-int64-mpi` |
| `GCC-GPU-4.0.0` | `4.4.0-int64-mpi` |
| `GCC-GPU-5.0.0` | `4.5.0-int64-mpi` |
| cp2k | `GCC-CPU-4.0.0` | `2024.3-elpa-omp-mpi` | CP2K is a quantum chemistry and solid state physics software package that can perform atomistic simulations of solid state, liquid, molecular, periodic, material, crystal, and biological systems |
| `GCC-CPU-5.0.0` | `2025.1-elpa-omp-mpi` |
| `GCC-GPU-4.0.0` | `2024.3-omp-rocm-mpi-gpu` |
| `GCC-GPU-5.0.0` | `2024.3-omp-rocm-mpi-gpu` |
| dftbplus | `GCC-CPU-4.0.0` | `24.1-omp-mpi` | DFTB+ is an implementation of the Density Functional based Tight Binding (DFTB) method, containing many extensions to the original method. |
| `GCC-CPU-5.0.0` | `24.1-omp-mpi` |
| gmake | `GCC-CPU-5.0.0` | `4.4.1` | GNU Make is a tool which controls the generation of executables and other non-source files of a program from the program’s source files. |
| `GCC-GPU-5.0.0` | `4.4.1` |
| gromacs | `CCE-CPU-4.0.0` | `2024.3-omp-mpi` | GROMACS is a molecular dynamics package primarily designed for simulations of proteins, lipids and nucleic acids. It was originally developed in the Biophysical Chemistry department of University of Groningen, and is now maintained by contributors in universities and research centers across the world. |
| `CCE-CPU-5.0.0` | `2025.2-omp-mpi` |
| `CCE-GPU-4.0.0` | `2024.3-omp-plumed-mpi-gpu` |
| `CCE-GPU-5.0.0` | `2025.4-omp-rocm-mpi-gpu` |
| `GCC-CPU-4.0.0` | `2024.3-cp2k-omp-mpi` |
| hdf5 | `CCE-CPU-4.0.0` | `1.14.5-mpi` | HDF5 is a data model, library, and file format for storing and managing data. It supports an unlimited variety of datatypes, and is designed for flexible and efficient I/O and for high volume and complex data. |
| `CCE-CPU-5.0.0` | `1.14.6-mpi` |
| `CCE-GPU-4.0.0` | `1.14.5-mpi` |
| `CCE-GPU-5.0.0` | `1.14.6-mpi` |
| `GCC-CPU-4.0.0` | `1.14.5-mpi` |
| `GCC-CPU-5.0.0` | `1.14.6-mpi` |
| `GCC-GPU-4.0.0` | `1.14.5-mpi` |
| `GCC-GPU-5.0.0` | `1.14.6-mpi` |
| heffte | `CCE-CPU-5.0.0` | `2.4.1-rocm-mpi-gpu` | Highly Efficient FFT for Exascale |
| `CCE-GPU-4.0.0` | `2.4.1-rocm-mpi-gpu` |
| `CCE-GPU-5.0.0` | `2.4.1-rocm-mpi-gpu` |
| hipsycl | `CCE-GPU-4.0.0` | `24.02.0-rocm-mpi-gpu` | hipSYCL is an implementation of the SYCL standard programming model over NVIDIA CUDA/AMD HIP |
| hypre | `CCE-CPU-4.0.0` | `2.32.0-mpi` | Hypre is a library of high performance preconditioners that features parallel multigrid methods for both structured and unstructured grid problems. |
| `CCE-CPU-5.0.0` | `2.33.0-mpi` |
| `GCC-CPU-4.0.0` | `2.32.0-mpi` |
| `GCC-CPU-5.0.0` | `2.33.0-mpi` |
| `GCC-GPU-4.0.0` | `2.32.0-omp-rocm-mpi-gpu` |
| `GCC-GPU-5.0.0` | `2.33.0-omp-rocm-mpi-gpu` |
| kokkos | `CCE-GPU-5.0.0` | `4.6.01-rocm-gpu` | Kokkos implements a programming model in C++ for writing performance portable applications targeting all major HPC platforms. |
| `GCC-GPU-5.0.0` | `4.6.01-rocm-gpu` |
| lammps | `CCE-GPU-4.0.0` | `20240829.1-plumed-rocm-kokkos-mpi-gpu` | LAMMPS stands for Large-scale Atomic/Molecular Massively Parallel Simulator. |
| `CCE-GPU-5.0.0` | `20250612-plumed-rocm-kokkos-mpi-gpu` |
| `GCC-CPU-4.0.0` | `20240829.1-omp-plumed-kokkos-mpi` |
| libtool | `GCC-CPU-5.0.0` | `2.4.7` | libtool – library building part of autotools. |
| `GCC-GPU-5.0.0` | `2.4.7` |
| magma | `CCE-GPU-4.0.0` | `2.8.0-rocm-gpu` | The MAGMA project aims to develop a dense linear algebra library similar to LAPACK but for heterogeneous/hybrid architectures, starting with current ‘Multicore+GPU’ systems. |
| `CCE-GPU-5.0.0` | `2.8.0-rocm-gpu` |
| `GCC-GPU-5.0.0` | `2.9.0-rocm-gpu` |
| mpfr | `GCC-GPU-5.0.0` | `4.2.1` | The MPFR library is a C library for multiple-precision floating-point computations with correct rounding. |
| mumps | `GCC-CPU-4.0.0` | `5.7.3-int64-omp-mpi` | MUMPS: a MUltifrontal Massively Parallel sparse direct Solver |
| `GCC-CPU-5.0.0` | `5.8.0-int64-omp-mpi` |
| `GCC-GPU-4.0.0` | `5.7.3-int64-omp-mpi` |
| `GCC-GPU-5.0.0` | `5.8.0-int64-omp-mpi` |
| namd | `GCC-CPU-4.0.0` | `3.0.1-mpi` | NAMD is a parallel molecular dynamics code designed for high-performance simulation of large biomolecular systems. |
| `GCC-CPU-5.0.0` | `3.0.2-mpi` |
| `GCC-GPU-4.0.0` | `3.0.1-rocm-gpu-resident-mpi-gpu` |
| `GCC-GPU-5.0.0` | `3.0.2-rocm-gpu-resident-mpi-gpu` |
| netcdf-c | `CCE-CPU-4.0.0` | `4.9.2-mpi` | NetCDF (network Common Data Form) is a set of software libraries and machine-independent data formats that support the creation, access, and sharing of array-oriented scientific data. This is the C distribution. |
| `CCE-CPU-5.0.0` | `4.9.2-mpi` |
| `CCE-GPU-4.0.0` | `4.9.2-mpi` |
| `CCE-GPU-5.0.0` | `4.9.2-mpi` |
| `GCC-CPU-4.0.0` | `4.9.2-mpi` |
| `GCC-CPU-5.0.0` | `4.9.2-mpi` |
| `GCC-GPU-5.0.0` | `4.9.2-mpi` |
| netcdf-cxx | `CCE-CPU-4.0.0` | `4.2-mpi` | Deprecated C++ compatibility bindings for NetCDF. These do NOT read or write NetCDF-4 files, and are no longer maintained by Unidata. Developers should migrate to current NetCDF C++ bindings, in Spack package netcdf-cxx4. |
| `CCE-CPU-5.0.0` | `4.2-mpi` |
| `CCE-GPU-4.0.0` | `4.2-mpi` |
| `CCE-GPU-5.0.0` | `4.2-mpi` |
| `GCC-CPU-4.0.0` | `4.2-mpi` |
| `GCC-CPU-5.0.0` | `4.2-mpi` |
| `GCC-GPU-4.0.0` | `4.2-mpi` |
| `GCC-GPU-5.0.0` | `4.2-mpi` |
| netcdf-cxx4 | `CCE-CPU-4.0.0` | `4.3.1-mpi` | NetCDF (network Common Data Form) is a set of software libraries and machine-independent data formats that support the creation, access, and sharing of array-oriented scientific data. This is the C++ distribution. |
| `CCE-CPU-5.0.0` | `4.3.1-mpi` |
| `CCE-GPU-4.0.0` | `4.3.1-mpi` |
| `CCE-GPU-5.0.0` | `4.3.1-mpi` |
| `GCC-CPU-4.0.0` | `4.3.1-mpi` |
| `GCC-CPU-5.0.0` | `4.3.1-mpi` |
| `GCC-GPU-4.0.0` | `4.3.1-mpi` |
| `GCC-GPU-5.0.0` | `4.3.1-mpi` |
| netcdf-fortran | `CCE-CPU-4.0.0` | `4.6.1-mpi` | NetCDF (network Common Data Form) is a set of software libraries and machine-independent data formats that support the creation, access, and sharing of array-oriented scientific data. This is the Fortran distribution. |
| `CCE-CPU-5.0.0` | `4.6.1-mpi` |
| `CCE-GPU-4.0.0` | `4.6.1-mpi` |
| `CCE-GPU-5.0.0` | `4.6.1-mpi` |
| `GCC-CPU-4.0.0` | `4.6.1-mpi` |
| `GCC-CPU-5.0.0` | `4.6.1-mpi` |
| `GCC-GPU-4.0.0` | `4.6.1-mpi` |
| `GCC-GPU-5.0.0` | `4.6.1-mpi` |
| ninja | `GCC-GPU-5.0.0` | `1.12.1` | Ninja is a small build system with a focus on speed. It differs from other build systems in two major respects: it is designed to have its input files generated by a higher-level build system, and it is designed to run builds as fast as possible. |
| octave | `GCC-CPU-5.0.0` | `9.4.0-mpi` | GNU Octave is a high-level language, primarily intended for numerical computations. |
| openblas | `CCE-CPU-4.0.0` | `0.3.28-omp` | OpenBLAS: An optimized BLAS library |
| `GCC-CPU-4.0.0` | `0.3.28-omp` |
| `GCC-CPU-5.0.0` | `0.3.29-omp` |
| openfoam | `GCC-CPU-4.0.0` | `2412-int64-mpi` | OpenFOAM is a GPL-opensource C++ CFD-toolbox. This offering is supported by OpenCFD Ltd, producer and distributor of the OpenFOAM software via www.openfoam.com, and owner of the OPENFOAM trademark. OpenCFD Ltd has been developing and releasing OpenFOAM since its debut in 2004. |
| `GCC-CPU-5.0.0` | `2412-int64-mpi`  `2506-int64-mpi`  `2512-int64-mpi` |
| openfoam-org | `GCC-CPU-4.0.0` | `12-int64-mpi` | OpenFOAM is a GPL-opensource C++ CFD-toolbox. The openfoam.org release is managed by the OpenFOAM Foundation Ltd as a licensee of the OPENFOAM trademark. This offering is not approved or endorsed by OpenCFD Ltd, producer and distributor of the OpenFOAM software via www.openfoam.com, and owner of the OPENFOAM trademark. |
| `GCC-CPU-5.0.0` | `12-int64-mpi` |
| parallel-netcdf | `CCE-CPU-4.0.0` | `1.12.3-mpi` | PnetCDF (Parallel netCDF) is a high-performance parallel I/O library for accessing files in format compatibility with Unidata’s NetCDF, specifically the formats of CDF-1, 2, and 5. |
| `CCE-CPU-5.0.0` | `1.14.0-mpi` |
| `CCE-GPU-4.0.0` | `1.12.3-mpi` |
| `CCE-GPU-5.0.0` | `1.14.0-mpi` |
| `GCC-CPU-4.0.0` | `1.12.3-mpi` |
| `GCC-CPU-5.0.0` | `1.14.0-mpi` |
| `GCC-GPU-4.0.0` | `1.12.3-mpi` |
| `GCC-GPU-5.0.0` | `1.14.0-mpi` |
| parmetis | `CCE-CPU-5.0.0` | `4.0.3-mpi` | ParMETIS is an MPI-based parallel library that implements a variety of algorithms for partitioning unstructured graphs, meshes, and for computing fill-reducing orderings of sparse matrices. |
| `CCE-GPU-5.0.0` | `4.0.3-mpi` |
| `GCC-CPU-5.0.0` | `4.0.3-mpi` |
| `GCC-GPU-5.0.0` | `4.0.3-mpi` |
| petsc | `CCE-CPU-4.0.0` | `3.22.1-omp-kokkos-mpi` | PETSc is a suite of data structures and routines for the scalable (parallel) solution of scientific applications modeled by partial differential equations. |
| `CCE-CPU-5.0.0` | `3.23.4-omp-kokkos-mpi` |
| `CCE-GPU-5.0.0` | `3.23.4-omp-rocm-kokkos-mpi-gpu` |
| `GCC-CPU-4.0.0` | `3.22.1-omp-kokkos-mpi` |
| `GCC-CPU-5.0.0` | `3.23.4-omp-kokkos-mpi` |
| `GCC-GPU-4.0.0` | `3.22.1-rocm-kokkos-mpi-gpu` |
| `GCC-GPU-5.0.0` | `3.23.4-omp-rocm-kokkos-mpi-gpu` |
| plumed | `CCE-CPU-5.0.0` | `2.9.3-omp-mpi` | PLUMED is an open source library for free energy calculations in molecular systems which works together with some of the most popular molecular dynamics engines. |
| `GCC-CPU-4.0.0` | `2.9.2-omp-mpi` |
| `GCC-CPU-5.0.0` | `2.9.3-omp-mpi` |
| `GCC-GPU-4.0.0` | `2.9.2-omp-mpi` |
| `GCC-GPU-5.0.0` | `2.9.2-omp-mpi` |
| proj | `GCC-GPU-5.0.0` | `9.4.1` | PROJ is a generic coordinate transformation software, that transforms geospatial coordinates from one coordinate reference system (CRS) to another. This includes cartographic projections as well as geodetic transformations. |
| quantum-espresso | `GCC-CPU-4.0.0` | `7.3.1-omp-mpi` | Quantum ESPRESSO is an integrated suite of Open-Source computer codes for electronic-structure calculations and materials modeling at the nanoscale. It is based on density-functional theory, plane waves, and pseudopotentials. |
| `GCC-CPU-5.0.0` | `7.5-omp-mpi` |
| siesta | `GCC-CPU-5.0.0` | `5.4.2-elpa-omp-mpi-openblas` | SIESTA performs electronic structure calculations and ab initio molecular dynamics simulations of molecules and solids. |
| slepc | `CCE-CPU-4.0.0` | `3.22.1-mpi` | Scalable Library for Eigenvalue Problem Computations. |
| `CCE-CPU-5.0.0` | `3.23.2-mpi` |
| `CCE-GPU-4.0.0` | `3.22.1-rocm-mpi-gpu` |
| `CCE-GPU-5.0.0` | `3.23.2-rocm-mpi-gpu` |
| `GCC-CPU-4.0.0` | `3.22.1-mpi` |
| `GCC-CPU-5.0.0` | `3.23.2-mpi` |
| `GCC-GPU-4.0.0` | `3.22.1-rocm-mpi-gpu` |
| `GCC-GPU-5.0.0` | `3.23.2-rocm-mpi-gpu` |
| suite-sparse | `CCE-CPU-5.0.0` | `7.8.3-omp`  `7.8.3` | SuiteSparse is a suite of sparse matrix algorithms |
| `CCE-GPU-5.0.0` | `7.8.3-omp`  `7.8.3` |
| `GCC-CPU-5.0.0` | `7.8.3-omp`  `7.8.3` |
| `GCC-GPU-5.0.0` | `7.8.3-omp`  `7.8.3` |
| sundials | `CCE-CPU-4.0.0` | `7.1.1-mpi` | SUNDIALS (SUite of Nonlinear and DIfferential/ALgebraic equation Solvers) |
| `CCE-CPU-5.0.0` | `7.4.0-mpi` |
| `GCC-CPU-4.0.0` | `7.1.1-mpi` |
| `GCC-CPU-5.0.0` | `7.4.0-mpi` |
| `GCC-GPU-5.0.0` | `7.4.0-mpi` |
| superlu-dist | `CCE-CPU-4.0.0` | `9.1.0-int64-omp-mpi` | A general purpose library for the direct solution of large, sparse, nonsymmetric systems of linear equations on high performance machines. |
| `CCE-CPU-5.0.0` | `9.1.0-int64-omp-mpi` |
| `CCE-GPU-4.0.0` | `9.1.0-int64-omp-rocm-mpi-gpu` |
| `CCE-GPU-5.0.0` | `9.1.0-int64-omp-rocm-mpi-gpu` |
| `GCC-CPU-4.0.0` | `9.1.0-int64-omp-mpi` |
| `GCC-CPU-5.0.0` | `9.1.0-int64-omp-mpi` |
| `GCC-GPU-4.0.0` | `9.1.0-int64-omp-rocm-mpi-gpu` |
| `GCC-GPU-5.0.0` | `9.1.0-int64-omp-rocm-mpi-gpu` |
| swig | `GCC-GPU-5.0.0` | `4.1.1` | SWIG is an interface compiler that connects programs written in C and C++ with scripting languages such as Perl, Python, Ruby, and Tcl. It works by taking the declarations found in C/C++ header files and using them to generate the wrapper code that scripting languages need to access the underlying C/C++ code. In addition, SWIG provides a variety of customization features that let you tailor the wrapping process to suit your application. |
| udunits | `GCC-GPU-5.0.0` | `2.2.28` | Automated units conversion |
| yambo | `GCC-CPU-4.0.0` | `5.3.0-omp-mpi` | Yambo is a FORTRAN/C code for Many-Body calculations in solid state and molecular physics. |
| `GCC-CPU-5.0.0` | `5.3.0-omp-mpi` |

<a id="currently-archived-products"></a>

## Currently archived products

| Software name | CINES Spack modules (environment) | Variant/version | Description |
| --- | --- | --- | --- |
| adios2 | `CCE-CPU-2.0.0` | `2.7.1-mpi-python3` | The Adaptable Input Output System version 2, developed in the Exascale Computing Program |
| `CCE-CPU-2.1.0` | `2.9.0-mpi-python3` |
| `CPE-23.02-aocc-3.2.0-CPU-softs` | `2.7.1-mpi-python3` |
| `CPE-23.02-cce-15.0.1-CPU-softs` | `2.7.1-mpi-python3` |
| `CPE-23.02-gcc-12.2.0-CPU-softs` | `2.7.1-mpi-python3` |
| `GCC-CPU-2.0.0` | `2.7.1-mpi-python3` |
| `GCC-CPU-2.1.0` | `2.9.0-mpi-python3` |
| `GCC-CPU-3.0.0` | `2.9.2-mpi-python3` |
| `GCC-CPU-3.1.0` | `2.9.2-mpi` |
| `GCC-CPU-3.2.0` | `2.10.0-mpi` |
| amber | `GCC-GPU-2.1.0` | `22` | Amber is a suite of biomolecular simulation programs together with Amber tools. |
| `GCC-GPU-3.0.0` | `22` |
| `GCC-GPU-3.1.0` | `22` |
| `GCC-GPU-3.2.0` | `24` |
| aspa | `CCE-GPU-2.0.0` | `master-mpi` | A fundamental premise in ExMatEx is that scale-bridging performed in heterogeneous MPMD materials science simulations will place important demands upon the exascale ecosystem that need to be identified and quantified. |
| `CCE-GPU-2.1.0` | `master-mpi` |
| `CCE-GPU-3.0.0` | `master-mpi` |
| `CCE-GPU-3.1.0` | `master-mpi` |
| `CPE-22.11-cce-15.0.0-softs` | `master-mpi` |
| `CPE-23.02-cce-15.0.1-GPU-softs` | `master-mpi` |
| blitz | `CPE-22.11-gcc-11.2.0-softs` | `1.0.2-python3` | N-dimensional arrays for C++ |
| `CPE-23.02-gcc-12.2.0-GPU-softs` | `1.0.2-python3` |
| `GCC-GPU-2.0.0` | `1.0.2-python3` |
| `GCC-GPU-2.1.0` | `1.0.2-python3` |
| `GCC-GPU-3.0.0` | `1.0.2-python3` |
| boost | `CCE-CPU-2.0.0` | `1.81.0-mpi-python3` | Boost provides free peer-reviewed portable C++ source libraries, emphasizing libraries that work well with the C++ Standard Library. |
| `CCE-CPU-2.1.0` | `1.81.0-mpi-python3` |
| `CCE-CPU-3.0.0` | `1.83.0-mpi-python3` |
| `CCE-CPU-3.1.0` | `1.83.0-mpi` |
| `CCE-CPU-3.2.0` | `1.85.0-mpi` |
| `CCE-GPU-2.0.0` | `1.81.0-mpi-python3` |
| `CCE-GPU-2.1.0` | `1.81.0-mpi-python3` |
| `CCE-GPU-3.0.0` | `1.83.0-mpi-python3` |
| `CCE-GPU-3.1.0` | `1.83.0-mpi` |
| `CCE-GPU-3.2.0` | `1.85.0-mpi` |
| `CPE-22.11-cce-15.0.0-softs` | `1.80.0-mpi-python3` |
| `CPE-22.11-gcc-11.2.0-softs` | `1.80.0-mpi-python3` |
| `CPE-22.11-rocmcc-5.2.3-softs` | `1.80.0-mpi-python3` |
| `CPE-23.02-aocc-3.2.0-CPU-softs` | `1.81.0-mpi-python3` |
| `CPE-23.02-cce-15.0.1-CPU-softs` | `1.81.0-mpi-python3` |
| `CPE-23.02-cce-15.0.1-GPU-softs` | `1.81.0-mpi-python3` |
| `CPE-23.02-gcc-12.2.0-CPU-softs` | `1.81.0-mpi-python3` |
| `CPE-23.02-gcc-12.2.0-GPU-softs` | `1.81.0-mpi-python3` |
| `CPE-23.02-rocmcc-5.3.0-GPU-softs` | `1.81.0-mpi-python3` |
| `GCC-CPU-2.0.0` | `1.81.0-mpi-python3` |
| `GCC-CPU-2.1.0` | `1.81.0-mpi-python3` |
| `GCC-CPU-3.0.0` | `1.83.0-mpi-python3` |
| `GCC-CPU-3.1.0` | `1.83.0-mpi` |
| `GCC-CPU-3.2.0` | `1.85.0-mpi` |
| `GCC-GPU-2.0.0` | `1.81.0-mpi-python3` |
| `GCC-GPU-2.1.0` | `1.81.0-mpi-python3` |
| `GCC-GPU-3.0.0` | `1.83.0-mpi-python3` |
| `GCC-GPU-3.1.0` | `1.83.0-mpi` |
| `GCC-GPU-3.2.0` | `1.85.0-mpi` |
| cdo | `CPE-23.02-cce-15.0.1-CPU-softs` | `2.1.1-mpi-omp-python3` | CDO is a collection of command line Operators to manipulate and analyse Climate and NWP model Data. |
| `GCC-CPU-3.2.0` | `2.4.2-omp-mpi` |
| cgns | `CPE-23.02-aocc-3.2.0-CPU-softs` | `4.3.0-mpi` | The CFD General Notation System (CGNS) provides a general, portable, and extensible standard for the storage and retrieval of computational fluid dynamics (CFD) analysis data. |
| `CPE-23.02-cce-15.0.1-CPU-softs` | `4.3.0-mpi` |
| `CPE-23.02-gcc-12.2.0-CPU-softs` | `4.3.0-mpi` |
| `GCC-CPU-2.0.0` | `4.3.0-mpi` |
| `GCC-CPU-2.1.0` | `4.3.0-mpi-int64` |
| `GCC-CPU-3.0.0` | `4.4.0-mpi-int64` |
| `GCC-CPU-3.1.0` | `4.4.0-int64-mpi` |
| `GCC-CPU-3.2.0` | `4.4.0-int64-mpi` |
| `GCC-GPU-3.2.0` | `4.4.0-int64-mpi` |
| charmpp | `CPE-23.02-gcc-12.2.0-CPU-softs` | `7.0.0-mpi-omp` | Charm++ is a parallel programming framework in C++ supported by an adaptive runtime system, which enhances user productivity and allows programs to run portably from small multicore computers (your laptop) to the largest supercomputers. |
| `GCC-CPU-2.0.0` | `7.0.0-mpi-omp` |
| `GCC-CPU-2.1.0` | `7.0.0-mpi-omp` |
| `GCC-CPU-3.1.0` | `7.0.0-omp-mpi` |
| cmake | `CCE-CPU-2.0.0` | `3.25.2` | A cross-platform, open-source build system. CMake is a family of tools designed to build, test and package software. |
| `CCE-CPU-2.1.0` | `3.25.2` |
| `CCE-CPU-3.0.0` | `3.27.7` |
| `CCE-GPU-2.0.0` | `3.25.2-python3` |
| `CCE-GPU-2.1.0` | `3.25.2-python3` |
| `CCE-GPU-3.0.0` | `3.27.7-python3` |
| `CPE-22.11-cce-15.0.0-softs` | `3.25.0-python3` |
| `CPE-22.11-gcc-11.2.0-softs` | `3.25.0-python3` |
| `CPE-22.11-rocmcc-5.2.3-softs` | `3.25.0-python3` |
| `CPE-23.02-cce-15.0.1-GPU-softs` | `3.25.2-python3` |
| `CPE-23.02-gcc-12.2.0-GPU-softs` | `3.25.2-python3` |
| `CPE-23.02-rocmcc-5.3.0-GPU-softs` | `3.25.2-python3` |
| `GCC-GPU-2.0.0` | `3.25.2-python3` |
| `GCC-GPU-2.1.0` | `3.25.2-python3` |
| `GCC-GPU-3.0.0` | `3.27.7-python3` |
| cp2k | `CPE-22.11-rocmcc-5.2.3-softs` | `8.1-mpi-omp-python3` | CP2K is a quantum chemistry and solid state physics software package that can perform atomistic simulations of solid state, liquid, molecular, periodic, material, crystal, and biological systems |
| `CPE-23.02-gcc-12.2.0-CPU-softs` | `2023.1-mpi-omp-plumed-python3` |
| `CPE-23.02-gcc-12.2.0-GPU-softs` | `2023.1-mpi-elpa-omp-plumed-scalapack-python3` |
| `GCC-CPU-2.0.0` | `2023.1-mpi-omp-plumed-python3` |
| `GCC-CPU-2.1.0` | `2023.1-mpi-omp-plumed-python3` |
| `GCC-CPU-3.0.0` | `2023.2-mpi-elpa-omp-plumed-scalapack-python3` |
| `GCC-CPU-3.1.0` | `2023.2-elpa-omp-plumed-mpi`  `2024.1-elpa-omp-plumed-mpi` |
| `GCC-CPU-3.2.0` | `2024.3-elpa-omp-plumed-mpi` |
| `GCC-GPU-2.0.0` | `2023.1-mpi-elpa-omp-plumed-scalapack-python3` |
| `GCC-GPU-2.1.0` | `2023.1-mpi-elpa-omp-plumed-scalapack-python3` |
| `GCC-GPU-3.0.0` | `2023.2-mpi-elpa-omp-plumed-scalapack-python3` |
| `GCC-GPU-3.1.0` | `2023.2-elpa-omp-plumed-rocm-mpi-gpu`  `2024.1-elpa-omp-plumed-rocm-mpi-gpu` |
| `GCC-GPU-3.2.0` | `2024.3-omp-plumed-rocm-mpi-gpu` |
| cpmd | `CPE-23.02-gcc-12.2.0-CPU-softs` | `4.3-mpi-omp` | The CPMD code is a parallelized plane wave / pseudopotential implementation of Density Functional Theory, particularly designed for ab-initio molecular dynamics. |
| `GCC-CPU-2.0.0` | `4.3-mpi-omp` |
| `GCC-CPU-2.1.0` | `4.3-mpi-omp` |
| `GCC-CPU-3.0.0` | `4.3-mpi-omp` |
| `GCC-CPU-3.1.0` | `4.3-omp-mpi` |
| dataspaces | `CCE-CPU-2.1.0` | `2.2.0-mpi-python3` | DataSpaces v2 based on margo, also called dspaces |
| `GCC-CPU-2.1.0` | `2.2.0-mpi-python3` |
| `GCC-CPU-3.0.0` | `2.2.0-mpi-python3` |
| `GCC-CPU-3.1.0` | `2.2.0-mpi` |
| dftbplus | `CCE-CPU-2.0.0` | `19.1` | DFTB+ is an implementation of the Density Functional based Tight Binding (DFTB) method, containing many extensions to the original method. |
| `CCE-CPU-2.1.0` | `19.1` |
| `CCE-CPU-3.0.0` | `19.1` |
| `CCE-CPU-3.1.0` | `19.1` |
| `CCE-GPU-2.0.0` | `19.1-gpu` |
| `CCE-GPU-2.1.0` | `19.1-gpu` |
| `CPE-22.11-cce-15.0.0-softs` | `19.1-gpu` |
| `CPE-23.02-cce-15.0.1-CPU-softs` | `19.1` |
| `CPE-23.02-cce-15.0.1-GPU-softs` | `19.1-gpu` |
| elpa | `CPE-22.11-gcc-11.2.0-softs` | `2021.11.001-gpu-omp-python3` | Eigenvalue solvers for Petaflop-Applications (ELPA) |
| `CPE-23.02-gcc-12.2.0-GPU-softs` | `2022.11.001-gpu-omp-python3` |
| ferret | `GCC-CPU-2.1.0` | `7.6.0` | Ferret is an interactive computer visualization and analysis environment designed to meet the needs of oceanographers and meteorologists analyzing large and complex gridded data sets. |
| `GCC-CPU-3.0.0` | `7.6.0-python3` |
| `GCC-CPU-3.1.0` | `7.6.0` |
| ffmpeg | `CPE-22.11-gcc-11.2.0-softs` | `4.4.1-python3` | FFmpeg is a complete, cross-platform solution to record, convert and stream audio and video. |
| `CPE-23.02-gcc-12.2.0-GPU-softs` | `5.1.2-python3` |
| `GCC-GPU-2.0.0` | `5.1.2-python3` |
| `GCC-GPU-2.1.0` | `5.1.2-python3` |
| `GCC-GPU-3.0.0` | `6.0-python3` |
| gdb | `CCE-CPU-2.0.0` | `13.1-python3` | GDB, the GNU Project debugger, allows you to see what is going on ‘inside’ another program while it executes – or what another program was doing at the moment it crashed. |
| `CCE-CPU-2.1.0` | `13.1-python3` |
| `CCE-GPU-2.0.0` | `13.1-python3` |
| `CCE-GPU-2.1.0` | `13.1-python3` |
| `CPE-22.11-gcc-11.2.0-softs` | `12.1-python3` |
| `CPE-23.02-aocc-3.2.0-CPU-softs` | `13.1-python3` |
| `CPE-23.02-cce-15.0.1-CPU-softs` | `13.1-python3` |
| `CPE-23.02-cce-15.0.1-GPU-softs` | `13.1-python3` |
| `CPE-23.02-gcc-12.2.0-CPU-softs` | `13.1-python3` |
| `CPE-23.02-gcc-12.2.0-GPU-softs` | `13.1-python3` |
| `CPE-23.02-rocmcc-5.3.0-GPU-softs` | `13.1-python3` |
| `GCC-CPU-2.0.0` | `13.1-python3` |
| `GCC-CPU-2.1.0` | `13.1-python3` |
| `GCC-CPU-3.0.0` | `13.1-python3` |
| `GCC-GPU-2.0.0` | `13.1-python3` |
| `GCC-GPU-2.1.0` | `13.1-python3` |
| `GCC-GPU-3.0.0` | `13.1-python3` |
| gmsh | `GCC-CPU-3.1.0` | `4.12.2-mpi` | Gmsh is a free 3D finite element grid generator with a built-in CAD engine and post-processor. Its design goal is to provide a fast, light and user-friendly meshing tool with parametric input and advanced visualization capabilities. Gmsh is built around four modules: geometry, mesh, solver and post-processing. The specification of any input to these modules is done either interactively using the graphical user interface or in ASCII text files using Gmsh’s own scripting language. |
| gromacs | `CCE-CPU-2.0.0` | `2023-mpi-omp-plumed-python3` | GROMACS is a molecular dynamics package primarily designed for simulations of proteins, lipids and nucleic acids. It was originally developed in the Biophysical Chemistry department of University of Groningen, and is now maintained by contributors in universities and research centers across the world. |
| `CCE-CPU-2.1.0` | `2023-mpi-omp-plumed-python3` |
| `CCE-CPU-3.0.0` | `2023.3-mpi-omp-plumed-python3` |
| `CCE-CPU-3.1.0` | `2023.3-omp-plumed-mpi` |
| `CCE-GPU-2.0.0` | `2022.3-mpi-omp-plumed-python3`  `2023-mpi-omp-plumed-ocl-python3`  `2023-mpi-omp-plumed-python3` |
| `CCE-GPU-2.1.0` | `2022.3-mpi-omp-plumed-python3`  `2023-mpi-omp-plumed-ocl-python3`  `2023-mpi-omp-plumed-python3` |
| `CCE-GPU-3.0.0` | `2023_amd-mpi-omp-plumed-python3` |
| `CCE-GPU-3.1.0` | `2023_amd-omp-plumed-rocm-mpi-gpu` |
| `CCE-GPU-3.2.0` | `2023.5-omp-mpi-gpu` |
| `CPE-22.11-cce-15.0.0-softs` | `2021.4-mpi-omp-plumed-ocl-python3`  `2022.3-mpi-omp-plumed-python3` |
| `CPE-23.02-cce-15.0.1-GPU-softs` | `2022.3-mpi-omp-plumed-python3`  `2023-mpi-omp-plumed-ocl-python3` |
| `CPE-23.02-gcc-12.2.0-CPU-softs` | `2022.5-mpi-omp-plumed-python3` |
| `GCC-CPU-2.0.0` | `2022.5-mpi-omp-plumed-python3` |
| `GCC-CPU-2.1.0` | `2022.5-mpi-omp-plumed-python3` |
| `GCC-CPU-3.0.0` | `2023.3-mpi-omp-plumed-python3` |
| `GCC-CPU-3.1.0` | `2023.3-cp2k-omp-plumed-mpi`  `2023.3-omp-plumed-mpi` |
| gsl | `GCC-CPU-2.1.0` | `2.7` | The GNU Scientific Library (GSL) is a numerical library for C and C++ programmers. It is free software under the GNU General Public License. The library provides a wide range of mathematical routines such as random number generators, special functions and least-squares fitting. There are over 1000 functions in total with an extensive test suite. |
| `GCC-CPU-3.0.0` | `2.7.1` |
| hdf5 | `CCE-CPU-3.2.0` | `1.14.3-mpi` | HDF5 is a data model, library, and file format for storing and managing data. It supports an unlimited variety of datatypes, and is designed for flexible and efficient I/O and for high volume and complex data. |
| `CCE-GPU-3.2.0` | `1.14.3-mpi` |
| `GCC-CPU-3.2.0` | `1.14.3-mpi` |
| `GCC-GPU-3.2.0` | `1.14.3-mpi` |
| hipsycl | `CCE-GPU-2.0.0` | `0.9.4-mpi-python3` | hipSYCL is an implementation of the SYCL standard programming model over NVIDIA CUDA/AMD HIP |
| `CCE-GPU-2.1.0` | `0.9.4-mpi-python3` |
| hpctoolkit | `CPE-22.11-gcc-11.2.0-softs` | `2021.05.15-mpi-python3` | HPCToolkit is an integrated suite of tools for measurement and analysis of program performance on computers ranging from multicore desktop systems to the nation’s largest supercomputers. By using statistical sampling of timers and hardware performance counters, HPCToolkit collects accurate measurements of a program’s work, resource consumption, and inefficiency and attributes them to the full calling context in which they occur. |
| `CPE-23.02-gcc-12.2.0-CPU-softs` | `2023.03.01-mpi-python3` |
| `CPE-23.02-gcc-12.2.0-GPU-softs` | `2023.03.01-mpi-python3` |
| `GCC-CPU-2.0.0` | `2023.03.01-mpi-python3` |
| `GCC-CPU-2.1.0` | `2023.03.01-mpi-python3` |
| `GCC-CPU-3.0.0` | `2023.08.1-mpi-python3` |
| `GCC-CPU-3.1.0` | `2023.08.1-mpi` |
| `GCC-GPU-2.0.0` | `2023.03.01-mpi-python3` |
| `GCC-GPU-2.1.0` | `2023.03.01-mpi-python3` |
| `GCC-GPU-3.0.0` | `2023.08.1-mpi-python3` |
| `GCC-GPU-3.1.0` | `2023.08.1-mpi` |
| hypre | `CCE-CPU-2.1.0` | `2.27.0-mpi` | Hypre is a library of high performance preconditioners that features parallel multigrid methods for both structured and unstructured grid problems. |
| `CCE-CPU-3.2.0` | `2.31.0-mpi` |
| `CPE-22.11-cce-15.0.0-softs` | `2.25.0-mpi-omp` |
| `CPE-22.11-gcc-11.2.0-softs` | `2.25.0-mpi-omp` |
| `CPE-22.11-rocmcc-5.2.3-softs` | `2.25.0-mpi-omp` |
| `CPE-23.02-cce-15.0.1-GPU-softs` | `2.27.0-mpi-omp` |
| `CPE-23.02-gcc-12.2.0-GPU-softs` | `2.27.0-mpi-omp` |
| `CPE-23.02-rocmcc-5.3.0-GPU-softs` | `2.27.0-mpi-omp` |
| `GCC-CPU-2.1.0` | `2.27.0-mpi` |
| `GCC-CPU-3.0.0` | `2.29.0-mpi` |
| `GCC-CPU-3.2.0` | `2.31.0-mpi` |
| `GCC-GPU-2.0.0` | `2.27.0-mpi-omp` |
| `GCC-GPU-2.1.0` | `2.27.0-mpi-omp` |
| `GCC-GPU-3.0.0` | `2.29.0-mpi-omp` |
| `GCC-GPU-3.1.0` | `2.29.0-omp-rocm-mpi-gpu` |
| `GCC-GPU-3.2.0` | `2.31.0-omp-rocm-mpi-gpu` |
| kokkos | `CCE-GPU-2.0.0` | `3.7.01-gpu-omp` | Kokkos implements a programming model in C++ for writing performance portable applications targeting all major HPC platforms. |
| `CCE-GPU-2.1.0` | `3.7.01-gpu-omp` |
| `CCE-GPU-3.0.0` | `4.1.00-gpu-omp` |
| `CCE-GPU-3.1.0` | `4.1.00-omp-rocm-gpu` |
| `CCE-GPU-3.2.0` | `4.3.00-omp-rocm-gpu` |
| `CPE-22.11-cce-15.0.0-softs` | `3.6.01-gpu-omp` |
| `CPE-22.11-gcc-11.2.0-softs` | `3.6.01-gpu-omp` |
| `CPE-22.11-rocmcc-5.2.3-softs` | `3.6.01-gpu-omp` |
| `CPE-23.02-cce-15.0.1-GPU-softs` | `3.7.01-gpu-omp` |
| `CPE-23.02-gcc-12.2.0-GPU-softs` | `3.7.01-gpu-omp` |
| `CPE-23.02-rocmcc-5.3.0-GPU-softs` | `3.7.01-gpu-omp` |
| `GCC-GPU-2.0.0` | `3.7.01-gpu-omp` |
| `GCC-GPU-2.1.0` | `3.7.01-gpu-omp` |
| `GCC-GPU-3.0.0` | `4.1.00-gpu-omp` |
| `GCC-GPU-3.1.0` | `4.1.00-omp-rocm-gpu` |
| `GCC-GPU-3.2.0` | `4.3.00-omp-rocm-gpu` |
| lammps | `CCE-CPU-2.0.0` | `20220623.3-mpi-omp-plumed-python3` | LAMMPS stands for Large-scale Atomic/Molecular Massively Parallel Simulator. |
| `CCE-CPU-2.1.0` | `20230802-mpi-omp-plumed-python3` |
| `CCE-CPU-3.0.0` | `20230802-mpi-omp-plumed-python3` |
| `CCE-CPU-3.1.0` | `20231121-omp-plumed-kokkos-mpi`  `20240207.1-omp-plumed-kokkos-mpi` |
| `CCE-GPU-3.1.0` | `20230802-plumed-rocm-kokkos-mpi-gpu`  `20240207.1-plumed-rocm-kokkos-mpi-gpu` |
| `CPE-22.11-rocmcc-5.2.3-softs` | `develop-mpi-omp-plumed-python3` |
| `CPE-23.02-cce-15.0.1-CPU-softs` | `develop-mpi-omp-plumed-python3` |
| `GCC-CPU-3.1.0` | `20231121-omp-plumed-kokkos-mpi` |
| `GCC-GPU-3.1.0` | `20230802-plumed-rocm-kokkos-mpi-gpu` |
| libint | `CCE-CPU-2.0.0` | `2.6.0-python3` | Libint is a high-performance library for computing Gaussian integrals in quantum mechanics. |
| `CCE-CPU-2.1.0` | `2.6.0-python3` |
| `CCE-CPU-3.0.0` | `2.6.0-python3` |
| `CCE-CPU-3.1.0` | `2.6.0` |
| `CPE-23.02-aocc-3.2.0-CPU-softs` | `2.6.0-python3` |
| `CPE-23.02-cce-15.0.1-CPU-softs` | `2.6.0-python3` |
| `CPE-23.02-gcc-12.2.0-CPU-softs` | `2.6.0-python3` |
| `GCC-CPU-2.0.0` | `2.6.0-python3` |
| `GCC-CPU-2.1.0` | `2.6.0-python3` |
| `GCC-CPU-3.0.0` | `2.6.0-python3` |
| `GCC-CPU-3.1.0` | `2.6.0` |
| libxc | `CCE-CPU-2.0.0` | `6.1.0` | Libxc is a library of exchange-correlation functionals for density-functional theory. |
| `CCE-CPU-2.1.0` | `6.1.0` |
| `CCE-CPU-3.0.0` | `6.2.2` |
| `CCE-CPU-3.1.0` | `6.2.2` |
| `CPE-23.02-aocc-3.2.0-CPU-softs` | `6.1.0` |
| `CPE-23.02-cce-15.0.1-CPU-softs` | `6.1.0` |
| `CPE-23.02-gcc-12.2.0-CPU-softs` | `6.1.0` |
| `GCC-CPU-2.0.0` | `6.1.0` |
| `GCC-CPU-2.1.0` | `6.1.0` |
| `GCC-CPU-3.0.0` | `6.2.2` |
| `GCC-CPU-3.1.0` | `6.2.2` |
| libxsmm | `CCE-CPU-2.0.0` | `1.17-python3` | Library for specialized dense and sparse matrix operations, and deep learning primitives. |
| `CCE-CPU-2.1.0` | `1.17-python3` |
| `CCE-CPU-3.0.0` | `1.17-python3` |
| `CPE-23.02-aocc-3.2.0-CPU-softs` | `1.17-python3` |
| `CPE-23.02-cce-15.0.1-CPU-softs` | `1.17-python3` |
| `CPE-23.02-gcc-12.2.0-CPU-softs` | `1.17-python3` |
| `GCC-CPU-2.0.0` | `1.17-python3` |
| `GCC-CPU-2.1.0` | `1.17-python3` |
| `GCC-CPU-3.0.0` | `1.17-python3` |
| magma | `CCE-GPU-2.0.0` | `2.7.0-gpu` | The MAGMA project aims to develop a dense linear algebra library similar to LAPACK but for heterogeneous/hybrid architectures, starting with current ‘Multicore+GPU’ systems. |
| `CCE-GPU-2.1.0` | `2.7.0-gpu` |
| `CCE-GPU-3.0.0` | `2.7.2-gpu` |
| `CCE-GPU-3.1.0` | `2.7.2-rocm-gpu` |
| `CCE-GPU-3.2.0` | `2.8.0-rocm-gpu` |
| `CPE-22.11-cce-15.0.0-softs` | `2.6.2-gpu` |
| `CPE-22.11-gcc-11.2.0-softs` | `2.6.2-gpu` |
| `CPE-22.11-rocmcc-5.2.3-softs` | `2.6.2-gpu` |
| `CPE-23.02-cce-15.0.1-GPU-softs` | `2.7.0-gpu` |
| `CPE-23.02-gcc-12.2.0-GPU-softs` | `2.7.0-gpu` |
| `CPE-23.02-rocmcc-5.3.0-GPU-softs` | `2.7.0-gpu` |
| `GCC-GPU-2.0.0` | `2.7.0-gpu` |
| `GCC-GPU-2.1.0` | `2.7.0-gpu` |
| `GCC-GPU-3.0.0` | `2.7.2-gpu` |
| `GCC-GPU-3.1.0` | `2.7.2-rocm-gpu` |
| `GCC-GPU-3.2.0` | `2.8.0-rocm-gpu` |
| metis | `CCE-CPU-2.0.0` | `5.1.0` | METIS is a set of serial programs for partitioning graphs, partitioning finite element meshes, and producing fill reducing orderings for sparse matrices. |
| `CCE-CPU-2.1.0` | `5.1.0-int64`  `5.1.0` |
| `CCE-CPU-3.0.0` | `5.1.0-int64`  `5.1.0` |
| `CCE-GPU-2.0.0` | `5.1.0` |
| `CCE-GPU-2.1.0` | `5.1.0` |
| `CCE-GPU-3.0.0` | `5.1.0` |
| `CPE-22.11-cce-15.0.0-softs` | `5.1.0` |
| `CPE-22.11-gcc-11.2.0-softs` | `5.1.0` |
| `CPE-23.02-aocc-3.2.0-CPU-softs` | `5.1.0` |
| `CPE-23.02-cce-15.0.1-CPU-softs` | `5.1.0` |
| `CPE-23.02-cce-15.0.1-GPU-softs` | `5.1.0` |
| `CPE-23.02-gcc-12.2.0-CPU-softs` | `5.1.0` |
| `CPE-23.02-gcc-12.2.0-GPU-softs` | `5.1.0` |
| `GCC-CPU-2.0.0` | `5.1.0` |
| `GCC-CPU-2.1.0` | `5.1.0` |
| `GCC-CPU-3.0.0` | `5.1.0` |
| `GCC-GPU-2.0.0` | `5.1.0` |
| `GCC-GPU-2.1.0` | `5.1.0` |
| `GCC-GPU-3.0.0` | `5.1.0` |
| mmg | `CCE-CPU-2.0.0` | `5.6.0-mpi-python3` | Mmg is an open source software for simplicial remeshing. It provides 3 applications and 4 libraries: - the mmg2d application and the libmmg2d library: adaptation and optimization of a two-dimensional triangulation and generation of a triangulation from a set of points or from given boundary edges - the mmgs application and the libmmgs library: adaptation and optimization of a surface triangulation and isovalue discretization - the mmg3d application and the libmmg3d library: adaptation and optimization of a tetrahedral mesh and implicit domain meshing - the libmmg library gathering the libmmg2d, libmmgs and libmmg3d libraries. |
| `CCE-CPU-2.1.0` | `5.6.0-mpi-python3` |
| `CCE-CPU-3.0.0` | `5.7.1-mpi-python3` |
| `CCE-GPU-2.0.0` | `5.6.0-mpi-python3` |
| `CCE-GPU-2.1.0` | `5.6.0-mpi-python3` |
| `CCE-GPU-3.0.0` | `5.7.1-mpi-python3` |
| `CPE-22.11-cce-15.0.0-softs` | `5.6.0-mpi-python3` |
| `CPE-22.11-gcc-11.2.0-softs` | `5.6.0-mpi-python3` |
| `CPE-23.02-aocc-3.2.0-CPU-softs` | `5.6.0-mpi-python3` |
| `CPE-23.02-cce-15.0.1-CPU-softs` | `5.6.0-mpi-python3` |
| `CPE-23.02-cce-15.0.1-GPU-softs` | `5.6.0-mpi-python3` |
| `CPE-23.02-gcc-12.2.0-CPU-softs` | `5.6.0-mpi-python3` |
| `CPE-23.02-gcc-12.2.0-GPU-softs` | `5.6.0-mpi-python3` |
| `GCC-CPU-2.0.0` | `5.6.0-mpi-python3` |
| `GCC-CPU-2.1.0` | `5.6.0-mpi-python3` |
| `GCC-CPU-3.0.0` | `5.7.1-mpi-python3` |
| `GCC-GPU-2.0.0` | `5.6.0-mpi-python3` |
| `GCC-GPU-2.1.0` | `5.6.0-mpi-python3` |
| `GCC-GPU-3.0.0` | `5.7.1-mpi-python3` |
| mpifileutils | `CCE-GPU-2.0.0` | `0.11.1-mpi` | mpiFileUtils is a suite of MPI-based tools to manage large datasets, which may vary from large directory trees to large files. High-performance computing users often generate large datasets with parallel applications that run with many processes (millions in some cases). However those users are then stuck with single-process tools like cp and rm to manage their datasets. This suite provides MPI-based tools to handle typical jobs like copy, remove, and compare for such datasets, providing speedups of up to 20-30x. |
| `CCE-GPU-2.1.0` | `0.11.1-mpi` |
| `CCE-GPU-3.0.0` | `0.11.1-mpi` |
| `CPE-23.02-cce-15.0.1-GPU-softs` | `0.11.1-mpi` |
| mumps | `GCC-CPU-3.1.0` | `5.5.1-int64-omp-mpi` | MUMPS: a MUltifrontal Massively Parallel sparse direct Solver |
| `GCC-CPU-3.2.0` | `5.6.2-int64-omp-mpi` |
| `GCC-GPU-3.1.0` | `5.5.1-int64-omp-mpi` |
| `GCC-GPU-3.2.0` | `5.6.2-int64-omp-mpi` |
| namd | `CPE-22.11-gcc-11.2.0-softs` | `3.0a9-mpi` | NAMD is a parallel molecular dynamics code designed for high-performance simulation of large biomolecular systems. |
| `CPE-23.02-gcc-12.2.0-CPU-softs` | `3.0a9-mpi` |
| `CPE-23.02-gcc-12.2.0-GPU-softs` | `3.0a9-mpi` |
| `GCC-CPU-2.0.0` | `3.0a9-mpi` |
| `GCC-CPU-2.1.0` | `3.0a9-mpi` |
| `GCC-CPU-3.0.0` | `3.0a13-mpi`  `3.0b5-mpi` |
| `GCC-CPU-3.1.0` | `3.0a13-mpi`  `3.0b5-mpi` |
| `GCC-GPU-3.0.0` | `3.0a9-mpi` |
| `GCC-GPU-3.1.0` | `3.0a9-rocm-mpi-gpu`  `3.0b5` |
| `GCC-GPU-3.2.0` | `3.0` |
| netcdf-c | `CCE-CPU-3.2.0` | `4.9.2-mpi` | NetCDF (network Common Data Form) is a set of software libraries and machine-independent data formats that support the creation, access, and sharing of array-oriented scientific data. This is the C distribution. |
| `CCE-GPU-3.2.0` | `4.9.2-mpi` |
| `GCC-CPU-3.2.0` | `4.9.2-mpi` |
| `GCC-GPU-3.2.0` | `4.9.2-mpi` |
| netcdf-cxx | `CCE-CPU-3.2.0` | `4.2-mpi` | Deprecated C++ compatibility bindings for NetCDF. These do NOT read or write NetCDF-4 files, and are no longer maintained by Unidata. Developers should migrate to current NetCDF C++ bindings, in Spack package netcdf-cxx4. |
| `CCE-GPU-3.2.0` | `4.2-mpi` |
| `GCC-CPU-3.2.0` | `4.2-mpi` |
| `GCC-GPU-3.2.0` | `4.2-mpi` |
| netcdf-cxx4 | `CCE-CPU-3.2.0` | `4.3.1-mpi` | NetCDF (network Common Data Form) is a set of software libraries and machine-independent data formats that support the creation, access, and sharing of array-oriented scientific data. This is the C++ distribution. |
| `CCE-GPU-3.2.0` | `4.3.1-mpi` |
| `GCC-CPU-3.2.0` | `4.3.1-mpi` |
| `GCC-GPU-3.2.0` | `4.3.1-mpi` |
| netcdf-fortran | `CCE-CPU-3.2.0` | `4.6.1-mpi` | NetCDF (network Common Data Form) is a set of software libraries and machine-independent data formats that support the creation, access, and sharing of array-oriented scientific data. This is the Fortran distribution. |
| `CCE-GPU-3.2.0` | `4.6.1-mpi` |
| `GCC-CPU-3.2.0` | `4.6.1-mpi` |
| `GCC-GPU-3.2.0` | `4.6.1-mpi` |
| nwchem | `CPE-23.02-gcc-12.2.0-CPU-softs` | `7.0.2-mpi-omp-python3` | High-performance computational chemistry software |
| octave | `GCC-CPU-3.1.0` | `8.2.0-mpi` | GNU Octave is a high-level language, primarily intended for numerical computations. |
| octopus | `GCC-CPU-3.1.0` | `13.0-mpi` | A real-space finite-difference (time-dependent) density-functional theory code. |
| `GCC-CPU-3.2.0` | `14.1-elpa-mpi` |
| openblas | `CCE-CPU-3.1.0` | `0.3.24-omp` | OpenBLAS: An optimized BLAS library |
| `CCE-CPU-3.2.0` | `0.3.26-omp` |
| `GCC-CPU-3.1.0` | `0.3.24-omp` |
| `GCC-CPU-3.2.0` | `0.3.26-omp` |
| openfoam | `GCC-CPU-3.0.0` | `2306-mpi-int64` | OpenFOAM is a GPL-opensource C++ CFD-toolbox. This offering is supported by OpenCFD Ltd, producer and distributor of the OpenFOAM software via www.openfoam.com, and owner of the OPENFOAM trademark. OpenCFD Ltd has been developing and releasing OpenFOAM since its debut in 2004. |
| `GCC-CPU-3.1.0` | `2306-int64-mpi` |
| `GCC-CPU-3.2.0` | `2312-int64-mpi` |
| parallel-netcdf | `CCE-CPU-3.2.0` | `1.12.3-mpi` | PnetCDF (Parallel netCDF) is a high-performance parallel I/O library for accessing files in format compatibility with Unidata’s NetCDF, specifically the formats of CDF-1, 2, and 5. |
| `CCE-GPU-3.2.0` | `1.12.3-mpi` |
| `GCC-CPU-3.2.0` | `1.12.3-mpi` |
| `GCC-GPU-3.2.0` | `1.12.3-mpi` |
| paraview | `CPE-22.11-gcc-11.2.0-softs` | `5.11.0-mpi-python3` | ParaView is an open-source, multi-platform data analysis and visualization application. This package includes the Catalyst in-situ library for versions 5.7 and greater, otherwise use the catalyst package. |
| parmetis | `CCE-CPU-2.0.0` | `4.0.3-mpi` | ParMETIS is an MPI-based parallel library that implements a variety of algorithms for partitioning unstructured graphs, meshes, and for computing fill-reducing orderings of sparse matrices. |
| `CCE-CPU-2.1.0` | `4.0.3-mpi` |
| `CCE-CPU-3.0.0` | `4.0.3-mpi-python3` |
| `CCE-CPU-3.1.0` | `4.0.3-mpi` |
| `CPE-23.02-aocc-3.2.0-CPU-softs` | `4.0.3-mpi` |
| `GCC-CPU-2.1.0` | `4.0.3-mpi` |
| `GCC-CPU-3.0.0` | `4.0.3-mpi-python3` |
| `GCC-CPU-3.1.0` | `4.0.3-mpi` |
| petsc | `CCE-CPU-2.0.0` | `3.18.3-mpi-python3` | PETSc is a suite of data structures and routines for the scalable (parallel) solution of scientific applications modeled by partial differential equations. |
| `CCE-CPU-2.1.0` | `3.18.3-mpi-python3` |
| `CCE-CPU-3.1.0` | `3.20.1-omp-kokkos-mpi` |
| `CCE-CPU-3.2.0` | `3.21.1-omp-kokkos-mpi` |
| `CPE-22.11-cce-15.0.0-softs` | `3.18.1-mpi-python3` |
| `CPE-23.02-cce-15.0.1-CPU-softs` | `3.18.3-mpi-python3` |
| `GCC-CPU-2.1.0` | `3.18.3-mpi-python3` |
| `GCC-CPU-3.0.0` | `3.20.1-mpi-python3` |
| `GCC-CPU-3.1.0` | `3.20.1-omp-mpi` |
| `GCC-CPU-3.2.0` | `3.21.1-omp-mpi` |
| `GCC-GPU-2.1.0` | `3.18.3-mpi-int64-python3` |
| `GCC-GPU-3.0.0` | `3.20.1-mpi-int64-python3` |
| `GCC-GPU-3.1.0` | `3.20.1-int64-rocm-mpi-gpu` |
| `GCC-GPU-3.2.0` | `3.21.1-rocm-mpi-gpu` |
| plumed | `CCE-CPU-2.0.0` | `2.8.2-mpi-python3` | PLUMED is an open source library for free energy calculations in molecular systems which works together with some of the most popular molecular dynamics engines. |
| `CCE-CPU-2.1.0` | `2.8.2-mpi-python3` |
| `CCE-CPU-3.0.0` | `2.9.0-mpi-python3` |
| `CCE-CPU-3.1.0` | `2.9.0-mpi` |
| `CCE-CPU-3.2.0` | `2.9.0-mpi` |
| `CCE-GPU-3.2.0` | `2.9.0-mpi` |
| `CPE-23.02-aocc-3.2.0-CPU-softs` | `2.8.2-mpi-python3` |
| `CPE-23.02-cce-15.0.1-CPU-softs` | `2.8.2-mpi-python3` |
| `GCC-CPU-2.0.0` | `2.9.0-mpi-python3` |
| `GCC-CPU-2.1.0` | `2.9.0-mpi-python3` |
| `GCC-CPU-3.1.0` | `2.9.0-mpi` |
| `GCC-CPU-3.2.0` | `2.9.0-mpi` |
| `GCC-GPU-3.2.0` | `2.9.0-mpi` |
| quantum-espresso | `GCC-CPU-3.1.0` | `7.3-elpa-omp-mpi` | Quantum ESPRESSO is an integrated suite of Open-Source computer codes for electronic-structure calculations and materials modeling at the nanoscale. It is based on density-functional theory, plane waves, and pseudopotentials. |
| `GCC-CPU-3.2.0` | `6.8-omp-mpi` |
| rust | `CPE-22.11-gcc-11.2.0-softs` | `1.60.0-python3` | The Rust programming language toolchain |
| scotch | `CCE-CPU-2.1.0` | `7.0.1-mpi` | Scotch is a software package for graph and mesh/hypergraph partitioning, graph clustering, and sparse matrix ordering. |
| `CCE-CPU-3.0.0` | `7.0.4-mpi` |
| `CCE-CPU-3.1.0` | `7.0.4-mpi` |
| `CPE-23.02-cce-15.0.1-CPU-softs` | `7.0.1-mpi` |
| `CPE-23.02-gcc-12.2.0-CPU-softs` | `7.0.1-mpi` |
| `GCC-CPU-2.0.0` | `7.0.1-mpi` |
| `GCC-CPU-2.1.0` | `7.0.1-mpi` |
| `GCC-CPU-3.0.0` | `7.0.4-mpi` |
| `GCC-CPU-3.1.0` | `7.0.4-mpi` |
| siesta | `CPE-23.02-gcc-12.2.0-CPU-softs` | `4.0.2-mpi` | SIESTA performs electronic structure calculations and ab initio molecular dynamics simulations of molecules and solids. |
| `GCC-CPU-2.0.0` | `4.0.2-mpi` |
| `GCC-CPU-2.1.0` | `4.0.2-mpi` |
| `GCC-CPU-3.0.0` | `4.0.2-mpi` |
| `GCC-CPU-3.1.0` | `4.0.2-mpi` |
| `GCC-CPU-3.2.0` | `4.1.5-elpa-omp-mpi`  `5.0.1-elpa-omp-mpi`  `5.0.1-elpa-omp-mpi` |
| slepc | `CCE-CPU-2.0.0` | `3.18.2-mpi-python3` | Scalable Library for Eigenvalue Problem Computations. |
| `CCE-CPU-2.1.0` | `3.18.2-mpi-python3` |
| `CCE-CPU-3.0.0` | `3.20.0-mpi-python3` |
| `CCE-CPU-3.1.0` | `3.20.0-mpi` |
| `CCE-CPU-3.2.0` | `3.21.0-mpi` |
| `CCE-GPU-3.2.0` | `3.21.0-rocm-mpi-gpu` |
| `CPE-23.02-cce-15.0.1-CPU-softs` | `3.18.2-mpi-python3` |
| `GCC-CPU-3.1.0` | `3.20.0-mpi` |
| `GCC-CPU-3.2.0` | `3.21.0-mpi` |
| `GCC-GPU-3.1.0` | `3.20.0-rocm-mpi-gpu` |
| `GCC-GPU-3.2.0` | `3.21.0-rocm-mpi-gpu` |
| spack | `CPE-22.11-gcc-11.2.0-softs` | `0.18.1-python3` | Spack is a multi-platform package manager that builds and installs multiple versions and configurations of software. It works on Linux, macOS, and many supercomputers. Spack is non-destructive: installing a new version of a package does not break existing installations, so many configurations of the same package can coexist. |
| `CPE-23.02-gcc-12.2.0-CPU-softs` | `0.20.0-python3` |
| `CPE-23.02-gcc-12.2.0-GPU-softs` | `0.20.0-python3` |
| `GCC-CPU-2.0.0` | `0.20.0-python3` |
| `GCC-CPU-2.1.0` | `0.20.0-python3` |
| `GCC-CPU-3.0.0` | `0.20.0-python3` |
| `GCC-GPU-2.0.0` | `0.20.0-python3` |
| `GCC-GPU-2.1.0` | `0.20.0-python3` |
| `user-CPU-2.0.0` | `0.20.0-python3` |
| `user-CPU-2.1.0` | `0.20.0-python3` |
| `user-CPU-3.0.0` | `0.20.0-python3` |
| `user-GPU-2.0.0` | `0.20.0-python3` |
| `user-GPU-2.1.0` | `0.20.0-python3` |
| `user-GPU-3.0.0` | `0.20.0-python3` |
| sundials | `CCE-CPU-3.1.0` | `6.6.1-mpi` | SUNDIALS (SUite of Nonlinear and DIfferential/ALgebraic equation Solvers) |
| `CCE-CPU-3.2.0` | `7.0.0-mpi` |
| `CPE-23.02-gcc-12.2.0-CPU-softs` | `6.5.0-mpi-python3` |
| `GCC-CPU-2.0.0` | `6.5.0-mpi-python3` |
| `GCC-CPU-2.1.0` | `6.5.0-mpi-python3` |
| `GCC-CPU-3.0.0` | `6.6.1-mpi-python3` |
| `GCC-CPU-3.1.0` | `6.6.1-mpi` |
| `GCC-CPU-3.2.0` | `7.0.0-mpi` |
| superlu-dist | `CCE-CPU-3.1.0` | `8.1.2-int64-omp-mpi` | A general purpose library for the direct solution of large, sparse, nonsymmetric systems of linear equations on high performance machines. |
| `CCE-CPU-3.2.0` | `8.2.1-int64-omp-mpi` |
| `CCE-GPU-3.1.0` | `8.1.2-int64-omp-rocm-mpi-gpu` |
| `CCE-GPU-3.2.0` | `8.2.1-int64-omp-rocm-mpi-gpu` |
| `GCC-CPU-3.1.0` | `8.1.2-int64-omp-mpi` |
| `GCC-CPU-3.2.0` | `8.2.1-int64-omp-mpi` |
| `GCC-GPU-3.1.0` | `8.1.2-int64-omp-rocm-mpi-gpu` |
| `GCC-GPU-3.2.0` | `8.2.1-int64-omp-rocm-mpi-gpu` |
| swig | `CCE-CPU-3.1.0` | `4.1.1-fortran` | SWIG is an interface compiler that connects programs written in C and C++ with scripting languages such as Perl, Python, Ruby, and Tcl. It works by taking the declarations found in C/C++ header files and using them to generate the wrapper code that scripting languages need to access the underlying C/C++ code. In addition, SWIG provides a variety of customization features that let you tailor the wrapping process to suit your application. |
| `GCC-CPU-3.1.0` | `4.1.1-fortran` |
