<!-- Source: https://dci.dci-gitlab.cines.fr/webextranet/software_stack/libraries/index.html -->
<!-- Title: Libraries & toolchains -->

<a id="libraries-toolchains"></a>

<a id="adastra-software-stack-libraries"></a>

# Libraries & toolchains

<a id="cines-spack-modules"></a>

## CINES Spack modules

CINES provides **libraries** built using Spack. To access these products, check [this document](../cines_software_stack/spack.md#adastra-software-stack-cines-software-stack-spack-using) and or look at this [product catalog](../cines_software_stack/spack_products_catalog.md#adastra-software-stack-spack-product-catalog).

<a id="example-script-for-cines-spack-modules-libraries"></a>

## Example script for CINES Spack modules libraries

**Warning**

Work in progress.

<a id="apex"></a>

## Apex

**Note**

You may benefit from using a Python virtual environment, check [this document](../tools/index.md#adastra-software-stack-tools-python-virtual-environment) on how to setup one.

Requirements:

- A recent [install of PyTorch](index.md#adastra-software-stack-libraries-pytorch-installing) for ROCm (say in a VEnv).

You can compile Apex on Adastra using the script below.

```shell
#!/bin/bash

set -eu

# Cloning the code on a login node.
git clone https://github.com/ROCm/apex || true
cd apex
git checkout a3feba8942c2627237ed96645b613aaa70e3b258 # release/1.6.0
git submodule init
git submodule update

module purge

module load cpe/24.07
module load craype-accel-amd-gfx90a craype-x86-trento
module load PrgEnv-gnu
module load amd-mixed/6.2.1 # Match this version with the PyTorch ROCm and Apex version.
module load cray-python

module list

# If you use a Virtual Environment (VEnv):
# - deactivate it before loading modules;
# - activate it after loading modules like so:
# source ./python_environment/bin/activate
# - ensure you have installed PyTorch for the correct GPUs.

pip3 install ninja

export PYTORCH_ROCM_ARCH="gfx90a;gfx942"
export MAX_JOBS="$(nproc)"

pip3 install --verbose --no-cache-dir --no-build-isolation --config-settings="--build-option=--cpp_ext" --config-settings="--build-option=--cuda_ext" ./
# # Or build the wheel that you can reuse later:
# python3 setup.py bdist_wheel --cpp_ext --cuda_ext
```

**Warning**

Apex has strong PyTorch and ROCm version dependencies. Check [this document](https://github.com/ROCm/apex?tab=readme-ov-file#supported-versions) for supported PyTorch versions for a given Apex version.

<a id="blas-lapack-scalapack"></a>

## BLAS, LAPACK & ScaLAPACK

**Note**

LibSci is based on OpenBLAS (GotoBLAS). You probably do **NOT** need to compile your own BLAS.

**Note**

We have know that applications using LibSci can observe better performance. We recommend LibSci if your code allows it.

<a id="libsci"></a>

### LibSci

LibSci is a collection of numerical routines. It contains, notably:

- a Basic Linear Algebra Subroutines (BLAS);
- a C interface to BLAS (CBLAS);
- a Basic Linear Algebra Communication Subprograms (BLACS);
- a Linear Algebra PACKage (LAPACK);
- and a Scalable LAPACK (ScaLAPACK).

Two flavors of this library exist, one for CPUs exposed through the `cray-libsci` module and a CPU/GPU hybrid one, exposed through the `cray-libsci_acc` module.

**Note**

The `CRAY_LIBSCI_BASE_DIR` and `CRAY_LIBSCI_PREFIX` environment variable bear a different name in older CPE versions. You way want to use `CRAY_PE_LIBSCI_PREFIX_DIR` and `CRAY_PE_LIBSCI_PREFIX` instead.

<a id="cpu"></a>

#### CPU

If you bypass the Cray compiler wrappers, you **need to do more work** and risk mixing incompatible libraries or ABI. Use at your own risk the information given below:

| Implementation | Module | Compiler or wrapper | Header Files & Linking |
| --- | --- | --- | --- |
| LibSci | `cray-libsci` | `cc`, `CC`, `ftn` (Cray compiler wrappers) | The wrappers will automatically add the header flags and the linker flags. |
| *Raw* compilers. | First, ensure you have the module loaded then,  to compile: `-isystem "${CRAY_LIBSCI_BASE_DIR}/<toolchain>/<version>/<cpu>/include"`;  to link: `-L"${CRAY_LIBSCI_BASE_DIR}/<toolchain>/<version>/<cpu>/lib" -lsci_<toolchain> -lsci_<toolchain>_<variant>`.  Or (more concisely, use `${CRAY_LIBSCI_PREFIX}`:  to compile: `-isystem "${CRAY_LIBSCI_PREFIX}/include"`;  to link: `-L"${CRAY_LIBSCI_PREFIX}/lib" -lsci_<toolchain> -lsci_<toolchain>_<variant>`. |

Where `<toolchain>` can be `[AMD|AOCC|CRAYCLANG|GNU|INTEL|NVIDIA]`; `cpu` is `x86_64`. `sci_<toolchain>_<variant>` is left as a choice for the user:

| Library name | Variant | Link type | Threading | MPI | Service provided |
| --- | --- | --- | --- | --- | --- |
| libsci_<toolchain>.a | - | Static | **Serial** non-threaded | non-MPI | BLAS/CBLAS/LAPACK |
| libsci_<toolchain>.so | Dynamic shared | **Serial** non-threaded | non-MPI |
| libsci_<toolchain>_mp.a | `mp` | Static | **Parallel** multi-threaded (OpenMP) | non-MPI |
| libsci_<toolchain>_mp.so | Dynamic shared | **Parallel** multi-threaded (OpenMP) | non-MPI |
| libsci_<toolchain>_mpi.a | `mpi` | Static | **Serial** non-threaded | MPI | BLACS/ScaLAPACK  These requires a BLAS and LAPACK. You should link one of the above mentioned libraries providing such facilities. |
| libsci_<toolchain>_mpi.so | Dynamic shared | **Serial** non-threaded | MPI |
| libsci_<toolchain>_mpi_mp.a | `mpi_mp` | Static | **Parallel** multi-threaded (OpenMP) | MPI |
| libsci_<toolchain>_mpi_mp.so | Dynamic shared | **Parallel** multi-threaded (OpenMP) | MPI |

**Note**

BLAS and LAPACK routines do not require MPI and are contained in the non-MPI version of the libraries. The ScaLAPACK routines are imported by linking with the MPI version of the library. The MPI version of the library implies a dependency on the non-MPI version (i.e., `libsci_<toolchain>_mpi.so` depends on the routines of `libsci_<toolchain>.so`). Obviously, this dependency chain does **NOT** work for static libraries; then you have to explicitly add the `libsci_<toolchain>.a`.

**Warning**

The LibSci module for the `PrgEnv-intel` does not exist, but the libraries do.

**Warning**

The static versions of LibSci for the AMD (ROCm stack) compiler needs the following additional linker flags: `-L${ROCM_PATH}/llvm/lib -lflang -lpgmath -lflangrti -lm -ldl`.

Regarding the OpenMP variants; if you call a LibSci routine inside of an OpenMP parallel region, the routine will always be serial. If you call a routine outside of a parallel region and if the LibSci linked is OpenMP enabled, the routine will be threaded, else it will be serial.

Generally, one relies on the compiler wrappers like so:

```shell-session
$ module load craype-x86-genoa
$ module load PrgEnv-gnu
$ # The cc, CC, ftn wrappers will automatically add the header flags and the
$ # linker flags.
```

By default, the compiler wrappers will link with a single threaded BLAS, LAPACK and ScaLAPACK. If you add the `-fopenmp` flag, the multi-threaded version we be used instead.

```shell-session
$ # Implies (as needed) lsci_<toolchain>_mpi.so    and lsci_<toolchain>.so
$ CC          main.cc
$ # Implies (as needed) lsci_<toolchain>_mpi_mp.so and lsci_<toolchain>_mp.so
$ CC -fopenmp main.cc
```

More details in:

```shell-session
$ module load cray-libsci
$ man intro_libsci
```

**Note**

The serial LibSci should be compatible across toolchain (thanks to proper C interfaces). This is not the case with the multi-threaded versions because the OpenMP backend differs across toolchains.

**Warning**

If using a [mixed](../../user_support/index.md#adastra-programming-environment-mixing-prgenv) PrgEnv (say, `PrgEnv-cray-amd`), the `${CRAY_LIBSCI_PREFIX}` variable points towards a build for the C/C++ compiler. For `PrgEnv-cray-amd` it would be the CCE. For `PrgEnv-gnu-amd` it would be GNU.

<a id="cpu-gpu-hybrid"></a>

#### CPU/GPU hybrid

The accelerated LibSci is augmented with GPU capabilities. It can decide for itself wether to use the GPU or CPU version of a routine.

Before calling such routines, one needs to initialize the library:

```
Fortran API:
    subroutine libsci_acc_init()
    subroutine libsci_acc_finalize()
C/C++ API:
    void libsci_acc_init(void);
    void libsci_acc_finalize(void);
```

If you bypass the Cray compiler wrappers, you **need to do more work** and risk mixing incompatible libraries or ABI. Use at your own risk the information given below:

| Implementation | Module | Compiler or wrapper | Header Files & Linking |
| --- | --- | --- | --- |
| LibSci_accel | `cray-libsci_acc` | `cc`, `CC`, `ftn` (Cray compiler wrappers) | The wrappers will automatically add the header flags and the linker flags. |
| *Raw* compilers. | First, ensure you have the module loaded then,  to compile: `-isystem "${LIBSCI_ACC_BASE_DIR}/<toolchain>/<version>/<cpu>/include"`;  to link: `-L"${LIBSCI_ACC_BASE_DIR}/<toolchain>/<version>/<cpu>/lib" -lsci_acc_<toolchain>_<variant>`.  Or (more concisely, use `${CRAY_LIBSCI_PREFIX}`):  to compile: `-isystem "${CRAY_LIBSCI_ACC_PREFIX_DIR}/include"`;  to link: `-L"${CRAY_LIBSCI_ACC_PREFIX_DIR}/lib" -lsci_acc_<toolchain>_<variant>`. |

Where `<toolchain>` can be `[AMD|CRAYCLANG|GNU]`; `cpu` is `x86_64`. `sci_acc_<toolchain>_<variant>`’s `<variant>` is conditioned by the architecture (`gfx90a` for MI250X, `gfx942` for MI300A).

Generally, one relies on the compiler wrappers like so:

```shell-session
$ module load craype-x86-trento craype-accel-amd-gfx90a
$ module load PrgEnv-cray
$ module load cray-libsci_acc
$ # The cc, CC, ftn wrappers will automatically add the header flags and the
$ # linker flags.
```

**Warning**

To properly link, the compiler wrappers need [loaded architecture modules](../../user_support/index.md#adastra-programming-environment-targeting-architecture)!

More details in:

```shell-session
$ module load cray-libsci_acc
$ man intro_libsci_acc
```

<a id="some-environment-variables"></a>

#### Some environment variables

| Feature/flag/environment variable | Explanation |
| --- | --- |
| `export CRAYBLAS_PROFILING_VERBOSITY=2` | Log profiling data about the Cray BLAS (libsci). |
| `export CRAYBLAS_LEVEL1_LEGACY=1` | As we mentioned above, LibSci is based on OpenBLAS. These environment variables make the routine calls into LibSci be directly forwarded to OpenBLAS. In such case, LibSci should behave as if it was OpenBLAS. |
| `export CRAYBLAS_LEVEL2_LEGACY=1` |
| `export CRAYBLAS_LEVEL3_LEGACY=1` |

<a id="openblas"></a>

### OpenBLAS

CINES provides OpenBLAS Spack products, for the codes that demand, require, necessitate, beg, cry for, expect it and prescribe or forbid any other implementation.

**Note**

You should first try to adapt your code so that it is flexible enough to accept a wrapper provided BLAS, LAPACK. Then use the Cray LibSci.

Check the [catalog](../cines_software_stack/spack_products_catalog.md#adastra-software-stack-spack-product-catalog) for the exact module names or use `module spider openblas`.

<a id="boltz"></a>

## Boltz

Boltz is a family of models for biomolecular interaction prediction.

Requirements:

- A recent [install of PyTorch](index.md#adastra-software-stack-libraries-pytorch-installing) for ROCm (say in a VEnv).

On AMD GPUs, installing Boltz can be done like so:

```shell-session
$ pip3 install boltz==2.2.1
```

Then, one has to be aware that Boltz rely on many external fils that it will try to cache, by default, into this directory: `~/.boltz`.

We advise to export an environment variable that will put these files into the *work* area:

```shell-session
$ export BOLTZ_CACHE="${SHAREDWORKDIR}/BOLTZ_CACHE"
```

Then it is recommended to launch `boltz` on a dummy test case, just so it can populate the cache with data. We need this step done before running on compute nodes because only the login nodes have access to the internet. This can be done like so:

```shell-session
$ # This is expected to fail.
$ boltz predict --out_dir=dummy_case_results cases/dummy_case.yaml || true
$ rm -rf dummy_case_results
```

When ou construct your case, you should remember than the compute node can’t contact the MSA server. As such, it is advised to either pull the MSA before hand and specify it in the YAML file representing the case, for instance:

```yaml
version: 1
sequences:
- protein:
    id: A
    sequence: QLEDSEVEAVAKGLEEMYANGVTEDNFKNYVKNNFAQQEISSVEEELNVNISDSCVANKIKDEFFAMISISAIVKAAQKKAWKELAVTVLRFAKANGLKTNAIIVAGQLALWAVQCG
    msa: ./cases/msa/xyz.a3m # The MSA is already present at this path.
```

**Warning**

Look for warning messages to ensure the MSA is correctly found.

Finally, to run a Boltz case, simply specify that you do not whish to use the CUDA specificities via the `--no_kernels` option. It could look like so:

```shell-session
$ boltz predict --no_kernels --accelerator=gpu cases/prot_custom_msa.yaml
```

<a id="c-standard-parallelization-stdpar"></a>

## C++ standard parallelization (STDPAR)

<a id="amd-hip-support"></a>

### AMD HIP support

HIP provides execution policies allowing the offload to GPUs.

The library is called roc-stdpar and is available here: <https://github.com/ROCm/roc-stdpar>.

A user guide is given here: <https://github.com/amd/amd-lab-notes/tree/release/hipstdpar>

<a id="deepspeed"></a>

## Deepspeed

When it comes to training large models, it becomes crucial to efficiently distribute the weights, gradient and optimizer state across devices. Deepspeed provides [first class AMD support](https://cloudblogs.microsoft.com/opensource/2022/03/21/supporting-efficient-large-model-training-on-amd-instinct-gpus-with-deepspeed/) for such functionalities.

**Note**

You may benefit from using a Python virtual environment, check [this document](../tools/index.md#adastra-software-stack-tools-python-virtual-environment) on how to setup one.

Requirements:

- A recent [install of PyTorch](index.md#adastra-software-stack-libraries-pytorch-installing) for ROCm (say in a VEnv).

<a id="jited-kernels"></a>

### JITed kernels

The default and most simple way to install Deepspeed is to `pip3 install deepspeed`, and let torch’s JIT C++ extension loader do the compiling at runtime.

<a id="prebuilt-kernels"></a>

### Prebuilt kernels

You can compile DeepSpeed on Adastra using the script below.

```shell
#!/bin/bash

set -eu

# Cloning the code on a login node.
git clone https://github.com/microsoft/DeepSpeed || true
cd DeepSpeed
git checkout v0.16.3

module purge

module load cpe/24.07
module load craype-accel-amd-gfx90a craype-x86-trento
module load PrgEnv-gnu
module load amd-mixed/6.2.1 # Match this version with the PyTorch ROCm version.
module load cray-python

module list

# If you use a Virtual Environment (VEnv):
# - deactivate it before loading modules;
# - activate it after loading modules like so:
# source ./python_environment/bin/activate
# - ensure you have installed PyTorch for the correct GPUs.

# Ensure we don't have deepspeed already. Indeed it is a common error to first
# install deepspeed and then try to re-install with prebuilt kernels, it ends up
# doing nothing! To ensure we rebuild, the "--no-cache-dir" is also helpful.
pip3 uninstall --yes deepspeed

export DS_ACCELERATOR="cuda" # Compile to HIP even on login node.
export DS_BUILD_OPS=1
export DS_BUILD_AIO=0                    # 0 KO missing libaio
export DS_BUILD_CCL_COMM=0               # 0 KO missing oneapi
export DS_BUILD_CPU_ADAGRAD=1
export DS_BUILD_CPU_ADAM=1
export DS_BUILD_CPU_LION=1
export DS_BUILD_EVOFORMER_ATTN=0         # 0 KO, idk why
export DS_BUILD_FP_QUANTIZER=0           # 0 KO cuda_bf16. not hip/hip_bf16.
export DS_BUILD_FUSED_ADAM=1
export DS_BUILD_FUSED_LAMB=1
export DS_BUILD_FUSED_LION=1
export DS_BUILD_INFERENCE_CORE_OPS=0     # 0 KO blas_utils_hip.h:60:1: error: ‘rocblas_operation' does not name a type
export DS_BUILD_CUTLASS_OPS=0            # 0 KO missing deepspeed-kernels
export DS_BUILD_QUANTIZER=1
export DS_BUILD_RAGGED_DEVICE_OPS=0      # 0 KO missing deepspeed-kernels
export DS_BUILD_RAGGED_OPS=1
export DS_BUILD_RANDOM_LTD=1
export DS_BUILD_SPARSE_ATTN=0            # 0 KO
export DS_BUILD_SPATIAL_INFERENCE=1
export DS_BUILD_STOCHASTIC_TRANSFORMER=1
export DS_BUILD_TRANSFORMER_INFERENCE=0  # 0 KO inference_cublas_wrappers_hip.h:24:20: error: ‘rocblas_operation' was not declared in this scope
export DS_BUILD_TRANSFORMER=1

export PYTORCH_ROCM_ARCH="gfx90a;gfx942"
export MAX_JOBS="$(nproc)"

pip3 install --verbose --no-cache-dir --no-build-isolation ./
# # Or build the wheel that you can reuse later:
# python3 setup.py bdist_wheel
```

**Warning**

Regardless of the `DS_BUILD_*` options you choose, do run the `ds_report` command on a compute node to check if the library is working properly. You should see a bunch of `OKAY` in the right column (compatible), and if you choose to build the “ops” (`DS_BUILD_*`), into the left column (installed), a bunch of `YES` should be present.

**Note**

You may **NOT** need all the deepspeed features reported by `ds_report`. Do not spend too much time tinkering with a DeepSpeed build script for a feature you do not need.

<a id="id1"></a>

### Some environment variables

| Feature/flag/environment variable | Explanation |
| --- | --- |
| `export DS_ENV_FILE=<path_to_spack_configuration>` | Can be used to factorize a configuration. See [this document](https://www.deepspeed.ai/docs/config-json/) on what should/can go into this file. |

<a id="flash-attention-v1-v2"></a>

<a id="adastra-software-stack-libraries-flash-attention"></a>

## Flash attention (v1/v2)

When it comes to training transformer based LLM, it becomes crucial to efficiently compute the attention mechanism. For Nvidia GPUs, a reference implementation is [flash-attn](https://github.com/Dao-AILab/flash-attention). There exist a [ROCm flash-attention repository](https://github.com/ROCm/flash-attention) that has not been **merged into upstream flash-attention**. That being said, an AMD flash attention package is not available in the official PyPi repository, you have to compile it yourself.

**Note**

You may benefit from using a Python virtual environment, check [this document](../tools/index.md#adastra-software-stack-tools-python-virtual-environment) on how to setup one.

Requirements:

- A recent [install of PyTorch](index.md#adastra-software-stack-libraries-pytorch-installing) for ROCm (say in a VEnv).

You can compile flash-attn on Adastra using the script below.

<a id="flash-attention-v1-for-pytorch-2-3-1-rocm5-7"></a>

### Flash attention v1 for PyTorch <= 2.3.1+rocm5.7

```shell
#!/bin/bash

set -eu

# Cloning the code on a login node.
git clone --branch="flash_attention_for_rocm" https://github.com/ROCm/flash-attention || true
cd flash-attention
git submodule init
git submodule update

module purge

module load cpe/23.12
module load craype-accel-amd-gfx90a craype-x86-trento
module load PrgEnv-gnu
module load amd-mixed
module load cray-python

module list

# If you use a Virtual Environment (VEnv):
# - deactivate it before loading modules;
# - activate it after loading modules like so:
# source ./python_environment/bin/activate
# - ensure you have installed PyTorch for the correct GPUs.

pip3 install ninja einops packaging wheel

export GPU_ARCHS="gfx90a"
export MAX_JOBS="$(nproc)"

pip3 install --verbose --no-cache-dir --no-build-isolation ./
# # Or build the wheel that you can reuse later:
# python3 setup.py bdist_wheel
```

<a id="flash-attention-v2-for-pytorch-2-3-1-rocm6"></a>

### Flash attention v2 for PyTorch > 2.3.1+rocm6

```shell
#!/bin/bash

set -eu

# Cloning the code on a login node.
git clone https://github.com/Dao-AILab/flash-attention || true
cd flash-attention
git checkout v2.7.4
git submodule init
git submodule update

module purge

module load cpe/24.07
module load craype-accel-amd-gfx90a craype-x86-trento
module load PrgEnv-gnu
module load amd-mixed/6.2.1 # Match this version with the PyTorch ROCm version.
module load cray-python

module list

# If you use a Virtual Environment (VEnv):
# - deactivate it before loading modules;
# - activate it after loading modules like so:
# source ./python_environment/bin/activate
# - ensure you have installed PyTorch for the correct GPUs.

pip3 install ninja packaging

export GPU_ARCHS="gfx90a;gfx942" BUILD_TARGET="rocm"
export MAX_JOBS="$(nproc)"

pip3 install --verbose --no-cache-dir --no-build-isolation ./
# # Or build the wheel that you can reuse later:
# python3 setup.py bdist_wheel
```

<a id="benchmarks"></a>

### Benchmarks

Measured 2024/09/09 on Flash2 v2.6.3 build using rocm/6.0.0 and PyTorch 2.4.1+rocm6.0.

<a id="on-mi250x"></a>

#### On MI250X:

```
### causal=False, headdim=128, batch_size=2, seqlen=8192 ###
Flash2 fwd: 100.18 TFLOPs/s, bwd: 49.36 TFLOPs/s, fwd + bwd: 57.73 TFLOPs/s
Pytorch fwd: 34.59 TFLOPs/s, bwd: 50.20 TFLOPs/s, fwd + bwd: 44.46 TFLOPs/s
Triton fwd: 0.00 TFLOPs/s, bwd: 0.00 TFLOPs/s, fwd + bwd: 0.00 TFLOPs/s # OOM
### causal=False, headdim=128, batch_size=1, seqlen=16384 ###
Flash2 fwd: 101.16 TFLOPs/s, bwd: 49.67 TFLOPs/s, fwd + bwd: 58.12 TFLOPs/s
Pytorch fwd: 27.96 TFLOPs/s, bwd: 40.23 TFLOPs/s, fwd + bwd: 35.75 TFLOPs/s
Triton fwd: 0.00 TFLOPs/s, bwd: 0.00 TFLOPs/s, fwd + bwd: 0.00 TFLOPs/s # OOM
### causal=True, headdim=128, batch_size=2, seqlen=8192 ###
Flash2 fwd: 92.83 TFLOPs/s, bwd: 46.02 TFLOPs/s, fwd + bwd: 53.77 TFLOPs/s
Pytorch fwd: 11.95 TFLOPs/s, bwd: 26.27 TFLOPs/s, fwd + bwd: 19.57 TFLOPs/s
Triton fwd: 0.00 TFLOPs/s, bwd: 0.00 TFLOPs/s, fwd + bwd: 0.00 TFLOPs/s # OOM
### causal=True, headdim=128, batch_size=1, seqlen=16384 ###
Flash2 fwd: 94.49 TFLOPs/s, bwd: 49.66 TFLOPs/s, fwd + bwd: 57.45 TFLOPs/s
Pytorch fwd: 10.01 TFLOPs/s, bwd: 21.15 TFLOPs/s, fwd + bwd: 16.05 TFLOPs/s
Triton fwd: 0.00 TFLOPs/s, bwd: 0.00 TFLOPs/s, fwd + bwd: 0.00 TFLOPs/s # OOM
```

<a id="on-mi300a"></a>

#### On MI300A:

```
### causal=False, headdim=128, batch_size=2, seqlen=8192 ###
Flash2 fwd: 377.58 TFLOPs/s, bwd: 74.65 TFLOPs/s, fwd + bwd: 96.85 TFLOPs/s
Pytorch fwd: 77.26 TFLOPs/s, bwd: 118.31 TFLOPs/s, fwd + bwd: 102.71 TFLOPs/s
Triton fwd: 0.00 TFLOPs/s, bwd: 0.00 TFLOPs/s, fwd + bwd: 0.00 TFLOPs/s
### causal=False, headdim=128, batch_size=1, seqlen=16384 ###
Flash2 fwd: 384.45 TFLOPs/s, bwd: 74.77 TFLOPs/s, fwd + bwd: 97.13 TFLOPs/s
Pytorch fwd: 71.74 TFLOPs/s, bwd: 120.53 TFLOPs/s, fwd + bwd: 100.92 TFLOPs/s
Triton fwd: 0.00 TFLOPs/s, bwd: 0.00 TFLOPs/s, fwd + bwd: 0.00 TFLOPs/s # OOM
### causal=True, headdim=128, batch_size=2, seqlen=8192 ###
Flash2 fwd: 288.32 TFLOPs/s, bwd: 68.16 TFLOPs/s, fwd + bwd: 87.18 TFLOPs/s
Pytorch fwd: 27.15 TFLOPs/s, bwd: 62.42 TFLOPs/s, fwd + bwd: 45.52 TFLOPs/s
Triton fwd: 0.00 TFLOPs/s, bwd: 0.00 TFLOPs/s, fwd + bwd: 0.00 TFLOPs/s
### causal=True, headdim=128, batch_size=1, seqlen=16384 ###
Flash2 fwd: 291.85 TFLOPs/s, bwd: 71.77 TFLOPs/s, fwd + bwd: 91.48 TFLOPs/s
Pytorch fwd: 25.17 TFLOPs/s, bwd: 64.43 TFLOPs/s, fwd + bwd: 44.57 TFLOPs/s
Triton fwd: 0.00 TFLOPs/s, bwd: 0.00 TFLOPs/s, fwd + bwd: 0.00 TFLOPs/s # OOM
```

<a id="hdf5"></a>

## HDF5

If you bypass the Cray compiler wrappers, you **need to do more work** and risk mixing incompatible libraries or ABI. Use at your own risk the information given below:

| Implementation | Module | Compiler or wrapper | Header Files & Linking |
| --- | --- | --- | --- |
| HDF5 | `cray-hdf5` | `cc`, `CC`, `ftn` (Cray compiler wrappers) | The wrappers will automatically add the header flags and the linker flags. |
| *Raw* compilers. | First, ensure you have the module loaded then,  to compile: `-isystem "${CRAY_HDF5_DIR}/<toolchain>/<version>/include"`;  to link: `-L"${CRAY_HDF5_DIR}/<toolchain>/<version>/lib" -lhdf5_hl -lhdf5 -lhdf5_hl_cpp -lhdf5_cpp -lhdf5hl_fortran -lhdf5_fortran`.  Or (more concisely):  to compile: `-isystem "${CRAY_HDF5_PREFIX}/include"`;  to link: `-L"${CRAY_HDF5_PREFIX}/lib" -lhdf5_hl -lhdf5 -lhdf5_hl_cpp -lhdf5_cpp -lhdf5hl_fortran -lhdf5_fortran`. |
| Parallel HDF5 | `cray-hdf5-parallel` | `cc`, `CC`, `ftn` (Cray compiler wrappers) | The wrappers will automatically add the header flags and the linker flags. |
| *Raw* compilers. | First, ensure you have the module loaded then,  to compile: `-isystem "${CRAY_HDF5_PARALLEL_DIR}/<toolchain>/<version>/include"`;  to link: `-L"${CRAY_HDF5_PARALLEL_DIR}/<toolchain>/<version>/lib" -lhdf5_hl_parallel -lhdf5_parallel`.  Or (more concisely):  to compile: `-isystem "${CRAY_HDF5_PARALLEL_PREFIX}/include"`;  to link: `-L"${CRAY_HDF5_PARALLEL_PREFIX}/lib" -lhdf5_hl_parallel -lhdf5_parallel`. |

**Note**

The `cray-hdf5[-parallel]` modules define the `${HDF5_ROOT}` environment variable. It is equivalent to `${CRAY_HDF5_PARALLEL_PREFIX}`.

Where `<toolchain>` can be `[AMD|AOCC|CRAYCLANG|GNU|INTEL|NVIDIA]`. `variant` is left as a choice for the user:

Generally, one relies on the compiler wrappers like so:

```shell-session
$ module load craype-x86-genoa
$ module load PrgEnv-gnu
$ # The cc, CC, ftn wrappers will automatically add the header flags and the
$ # linker flags.
```

**Warning**

The `PrgEnv-intel` only provides the `cray-hdf5-parallel`.

**Warning**

The C++ bindings (`H5Cpp.h`) are only provided with `cray-hdf5`, not with `cray-hdf5-parallel`.

<a id="h5py"></a>

### h5py

**Note**

You may benefit from using a Python virtual environment, check [this document](../tools/index.md#adastra-software-stack-tools-python-virtual-environment) on how to setup one.

You can compile h5py on Adastra using the script below.

```shell
#!/bin/bash

set -eu

module purge

module load cpe/24.07
module load craype-accel-amd-gfx90a craype-x86-trento # For a GPU aware MPI
# module load craype-x86-rome # For a CPU only MPI
module load PrgEnv-gnu
# module load PrgEnv-cray

module load amd-mixed/6.1.2 # For a GPU aware MPI
module load cray-python
module load cray-hdf5-parallel # You may change that to use the non parallel HDF5.

module list

# If you use a Virtual Environment (VEnv):
# - deactivate it before loading modules;
# - activate it after loading modules like so:
# source ./python_environment/bin/activate
# - ensure you have installed PyTorch for the correct GPUs.

export CC="cc"
export HDF5_MPI="ON"

pip3 install Cython numpy
pip3 install --verbose --compile --no-cache-dir --no-build-isolation --no-binary=h5py h5py
```

**Warning**

This script build with support for a GPU aware MPI. If you do not need that feature, please comment the `amd-mixed` module and change the `craype-` modules.

<a id="llvm-gcc-toolchain"></a>

## LLVM & GCC toolchain

LLVM is know to be a [bit slow supporting recent GCC toolsets](https://github.com/llvm/llvm-project/pull/178459) on RHEL based distributions, the `--gcc-toolchain=` may be of use then:

```shell-session
$ module purge
$ module load gcc-native/13
$ module load rocm/6.1.2
$ amdclang++ --verbose ./test.cc
AMD clang version 17.0.0 (https://github.com/RadeonOpenCompute/llvm-project roc-6.1.2 24193 669db884972e769450470020c06a6f132a8a065b)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /lus/home/softs/rocm/6.1.2/lib/llvm/bin
Configuration file: /lus/home/softs/rocm/6.1.2/lib/llvm/bin/clang++.cfg
Found candidate GCC installation: /opt/rh/gcc-toolset-12/root/usr/lib/gcc/x86_64-redhat-linux/12
Selected GCC installation: /opt/rh/gcc-toolset-12/root/usr/lib/gcc/x86_64-redhat-linux/12
Candidate multilib: .;@m64
Candidate multilib: 32;@m32
Selected multilib: .;@m64
Found HIP installation: /lus/home/softs/rocm/6.1.2/lib/llvm/bin/../../.., version 6.1.40093
"/lus/home/softs/rocm/6.1.2/lib/llvm/bin/clang-17" -cc1 -triple x86_64-unknown-linux-gnu -emit-obj -mrelax-all -dumpdir a- -disable-free -clear-ast-before-backend -disable-llvm-verifier -discard-value-names -main-file-name test.cc -mrelocation-model static -mframe-pointer=all -fmath-errno -ffp-contract=on -fno-rounding-math -mconstructor-aliases -funwind-tables=2 -target-cpu x86-64 -tune-cpu generic -debugger-tuning=gdb -v -fcoverage-compilation-dir=./test_diretory -resource-dir /lus/home/softs/rocm/6.1.2/lib/llvm/lib/clang/17 -internal-isystem /opt/rh/gcc-toolset-12/root/usr/lib/gcc/x86_64-redhat-linux/12/../../../../include/c++/12 -internal-isystem /opt/rh/gcc-toolset-12/root/usr/lib/gcc/x86_64-redhat-linux/12/../../../../include/c++/12/x86_64-redhat-linux -internal-isystem /opt/rh/gcc-toolset-12/root/usr/lib/gcc/x86_64-redhat-linux/12/../../../../include/c++/12/backward -internal-isystem /lus/home/softs/rocm/6.1.2/lib/llvm/lib/clang/17/include -internal-isystem /usr/local/include -internal-isystem /opt/rh/gcc-toolset-12/root/usr/lib/gcc/x86_64-redhat-linux/12/../../../../x86_64-redhat-linux/include -internal-externc-isystem /include -internal-externc-isystem /usr/include -fdeprecated-macro -fdebug-compilation-dir=./test_diretory -ferror-limit 19 -fgnuc-version=4.2.1 -fcxx-exceptions -fexceptions -fcolor-diagnostics -faddrsig -D__GCC_HAVE_DWARF2_CFI_ASM=1 -o /tmp/test-f2f7ef.o -x c++ ./test.cc
clang -cc1 version 17.0.0 based upon LLVM 17.0.0git default target x86_64-unknown-linux-gnu
ignoring nonexistent directory "/opt/rh/gcc-toolset-12/root/usr/lib/gcc/x86_64-redhat-linux/12/../../../../x86_64-redhat-linux/include"
ignoring nonexistent directory "/include"
#include "..." search starts here:
#include <...> search starts here:
/opt/rh/gcc-toolset-12/root/usr/lib/gcc/x86_64-redhat-linux/12/../../../../include/c++/12
/opt/rh/gcc-toolset-12/root/usr/lib/gcc/x86_64-redhat-linux/12/../../../../include/c++/12/x86_64-redhat-linux
/opt/rh/gcc-toolset-12/root/usr/lib/gcc/x86_64-redhat-linux/12/../../../../include/c++/12/backward
/lus/home/softs/rocm/6.1.2/lib/llvm/lib/clang/17/include
/usr/local/include
/usr/include
End of search list.
"/lus/home/softs/rocm/6.1.2/lib/llvm/bin/ld.lld" --hash-style=gnu --eh-frame-hdr -m elf_x86_64 -dynamic-linker /lib64/ld-linux-x86-64.so.2 -o a.out /lib/../lib64/crt1.o /lib/../lib64/crti.o /lus/home/softs/rocm/6.1.2/lib/llvm/lib/clang/17/lib/linux/clang_rt.crtbegin-x86_64.o -L/opt/rh/gcc-toolset-12/root/usr/lib/gcc/x86_64-redhat-linux/12 -L/opt/rh/gcc-toolset-12/root/usr/lib/gcc/x86_64-redhat-linux/12/../../../../lib64 -L/lib/../lib64 -L/usr/lib/../lib64 -L/lib -L/usr/lib --enable-new-dtags /tmp/test-f2f7ef.o -lstdc++ -lm /lus/home/softs/rocm/6.1.2/lib/llvm/lib/clang/17/lib/linux/libclang_rt.builtins-x86_64.a -lgcc_s -lc /lus/home/softs/rocm/6.1.2/lib/llvm/lib/clang/17/lib/linux/libclang_rt.builtins-x86_64.a -lgcc_s /lus/home/softs/rocm/6.1.2/lib/llvm/lib/clang/17/lib/linux/clang_rt.crtend-x86_64.o /lib/../lib64/crtn.o
$ amdclang++ --gcc-install-dir="${GCC_PATH}/lib/gcc/x86_64-redhat-linux/13" --verbose ./test.cc
AMD clang version 17.0.0 (https://github.com/RadeonOpenCompute/llvm-project roc-6.1.2 24193 669db884972e769450470020c06a6f132a8a065b)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /lus/home/softs/rocm/6.1.2/lib/llvm/bin
Configuration file: /lus/home/softs/rocm/6.1.2/lib/llvm/bin/clang++.cfg
Selected GCC installation: /opt/rh/gcc-toolset-13/root/usr/lib/gcc/x86_64-redhat-linux/13
Candidate multilib: .;@m64
Candidate multilib: 32;@m32
Selected multilib: .;@m64
Found HIP installation: /lus/home/softs/rocm/6.1.2/lib/llvm/bin/../../.., version 6.1.40093
"/lus/home/softs/rocm/6.1.2/lib/llvm/bin/clang-17" -cc1 -triple x86_64-unknown-linux-gnu -emit-obj -mrelax-all -dumpdir a- -disable-free -clear-ast-before-backend -disable-llvm-verifier -discard-value-names -main-file-name test.cc -mrelocation-model static -mframe-pointer=all -fmath-errno -ffp-contract=on -fno-rounding-math -mconstructor-aliases -funwind-tables=2 -target-cpu x86-64 -tune-cpu generic -debugger-tuning=gdb -v -fcoverage-compilation-dir=./test_diretory -resource-dir /lus/home/softs/rocm/6.1.2/lib/llvm/lib/clang/17 -internal-isystem /opt/rh/gcc-toolset-13/root/usr/lib/gcc/x86_64-redhat-linux/13/../../../../include/c++/13 -internal-isystem /opt/rh/gcc-toolset-13/root/usr/lib/gcc/x86_64-redhat-linux/13/../../../../include/c++/13/x86_64-redhat-linux -internal-isystem /opt/rh/gcc-toolset-13/root/usr/lib/gcc/x86_64-redhat-linux/13/../../../../include/c++/13/backward -internal-isystem /lus/home/softs/rocm/6.1.2/lib/llvm/lib/clang/17/include -internal-isystem /usr/local/include -internal-isystem /opt/rh/gcc-toolset-13/root/usr/lib/gcc/x86_64-redhat-linux/13/../../../../x86_64-redhat-linux/include -internal-externc-isystem /include -internal-externc-isystem /usr/include -fdeprecated-macro -fdebug-compilation-dir=./test_diretory -ferror-limit 19 -fgnuc-version=4.2.1 -fcxx-exceptions -fexceptions -fcolor-diagnostics -faddrsig -D__GCC_HAVE_DWARF2_CFI_ASM=1 -o /tmp/test-f35f9a.o -x c++ ./test.cc
clang -cc1 version 17.0.0 based upon LLVM 17.0.0git default target x86_64-unknown-linux-gnu
ignoring nonexistent directory "/opt/rh/gcc-toolset-13/root/usr/lib/gcc/x86_64-redhat-linux/13/../../../../x86_64-redhat-linux/include"
ignoring nonexistent directory "/include"
#include "..." search starts here:
#include <...> search starts here:
/opt/rh/gcc-toolset-13/root/usr/lib/gcc/x86_64-redhat-linux/13/../../../../include/c++/13
/opt/rh/gcc-toolset-13/root/usr/lib/gcc/x86_64-redhat-linux/13/../../../../include/c++/13/x86_64-redhat-linux
/opt/rh/gcc-toolset-13/root/usr/lib/gcc/x86_64-redhat-linux/13/../../../../include/c++/13/backward
/lus/home/softs/rocm/6.1.2/lib/llvm/lib/clang/17/include
/usr/local/include
/usr/include
End of search list.
"/lus/home/softs/rocm/6.1.2/lib/llvm/bin/ld.lld" --hash-style=gnu --eh-frame-hdr -m elf_x86_64 -dynamic-linker /lib64/ld-linux-x86-64.so.2 -o a.out /lib/../lib64/crt1.o /lib/../lib64/crti.o /lus/home/softs/rocm/6.1.2/lib/llvm/lib/clang/17/lib/linux/clang_rt.crtbegin-x86_64.o -L/opt/rh/gcc-toolset-13/root/usr/lib/gcc/x86_64-redhat-linux/13 -L/opt/rh/gcc-toolset-13/root/usr/lib/gcc/x86_64-redhat-linux/13/../../../../lib64 -L/lib/../lib64 -L/usr/lib/../lib64 -L/lib -L/usr/lib --enable-new-dtags /tmp/test-f35f9a.o -lstdc++ -lm /lus/home/softs/rocm/6.1.2/lib/llvm/lib/clang/17/lib/linux/libclang_rt.builtins-x86_64.a -lgcc_s -lc /lus/home/softs/rocm/6.1.2/lib/llvm/lib/clang/17/lib/linux/libclang_rt.builtins-x86_64.a -lgcc_s /lus/home/softs/rocm/6.1.2/lib/llvm/lib/clang/17/lib/linux/clang_rt.crtend-x86_64.o /lib/../lib64/crtn.o
$ amdclang++ --gcc-toolchain="${GCC_PATH}" ./test.cc --verbose
AMD clang version 17.0.0 (https://github.com/RadeonOpenCompute/llvm-project roc-6.1.2 24193 669db884972e769450470020c06a6f132a8a065b)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /lus/home/softs/rocm/6.1.2/lib/llvm/bin
Configuration file: /lus/home/softs/rocm/6.1.2/lib/llvm/bin/clang++.cfg
Found candidate GCC installation: /opt/rh/gcc-toolset-13/root/usr/lib/gcc/x86_64-redhat-linux/13
Selected GCC installation: /opt/rh/gcc-toolset-13/root/usr/lib/gcc/x86_64-redhat-linux/13
Candidate multilib: .;@m64
Candidate multilib: 32;@m32
Selected multilib: .;@m64
Found HIP installation: /lus/home/softs/rocm/6.1.2/lib/llvm/bin/../../.., version 6.1.40093
"/lus/home/softs/rocm/6.1.2/lib/llvm/bin/clang-17" -cc1 -triple x86_64-unknown-linux-gnu -emit-obj -mrelax-all -dumpdir a- -disable-free -clear-ast-before-backend -disable-llvm-verifier -discard-value-names -main-file-name test.cc -mrelocation-model static -mframe-pointer=all -fmath-errno -ffp-contract=on -fno-rounding-math -mconstructor-aliases -funwind-tables=2 -target-cpu x86-64 -tune-cpu generic -debugger-tuning=gdb -v -fcoverage-compilation-dir=./test_diretory -resource-dir /lus/home/softs/rocm/6.1.2/lib/llvm/lib/clang/17 -internal-isystem /opt/rh/gcc-toolset-13/root/usr/lib/gcc/x86_64-redhat-linux/13/../../../../include/c++/13 -internal-isystem /opt/rh/gcc-toolset-13/root/usr/lib/gcc/x86_64-redhat-linux/13/../../../../include/c++/13/x86_64-redhat-linux -internal-isystem /opt/rh/gcc-toolset-13/root/usr/lib/gcc/x86_64-redhat-linux/13/../../../../include/c++/13/backward -internal-isystem /lus/home/softs/rocm/6.1.2/lib/llvm/lib/clang/17/include -internal-isystem /usr/local/include -internal-isystem /opt/rh/gcc-toolset-13/root/usr/lib/gcc/x86_64-redhat-linux/13/../../../../x86_64-redhat-linux/include -internal-externc-isystem /include -internal-externc-isystem /usr/include -fdeprecated-macro -fdebug-compilation-dir=./test_diretory -ferror-limit 19 -fgnuc-version=4.2.1 -fcxx-exceptions -fexceptions -fcolor-diagnostics -faddrsig -D__GCC_HAVE_DWARF2_CFI_ASM=1 -o /tmp/test-015d4c.o -x c++ ./test.cc
clang -cc1 version 17.0.0 based upon LLVM 17.0.0git default target x86_64-unknown-linux-gnu
ignoring nonexistent directory "/opt/rh/gcc-toolset-13/root/usr/lib/gcc/x86_64-redhat-linux/13/../../../../x86_64-redhat-linux/include"
ignoring nonexistent directory "/include"
#include "..." search starts here:
#include <...> search starts here:
/opt/rh/gcc-toolset-13/root/usr/lib/gcc/x86_64-redhat-linux/13/../../../../include/c++/13
/opt/rh/gcc-toolset-13/root/usr/lib/gcc/x86_64-redhat-linux/13/../../../../include/c++/13/x86_64-redhat-linux
/opt/rh/gcc-toolset-13/root/usr/lib/gcc/x86_64-redhat-linux/13/../../../../include/c++/13/backward
/lus/home/softs/rocm/6.1.2/lib/llvm/lib/clang/17/include
/usr/local/include
/usr/include
End of search list.
"/lus/home/softs/rocm/6.1.2/lib/llvm/bin/ld.lld" --hash-style=gnu --eh-frame-hdr -m elf_x86_64 -dynamic-linker /lib64/ld-linux-x86-64.so.2 -o a.out /lib/../lib64/crt1.o /lib/../lib64/crti.o /lus/home/softs/rocm/6.1.2/lib/llvm/lib/clang/17/lib/linux/clang_rt.crtbegin-x86_64.o -L/opt/rh/gcc-toolset-13/root/usr/lib/gcc/x86_64-redhat-linux/13 -L/opt/rh/gcc-toolset-13/root/usr/lib/gcc/x86_64-redhat-linux/13/../../../../lib64 -L/lib/../lib64 -L/usr/lib/../lib64 -L/lib -L/usr/lib --enable-new-dtags /tmp/test-015d4c.o -lstdc++ -lm /lus/home/softs/rocm/6.1.2/lib/llvm/lib/clang/17/lib/linux/libclang_rt.builtins-x86_64.a -lgcc_s -lc /lus/home/softs/rocm/6.1.2/lib/llvm/lib/clang/17/lib/linux/libclang_rt.builtins-x86_64.a -lgcc_s /lus/home/softs/rocm/6.1.2/lib/llvm/lib/clang/17/lib/linux/clang_rt.crtend-x86_64.o /lib/../lib64/crtn.o
```

<a id="low-level-primitives"></a>

<a id="adastra-software-stack-libraries-low-level-primitives"></a>

## Low level primitives

All the libraries show below are not guaranteed to be available on Adastra. If you have a strong need for a particular library to be installed by CINES, please notify [svp@cines.fr](mailto:svp%40cines.fr).

| Operation | AMD GPU | Nvidia GPU | x86 CPU |
| --- | --- | --- | --- |
| BLAS/CBLAS (level 1, 2, 3) | rocBLAS (hipBLAS)/cray-libsci_acc | cuBLAS (hipBLAS)/cray-libsci_acc | cray-libsci/Intel MKL/OpenBLAS/AMD BLIS |
| Dense system solvers | rocSOLVER (hipSOLVER)/cray-libsci_acc/Magma/SLATE | cuSOLVER (hipSOLVER)/cray-libsci_acc/Magma/SLATE | cray-libsci/Magma/Intel MKL/OpenBLAS/AMD libFLAME/LAPACK/ScaLAPACK/SLATE |
| Sparse BLAS (level 1, 2, 3) | rocSPARSE (hipSPARSE) | cuSPARSE (hipSPARSE) | Intel MKL |
| Sparse system solvers (preconditioners and geometric or algebraic multigrid solver) | rocALUTION/PETSc/Ginkgo/HYPRE | Nvidia AMGx/PETSc/Ginkgo/HYPRE | Intel MKL/PETSc/HYPRE |
| Discrete Fourier transform | rocFFT (hipFFT)/vkFFT | cuFFT (hipFFT)/vkFFT | cray-fftw/FFTW/Intel MKL |
| Deep learning primitives | MIOpen | cuDNN | Caffe/Uncountable |
| Algorithmic building blocks | rocThrust | Thrust | Thrust/C++ standard library |
| Communication primitives | MPI/RCCL | MPI/NCCL | MPI/PVM |
| Pseudo number generation | rocRAND (hipRAND) | cuRAND (hipRAND) | Uncountable |
| Low level GPU primitives | rocPRIM (hipCUB) | CUB (hipCUB) | - |

**Note**

AMD provides compatibility layers prefixed with `hip` like hipBLAS. These libraries provide a **stable interface** allowing the user to change the backend from rocBLAS to cuBLAS easily. Theses compatibility layers **should** be used instead of the platform specific roc/cuBLAS.

**Note**

Not all the technologies on a row are strictly equivalent.

<a id="miopen"></a>

## MIOpen

If using MIOpen we strongly recommend that you use the environment variables show below. These serves to mitigate the contention that can occur due to the usage of an auto-tunning caching database MIOpen writes in the home directory.

```shell-session
$ export MIOPEN_USER_DB_PATH="/tmp/${USER}-miopen-cache-${SLURM_JOB_ID}"
$ export MIOPEN_CUSTOM_CACHE_DIR="${MIOPEN_USER_DB_PATH}"
```

Or (disable auto-tunning caching entirely, less recommended):

```shell-session
$ export MIOPEN_DEBUG_DISABLE_FIND_DB=1
```

In addition to making large distributed training more scalable, it can prevent issues of the following form:

```
Failed to store record to find-db at </lus/home/<user_path>/.config/miopen//....ufdb.txt>
Ill-formed record: key not found: /lus/home/<user_path>/.config/miopen//....ufdb.txt
```

<a id="mpi"></a>

<a id="adastra-software-stack-libraries-mpi"></a>

## MPI

The provided and thus, **default** and **preferred** MPI implementation on Cray systems such as Adastra is Cray’s MPICH.

<a id="cray-mpich"></a>

<a id="adastra-software-stack-libraries-mpi-cray-mpich"></a>

### Cray MPICH

You will find information regarding Cray MPICH in the `INTRO_MPI(3)` man page or, as Cray tries to mirror some of it’s documentation online, on this URL: <https://cpe.ext.hpe.com/docs/latest/mpt/mpich/index.html>.

Some features of the Cray MPICH implementation are that:

- it supports the MPI 3.2 standard;
- its **GPU aware**, meaning it gives the ability to pass a GPU buffer to the MPI API;
- its **GPU direct**, meaning it has the transparent (few visible artifacts) ability to use RDMA technics between GPUs. This can elide copies.

The Cray compiler wrappers justify the *lack* of the usual MPI compiler wrappers like `mpicc` or similar (which often only add link and header flags). You implicitly link with Cray’s MPICH when you use the Cray compiler wrappers (`cc`, `CC` and `ftn`) instead of the common `mpicc`, `mpicxx` and `mpif90` compiler wrappers. The `cray-mpich` module is automatically loaded when you load a `PrgEnv-*`.

If you bypass the Cray compiler wrappers, you **need to do more work** and risk mixing incompatible libraries or ABI. Use at your own risk the information given below:

| Implementation | Module | Compiler or wrapper | Header Files & Linking |
| --- | --- | --- | --- |
| Cray MPICH | `cray-mpich` | `cc`, `CC`, `ftn` (Cray compiler wrappers) | The wrappers will automatically add the header flags and the linker flags. |
| *Raw* compilers and **GPU-direct** MPI. | First, ensure you have the module loaded. This is implicit to the usage of a `PrgEnv-*` then,  to compile: `-isystem ${CRAY_MPICH_PREFIX}/include`;  to link: `-L${CRAY_MPICH_PREFIX}/lib -lmpi` (add `-lmpifort` for code using MPI in Fortran).  `${PE_MPICH_GTL_DIR_amd_gfx90a} ${PE_MPICH_GTL_LIBS_amd_gfx90a}`. You can change `gfx90a` if needed. |
| *Raw* compilers and **CPU only** MPI. | First, ensure you have the module loaded. This is implicit to the usage of a `PrgEnv-*` then,  to compile: `-isystem ${CRAY_MPICH_PREFIX}/include`;  to link: `-L${CRAY_MPICH_PREFIX}/lib -lmpi` (add `-lmpifort` for code using MPI in Fortran). |

<a id="gpu-aware-gpu-direct"></a>

<a id="adastra-software-stack-libraries-mpi-cray-mpich-gpu-aware"></a>

#### GPU aware & GPU direct

**Warning**

Only the PrgEnv-amd, PrgEnv-cray and PrgEnv-gnu provide a supported GPU aware Cray MPICH.

To use the Cray MPICH’s *GPU-aware* functionality, **the user must load some modules and set an environment variable**. You need to load the `cray-mpich` but know that any `PrgEnv` loads it for you. As an example, with `PrgEnv-cray`:

```shell-session
$ module purge
$ module load cpe/24.07
$ module load craype-accel-amd-gfx90a craype-x86-trento
$ module load PrgEnv-cray
$ module load amd-mixed
$ # This is the environment variable that tells Cray MPICH to enable GPU aware features.
$ export MPICH_GPU_SUPPORT_ENABLED=1
```

If you chose to use the Cray compiler wrappers, make sure you correctly load the modules used to target an architecture. If a `craype-accel-amd-*` module is not loaded, the Cray compiler wrappers wont link with the `mpi_gtl_hsa` library and at runtime, if you set `export MPICH_GPU_SUPPORT_ENABLED=1` you will get an error like that:

```
MPIDI_CRAY_init: GPU_SUPPORT_ENABLED is requested, but GTL library is not linked
```

If you try to pass GPU memory buffer pointer to MPI while `MPICH_GPU_SUPPORT_ENABLED=1` is not set, you will get error such as:

```
0: process_vm_readv: Bad address
0: Assertion failed in file ../src/mpid/ch4/shm/cray_common/cray_common_memops.c at line 461: 0
0: /opt/cray/pe/lib64/libmpi_cray.so.12(MPL_backtrace_show+0x26) [0x14c1063c081b]
...
0: /opt/cray/pe/lib64/libmpi_cray.so.12(+0x1aac125) [0x14c105b5d125]
0: /opt/cray/pe/lib64/libmpi_cray.so.12(PMPI_Allreduce+0xa3b) [0x14c10427fc5b]
0: /opt/cray/pe/lib64/libmpifort_cray.so.12(mpi_allreduce_+0x46) [0x14c102fbc456]
```

```
MPIDI_OFI_do_irecv:Bad addre
```

```
cxil_map: write error
```

<a id="asynchronous-gpu-operations-and-mpi-calls"></a>

##### Asynchronous GPU operations and MPI calls

Some operation that may seem like they are always synchronous may in fact by asynchronous. Namely, `hipMemcpy` or `hipMemset` may be asynchronous unless there can be a side effect from the point of view of the host. For instance on [Nvidia devices](https://docs.nvidia.com/cuda/cuda-driver-api/api-sync-behavior.html#api-sync-behavior__memcpy-sync), `cudaMemset` will be synchronous only when the target memory is pinned host memory. Such host memory can be observed from the host and as such, the `cudaMemset` should produce all its effects before the host can try to observe, that is, before `cudaMemset` returns (for other kind of host memory not related to the GPU, you should use `std::memset`).

Now, there is a slight catch to that, on Adastra’s MI250X nodes, the Trento CPU is able to observe GPU memory (allocated using `hipMalloc`), something which is not common. The Cray MPICH libraries can take advantage of that and initiate transfers from the host to avoid latency in small operations. But this poses a problem because, if an asynchronous operation such as `hipMemset` is scheduled, returns immediately and is followed by a read/modify of the host, the *sequential semantic of* the HIP programming model is violated, and we have a race condition, the host may or may not observe the `hipMemset`.

In the code below, this can lead to the reduce operation returning before the `hipMemset` has ended and produced its side effects, leading to `d_recvbuf` containing only `-NAN`.

```c++
// -1 is 0xF..FF, so -NAN
HIP_CHECK(hipMemset(d_recvbuf, -1, count * sizeof(value_type)));

// HIP memset is async..., we have to barrier.
// HIP_CHECK(hipStreamSynchronize(nullptr));
// HIP_CHECK(hipDeviceSynchronize());

MPI_Reduce(d_sendbuf, d_recvbuf, count,
           MPI_INT,
           MPI_SUM, 0, MPI_COMM_WORLD);
```

Arguably this is a bug in ROCm, the runtime should, if it detects the Trento 7A53, ensure than `hipMemset` and alike are synchronous.
A solution is to always use the `Async` version of function and explicitly call a barrier (`StreamSynchronize` or `DeviceSynchronize`) this way you avoid the shenanigans of the **might**, **could be** and other potentiality of the underlying implementation semantic and only manipulate operation that are simple to understand and reason with.

More detail is given here: <https://github.com/ROCm/hip/issues/3869>

<a id="id2"></a>

#### Some environment variables

<a id="performance"></a>

##### Performance

| Feature/flag/environment variable | Explanation |
| --- | --- |
| `export MPICH_GPU_IPC_THRESHOLD=1` | Always use device-device copies regardless of the p2p transfer size. Helps lower the latency. |
| `export MPICH_GPU_ALLREDUCE_BLK_SIZE=134217728` | Large GPU kernel staging buffer improving large single node allreduce performance. |
| `export HSA_ENABLE_SDMA=0` | Disabling SDMA engines in favor of copy kernels improves maximum throughput by utilizing more inter GCD xGMI3 links. |

<a id="miscellaneous"></a>

##### Miscellaneous

| Feature/flag/environment variable | Explanation |
| --- | --- |
| `export MPICH_VERSION_DISPLAY=1` | If enabled, causes MPICH to display the Cray MPI version number as well as build date information. |
| `export MPICH_ENV_DISPLAY=1` | If set, causes rank 0 to display all MPICH environment variables and their current settings at MPI initialization time. |
| `export MPICH_MEMORY_REPORT=3` | If set to 1, print a summary of the min/max high water mark and associated rank to stderr. If set to 2, output each rank’s high water mark to a file as specified using `${MPICH_MEMORY_REPORT_FILE}`. If set to 3, do both 1 and 2. |
| `export MPICH_ABORT_ON_ERROR=1` | If enabled, causes MPICH to abort and produce a core dump when MPICH detects an internal error. Note that the core dump size limit (usually 0 bytes by default) must be reset to an appropriate value in order to enable coredumps. |
| `export MPICH_CPUMASK_DISPLAY=1` | Dump the cpuset associated to each rank (verbose). |
| `export MPICH_MPIIO_HINTS_DISPLAY=1` | If enabled, causes rank 0 in the participating communicator to display the names and values of all MPI-IO hints that are set for the file being opened with the `MPI_File_open` call. |
| `export MPICH_OFI_VERBOSE=1` | If set, more verbose output will be displayed during `MPI_Init` to verify which libfabric provider has been selected, along with the name and address of the NIC being used. This may be helpful for debugging errors encountered during `MPI_Init`. |
| `export MPICH_OFI_NIC_VERBOSE=[0-2]` | If set to 1, verbose information pertaining to NIC selection is printed at the start of the job. All available NIC domain names, addresses and index values are displayed. Setting this variable to 2 displays additional details, including the specific NIC each rank has been assigned, which is based on `${MPICH_OFI_NIC_POLICY}`. |
| `export MPICH_OFI_NIC_POLICY=NUMA` | Advanced,should be left undefined or set to NUMA.See `man intro_mpi`. |
| `export MPICH_OFI_CXI_COUNTER_REPORT=[0-5]` | Determines if Cassini (CXI) counters are collected during the application and the verbosity of the counter data report displayed during `MPI_Finalize`. |
| `export MPICH_OFI_CXI_COUNTER_VERBOSE=1` | If set to a non-zero value, this enables more verbose output about the Cassini counters being collected. Can be helpful for debugging and/or identifying which counters are being collected. Only applicable to Slingshot 11. |
| `export FI_LOG_LEVEL=[debug|info|race|warn]` | Controls the amount of logging data that is output. |
| `export FI_CXI_RX_MATCH_MODE=hybrid` | Use this for flow control or queue exhaustion problems. We are seeing a lot of these when a burst of communication occurs, and that there are too many incoming data without a recv operation to match against, yet. This is why it is often advised to post recv before sends. |
| `export MPICH_SINGLE_HOST_ENABLED=0` | When all the ranks are on the same node, forces the traffic through the NIC instead of using node local optimization (shared memory). |
| `export MPICH_SMP_SINGLE_COPY_MODE=NONE` | Disable P2P IPC for CPU to CPU, CPU to GPU and GPU to GPU. |
| `export MPICH_ASYNC_PROGRESS=1` | Spawn a thread that will make progress without you having to call MPI_Test/MPI_Wait or variants but at the cost of some overhead. |

Further reading: `man intro_mpi`.

<a id="id3"></a>

#### Miscellaneous

- Messages such as `MPICH Slingshot Network Summary: 9 network timeouts` signal that packets have be retransmitted. Generally, HPC fabric are lossless, they do not drop packets (say infiniband), except when bit error occurs. These timeout on not necessarily an issue on a SlingShot fabric. Check `MPICH_OFI_CXI_COUNTER_REPORT` for a detailed counter report.
- `MPI_LONG_DOUBLE` is not supported by `cray-mpich`.
- There is a low limit to the tag identifier you can use: <https://cpe.ext.hpe.com/docs/24.07/mpt/mpich/intro_mpi.html#maximum-tag-value-varies-with-network-interconnect>

<a id="using-mpi-in-fortran-a-code"></a>

### Using MPI in Fortran a code

Some remarks from the MPI 3.0 forum meetings:

- Use of `mpif.h` provides no type checking and should only be used for very, very legacy codes;
- The `use mpi` module is impossible to fully implement in a standards-compliant way;
- Very scary issues with compiler optimizations when using `mpif.h`:
  :   - Compiler may copy buffers used with nonblocking communication;
      - Compiler can move code statements surrounding MPI_WAIT calls.
- Existing `use mpi` module with full compile time argument checking;
- New `use mpi_f08` module with typed MPI handles;
  :   - MPI_Comm, MPI_Datatype, MPI_Errhandler, MPI_Info, MPI_Request, …etc.;
      - Array subsections supported;
      - The IERROR argument in Fortran calls is optional;
      - Formal guidance provided to users how to use non-blocking MPI functionality.

<a id="detecting-if-mpi-is-gpu-aware"></a>

### Detecting if MPI is GPU aware

As far as we know, there is no standard way to detect if a MPI implementation is GPU aware, even across MPI extension (MPIx). We propose the following GPU aware MPI check implementation that should work for recent OpenMPI and Cray MPICH.

**Note**

There is an issue on the official MPI standardization committee forum: <https://github.com/mpi-forum/mpi-issues/issues/580>; but note that it will take quite come time before it is implemented universally.

The client code would look like that:

```c++
#include <mpi.h>

#include <iostream>

#include "mpi_gpu_aware.h"

int main(int argc, char** argv) {
    ::MPI_Init(&argc, &argv);

#if defined(MPI_GPU_AWARE_API_SUPPORT)
    std::cout << "[compiletime] Is MPI GPU aware API supported: true\n";
#else
    std::cout << "[compiletime] Is MPI GPU aware API supported: false\n";
#endif

#if defined(MPI_GPU_AWARE_POTENTIAL_SUPPORT)
    std::cout << "[compiletime] Can MPI GPU aware be assumed: true\n";
#else
    std::cout << "[compiletime] Can MPI GPU aware be assumed: false\n";
#endif

    std::cout << "[runtime]     Is MPI GPU aware:               " << ((::mpi_gpu_aware() < 0) ? "false" : "true") << "\n";

    ::MPI_Finalize();
    return 0;
}
```

The `mpi_gpu_aware.h` code is:

```c++
#ifndef MPI_GPU_AWARE_H
#define MPI_GPU_AWARE_H

#include <mpi.h>

#if defined(CRAY_MPICH_VERSION) && defined(MPIX_GPU_SUPPORT_CUDA)
    #define MPI_GPU_AWARE_CRAYMPICH_API_SUPPORT       1
    #define MPI_GPU_AWARE_CRAYMPICH_POTENTIAL_SUPPORT 1

#elif defined(OPEN_MPI)

    #include <mpi-ext.h>

    #if(defined(OMPI_HAVE_MPI_EXT_ROCM) && OMPI_HAVE_MPI_EXT_ROCM) || \
        (defined(OMPI_HAVE_MPI_EXT_CUDA) && OMPI_HAVE_MPI_EXT_CUDA)

        #define MPI_GPU_AWARE_OPENMPI_API_SUPPORT 1

        #if defined(MPIX_CUDA_AWARE_SUPPORT) && MPIX_CUDA_AWARE_SUPPORT
            #define MPI_GPU_AWARE_OPENMPI_POTENTIAL_SUPPORT 1
        #endif
    #endif
#endif

#if defined(MPI_GPU_AWARE_CRAYMPICH_API_SUPPORT) || \
    defined(MPI_GPU_AWARE_OPENMPI_API_SUPPORT)

    /// The MPI implementation supports a runtime API we can use to ensure GPU
    /// awareness.
    ///
    #define MPI_GPU_AWARE_API_SUPPORT 1
#endif

#if defined(MPI_GPU_AWARE_CRAYMPICH_POTENTIAL_SUPPORT) || \
    defined(MPI_GPU_AWARE_OPENMPI_POTENTIAL_SUPPORT)

    /// We assume it is likely that the MPI implementation is GPU aware ?
    ///
    #define MPI_GPU_AWARE_POTENTIAL_SUPPORT 1
#endif

/// GPU aware MPI is a runtime decision on Cray MPICH. It relies on a library
/// called GPU Transport Layer (GTL). This library is linked by the wrapper when
/// a GPU architecture module is loaded (i.e.: craype-x86-trento).
/// It is not possible to determine at compile time if the MPI implementation
/// will be GPU aware. We can know if the MPI could have that feature enabled,
/// but not if it will be enabled.
/// Returns: < 0 if we could not determine if the MPI is GPU aware.
///
extern "C" int mpi_gpu_aware(void);

#endif
```

The `mpi_gpu_aware.cc` code is:

```c++
#include <cstdlib>

#include "mpi_gpu_aware.h"

namespace detail {

    static inline int
    EnsureMPIIsInitialized() {
        int is_mpi_initialized = 0;

        if((::MPI_Initialized(&is_mpi_initialized) != MPI_SUCCESS) ||
        (is_mpi_initialized == 0)) {
            return -1;
        }

        // At this point MPI should be initialized. Except if an other thread
        // called MPI_Finalize() in between.

        return 0;
    }

#if defined(MPI_GPU_AWARE_CRAYMPICH_API_SUPPORT)
    static inline int
    getenv() {
        const char* environment_string = std::getenv("MPICH_GPU_SUPPORT_ENABLED");
        if(environment_string == NULL) {
            return -1;
        }

        if(environment_string[0] != '1') {
            return -1;
        }

        return 0;
    }

    /// Rely on MPIX_GPU_query_support. It requires that we have
    /// MPIX_GPU_SUPPORT_CUDA defined to plug into the MPIX_GPU_query_support.
    /// https://www.mpich.org/static/docs/v4.0.x/www3/MPIX_GPU_query_support.html
    ///
    static inline int
    MPIx() {
        int result = 0;

        const auto CheckGPUKindSupport = [](int offset, int gpu_kind) -> int {
            int is_gpu_kind_supported = 0;

            if(::MPIX_GPU_query_support(gpu_kind, &is_gpu_kind_supported) != MPI_SUCCESS) {
                return -1;
            }

            return is_gpu_kind_supported << offset;
        };

    #if defined(MPIX_GPU_SUPPORT_CUDA)
        result |= CheckGPUKindSupport(0, MPIX_GPU_SUPPORT_CUDA);
    #endif

    #if defined(MPIX_GPU_SUPPORT_ZE)
        result |= CheckGPUKindSupport(1, MPIX_GPU_SUPPORT_ZE);
    #endif

    #if defined(MPIX_GPU_SUPPORT_HIP)
        result |= CheckGPUKindSupport(2, MPIX_GPU_SUPPORT_HIP);
    #endif
        return result == 0 ? -1 : result;
    }

    static inline int
    DoCheck() {
        if(getenv() < 0) {
            return -1;
        }

        if(EnsureMPIIsInitialized() < 0) {
            return -1;
        }

        if(MPIx() < 0) {
            return -1;
        }

        return 0;
    }

#elif defined(MPI_GPU_AWARE_OPENMPI_API_SUPPORT)
    static inline int
    MPIx() {
        int result = 0;

    #if defined(MPI_GPU_AWARE_OPENMPI_API_SUPPORT) && defined(OMPI_HAVE_MPI_EXT_CUDA)
        if(::MPIX_Query_cuda_support() != 1) {
            return -1;
        }
        result |= 1 << 0;
    #endif

        // #if defined(MPI_GPU_AWARE_OPENMPI_API_SUPPORT) && defined(OMPI_HAVE_MPI_EXT_ZERO)
        //         if(::MPIX_Query_zero_support() != 1) {
        //             return -1;
        //         }
        //         result |= 1 << 2;
        // #endif

    #if defined(MPI_GPU_AWARE_OPENMPI_API_SUPPORT) && defined(OMPI_HAVE_MPI_EXT_ROCM)
        if(::MPIX_Query_rocm_support() != 1) {
            return -1;
        }
        result |= 1 << 2;
    #endif

        return result == 0 ? -1 : result;
    }

    static inline int
    DoCheck() {
        if(EnsureMPIIsInitialized() < 0) {
            return -1;
        }

        if(MPIx() < 0) {
            return -1;
        }

        return 0;
    }
#elif !defined(MPI_GPU_AWARE_API_SUPPORT)
    static inline int
    DoCheck() {
        return -1;
    }
#endif
} // namespace detail

extern "C" int mpi_gpu_aware(void) {
    static const int result = detail::DoCheck();
    return result;
}
```

<a id="mpi4py"></a>

### mpi4py

**Note**

You may benefit from using a Python virtual environment, check [this document](../tools/index.md#adastra-software-stack-tools-python-virtual-environment) on how to setup one.

You can compile mpi4py on Adastra using the script below.

```shell
#!/bin/bash

set -eu

module purge

module load cpe/24.07
module load craype-accel-amd-gfx90a craype-x86-trento # For a GPU aware MPI
# module load craype-x86-rome # For a CPU only MPI
module load PrgEnv-gnu
# module load PrgEnv-cray

module load amd-mixed/6.1.2 # For a GPU aware MPI
module load cray-python

module list

# If you use a Virtual Environment (VEnv):
# - deactivate it before loading modules;
# - activate it after loading modules like so:
# source ./python_environment/bin/activate
# - ensure you have installed PyTorch for the correct GPUs.

export MPI4PY_BUILD_MPICC="cc"

pip3 install Cython
pip3 install --verbose --no-binary=mpi4py --compile --no-cache-dir --no-build-isolation mpi4py
```

**Warning**

This script build with support for a GPU aware MPI. If you do not need that feature, please comment the `amd-mixed` module and change the `craype-` modules.

<a id="opencl"></a>

## OpenCL

API providers such as `libintelocl.so` for Intel (CPU) or `libamdocl64.so` for AMD ROCm (GPU) can be explicitly linked against your applications or implicitly through the OpenCL ICD loader.

**Note**

It is recommended to rely on the [OpenCL ICD loader](https://github.com/KhronosGroup/OpenCL-ICD-Loader) to manage OpenCL API providers.

You can use an ICD loader by loading this module:

```shell-session
$ module load opencl-icd-loader
```

The ICD loader(s) are always represented by a shared library named `libOpenCL.so`, and this is against this library that you should link if you want to use the ICD loader.

Alternatively, you can explicitly link against a vendor’s API. That would be `libintelocl.so` for Intel (CPU) or `libamdocl64.so` for AMD ROCm (GPU).

On AMD GPUs supported by ROCm you only have to load the ICD loader and ROCm modules.

```shell-session
$ module load opencl-icd-loader
$ module load rocm
$ clinfo
...
```

On CPU, we recommend the Intel OpenCL backend which can be used like so:

```shell-session
$ module load opencl-icd-loader
$ module load intel-oneapi-compilers
$ export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:${INTEL_ONEAPI_COMPILERS_ROOT}/tbb/latest/lib"
```

<a id="debugging-the-icd-loader"></a>

### Debugging the ICD loader

You may find this [resource of use if you are new to OpenCL](https://bashbaug.github.io/opencl/2019/07/06/OpenCL-On-Linux.html).

To debug the ICD loader’s doing, you can use [this variable](https://github.com/KhronosGroup/OpenCL-ICD-Loader?tab=readme-ov-file#table-of-debug-environment-variables):

```shell-session
$ export OCL_ICD_ENABLE_TRACE="True"
```

<a id="openmp"></a>

## OpenMP

<a id="id4"></a>

### CPU

| Implementation | Compiler or wrapper | Header Files & Linking |
| --- | --- | --- |
| Compiler specific OpenMP | `cc`, `CC`, `ftn` (Cray compiler wrappers) | To compile: `-fopenmp`;  to link: `-fopenmp`. |
| *Raw* compilers. For CCE, AMD, GCC. |

**Note**

You may observe the `-openmp` flag in CMake logs or other documentation. In the CPE context, it is an alias to `-fopenmp`.

**Note**

As of 2023/06/01, the Cray compiler provides full OpenMP 4.5 support and and near complete OpenMP 5.0 and 5.1 support (as it depends on [Clang’s OpenMP support](https://clang.llvm.org/docs/OpenMPSupport.html)). The OpenMP version reported to C and C++ codes thanks to the `_OPENMP` preprocessor definition is `201811` which means version 5.0.

<a id="gpu-offload"></a>

### GPU offload

This section shows how to compile with OpenMP Offload using the different compilers covered above.

Understand that if you use the wrappers, the only action you need to take is to load a `craype-accel-amd-*` module. It will instruct the wrapper to add the proper flags.

**Warning**

(When you use the Cray **Fortran** compiler) You must the `ftn` wrapper to use OpenMP/OpenACC GPU offload. Using the raw `crayftn` will **not** work.

| Compiler or wrapper | Header Files & Linking |
| --- | --- |
| `cc`, `CC`, `ftn` (Cray compiler wrappers) | To compile: `-fopenmp`;  to link: `-fopenmp`. |
| *Raw* compilers. For CCE, AMD. | To compile: `-fopenmp --offload-arch=<hardware>`;  to link: `-fopenmp --offload-arch=<hardware>`. |

With `<hardware>` set to `gfx90a` (MI200) or `gfx942` (MI300).

**Warning**

Do not forget adding optimization flags such as `-O3` to the compiler **and** link commands, to ensure the compiler produces optimized GPU code. While this is not required when building HIP code (it is implicit even if you specify `-O0`), by default the LLVM based compiler will not optimized OpenMP target GPU code.

**Warning**

(When using CCE + `craype-accel-amd-*`) CMake is known to have some issues with Cray’s GPU offload implementation’s special linker (`cce_omp_offload_linker`). This causes link time issues or false positive (running on GPU). Check [this document](../tools/index.md#adastra-software-stack-tools-building-cmake-example-openmp) work around this problem.

When using OpenMP through `amdclang`/`hipcc` or `flang`/`clang` itself, some flags can be used to help the compiler generate quality machine code. These flags could be of help:

```
-Rpass=openmp-opt -Rpass-missed=openmp-opt -Rpass-analysis=openmp-opt
# Enables inter-procedural optimization of kernels. Mandatory for
# performance if your kernel code span multiples translation units.
-foffload-lto
-fopenmp-target-fast enables:
    # Assume no ICVs governing the work sharing schedule, tasking and nested
    # parallelism.
    -fopenmp-target-ignore-env-vars
    # Assume no ICVs modification, tasking or nested parallelism.
    -fopenmp-assume-no-thread-state
    # Ignore nested parallelism possibility, which would be serialized on
    GPU anyway.
    -fopenmp-assume-no-nested-parallelism
# Assumes that when collapsing loops, the resulting index will not overflow
# a 32 bits integer. By default it first casts to 64 bits integers.
-fopenmp-optimistic-collapse
# Disable variable globalization. The OpenMP standard mandates that threads
# can observe an other thread's variable. This does not map well to the GPU
# hardware. This flags enforce thread local behavior that CUDA/HIP offers.
-fopenmp-cuda-mode
# Tells the compiler that nowhere a loop distributed over the teams will
# need more teams than what was implied or specified in num_teams().
-fopenmp-assume-teams-oversubscription
# Same as -fopenmp-assume-teams-oversubscription but for num_threads().
-fopenmp-assume-threads-oversubscription
-fopenmp-offload-mandatory
-fopenmp-force-usm
```

**Note**

ROCm’s OpenMP offloading backend bypasses HPI and goes straight to the HSA layer.

**Note**

Cray’s OpenMP offloading backend uses HPI and allocates streams.

<a id="id5"></a>

### Some environment variables

| Feature/flag/environment variable | Explanation |
| --- | --- |
| `export OMP_DISPLAY_ENV=VERBOSE` | Instructs the runtime to display the OpenMP version number and the value of the ICVs. |
| `export OMP_DISPLAY_AFFINITY=TRUE` | Instructs the runtime to display formatted affinity information for all OpenMP threads in the parallel region upon entering the first parallel region. |

Further reading: `man intro_openmp`.

<a id="for-the-cray-openmp-and-openacc-backend-for-gpu-offloading"></a>

#### For the Cray OpenMP and OpenACC backend for GPU offloading

| Feature/flag/environment variable | Explanation |
| --- | --- |
| `export CRAY_ACC_DEBUG=[0-3]` | (Only for OpenACC and OpenMP offload) When the runtime environment variable `${CRAY_ACC_DEBUG}` is set to `1`, `2`, or `3`, CCE writes runtime commentary of accelerator activity to STDERR for debugging purposes; every accelerator action on every PE generates output prefixed with “ACC:”. This may produce a large volume of output and it may be difficult to associate messages with certain routines and/or certain PEs. |

Further reading: `man intro_openmp`, `man intro_openacc`.

<a id="pytorch"></a>

## PyTorch

(Py)Torch is the defacto library for neural network based artificial intelligence.

To ensure competitive performance, take a lock at theses documents: [Installing PyTorch for AMD GPUs](index.md#adastra-software-stack-libraries-pytorch-installing), [RCCL](index.md#adastra-software-stack-libraries-rccl) and [IDRIS’ accelerate wrapper](index.md#adastra-software-stack-libraries-pytorch-accelerate).

<a id="installing-pytorch-for-amd-gpus"></a>

<a id="adastra-software-stack-libraries-pytorch-installing"></a>

### Installing PyTorch for AMD GPUs

By default `pip` will install PyTorch for Nvidia GPU. To use PyTorch for AMD GPUs (ROCm stack), you will have to specify a repository like so:

```shell-session
# For ROCm 5.7
$ pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.7
# For ROCm 6.0
$ pip3 install torch==2.4.1 torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.0
# For ROCm 6.2 (at least 2.5.0 is mandatory for the MI300A)
$ pip3 install torch==2.5.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.2
$ pip3 install torch==2.6.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.2.4
$ pip3 install torch==2.9.1 torchvision --index-url https://download.pytorch.org/whl/rocm6.4
# For ROCm 7.1
$ pip3 install torch==2.10.0 torchvision --index-url https://download.pytorch.org/whl/rocm7.1
```

**Note**

To install pre-release, you can use the following url for pip: `https://download.pytorch.org/whl/test/` or, for conda: `https://anaconda.org/pytorch-test`.

**Note**

You may benefit from using a Python virtual environment, check [this document](../tools/index.md#adastra-software-stack-tools-python-virtual-environment) on how to setup one.

<a id="building-dependencies"></a>

### Building dependencies

Many produce extend PyTorch, like Apex, Flash-attention etc.. These need to be built for AMD GPUs and we provide recipes for them.

**Warning**

If you build dependencies (say, flash-attention), we strongly recommend using a ROCm version (introduced into your environment using the `amd-mixed` or `rocm` modules) **similar** to the one used by PyTorch. For instance, if you use `torch==2.5.0+rocm6.2`, use `amd-mixed/6.2.1` or `rocm/6.2.1`.

<a id="torch-elastic"></a>

### Torch elastic

**Note**

If you only use a tiny amount of resource, [this document](../../user_support/index.md#adastra-running-jobs-small-job) will give you recommendations on how to use the compute resources.

To make use of PyTorch’s distributed features, you can take example from the script below.

```shell
#!/bin/bash
#SBATCH --account=<account_to_charge>
#SBATCH --job-name="<job_name>"
#SBATCH --constraint=MI250
#SBATCH --nodes=2
#SBATCH --exclusive
#SBATCH --time=1:00:00

module purge

module load cray-python
# For ROCm 5
# module load aws-ofi-rccl/1.4.0
# For ROCm 6
module load aws-ofi-rccl/1.4.0_rocm6

module list

# If you use a Virtual Environment (VEnv):
# - deactivate it before loading modules;
# - activate it after loading modules like so:
# source ./python_environment/bin/activate
# - ensure you have installed PyTorch for the correct GPUs.

# NOTE: We recommend that you prefetch your datasets and models on login
# nodes and use the HF_HOME or the DS_DIR environment variable.
# export HF_HOME="${WORKDIR}/USER_DSDIR"
export HF_HUB_OFFLINE=1

export MIOPEN_USER_DB_PATH="/tmp/${USER}-miopen-cache-${SLURM_JOB_ID}"
export MIOPEN_CUSTOM_CACHE_DIR="${MIOPEN_USER_DB_PATH}"

################################################################################
# Run
################################################################################

srun --ntasks-per-node=1 --gpus-per-task=8 --cpu-bind=none --mem-bind=none --label \
    -- torchrun --nnodes="${SLURM_JOB_NUM_NODES}" --nproc_per_node="8" \
    --rdzv-id="${SLURM_JOB_ID}" \
    --rdzv-backend=c10d \
    --rdzv-endpoint="$(scontrol show hostname "${SLURM_JOB_NODELIST}" | head -n 1):29400" \
    --max-restarts="0" \
    -- ./script.py
```

**Note**

`nproc_per_node` should be equal to `gpus-per-task`. This is because `torchrun` will spawn `nproc_per_node` child processes, each with its own GPU. This explains why we have `ntasks-per-node=1`. We only run one `torchrun` task per node.

**Note**

The `LOGLEVEL="INFO"` environment variable may clutter the log. You can comment them if wanted.

<a id="adastra-software-stack-libraries-pytorch-accelerate"></a>

<a id="idris-accelerate-wrapper"></a>

### IDRIS’ `accelerate` wrapper

IDRIS provides a wrapper abstracting the task scheduler (say, SLURM) and the parallelization framework (PyTorch’s DDP or FSDP, Microsoft’s DeepSpeed) through HuggingFace’s Accelerate. A typical installation can be done like so:

```shell-session
$ pip3 install transformers deepspeed accelerate datasets torchmetrics idr-torch idr_accelerate
```

**Warning**

Be careful with the `torch` package. Ensure, you still have the ROCm version at the end of every install.

**Note**

You may benefit from using a Python virtual environment, check [this document](../tools/index.md#adastra-software-stack-tools-python-virtual-environment) on how to setup one.

To use `idr_accelerate`, we provide a example script below. It will run an example script given in: <https://github.com/idriscnrs/idr_accelerate/blob/main/examples/multi-node/train_accelerate.py>, provided you have downloaded the dataset and model configuration.

```shell
#!/bin/bash
#SBATCH --account=<account_to_charge>
#SBATCH --job-name="<job_name>"
#SBATCH --constraint=MI250
#SBATCH --nodes=2
#SBATCH --exclusive
#SBATCH --time=1:00:00

module purge

module load cray-python
# For ROCm 5
# module load aws-ofi-rccl/1.4.0
# For ROCm 6
module load aws-ofi-rccl/1.4.0_rocm6

module list

# If you use a Virtual Environment (VEnv):
# - deactivate it before loading modules;
# - activate it after loading modules like so:
# source ./python_environment/bin/activate
# - ensure you have installed PyTorch for the correct GPUs.

# NOTE: We recommend that you prefetch your datasets and models on login
# nodes and use the HF_HOME or the DS_DIR environment variable.
# export HF_HOME="${WORKDIR}/USER_DSDIR"
export HF_HUB_OFFLINE=1

export MIOPEN_USER_DB_PATH="/tmp/${USER}-miopen-cache-${SLURM_JOB_ID}"
export MIOPEN_CUSTOM_CACHE_DIR="${MIOPEN_USER_DB_PATH}"

################################################################################
# Run
################################################################################

srun --ntasks-per-node=1 --gpus-per-task=8 --cpu-bind=none --mem-bind=none --label \
    -- idr_accelerate train_accelerate.py \
    --lr 0.5 \
    --model_dir="..." \
    --data_path="..."
```

**Note**

The `LOGLEVEL="INFO"` environment variable may clutter the log. You can comment them if wanted.

<a id="distributed-training"></a>

### Distributed training

Adastra is a parallel machine and you should make use of that fact to distributed your workload onto many nodes. The neural network AI community is very fond of such distributed training.

Distributing a model is very situational, can be tricky and require deeper knowledge of how models work, but the benefit can be tremendous. CINES recommends that you try to maximize Hardware Flop Utilization (HFU) and be aware of Model Flop Utilization (MFU). A decent introduction to distributed training is given here <https://nanotron-ultrascale-playbook.static.hf.space/dist/index.html#5d_parallelism_in_a_nutshell>

<a id="id6"></a>

### Some environment variables

| Feature/flag/environment variable | Explanation |
| --- | --- |
| `export LOGLEVEL="INFO"` | PyTorch logging level. |
| `export MIOPEN_USER_DB_PATH=/tmp/${USER}-miopen-cache-${SLURM_JOB_ID}`  `export MIOPEN_CUSTOM_CACHE_DIR=${MIOPEN_USER_DB_PATH}` | Prevent the ranks from starving the filesystem, trying to atomically update a SQLite database. |
| `export TORCHINDUCTOR_FORCE_DISABLE_CACHES="1"` | Disable PyTorch compilation cache. |
| `export ROCBLAS_INTERNAL_FP16_ALT_IMPL="1"` | Emulate denormal computation. |
| `export MIOPEN_DEBUG_CONVOLUTION_ATTRIB_FP16_ALT_IMPL="1"` | Emulate denormal computation. |

Due to the denormal flushing of FP16 data types on CDNA2, some unstable model will fail to converge. You can choose, at the cost of performance, to enable software denormal computation by defining the following environment variables: `ROCBLAS_INTERNAL_FP16_ALT_IMPL` and `MIOPEN_DEBUG_CONVOLUTION_ATTRIB_FP16_ALT_IMPL`. If your model is so unstable that they fail to converge without denormals, and because the variables above will lower performance, we recommend instead that you use BF16 or FP16 with loss scaling.

<a id="debugging-parallel-loops"></a>

### Debugging parallel loops

Typically, torch run silence the error when a process crashes, for instance you would get:

```
0: E0909 13:42:06.141000 23158946920256 torch/distributed/elastic/multiprocessing/api.py:833] failed (exitcode: -11) local_rank: 0 (pid: 2125406) of binary: ...<redacted>.../python_environment/bin/python
0: Traceback (most recent call last):
0:   File "...<redacted>.../python_environment/bin/torchrun", line 10, in <module>
0:     sys.exit(main())
0:              ^^^^^^
0:   File "...<redacted>.../python_environment/lib/python3.11/site-packages/torch/distributed/elastic/multiprocessing/errors/__init__.py", line 348, in wrapper
0:     return f(*args, **kwargs)
0:            ^^^^^^^^^^^^^^^^^^
0:   File "...<redacted>.../python_environment/lib/python3.11/site-packages/torch/distributed/run.py", line 901, in main
0:     run(args)
0:   File "...<redacted>.../python_environment/lib/python3.11/site-packages/torch/distributed/run.py", line 892, in run
0:     elastic_launch(
0:   File "...<redacted>.../python_environment/lib/python3.11/site-packages/torch/distributed/launcher/api.py", line 133, in __call__
0:     return launch_agent(self._config, self._entrypoint, list(args))
0:            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
0:   File "...<redacted>.../python_environment/lib/python3.11/site-packages/torch/distributed/launcher/api.py", line 264, in launch_agent
0:     raise ChildFailedError(
0: torch.distributed.elastic.multiprocessing.errors.ChildFailedError:
0: =========================================================
0: ./1.basic.py FAILED
0: ---------------------------------------------------------
0: Failures:
0:   <NO_OTHER_FAILURES>
0: ---------------------------------------------------------
0: Root Cause (first observed failure):
0: [0]:
0:   time      : 2024-09-09_13:42:06
0:   host      : g1002.hostmgmt2000.adastra.cines.fr
0:   rank      : 0 (local_rank: 0)
0:   exitcode  : -11 (pid: 2125406)
0:   error_file: <N/A>
0:   traceback : Signal 11 (SIGSEGV) received by PID 2125406
0: =========================================================
```

This obviously serves no purpose, no information is given and this is very badly designed.

To get more information, you can wrap the main function of the script you try to run using torchrun with: `@torch.distributed.elastic.multiprocessing.errors.record`. You will need to `import torch.distributed.elastic.multiprocessing`.

This will create a way better error:

```
0: Fatal Python error: Segmentation fault
0:
0: Thread 0x0000153df5733740 (most recent call first):
0:   File "...<redacted>.../python_environment/lib/python3.11/site-packages/torch/distributed/distributed_c10d.py", line 3936 in barrier
0:   File "...<redacted>.../python_environment/lib/python3.11/site-packages/torch/distributed/c10d_logger.py", line 79 in wrapper
0:   File "...<redacted>.../test/./1.basic.py", line 308 in Main
0:   File "...<redacted>.../python_environment/lib/python3.11/site-packages/torch/distributed/elastic/multiprocessing/errors/__init__.py", line 348 in wrapper
0:   File "...<redacted>.../test/./1.basic.py", line 373 in <module>
0:
0: Extension modules: numpy._core._multiarray_umath, numpy.linalg._umath_linalg, torch._C, torch._C._fft, torch._C._linalg, torch._C._nested, torch._C._nn, torch._C._sparse, torch._C._special (total: 9)
0: E0909 13:43:29.932000 23358933792576 torch/distributed/elastic/multiprocessing/api.py:833] failed (exitcode: -11) local_rank: 0 (pid: 2125634) of binary: ...<redacted>.../python_environment/bin/python
0: Traceback (most recent call last):
0:   File "...<redacted>.../python_environment/bin/torchrun", line 10, in <module>
0:     sys.exit(main())
0:              ^^^^^^
0:   File "...<redacted>.../python_environment/lib/python3.11/site-packages/torch/distributed/elastic/multiprocessing/errors/__init__.py", line 348, in wrapper
0:     return f(*args, **kwargs)
0:            ^^^^^^^^^^^^^^^^^^
0:   File "...<redacted>.../python_environment/lib/python3.11/site-packages/torch/distributed/run.py", line 901, in main
0:     run(args)
0:   File "...<redacted>.../python_environment/lib/python3.11/site-packages/torch/distributed/run.py", line 892, in run
0:     elastic_launch(
0:   File "...<redacted>.../python_environment/lib/python3.11/site-packages/torch/distributed/launcher/api.py", line 133, in __call__
0:     return launch_agent(self._config, self._entrypoint, list(args))
0:            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
0:   File "...<redacted>.../python_environment/lib/python3.11/site-packages/torch/distributed/launcher/api.py", line 264, in launch_agent
0:     raise ChildFailedError(
0: torch.distributed.elastic.multiprocessing.errors.ChildFailedError:
0: =========================================================
0: ./1.basic.py FAILED
0: ---------------------------------------------------------
0: Failures:
0:   <NO_OTHER_FAILURES>
0: ---------------------------------------------------------
0: Root Cause (first observed failure):
0: [0]:
0:   time      : 2024-09-09_13:43:29
0:   host      : g1002.hostmgmt2000.adastra.cines.fr
0:   rank      : 0 (local_rank: 0)
0:   exitcode  : -11 (pid: 2125634)
0:   error_file: <N/A>
0:   traceback : Signal 11 (SIGSEGV) received by PID 2125634
0: =========================================================
srun: error: g1002: task 0: Exited
```

Now, we see we got a segfault somewhere in `distributed_c10d.py`, with a proper call stack.

<a id="miscellaneous-documents"></a>

### Miscellaneous documents

<https://rocm.docs.amd.com/en/latest/how-to/tuning-guides/mi300x/workload.html#pytorch-tunableop>

<https://rocm.docs.amd.com/en/latest/how-to/tuning-guides/mi300x/workload.html#miopen>
<https://rocm.docs.amd.com/projects/MIOpen/en/latest/conceptual/perfdb.html>

<https://rocm.docs.amd.com/en/latest/how-to/llm-fine-tuning-optimization/multi-gpu-fine-tuning-and-inference.html#fine-tuning-and-inference-using-multiple-accelerators>

<a id="rccl"></a>

<a id="adastra-software-stack-libraries-rccl"></a>

## RCCL

RCCL is AMD’s ROCm stack’s fork of Nvidia’s NCCL. This stands for ROCm Communication Collectives Library (RCCL).

Adastra is built on top of a fast interconnect dubbed Slingshot by Cray. To use this interconnect when doing distributed training, you should load the `aws-ofi-rccl` module which introduces a LibFabric Slingshot shim. Also, you should remove all NCCL or RCCL environment variables that could interfere with the libraries’ inner working (or use them at your own risk). As an example:

```shell
#!/bin/bash
#SBATCH --account=<account_to_charge>
#SBATCH --job-name="<job_name>"
#SBATCH --constraint=MI250
#SBATCH --nodes=2
#SBATCH --exclusive
#SBATCH --time=1:00:00

module purge

module load cray-python
# For ROCm 5
# module load aws-ofi-rccl/1.4.0
# For ROCm <= 6.2 - https://support.hpe.com/hpesc/public/docDisplay?docId=dp00007412en_us&page=user/rccl.html&docLocale=en_US
module load aws-ofi-rccl/1.4.0_rocm6
# For ROCm >= 6.2 and < 7 or if you experience hangs with previous version
# see https://support.hpe.com/hpesc/public/docDisplay?docId=dp00005991en_us&page=user/memory_cache_monitor_settings.html&docLocale=en_US
module load aws-ofi-rccl/1.18.0_rocm6
# For ROCm >= 7
module load aws-ofi-rccl/1.18.0_rocm_7

module list

srun ..
```

**Warning**

If you are using `RCCL` as part of PyTorch or any other product that comes with its own ROCm libraries (`libamdhip64`), you do not need to load a `rocm` or `amd-mixed` module. Else, you should load either `amd-mixed` or `rocm` on which, more details are given in [this document](../../user_support/index.md#adastra-programming-environment-mixing-toolchain).

**Note**

RCCL + aws-ofi-rccl is known not to scale well past 128 MI250X nodes. We are aware that hangs can happen past 256 nodes.

Brian Barrett presents aws-ofi-rccl in [NCCL and libfabric: High-Performance Networking for Machine Learning](https://www.youtube.com/watch?v=CcqpPAscMog).

<a id="debugging-networking-issues"></a>

### Debugging networking issues

In the scripts you may use the following logging environment variables. The logs get be very verbose:

```shell
export NCCL_DEBUG="TRACE"
export NCCL_DEBUG_SUBSYS="ALL"
```

**Note**

To ensure you are using the Slingshot interconnect, define the verbose logging environment variable above and you should find the following lines at the start of the logs: `NCCL INFO NET/OFI Using aws-ofi-rccl 1.4.0`, `NCCL INFO NET/OFI Selected Provider is cxi` and most importantly, the `Libfabric/0/GDRDMA` strings repeated multiple times.

<a id="throughput-and-fabric-tuning"></a>

### Throughput and fabric tuning

The advices given here apply mostly to large communication patterns (typically for models on the order of the billion parameters). You may try for smaller models.

The most simple and effective knobs that you can tune are the following environment variables:

```shell
export NCCL_MIN_NCHANNELS=<>
export NCCL_NSOCKS_PERTHREAD=<>
export NCCL_SOCKET_NTHREADS=<>
```

You can play around with `NCCL_MIN_NCHANNELS`, knowing that the largest value is not always better. For instance, on a MI300A node, we can get 10% better performance by backing off ~35% from the maximum, the maximum is 64 channels but the most performance is seen using 42 channels.

**Warning**

The values below are guidelines observed on real world case and benchmarks, it may not apply at ALL to your application. Note that the higher the number of chanel, the less CU/SM are avaialble for user computations (NCCL launches persistent kernels).

The Memory Registration (MR) Cache Monitor settings control how memory registrations are managed and cached. `FI_MR_CACHE_MONITOR` selects the monitoring mechanism, with `memhooks` currently being the default due to its wide availability; however, it is not the optimal choice for the CXI provider. `kdreg2` is recommended whenever possible, but applications using NCCL or RCCL can require `userfaultfd` (on Adastra it can lead to a crash though!). The `FI_MR_CACHE_MAX_SIZE` parameter defines the maximum cache size in bytes, where `-1` indicates unlimited caching. By default, Libfabric sets this limit to half of the system memory divided by the number of CPUs (`cpu_cnt`), whereas the HPE Cray Programming Environment sets it to unlimited. The `FI_MR_CACHE_MAX_COUNT` parameter specifies the maximum number of cached memory registrations (MRs), with a default of 1024. This value is generally too small for most applications, so increasing it is recommended; the HPE Cray Programming Environment uses a value of 524288.

The endpoint receive size attribute (`FI_CXI_DEFAULT_RX_SIZE`) determines the size of the internal receive command and hardware event queues allocated at job startup, with a default value of 512. It should be configured according to the expected number of outstanding receive buffers posted by the application. Overestimating this value increases memory consumption, while underestimating it can trigger flow control and reduce performance. Similarly, the endpoint transmit size attribute (`FI_CXI_DEFAULT_TX_SIZE`) controls the size of the internal transmit command and hardware event queues, also defaulting to 512. It determines how many messages can be in flight and should therefore be configured according to the expected number of outstanding initiator RDMA operations. Cray MPI uses a value of 1024. The cxi libfabric provider allows a maximum of 16384 outstanding MPI rendezvous messages. Setting this value too high can waste memory and allow an excessive number of messages in flight, potentially overwhelming the endpoint. Conversely, setting it too low can introduce flow control and degrade performance; in some cases, it may even cause deadlocks if an application posts too many transmissions before posting the corresponding receives.

The completion queue size attribute (`FI_CXI_DEFAULT_CQ_SIZE`) specifies the maximum number of entries in the CXI provider completion queue, with a default value of 1024. It should be configured based on the expected number of outstanding RDMA operations to and from a single endpoint. Applications, including MPI implementations, can override the provider’s default value. The default CXI provider configuration is designed to accommodate the combined TX and RX queue sizes; therefore, the completion queue size must not be smaller than the sum of the configured TX and RX values, particularly when these differ from their defaults. Cray MPI sets this parameter to 131072 by default.

The tag matching mode (`FI_CXI_RX_MATCH_MODE`) determines how incoming messages are matched against posted receives. The default hardware mode provides better performance because host-based matching can consume significant CPU resources and memory bandwidth. The hybrid mode is recommended when users are uncertain whether the combined number of unexpected messages and posted receives will exceed the application’s configured hardware receive resource limit, but still want to ensure that the application continues to function when hardware resources are exhausted. Hybrid matching provides greater flexibility and robustness than hardware-only matching. However, it introduces an additional host memory overhead of approximately 8 MB per rank/domain, even if the application never transitions to software-based matching.

A summary from <https://github.com/HewlettPackard/shs-ccl-docs> is given below, these are variales recommended by the constructor:

```shell
# NOTE: NCCL_NET on single-node Slurm forces NCCL to use the network transport even when all ranks share the same node. This may not impact performance.
export NCCL_NET="AWS Libfabric" # (Sanity check) Ensures that RCCL will terminate if it fails to load the Libfabric plugin, preventing an undesirable fallback to sockets.
export NCCL_NET_PLUGIN="librccl-net.so"         # (Perf) Name of the plugin.
export NCCL_NET_GDR_LEVEL="PHB"                 # (Perf) Required to enable RDMA between GPUs.
export NCCL_SOCKET_IFNAME="hsn0,hsn1,hsn2,hsn3" # (Bootstrap) Limits RCCL's bootstrap and socket communication to a specific interface. These should match the interfaces available.
# export NCCL_MIN_NCHANNELS=32                    # (Perf) For multinode runs only, it lowers performance on single node run. This reduces the available compute power of the device.
export NCCL_CROSS_NIC="1"                       # (Scale) Has been found to improve performance on large systems.

export HSA_FORCE_FINE_GRAIN_PCIE="1"    # (Perf) Enable peer-to-peer access to large BAR addressing support.

export FI_MR_CACHE_MONITOR="kdreg2"     # (Crash) Sets the memory cache monitor to detect changes between virtual and physical memory pages. userfaultd leads to a crash on Adastra.
export FI_CXI_DEFAULT_CQ_SIZE="131072"  # (Scale) Should be increased, especially for large jobs.
export FI_CXI_DEFAULT_TX_SIZE="2048"    # (Scale) Should be set especially for large jobs that are dependent on unexpected rendezvous messaging.
export FI_CXI_DISABLE_HOST_REGISTER="1" # (Deadlock) Avoids ROCm allocation calls from the provider that may cause RCCL deadlocks.
# export FI_CXI_RDZV_PROTO="alt_read"     # (Perf) Use the alt_read rendezvous protocol. If used, the user MUST specify the SLURM's srun --network=disable_rdzv_get
# export FI_CXI_RDZV_GET_MIN="0"          # (Perf) Disables the rendezvous get optimization; use with `FI_CXI_RDZV_PROTO=alt_read`.
export FI_CXI_RDZV_EAGER_SIZE="0"       # (Deadlock) Prevents sending data before the receiver is ready.
export FI_CXI_RDZV_THRESHOLD="0"        # (Sanity check) Sets the message size threshold above which the rendezvous protocol is used; setting to `0` forces all messages through the rendezvous path.
export FI_CXI_RX_MATCH_MODE="hybrid"    # (Error) It allows the network stack to transition to software matching if hardware resources are exhausted.
```

**Note**

In theory, `NCCL_MIN_NCHANNELS` is mostly beneficial when you are not using all the xGMI links of a node.

<a id="id7"></a>

#### On MI250X

| Environment variables | When | Value |
| --- | --- | --- |
| `export NCCL_MIN_NCHANNELS=<>` | <= 8 GPUs | 16 |
| > 8 GPUs | 32 |
| > 32 GPUs | 16 |
| `export NCCL_NSOCKS_PERTHREAD=<>` |  | 1 |
| `export NCCL_SOCKET_NTHREADS=<>` |  | 1 |

<a id="id8"></a>

#### On MI300A

| Environment variables | When | Value |
| --- | --- | --- |
| `export NCCL_MIN_NCHANNELS=<>` | <= 4 APUs | 42 |
| > 4 APUs | 32 |
| > 16 APUs | 16 |
| `export NCCL_NSOCKS_PERTHREAD=<>` |  | 1 |
| `export NCCL_SOCKET_NTHREADS=<>` |  | 1 |

Decent tuning of `NCCL_MIN_NCHANNELS` is very significant for MI300 cards.

<a id="rocm"></a>

## ROCm

**Warning**

ROCm is generally backward compatible which means you can use a recent ROCm with a binary built using an older ROCm. It is not forward compatible, meaning using a recent binary using an older ROCm may not work.

<a id="modules-and-paths"></a>

### Modules and paths

The ROCm stack can be used by loading a module providing ROCm.

```shell-session
$ # A standalone ROCm.
$ module load rocm
$ # A standalone ROCm with a Cray compiler in the mix.
$ module load amd-mixed
$ # Or a programming environment.
$ module load PrgEnv-amd
```

The libraries can be found in the `${ROCM_PATH}/lib` directory. Note that the `${ROCM_PATH}` environment variable is defined by the modules given above.

The ROCm libraries provided are:

```
amd_comgr
amd-dbgapi
AMDDeviceLibs
hip
hip-lang
hsa-runtime64

rocm_smi

miopen
rccl

rocalution
rocblas & hipblas
rocfft & hipfft
rocrand & hiprand
rocsolver & hipsolver
rocsparse & hipsparse

rocprim & hipcub
rocthrust
```

AMD is extensively improving its documentation. You can find a trove of example on mixing CMake with ROCm [here](https://rocm.docs.amd.com/en/latest/conceptual/cmake-packages.html).

Starting with ROCm 5.1.0, here are the CMake prefixes for the provided libraries:

```cmake
set(amd_comgr_DIR     "$ENV{ROCM_PATH}/lib/cmake/amd_comgr")
set(AMDDeviceLibs_DIR "$ENV{ROCM_PATH}/lib/cmake/AMDDeviceLibs")
set(hip_DIR           "$ENV{ROCM_PATH}/lib/cmake/hip")
set(hsa-runtime64_DIR "$ENV{ROCM_PATH}/lib/cmake/hsa-runtime64")

set(rocm_smi_DIR      "$ENV{ROCM_PATH}/lib/cmake/rocm_smi")

set(miopen_DIR        "$ENV{ROCM_PATH}/lib/cmake/miopen")
set(rccl_DIR          "$ENV{ROCM_PATH}/lib/cmake/rccl")

set(rocalution_DIR    "$ENV{ROCM_PATH}/lib/cmake/rocalution")
set(rocblas_DIR       "$ENV{ROCM_PATH}/lib/cmake/rocblas")
set(hipblas_DIR       "$ENV{ROCM_PATH}/lib/cmake/hipblas")
set(rocfft_DIR        "$ENV{ROCM_PATH}/lib/cmake/rocfft")
set(hipfft_DIR        "$ENV{ROCM_PATH}/lib/cmake/hipfft")
set(rocrand_DIR       "$ENV{ROCM_PATH}/lib/cmake/rocrand")
set(hiprand_DIR       "$ENV{ROCM_PATH}/lib/cmake/hiprand")
set(rocsolver_DIR     "$ENV{ROCM_PATH}/lib/cmake/rocsolver")
set(hipsolver_DIR     "$ENV{ROCM_PATH}/lib/cmake/hipsolver")
set(rocsparse_DIR     "$ENV{ROCM_PATH}/lib/cmake/rocsparse")
set(hipsparse_DIR     "$ENV{ROCM_PATH}/lib/cmake/hipsparse")

set(rocprim_DIR       "$ENV{ROCM_PATH}/lib/cmake/rocprim")
set(hipcub_DIR        "$ENV{ROCM_PATH}/lib/cmake/hipcub")
set(rocthrust_DIR     "$ENV{ROCM_PATH}/lib/cmake/rocthrust")
```

The CMAke package and component one should link against are:

| Library | CMake package name | CMake component |
| --- | --- | --- |
| HIP | `hip` | `hip::host` |
| rocPRIM | `rocprim` | `roc::rocprim` |
| rocThrust | `rocthrust` | `roc::rocthrust` |
| hipcub | `hipcub` | `hip::hipcub` |
| rocRAND | `rocrand` | `roc::rocrand` |
| rocSOLVER | `rocsolver` | `roc::rocsolver` |
| hipBLAS | `hipblas` | `roc::hipblas` |
| rocFFT | `rocfft` | `roc::rocfft` |
| hipFFT | `hipfft` | `hip::hipfft` |
| rocSPARSE | `rocsparse` | `roc::rocsparse` |
| hipSPARSE | `hipsparse` | `roc::hipsparse` |
| rocALUTION | `rocalution` | `roc::rocalution` |
| RCCL | `rccl` | `rccl` |
| MIOpen | `miopen` | `MIOpen` |
| MIGraphX | `migraphx` | `migraphx::migraphx` `migraphx::migraphx_c` `migraphx::migraphx_cpu`, `migraphx::migraphx_gpu`, `migraphx::migraphx_onnx`, `migraphx::migraphx_tf` |

<a id="build-integration"></a>

<a id="adastra-software-stack-libraries-rocm-integration"></a>

### Build integration

<a id="using-cmake-to-properly-consume-a-rocm-library"></a>

#### Using CMake to properly consume a ROCm library

```cmake
cmake_minimum_required(VERSION 3.5)
cmake_policy(VERSION 3.5...3.27)
project(example LANGUAGES CXX)

add_library(example_library ...)

find_package(miopen)
target_link_libraries(example_library PUBLIC MIOpen)
```

<a id="hip-as-a-cmake-language"></a>

#### HIP as a CMake language

```cmake
cmake_minimum_required(VERSION 3.21) # HIP language support requires 3.21
cmake_policy(VERSION 3.21.3...3.27)
project(example LANGUAGES HIP)

add_executable(example_binary main.hip)

# If you have .cu files, you can tell CMake to treat them as HIP like so:
add_library(example_library library.cu)
set_source_files_properties(library.cu PROPERTIES LANGUAGE HIP)
```

**Note**

`CMAKE_HIP_ARCHITECTURES` is a semicolon variable that defines the targeted devices. Example: `gfx801;gfx900;gfx90a`.

<a id="hip-using-raw-compilers-or-wrappers"></a>

#### HIP using raw compilers or wrappers

**Warning**

Compiling HIP code is different than just using and linking against the HIP runtime. See [Using CMake to properly consume the HIP runtime](index.md#adastra-software-stack-libraries-rocm-integration-cmake-runtime).

**Warning**

If you use `hipcc`, you may want to use the `${HIPCC_COMPILE_FLAGS_APPEND}` and `${HIPCC_LINK_FLAGS_APPEND}` environment variables to specify your flags. Else, the `hipcc` wrapper may ignore them.

This section shows how to compile HIP codes using the Cray compiler wrappers and `hipcc` (itself an `amdclang` wrapper).

**Note**

Make sure the `craype-accel-amd-gfx90a` (or the equivalent MI300A) module is loaded when compiling HIP with the Cray compiler wrappers.

| Compiler | Compile/Link Flags, Header Files, and Libraries |
| --- | --- |
| `CC`  Only with:  `PrgEnv-cray`  `PrgEnv-amd` | First load the `rocm` or `amd-mixed` module then,  to compile: `--rocm-path="${ROCM_PATH}" -xhip`;  to link: `--rocm-path="${ROCM_PATH}" -L"${ROCM_PATH}/lib" -lamdhip64`. |
| `hipcc` | Can be used directly to compile and link with HIP source/object files.  To see what is being invoked within this compiler wrapper, issue the command, `hipcc --verbose`.  To explicitly target AMD MI250X, use `--offload-arch=gfx90a`.  To explicitly target AMD MI300A, use `--offload-arch=gfx942`. |
| `CC` and `hipcc`  With:  `CC` as a non HIP  compiler like  `PrgEnv-gnu`. | The GNU compilers **cannot** be used to compile HIP code, so all HIP kernels must be separated from CPU code.  During compilation, all non-HIP files must be compiled with `CC` while HIP kernels must be compiled with `hipcc`.  Then linking can be performed as done above for the AMD/Cray vendors.  First load the `rocm` or `amd-mixed` module then,  to compile non HIP code: `CC <file.cpp>`;  to compile HIP code: `hipcc --offload-arch=gfx90a` (or `gfx942`);  to link: `CC --rocm-path="${ROCM_PATH}" -L"${ROCM_PATH}/lib" -lamdhip64`. |

The ROCm modules (`rocm` or `amd-mixed`) introduce several environment variables for HIP programming. The command `hipconfig --full` can be used to check some environment related information.

**Warning**

By default, if you do not specify the `--rocm-path="${ROCM_PATH}"`, Clang will take the ROCm install present in `/opt/rocm` or pointed to by the `${ROCM_PATH}` environment variable.

**Warning**

By default `amdclang` (HIP-Clang) and CrayClang (actually all Clang based GPU code compilers) assumes `-ffp-contract=fast-honor-pragmas` (less finicky than `-Ofast`). Users can use `#pragma clang fp contract(on|off|fast)` to control fp contraction of a block of code. For x86_64, FMA is off by default since the generic x86_64 target does not support FMA by default. To turn on FMA on x86_64, either use `-mfma` or `-march=native` on CPUs supporting FMA. When contractions are enabled and the CPU has not enabled FMA instructions, the GPU can produce different numerical results than the CPU for expressions that can be contracted. Tolerance should be used for floating point comparisons. We recommend that you read the HIP Programming Manual or [the clang section on local optimization disabling](https://clang.llvm.org/docs/LanguageExtensions.html#extensions-for-selectively-disabling-optimization).

**Warning**

We do **NOT** recommend that you use `amdclang` directly, always try to use the `hipcc` wrapper instead. that said, if you must use `amdclang`, know that you have to pass the `-isystem "${ROCM_PATH}/include" --hip-device-lib-path="${ROCM_PATH}/amdgcn/bitcode" --rocm-path=${ROCM_PATH}` flags.

An other way to check which flags to use for compilation and linking is to call `hipconfig`. On a ROCm 5.7.1 it could return:

```shell-session
$ hipconfig
HIP version  : 5.7.31921-1949b1621

== hipconfig
HIP_PATH     : /lus/home/softs/rocm/5.7.1
ROCM_PATH    : /opt/rocm-5.7.1
HIP_COMPILER : clang
HIP_PLATFORM : amd
HIP_RUNTIME  : rocclr
CPP_CONFIG   :  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/lus/home/softs/rocm/5.7.1/include -I/lus/home/softs/rocm/5.7.1/llvm/lib/clang/17.0.0

== hip-clang
HIP_CLANG_PATH   : /opt/rocm-5.7.1/llvm/bin
AMD clang version 17.0.0 (https://github.com/RadeonOpenCompute/llvm-project roc-5.7.1 23382 f3e174a1d286158c06e4cc8276366b1d4bc0c914)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /opt/rocm-5.7.1/llvm/bin
AMD LLVM version 17.0.0git
Optimized build.
Default target: x86_64-unknown-linux-gnu
Host CPU: znver4

Registered Targets:
    amdgcn - AMD GCN GPUs
    r600   - AMD GPUs HD2XXX-HD6XXX
    x86    - 32-bit X86: Pentium-Pro and above
    x86-64 - 64-bit X86: EM64T and AMD64
hip-clang-cxxflags :  -isystem "/lus/home/softs/rocm/5.7.1/include" -O3
hip-clang-ldflags  :  -O3 --hip-link --rtlib=compiler-rt -unwindlib=libgcc

=== Environment Variables
PATH=/opt/rocm-5.7.1/bin:/lus/home/BCINES/dci/user/.local/bin:/lus/home/BCINES/dci/user/bin:/opt/clmgr/sbin:/opt/clmgr/bin:/opt/sgi/sbin:/opt/sgi/bin:/usr/share/Modules/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/opt/c3/bin:/sbin:/bin
LD_LIBRARY_PATH=/opt/rocm-5.7.1/lib/roctracer:/opt/rocm-5.7.1/lib/rocprofiler:/opt/rocm-5.7.1/lib
HIP_LIB_PATH=/opt/rocm-5.7.1/lib

== Linux Kernel
Hostname     : login5
Linux login5 4.18.0-477.10.1.el8_8.x86_64 #1 SMP Wed Apr 5 13:35:01 EDT 2023 x86_64 x86_64 x86_64 GNU/Linux
LSB Version:    :core-4.1-amd64:core-4.1-noarch
Distributor ID: RedHatEnterprise
Description:    Red Hat Enterprise Linux release 8.8 (Ootpa)
Release:        8.8
Codename:       Ootpa
```

<a id="hip-openmp-cpu-threading-using-raw-compilers-or-wrappers"></a>

#### HIP + OpenMP CPU threading using raw compilers or wrappers

This section shows how to compile HIP + OpenMP CPU threading hybrid codes. Note that HIP kernels may not appear in translation units with OpenMP support enabled. However, HIP runtime API calls may be used in such previously described translation units.

**Note**

Make sure the `craype-accel-amd-gfx90a` (or the equivalent MI300A) module is loaded when compiling HIP with the Cray compiler wrappers.

| Compiler | Compile/Link Flags, Header Files, and Libraries |
| --- | --- |
| `CC`  Only with:  `PrgEnv-cray`  `PrgEnv-amd` | First load the `rocm` or `amd-mixed` module then,  to compile: `-fopenmp --rocm-path="${ROCM_PATH}" -xhip`;  to link: `-fopenmp --rocm-path="${ROCM_PATH}" -L"${ROCM_PATH}/lib" -lamdhip64`. |
| `hipcc` | First load the `rocm` or `amd-mixed` module then,  to compile: `-fopenmp`;  to link: `-fopenmp`.  To explicitly target AMD MI250X, use `--offload-arch=gfx90a`.  To explicitly target AMD MI300A, use `--offload-arch=gfx942`. |
| `CC` and `hipcc`  With:  `CC` as a non HIP  compiler like  `PrgEnv-gnu`. | The GNU compilers **cannot** be used to compile HIP code, so all HIP kernels must be separated from OpenMP CPU code.  During compilation, all non-HIP files must be compiled with `CC` while HIP kernels must be compiled with `hipcc`.  Then linking can be performed as done above for the AMD/Cray vendors.  First load the `rocm` or `amd-mixed` module then,  to compile non HIP code: `CC -fopenmp`;  to compile HIP code: `hipcc --offload-arch=gfx90a` (or `gfx942`);  to link: `CC -fopenmp --rocm-path="${ROCM_PATH}" -L"${ROCM_PATH}/lib" -lamdhip64`. |

<a id="using-cmake-to-properly-consume-the-hip-runtime"></a>

<a id="adastra-software-stack-libraries-rocm-integration-cmake-runtime"></a>

#### Using CMake to properly consume the HIP runtime

Above, we introduced a way to compile `.hip` files. Sometimes you only want to have access to the HIP runtime (say, `hipMalloc`) through the C API. This does not require a special device compiler, we only need the header and libraries. Under CMake it is done like so:

```cmake
cmake_minimum_required(VERSION 3.5)
cmake_policy(VERSION 3.5...3.27)
project(example LANGUAGES CXX)

add_executable(example_binary ...)

find_package(hip REQUIRED)
target_link_libraries(example_binary PRIVATE hip::host)
```

<a id="hip-runtime-using-raw-compilers-or-wrappers"></a>

#### HIP runtime using raw compilers or wrappers

| Compiler/wrapper | Compile/Link Flags, Header Files, and Libraries |
| --- | --- |
| Virtually all. | First load the `rocm` or `amd-mixed` module then,  to compile non HIP code but to include the HIP headers: `--rocm-path="${ROCM_PATH}" -isystem "${ROCM_PATH}/include"`;  to link, the simplest for LLVM based compiler is: `--rocm-path="${ROCM_PATH}" --hip-link`,  to link, the most versatile (e.g. with GNU) is: `--rocm-path="${ROCM_PATH}" -L"${ROCM_PATH}/lib" -lamdhip64`. |

**Warning**

See below about the RDC pitfall.

<a id="relocatable-device-code-rdc"></a>

### Relocatable Device Code (RDC)

If you require RDC directly via `-fgpu-rdc` or implicitly through libraries such as Kokkos (`Kokkos_ENABLE_HIP_RELOCATABLE_DEVICE_CODE`) and you **do not use** `hipcc`, you will have to **link** using the additional `--hip-link` flag.

For now, the only HIP compilers are derivatives of Clang. As such, RDC is only possible if the linker used comes from either the Cray toolchain, the AMD (ROCm stack) toolchain or any Clang with HIP support based compiler.

**Warning**

Failure to specify `-fgpu-rdp --hip-link` at link time, on a RDC compiled set of object file could result in the following error: `error: undefined symbol: __hip_fatbin`.

<a id="c-preprocessor-definitions"></a>

<a id="adastra-software-stack-libraries-rocm-cpreproc"></a>

### C preprocessor definitions

| HIP and CUDA equivalent definitions | Meaning |
| --- | --- |
| `__CUDA__`/`__HIP__` | (For LLVM based compiler **ONLY**) It tels you which language the file is to be interpreted as. Respectively defined if `-x cu` or `-x hip` or if the file extensions are in `.cu` or `.hip`. |
| `__CUDA_ARCH__`/`__HIP_DEVICE_COMPILE__` | It tels you that you are in the GPU code generation pass. It is useful when one want to make use of conditional compilation to distinguish GPU and CPU code paths. Respectively defined if `-x cu` or `-x hip` or if the file extensions are in `.cu` or `.hip`. |
| `__CUDACC__`/`__HIPCC__` | Which compiler is being used to build the code. |
| `__HIP_PLATFORM_NVIDIA__`/`__HIP_PLATFORM_AMD__` | **Should not** be used used as the semantic often is not what one wants. Defined in `hip/hip_common.h` if `__HIP__` is defined. |

We recommend that you use `__CUDACC__` and `__HIPCC__` to discriminate CUDA and HIP implementations. This will work for any known CUDA and HIP compiler.

<a id="id9"></a>

### Some environment variables

| Feature/flag/environment variable | Explanation |
| --- | --- |
| `export AMD_LOG_LEVEL=[0-4]` | `0`: Disable log. `1`: Enable log on error level. `2`: Enable log on warning and below levels. `3`: Enable log on information and below levels. `4`: Decode and display AQL packets. |
| `export AMD_SERIALIZE_COPY=<N>` | `1`: Wait for completion before enqueue. `2`: Wait for completion after enqueue. `3`: Both. |
| `export AMD_SERIALIZE_KERNEL=[0-3]` | `1`: Wait for completion before enqueue. `2`: Wait for completion after enqueue. `3`: Both. |
| `export CUDA_VISIBLE_DEVICES=<N>` | Restrict the devices that your CUDA/HIP application sees. Very important to avoid MPI ranks walking on each other. The AMD runtime supports this environment variable. |
| `export HIP_VISIBLE_DEVICES=<N>` | Same as `${CUDA_VISIBLE_DEVICES}` but for HIP. |
| `export ROCR_VISIBLE_DEVICES=<N>` | Same as `${HIP_VISIBLE_DEVICES}` but works at the HSA level. Recommend for highly tunned applications. It restricts the visibility of `${HIP_VISIBLE_DEVICES}` and `${CUDA_VISIBLE_DEVICES}`. So `ROCR_VISIBLE_DEVICES=2 HIP_VISIBLE_DEVICES=2` is same as hiding all the devices. `HIP_VISIBLE_DEVICES="0,1,2" HIP_VISIBLE_DEVICES="2"` would only show the third device. |
| `export GPU_DEVICE_ORDINAL=<N>` | Same as `${CUDA_VISIBLE_DEVICES}` but for OpenCL and HIP. |
| `export GPU_MAX_HW_QUEUES=<N>` | The variable controls how many independent hardware queues HIP runtime can create per process, per device. If application allocates more HIP streams than this number, then HIP runtime will reuse the same hardware queues for the new streams in round robin manner. Somewhat equivalent to `CUDA_DEVICE_MAX_CONNECTIONS`. |
| `export AMD_DIRECT_DISPATCH=0` | Disable direct dispatch (do not use a special thread to launch the kernels). |
| `export HSA_ENABLE_SDMA=[0-1]` | It causes host-to-device and device-to-host copies to use compute shader blit kernels rather than the dedicated DMA copy engines. It has been shown that high HtoD and DtoH copy throughput can be achieved this way at a cost of less compute power available for computations. |
| `export HIPCC_VERBOSE=[0-1]` | Ask `hipcc` to dump the compiler command it launches (there is also the `--cxxflags` and `--ldflags`). |
| `export HSA_ENABLE_INTERRUPT=0` | Causes completion signals to be detected with memory-based polling, rather than interrupts. |
| `export HSAKMT_DEBUG_LEVEL=7` | ROCM-Thunk log level. |

More details on the AMD GPU debugging options in [this document](https://rocm.docs.amd.com/projects/HIP/en/develop/how_to_guides/debugging.html).

**Note**

While not specific to ROCm, the `--save-temps` option is of the upmost importance when one seeks to dive deeper into the machine and assembly code.

<a id="hip-compiler-flag-details"></a>

### HIP compiler flag details

| Feature/flag/environment variable | Explanation |
| --- | --- |
| `--rocm-path=<value>`/`export ROCM_PATH=<value>` | ROCm installation path, used for deriving the `HIP_PATH`. |
| `--hip-path=<value>`/`export HIP_PATH=<value>` | (Generally not used) (Is automatically derived from the `ROCM_PATH` or the equivalent flag) HIP runtime installation path, used for the HIP include path, and library path (`-L`). |
| `--hip-link` | Instruct LLVM based compilers with HIP support to handle advanced HIP linking. Thus is mandatory for RDC. This implicitly link against the current ROCm’s `amdhip64`. In addition to the RDC shenanigans, it is close to the following option set: `-L"${ROCM_PATH}" -rpath="${ROCM_PATH}/lib" -lamdhip64`. By default, if the LLVM `--rocm-path=` flag is not given, it’ll point to `${ROCM_PATH}/lib/llvm/bin/../../../lib`. |

The source of truth remains [at this location](https://clang.llvm.org/docs/HIPSupport.html#order-of-precedence-for-device-library-path).

<a id="offload-architecture"></a>

### Offload architecture

Values that should be passed to `--offload-arch=` are, in the context of Adastra:

- gfx90a to target the MI250X;
- gfx942 to target the MI300A.

If the HIP runtime cannot find a kernel image that matches the device on which the HIP runtime is *bound* mode of the device, it will fail with `hipErrorNoBinaryForGpu`.

```
"hipErrorNoBinaryForGpu: Unable to find code object for all current devices!"
```

<a id="dumping-assembly-code"></a>

### Dumping assembly code

If you compile HIP code (using `hipcc` or `-xhip`), you can rely on the `--save-temps` flag that all the LLVM based compiler provide. You then have to look for the `<file_name>-hip-amdgcn-amd-amdhsa-<architecture>.s` files, where `<file_name>` is the file the compiler processed and `<architecture>` is the AMD GPU architecture (gfx90a, gfx942, etc.) for example, for a file named `main.cc` compiled using `hipcc main.cc`, you would look for the file `main-hip-amdgcn-amd-amdhsa-gfx90a.s`.

If you use OpenMP offloading using the **Cray compiler** (CCE), you’ll also want to add the `--save-temps` option but this time, because the compilation steps in fact only produce LLVM IR, you will look at link time, for the files generated. Generally, a file of the form `<file_name>-cce-openmppost-llc.s`.

**Note**

The OpenMP offload compilers and notably CCE, works somewhat like when LTO is enabled. that is, during the compile step the compiler produces LLVM Intermediate Representation (IR) for the GPU code, and machine code for the CPU. This gets put into a code object (`.o` file). At link time, a special linker (`cce_omp_offload_linker`) will orchestrate the GPU code generation and merging with CPU (host) code. All the object files get unbundled, the LLVM IR of the different files are merged into one big blob (`<binary_name>-cce-openmp__ll_app.amdgpu`) and then merged with the amdgcn bitcode (`${ROCM_PATH}/amdgcn/bitcode/*`) used to resolve the compiler builtin and AMD optimized math functions (`<binary_name>-cce-openmp__ll.amdgpu`). Finally, it optimizes the big LLVM IR files (`<binary_name>-cce-openmppost-opt.bc`) links in the OpenMP runtime GPU bitcode (`libcrayomptarget-states-amdgcn-gfx90a.bc`) and then compile the final bitcode(`<binary_name>-cce-openmp-pre-llc.bc`) into GPU machine code (`<binary_name>-cce-openmppost-llc.s`).

If, post build, you want to extract GPU code coming from a HIP source (it will not work for CCE OpenMP generated GPU code), you can do it like so:

```shell-session
$ module load rocm
$ roc-obj-ls <my program/shared object/object file>
$ roc-obj-extract <URI>
$ ${ROCM_PATH}/llvm/bin/llvm-objdump -d <extracted_file_name>.co
<assembly>
```

For instance:

```shell-session
$ module load rocm
$ roc-obj-ls main
1        host-x86_64-unknown-linux--                                         file://main#offset=65536&size=0
1        hipv4-amdgcn-amd-amdhsa--gfx90a                                     file://main#offset=65536&size=25248
$ roc-obj-extract "file://main#offset=65536&size=25248"
$ ${ROCM_PATH}/llvm/bin/llvm-objdump -d main-offset65536-size25248.co
main-offset65536-size25248.co:  file format elf64-amdgpu

Disassembly of section .text:

0000000000005400 <_Z8Flat6D3MIjTnT_Lj64ETnS0_Lj2ETnS0_Lj2ETnS0_Lj256ETnS0_Lj128ETnS0_Lj128E7Mapper0IjLi6EEEvT6_>:
        s_add_u32 flat_scratch_lo, s6, s9                          // 000000005400: 80660906
        s_addc_u32 flat_scratch_hi, s7, 0                          // 000000005404: 82678007
        s_load_dword s6, s[4:5], 0x24                              // 000000005408: C0020182 00000024
        s_load_dwordx4 s[12:15], s[4:5], 0x0                       // 000000005410: C00A0302 00000000
        s_load_dword s7, s[4:5], 0x10                              // 000000005418: C00201C2 00000010
        s_add_u32 s0, s0, s9                                       // 000000005420: 80000900
        s_addc_u32 s1, s1, 0                                       // 000000005424: 82018001
        s_waitcnt lgkmcnt(0)                                       // 000000005428: BF8CC07F
        s_and_b32 s4, s6, 0xffff                                   // 00000000542C: 8604FF06 0000FFFF
...
```

<a id="id10"></a>

### Miscellaneous documents

<https://rocm.docs.amd.com/en/latest/how-to/tuning-guides/mi300x/workload.html#debug-memory-access-faults>

<a id="scale"></a>

## SCALE

SCALE is a trendy new compiler that claims to compile CUDA code to AMD GPUs by relying on parts of the HSA layer (skipping HIP). Some Adastra users have found SCALE to be competitive with ROCm on finite element codes. CINES does not provide modules for SCALE yet though it can be easily setup by any user. Fundamentally, SCALE acts as a CUDA API forwarding and adapting the user request to AMD’s HSA kernel interface (HSA KMT). SCALE does not handle PTX/SASS machine code compilation to CDNA ISAs, so a recompilation of all products dependent on the CUDA runtime will be needed, with exception made if: they do not contain kernels, the symbols from the CUDA runtime are not versioned (e.g., not `cudaFree@libcudart.so.12`).

SCALE is available here for non commercial use:

```shell-session
$ wget "https://pkgs.scale-lang.com/tar/scale-latest-amd64.tar.xz"
$ tar xf scale-latest-amd64.tar.xz
```

**Warning**

SCALE is not HIP and is not interoperable with the ROCm/HIP runtime. Do not mix SCALE and HIP/ROCm APIs. Think of CUDA as a programming language (like C), not an NVIDIA-specific platform. Do not try to: link Cray-MPICH’s HSA GTL to a SCALE binary, do not try to use the HSA layer with SCALE, SCALE has its own allocators and [may confuse HSA logic](https://github.com/spectral-compute/scale-validation/issues/66). As of 2026/08/01, this means GPU-aware Cray-MPICH is not supported (you’ll get segfaults in `memcpy` or failure to find devices.

As of 2026/08/01, SCALE relies on ROCm 6. Dependency on ROCm is planned to be removed.

<a id="compiling-a-cuda-mpi-program-with-scale"></a>

### Compiling a CUDA+MPI Program with SCALE

Use `nvcc` as provided by SCALE to compile `.cu` files (or use `-X`), for example for MI250X (gfx90a):

```shell-session
$ source .../scale-...-Linux/bin/scaleenv gfx90a
$ nvcc -lineinfo -g -std=c++17 --offload-arch=gfx90a -O3 \
   -o my_program my_program.cu \
   --gcc-install-dir=/opt/software/gcc/13.2.0/lib/gcc/x86_64-pc-linux-gnu/13.2.0 \
   -Wl,-rpath,/opt/software/gcc/13.2.0/lib64
```

Note that the `--gcc-install-dir`/rpath is needed to point toward a `libstdc++` more recent that the one provided by RHEL 9.6.

<a id="debugging-environment-variables"></a>

### Debugging Environment Variables

The following variables can help diagnose issues:

```shell-session
$ export SCALE_EXCEPTIONS=2
$ export SCALE_DETECT_LEAKS=1
$ export REDSCALE_CRASH_REPORT_DETAILED=1
```

<a id="sycl"></a>

## Sycl

<a id="intel-llvm"></a>

### Intel LLVM

On Adastra, Intel LLVM/DPC++ (which normally comes with Intel’s OneAPI) is exposed through the `PrgEnv-intel` and the `intel` or `intel-oneapi` modules. The version we provide is quite old (2022.1). You may need to recompile it, see below.

**Note**

Make sure, if you compile your own toolchain, that your `${PATH}` and `${LD_LIBRARY_PATH}` environment variables point towards it!

You can test if a Sycl toolchain is working as expected on MI250 GPUs like so; compile a Sycl hello world:

```c++
#include <mpi.h>

#include <iostream>
#include <sycl/sycl.hpp>

int main(int argc, char** argv) {
    ::MPI_Init(&argc, &argv);

    size_t sz = 1000;

    sycl::buffer<int> buf(sz);

    std::cout << "Device name : "
            << sycl::queue{}.get_device().get_info<sycl::info::device::name>()
            << std::endl;

    sycl::queue{}.submit([&](sycl::handler& cgh) {
                    sycl::accessor acc{buf, cgh, sycl::write_only, sycl::no_init};

                    cgh.parallel_for(sycl::range<1>{sz}, [=](sycl::item<1> id) {
                        acc[id] = id.get_linear_id();
                    });
                })
        .wait();

    sycl::host_accessor acc{buf, sycl::read_only};

    std::cout << "expected : 999 | found : " << acc[sz - 1] << "\n";

    ::MPI_Finalize();
    return 0;
}
```

```shell-session
$ # NOTE: Our example uses MPI, we have to add the include and linker flags.
$ clang++ -O3 \
      -isystem "${CRAY_MPICH_PREFIX}/include" \
      -fsycl -fsycl-targets=amdgcn-amd-amdhsa -Xsycl-target-backend --offload-arch=gfx90a \
      --rocm-path="${ROCM_PATH}" \
      hello.cc -c
$ clang++ -O3 \
      -L"${CRAY_MPICH_PREFIX}/lib" -lmpi ${PE_MPICH_GTL_DIR_amd_gfx90a} ${PE_MPICH_GTL_LIBS_amd_gfx90a} \
      -fsycl -fsycl-targets=amdgcn-amd-amdhsa -Xsycl-target-backend --offload-arch=gfx90a \
      --rocm-path="${ROCM_PATH}" \
      hello.o -o hello
```

Run the example:

```shell-session
$ srun --account=<account_to_charge> \
      --nodes=1 \
      --constraint=MI250 \
      --job-name="example" \
      --time=1:00:00 \
      --exclusive \
      --ntasks-per-node=8 \
      -- ./hello | head
srun: job 319271 queued and waiting for resources
srun: job 319271 has been allocated resources
Device name : AMD Instinct MI250X
Device name : AMD Instinct MI250X
Device name : AMD Instinct MI250X
Device name : AMD Instinct MI250X
Device name : AMD Instinct MI250X
Device name : AMD Instinct MI250X
Device name : AMD Instinct MI250X
Device name : AMD Instinct MI250X
expected : 999 | found : 999
expected : 999 | found : 999
...
```

<a id="compiling-intel-llvm"></a>

#### Compiling Intel LLVM

To enjoy the latest release of Intel LLVM you will have to build it yourself. Its embarrassingly easy, as all software build should be ! (right ?):

```shell
#!/bin/bash

set -eu

# Cloning the code on a login node.
git clone --branch="sycl" https://github.com/intel/llvm intel-llvm-src || true
cd intel-llvm-src
git checkout d5f649b706f63b5c74e1929bc95db8de91085560

module purge

module load cpe/24.07
module load rocm/6.4.3

module load develop python cmake ninja libtool

module list

INSTALL_PATH="$(pwd)/install"

rm -rf ./build ./install

python3 buildbot/configure.py \
    --hip --hip-platform=AMD \
    --cmake-opt="-DCMAKE_C_COMPILER=amdclang" \
    --cmake-opt="-DCMAKE_CXX_COMPILER=amdclang++" \
    --cmake-opt="-DSYCL_BUILD_PI_HIP_ROCM_DIR=${ROCM_PATH}" \
    --cmake-opt="-DUR_HIP_ROCM_DIR=${ROCM_PATH}" \
    --cmake-opt="-DCMAKE_INSTALL_PREFIX=${INSTALL_PATH}" \
    --cmake-gen="Ninja"

cd build

time ninja -k0 all lib/all tools/libdevice/libsycldevice
time ninja -k0 install

echo "INSTALL_PATH=\"${INSTALL_PATH}\""
```

Additional detail is given here: <https://github.com/intel/llvm/blob/sycl/sycl/doc/GetStartedGuide.md>

Ensure your environment points towards the toolchain and that a `PrgEnv-amd`, `amd`, `amd-mixed` or `rocm` module is loaded:

```shell-session
$ export PATH="${INSTALL_PATH}/bin${PATH:+:${PATH}}"
$ export LD_LIBRARY_PATH="${INSTALL_PATH}/lib${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}"
```

**Note**

Ensure that you have recent CMake and Ninja versions. We provide guides on how to setup theses tools [here for CMake](../tools/index.md#adastra-software-stack-tools-building-cmake) and [here for Ninja](../tools/index.md#adastra-software-stack-tools-building-ninja).

**Note**

In the example compilation above we explicitly tell LLVM’s CMake machinery to use the amdclang compiler, you can choose another one.

<a id="adaptivecpp"></a>

### AdaptiveCPP

**Note**

`hipsycl` was rebrand as AdaptiveCPP for legal reasons.

CINES proposes a `hipsycl` installation done using Spack, for instance:

```shell-session
$ module spider hipsycl
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
hipsycl: hipsycl/0.9.4-mpi-python3
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    You will need to load all module(s) on any one of the lines below before the "hipsycl/0.9.4-mpi-python3" module is available to load.

    CCE-GPU-2.0.0
    CCE-GPU-2.1.0
    develop  CCE-GPU-3.0.0
```

We do not propose that you use this toolchain to compile Sycl code on Adastra as hipsycl 0.9.4 is quite old.

<a id="the-transformers-datasets-libraries"></a>

<a id="adastra-software-stack-libraries-transformers"></a>

## The `transformers` & `datasets` libraries

The python `transformers` and `datasets` libraries are a simple way to download datasets (that are not already available on Adastra’s [DSDIR](../../data_storage_and_transfers/index.md#adastra-storage-and-transfer-storage-datasets)), download models and tokenizers, create inference pipelines and fine tune models.

- We believe the datasets and models should preferably be on the scratch or the work storage areas. You can tell the library to cache the datasets and models in a user defined directory like so:

```shell-session
$ export HF_HOME="${WORKDIR}/USER_DSDIR"
```

Alternatively, you can programmatically, tell the HuggingFace libraries where to cache the data using the `cache_dir` argument.

```python
import os

# Store the data in the work.
cache_dir = os.path.join(os.environ['WORKDIR'], 'USER_DSDIR')

from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained('Equall/Saul-Instruct-v1', cache_dir=cache_dir)
model = AutoModelForCausalLM.from_pretrained('Equall/Saul-Instruct-v1', cache_dir=cache_dir)

from datasets import load_dataset
squad_dataset = load_dataset('squad', cache_dir=cache_dir)
```

If not specified, `HF_HOME` or `cache_dir` will likely point to your home directory’s `.cache/huggingface` folder.

**Warning**

Using `HF_HOME` is not same as using `cache_dir=${WORKDIR}`.

- You will run your computation on compute nodes who do not have internet access. Use `HF_HUB_OFFLINE` as shown below to avoid timeout during your code start up sequence. This implies you have downloaded your data (using say, `from_pretrained`) on a login node, prior to running your computations.

<a id="id11"></a>

### Some environment variables

| Feature/flag/environment variable | Explanation |
| --- | --- |
| `export HF_HOME="${WORKDIR}/USER_DSDIR"` | Specify where to put the cached data. Defaults to `~/.cache/huggingface`. We recommend something like: `${WORKDIR}/USER_DSDIR`. |
| `export HF_HUB_OFFLINE=1` | This prevent having to wait for a network connection timeout when using HuggingFace’s libraries (say, `transformers` or `datasets`). |
| `export TRANSFORMERS_OFFLINE=1` | Fine grain version of `HF_HUB_OFFLINE` for `transformer`’s `Auto***.from_pretrained` and the like. |
| `export HF_DATASETS_OFFLINE=1` | Fine grain version of `HF_HUB_OFFLINE` for `datasets`’ `load_dataset`. |
| `export TRANSFORMERS_VERBOSITY="info"` | Transformer library logging level. |

<a id="vllm"></a>

<a id="adastra-software-stack-libraries-vllm"></a>

## vLLM

**Note**

You may benefit from using a Python virtual environment, check [this document](../tools/index.md#adastra-software-stack-tools-python-virtual-environment) on how to setup one.

Requirements:

- A recent [install of PyTorch](index.md#adastra-software-stack-libraries-pytorch-installing) for ROCm (say in a VEnv);
- a recent [install of flash-attn](index.md#adastra-software-stack-libraries-flash-attention) for ROCm (say in a venv).

You can compile vLLM on Adastra using the script below.

<a id="for-rocm-6-1-2-and-up"></a>

### For ROCm 6.1.2 and up:

```shell
#!/bin/bash

set -eu

# Cloning the code on a login node.
git clone https://github.com/ROCm/vllm || true # Or use https://github.com/vllm-project/vllm
cd vllm
# git checkout v0.6.1 # v0.6.1-v0.6.6 For ROCm 6.1.2
git checkout v0.7.2+rocm

module purge

module load cpe/24.07
module load craype-accel-amd-gfx90a craype-x86-trento
module load PrgEnv-gnu
module load amd-mixed/6.2.1 # Match this version with the PyTorch ROCm version.
module load cray-python

module load cmake

module list

# If you use a Virtual Environment (VEnv):
# - deactivate it before loading modules;
# - activate it after loading modules like so:
# source ./python_environment/bin/activate
# - ensure you have installed PyTorch for the correct GPUs.

pip3 install --upgrade -r requirements-rocm.txt
pip3 install setuptools_scm

export PYTORCH_ROCM_ARCH="gfx90a;gfx942"
export MAX_JOBS="$(nproc)"

pip3 install --verbose --no-cache-dir --no-build-isolation ./
# # Or build the wheel that you can reuse later:
# python3 setup.py bdist_wheel
```

**Note**

You may have to change the CPE and ROCm (amd-mixed) versions as Adastra evolves.

<a id="usage"></a>

### Usage

If you do node distributed inferencing, you will want to use RCCL’s [AWS-OFI pluging](index.md#adastra-software-stack-libraries-rccl).

Distributed inference using vLLM typically rely on a [Ray](thttps://docs.ray.io/en/latest/) cluster. On Adastra such a cluster can be instanciated by first allocating a pool of node, for instance using `salloc` or `sbatch` and then calling `srun` to start a Ray instance per node. One of the Ray instance must be the master, other Ray instances will connect to it to synchronize, forming a cluster.

Assuming you have Ray in your Python environment, and an ongoing SLURM allocation, you can start Ray instances like so:

```shell-session
$ srun --ntasks-per-node=1 --cpu-bind=none --mem-bind=none --label -- ./ray.wrapper.sh
```

With `ray.wrapper.sh` as:

```shell
#!/bin/bash

set -eu

if [ "${SLURM_NODEID}" == "0" ]; then
    exec -- ray start --disable-usage-stats --block --head --port="29400"
else
    exec -- ray start --disable-usage-stats --block --address="$(scontrol show hostname "${SLURM_JOB_NODELIST}" | head -n 1):29400"
fi
```

You can then start vLLM by first `ssh` ing to one of the node forming the Ray cluster, and calling the following commands:

```shell-session
$ export RAY_ADDRESS="${MASTER_NODE_HOSTNAME}:29400"
$ # Ensure the ray cluster is reachable and available.
$ ray status
$ vllm serve "<path_to_hugging_face_model_snapshots>" --tensor-parallel-size 4 --pipeline-parallel-size 4 --gpu-memory-utilization 0.7 --trust-remote-code
```

Where `MASTER_NODE_HOSTNAME` is the hostname of the master node. `--tensor-parallel-size 4` will distribute layers onto 4 devices. `--pipeline-parallel-size 4` will distribute the model onto 4 accelerator partition (typically one partition is a node). As such, in the example above, it is assumed that 4*4=16 accelerator are available. `--gpu-memory-utilization 0.7` will prevent vLLM from allocating more than 70% of an accelerator’s memory.

**Warning**

Some environment variable are mandatory for all this machinery to work properly, notably, `export PYTHONPATH="${ROCM_PATH}/share/amd_smi${PYTHONPATH:+:${PYTHONPATH}}"`, `export RAY_EXPERIMENTAL_NOSET_ROCR_VISIBLE_DEVICES="1"` must be set before both the Ray cluster is launched and before the vLLM server is started. See below for additional environment variable of interest.

<a id="id12"></a>

### Some environment variables

| Feature/flag/environment variable | Explanation |
| --- | --- |
| `export RAY_EXPERIMENTAL_NOSET_ROCR_VISIBLE_DEVICES="1"` | (only for distributed cases tensor parallelism > 1 and/or pipeline parallelism > 1) Instructs Ray to not use this environment variable as it conflicts with vLLM. |
| `export PYTHONPATH="${ROCM_PATH}/share/amd_smi${PYTHONPATH:+:${PYTHONPATH}}"` | Tell vLLM where to use AMD SMI’s library. |
| `export NCCL_DEBUG="INFO"` | Ensure that RCCL is correctly configured and that the AWS plugin is in use. |
| `export VLLM_LOGGING_LEVEL="DEBUG"` | More information. |

<a id="id13"></a>

### Miscellaneous documents

<https://rocm.docs.amd.com/en/latest/how-to/tuning-guides/mi300x/workload.html#vllm-performance-optimization>
<https://rocm.docs.amd.com/en/latest/how-to/llm-fine-tuning-optimization/llm-inference-frameworks.html>
