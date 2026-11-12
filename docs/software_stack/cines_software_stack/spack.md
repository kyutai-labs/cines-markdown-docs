<!-- Source: https://dci.dci-gitlab.cines.fr/webextranet/software_stack/cines_software_stack/spack.html -->
<!-- Title: CINES’ Spack software stack -->

<a id="cines-spack-software-stack"></a>

<a id="adastra-software-stack-cines-software-stack-spack"></a>

# CINES’ Spack software stack

<a id="introduction"></a>

<a id="adastra-software-stack-cines-software-stack-spack-introduction"></a>

## Introduction

Before going into more technical subjects, know that CINES uses [Spack](https://spack.io/) to provide precompiled softwares which we shall name Spack products. We recommend that you first search for an already CINES provided software before trying to install it yourself. To look for such preinstalled software, search the modules using `module spider` or browse the [catalog](spack_products_catalog.md#adastra-software-stack-spack-product-catalog).

<a id="a-note-on-dependencies"></a>

### A note on dependencies

Spack tries to solve the **problem** of satisfying the somewhat esoteric and hpc specific dependencies and does a reasonably good job at it. It is good enough that it is considered viable and used by many sites. That said, note that dependencies are a **problem** and that even if Spack mitigates this to a certain extent, the resolution of a dependency is still a **problem**. You should probably not add new dependencies lightly. To that, we should add:

- Are all your dependencies built and tested in CI on all target platform ? Probably not, so you should be even more careful with dependencies?
- It is almost always costlier to fix something, than to start from scratch.

<a id="basic-tools-and-libraries"></a>

<a id="adastra-software-stack-cines-software-stack-spack-basic"></a>

## Basic tools and libraries

CINES offers a basic software suite primarily deployed using the Spack package manager and GCC toolchain. This suite includes commonly used tools and libraries with no MPI dependencies (with a few exceptions), ensuring there are no risks of ABI (Application Binary Interface) incompatibilities or symbol conflicts during linking.

You can safely use these modules without risk of conflicts with other modules, either to link your applications with the available libraries or to use the underlying tools.

Running `module available` could give you:

```
--------------------------------------------------------- /opt/software/gaia/prod/latest/Base ---------------------------------------------------------
    anaconda3/2023.09-0    ferret/7.6.0-mpi    hpctoolkit/2025.0.stable-mpi       libxml2/2.13.4             nsimd/3.0.1                     r/4.4.0
    aocc/5.0.0             ffmpeg/6.1.1        hpcviewer/2024.02                  libxsmm/1.17               openblas/0.3.28                 rclone/1.68.1
    binutils/2.43.1        gdal/3.8.5          hwloc/2.9.1-rocm-gpu               likwid/5.4.1-cuda          opencl-icd-loader/2024.05.08    rust/1.78.0
    blitz/1.0.2            gdb/16.2            hwloc/2.9.1                        llvm/20.1.6                openjdk/17.0.11_9               sox/14.4.2
    bzip2/1.0.8            git/2.48.1          imagemagick/7.1.1-29               metis/5.1.0-int64          papi/7.1.0                      suite-sparse/7.8.3
    cfitsio/4.3.0          glew/2.2.0          intel-oneapi-compilers/2025.2.0    metis/5.1.0                paraview/5.13.0-osmesa          swig/4.1.1
    chapel/2.5.0           gmake/4.4.1         intel-oneapi-mkl/2025.2.0          mmg/5.7.1                  paraview/5.13.0                 udunits/2.2.28
    cmake/4.0.3            gmp/6.2.1           jasper/3.0.3                       mpfr/4.2.1                 patchelf/0.17.2                 valgrind/3.23.0-mpi
    ddt/25.0.1             gmsh/4.13.1-mpi     jdk/21.0.8                         mpifileutils/0.11.1-mpi    poppler/23.04.0                 visit/3.4.2
    doxygen/1.13.2         gnuplot/6.0.0       julia/1.10.0                       nco/5.1.9-omp-mpi          proj/9.4.1                      xpmem/2.6.5-36
    easybuild/4.7.0        grace/5.1.25-mpi    libsndfile/1.2.2                   ncview/2.1.9-mpi           python/3.12.1                   zlib-ng/2.1.4
    eigen/3.4.0            gsl/2.7.1           libtirpc/1.3.3                     ninja/1.12.1               qt/5.15.11                      zlib/1.3.1
```

<a id="extensible-software-stacks"></a>

<a id="adastra-software-stack-cines-software-stack-spack-extensible"></a>

## Extensible software stacks

CINES offers extensible software stacks in the form of modules named according to the format `<compiler>-[GPU|CPU]-<version>`. Each extensible software stack groups together a set of software packages targeting a specific architecture and built using a **specific toolchain**. CINES will provide software stacks adapted to each Adastra hardware partition. Each software stack version is based on a specific version of the Cray programming environment (`cpe/XX.YY`).

The `<compiler>-[GPU|CPU]-<version>` modules can be considered as architecture- and compiler-specific environments. The `<version>` number represents the production version of the software stack. CINES will endeavor to respect [semantic versioning concepts](https://semver.org/).

| Adastra partition | Extensible software stacks | Toolchain used |
| --- | --- | --- |
| `MI250` (GPU) | `CCE-GPU-<version>` | CCE |
| `GCC-GPU-<version>` | GCC |
| `GENOA` (CPU) | `CCE-CPU-<version>` | CCE |
| `GCC-CPU-<version>` | GCC |
| `HPDA` (GPU, visualization) | **TBD** | **TBD** |

In addition to these extensible software stacks mapped to the partitions of Adastra, we provide what we call Spack **user** or Spack pre-configured environment (PreConf). It enables the user to install their own softwares by **reusing** the CINES’ Spack configuration and binary cache. Spack PreConf provides Spack support for a given partition and a set of compiler. The syntax is: `spack-user-<version>`. More information on how you can reuse the CINES’ Spack configuration is given in the [Spack-user : Using pre-configured Spack installation on Adastra](../spack_user/index.md#adastra-software-stack-spack-user) section.

Running `module available` could give you:

```
--------------------------------- /opt/software/gaia/prod/latest/Core ---------------------------------
   CCE-CPU-5.0.0    CCE-GPU-5.0.0    GCC-CPU-5.0.0    GCC-GPU-5.0.0    develop    spack-user-5.0.0
```

The `develop` extensible module exposes the software stacks being currently developed (release candidate). Running `module load develop` and then `module av` could give you:

```
--------------------------------- /opt/software/gaia/dev/latest/Core ----------------------------------
    CCE-CPU-develop    CCE-GPU-develop    GCC-CPU-develop    GCC-GPU-develop    spack-user-develop
```

**Warning**

This category includes software versions under development and testing before their deployment in production. Use at your own risk. Package stability is not guaranteed, and packages may be removed or modified when redeploying develop packages/modules.

A production release will take place every 3 to 6 months. Each such release may introduce new versions for the components of the stack (say a CCE or GCC version bump). As the machine evolves, more extensible software stacks (based on a CrayPE release) and their respective products will be added, some will be deprecated. We do not guarantee an extensible software stacks will be produced for each CrayPE release. CINES is likely to release a new extensible software stacks at the start of each DARI call. We guarantee that the CINES’ software stack will be available for at least **2** CrayPE releases before being removed from the system. This should give the user something like 9 months to 1 year of support per release (**at least**).

When the software stack is put into production, the old modules are moved to a space called `deprecated` and are still available, as shown below using `module available`:

```
------------------------------------ /opt/software/gaia/deprecated ------------------------------------
   CCE-CPU-4.0.0    CCE-GPU-4.0.0    GCC-CPU-4.0.0    GCC-GPU-4.0.0    archive
```

Finally, deprecated modules are moved to the `.archive` directory and become available only after the `module load archive` command is executed. These archives are kept for a long time, our only support limit would be the operating system itself not being able to run the binary. In this case, ask [svp@cines.fr](mailto:svp%40cines.fr) for a reinstallation of the product old product version.

<a id="using-the-cines-software-stack"></a>

<a id="adastra-software-stack-cines-software-stack-spack-using"></a>

## Using the CINES software stack

To see the softwares made available by an environment, you can simply load the extensible module corresponding to an environment. That said the recommended way is the following; supposing you want to use the [GROMACS](https://www.gromacs.org/) software, you would do:

```shell-session
$ module spider gromacs
----------------------------------------------------------------------------
gromacs:
----------------------------------------------------------------------------
    Versions:
        gromacs/2021.4-mpi-omp-plumed-ocl-python3
        gromacs/2022.3-mpi-omp-plumed-python3
        gromacs/2022.5-mpi-omp-plumed-python3
        gromacs/2023-mpi-omp-plumed-ocl-python3
        gromacs/2023.3-cp2k-omp-plumed-mpi
        gromacs/2023.3-mpi-omp-plumed-python3
        gromacs/2024.3-cp2k-omp-mpi
```

Here, `module` shows multiple GROMACS versions (2021.4, 2022.3, 2022.5, 2023, …) but with different variants for the 2023 version. Lets use `gromacs/2023-mpi-omp-plumed-ocl-python3`. To find which programming environment provides the software package we do:

```shell-session
$ module spider gromacs/2023-mpi-omp-plumed-ocl-python3
----------------------------------------------------------------------------
gromacs: gromacs/2023-mpi-omp-plumed-ocl-python3
----------------------------------------------------------------------------

    You will need to load all module(s) on any one of the lines below before the "gromacs/2023-mpi-omp-plumed-ocl-python3" module is available to load.

    CCE-GPU-2.0.0
    CPE-23.02-cce-15.0.1-GPU-softs
```

This tells us that `gromacs/2023-mpi-omp-plumed-ocl-python3` is available, under the `CCE-GPU-2.0.0` and `CPE-23.02-cce-15.0.1-GPU-softs` extensible module. Latest stable version of the extensible module/environment (i.e. production) should be preferably used.

In your scripts, the procedure above reduces to the following commands:

```shell-session
$ module purge
$ module load CCE-GPU-2.0.0
$ module load gromacs/2023-mpi-omp-plumed-ocl-python3
```

<a id="advanced-module-mixing"></a>

<a id="adastra-software-stack-cines-software-stack-spack-using-advanced-module-mixing"></a>

## Advanced module mixing

As an example, let’s suppose you’ve located (using the `module spider`) a library from the CINES software stack. Let’s assume that this library has been built in an environment (extensible module of the form `<compiler>-[GPU|CPU]-<version>`) using the Cray compiler, but you want to use the GCC toolchain (`PrgEnv-gnu`). Conventional wisdom says you **shouldn’t mix the two**.

In practice, **if** the interfaces are properly defined, as it is in the library used in this example, and **if** the library does not have toolchain dependencies such as an OpenMP runtime (which you absolutely do not want to mix), then you should be able to have interoperability of the library across toolchains.

**Note**

Check the dependencies on shared libraries using `readelf -d` or `ldd`. It is trickier on static libraries.
