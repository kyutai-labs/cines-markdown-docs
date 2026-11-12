<!-- Source: https://dci.dci-gitlab.cines.fr/webextranet/quick_start/index.html -->
<!-- Title: Adastra quick start -->

<a id="adastra-quick-start"></a>

<a id="id1"></a>

# Adastra quick start

<a id="get-started-in-video"></a>

## Get started in video

A series of introductory videos (in French) is available on Canal U, the audiovisual platform for higher education and research. These videos walk you through the essential steps to get started on Adastra:

1. [Overview of the machine](https://www.canal-u.tv/chaines/cines/1-presentation-generale-de-la-machine-quickstart-adastra)
2. [Accessing Adastra](https://www.canal-u.tv/chaines/cines/2-acceder-a-adastra-quickstart)
3. [The Adastra software environment](https://www.canal-u.tv/chaines/cines/3-l-environnement-logiciel-d-adastra-quickstart-adastra)
4. [Job manager](https://www.canal-u.tv/chaines/cines/4-gestionnaire-de-travaux-quickstart-adastra)
5. [HPC application containers on Adastra](https://www.canal-u.tv/chaines/cines/5-les-conteneurs-d-applications-hpc-sur-adastra-quickstart-adastra)

<a id="how-to-ask-for-help"></a>

## How to ask for help

You can always ask you questions at [svp@cines.fr](mailto:svp%40cines.fr). We recommend that you follow the “asking for help” tips listed in [this document](../other/contact.md#other-contact).

<a id="registering-an-account"></a>

## Registering an account

We recommend that you follow [this document](../user_support/index.md#adastra-accessing-account-opening). In case you want to submit a new research project instead of simply joining an already existing one, things can get more involved and we recommend that you contact your Comité Thématique (CT) representative.

<a id="connecting-to-adastra"></a>

## Connecting to Adastra

We will refer to `<login>` as the username used to log on Adastra.

- If you are running Windows, launch an SSH client (like PuTTy) and connect to the Adastra address: `adastra.cines.fr`. In Putty’s settings: `Connection/SSH/X11` check the `Enable X11 forwarding` box.
- If you are on Linux, open a terminal, and connect to Adastra like so:

```shell-session
$ ssh -X <login>@adastra.cines.fr
```

Your terminal’s working directory now points to your home directory and you can now enter commands which will execute on a **login** node. On Adastra you will find login nodes on which you are to compile and submit tasks to the hundreds of **compute** nodes. The way a user can be attached to multiple project (DARI allocation) is handled using the concept of login unique.

More details in:

- [Connecting](../user_support/index.md#adastra-accessing-connection);
- [Login unique](../user_support/index.md#adastra-accessing-unique-login);
- [Layout of common files and directories](../user_support/index.md#adastra-file-layout).

<a id="transferring-sources-to-adastra"></a>

## Transferring sources to Adastra

If possible, use something like Gitlab or Github.

If the IP address of your Git repository is **not** authorized by Adastra’s firewall, you may ask [svp@cines.fr](mailto:svp%40cines.fr) to fix that for you. Else:

- Under Windows: use an SFTP solution such as FileZilla.
- Under Unix like, you can use FileZilla or the following command:

```shell-session
me@lab:~$ scp -r local_dir <login>@adastra.cines.fr:~/my_adastra_path
```

More details in:

- [Accessing the storage areas](../data_storage_and_transfers/index.md#adastra-storage-and-transfer-storage-accessing);
- [Quotas](../data_storage_and_transfers/index.md#adastra-storage-and-transfer-policies-data-quota);
- [Tools to transfer Data](../data_storage_and_transfers/index.md#adastra-storage-and-transfer-transfer-tools).

<a id="the-module-environment"></a>

## The module environment

Adastra uses modules to expose softwares. If you want to use prebuilt simulation software please refer to these documents [Using the CINES software stack](../software_stack/cines_software_stack/spack.md#adastra-software-stack-cines-software-stack-spack-using), [Simulation software scripts and tips](../software_stack/simulation_software/index.md#adastra-software-stack-simulation-software-script-and-tips) and [CINES’ Spack module catalog](../software_stack/cines_software_stack/spack_products_catalog.md#adastra-software-stack-spack-product-catalog).

If you want to compile your own code, you might benefit from reading theses documents: [CrayPE basics](../user_support/index.md#adastra-programming-environment-cray-pe-basics), [Libraries & toolchains](../software_stack/libraries/index.md#adastra-software-stack-libraries)

A typical environment for the GENOA (CPU) partition looks like that:

```shell-session
$ module purge
$ # A CrayPE environment version
$ module load cpe/24.07
$ # An architecture
$ module load craype-x86-genoa
$ # A compiler to target the architecture
$ module load PrgEnv-cray
```

<a id="compiling-code"></a>

## Compiling code

For **CPU** compilations:

> - C/C++ codes can rely on `PrgEnv-gnu`, `PrgEnv-aocc` or `PrgEnv-cray`;
> - Fortran codes can rely on `PrgEnv-gnu`, `PrgEnv-cray` or `PrgEnv-intel`.

**Note**

If you target the Genoa CPUs, **you must ensure** that the GCC version is more recent or equal to `gcc/13.2.0`.

For **GPU** compilations:

- C/C++ codes can rely `PrgEnv-amd`, `PrgEnv-cray` or potentially `PrgEnv-gnu` with `rocm`;
- Fortran codes can rely `PrgEnv-cray` (required for OpenMP target/OpenACC + Fortran).

More details in [this document](../user_support/index.md#adastra-programming-environment-prgenv-compiler).

Assuming the environment above (for the GENOA partition), you would compile a hello world program like so:

```c++
#include <mpi.h>

#include <iostream>

int main(int argc, char ** argv) {
    ::MPI_Init(&argc, &argv);

    std::cout << "Hello world\n";

    ::MPI_Finalize();

    return 0;
}
```

```shell-session
$ CC -O3 -Wall hello_world.cpp -o hello_world
```

**Note**

The MPI library is implicitly linked.

Example compilation using CMake are given here in [CMake examples](../software_stack/tools/index.md#adastra-software-stack-tools-building-cmake-example).

More details in:

- [Programming environment](../user_support/index.md#adastra-programming-environment).

<a id="running-a-compute-job"></a>

## Running a compute job

Assuming the build above, you could submit a job onto the GENOA partition, using SLURM:

```shell-session
$ srun --account=<account_to_charge> \
      --job-name="hello_world" \
      --constraint=GENOA \
      --nodes=1 \
      --exclusive \
      --time=1:00:00 \
      --ntasks-per-node=24 \
      --cpus-per-task=8 \
      --threads-per-core=1 \
      -- ./hello_world
srun: job 548214 queued and waiting for resources
srun: job 548214 has been allocated resources
Hello world
Hello world
Hello world
Hello world
...
```

**Note**

Here we use `srun` as shortcut for allocating and submitting work. This is but an example, not the recommend way. In practice you should use proper [batch scripts](../user_support/index.md#adastra-running-jobs-batch-scripts).

**Warning**

The *scratch* storage area is cleaned up of old file on [a regular basis](../data_storage_and_transfers/index.md#adastra-storage-and-transfer-policies-data-purge).

More details in:

- [Job submission](../user_support/index.md#adastra-running-jobs).

<a id="submitting-a-job"></a>

## Submitting a job

When running real world cases, we prefer using the concept of scheduled job. It consist in specifying, in a script, a list of statements to execute at a later time, when the compute resources are available. The above mentioned `srun` command would be expressed in a file named `job.sh` like so:

```shell
#!/bin/bash
#SBATCH --account=<account_to_charge>
#SBATCH --job-name="hello_world"
#SBATCH --constraint=GENOA
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=1:00:00

# # With    HyperThreading (SMT), 192 cores and 384 hardware threads.
# srun --ntasks-per-node=24 --cpus-per-task=16 --threads-per-core=2 -- ./hello_world
# Without HyperThreading (SMT), 192 cores and 192 hardware threads.
srun --ntasks-per-node=24 --cpus-per-task=8  --threads-per-core=1 -- ./hello_world
```

You can schedule the task for later execution like so:

```shell-session
$ sbatch job.sh
```

If and only if you need **less** than a whole node worth of compute resources, you can use the following script showing an example job of 20 tasks each associated to 1 core. We call that [shared mode](../user_support/index.md#adastra-running-jobs-shared-exclusive-mode) as you share a node with other users.

```shell
#!/bin/bash
#SBATCH --account=<account_to_charge>
#SBATCH --job-name="hello_world"
#SBATCH --constraint=GENOA
#SBATCH --nodes=1
# #SBATCH --exclusive # Shared !
#SBATCH --ntasks-per-node=20
#SBATCH --cpus-per-task=2
#SBATCH --threads-per-core=2
#SBATCH --time=1:00:00

# # With    HyperThreading (SMT), 20 cores and 40 hardware threads.
# srun --ntasks-per-node=20 --cpus-per-task=2 --threads-per-core=2 -- ./hello_world
# Without HyperThreading (SMT), 20 cores and 20 hardware threads.
srun --ntasks-per-node=20 --cpus-per-task=1 --threads-per-core=1 -- ./hello_world
```
