<!-- Source: https://dci.dci-gitlab.cines.fr/webextranet/software_stack/simulation_software/index.html -->
<!-- Title: Simulation software scripts and tips -->

<a id="simulation-software-scripts-and-tips"></a>

<a id="adastra-software-stack-simulation-software-script-and-tips"></a>

# Simulation software scripts and tips

**Warning**

Please understand that we do not whish to provide general documentation on how to use a given tool (say generic GROMACS concepts). That is left to the developer of the tools and we’ll try not redo what already exists. That said, we wish to detail our machine’ specificities and what choice of option one should select to best exploit the hardware.

<a id="cines-software-stack"></a>

## CINES software stack

<a id="amber"></a>

### Amber

<a id="gpu"></a>

#### GPU

Molecular dynamics jobs are ran the fastest using `pmemd.hip` (which is **single GPU**). At the moment, Amber is found not to scale well on Adastra. That said we obtain competitive performance on 1 GPU which is what we recommend.

```shell
#!/bin/bash
#SBATCH --account=<account_to_charge>
#SBATCH --job-name="<job_name>"
#SBATCH --constraint=MI250
#SBATCH --nodes=1
# #SBATCH --exclusive # Shared !
#SBATCH --gpus-per-node=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --threads-per-core=1
#SBATCH --time=1:00:00

module purge

module load archive
module load GCC-GPU-2.1.0
module load amber

module list

NUM_THREADS=1
# Not meaningful on non MPI (pmemd.hip vs pmemd.hip.mpi) jobs but required on
# multi-process ones!
# export MPICH_GPU_SUPPORT_ENABLED=1
srun --ntasks-per-node=1 --cpus-per-task="${NUM_THREADS}" --threads-per-core=1 --gpus-per-task=1 --gpu-bind=closest --label \
    -- pmemd.hip -O -i <input.0> -o mdout -p <input.1> -c <input.2>
```

A performance comparison of Amber on GPUs is shown below. It was established in october 2023 using Amber 22. We observe competitive performance to same generation GPUs (H100).

[![../../_images/benchmark_amber.png](https://dci.dci-gitlab.cines.fr/webextranet/_images/benchmark_amber.png)](https://dci.dci-gitlab.cines.fr/webextranet/_images/benchmark_amber.png)

<a id="cp2k"></a>

### CP2K

<a id="id1"></a>

#### GPU

```shell
#!/bin/bash
#SBATCH --account=<account_to_charge>
#SBATCH --job-name="<job_name>"
#SBATCH --constraint=MI250
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=1:00:00

module purge

module load archive
module load GCC-GPU-2.1.0
module load cp2k/2023.1-mpi-elpa-omp-plumed-scalapack-python3

module list

# export OMP_DISPLAY_AFFINITY=TRUE

export OMP_NUM_THREADS=8
srun --ntasks-per-node=8 --cpus-per-task="${OMP_NUM_THREADS}" --threads-per-core=1 --gpus-per-task=1 --gpu-bind=closest --label \
    -- cp2k.psmp <case.inp>
```

<a id="cpu"></a>

#### CPU

```shell
#!/bin/bash
#SBATCH --account=<account_to_charge>
#SBATCH --job-name="<job_name>"
#SBATCH --constraint=GENOA
#SBATCH --nodes=2
#SBATCH --exclusive
#SBATCH --time=1:00:00

module purge

module load archive
module load GCC-CPU-2.1.0
module load cp2k

module list

# export OMP_DISPLAY_AFFINITY=TRUE
export OMP_PROC_BIND=CLOSE
export OMP_PLACES=THREADS

export OMP_NUM_THREADS=4
srun --ntasks-per-node=48 --cpus-per-task="${OMP_NUM_THREADS}" --threads-per-core=1 --label \
    -- cp2k.psmp <case.inp>
```

<a id="dftb"></a>

### DFTB+

<a id="id2"></a>

#### CPU

```shell
#!/bin/bash
#SBATCH --account=<account_to_charge>
#SBATCH --job-name="<job_name>"
#SBATCH --constraint=GENOA
#SBATCH --nodes=1
# #SBATCH --exclusive # Shared, it DOES NOT SCALE past one core !
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --threads-per-core=1
#SBATCH --time=1:00:00

module purge

module load archive
module load CCE-CPU-2.1.0
module load dftbplus

module list

# export OMP_DISPLAY_AFFINITY=TRUE
export OMP_PROC_BIND=CLOSE
export OMP_PLACES=THREADS

export OMP_NUM_THREADS=1
srun --ntasks-per-node=1 --cpus-per-task="${OMP_NUM_THREADS}" --threads-per-core=1 --label \
    -- dftb+
```

<a id="gromacs"></a>

### GROMACS

**Note**

You may find [this website](https://mdbench.ace-net.ca/mdbench/) interesting to select the software and SLURM options.

**Warning**

Different versions may have significant differences in simulation methods and default parameters. Reproducing results of older versions with a newer version may not be straightforward.

**Note**

If you have used a combination of GROMACS options that work best for a specific use case, please let us know so we can collectively benefit from your work.

External documentation can be found on the official documentation <https://manual.gromacs.org/documentation/> and this document <https://docs.alliancecan.ca/wiki/GROMACS>t__ is good a explaining the inefficiencies of GROMACS.

<a id="id3"></a>

#### GPU

**Warning**

GROMACS and other MD software are [known not to scale well a single molecule](https://docs.alliancecan.ca/wiki/GROMACS#Notes_on_running_GROMACS_on_GPUs) on multi GPUs. If you want to scale, you should prefer replicas.

```shell
#!/bin/bash
#SBATCH --account=<account_to_charge>
#SBATCH --job-name="<job_name>"
#SBATCH --constraint=MI250
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=1:00:00

module purge

module load CCE-GPU-3.0.0
module load gromacs/2023_amd-mpi-omp-plumed-python3

module list

# export OMP_DISPLAY_AFFINITY=TRUE
export OMP_PROC_BIND=CLOSE
export OMP_PLACES=THREADS

export OMP_NUM_THREADS=8
# Depending on your case, you may want to activate or deactivate the
# variables below:
# export GMX_ENABLE_DIRECT_GPU_COMM=1
# export GMX_FORCE_GPU_AWARE_MPI=1
# export MPICH_GPU_SUPPORT_ENABLED=1
srun --ntasks-per-node=8 --cpus-per-task="${OMP_NUM_THREADS}" --threads-per-core=1 --gpus-per-task=1 --gpu-bind=closest --label \
    -- gmx_mpi mdrun \
    -s <case.tpr> \
    -nsteps 1000 \
    -pin off \
    -nb gpu \
    -npme 1 \
    -pme gpu \
    -bonded gpu \
    -update auto
```

<a id="id4"></a>

#### CPU

```shell
#!/bin/bash
#SBATCH --account=<account_to_charge>
#SBATCH --job-name="<job_name>"
#SBATCH --constraint=GENOA
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=1:00:00

module purge

module load archive
module load CCE-CPU-2.1.0
module load gromacs

module list

# export OMP_DISPLAY_AFFINITY=TRUE
export OMP_PROC_BIND=CLOSE
export OMP_PLACES=THREADS

export OMP_NUM_THREADS=2
srun --ntasks-per-node=96 --cpus-per-task="${OMP_NUM_THREADS}" --threads-per-core=1 --label \
    -- gmx_mpi mdrun \
    -s <case.tpr> \
    -plumed <plume_configuration.dat> \
    -nsteps <step_count> \
    -pin off
```

<a id="lammps"></a>

### LAMMPS

<a id="id5"></a>

#### GPU

```shell
#!/bin/bash
#SBATCH --account=<account_to_charge>
#SBATCH --job-name="<job_name>"
#SBATCH --constraint=MI250
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=1:00:00

module purge

module load CCE-GPU-3.1.0
module load lammps

module list

export MPICH_GPU_SUPPORT_ENABLED=1

export NUM_THREADS=1
srun --nodes=1 --ntasks-per-node=8 --cpus-per-task="${NUM_THREADS}" --threads-per-core=1 --gpus-per-task=1 --gpu-bind=closest --label \
    -- lmp -sf kk -k on g 8 -i in.lj
```

<a id="id6"></a>

#### CPU

```shell
#!/bin/bash
#SBATCH --account=<account_to_charge>
#SBATCH --job-name="<job_name>"
#SBATCH --constraint=GENOA
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=1:00:00

module purge

module load archive
module load CCE-CPU-2.1.0
module load lammps

module list

# export OMP_DISPLAY_AFFINITY=TRUE
export OMP_PROC_BIND=CLOSE
export OMP_PLACES=THREADS

export OMP_NUM_THREADS=2
srun --ntasks-per-node=192 --cpus-per-task="${OMP_NUM_THREADS}" --threads-per-core=2 --label \
    -- lmp -sf omp -i <case>
```

<a id="namd"></a>

### NAMD

**Note**

You may find [this website](https://mdbench.ace-net.ca/mdbench/) interesting to select the software and SLURM options.

<a id="id7"></a>

#### GPU

The NAMD GPU binary is **single node, multi GPU**.

```shell
#!/bin/bash
#SBATCH --account=<account_to_charge>
#SBATCH --job-name="<job_name>"
#SBATCH --constraint=MI250
#SBATCH --nodes=1 # Only support mono node (non-MPI) computations.
#SBATCH --exclusive
#SBATCH --time=1:00:00

module purge

module load develop
module load archive

module load GCC-GPU-5.0.0
module load namd/3.0.2-rocm-gpu-resident-mpi-gpu

module list

# As many core as GPUs.
NUM_THREADS=8
srun --nodes=1 --ntasks-per-node=1 --cpus-per-task="${NUM_THREADS}" --threads-per-core=1 --cpu-bind=none --mem-bind=none --label \
    -- namd3 +p "${NUM_THREADS}" --CUDASOAintegrate on +devices 0,1,2,3,4,5,6,7 ./stmv.namd
```

<a id="id8"></a>

#### CPU

```shell
#!/bin/bash
#SBATCH --account=<account_to_charge>
#SBATCH --job-name="<job_name>"
#SBATCH --constraint=GENOA
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=1:00:00

module purge

module load archive
module load GCC-CPU-2.1.0
module load namd

module list

NUM_THREADS=4
srun --ntasks-per-node=48 --cpus-per-task="${NUM_THREADS}" --threads-per-core=1 --label \
    -- namd3 +p "${NUM_THREADS}" +setcpuaffinity <case>
```

<a id="quantum-espresso"></a>

### Quantum espresso

<a id="id9"></a>

#### CPU

```shell
#!/bin/bash
#SBATCH --account=<account_to_charge>
#SBATCH --job-name="<job_name>"
#SBATCH --constraint=GENOA
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=1:00:00

module purge

module load develop GCC-CPU-3.1.0
module load quantum-espresso

module list

# export OMP_DISPLAY_AFFINITY=TRUE
export OMP_PROC_BIND=CLOSE
export OMP_PLACES=THREADS

export OMP_NUM_THREADS=1
srun --ntasks-per-node=192 --cpus-per-task="${OMP_NUM_THREADS}" --threads-per-core=1 --label \
    -- pw.x < <case>
```

<a id="other-simulation-softwares"></a>

## Other simulation softwares

<a id="boltz"></a>

### Boltz

One possible way to use Boltz on Adastra is to separate MSA from structure predictions, i.e. using `compute_msa` to generate MSA files for your sequences on the login node (or wherever you have internet access), specifying the files in the input FASTA files, and running predictions without the flag `--use_msa_server`. Unless you do that Boltz will try to download file from the internet while it is running on a compute node which does not have access <https://api.colabfold.com>.

You can ask more questions on the subject here <https://github.com/jwohlwend/boltz/issues/176#issuecomment-2646006610>

<a id="vasp"></a>

### VASP

<a id="id10"></a>

#### CPU

An example module environment is given below. This is the one we typically use in combination with the VASP `makefile.include` below:

```shell-session
$ module purge
$ module load cpe/24.07
$ module load craype-x86-genoa
$ module load PrgEnv-gnu
$ module load cray-hdf5 cray-fftw
$ module list
```

<a id="compilation"></a>

##### Compilation

**Note**

We tend to prefer building using the GNU toolchain instead of the Intel toolchain. The Intel Classic (`ifort`) compiler is no longer supported. The new Intel Fortran compiler (`ifx`) is not as well known and *battle tested* as the older one.

CINES provides a `makefile.include` machine file for the environment defined above (GNU/GCC based).

The `makefile.include` file is to be placed into the Vasp repository’s directory (next to the `makefile` and `README.md`), its content is:

```makefile
# Default precompiler options
CPP_OPTIONS = -DHOST=\"LinuxGNU\" \
              -DMPI -DMPI_BLOCK=8000 -Duse_collective \
              -DscaLAPACK \
              -DCACHE_SIZE=4000 \
              -Davoidalloc \
              -Dvasp6 \
              -Duse_bse_te \
              -Dtbdyn \
              -Dfock_dblbuf \
              -D_OPENMP \
              -DMPI_INPLACE

CPP         = cc -E -C -w $*$(FUFFIX) >$*$(SUFFIX) $(CPP_OPTIONS)
CC          = cc -fopenmp
FC          = ftn -fopenmp
FCL         = ftn -fopenmp

FREE        = -ffree-form -ffree-line-length-none

FFLAGS      = -w -ffpe-summary=none

OFLAG       = -O2 # Or O3
OFLAG_IN    = $(OFLAG)
DEBUG       = -O0

# NOTE: you have to comment these tree lines below if you want to build
# Vasp 6.5.
OBJECTS     = fftmpiw.o fftmpi_map.o fftw3d.o fft3dlib.o
OBJECTS_O1 += fftw3d.o fftmpi.o fftmpiw.o
OBJECTS_O2 += fft3dlib.o

CPP_LIB     = $(CPP)
FC_LIB      = $(FC)
CC_LIB      = $(CC)
CFLAGS_LIB  = -O
FFLAGS_LIB  = -O1
FREE_LIB    = $(FREE)

OBJECTS_LIB = linpack_double.o

# For the parser library
CXX_PARS    = CC

# We need that because we link using the `ftn` which does not link with the C++
# library (obviously).
LLIBS       = -lstdc++

##
## Customize as of this point! Of course you may change the preceding
## part of this file as well if you like, but it should rarely be
## necessary ...
##

# When compiling on the target machine itself, change this to the
# relevant target when cross-compiling for another architecture
# Implicit with Cray wrappers:
# FFLAGS += -march=znver4

# For gcc-10 and higher (VASP is non standard)
FFLAGS += -fallow-argument-mismatch

# BLAS (mandatory)
# LAPACK (mandatory)
# scaLAPACK (mandatory)
# Implicit with Cray wrappers.

# HDF5-support (optional but strongly recommended)
CPP_OPTIONS+= -DVASP_HDF5
# Implicit with Cray wrappers.

# For the fftlib library (recommended)
CPP_OPTIONS += -Dsysv
FCL         += fftlib.o
CXX_FFTLIB   = CC -fopenmp -std=c++11 -DFFTLIB_THREADSAFE
INCS_FFTLIB  = -I./include
LIBS        += fftlib
LLIBS       += -ldl
```

**Note**

This makefile configuration is regularly used for GNU based builds for Vasp 6.3.2 sometimes with VTST and Vaspsol.

Then one does the following commands:

```shell-session
$ rm -rf build
$ mkdir -p bin
$ make -j DEPS=1 VASP_BUILD_DIR=build all
```

The binaries will be placed in the `bin` directory inside the Vasp repository’s directory.

**Warning**

Before compiling, ensure you do not have older binaries in the `bin` directory.

To build with `ifort`, you may use the following environment and makefile configuration.

```shell-session
$ module purge
$ module load cpe/24.07
$ module load craype-x86-rome
$ module load PrgEnv-intel
$ module load intel-classic
$ module unload cray-libsci
$ module load cray-hdf5-parallel cray-fftw
$ module list
$ export LD_LIBRARY_PATH="/opt/cray/pe/lib64:${LD_LIBRARY_PATH}"
```

```makefile
# Default precompiler options
CPP_OPTIONS = -DHOST=\"LinuxIFC\" \
              -DMPI -DMPI_BLOCK=8000 -Duse_collective \
              -DscaLAPACK \
              -DCACHE_SIZE=4000 \
              -Davoidalloc \
              -Dvasp6 \
              -Duse_bse_te \
              -Dtbdyn \
              -Dfock_dblbuf \
              -D_OPENMP \
              -DMPI_INPLACE

CPP         = fpp -f_com=no -free -w0 $*$(FUFFIX) $*$(SUFFIX) $(CPP_OPTIONS)
CC          = cc -fopenmp
FC          = ftn -fopenmp
FCL         = ftn -fopenmp

FREE        = -free -names lowercase

FFLAGS      = -assume byterecl -w

OFLAG       = -O2
OFLAG_IN    = $(OFLAG)
DEBUG       = -O0

# NOTE: you have to comment these tree lines below if you want to build
# Vasp 6.5.
OBJECTS     = fftmpiw.o fftmpi_map.o fftw3d.o fft3dlib.o
OBJECTS_O1 += fftw3d.o fftmpi.o fftmpiw.o
OBJECTS_O2 += fft3dlib.o

CPP_LIB     = $(CPP)
FC_LIB      = $(FC)
CC_LIB      = $(CC)
CFLAGS_LIB  = -O
FFLAGS_LIB  = -O1
FREE_LIB    = $(FREE)

OBJECTS_LIB = linpack_double.o

# For the parser library
CXX_PARS    = CC

# We need that because we link using the `ftn` which does not link with the C++
# library (obviously).
LLIBS       = -lstdc++

##
## Customize as of this point! Of course you may change the preceding
## part of this file as well if you like, but it should rarely be
## necessary ...
##

# When compiling on the target machine itself, change this to the
# relevant target when cross-compiling for another architecture
FFLAGS += -xAVX

# BLAS (mandatory)
# LAPACK (mandatory)
# scaLAPACK (mandatory)
LLIBS += -L/opt/cray/pe/libsci/24.07.0/GNU/12.2/x86_64/lib -lsci_gnu -lsci_gnu_mpi

# HDF5-support (optional but strongly recommended)
CPP_OPTIONS+= -DVASP_HDF5
# Implicit with Cray wrappers.

# For the fftlib library (recommended)
CPP_OPTIONS += -Dsysv
FCL         += fftlib.o
CXX_FFTLIB   = CC -fopenmp -std=c++11 -DFFTLIB_THREADSAFE
INCS_FFTLIB  = -I./include
LIBS        += fftlib
LLIBS       += -ldl
```

<a id="running"></a>

##### Running

```shell
#!/bin/bash
#SBATCH --account=<account_to_charge>
#SBATCH --job-name="<job_name>"
#SBATCH --constraint=GENOA
#SBATCH --nodes=2
#SBATCH --exclusive
#SBATCH --time=1:00:00

module purge

module load cpe/24.07
module load craype-x86-genoa
module load PrgEnv-gnu

module load cray-hdf5 cray-fftw

module list

# export OMP_DISPLAY_AFFINITY=TRUE
export OMP_PROC_BIND=CLOSE
export OMP_PLACES=THREADS

export OMP_NUM_THREADS=1
srun --ntasks-per-node=192 --cpus-per-task="${OMP_NUM_THREADS}" --threads-per-core=1 --label \
    -- vasp_std
```
