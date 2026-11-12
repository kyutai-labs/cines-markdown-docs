<!-- Source: https://dci.dci-gitlab.cines.fr/webextranet/software_stack/spack_user/index.html -->
<!-- Title: Spack-user : Using pre-configured Spack installation on Adastra -->

<a id="spack-user-using-pre-configured-spack-installation-on-adastra"></a>

<a id="adastra-software-stack-spack-user"></a>

# Spack-user : Using pre-configured Spack installation on Adastra

**Note**

The pre-configured Spack environment is also referred to as *spack-user*.

Adastra provides a Spack module named *spack-user-<version>*, which gives access to a pre-configured instance of Spack tailored to Adastra’s architecture. This Spack instance will allow you to compile software while reusing the Cray programming environment toolchain and architecture. The software will be installed in a location determined by the `${SPACK_USER_PREFIX}` environment variable. If not explicitly set, this defaults to `${HOME}`. It is recommended to change this value when working across multiple Adastra partitions to better organize your installations. Although this setup benefits from the build cache maintained by the CINES support team, it does not use CINES’ complete software stack as an upstream source in Spack. This choice ensures that your installations remain self-contained and do not depend on external or centrally-managed software stacks.

**Pro and cons** : Using spack-user ties you to a specific Spack version maintained by CINES, offering quick access to pre-built packages via shared mirrors and binary caches. This results in significantly faster installation times, at the cost of some flexibility.

<a id="getting-started"></a>

<a id="adastra-software-stack-spack-user-getting-started"></a>

## Getting started

To install software with Spack, follow these steps:

1. Initialize Spack.

We provide the following Spack pre-configured module that you can use to introduce CINES’ Spack configuration to your environment.

| Targeted partition | Spack PreConf module | Configured toolchains |
| --- | --- | --- |
| All | `spack-user-<version>` | CCE, GCC, AMD LLVM |

**Note**

We provide multiple compilers per spack-user defined in [Available Preconfigured Compilers](index.md#adastra-software-stack-spack-user-available-preconfigured-compilers) section, this differs from the environment mentioned in the [Extensible software stacks](../cines_software_stack/spack.md#adastra-software-stack-cines-software-stack-spack-extensible) section.

**Note**

An extensible software stack module (or environment) or spack-user module will implicitly load modules; a behavior you can observe using `module show spack-user-<version>`. Running `module purge` before loading an extensible software stack module is recommended.

```shell-session
$ module purge
$ export SPACK_USER_PREFIX="${WORKDIR}/spack-install-<version>"
$ module load develop
$ module load spack-user-<version>
For more information on how spack user works on Adastra, please consult documentation https://dci.dci-gitlab.cines.fr/webextranet/software_stack/spack_user/index.html
SPACK_USER_PREFIX=<path_to_spack_user_files>/
SPACK_USER_CONFIG_PATH=<path_to_spack_configuration>/
```

**Note**

We recommend that you set `${SPACK_USER_PREFIX}` in an environment script or in your `.bash_profile` to avoid having to set it every time you want to use Spack.

**Warning**

Ensure that the `${SPACK_USER_PREFIX}` variable is not too long (ambiguous) or you may get Spack errors of this kind: `Error: Failed to install XXX due to SbangPathError: Install tree root is too long. Spack cannot patch shebang lines when script path length (YYY) exceeds limit (127).`

When loading the Spack PreConf module, a fully preconfigured Spack instance will be placed where the `${SPACK_USER_PREFIX}` points to.

2. Consult the information that Spack has on the product you wish to install and in particular on the configuration options that Spack calls *variant*:

```shell-session
$ spack info kokkos
```

Let’s assume that we intend to setup this product using the ROCm toolchain. Upon reviewing the product information, it follows that the installation command could be:

```shell-session
$ spack install kokkos@4.2.00%rocmcc@5.7.1~aggressive_vectorization~compiler_warnings~cuda~debug~debug_bounds_check~debug_dualview_modify_check~deprecated_code~examples~hpx~hpx_async_dispatch~hwloc~ipo~memkind~numactl~openmp~openmptarget~pic+rocm+serial+shared~sycl~tests~threads~tuning~wrapper amdgpu_target==gfx90a build_system=cmake build_type=Release cxxstd=17 generator=ninja patches=145619e arch=linux-rhel8-zen3
```

The `+rocm` flag enables AMD GPU support. Additionally, we need to specify the GPU type: `amdgpu_target==gfx90a` (note the double equal signs, which have the special meaning of propagating the GPU target to all dependencies). While we specify the `rocmcc@5.7.1` compiler, it’s `hipcc` of the ROCm toolchain that will be used for this build. The `arch=linux-rhel8-zen3` tells Spack to target the Zen3 CPU architecture (say, enable AVX2).

**Warning**

You must ensure that the `arch=` is correctly specified. If you want to target the MI250X nodes, you should use `arch=linux-rhel8-zen3`, else you should use `arch=linux-rhel8-zen4`.

3. It is advisable to review the dependencies that Spack intends to install:

```shell-session
$ spack spec kokkos%rocmcc amdgpu_target=gfx90a arch=linux-rhel8-zen3
--------------------------------
-   kokkos@4.4.01%rocmcc@6.1.2.genoa~aggressive_vectorization~cmake_lang~compiler_warnings~cuda~debug~debug_bounds_check~debug_dualview_modify_check~deprecated_code~examples~hpx~hpx_async_dispatch~hwloc~ipo~memkind~numactl~openmp~openmptarget~pic+rocm+serial+shared~sycl~tests~threads~tuning~wrapper amdgpu_target=gfx90a build_system=cmake build_type=Release cxxstd=17 generator=make intel_gpu_arch=none arch=linux-rhel8-zen3
-       ^cmake@3.30.5%rocmcc@6.1.2.genoa~doc+ncurses+ownlibs~qtgui build_system=generic build_type=Release patches=dbc3892 arch=linux-rhel8-zen3
-           ^curl@8.10.1%rocmcc@6.1.2.genoa~gssapi~ldap~libidn2~librtmp~libssh~libssh2+nghttp2 build_system=autotools libs=shared,static tls=openssl arch=linux-rhel8-zen3
-               ^nghttp2@1.63.0%rocmcc@6.1.2.genoa build_system=autotools arch=linux-rhel8-zen3
-                   ^diffutils@3.10%rocmcc@6.1.2.genoa build_system=autotools arch=linux-rhel8-zen3
-                       ^libiconv@1.17%rocmcc@6.1.2.genoa build_system=autotools libs=shared,static arch=linux-rhel8-zen3
-               ^openssl@3.4.0%rocmcc@6.1.2.genoa~docs+shared build_system=generic certs=mozilla arch=linux-rhel8-zen3
-                   ^ca-certificates-mozilla@2023-05-30%rocmcc@6.1.2.genoa build_system=generic arch=linux-rhel8-zen3
-                   ^perl@5.40.0%rocmcc@6.1.2.genoa+cpanm+opcode+open+shared+threads build_system=generic arch=linux-rhel8-zen3
-                       ^berkeley-db@18.1.40%rocmcc@6.1.2.genoa+cxx~docs+stl build_system=autotools patches=26090f4,b231fcc arch=linux-rhel8-zen3
-                       ^bzip2@1.0.8%rocmcc@6.1.2.genoa~debug~pic+shared build_system=generic arch=linux-rhel8-zen3
-                       ^gdbm@1.23%rocmcc@6.1.2.genoa build_system=autotools arch=linux-rhel8-zen3
-                           ^readline@8.2%rocmcc@6.1.2.genoa build_system=autotools patches=bbf97f1 arch=linux-rhel8-zen3
-               ^pkgconf@2.2.0%rocmcc@6.1.2.genoa build_system=autotools arch=linux-rhel8-zen3
-           ^ncurses@6.5%rocmcc@6.1.2.genoa~symlinks+termlib abi=none build_system=autotools patches=7a351bc arch=linux-rhel8-zen3
-           ^zlib-ng@2.2.1%rocmcc@6.1.2.genoa+compat+new_strategies+opt+pic+shared build_system=autotools arch=linux-rhel8-zen3
[e]      ^glibc@2.28%rocmcc@6.1.2.genoa build_system=autotools arch=linux-rhel8-zen3
-       ^gmake@4.4.1%rocmcc@6.1.2.genoa~guile build_system=generic arch=linux-rhel8-zen3
[e]      ^hip@6.1.2%rocmcc@6.1.2.genoa~asan~cuda+rocm build_system=cmake build_type=Release generator=make patches=1f65dfe,6bbe83b arch=linux-rhel8-zen3
[e]      ^hsa-rocr-dev@6.1.2%rocmcc@6.1.2.genoa~asan+image+shared build_system=cmake build_type=Release generator=make arch=linux-rhel8-zen3
[e]      ^llvm-amdgpu@6.1.2%rocmcc@6.1.2.genoa~link_llvm_dylib~llvm_dylib+rocm-device-libs build_system=cmake build_type=Release generator=ninja patches=b4774ca,eaf700a arch=linux-rhel8-zen3
[e]      ^rocthrust@6.1.2%rocmcc@6.1.2.genoa amdgpu_target=auto build_system=cmake build_type=Release generator=make arch=linux-rhel8-zen3
```

In your Spack instance, packages you installed will be denoted by a `[+]` in the first column, while packages already provided by Spack and cached from previous builds will display `[^]`. A `-` indicates that Spack did not find the package and will proceed to build it. A `[e]` indicates that the product is external to Spack, typical a system product, in our case, it is looking for ROCm libraries.

4. Once you’ve reviewed Spack’s plan and are satisfied with it, proceed to install the packages.

**Warning**

We are experiencing some signature inconsistency, so to workaround issues such as `Error: Failed to install XXX due to NoVerifyException`, specify `--no-check-signature` in the `spack install` command. Alternatively, you can use `--no-cache` to bypass the CINES’ build cache but you will experience longer build time.

```shell-session
$ spack install kokkos@4.4.01%rocmcc@6.1.2.genoa~aggressive_vectorization~cmake_lang~compiler_warnings~cuda~debug~debug_bounds_check~debug_dualview_modify_check~deprecated_code~examples~hpx~hpx_async_dispatch~hwloc~ipo~memkind~numactl~openmp~openmptarget~pic+rocm+serial+shared~sycl~tests~threads~tuning~wrapper amdgpu_target=gfx90a build_system=cmake build_type=Release cxxstd=17 generator=make intel_gpu_arch=none arch=linux-rhel8-zen3
...
Stage: 0.09s.  Cmake: 8.46s.  Build: 9.32s.  Install: 2.57s.  Post-install: 0.97s.  Total: 21.70s
[+] <path_to_spack_configuration>/spack-install-4.0.0/linux-rhel8-zen3/rocmcc-6.1.2.genoa/kokkos-4.4.01-xdxx
```

The last line indicates the location of the software installation on the disk.

5. After successful installation of the product, you may want to ask Spack to forcefully generate modules (This should happen automatically).

```shell-session
$ spack module tcl refresh --delete-tree --yes-to-all
```

Then, you can find your product in your module environment:

```shell-session
$ module available kokkos/4.4.01
---- <path_to_spack_configuration>/spack-install-4.0.0/modules/tcl/linux-rhel8-zen3 ----
rocmcc/6.1.2.genoa/zen3/kokkos/4.4.01
```

If you wish to utilize the modules generated by this Spack instance without loading the associated modules (`spack-user-<version>`), you can simply add the path of your modules to the `${MODULEPATH}` (they should be under `${SPACK_USER_PREFIX}/modules/tcl/linux-rhel8-[zen3|zen4]`).

```shell-session
$ # For MI250:
$ module use "${SPACK_USER_PREFIX}/modules/tcl/linux-rhel8-zen3"
$ # For GENOA:
$ module use "${SPACK_USER_PREFIX}/modules/tcl/linux-rhel8-zen4"
```

<a id="available-preconfigured-compilers"></a>

<a id="adastra-software-stack-spack-user-available-preconfigured-compilers"></a>

## Available Preconfigured Compilers

When using the `spack-user-<version>` module on Adastra, a set of compilers is preconfigured to match the available hardware partitions and toolchains. These compilers are already integrated into the Spack environment and ready to use for building software optimized for specific architectures.

The currently available compilers include:

```shell-session
$ spack compiler list
==> Available compilers
-- cce rhel8-x86_64 ---------------------------------------------
cce@18.0.0.mi250  cce@18.0.0.genoa

-- gcc rhel8-x86_64 ---------------------------------------------
gcc@13.2.1.mi250  gcc@13.2.1.genoa  gcc@13.2.1.generic

-- rocmcc rhel8-x86_64 ------------------------------------------
rocmcc@6.1.2.mi250  rocmcc@6.1.2.genoa  rocmcc@6.1.2
```

With:

- `cce@18.0.0.mi250`: Cray CCE (Cray Compiler Environment) configured for the MI250X partition (Zen3 + AMD GPUs)
- `cce@18.0.0.genoa`: Cray CCE (Cray Compiler Environment) configured for the GENOA partition (Zen4)
- `gcc@13.2.1.mi250`: GCC (GNU Compiler Collection) configured for MI250X partition (Zen3 + AMD GPUs)
- `gcc@13.2.1.genoa`: GCC (GNU Compiler Collection) configured for GENOA partition (Zen4)
- `gcc@13.2.1.generic`: A generic GCC build not tied to a specific architecture
- `rocmcc@6.1.2.mi250`: ROCm Compiler Collection (ROCmCC) configured for the MI250X partition (Zen3 + AMD GPUs)
- `rocmcc@6.1.2.genoa`: ROCm Compiler Collection (ROCmCC) configured for the GENOA partition (Zen4)

Each of these compilers is pre-integrated into the `spack-user` configuration and can be used directly in Spack commands, such as:

```shell-session
$ spack install <package>%gcc@13.2.1.mi250
```

These compiler versions are chosen and maintained by the CINES support team to ensure compatibility and performance on Adastra’s different partitions.

**Note**

You can view the full list of detected compilers with `spack compiler list`, and their corresponding configuration file is located at `${SPACK_USER_PREFIX}/configuration/compilers.yaml`. Additional compiler definitions are included but commented out in this file, allowing you the flexibility to enable them if needed. Keep in mind that the more compilers you enable, the longer Spack’s concretization phase will take, as it performs checks on all defined compilers.

<a id="troubleshooting"></a>

<a id="adastra-software-stack-spack-user-troubleshooting"></a>

## Troubleshooting

If you encounter a failed Spack installation, consider examining the error message displayed. Additionally, Spack may direct you to an installation log for the specific product, which can be found in the same directory. The complete build directory is also available in `/tmp`. Examining the configure or cmake output logs may sometimes yield fruitful results. Finally, the `spack -d install -v` command may prove useful.

Here are some tips if the installation fails:

- Modify the software version;
- Modify the compiler : If the compiler is not specified, it takes by default the cce compiler (the recommended compiler for installing our software on Cray systems). If the installation fails, try with another compiler;
- Disable variants that seem to cause problems;
- Modify the dependencies used to build the target product (also called package);
- Edit `package.py`: take a look at the `package.py` of the package that crashes: `spack edit package_name`. Unfortunately the process is not always simple since the package repository is situated in a read-only location. In these situations, it is necessary to clone your own Spack instance and configure it using our configuration files.

Assistance is available: you may refer to the official [Spack documentation](https://spack.readthedocs.io/en/latest/), open a ticket at the CINES help desk, or seek help from the Spack community via the [Spack Slack](https://slack.spack.io/).

<a id="limitations"></a>

<a id="adastra-software-stack-spack-user-limitations"></a>

## Limitations

- Spack evolves quickly, the tagged Spack version (i.e.: 0.22) are always lacking compared to the develop Spack branch;
- you may have to specify `--no-check-signature`.
- **Spack is installed on login nodes that do not have access to all the internet**, only certain package versions are available to users. These versions are those previously downloaded by the CINES support team, they can be found in the local repository of archive packages, called mirror (see [mirrors documentation](https://spack.readthedocs.io/en/latest/mirrors.html) for more information). The CINES mirror is located in this path: `/opt/software/gaia/local_repo` (you can search in it if the package you want to install is already there). To circumvent this limitation you can download yourself the archive packages (tarballs) then copy it in a folder created for this purpose, overload the configuration file `mirrors.yaml` by adding a mirror pointing to your archive packages folder. Here is an example of this protocol:

Download the tarballs from your workstation (**spack expect a file with a tar.gz extension files**), copy it to Adastra and connect to Adastra :

```shell-session
$ scp packages.tar.gz <login>@adastra.cines.fr:/path/to/your/home
$ ssh <login>@adastra.cines.fr
```

After initializing spack, copy your tarballs into your archive package folder, for example :

```shell-session
$ export SPACK_USER_PREFIX="${HOME}/spack-install-<version>"
$ module load spack-user-<version>
$ mkdir -p -- "${SPACK_USER_PREFIX}/mirror/<package_name>" # change <package_name> to its real name, e.g. “cmake”.
$ mv "${HOME}/packages.tar.gz" "${SPACK_USER_PREFIX}/mirror/<package_name>/."
```

Then overload the defaults configuration file `mirrors.yaml` by adding a mirror pointing to your archive packages folder :
Next, update the default `mirrors.yaml` configuration file by adding a mirror that points to your archive packages folder using the `spack mirror add` command. Ensure that the path to the mirror is hardcoded, as Spack will not automatically resolve variables in `mirrors.yaml`. By using the `spack mirror add` command, Spack evaluates the provided path directly, effectively avoiding this issue.

```shell-session
$ spack mirror add local_filesystem_user $SPACK_USER_PREFIX/mirror
$ grep -v ^"  #" ${SPACK_USER_PREFIX}/configuration/mirrors.yaml
  mirrors:
    local_filesystem_user: /lus/home/path/to/your/login/hardcoded_spack_user_prefix/mirror
    local_filesystem:
      url: file:///opt/software/gaia/local_repo
      binary: true
      source: true
      signed: false # disable signing and verification
    spack-public: https://mirror.spack.io
```

<a id="recommendations"></a>

<a id="adastra-software-stack-spack-user-recommendations"></a>

## Recommendations

<a id="shared-spack-installation"></a>

### Shared Spack installation

**Note**

Starting with `spack-user-4.0.0`, these configuration options (especially `concretizer:unify:true` and `permission` settings) are applied by default. You can still override them manually if needed.

To ensure a functional and collaborative setup, make sure that the spack directories are readable by all the project members.

```shell-session
$ spack config --scope user update packages
$ spack config --scope user add 'packages:all:permissions:read:world'
$ spack config --scope user add 'packages:all:permissions:write:group'
$ spack config --scope user add 'concretizer:unify:true'
```

Unifying the installed package is important if your concretization shares dependencies with different spec, but all being linked into the same final binaries. For instance, you have an OpenBLAS with openmp support and an other without. If you link both you could expose yourself to troubles.

You may also want to prevent Spack from writing files in your home. This can be done like so:

```shell-session
$ export SPACK_USER_CACHE_PATH="${SPACK_USER_PREFIX}/cache"
$ export SPACK_USER_CONFIG_PATH="${SPACK_USER_PREFIX}/Environment"
```

<a id="best-practices"></a>

### Best Practices

Below, we give an example script that you can use as is (you’ll probably want to change the `VERSION` environment variable as time evolves).

```shell
#!/bin/bash

SCRIPT_DIRECTORY="$(dirname -- "$(readlink -f -- "${BASH_SOURCE[0]:-${0}}")")"

# VERSION="spack-user-3.2.0"
# VERSION="spack-user-4.0.0"
VERSION="spack-user-5.0.0"

export SPACK_USER_PREFIX="${SCRIPT_DIRECTORY}/Configuration.${VERSION}"
export SPACK_USER_CACHE_PATH="${SPACK_USER_PREFIX}/cache"

module purge
module load develop
module load "${VERSION}"
module list

spack debug report
# # Following lines can be of use for user of our spack configuration before version 5.0.
# spack config --scope user update --yes-to-all packages
# spack config --scope user update --yes-to-all config
# spack config --scope user add 'packages:all:permissions:read:world'
# spack config --scope user add 'packages:all:permissions:write:group'
# spack config --scope user add 'concretizer:unify:true'
# spack config --scope user add 'modules:default:tcl:hash_length:4'
```

We recommend that you write this script into your `WORKDIR`, you can source it and install an application like below, taking the example of Charmpp:

```shell-session
$ spack install charmpp@7.0.0%gcc@13.2.1.generic~cuda~omp~papi+production~pthreads+shared+smp~syncft~tcp~tracing backend=netlrts build-target='charm++' build_system=generic pmi=none arch=linux-rhel8-zen3
$ # Then clean to minimize the number of small files
$ spack gc --yes-to-all
$ spack clean --all
```

For some software, the source is not publicly available. In such case, you should place it in a directory, go to this directory and execute `spack install` from it. If you have more troubles, contact [svp@cines.fr](mailto:svp%40cines.fr)

<a id="saving-some-inodes"></a>

#### Saving some inodes

User are often constrained by the number of inodes per storage area. Spack offers a tool that can automatically purge unneeded products such as build dependencies. A typical workflow would look like so:

```shell-session
$ spack -e MyEnv concretize --force
$ spack -e MyEnv install -j .. -p ..
$ spack -e MyEnv gc # <- Remove non runtime dependencies of explicit products.
```

<a id="further-reading"></a>

## Further reading

- [Spack documentation](https://spack.readthedocs.io/en/latest/)
- [Spack tutorial](https://spack.readthedocs.io/en/latest/tutorial.html)
- [Spack Source code](https://github.com/spack/spack)
