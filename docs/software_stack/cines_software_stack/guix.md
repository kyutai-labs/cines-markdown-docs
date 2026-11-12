<!-- Source: https://dci.dci-gitlab.cines.fr/webextranet/software_stack/cines_software_stack/guix.html -->
<!-- Title: CINES’ Guix software stack -->

<a id="cines-guix-software-stack"></a>

<a id="adastra-software-stack-cines-software-stack-guix"></a>

# CINES’ Guix software stack

Modules are CINES’s main way of distributing software products. These products are often built using Spack. CINES now provide experimental access to [Guix](https://guix.gnu.org).

**Warning**

Guix is currently in a “beta test” phase on Adastra. We welcome your feedback both on setup issues and application-level issues (see the “Support” section below).

<a id="what-is-guix"></a>

## What is Guix?

Guix can be used in addition to and in parallel with module. Guix:

- provides [more than 30,000 software packages **variants**](https://hpc.guix.info/browse) (note the **variants** these packages are not comparable to Spack’s package concept). These include **variants** of the software like Vim, compiler toolchains (GCC, Clang), Python software (Scikit-Learn, NumPy, etc.), HPC libraries and applications (OpenMPI, MUMPS, PETSc, CP2K, etc.);
- distribute pre-built binaries (*substitutes* in Guix parlance) are usually available for packages you install, which makes installation faster;
- offer flexible installation and removal of user packages, you can roll back any time you want should an upgrade go wrong;
- enforces strong reproductilibily, so the *the exact same software environment*, bit-for-bit, on Adastra and on other machines (laptop, cluster, etc.);
- can *pack* software environments as a Docker or Singularity image for use on other systems.

<a id="getting-started"></a>

## Getting started

Once you are connected to Adastra, you can load the `guix` module:

```shell-session
$ module purge
$ module load guix
```

At this point, the `guix` command should be available:

```shell-session
$ guix describe
```

The sections below help you get started with Guix.

<a id="setting-up-your-environment"></a>

### Setting up your environment

The main command to set up an environment is `guix shell`, which can be thought of as similar to `module load`. To create an environment that contains GROMACS (CPU-only version) and to execute it, run:

```shell-session
$ guix shell gromacs -- gmx --version
```

Likewise, to create an interactive environment containing Python, NumPy, and SciPy, run:

```shell-session
$ guix shell python python-numpy python-scipy
```

The command above creates a *new shell* where `PATH` and similar variables point to these packages; the prompt in this shell has the `[env]` suffix. Exit this shell to return to your initial environment.

Alternatively, for a fully isolated environment, you can pass the `--container` (or `-C`) option:

```shell-session
$ guix shell --container python python-numpy python-scipy
```

Check out [the manual](https://guix.gnu.org/manual/devel/en/html_node/Invoking-guix-shell.html) for more information.

<a id="finding-packages"></a>

### Finding packages

To discover the packages Guix provides, you can browse the [on-line package list](https://hpc.guix.info/browse) or use one of these
commands:

```shell-session
$ guix package --list-available
$ guix search <keyword>
```

Additional packages are provided by additional [channels](https://hpc.guix.info/channels) such as:

- [Guix-Science](https://codeberg.org/guix-science/guix-science), which provides more scientific software;
- [Guix-Science-Nonfree](https://codeberg.org/guix-science/guix-science-nonfree), which provides packages for proprietary software.

The next section explains how to upgrade Guix and to pull additional channels.

<a id="upgrading-and-pulling-additional-channels"></a>

### Upgrading and pulling additional channels

To upgrade Guix and its package collection, run `guix pull`:

```shell-session
$ guix pull
```

**Warning**

Your very first run of `guix pull` will last about 20 minutes because it starts by performing a Git clone of [the entire Guix repository](https://git.guix.gnu.org/guix).

To pull in additional channels, create a `~/.config/guix/channels.scm` file that lists the channel you want to add. For example, the instructions on what to add to this file if you want to pull in Guix-Science [can be found on-line](https://hpc.guix.info/channel/guix-science).

**Note**

Running `guix describe` will show you which revision of Guix and which revision of additional channels are being used.

For more information, check out [the manual](https://guix.gnu.org/manual/devel/en/html_node/Invoking-guix-pull.html).

<a id="running-mpi-programs"></a>

### Running MPI programs

You can invoke `guix shell` to set up the environment of the MPI program you want to run.

For example, to run the Intel MPI Benchmarks (IMB) against OpenMPI 5, you can first, for example, allocate nodes:

```shell-session
$ salloc --account=<account_to_charge> --job-name="interactive" --constraint=GENOA --nodes=2 --time=1:00:00 --exclusive
```

and then, with that allocation, you can run the benchmarks with:

```shell-session
$ guix shell intel-mpi-benchmarks --with-input=openmpi=openmpi@5 openmpi@5 -- mpirun IMB-MPI1 PingPong
```

**Warning**

We recommend trying out your `guix shell` command *outside* the allocation so that software downloads or builds are not done during the allocation time.

**Warning**

As of this writing, `srun` is not supported because OpenMPI 5 only supports PMIx, which Adastra’s SLURM does not support.

<a id="running-hip-rocm-programs-on-gpus"></a>

### Running HIP/ROCm programs on GPUs

The example below allocates one GPU node and runs the ROCm bandwidth test on it:

```shell-session
$ srun --account=<account_to_charge> --job-name="interactive" --constraint=MI250 --nodes=1 --time=00:02:00 --exclusive --tasks-per-node=1 \
  -- guix shell rocm-bandwidth-test -- rocm-bandwidth-test plugin --run tb p2p
```

**Note**

By default, most packages are built *without* HIP/ROCm support. For instance, the `python-pytorch` and `cp2k` packages lack ROCm support. In some cases, a GPU-enabled version exists, such as `cp2k-hip-rocm`.

<a id="creating-portable-bundles"></a>

## Creating portable bundles

Once you have a software environment that works well on Adastra, you may want to create a self-contained “bundle” that you can send and use on other machines that do not have Guix.

With [guix pack](https://guix.gnu.org/manual/devel/en/html_node/Invoking-guix-pack.html) you can create *container images* for Docker or Singularity, or even standalone tarballs. See the following articles for more information:

- [With or without Guix: Deploying complex software stacks on major supercomputers](https://hpc.guix.info/blog/2025/12/with-or-without-guix-deploying-complex-software-stacks/)

<a id="support"></a>

## Support

For more information, please see:

- [Getting Started](https://guix.gnu.org/manual/devel/en/html_node/Getting-Started.html) ([français](https://guix.gnu.org/manual/devel/fr/html_node/Guide-de-d_00e9marrage.html))
- [Guix Reference Card](https://guix.gnu.org/guix-refcard.pdf)
- [Guix-HPC web site](https://hpc.guix.info)

Please send Guix-specific support requests to adastra-guix@inria.fr, which is handled by an Inria/[NumPEx](https://numpex.org/exadi-development-and-integration/) team.
