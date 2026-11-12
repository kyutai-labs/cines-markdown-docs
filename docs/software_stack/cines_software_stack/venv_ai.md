<!-- Source: https://dci.dci-gitlab.cines.fr/webextranet/software_stack/cines_software_stack/venv_ai.html -->
<!-- Title: CINES’ AI virtual environments -->

<a id="cines-ai-virtual-environments"></a>

<a id="adastra-software-stack-cines-software-stack-venv-ai"></a>

# CINES’ AI virtual environments

**Note**

The **AI venv** is currently in **beta**. Your feedback, criticism and feature requests are welcome.

<a id="overview"></a>

<a id="adastra-software-stack-cines-software-stack-venv-ai-overview"></a>

## Overview

The **AI venv** provides a Python environment that include, by default, the many
of the common artificial-intelligence libraries (PyTorch, JAX, vLLM,
Flash-Attention, DeepSpeed, aiter, …) pre-compiled for Adastra AMD GPUs
(MI250, MI300A).

To guarantee **reproducibility**, each module version pins the exact versions of
the underlying libraries and the software stack.

All creation, update, duplication and restoration operations are driven by the
`poverlay-pip` wrapper which:

> - Resolves dependencies reproducibly using **uv pip compile**, while reusing
>   the installed stack when possible.
> - Automatically creates **snapshots** whenever environment-change files are
>   modified, making rollback easy.

Creation or modification of a virtual env must be performed on a **login node**
(the compute nodes have no Internet access). Once created, the venv can be used
in `sbatch` sessions.

<a id="creating-an-ai-venv"></a>

<a id="adastra-software-stack-cines-software-stack-venv-ai-creation"></a>

## Creating an AI venv

On a login node

```shell
export AI_VENV_PATH="${WORK}/venv/myproject"
module purge
module load develop
module load AI-develop
module load venv/0.8.0+torch2.11.0+rocm7.2.0
```

The directory `${WORK}/venv/myproject` will contain the virtual-env and :

- `bin/activate.poverlay` - activation script that loads the required modules.
  You can update it manually if you want to load custom modules, set env
  variables, or upgrade the base version.
- the `.snapshots` sub-directory that holds automatic snapshots.

<a id="activating-the-venv"></a>

<a id="adastra-software-stack-cines-software-stack-venv-ai-activation"></a>

## Activating the venv

<a id="activation-via-the-module-load"></a>

### Activation via the module load

1. Set the venv path in `AI_VENV_PATH`

```shell
export AI_VENV_PATH="${WORK}/venv/myproject"
```

1. Load the modules

```shell
module purge
module load develop
module load AI-develop
module load venv/0.8.0+torch2.11.0+rocm7.2.0
python -c "import torch; print(torch.__version__)"
```

The module automatically sources `${AI_VENV_PATH}/bin/activate`; no manual
`source` is required.

<a id="shortcut-using-source"></a>

### Shortcut using `source`

```shell
source -- "${WORK}/venv/myproject/bin/activate.poverlay"
(myproject) $ python
>>> import torch, vllm
```

Both approaches are equivalent. Python standard activation (source
*bin/activate*) also works but will reload the modules each time `python` is
invoked.

<a id="rocm-environment-variables"></a>

<a id="adastra-software-stack-cines-software-stack-venv-ai-rocm-environment"></a>

## ROCm environment variables

The module loads the variables needed for the libraries to work on AMD GPUs:

- `ROCM_PATH` -> `/opt/software/rocm/<version>/`
- `PYTORCH_ROCM_ARCH` -> `gfx90a;gfx942`
- `LD_LIBRARY_PATH` -> the `lib` and `lib64` paths of ROCm
- aws-ofi-rccl plugin …

These variables **should generally not be modified manually**. You can display
them with

```shell
module show venv/0.7.0+torch2.10.0+rocm7.2.0
```

<a id="dependency-management-with-poverlay-pip"></a>

<a id="adastra-software-stack-cines-software-stack-venv-ai-dependency-management"></a>

## Dependency management with `poverlay-pip`

<a id="add-remove-constrain-a-package"></a>

### Add / remove / constrain a package

```shell
# Add or update a package
poverlay-pip --stage install scipy==1.13.0
# Remove a package
poverlay-pip --stage uninstall scipy
# Add a version constraint
poverlay-pip --stage constraint protobuf==5.27.3
```

Each call **automatically** creates a snapshot in `.snapshots` (name =
timestamp) so you can roll back if needed.

<a id="synchronising-the-environment"></a>

### Synchronising the environment

After any modification (or after a ROCm or framework upgrade) run

```shell
# Compile and install packages
poverlay-pip sync
# Or, for a preview without applying changes
poverlay-pip --stage sync
```

`poverlay-pip sync` performs the following steps:

1. **Merges** the `*.in` files of the venv with those of base environments
   defined via `POVERLAY_PYTHONPATH` (determined by the `venv/@version@`
   module),
2. **Compiles** `requirements.txt` with `uv pip compile`,
3. **Dry-run** showing packages that will be installed or removed,
4. **Installs** the packages with `pip install --no-deps -r requirements.txt`.

<a id="snapshots-duplication-and-rollback"></a>

<a id="adastra-software-stack-cines-software-stack-venv-ai-snapshot-restore"></a>

## Snapshots, duplication and rollback

A **snapshot** is created on every `poverlay-pip` call that changes the
dependency resolution (result of `uv pip compile`). The name is
timestamp-based, e.g. `20260301101530`. List snapshots with

```shell
ls -- "${POVERLAY_ACTIVE_VENV}/.snapshots"
```

<a id="restoring-a-previous-state"></a>

### Restoring a previous state

```shell
poverlay-pip restore 20260312131235
# -> current files are archived in .snapshots/.archive/<timestamp>
```

<a id="duplicating-a-venv"></a>

### Duplicating a venv

```shell
poverlay-pip duplicate /lus/work/.../venv/clone 20260301_101530
```

The new venv contains exactly the same packages (and the same local wheels)
without duplicating the large binary files.

<a id="managing-blacklist-and-whitelist"></a>

<a id="adastra-software-stack-cines-software-stack-venv-ai-blacklist-whitelist"></a>

## Managing blacklist and whitelist

Some packages can be excluded (incompatibilities)

```shell
poverlay-pip blacklist aiter
python -c 'import aiter' # ModuleNotFoundError: No module named 'aiter'
```

To re-enable a package

```shell
poverlay-pip unblacklist aiter
python -c 'import aiter' # OK
```

The lists are stored in `${POVERLAY_ACTIVE_VENV}/blacklist.in` and
`${POVERLAY_ACTIVE_VENV}/whitelist.in`; each line accepts regular-expression
patterns.

<a id="key-points-usage-best-practices"></a>

<a id="adastra-software-stack-cines-software-stack-venv-ai-best-practices"></a>

## Key points / usage best practices

- **Always work on a login node** when creating or modifying the venv:
  `poverlay-pip` needs access to compilers and the Internet.
- **After any version change or installation**, run on **login node**
  `poverlay-pip sync` (or `--stage sync` to inspect first).
- **Do not unload/load modules once the env is activated**; the activation
  script configures it correctly for ROCm, compilers, aws-ofi plugin and the
  venv.
- **Prefer ``poverlay-pip –stage install`` + ``poverlay-pip sync`` over a raw
  ``pip install``**: the system ensures global environment consistency and avoid
  desinstallation at the next sync.
- **Prefer poverlay pip –stage install -r requirements.in to poverlay pip
  –stage install -r requirements.txt**: Easier upgrades.

<a id="upgrade-wheels-compile-rocm-compatible-wheels-versions"></a>

<a id="adastra-software-stack-cines-software-stack-venv-ai-upgrade-wheels"></a>

## Upgrade wheels / compile ROCM compatible wheels versions

**Note**

The module comes with a compilation env that should simplify the building of
packages compatible with ROCm. Keep in mind that you will need to rebuild
your wheels if you want to upgrade the base version in the future as many of
them depends on already installed frameworks like pytorch.

```shell
# Pre-requist
WHEELHOUSE_PATH="${POVERLAY_ACTIVE_VENV}/wheelhouse/${POVERLAY_ACTIVE_VENV_VERSION}"
mkdir -p -- "${WHEELHOUSE_PATH}"
cd "${WHEELHOUSE_PATH}"

# Flash attention
BUILD_TARGET="rocm" FORCE_BUILD=TRUE CAUSAL_CONV1D_FORCE_BUILD=TRUE pip wheel --no-build-isolation --no-deps git+https://github.com/Dao-AILab/flash-attention@fa4-v4.0.0.beta4  | tee build_flash_attn.log
export FLASHATTN_WHL="${WHEELHOUSE_PATH}"/flash_attn-*.whl
poverlay-pip override "flash-attn @ file://${FLASHATTN_WHL}"

# VLLM
pip wheel --no-build-isolation --no-deps -vv git+https://github.com/vllm-project/vllm.git@v0.17.1  | tee build_vllm.log
export VLLM_WHL="${WHEELHOUSE_PATH}"/wheelhouse/vllm-*.whl
poverlay-pip override "vllm @ file://${VLLM_WHL}"
```

**Note**

For many open source project, the github repository is a good starting point
to build a ROCm compatible version. You may need to look to the README,
setup.py files, Dockerfiles for ROCM to find the right building
configuration (often a few environments variables are required).

<a id="example-vllm"></a>

<a id="adastra-software-stack-cines-software-stack-venv-ai-examples"></a>

## Example VLLM

1. **Create the virtual environment (login node)**

```shell
module purge
module load develop
export AI_VENV_PATH="${WORK}/venv/vllm"
module load AI-develop
module load venv/0.8.0+torch2.11.0+rocm7.2.0
hf download facebook/opt-125m # download the model on the login node
```

2. **Submit a Slurm batch job** (script `run_vllm.sh`)

```shell
#!/bin/bash
#SBATCH --account=__account_name__
#SBATCH --constraint=MI250
#SBATCH --job-name=run_llm
#SBATCH --nodes=1
#SBATCH --time=01:00:00
#SBATCH --output=run_llm.log
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --gpus=1

set -eu

module purge
module load develop
export AI_VENV_PATH="${WORK}/venv/vllm"
module load AI-develop
module load venv/0.8.0+torch2.11.0+rocm7.2.0

# alternatively: source "${WORK}/venv/vllm/bin/activate.poverlay"

export TRANSFORMERS_OFFLINE=1
export HF_DATASETS_OFFLINE=1
export HIP_VISIBLE_DEVICES=0

srun vllm bench throughput --model facebook/opt-125m --dataset-name random
```

<a id="example-2-installing-boltzgen"></a>

## Example 2: Installing `boltzgen`

1. **Create (or reuse) the venv and load the modules**

```shell
module purge
module load develop
export AI_VENV_PATH="${WORK}/venv/boltzgen"
rm -rf "${AI_VENV_PATH}" # optional: start from a clean venv
module load AI-develop
module load venv/0.8.0+torch2.11.0+rocm7.2.0
```

2. **Attempt to install ``boltzgen`` (use ``–stage`` to see conflicts)**

```shell
poverlay-pip --stage install boltzgen
```

The command fails because `vllm` requires `numba==0.61.2` while `boltzgen`
pins `numba==0.61.0`.

Resolve the conflict by adding an override:

```shell
poverlay-pip --stage override "numba==0.61.0"
```

3. **Apply the changes**

```shell
poverlay-pip sync
```

4. **Verify that the binary works**

```shell
boltzgen --help
```

<a id="example-2-using-alphafold3"></a>

## Example 2: Using `alphafold3`

```shell
module purge
module load develop
export AI_VENV_PATH="${WORK}/venv/alphafold3"
module load AI-develop
module load venv/0.5.0+torch2.10.0
"${POVERLAY_PYTHONPATH}/scripts/alphafold3_gen_sbatch.sh" --account xxxx --json_path alphafold3_case.json --model_dir /path/to/alphafold/model/ # --help for more options
Successfully generated sbatch file alphafold3_case.sbatch
```

<a id="available-modules"></a>

<a id="adastra-software-stack-cines-software-stack-venv-ai-online-instances"></a>

## Available modules

*Due to the PyTorch security issue previous versions have been removed.* The
three virtual environments available through the Lmod modules (at the time of
writing) are:

| Module name | Version / ROCm | Variants |
| --- | --- | --- |
| `venv/0.5.0+torch2.10.0+rocm6.4.0` | ROCm 6.4.0, PyTorch 2.10.0 | alphafold3, boltz2 |
| `venv/0.6.0+torch2.10.0` | ROCm 6.4.3, PyTorch 2.10.0 | boltz2 |
| `venv/0.7.0+torch2.10.0+rocm7.2.0` | ROCm 7.2.0, PyTorch 2.10.0 | boltz2 |
| `venv/0.8.0+torch2.11.0+rocm7.2.0` | ROCm 7.2.0, PyTorch 2.11.0 | boltz2 |

<a id="last-version-of-principal-packages"></a>

<a id="adastra-software-stack-cines-software-stack-venv-ai-overrides-current"></a>

## Last version of principal packages

| Package | Version |
| --- | --- |
| torch | 2.11.0 |
| apex | 1.12.0 |
| deepspeed | 0.18.9 |
| vllm | 0.20.1 |
| triton | 3.6.0 |
| rocm-composable-kernel | 7.2.0 |
| jax | 0.9.1 |
| megatron-core | 0.15.0 |
| flash-attn | 2.8.3 |
| torchvision | 0.26.0 |
| bitsandbytes | 0.49.2 |
| amd-aiter | 0.1.10 |
| onnxruntime-training | 1.25.1 |
