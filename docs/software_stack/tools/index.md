<!-- Source: https://dci.dci-gitlab.cines.fr/webextranet/software_stack/tools/index.html -->
<!-- Title: Tools -->

<a id="tools"></a>

<a id="adastra-software-stack-tools"></a>

# Tools

<a id="cines-spack-modules"></a>

## CINES Spack modules

CINES provides **tools** built using Spack. To access these products, check [this document](../cines_software_stack/spack.md#adastra-software-stack-cines-software-stack-spack-using) and or look at this [product catalog](../cines_software_stack/spack_products_catalog.md#adastra-software-stack-spack-product-catalog).

<a id="building-software"></a>

## Building software

A build system is a model of a project that represents artifacts and the dependencies between them (e.g., CMake, Bazel, Meson).

A build tool executes a DAG representing the actions encoded by the build system’s semantic (e.g., Bazel, make, ninja). That is, it launches say, the compiler and linker.

<a id="cmake"></a>

<a id="adastra-software-stack-tools-building-cmake"></a>

### CMake

CMake is a meta-build system. It is used to generate build system configuration files (Makefile, Ninja configuration file, etc.). A great documentation on *modern* CMake is [offered by Henry Schhreiner](https://cliutils.gitlab.io/modern-cmake).

CINES provides the latest CMake release available in the OS’s repositories. To get the very latest release, you can build CMake yourself or rely on `pip3`:

```shell-session
$ pip3 install --user --upgrade cmake
$ cmake --version
3.28.1 # The latest release as of 2024/01/01
```

**Note**

Using `pip` this way assume your `.bashrc` or `.bash_profile` correctly defines your path to include `~/.local/bin`.

**Note**

CMake < 3.28 was recognizing CrayClang as a Clang compiler (which it is). With CMake >= 3.28, it recognizes it as CrayClang.

**Note**

To debug CMake’s search for libraries, use the `--debug-find --trace-expand` flags.

<a id="cmake-examples"></a>

<a id="adastra-software-stack-tools-building-cmake-example"></a>

#### CMake examples

**Warning**

Before going into further detail, know that it is possible to bypass the Cray compiler wrapper by explicitly adding compiler flags. This generally takes the form of: `-DCMAKE_CXX_FLAGS="$(CC --cray-print-opts)"` for CMake configurations. Note that using this method as is, you’ll get a lot of `-Wunused-command-line-argument` compiler warnings. This in inconvenient but harmless. See [this document](../../user_support/index.md#adastra-programming-environment-wrapper-flags-spewing) for more detail.

<a id="cmake-openmp"></a>

<a id="adastra-software-stack-tools-building-cmake-example-openmp"></a>

##### CMake + OpenMP

Assuming you have the following Genoa environment (which is very typical):

```shell-session
$ module purge
$ module load cpe/24.07
$ module load craype-x86-genoa
$ module load PrgEnv-cray
```

Assuming the following example CMake script:

```cmake
cmake_minimum_required(VERSION 3.12)
project(example VERSION 1.0 LANGUAGES CXX)

add_executable(example_binary example.cc)

find_package(OpenMP 4.0 REQUIRED)
target_link_libraries(example_binary PRIVATE OpenMP::OpenMP_CXX)
```

Use the following commands (do not forget the `CMAKE_CXX_COMPILER`):

```shell-session
$ mkdir -p build && cd build
$ cmake -DCMAKE_CXX_COMPILER=CC ..
```

When using the Cray wrappers and `craype-accel-amd-gfx90a`, CMake is known to have some issues with Cray’s GPU offload implementation’s special linker, the CCE OpenMP offload linker (COOL): `cce_omp_offload_linker`. This causes link time issues or false positive (running on GPU).

Example linker issue:

```
FAILED: example_binary
: && /opt/cray/pe/craype/2.7.30/bin/CC  -dynamic CMakeFiles/example_binary.dir/example.cc.o -o example_binary   && :
ld.lld: error: undefined symbol: _cray$mt_kmpc_fork_call_with_flags
>>> referenced by example.cc
>>>               CMakeFiles/example_binary.dir/example.cc.o:(main)
clang++: error: linker command failed with exit code 1 (use -v to see invocation)
```

We propose a work around, assuming you have the following MI250 environment (which is very typical):

```shell-session
$ module purge
$ module load cpe/24.07
$ module load craype-x86-trento craype-accel-amd-gfx90a # <- note the craype-accel-amd-gfx90a
$ module load PrgEnv-cray
$ module load amd-mixed
```

Now, at least two situation arise, either you **want** OpenMP offloading (`#pragma omp target`), or you do **not**. In the second situation, you may have loaded `craype-accel-amd-gfx90a` for the Cray wrappers to link correctly with a library like MPI, LibSci but do **not** need OpenMP offloading.

If you are in the **first situation** you should use CMake like that (force the `-fopenmp` flag at link time):

```shell-session
$ mkdir -p build && cd build
$ cmake -DCMAKE_CXX_COMPILER=CC -DCMAKE_EXE_LINKER_FLAGS="-fopenmp" ..
```

If you are in the **second situation**:

```shell-session
$ mkdir -p build && cd build
$ cmake -DCMAKE_CXX_COMPILER=CC -DCMAKE_LINKER="${CC_X86_64}/bin/cce_omp_offload_linker" ..
```

<a id="cmake-cray-mpich"></a>

##### CMake + Cray MPICH

Assuming you have the following environment (which is very typical):

```shell-session
$ module purge
$ module load cpe/24.07
$ module load craype-x86-trento craype-accel-amd-gfx90a
$ module load PrgEnv-cray
```

Assuming the following example CMake script:

```cmake
cmake_minimum_required(VERSION 3.12)
project(example VERSION 1.0 LANGUAGES CXX)

add_executable(example_binary example.cc)

find_package(MPI REQUIRED)
target_link_libraries(example_binary PRIVATE MPI::MPI_CXX)
```

Use the following commands (do not forget the `CMAKE_CXX_COMPILER`):

```shell-session
$ mkdir -p build && cd build
$ cmake -DCMAKE_CXX_COMPILER=CC ..
```

Had you not used the Cray wrappers (here the raw Cray C++ compiler `crayCC`), the following commands would have been an alternative:

```shell-session
$ mkdir build && cd build
$ CRAY_WRAPPER_LINK_FLAGS="$({ CC --cray-print-opts=libs; } | tr '\n' ' ' | sed -e 's/-Wl,--as-needed,//g' -e 's/,--no-as-needed//g')"
$ cmake \
      -DCMAKE_CXX_COMPILER=crayCC \
      -DCMAKE_CXX_FLAGS="$(CC --cray-print-opts=cflags)" \
      -DCMAKE_EXE_LINKER_FLAGS="${CRAY_WRAPPER_LINK_FLAGS}" \
      ..
```

<a id="cmake-cray-hdf5-cray-wrappers"></a>

##### CMake + Cray HDF5 + Cray wrappers

Assuming you have the following environment (which is very typical):

```shell-session
$ module purge
$ module load cpe/24.07
$ module load craype-accel-amd-gfx90a craype-x86-trento
$ module load PrgEnv-amd
$ module load cray-hdf5
```

Assuming the following example CMake script:

```cmake
cmake_minimum_required(VERSION 3.12)
project(example VERSION 1.0 LANGUAGES CXX)

add_executable(example_binary example.cc)

# This variable does not affect the build when using the Cray wrappers!
# set(HDF5_PREFER_PARALLEL TRUE)
find_package(HDF5 REQUIRED COMPONENTS C)
target_link_libraries(example_binary PRIVATE HDF5::HDF5)
```

Use the following commands (do not forget the `CMAKE_CXX_COMPILER`):

```shell-session
$ mkdir -p build && cd build
$ cmake -DCMAKE_CXX_COMPILER=CC ..
```

**Note**

The process is the same for `cray-hdf5-parallel`, just swap the HDF5 modules.

<a id="cmake-cray-hdf5-raw-compilers"></a>

##### CMake + Cray HDF5 + raw compilers

**Note**

There is an issue with the HDF5 wrappers (h5fc, h5cc et h5c++ et h5pcc, h5pfc etc.) provided by Cray. Make sure you workaround the issue as described below.

Assuming you have the following environment (which is very typical):

```shell-session
$ module purge
$ module load cpe/24.07
$ module load craype-accel-amd-gfx90a craype-x86-trento
$ module load PrgEnv-amd
$ module load cray-hdf5
```

Assuming the following example CMake script:

```cmake
cmake_minimum_required(VERSION 3.12)
project(example VERSION 1.0 LANGUAGES CXX)

add_executable(example_binary example.cc)

find_package(HDF5 REQUIRED COMPONENTS C)
target_link_libraries(example_binary PRIVATE HDF5::HDF5)
```

Use the following commands (do not forget the `CMAKE_CXX_COMPILER`):

```shell-session
$ mkdir -p build && cd build
$ CRAY_WRAPPER_LINK_FLAGS="$({ CC --cray-print-opts=libs; } | tr '\n' ' ' | sed -e 's/-Wl,--as-needed,//g' -e 's/,--no-as-needed//g')"
$ cmake \
      -DCMAKE_CXX_COMPILER=amdclang++ \
      -DCMAKE_CXX_FLAGS="$(CC --cray-print-opts=cflags)" \
      -DCMAKE_EXE_LINKER_FLAGS="${CRAY_WRAPPER_LINK_FLAGS}" \
      ..
```

**Note**

The process is the same for `cray-hdf5-parallel`, just swap the HDF5 modules.

<a id="cmake-kokkos-hip-openmp"></a>

<a id="adastra-software-stack-tools-building-cmake-example-kk-hip-openmp"></a>

##### CMake + Kokkos HIP + OpenMP

Compiling Kokkos with a HIP backend for MI250X and an OpenMP backend for CPUs:

```shell-session
$ module purge
$ module load cpe/24.07
$ module load craype-x86-trento craype-accel-amd-gfx90a
$ module load PrgEnv-cray
$ module load amd-mixed
$ module list

$ git clone -b 4.2.00 https://github.com/kokkos/kokkos.git
$ cd kokkos

$ cmake \
      -DCMAKE_CXX_COMPILER=CC \
      -DCMAKE_CXX_STANDARD=17 \
      -DKokkos_ENABLE_HIP=ON \
      -DKokkos_ARCH_AMD_GFX90A=ON \
      -DKokkos_ENABLE_OPENMP=ON \
      ..
$ cmake --build build --clean-first --parallel 128
```

If you want to use the raw `amdclang++` or `hipcc` compiler, you could use this CMake configuration line:

```shell-session
$ CRAY_WRAPPER_LINK_FLAGS="$({ CC --cray-print-opts=libs; } | tr '\n' ' ' | sed -e 's/-Wl,--as-needed,//g' -e 's/,--no-as-needed//g')"
$ cmake \
      -DCMAKE_CXX_COMPILER=hipcc \
      -DCMAKE_CXX_FLAGS="$(CC --cray-print-opts=cflags)" \
      -DCMAKE_EXE_LINKER_FLAGS="${CRAY_WRAPPER_LINK_FLAGS}" \
      -DCMAKE_CXX_STANDARD=17 \
      -DKokkos_ENABLE_HIP=ON \
      -DKokkos_ARCH_AMD_GFX90A=ON \
      -DKokkos_ENABLE_OPENMP=ON \
      ..
```

<a id="cmake-libsci"></a>

##### CMake + LibSci

Assuming you have the following environment (which is very typical):

```shell-session
$ module purge
$ module load cpe/24.07
$ module load craype-x86-trento craype-accel-amd-gfx90a
$ module load PrgEnv-cray
```

Assuming the following example CMake script:

```cmake
cmake_minimum_required(VERSION 3.12)
project(example VERSION 1.0 LANGUAGES CXX)

add_executable(example_binary example.cc)

find_package(BLAS REQUIRED)
target_link_libraries(example_binary PRIVATE BLAS::BLAS)
```

Use the following commands (do not forget the `CMAKE_CXX_COMPILER`):

```shell-session
$ mkdir -p build && cd build
$ cmake -DCMAKE_CXX_COMPILER=CC ..
```

Had you not used the Cray wrappers (here the raw Cray C++ compiler `crayCC`), the following commands would have been an alternative:

```shell-session
$ mkdir build && cd build
$ CRAY_WRAPPER_LINK_FLAGS="$({ CC --cray-print-opts=libs; } | tr '\n' ' ' | sed -e 's/-Wl,--as-needed,//g' -e 's/,--no-as-needed//g')"
$ cmake \
     -DCMAKE_CXX_COMPILER=crayCC \
     -DCMAKE_CXX_FLAGS="$(CC --cray-print-opts=cflags)" \
     -DBLAS_LIBRARIES="${CRAY_WRAPPER_LINK_FLAGS}" \
     -DLAPACK_LIBRARIES="${CRAY_WRAPPER_LINK_FLAGS}" \
     ..
```

<a id="ninja"></a>

<a id="adastra-software-stack-tools-building-ninja"></a>

### Ninja

[Ninja](https://ninja-build.org/manual.html) is yet another build system. It takes as input the interdependencies of files (typically source code and output executables) and orchestrates building them, *quickly*. It plays a similar role to GNU Make but without most of the clutter. It is simpler, faster, more reliable. You should not write Ninja configuration files like you may do for Makefiles. Instead, rely on a meta-build system such as CMake, Meson, etc..

To install Ninja on any machine (assuming you have `pip3` installed):

```shell-session
$ pip3 install --user --upgrade ninja
```

To ask CMake to use Ninja:

```shell-session
$ cmake -GNinja <your_other_flags>
```

<a id="conda"></a>

## Conda

CINES proposes a `conda` module:

```shell-session
$ module load conda
```

**Note**

CINES uses a package cache.

<a id="debugging"></a>

## Debugging

<a id="cray-tools"></a>

### Cray tools

**Warning**

Theses tools are known to be clunky and poorly tested. Use theme at your own risk. We expose these into the documentation mostly to inform the user of the concepts related to these tools, not because we want you to use them…

<a id="stack-track-analysis-tool"></a>

#### Stack Track Analysis Tool

It’s a lightweight, highly scalable tool that collects and merges the stack traces of all processes in a parallel application at runtime. It creates a result directory in the application’s working directory. This directory contains the merged stack traces, which can be viewed using the statview graphical interface. STAT supports applications using the MPI, SHMEM, UPC and Fortran Coarrays programming models. There’s no need to recompile applications or enable special compiler debugging options that would potentially disable optimization. Compilation with DWARF options enabled is required to issue function names in the stack trace.

Cray’s [Stack Trace Analysis Tool (STAT)](https://web.archive.org/web/20231126220622/https://cpe.ext.hpe.com/docs/guides/CPE/HPE_CPE_User_Guide_Apollo_2000_Gen10_Plus_x86_Systems_23.09_S-8008.html#debug-hung-applications-with-stat) documentation.

<a id="abnormal-termination-process-atp"></a>

#### Abnormal Termination Process (ATP)

This is a system that monitors users’ running applications. If an application enters a system trap, ATP performs an analysis of the faulty application. All application process traces are collected in a merged “stack traces” tree and written to disk. The backtrack tree of the first process to terminate is sent to stderr, along with the number of the signal that caused the application to stop. If core dumping is enabled in the Linux kernel, a set of heuristically selected processes will also be dumped. ATP supports sequential and parallel applications using the MPI, Cray SHMEM, OpenMP, UPC and Fortran Coarrays programming models. The merged backtrace tree provides a scalable, comprehensive view of the application’s state at shutdown. ATP can be leveraged by adding a library of when editing links, or by using the preloading mechanism (LD_PRELOAD) in the case of dynamically linked applications. It is also possible to programmatically trigger the display of the call stack at any time.

Cray’s [Abnormal Termination Processing (ATP)](https://web.archive.org/web/20231126220622/https://cpe.ext.hpe.com/docs/guides/CPE/HPE_CPE_User_Guide_Apollo_2000_Gen10_Plus_x86_Systems_23.09_S-8008.html#debug-crashed-applications-with-atp) documentation.

<a id="cray-comparative-debugger"></a>

#### Cray Comparative Debugger

This is the data-centric debugging tool originally developed by Cray. CCDB features a graphical interface that extends GDB4HPC’s comparative debugging capabilities, making it easy to compare data structures between two running applications. When the values of selected data structures diverge, this may be an error, and the user is alerted. This capability is useful for locating errors introduced when applications are modified by code, compiler or library changes. It is also useful for porting applications to new architectures or programming models.

<a id="gdb4hpc"></a>

<a id="adastra-software-stack-tools-debugging-cray-tools-gdb4hpc"></a>

#### GDB4HPC

An introduction guide on using GDB4HPC is given in [debugging a hung application](https://web.archive.org/web/20231126220622/https://cpe.ext.hpe.com/docs/guides/CPE/HPE_CPE_User_Guide_Apollo_2000_Gen10_Plus_x86_Systems_23.09_S-8008.html#debug-a-hung-application-using-gdb4hpc) or [crashed application](https://web.archive.org/web/20231126220622/https://cpe.ext.hpe.com/docs/guides/CPE/HPE_CPE_User_Guide_Apollo_2000_Gen10_Plus_x86_Systems_23.09_S-8008.html#debug-crashing-applications-with-gdb4hpc) using GDB4HPC.

<a id="valgrind4hpc"></a>

#### Valgrind4HPC

Cray provides the valgrind4HPC tool and [documents its use in this document](https://cpe.ext.hpe.com/docs/latest/debugging-tools/valgrind4hpc/guides/user_guide.html).

<a id="ddt"></a>

### DDT

Linaro DDT is a used for debugging MPI and OpenMP (CPU) program with increasing support for GPU kernel debugging. Linaro provides [videos](https://www.youtube.com/playlist?list=PLKZSArYQptsO7Vfl5UJfWdzdVgmVA848q) to learn the tool.

To use DDT, CINES proposes a module. First on a login node, execute the following:

```shell-session
$ module load ddt
$ ddt
```

In the GUI’s `options>system`, choose `MPI/UPC implementation: Auto-Detect`.

We recommend that you use the command line to launch the ddt server. In your `sbatch` file, execute the following:

```shell-session
$ module load ddt
$ ddt --connect srun <my_slurm_options> -- ./my_program
```

At this point, the GUI will notify that it has detected the server and prompt you with the following popup:

[![../../_images/ddt_popup.png](https://dci.dci-gitlab.cines.fr/webextranet/_images/ddt_popup.png)](https://dci.dci-gitlab.cines.fr/webextranet/_images/ddt_popup.png)

Press accept and then check the boxes corresponding to the properties you whish to track:

[![../../_images/ddt_popup2.png](https://dci.dci-gitlab.cines.fr/webextranet/_images/ddt_popup2.png)](https://dci.dci-gitlab.cines.fr/webextranet/_images/ddt_popup2.png)

We currently provide the following ways to use DDT:

- Via X11 (very latency sensitive);
- Via HPDA nodes (see [Data visualization and analytics](../../data_visualization_and_analytics/index.md#visualization));
- Via port forwarding multiplexed through VSCode.

<a id="gdb"></a>

### GDB

GDB is the defacto, system programming debugger. It requires quite a lot of skill to get anything out of it on real world problems (notably if you do not have access to the source). If you plan to use it, make sure that, regardless of the level of optimization you specify to your compiler, you ship the debug info too. This is generally done using `-ggdb` on GCC and LLVM based compilers.

**Note**

If you are a novice, you may be better off using [ChatGDB](../../other/cines_virtual_assistant.md#adastra-other-cines-virtual-assistant) with a prompt such as *What the root cause of this error is? Given the following source code context and propose a fix. In your response, always refer only to specific lines and filenames of source code.*.

<a id="rocgdb"></a>

### rocGDB

Based on the GNU debugger, it allows you to step instruction by instruction (with limitations) into a AMD GPU program (*kernel*). Slides explaining how to use rocGDB are [`made available here`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/189a11ef04d2fc20df56f50066d27652/rocgdb_tutorial.pdf).

<a id="valgrind"></a>

### Valgrind

You may also use tools such as or [Dr. Memory](https://drmemory.org/) or [Valgrind](https://valgrind.org/). Note that these tools’ functionalities is not limited to memory leak detection. As an example Valgrind provides tools to observe cache misses.

To check for memory leaks:

```shell-session
$ valgrind -- ./my_program
```

**Note**

Tools such as Valgrind basically emulate the CPU, the program under test runs in a sandbox. The advantage being that the host (say, Valgrind) is omniscient and can thus, catch calls to say, `malloc` and deduce if the memory was accessed out of bound or even, not released. This emulation method is expensive and the program may experience slowdowns ranging from x5 to x40. For this reason, we **strongly** recommend running your everyday tests under the more lightweight sanitizer such as the ones presented [here](index.md#adastra-software-stack-tools-debugging-sanitizer).

<a id="sanitizers"></a>

<a id="adastra-software-stack-tools-debugging-sanitizer"></a>

### Sanitizers

Compiler toolchains such as GCC or LLVM provide sanitizers (runtime advanced diagnostics) for the C and C++ compilers. On Clang or GCC based compilers, you would use `-fsanitize=address` to check for memory leaks. There are more sanitizer available: for the detection of undefined behavior, race condition or uninitialized memory usage. Do not hesitate to read the Clang [address](https://github.com/google/sanitizers/wiki/AddressSanitizer) and [memory](https://github.com/google/sanitizers/wiki/MemorySanitizer) sanitizer documentation.

<a id="ldd-and-nm"></a>

### `ldd` and `nm`

`ldd` prints shared library dependencies. Can be used to check if all shared object dependencies are satisfied. `ldd` is recursive and does not stop at the first level of the dependency tree.

`nm` lists symbols from object files. This is useful to diagnose undefined reference issue. you have to de-mangle C++ symbols. For that, you can pipe `nm` into the `c++filt` h command.

<a id="gstack"></a>

### `gstack`

Prints a stack trace of a running process. Can be used in conjunction with `watch` to observe how the stack evolves.

```shell-session
$ watch -n0 -- "gstack <pid>"
```

<a id="julia"></a>

<a id="adastra-software-stack-tools-julia"></a>

## Julia

[Julia](https://julialang.org/) defines itself like so:

```
Scientific computing has traditionally required the highest performance, yet domain experts have largely moved to slower dynamic languages for daily work. We believe there are many good reasons to prefer dynamic languages for these applications, and we do not expect their use to diminish. Fortunately, modern language design and compiler techniques make it possible to mostly eliminate the performance trade-off and provide a single environment productive enough for prototyping and efficient enough for deploying performance-intensive applications. The Julia programming language fills this role: it is a flexible dynamic language, appropriate for scientific and numerical computing, with performance comparable to traditional statically-typed languages.
```

While the performance aspect is not entirely founded, it is undeniably a better solution than using Python to do scientific computation, scripting, pre/post-processing.

If you can, we recommend that you use Julia instead of Python. In the long run, you should make a better use of HPC resources.

<a id="jupyter"></a>

<a id="adastra-software-stack-tools-jupyter"></a>

## Jupyter

You use Jupyter, a free software, open standards, and web services for interactive computing across all programming languages on Adastra, follow this procedure:

- Connect to an [HPDA node](../../data_visualization_and_analytics/index.md#visualization-hpda-remote-desktop);
- Click on **JupyterLab**.

[![../../_images/jupyterlab.PNG](https://dci.dci-gitlab.cines.fr/webextranet/_images/jupyterlab.PNG)](https://dci.dci-gitlab.cines.fr/webextranet/_images/jupyterlab.PNG)

**Note**

Only one instance of JupyterLab can be launched on HPDA nodes.
Attempting to open multiple sessions may result in the following error:
`Firefox is already running, but is not responding. To use Firefox, you must first close the existing Firefox process, restart your device, or use a different profile.`

<a id="linker-assembly-abi"></a>

## Linker, assembly, ABI

<a id="objdump"></a>

### `objdump`

`objdump` displays information about one or more object files. The options control what particular information to display.

```shell-session
$ objdump -M intel -S aws-ofi-rccl-test/build/all_reduce_perf

aws-ofi-rccl-test/build/all_reduce_perf:     file format elf64-x86-64

Disassembly of section .text:

000000000031f9e0 <_start>:
31f9e0:       f3 0f 1e fa             endbr64
31f9e4:       31 ed                   xor    ebp,ebp
31f9e6:       49 89 d1                mov    r9,rdx
31f9e9:       5e                      pop    rsi
31f9ea:       48 89 e2                mov    rdx,rsp
31f9ed:       48 83 e4 f0             and    rsp,0xfffffffffffffff0
31f9f1:       50                      push   rax
31f9f2:       54                      push   rsp
31f9f3:       4c 8d 05 06 66 02 00    lea    r8,[rip+0x26606]        # 346000 <__libc_csu_fini>
31f9fa:       48 8d 0d 8f 65 02 00    lea    rcx,[rip+0x2658f]        # 345f90 <__libc_csu_init>
31fa01:       48 8d 3d d8 5d 00 00    lea    rdi,[rip+0x5dd8]        # 3257e0 <main>
31fa08:       ff 15 c2 7e 02 00       call   QWORD PTR [rip+0x27ec2]        # 3478d0 <__libc_start_main@GLIBC_2.2.5>
31fa0e:       f4                      hlt
...
```

<a id="ld-linux-so"></a>

### `ld-linux.so`

<a id="environment-variable"></a>

#### Environment variable

- `LD_DEBUG=libs` Output verbose debugging information about operation of the dynamic linker. With `libs`: Display library search paths.
- `LD_PRELOAD=` A list of additional, user-specified, ELF shared objects to be loaded before all others.
- `LD_LIBRARY_PATH=` A list of directories in which to search for ELF libraries at execution time.

<a id="ldd"></a>

#### `ldd`

`ldd` prints the shared objects (shared libraries) required by each program or shared object specified on the command line. An example of its use and output is the following:

```shell-session
$ ldd /bin/ls
linux-vdso.so.1 (0x00007ffcc3563000)
libselinux.so.1 => /lib64/libselinux.so.1 (0x00007f87e5459000)
libcap.so.2 => /lib64/libcap.so.2 (0x00007f87e5254000)
libc.so.6 => /lib64/libc.so.6 (0x00007f87e4e92000)
libpcre.so.1 => /lib64/libpcre.so.1 (0x00007f87e4c22000)
libdl.so.2 => /lib64/libdl.so.2 (0x00007f87e4a1e000)
/lib64/ld-linux-x86-64.so.2 (0x00005574bf12e000)
libattr.so.1 => /lib64/libattr.so.1 (0x00007f87e4817000)
libpthread.so.0 => /lib64/libpthread.so.0 (0x00007f87e45fa000)
```

<a id="libtree"></a>

#### libtree

Libtree is a more versatile `ldd`. Available here: <https://github.com/haampie/libtree>

```shell-session
$ libtree aws-ofi-rccl-test/build/all_reduce_perf
aws-ofi-rccl-test/build/all_reduce_perf
├── libhsa-runtime64.so.1 [runpath]
│   ├── librocprofiler-register.so.0 [runpath]
│   │   └── libpthread.so.0 [default path]
│   ├── libdrm_amdgpu.so.1 [ld.so.conf]
│   │   ├── libdrm.so.2 [ld.so.conf]
│   │   └── libpthread.so.0 [default path]
│   ├── libdrm.so.2 [ld.so.conf]
│   ├── libelf.so.1 [default path]
│   │   ├── libz.so.1 [default path]
│   │   ├── libbz2.so.1 [default path]
│   │   ├── liblzma.so.5 [default path]
│   │   │   └── libpthread.so.0 [default path]
│   │   └── libzstd.so.1 [default path]
│   ├── librt.so.1 [default path]
│   │   └── libpthread.so.0 [default path]
│   ├── libpthread.so.0 [default path]
│   └── libnuma.so.1 [default path]
├── librccl.so.1 [runpath]
│   ├── librocm_smi64.so.7 [runpath]
│   │   ├── libpthread.so.0 [default path]
│   │   └── librt.so.1 [default path]
│   ├── libamdhip64.so.6 [runpath]
│   │   ├── librocprofiler-register.so.0 [runpath]
│   │   ├── libamd_comgr.so.2 [runpath]
│   │   │   ├── libpthread.so.0 [default path]
│   │   │   ├── libzstd.so.1 [default path]
│   │   │   ├── libz.so.1 [default path]
│   │   │   ├── libtinfo.so.6 [default path]
│   │   │   └── librt.so.1 [default path]
│   │   ├── libhsa-runtime64.so.1 [runpath]
│   │   ├── libpthread.so.0 [default path]
│   │   ├── librt.so.1 [default path]
│   │   └── libnuma.so.1 [default path]
│   ├── librt.so.1 [default path]
│   └── libpthread.so.0 [default path]
├── libamdhip64.so.6 [runpath]
├── libmpi_gnu_112.so.12 [ld.so.conf]
│   ├── libfabric.so.1 [LD_LIBRARY_PATH]
│   │   ├── libcxi.so.1 [default path]
│   │   │   └── libnl-3.so.200 [default path]
│   │   │       └── libpthread.so.0 [default path]
│   │   ├── librt.so.1 [default path]
│   │   ├── libatomic.so.1 [default path]
│   │   │   └── libpthread.so.0 [default path]
│   │   └── libpthread.so.0 [default path]
│   ├── libpmi.so.0 [ld.so.conf]
│   │   ├── libpals.so.0 [ld.so.conf]
│   │   │   └── libjansson.so.4 [default path]
│   │   └── libpthread.so.0 [default path]
│   ├── libpmi2.so.0 [ld.so.conf]
│   │   ├── libpals.so.0 [ld.so.conf]
│   │   └── libpthread.so.0 [default path]
│   ├── libquadmath.so.0 [ld.so.conf]
│   ├── libgfortran.so.5 [default path]
│   │   ├── libquadmath.so.0 [ld.so.conf]
│   │   └── libz.so.1 [default path]
│   ├── libpthread.so.0 [default path]
│   └── librt.so.1 [default path]
├── libpthread.so.0 [default path]
└── librt.so.1 [default path]
```

<a id="monitoring"></a>

## Monitoring

<a id="htop"></a>

<a id="adastra-software-stack-tools-monitoring-htop"></a>

### `htop`

An interactive process viewer. This is useful to monitor how your program uses the machine. A typical workflow would be to start a job using say, `sbatch`, do an `squeue --me` to obtain the list of node associated to the job. Select a node from the list and connect to it using `ssh <node_hostname>`. Do `htop`.

**Warning**

When you launch this tool for the first time, you might get surprised by the layout due to the *unfortunately* huge amount of cores on Adastra’s login and Genoa nodes. This requires some layout tuning to get a proper reading. Check the configuration below to workaround the issue.

Example configuration to place into `~/.config/htop/htoprc`

```
# Beware! This file is rewritten by htop when settings are changed in the interface.
# The parser is also very primitive, and not human-friendly.
fields=0 48 17 114 18 38 39 40 2 113 46 47 49 1
sort_key=46
sort_direction=1
tree_sort_key=49
tree_sort_direction=1
hide_kernel_threads=1
hide_userland_threads=1
shadow_other_users=0
show_thread_names=0
show_program_path=0
highlight_base_name=1
highlight_megabytes=1
highlight_threads=1
highlight_changes=0
highlight_changes_delay_secs=5
find_comm_in_cmdline=1
strip_exe_from_cmdline=1
show_merged_command=0
tree_view=1
tree_view_always_by_pid=0
header_margin=1
detailed_cpu_time=1
cpu_count_from_one=0
show_cpu_usage=1
show_cpu_frequency=0
update_process_names=0
account_guest_in_cpu_meter=0
color_scheme=0
enable_mouse=1
delay=15
left_meters=LeftCPUs8 Memory Swap NetworkIO DiskIO
left_meter_modes=1 1 1 2 2
right_meters=RightCPUs8 Hostname Tasks LoadAverage Uptime SELinux
right_meter_modes=1 2 2 2 2 2
hide_function_bar=0
```

<a id="rocmsmi"></a>

<a id="adastra-software-stack-tools-monitoring-rocmsmi"></a>

### `rocmsmi`

**Note**

It is somewhat equivalent to NVIDIA’s `nvidia-smi`.

One can load the `amd-mixed` module and use the `rocm-smi` command. A typical workflow would be to start a job using say, `sbatch`, do an `squeue --me` to obtain the list of node associated to the job. Select a node from the list and connect to it using `ssh <node_hostname>`. Do `module load amd-mixed` and `watch -n0 -- rocm-smi`.

It will give you the following output:

```shell-session
$ watch -- rocm-smi
Every 0.1s: rocm-smi                            <node>: <date>

======================= ROCm System Management Interface =======================
================================= Concise Info =================================
GPU  Temp   AvgPwr  SCLK     MCLK     Fan  Perf  PwrCap  VRAM%  GPU%
0    63.0c  444.0W  1700Mhz  1600Mhz  0%   auto  560.0W   30%   100%
1    58.0c  N/A     1700Mhz  1600Mhz  0%   auto  0.0W     30%   100%
2    63.0c  465.0W  1700Mhz  1600Mhz  0%   auto  560.0W   30%   100%
3    69.0c  N/A     1700Mhz  1600Mhz  0%   auto  0.0W     30%   100%
4    58.0c  443.0W  1700Mhz  1600Mhz  0%   auto  560.0W   30%   100%
5    57.0c  N/A     1700Mhz  1600Mhz  0%   auto  0.0W     30%   100%
6    68.0c  460.0W  1700Mhz  1600Mhz  0%   auto  560.0W   30%   100%
7    64.0c  N/A     1700Mhz  1600Mhz  0%   auto  0.0W     30%   99%
================================================================================
============================= End of ROCm SMI Log ==============================
```

In addition is can be a trove of information regarding the hardware topology (BUS, PCIe, etc.).

<a id="paraview-vtk"></a>

<a id="adastra-software-stack-tools-paraview"></a>

## ParaView & VTK

ParaView is exposed through modules:

```shell-session
$ module spider paraview
-----------------------------------------
paraview:
-----------------------------------------
    Versions:
        paraview/5.13.0
        paraview/5.13.0-osmesa
```

The versions will evolve in time.

- If you want interactive visualization (say, moving around in a volume) we recommend HPDA nodes and the `paraview/X.Y.Z` module.
- If you want non interactive visualization (say, saving screenshot of loaded data) we recommend the GENOA shared nodes (or HPDA if you do not have GENOA CPU hours) and the `paraview/X.Y.Z-osmesa` module.

The HPDA nodes offer large amount of memory and GPUs designed to handle large visualization tasks. If you do not need GPUs or 2 Tio of RAM, you may want to use the GENOA nodes instead.

The `osmesa` version (for headless machines) is to be used in case you use scripts that will run without a X11 server. That is **without** `ssh -XY` and **not on** the [HPDA visualization platform](../../data_visualization_and_analytics/index.md#visualization-hpda-remote-desktop). If you use `paraview/5.13.0` (the non `osmesa` version) in a sbatch script, you will get the following error:

```
(  36.706s) [pvbatch         ]vtkXOpenGLRenderWindow.:459    ERR| vtkXOpenGLRenderWindow (0x46bc060): bad X server connection. DISPLAY=.... Aborting
```

<a id="profiling"></a>

## Profiling

<a id="cray-pat-s-perftools"></a>

<a id="adastra-software-stack-tools-profiling-perftools"></a>

### Cray-PAT’s `perftools`

Introducing Cray-PAT can be done in multiple ways. First ensure the `perftools-base` module is loaded. Then load a `perftools-lite*` modules. They exist in flavor variation such as:

> - `perftools-lite`: Gives execution time, memory peak, most time-consuming functions, I/O read and write rates, and total energy consumed.
> - `perftools-lite-events`: Gives the time-consuming functions, MPI and OpenMP (CPU) information, as well as node observations and possible rank order suggestions.
> - `perftools-lite-gpu`: Gives kernel execution times, synchronization time, as well as data movement information (time and size of transfers).
> - `perftools-lite-loops`: Gives loop trip counts and execution times. The results of this profile can be used with Reveal. More on that Later.

**Note**

Cray provides some [documentation on using theses tools](https://cpe.ext.hpe.com/docs/guides/CPE/HPE_CPE_User_Guide_Apollo_2000_Gen10_Plus_x86_Systems_23.09_S-8008.html#profiling-an-application).

when the modules given above is loaded, **recompile your application using the Cray wrappers**. After executing the test case, a folder is created in the working directory in use when you launched the application. At the end of the execution, perftools also print partial results to the standard output. A sample of such output could look like this:

```
#################################################################
#                                                               #
#            CrayPat-lite Performance Statistics                #
#                                                               #
#################################################################
CrayPat/X:  Version 22.04.0 Revision 044b9fa85  03/10/22 21:59:07
Experiment:                  lite  lite-samples
Number of PEs (MPI ranks):      1
Numbers of PEs per Node:        1
Numbers of Threads per PE:      1
Number of Cores per Socket:    64
Accelerator Model: AMD MI100 Memory: 32.00 GB Frequency: 1.00 GHz
Execution start time:  Tue May 31 10:23:14 2022
System name and speed:  g1003  2.304 GHz (nominal)
AMD   Trento               CPU  Family: 25  Model: 48  Stepping:  1
Core Performance Boost:  1 PE has CPB capability
Avg Process Time:      57.62 secs
High Memory:         2,598.3 MiBytes     2,598.3 MiBytes per PE
I/O Write Rate:   108.928487 MiBytes/sec
Notes for table 1:
This table shows functions that have significant exclusive sample
hits, averaged across ranks.
For further explanation, see the "General table notes" below,
or use:  pat_report -v -O samp_profile ...
Table 1:  Profile by Function
Samp% |    Samp | Imb. |  Imb. | Group
|         | Samp | Samp% |  Function=[MAX10]
100.0% | 2,234.0 |   -- |    -- | Total
|---------------------------------------------------------
|  67.0% | 1,497.0 |   -- |    -- | ETC
||--------------------------------------------------------
||  36.5% |   815.0 |   -- |    -- | __sci_sgemv_
||  16.0% |   357.0 |   -- |    -- | openblas_sgemv_t_naples
||   8.6% |   192.0 |   -- |    -- | sgemv_kernel_4x2
||   3.4% |    76.0 |   -- |    -- | cblas_sgemv
||   1.9% |    42.0 |   -- |    -- | sgemv_kernel_4x1
||========================================================
|  32.9% |   735.0 |   -- |    -- | USER
||--------------------------------------------------------
||  26.3% |   588.0 |   -- |    -- | main
||   2.3% |    52.0 |   -- |    -- | matrix
||   2.2% |    49.0 |   -- |    -- | WriteHdf5MeshFile2D
||   1.2% |    27.0 |   -- |    -- | Compute_Epsi
|=========================================================
```

You can observe in which function the time is spent. The time presented here, in percentage and samples, is exclusive. Meaning that, if you imagine the history if the call stack as a rooted tree (graph theory) the time spent in a function (a vertex) does not account for the time spent in the callee (children vertices).

In the example shown above, most of the time is spent in `__sci_sgemv_` a BLAS API to compute a matrix-vector operation.

<a id="instrumenting-an-already-existing-executable-binary"></a>

#### Instrumenting an already existing executable binary

Cray offers the `pat_build` command that can be used to instrument already compiled codes. Still, one must make sure that the `perftools-base` and `perftools` modules were loaded during compilation. Then, to instrument the binary, one case do the following:

```shell-session
$ pat_build -g <trace_group> -f <path_to_original_binary> -o <path_to_instrumented_binary>
```

You are to specify what you would like to profile using a `trace-group`. The values it can take are given below (you can use multiple separated by a comma):

```
adios2
    Adaptable Input Output System Version 2
aio
    Functions that perform asynchronous I/O.
blacs
    Basic Linear Algebra communication subprograms
blas
    Basic Linear Algebra subprograms
caf
    Co-Array Fortran (CCE compiler only)
charm++
    Charm++ independent parallel programming system (deprecated)
comex
    Communications Runtime for Extreme Scale
converse
    Charm++ Converse low-level message passing API (deprecated)
craymem
    Cray memory allocation with attributes
cuda
    NVidia Compute Unified Device Architecture runtime and driver API
curl
    Multi-protocol file transfer API
dl
    functions that manage dynamic linking
dmapp
    Distributed Memory Application API
fabric
    Open network communication services API
ffio
    functions that perform Flexible File I/O (CCE compiler only)
fftw
    Fast Fourier Transform library (32- and 64-bit only)
ga
    Global Arrays API
gmp
    GNU MultiPrecision Arithmetic Library
gni
    Generic Network Interface API
hbw
    High Bandwidth Memory API
hdf5
    Hierarchical Data Format library
heap
    dynamic heap
hip
    AMD Heterogeneous-compute Interface for Portability runtime API
hsa
    AMD Heterogeneous System Architecture API
huge
    Linux huge pages
io
    functions and system calls that perform I/O
jemalloc
    heap allocation emphasizing fragmentation avoidance and scalable concurrency
lapack
    Linear Algebra Package
lustre
    Lustre User API
math
    POSIX.1 math functions
memkind
    User extensible heap manager API
memory
    memory management operations
mpfr
    GNU MultiPrecision Floating-Point Library
mpi
    Message Passing Interface library
netcdf
    Network Common Data Form
numa
    Non-uniform Memory Access API (see numa(3))
oacc
    OpenAccelerator API
omp
    OpenMP API
opencl
    Open Computing Language API
pblas
    Parallel Basic Linear Algebra Subroutines
petsc
    Portable Extensible Toolkit for Scientific Computation. Supported for "real" computations only.
pgas
    Parallel Global Address Space
pnetcdf
    Parallel Network Common Data Form
pthreads
    POSIX threads
pthreads_mutex
    POSIX threads concurrent process control
pthreads_spin
    POSIX threads low-level synchronization control
realtime
    POSIX realtime extensions
scalapack
    Scalable LAPACK
shmem
    One-sided Remote Direct Memory Access Parallel-Processing Interface library
signal
    POSIX signal handling and control
spawn
    POSIX realtime process creation
stdio
    all library functions that accept or return the FILE* construct
string
    String operations
syscall
    system calls
sysfs
    system calls that perform miscellaneous file management
sysio
    system calls that perform I/O
umpire
    Heterogeneous Memory Resources Management Library
upc
    Unified Parallel C (CCE compiler only)
xpmem
    cross-process memory mapping
zmq
    High-performance asynchronous messaging API
```

For CPU profiling, a typical set of `trace-group` would be `mpi,syscall,io,omp` and for AMD GPUs: `mpi,syscall,io,hip`.

When the `instrumented_binary` is produced, you can use it similarly to the original binary. Profiling results will be output in `results_path` of the form `instrumented_binary+<PID>_<timestamp>s`. The folder is placed in the working directory of the executable.

You can finally use `pat_report -v <results_path>` and optionally, specify an option to orient what to report: `pat_report -v -O <report_option> <results_path>`. the report options are given below. Note that not all report options are available for a given profile. Indeed, you have to record the appropriate information first to be able to report it. Do not expect MPI information from an OpenMP profile.

```
accelerator
    Show calltree of accelerator performance data sorted by host time.
accpc
    Show accelerator performance counters.
acc_fu
    Show accelerator performance data sorted by host time.
acc_time_fu
    Show accelerator performance data sorted by accelerator time.
acc_time
    Show calltree of accelerator performance data sorted by accelerator time.
acc_show_by_ct
    (Deferred implementation) Show accelerator performance data sorted alphabetically.
affinity
    Shows affinity bitmask for each node. Can use -s pe=ALL and -s th=ALL to see affinity for each process and thread, and use -s filter_input=expression to limit the number of PEs shown.
profile
    Show data by function name only
callers (or ca)
    Show function callers (bottom-up view)
calltree (or ct)
    Show calltree (top-down view)
ca+src
    Show line numbers in callers
ct+src
    Show line numbers in calltree
hbm_ct
    Show memory bandwidth data by object, sorted by sample count.
hbm_details
    Show hbm data collection statistics, including counts of sampled addresses that could not be mapped to a registered object.
hbm_frees
    Show program locations at which objects are freed by explicit calls to free or delete.
hbm_wt
    Show memory bandwidth data by object, sorted by aggregate sample weight. The weight estimates the benefit of allocating the object in high bandwidth memory.
heap
    Implies heap_program. heap_hiwater, and heap_leaks. Instrumented executables must be built using the pat_build -g heap option or executed with the pat_run -g heap option in order to show heap_hiwater and heap_leaks information.
heap_program
    Compare heap usage at the start and end of the program, showing heap space used and free at the start, and unfreed space and fragmentation at the end.
heap_hiwater
    If the pat_build -g heap option was used to instrument the program or the program was executed with the pat_run -g heap option, this report option shows the heap usage "high water" mark, the total number of allocations and frees, and the number and total size of objects allocated but not freed between the start and end of the program.
heap_leaks
    If the pat_build -g heap option was used to instrument the program or the program was executed with the pat_run -g heap option, this report option shows the largest unfreed objects by call site of allocation and PE number.
himem
    Memory high water mark by Numa Node. For nodes with multiple sockets, or nodes with Intel KNL processors, the default report should also have a table showing high water usage by numa node. That table is not shown if all memory was mapped to numa node 0, but can be explicitly requested with pat_report -O himem.
acc_kern_stats
    Show kernel-level statistics including average kernel grid size, average block size, and average amount of shared memory dynamically allocated for the kernel.
load_balance
    Implies load_balance_program, load_balance_group, and load_balance_function. Show PEs with maximum, minimum, and median times.
load_balance_program, load_balance_group, load_balance_function
    For the whole program, groups, or functions, respectively, show the imb_time (difference between maximum and average time across PEs) in seconds and the imb_time% (imb_time/max_time * NumPEs/(NumPEs - 1)). For example, an imbalance of 100% for a function means that only one PE spent time in that function.
load_balance_cm
    If the pat_build -g mpi option was used to instrument the program or the program was executed with the pat_run -g mpi option, this report option shows the load balance by group with collective-message statistics.
load_balance_sm
    If the pat_build -g mpi option was used to instrument the program or the program was executed with the pat_run -g mpi option, this report option shows the load balance by group with sent-message statistics.
load_imbalance_thread
    Shows the active time (average over PEs) for each thread number.
loop_times
    Inclusive and Exclusive Time in Loops. If the CCE Classic compiler -h profile_generate or CCE compiler -finstrument-loops option was used, then this table will be included in a default report and the following additional loop reporting options are also available.
loop_callers
    Loop Stats by Function and Caller. Available only if the CCE Classic compiler -h profile_generate or CCE compiler -finstrument-loops option was used.
loop_callers+src
    Loop Stats by Function and Callsites. Available only if the CCE Classic compiler -h profile_generate or CCE compiler -finstrument-loops option was used.
loop_calltree
    Function and Loop Calltree View. Available only if the CCE Classic compiler -h profile_generate or CCE compiler -finstrument-loops option was used.
loop_calltree+src
    Function and Loop Calltree with Line Numbers. Available only if the CCE Classic compiler -h profile_generate or CCE compiler -finstrument-loops option was used.
profile_loops
    Profile by Group and Function with Loops. Available only if the CCE Classic compiler -h profile_generate or CCE compiler -finstrument-loops option was used.
mcdram
    Display the MCDRAM configuration for each PE with pat_report -O mcdram ...
mesh_xyz
    Show the coordinates in the network mesh.
mpi_callers
    Show MPI sent- and collective-message statistics
mpi_sm_callers
    Show MPI sent-message statistics
mpi_coll_callers
    Show MPI collective-message statistics
mpi_dest_bytes
    Show MPI bin statistics as total bytes
mpi_dest_counts
    Show MPI bin statistics as counts of messages
mpi_sm_rank_order
    Calculate a suggested rank order based on MPI grid detection and MPI point-to-point message optimization. Uses sent-message data from tracing MPI functions to generate suggested MPI rank order information. Requires the program to be instrumented using the pat_build -g mpi option or executed with the pat_run -g mpi option.
mpi_rank_order
    Calculate a rank order to balance a shared resource such as USER time over all nodes. Uses time in user functions, or alternatively, any other metric specified by using the -s mro_metric options, to generate suggested MPI rank order information.
mpi_hy_rank_order
    Calculate a rank order based on a hybrid combination of mpi_sm_rank_order and mpi_rank_order.
nids
    Show PE to NID mapping.
nwpc
    Program network performance counter activity.
profile_nwpc
    Network performance counter data by Function Group and Function. Table shown by default if NWPCs are present in the .ap2 file.
profile_pe.th
    Show the imbalance over the set of all threads in the program.
profile_pe_th
    Show the imbalance over PEs of maximum thread times.
profile_th_pe
    For each thread, show the imbalance over PEs.
program_time
    Shows which PEs took the maximum, median, and minimum time for the whole program.
read_stats, write_stats
    If the pat_build -g io option was used to instrument the program or the program was executed with the pat_run -g io option, these options show the I/O statistics by filename and by PE, with maximum, median, and minimum I/O times. The -O io option is a shortcut for both read_stats and write_stats.
samp_profile+src
    Show sampled data by line number with each function.
thread_times
    For each thread number, show the average of all PE times and the PEs with the minimum, maximum, and median times.
```

<a id="hpctoolkit"></a>

<a id="adastra-software-stack-tools-profiling-hpctoolkit"></a>

### HPCToolkit

`hpctoolkit` is a sampling profiler. It has proven very useful when one want to observe load imbalance.

CINES proposes build of HPCToolkit via modules.

You can find them through `module spider hpctoolkit`.

The GUI can be used via [X11 forwarding](../../user_support/index.md#adastra-x11-forwarding).

Assuming you want to profile a program `my_program` and that you have loaded the `hpctoolkit` module:

```shell-session
$ # hpcrun will produce one ore more *measurement* directories.
$ hpcrun --event CPUTIME --trace --output hpctoolkit-measurements -- ./my_program <arguments>
$ # (optional) Ask HPCtookit to inspect your program to refine the mapping
$ # of machine code (instruction) to profiling data (sample).
$ # You may want to use the --cache option.
$ hpcstruct --jobs=8 --psize 2097152 ./hpctoolkit-measurements
$ # Post-process the recorded trace and a generate a *database* directory.
$ hpcprof ./hpctoolkit-measurements
$ # Analyse using the GUI:
$ hpcviewer ./hpctoolkit-database
```

If you want to profile a specific rank of an MPI based, multi rank program, use a trivial shell wrapper to profile only if the `SLURM_PROCID` is equal to the rank you wish to profile:

```shell
#!/bin/bash

set -eu

if [ "${SLURM_PROCID}" == "0" ]; then
    exec -- hpcrun -- "${@}"
else
    exec -- "${@}"
fi
```

John Mellor-Crummey presents [HPCtoolkit: Performance Analysis of GPU-accelerated Kokkos Applications on NVIDIA GPUs](https://www.youtube.com/watch?v=zf_yXAf7lYM).

<a id="linaro-map"></a>

<a id="adastra-software-stack-tools-profiling-map"></a>

### Linaro MAP

`Linaro MAP` is another profiler provided by the CINES. It gives an overview of your program, via different metrics. CINES proposes builds of `MAP` via modules entitled `ddt`, which can be found through `module spider ddt`. The associated GUI can be used via [X11 forwarding](../../user_support/index.md#adastra-x11-forwarding) or the HPDA nodes.

Assuming you want to profile your `my_program`, the first step is to compile your code with the `-g` compile flag to have access to the debugging symbols. Then, in your `sbatch` file, you should add the following commands:

```shell-session
$ module load ddt
$ map --profile srun <slurm_args> -- my_program
```

It creates a file with suffix `.map`. You can open it on a login node via the following commands:

```shell-session
$ module load ddt
$ map result_file.map
```

Here is a typical example of such an output:

[![../../_images/MAP.PNG](https://dci.dci-gitlab.cines.fr/webextranet/_images/MAP.PNG)](https://dci.dci-gitlab.cines.fr/webextranet/_images/MAP.PNG)

For example, the graphs at the top represents different metrics with respect to the time of the simulation. The `Application activity` gives you the decomposition of the activity of the different CPU cores in categories like OpenMP, MPI, IO… You can also track the memory footprint of your code with the `Memory usage` metric…

Much more details can be found in the official documentation: <https://docs.linaroforge.com/26.0/html/forge/map/index.html>

**Warning**

DDT can add a x1.5 memory overhead when the debugger with the memory usage feature is enabled.

<a id="intel-vtune-advisor"></a>

### Intel VTune & Advisor

CINES proposes both softwares under the following paths:

```
/opt/software/intel/oneapi/advisor/latest/bin64/advisor-gui
/opt/software/intel/oneapi/vtune/latest/bin64/vtune-gui
```

The GUI can be used via [X11 forwarding](../../user_support/index.md#adastra-x11-forwarding).

Assuming you want to profile a program `my_program`:

```shell-session
$ /opt/software/intel/oneapi/vtune/latest/bin64/vtune -collect hotspots -result-dir="<result_dir>" -- ./my_program <arguments>
$ # Visualize the trace in the shell:
$ /opt/software/intel/oneapi/vtune/latest/bin64/vtune -report hotspots -result-dir="<result_dir>"
$ # Or via the GUI:
$ /opt/software/intel/oneapi/vtune/latest/bin64/vtune-gui
```

If you want to profile a specific rank of an MPI based, multi rank program, use a trivial shell wrapper to profile only if the `SLURM_PROCID` is equal to the rank you wish to profile:

```shell
#!/bin/bash

set -eu

if [ "${SLURM_PROCID}" == "0" ]; then
    exec -- /opt/software/intel/oneapi/vtune/latest/bin64/vtune \
        -collect hotspots \
        -result-dir="vtune_${SLURM_PROCID}.data" \
        -- "${@}"
else
    exec -- "${@}"
fi
```

<a id="rocprofiler-compute"></a>

### rocProfiler Compute

**Note**

Previously called Omniperf.

**Warning**

Ensure you use a profiler from a ROCm in **version equal or more recent** than the ROCm used to build the binary.

**Note**

We provide [`slides given in 2024`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/25d0b0f1975cbc2468f19a50eb8695c3/AMD_GPU_Performance_Analysis_Tools.pdf) on using this tool.

**Note**

Can be used go into the nitty-gritty details of the GPU kernels. Its at a lower level than rocProfiler Compute.

A crash course is [`made available here`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/189a11ef04d2fc20df56f50066d27652/rocgdb_tutorial.pdf).

ROCm Compute Profiler is a performance profiling tool for Machine Learning and HPC workloads running on AMD Instinct Accelerators (MI100, MI200, MI300, etc.). It is currently built on top of the rocProfiler (lower level tool) to monitor hardware performance counters. Basically it is a pretty interface to rocPROF.

It offers the following analysis related features:

- System information;
- System Speed-of-Light (SOL);
- Kernel statistic;
- Memory chart analysis;
- Roofline analysis (supported on MI200 only, SLES 15 SP3 or RHEL8);
- Command Processor (CP);
- Shader Processing Input (SPI);
- Wavefront launch;
- Compute Unit (CU) - instruction mix;
- Compute Unit (CU) - pipeline;
- Local Data Share (LDS);
- Instruction cache;
- Scalar L1D cache;
- Texture addresser and data;
- Vector L1D cache;
- L2 cache;
- L2 cache (per-channel).

Metric explanations are given here in <https://rocm.docs.amd.com/projects/rocprofiler-compute/en/latest/conceptual/pipeline-metrics.html> and <https://rocm.docs.amd.com/projects/rocprofiler-compute/en/latest/conceptual/local-data-share.html>.

On Adastra, we recommend that you build the latest version of rocProfiler Compute using the latest ROCm version available on Adastra.

To use the tool, please refer to their official documents <https://rocm.docs.amd.com/projects/rocprofiler-compute/en/latest/index.html>. A good video introduction to the tool is given by Cole Ramos in [GPU Profiling (Performance Profile: rocProfiler Compute/Omniperf)](https://vimeo.com/881862090).

Step by step examples are given in [this document](https://rocm.docs.amd.com/projects/rocprofiler-compute/en/latest/tutorial/profiling-by-example.html).

<a id="building-rocprofiler-compute"></a>

#### Building rocProfiler Compute

To ensure you always have the latest rocProfiler Compute version you should compile your own. Since ROCm 7, rocProfiler Compute is built in, this guide was made for ROCm >=7. Still, some python packages are needed to use it.

**Note**

You may benefit from using a Python virtual environment, check [this document](index.md#adastra-software-stack-tools-python-virtual-environment) on how to setup one.

Then, prepare an environment file (`environment.sh`):

```shell
#!/bin/bash

module purge

module load rocm/7.2.0
# rocProfiler Compute expects old Python versions 3.10.
module load cray-python/3.10

module list
```

Install the Python packages:

```shell
#!/bin/bash

set -eu

source environment.sh

pip3 install -r "${ROCM_PATH}/libexec/rocprofiler-compute/requirements.txt"
```

The dependencies are now installed.

<a id="environment-variables"></a>

#### Environment variables

```shell-session
$ export ROCPROFCOMPUTE_LOGLEVEL="DEBUG" # TRACE,INFO
$ export ROCPROFCOMPUTE_COLOR="0"
$ # export ROCPROF="rocprofv3" # By default starting with ROCm 6.4.0.
```

<a id="advanced-gpu-profiling"></a>

#### Advanced GPU Profiling

**Note**

Be careful, rocProfiler compute will run your binary multiple times. Ensure that there is reproducibility between runs.

```shell-session
$ rocprof-compute profile -n <case_name> --device 0 -- ./my_program <arguments>
...
```

When the profiling finished collecting, you can analyze the result. Because your application may generate many kernel launch, rocProfiler compute needs to know for which kernel launch to report the performance counters.

To get the list of kernel launch, you should take a look at the `workloads/<case_name>/<device>/pmc_perf.csv` file with `<device>` either set to `MI200` or `MI300`. This file lists all kernel launch and associated metrics. From this kernel list, select the identifier (the number in the first column) and pass it to rocProfiler compute via the `--dispatch <N>` option, with `<N>` the number you got from the CSV file.

```shell-session
$ rocprof-compute analyze --block 17.2.1 17.2.2 17.5.3 17.5.4 --dispatch 27 --path workloads/<case_name>/<device>/

  ___                  _                  __
 / _ \ _ __ ___  _ __ (_)_ __   ___ _ __ / _|
| | | | '_ ` _ \| '_ \| | '_ \ / _ \ '__| |_
| |_| | | | | | | | | | | |_) |  __/ |  |  _|
 \___/|_| |_| |_|_| |_|_| .__/ \___|_|  |_|
                        |_|

INFO Analysis mode = cli
INFO [analysis] deriving Omniperf metrics...

--------------------------------------------------------------------------------
1. Top Stats
0.1 Top Kernels
╒════╤══════════════════════════════════════════╤═════════╤════════════╤════════════╤══════════════╤════════╕
│    │ Kernel_Name                              │   Count │    Sum(ns) │   Mean(ns) │   Median(ns) │    Pct │
╞════╪══════════════════════════════════════════╪═════════╪════════════╪════════════╪══════════════╪════════╡
│  0 │ void splb2::portability::ncal::hip::deta │    1.00 │ 2311218.00 │ 2311218.00 │   2311218.00 │ 100.00 │
│    │ il::DoRun<splb2::portability::ncal::hip: │         │            │            │              │        │
│    │ :DeviceQueue::DefaultPropsType, splb2... │         │            │            │              │        │
╘════╧══════════════════════════════════════════╧═════════╧════════════╧════════════╧══════════════╧════════╛
0.2 Dispatch List
╒════╤═══════════════╤══════════════════════════════════════════════════════════════════════════════════╕
│    │   Dispatch_ID │ Kernel_Name                                                                      │
╞════╪═══════════════╪══════════════════════════════════════════════════════════════════════════════════╡
│  0 │            27 │ void splb2::portability::ncal::hip::detail::DoRun<splb2::portability::ncal::hip: │
│    │               │ :DeviceQueue::DefaultPropsType, splb2::portability::ncal::hip::detail::DoApply<s │
│    │               │ plb2::portability::ncal::hip::DeviceQueue::DefaultPropsType, DoStream<splb2::por │
│    │               │ tability::ncal::hip::DeviceQueue>()::{lambda(long)#3}>(ihipStream_t*, splb2::... │
╘════╧═══════════════╧══════════════════════════════════════════════════════════════════════════════════╛

--------------------------------------------------------------------------------
1.  L2 Cache
17.2 L2 - Fabric Transactions
╒═════════════╤═════════════════════╤════════╤════════╤════════╤════════╕
│ Metric_ID   │ Metric              │    Avg │    Min │    Max │ Unit   │
╞═════════════╪═════════════════════╪════════╪════════╪════════╪════════╡
│ 17.2.1      │ HBM Read Traffic    │ 100.00 │ 100.00 │ 100.00 │ Pct    │
├─────────────┼─────────────────────┼────────┼────────┼────────┼────────┤
│ 17.2.2      │ Remote Read Traffic │   0.00 │   0.00 │   0.00 │ Pct    │
╘═════════════╧═════════════════════╧════════╧════════╧════════╧════════╛
17.5 L2 - Fabric Detailed Transaction Breakdown
╒═════════════╤═════════════╤═══════╤═══════╤═══════╤══════════════╕
│ Metric_ID   │ Metric      │   Avg │   Min │   Max │ Unit         │
╞═════════════╪═════════════╪═══════╪═══════╪═══════╪══════════════╡
│ 17.5.3      │ HBM Read    │ 63.76 │ 63.76 │ 63.76 │ Req per wave │
├─────────────┼─────────────┼───────┼───────┼───────┼──────────────┤
│ 17.5.4      │ Remote Read │  0.00 │  0.00 │  0.00 │ Req per wave │
╘═════════════╧═════════════╧═══════╧═══════╧═══════╧══════════════╛
```

Here, the profiling report focuses the 27th kernel launch on device 0 and on what rocProfiler compute calls *block* `17.2.1 17.2.2 17.5.3 17.5.4`. These blocks correspond to sets of related metrics. In this example, we see we are hitting perfect HBM throughput (100% of the peak).

The list of the available metric blocs is dependent on the GPU architecture and the profile that was done earlier. It can be obtained like so:

```shell-session
$ rocprof-compute analyze --list-metrics gfx90a --path workloads/<case_name>/<device>/ | less
```

Remember, MI250X’s code name is `gfx90a` and the MI300A is `gfx942`.

Commonly used metrics with the implication (`->`):

```
7.1.9 - Scratch Allocation -> spilling and GMEM accesses.
2.1.14 - IPC (high is better) -> stall
2.1.13 - VALU Active Threads (higher is better) -> divergence
2.1.15 - Wavefront Occupancy (higher is better > 90%: CU/device * VALU/cu * Warp/VALU | 110 * 4 * 8) -> tail latency, warp count not multiple of device queue slot
2.1.17 - LDS Bank Conflicts/Access (ratio) (lower is better) -> same address used by multiple lane
2.1.18 - vL1D Cache Hit Rate / 16.1.0 - Hit rate (higher is better > 70%)
    16.1.3 - Coalescing (higher is better) -> if low, random access, memory transaction wastage
    16.4.5 - NC - Write 16.4.6 - UC - Write 16.4.7 - CC - Write -> if low, no cache bypass. NC writes can help avoiding trashing
2.1.28 - L1I Hit Rate (higher is better > 95%) -> if low, kernel too large (#fortran array syntax)
2.1.20 - L2 Cache Hit Rate (higher is better > 70%)
```

If you want to profile a specific rank of an MPI based, multi rank program, use a trivial shell wrapper to profile only if the `SLURM_PROCID` is equal to the rank you wish to profile:

```shell
#!/bin/bash

set -eu

if [ "${SLURM_PROCID}" == "0" ]; then
    exec -- rocprof-compute profile -n "rocprof-compute_${SLURM_PROCID}" \
        -- "${@}"
else
    exec -- "${@}"
fi
```

<a id="gpu-roofline"></a>

#### GPU roofline

**Note**

Be careful, rocProfiler compute will run your binary multiple times. Ensure that there is reproducibility between runs.

rocProfiler compute uses rocPROF to build rooflines graphs for you. It can be used like so:

```shell-session
$ rocprof-compute profile -n <case_name> --roof-only --device 0 --kernel-names -- ./my_program <arguments>
```

rocProfiler compute will start the `my_program` as many time as needed for all the counter to be retrieved and run exclusively on the device `0`. When the process finishes, you will find PDF files in `workloads/<case_name>/<device>/`. These documents are roofline graph.

[![../../_images/omniperf_roofline_0.png](https://dci.dci-gitlab.cines.fr/webextranet/_images/omniperf_roofline_0.png)](https://dci.dci-gitlab.cines.fr/webextranet/_images/omniperf_roofline_0.png)

**Note**

The `--dispatch <N>` option is of the upmost importance if you program launches one than one kernel because rocProfiler compute will always produce a roofline of the first kernel it sees (after the filters are applied), not the other.

**Warning**

Careful when mixing `ROCR_VISIBLE_DEVICES` or similar with the `--device=<N>` option.

<a id="rocprofiler-systems"></a>

### rocProfiler Systems

**Note**

Previously called Omnitrace.

**Warning**

Ensure you use a profiler from a ROCm in **version equal or more recent** than the ROCm used to build the binary.

**Note**

We provide [`slides given in 2024`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/25d0b0f1975cbc2468f19a50eb8695c3/AMD_GPU_Performance_Analysis_Tools.pdf) on using this tool.

**Note**

Closer to a typical profiler (say VTune, `perf`) with additional AMD GPU kernel details.

rocProfiler System is designed for both high-level profiling and comprehensive tracing of applications running on the CPU or the CPU+GPU via dynamic binary instrumentation, call-stack sampling, and various other means for determining currently executing function and line information.

The profiler results can be viewed in any modern web browser. Visiting <https://ui.perfetto.dev> and loading the output .json/.proto files produced by the profiler (nothing is sent to this website, you just use the interface).

It offers the following analysis related features:

- Dynamic instrumentation;
  - Runtime instrumentation;
  - Binary rewriting;
- Statistical sampling;
- Process-level sampling;
- Causal profiling;
- High-level summary profiles with mean/min/max/stddev statistics;
- Application speedup predictions resulting from potential optimizations in functions and lines of code (causal profiling);
- Critical trace generation;
- Critical trace analysis;
- HIP;
- HSA;
- Pthreads;
- MPI;
- Kokkos-Tools (KokkosP);
- OpenMP-Tools (OMPT);
- GPU hardware counters;
- HIP API tracing;
- HIP kernel tracing;
- HSA API tracing;
- HSA operation tracing;
- System-level sampling (via rocm-smi);
- CPU hardware counters sampling and profiles;
- CPU frequency sampling;
- Various timing metrics;
- Various memory metrics;
- Network statistics;
- I/O metrics;
- Third-party API support:
  :   - TAU;
      - LIKWID;
      - Caliper;
      - CrayPAT;
      - VTune;
      - NVTX;
      - ROCTX.

On Adastra, we provide a module (currently hidden) which you can load like so:

```shell-session
$ module load rocm/5.5.1
$ module load .omnitrace/1.10.4
```

To use the tool, please refer to their official documents <https://rocm.docs.amd.com/projects/rocprofiler-systems/en/latest/index.html>.

<a id="perf"></a>

<a id="adastra-software-stack-tools-profiling-perf"></a>

### `perf`

**Warning**

You may have to use the full path: `/usr/bin/perf` if the `cray-hdf5-parallel` module is used.

**Note**

`perf` prepends `/usr/libexec/perf-core:/usr/bin` to the `PATH` environment variable.

`perf` is the performance analysis tool for Linux. It is developed as part of the [Linux kernel](https://perf.wiki.kernel.org/index.php/Main_Page). This tools is *simple* to use, lightweight and versatile. You can record traces of many kind and exploit them using specific tools such as the [hotspot visualizer](https://github.com/KDAB/hotspot).

Assuming you want to profile a program `my_program`:

```shell-session
$ perf record -o perf.data --sample-cpu --freq=1000 --call-graph dwarf,512 --event instructions,cpu-cycles,cache-misses,branches --aio=1 --compression-level=1 -- ./my_program <arguments>
$ perf report
$ perf annotate
```

The profiler results can be viewed in any modern web browser. Visiting <https://profiler.firefox.com> and loading the output of `perf script -i perf.data -F +pid>my_firefox_profile_data.txt` (nothing is sent to this website, you just use the interface).

**Warning**

Using <https://profiler.firefox.com> requires that you enable call graph support (use at least `perf record --call-graph -- ./my_program <arguments>`).

Other interesting event to monitor (as argument to the `-e` flag):

```
dTLB-loads
dTLB-load-misses
```

Many more event exist, check them out using `perf list`.

If you want to profile a specific rank of an MPI based, multi rank program, use a trivial shell wrapper to profile only if the `SLURM_PROCID` is equal to the rank you wish to profile:

```shell
#!/bin/bash

set -eu

if [ "${SLURM_PROCID}" == "0" ]; then
    exec -- /usr/bin/perf record -o "perf_${SLURM_PROCID}.data" -- "${@}"
else
    exec -- "${@}"
fi
```

**Note**

Piping the output of `perf` makes it write the trace file to stdout. In this case be sure to specify the `-o perf.data` option: `perf record -o perf.data -- ./a.out | tee logs`.

<a id="snooping-on-a-process"></a>

#### Snooping on a process

You can launch a workload, connect to one of the nodes currently being used by the code using `ssh` and executing:

```shell-session
$ perf top -p <pid>
```

This will provide you with a live tracing capability.

<a id="intel-topdown-microarchitecture-analysis-tma"></a>

#### Intel TopDown Microarchitecture Analysis (TMA)

TMA is a method popularized by Intel that gives guidelines on how to tune an application for CPU.

Details can be read here: <https://web.archive.org/web/20250128231911/https://www.intel.com/content/www/us/en/docs/vtune-profiler/cookbook/2023-0/top-down-microarchitecture-analysis-method.html> and <https://web.archive.org/web/20240424232407/https://www.intel.com/content/www/us/en/developer/articles/technical/demystifying-software-performance-optimization.html>.

Basically, it revolves around knowing which part fo the CPU is limiting the performance and tuning to solve the bottleneck.

[![../../_images/tma_intel0.jpg](https://dci.dci-gitlab.cines.fr/webextranet/_images/tma_intel0.jpg)](https://dci.dci-gitlab.cines.fr/webextranet/_images/tma_intel0.jpg)

Recent releases of `perf` provides metrics that can help figure out in which part of the diagram a program is and thus where to tune from there.

For instance on recent `perf`:

```shell-session
$ (sudo) perf stat -M tma_frontend_bound,tma_backend_bound,tma_bad_speculation,tma_retiring -- ./my_program <arguments>
```

On older `perf`:

```shell-session
$ (sudo) perf stat -M frontend_bound,backend_bound,bad_speculation,retiring -- ./my_program <arguments>
```

Other metrics exist, such as `tma_memory_bound,tma_core_bound,tma_l3_bound`.

<a id="rocprof"></a>

<a id="adastra-software-stack-tools-profiling-rocprof"></a>

### rocPROF

**Note**

We recommend that you use rocPROFv3 if possible, see below.

**Warning**

Ensure you use a profiler from a ROCm in **version equal or more recent** than the ROCm used to build the binary.

**Note**

We provide [`slides given in 2024`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/25d0b0f1975cbc2468f19a50eb8695c3/AMD_GPU_Performance_Analysis_Tools.pdf) on using this tool.

`rocprof` is the performance analysis tool for GPGPU oriented AMD GPUs.

**Note**

When doing an initial profiling, you *may* benefit from using `export AMD_SERIALIZE_COPY=3 AMD_SERIALIZE_KERNEL=3 GPU_MAX_HW_QUEUES=1`. This will force kernels to be serialized on one physical stream which *may* ease resource usage analysis of the kernels and generally gives a cleaner trace.

If you want to profile a specific rank of an MPI based, multi rank program, use a trivial shell wrapper to profile only if the `SLURM_PROCID` is equal to the rank you wish to profile:

```shell
#!/bin/bash

set -eu

if [ "${SLURM_PROCID}" == "0" ]; then
    exec -- rocprof --stats --timestamp on -o stats_${SLURM_JOB_ID}-${SLURM_PROCID}.csv "${@}"
else
    exec -- "${@}"
fi
```

This scripts serves to select which rank is to be profiled. But also, to properly label the trace data to disk using `SLURM_PROCID`.

**Warning**

In the script above, only the first rank (0) is going to be profiled. Change the `"${SLURM_PROCID}" == "XXX"` if needed.

<a id="simple-gpu-tracing"></a>

#### Simple GPU tracing

```shell-session
$ rocprof --hip-trace ./my_program <arguments>
```

<a id="simple-gpu-profiling"></a>

#### Simple GPU profiling

This tools can be used to gather GPU kernel statistics.

For rocPROF to be available in your environment, the correct `amd-mixed` or `rocm` module (if you did not use `PrgEnv-amd`). We recommend the rocPROF built in ROCm versions equal **or more recent** than 5.3.0. **Earlier rocPROF versions had crippling bugs**.

The first step is to *map the landscape*. This can be done by asking rocPROF to produce simple statistics about all the kernel like so:

```shell-session
$ rocprof --stats --timestamp on -o stats_${SLURM_JOB_ID}-${SLURM_PROCID}.csv ./my_program <arguments>
```

This will produce a CSV output composed of the following significant files: `stats_<slurm_job_id>-<slurm_mpi_rank>.csv` and `stats_<slurm_job_id>-<slurm_mpi_rank>.stats.csv`. This first files represents the list of all information gather for each kernel launched.

Sample of the first file (`.csv`) after formatting the CSV as a table:

| Index | KernelName | gpu-id | queue-id | queue-index | pid | tid | grd | wgr | lds | scr | vgpr | sgpr | fbar | sig | obj | DispatchNs | BeginNs | EndNs | CompleteNs | DurationNs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | void thrust::hip_rocprim::__parallel_for::kernel<256u, 1u, thrust::hip_rocprim:: … [clone .kd] | 0 | 1 | 0 | 796946 | 796946 | 11796480 | 256 | 0 | 0 | 8 | 24 | 94656 | 0x0 | 0x7f1e35826300 | 1191607302876252 | 1191607302920469 | 1191607303043669 | 1191607303053971 | 123200 |
| 1 | void rocprim::detail::scan_batches_kernel<256u, 2u, 6u>(unsigned int*, unsigned int*, unsigned int) [clone .kd] | 0 | 1 | 48 | 796946 | 796946 | 16384 | 256 | 512 | 0 | 16 | 24 | 36864 | 0x0 | 0x7f1e35825bc0 | 1191607404624006 | 1191607404963922 | 1191607404970162 | 1191607404973843 | 6240 |
| 2 | __omp_offloading_30_40e0070__ZN5Field6put_toEd_l21_cce$noloop$form.kd | 0 | 0 | 4 | 796946 | 796946 | 68352 | 256 | 0 | 0 | 4 | 24 | 68224 | 0x0 | 0x7f1e2fdc8240 | 1191607515378464 | 1191607515391455 | 1191607515400735 | 1191607515402559 | 9280 |

Sample of the second file (`.stats.csv`) after formatting the CSV as a table:

| Name | Calls | TotalDurationNs | AverageNs | Percentage |
| --- | --- | --- | --- | --- |
| void hip::kernel::DepositCurrentDensity_2D_Order2<double, float, 128ul>(double*, … [clone .kd] | 600 | 8559183476 | 14265305 | 50.06434641750023 |
| void rocprim::detail::partition_kernel<(rocprim::detail::select_method)1, true, … [clone .kd] | 600 | 1260501300 | 2100835 | 7.372919849172466 |
| void rocprim::detail::partition_kernel<(rocprim::detail::select_method)1, true, … [clone .kd] | 600 | 1247304037 | 2078840 | 7.29572646402685 |
| __omp_offloading_30_40e035b__ZN20Interpolator2D2Order13fieldsWrapperEP11ElectroMagnR9ParticlesP9MPIPiS6_iji_l186_cce$noloop$form.kd | 600 | 1245721159 | 2076201 | 7.2864678994977865 |
| __omp_offloading_30_40e0060__ZN11PusherBorisclER9ParticlesP9MPIiiii_l57_cce$noloop$form.kd | 600 | 1040969461 | 1734949 | 6.088834974933595 |

From theses two sample tables we can note some interesting information such as:

**Calls** - How many time a given kernel has been launched.

**DurationNs** - Execution duration for a given kernel launch.

**AverageNs** - Average kernel duration in nanosecond (`=sum(DurationNs of a given kernel) / Calls of a given kernel`).

**Percentage** - Percentage of the GPU time (not user, cpu or system time) spent on a given kernel (`=sum(DurationNs of a given kernel) / sum(DurationNs of all kernels`).

**grd** - Size of the grid (in thread/work-item) (`=wgr*grp_count`).

**wgr** - Size of the workgroup (in thread/work-item) (`=grd/grp_count`).

**lds** - Amount of LDS used in octet.

**scr** - Amount of scratch memory space usage in octet.

**vgpr** - Amount of vector general purpose register (a GPR is 4 octets wide).

**sgpr** - Amount of scalar general purpose register (a GPR is 4 octets wide).

**Note**

The rocPROF overhead is not very high (~ 5-10%) when only asking for basic statistics (`--stats`) but the amount of data can grow very fast!

**Note**

rocPROF gather data on every kernel launched on a given GPU, that is, your kernels or other’s kernels. Make sure only your code is executing on it, else you will get noisy reports.

<a id="precise-gpu-profiling"></a>

<a id="adastra-software-stack-tools-profiling-rocprof-precise"></a>

#### Precise GPU profiling

This topic can become very advanced quite quickly, here we only present a way to gather information, not how to interpret the results which. rocPROF can be fed with a `-i <file_name>.txt` option. This `<file_name>.txt` point to a configuration file inside which we can specify a list of hardware counters or metrics (based on hardware counters) sampled at runtime. One **can not ask** to log all the hardware counters due to hardware limitations.

Here is such a configuration file with often relevant metrics:

```
pmc: VALUUtilization VALUBusy L2CacheHit LDSBankConflict ALUStalledByLDS
```

It shall be used like so:

```shell-session
$ rocprof -i <filename>.txt ./my_program <arguments>
```

Where the metrics signify:

**VALUUtilization** - The percentage of active vector ALU threads in a wave. A lower number can mean either more thread divergence in a wave or that the work-group size is not a multiple of 64. Value range: 0% (bad), 100% (ideal - no thread divergence).

**VALUBusy** - The percentage of GPUTime vector ALU instructions are processed. Value range: 0% (bad) to 100% (optimal).

**L2CacheHit** - The percentage of fetch, write, atomic, and other instructions that hit the data in L2 cache. Value range: 0% (no hit) to 100% (optimal).

**LDSBankConflict** - The percentage of GPUTime LDS is stalled by bank conflicts. Value range: 0% (optimal) to 100% (bad).

**ALUStalledByLDS** - The percentage of GPUTime ALU units are stalled by the LDS input queue being full or the output queue being not ready. If there are LDS bank conflicts, reduce them. Otherwise, try reducing the number of LDS accesses if possible. Value range: 0% (optimal) to 100% (bad).

The tool will produce a `.csv` file which can be manipulated in a spreadsheet. A *heavier* tool called rocProfiler-compute can by used to gather the same metrics, but provide you with reference value that you can compare to.

More information can be found on [the rocPROF Github page](https://github.com/ROCm/rocprofiler/blob/amd-master/doc/rocprof.md) and by reading [the documentation on the available metrics](https://github.com/ROCm-Developer-Tools/rocprofiler/blob/amd-master/test/tool/metrics.xml) (also see `$ rocprof --list-basic` and `$ rocprof --list-derived`.

**Note**

A detailed list of available hardware counters and their respective meaning is available here: <https://rocm.docs.amd.com/en/latest/conceptual/gpu-arch/mi200-performance-counters.html>

**Note**

One can choose to restrain the set of kernel on which data should be collected by adding the line: `kernel: <kernel_symbol_00>`. Where `kernel_symbol_00` is the kernel name (you can get it from a rocPROF `.stats.csv` file if unknown due to, say OpenMP). You can restrain the set to more than one kernel.

<a id="id1"></a>

#### GPU roofline

The [roofline model](https://en.wikipedia.org/wiki/Roofline_model) enables the developer to quickly assert how far from the theoretical peak performance a specific piece of code is.

Effectively, it plots the floating point throughput (Flop/s) as a function of the arithmetic intensity of kernels. The arithmetic intensity represents the amount of Flop per unit of data loaded from (Flop/octet), typically, cache or main memory.

Then, one derives a theoretical peak performance based on the capacities of the hardware. The shape of this upper bound performance has the shape of a roofline, thus the name.

In practice we have multiple rooflines, one for Binary64 (double), one for Binary32 (float) etc..

In case of the MI250X cards and as an example, we can derive, for a GCD, a Binary64 roofline based on the peak theoretical memory throughput \(\textrm{B} = 1.6\) Tio/s and a peak Flop/s \(\textrm{F} = 23.9\) TFlop/s. The memory throughput, like the peak Flop/s can also be experimentally derived using benchmarks.

\[\begin{split}{\displaystyle \textrm{P} = \min {\begin{cases} \textrm{F} \\ \textrm{B} \times \textrm{I} \end{cases}}}\end{split}\]

Plotting \(\textrm{P}\) as a function of \(\textrm{I}\) gives:

[![../../_images/rocprof_roofline_0.png](https://dci.dci-gitlab.cines.fr/webextranet/_images/rocprof_roofline_0.png)](https://dci.dci-gitlab.cines.fr/webextranet/_images/rocprof_roofline_0.png)

Then using [rocPROF and specific hardware counters](index.md#adastra-software-stack-tools-profiling-rocprof-precise), we can obtain, for each kernel, the arithmetic intensity and its associated floating point throughput.

Under the assumption that one does not mix floating point precision inside a given kernel, we provide the following rocPROF configuration files for Binary64 (double):

```
pmc: TCC_EA_RDREQ_32B_sum TCC_EA_RDREQ_sum TCC_EA_WRREQ_sum TCC_EA_WRREQ_64B_sum SQ_INSTS_VALU_ADD_F64 SQ_INSTS_VALU_MUL_F64 SQ_INSTS_VALU_FMA_F64 SQ_INSTS_VALU_TRANS_F64 SQ_INSTS_VALU_MFMA_MOPS_F64
```

For Binary32 (float) we would have:

```
pmc: TCC_EA_RDREQ_32B_sum TCC_EA_RDREQ_sum TCC_EA_WRREQ_sum TCC_EA_WRREQ_64B_sum SQ_INSTS_VALU_ADD_F32 SQ_INSTS_VALU_MUL_F32 SQ_INSTS_VALU_FMA_F32 SQ_INSTS_VALU_TRANS_F32 SQ_INSTS_VALU_MFMA_MOPS_F32
```

And for Binary16 (half) and [Brain16](https://en.wikipedia.org/wiki/Bfloat16_floating-point_format) we would have:

```
pmc: TCC_EA_RDREQ_32B_sum TCC_EA_RDREQ_sum TCC_EA_WRREQ_sum TCC_EA_WRREQ_64B_sum SQ_INSTS_VALU_ADD_F16 SQ_INSTS_VALU_MUL_F16 SQ_INSTS_VALU_FMA_F16 SQ_INSTS_VALU_TRANS_F16 SQ_INSTS_VALU_MFMA_MOPS_F16 SQ_INSTS_VALU_MFMA_MOPS_BF16
```

The data gathered using rocPROF and the counters above needs to be further processed to obtain the kernel’s arithmetic intensity \(\textrm{I}\) and the Flop/s \(\textrm{F}\).

\[\textrm{Load} = 32 \times \textrm{TCC_EA_RDREQ_32B_sum} + 64 \times (\textrm{TCC_EA_RDREQ_sum} - \textrm{TCC_EA_RDREQ_32B_sum})\]

\[\textrm{Store} = 64 \times \textrm{TCC_EA_WRREQ_64B_sum} + 32 \times (\textrm{TCC_EA_WRREQ_sum} - \textrm{TCC_EA_WRREQ_64B_sum})\]

\[\textrm{MFMA} = 256 \times \textrm{SQ_INSTS_VALU_MFMA_MOPS_F64}\]

\[\textrm{Scalar} = 64 \times (\textrm{SQ_INSTS_VALU_ADD_F64} + \textrm{SQ_INSTS_VALU_MUL_F64} + 2 \times \textrm{SQ_INSTS_VALU_FMA_F64} + \textrm{SQ_INSTS_VALU_TRANS_F64})\]

\[\textrm{Flop} = \textrm{MFMA} + \textrm{Scalar}\]

\[\textrm{I} = (\textrm{Load} + \textrm{Store}) / \textrm{Flop}\]

\[\textrm{F} = \textrm{Flop} / (\textrm{EndNs} - \textrm{BeginNs})\]

If one seeks to analyze the Binary32 data, only the \(\textrm{Flop}\) computation needs to change (use the correct counters by replacing `64` by `32`). Note that for the MFMA operations, in 32 and 64 bits floats, represents 256 floating point operations, and for 16 bit floats it represents 1024 operations. Also, for 16 bits floats, there is `SQ_INSTS_VALU_MFMA_MOPS_BF16` to take into account in addition to `SQ_INSTS_VALU_MFMA_MOPS_F16`.

You can then plot the points for each kernel, giving:

[![../../_images/rocprof_roofline_1.png](https://dci.dci-gitlab.cines.fr/webextranet/_images/rocprof_roofline_1.png)](https://dci.dci-gitlab.cines.fr/webextranet/_images/rocprof_roofline_1.png)

**Note**

You could also use the LDS, L1 or L2 cache throughput to build the roofline but you need to replace the HBM usage counter with the appropriate LDS, LI or L2 counters. Do not compare a measured HBM throughput and AI to a roofline other than the HBM one.

<a id="rocprofv3"></a>

### rocPROFv3

rocPROFv3 is the latest version of the ROCm GPU profiler. It allows you to collect precise traces about the HIP API and kernel launches but also the hardware counter values after a kernel’s execution.

The official documentation can be found here:
<https://rocm.docs.amd.com/projects/rocprofiler-sdk/en/latest/how-to/using-rocprofv3.html>

A crash course is [`made available here`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/189a11ef04d2fc20df56f50066d27652/rocgdb_tutorial.pdf).

**Warning**

rocPROFv3 is available starting ROCm 6.2 !

<a id="tracing"></a>

#### Tracing

**Note**

When tracing only (no performance counter), the overhead is very small (<1 % of runtime).

rocPROFv3 allows you to export traces under multiple format. We recommend that you always use the `pftrace` variant.

The profiler results can be viewed in any modern web browser. Visiting <https://ui.perfetto.dev> and loading the output files produced by the profiler (nothing is sent to this website, you just use the interface).

To profile the HIP API calls (`hipMemcpy`, `hipStreamSynchronize`, etc.):

```shell-session
$ rocprofv3 --output-format=pftrace --hip-runtime-trace -- ./my_program <arguments>
```

To profile the HIP kernels:

```shell-session
$ rocprofv3 --output-format=pftrace --kernel-trace -- ./my_program <arguments>
```

You can mix trace modes, for instance:

```shell-session
$ rocprofv3 --output-format=pftrace --hip-runtime-trace --kernel-trace -- ./my_program <arguments>
```

[![../../_images/rocprofv3_multi_trace.png](https://dci.dci-gitlab.cines.fr/webextranet/_images/rocprofv3_multi_trace.png)](https://dci.dci-gitlab.cines.fr/webextranet/_images/rocprofv3_multi_trace.png)

To trace pretty much everything, you can use:

```shell-session
$ rocprofv3 --output-format=pftrace --sys-trace -- ./my_program <arguments>
```

**Warning**

Careful with system trace, they are at least 10 times larger than the kernel or HIP trace and can go way above 20 times the size.

You can ask the tool to consolidate the trace data by adding the `--stats` flag. It’ll produce a CSV file that contains averaged and total duration of say, a kernel. Note that this only works decently if you use `--output-format=csv` (which is the default by the way).

```shell-session
$ rocprofv3 --sys-trace --stats -- ./my_program <arguments>
...
[...] Opened result file: /.../1951546_agent_info.csv
[...] Opened result file: /.../1951546_kernel_trace.csv
[...] Opened result file: /.../1951546_kernel_stats.csv
[...] Opened result file: /.../1951546_hsa_api_trace.csv
[...] Opened result file: /.../1951546_hsa_stats.csv
[...] Opened result file: /.../1951546_hip_api_trace.csv
[...] Opened result file: /.../1951546_hip_stats.csv
[...] Opened result file: /.../1951546_memory_copy_trace.csv
[...] Opened result file: /.../1951546_memory_copy_stats.csv
[...] Opened result file: /.../1951546_domain_stats.csv
$ cat 1951546_memory_copy_stats.csv
"Name","Calls","TotalDurationNs","AverageNs","Percentage","MinNs","MaxNs","StdDev"
"HOST_TO_DEVICE",215,1963211,9131.213953,97.45,2560,662404,54989.360012
"DEVICE_TO_HOST",14,51360,3668.571429,2.55,2720,6560,1244.846961
```

A good mix of feature with less than a % of reduced time to solution:

```shell-session
$ rocprofv3 --output-format=pftrace --memory-allocation-trace --hip-trace --kernel-trace --kokkos-trace -- ./my_program <arguments>
```

[![../../_images/rocprofv3_good_set_of_feature.png](https://dci.dci-gitlab.cines.fr/webextranet/_images/rocprofv3_good_set_of_feature.png)](https://dci.dci-gitlab.cines.fr/webextranet/_images/rocprofv3_good_set_of_feature.png)

<a id="id2"></a>

#### Profiling

With rocProf v3 and ROCm 6.4.0, we now have the possibility of profiling kernels more similarly to what one would expect from a CPU perspective. That is, sampling of the instruction pointer, collecting “stack traces” (which does not really exist on GPU) and mapping instruction to sources lines.

This feature is called Program Counter (PC) sampling on AMD GPUs. As of this writing, it is not available on MI300A. See <https://github.com/ROCm/rocprofiler-sdk/blob/amd-staging/source/docs/how-to/using-pc-sampling.rst>.

**Warning**

You need to enable debug info generation using the traditional `-g` compiler flag. No change is made to the code, this has no performanc impact. The binary will be larger, though.

```shell-session
$ rocprofv3 --output-format=csv --pc-sampling-beta-enabled --pc-sampling-method host_trap --pc-sampling-unit time --pc-sampling-interval 1 -- ./my_program <arguments>
```

**Note**

The sampling interval is in microseconds. The trace quickly gets big. Try to process a limited set of kernel.

**Note**

With the `host_trap` method, you should expect a x0.8 speedup.

To post process the resulting CSV file, we offer this naive python script, it will correlate samples to lines and report a percentage of time spent in a region of the code:

```python
#!/usr/bin/env python3
import sys
import csv
from collections import defaultdict
def BuildTraceHistogram(trace_lines):
    source_line_to_hit_count = defaultdict(int)
    trace_line_count = 0
    for itrace, a_trace_line in enumerate(trace_lines):
        if itrace == 0:
            # Skip the header
            continue
        trace_line_count += 1
        source_line_to_hit_count[a_trace_line[4]] += 1
        if trace_line_count % 400000 == 0 and trace_line_count != 0:
            print(f"Processed {trace_line_count} lines.", flush=True)
    return trace_line_count, source_line_to_hit_count
def ExcludeSourceLine(source_line):
    if not source_line:
        return True
    if "Unrecognized code object id" in source_line:
        return True
    # TODO(): More exclusion.
    return False
def Present(source_line_histogram):
    trace_line_count, source_line_to_hit_count = source_line_histogram
    excluded_hit_count = 0
    hit_percentage_sum = 0.0
    def OrderingKey(source_line):
        source_line_splitted = source_line.split(":")
        if len(source_line_splitted) != 2:
            print(f"Weird source file {source_line_splitted}")
            return ("", 0)
        return (source_line_splitted[0], int(source_line_splitted[1]))
    source_file_to_hit_count = defaultdict(float)
    print("Per source line:")
    for source_line in sorted(source_line_to_hit_count, key=OrderingKey):
        source_line_hit_count = source_line_to_hit_count[source_line]
        if ExcludeSourceLine(source_line):
            excluded_hit_count += source_line_hit_count
            continue
        hit_percentage = (source_line_hit_count / trace_line_count) * 100.0
        hit_percentage_sum += hit_percentage
        source_file_to_hit_count[source_line.split(":")[0]] += hit_percentage
        print(f"'{source_line}' -> {hit_percentage:.2F}")
    print(f"excluded_hit_count: {excluded_hit_count}")
    print(f"hit_percentage_sum: {hit_percentage_sum:.2F}%")
    print("Per source file:")
    for source_file, hit_percentage in sorted(
        source_file_to_hit_count.items(), key=lambda item: item[1], reverse=True
    ):
        print(f"'{source_file}' -> {hit_percentage:.2F}")
def ProcessCSVTrace(csv_trace_file_fullpath):
    with open(csv_trace_file_fullpath) as csv_trace:
        trace_lines = csv.reader(csv_trace, delimiter=",", quotechar='"')
        source_line_histogram = BuildTraceHistogram(trace_lines)
        Present(source_line_histogram)
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Collect traces like so:\n"
            "rocprofv3 --output-format=csv --pc-sampling-beta-enabled --pc-sampling-method host_trap --pc-sampling-unit time --pc-sampling-interval 1 -- ./my_program <arguments>"
        )
    else:
        ProcessCSVTrace(sys.argv[1])
```

<a id="performance-counters"></a>

#### Performance counters

rocPROFv3 works similarly to rocPROF (v1) when it comes to gathering performance counters. You provide the tool with a [TXT file](https://rocm.docs.amd.com/projects/rocprofiler-sdk/en/latest/how-to/using-rocprofv3.html#kernel-profiling) (or json/yaml) and you run it like so:

```shell-session
$ cat counters.txt
pmc: TCC_HIT TCC_MISS
$ rocprofv3 --input=counters.txt -- ./my_program <arguments>
...
[...] Opened result file: /.../1960578_agent_info.csv
[...] Opened result file: /.../1960578_counter_collection.csv
```

**Note**

Note, however, that the CSV format output by rocPROFv3 is not the same as rocPROF (v1). To fix this issue, we [`provide a script`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/da1778d1728f02f019ebdd3100a4f790/rocprofv3.reformat.py) that will reformat the data in a friendly CSV.

**Warning**

Performance counter gathering has an overhead. In the example above, the it reaches ~ x1.08 of the original kernel duration. When creating rooflines, you should remember that fact and not compute erroneous Flop/s values.

<a id="roofline"></a>

#### Roofline

First, you will have to collect counters using rocPROFv3, here is the list we’ll need for a binary64 profiling:

```shell-session
$ cat counters.txt
pmc: TCC_EA_RDREQ_32B_sum TCC_EA_RDREQ_sum TCC_EA_WRREQ_sum TCC_EA_WRREQ_64B_sum SQ_INSTS_VALU_ADD_F64 SQ_INSTS_VALU_MUL_F64 SQ_INSTS_VALU_FMA_F64 SQ_INSTS_VALU_TRANS_F64 SQ_INSTS_VALU_MFMA_MOPS_F64
```

Once you have the results, the output CSV will have to be reformated, [`see this script`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/da1778d1728f02f019ebdd3100a4f790/rocprofv3.reformat.py).

Then you can plot rooflines using [`this script`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/1cdca254e1302b73fa16980ab1398702/roofline.py). The output would look like so:

[![../../_images/rocprofv3_roofline.png](https://dci.dci-gitlab.cines.fr/webextranet/_images/rocprofv3_roofline.png)](https://dci.dci-gitlab.cines.fr/webextranet/_images/rocprofv3_roofline.png)

<a id="pytorch"></a>

### PyTorch

PyTorch comes with its own [profiler](https://pytorch.org/tutorials/recipes/recipes/profiler_recipe.html) that integrate well into its [architecture](https://pytorch.org/docs/stable/profiler.html). We propose the following helper function that one can use to produces traces.

```python
import contextlib
import torch
import os

@contextlib.contextmanager
def GetProfiler():
    profile_dir = "ProfilerResults"
    os.makedirs(profile_dir, exist_ok=True)

    def TraceHandler(p):
        p.export_chrome_trace(f"{profile_dir}/trace_{p.step_num}.json")

    print(f"Profiling data will be saved in: {profile_dir}")
    with torch.profiler.profile(
        activities=[
            torch.profiler.ProfilerActivity.CPU,
            torch.profiler.ProfilerActivity.CUDA,
        ],
        schedule=torch.profiler.schedule(wait=10, warmup=7, active=3, repeat=1),
        on_trace_ready=trace_handler,
        profile_memory=True,
        with_stack=True,
        with_flops=True,
    ) as prof:
        yield prof

def MyTrainingLoop(do_profiling, is_master_rank):
    profiler = GetProfiler() if do_profiling and is_master_rank else nullcontext()

    with profiler as prof:
        for step in range(1, num_steps + 1):
            loss = model(input_ids, labels=labels, cache=cache)
            loss.backward()

            optimizer.step()
            optimizer.zero_grad()

            if isinstance(prof, torch.profiler.profile) and is_master_rank:
                prof.step()
```

The profiler results can be viewed in any modern web browser. Visiting <https://ui.perfetto.dev> and loading the output .json/.proto files produced by the profiler (nothing is sent to this website, you just use the interface).

One such visualization could look like that:

![../../_images/pytorch_profile.PNG](https://dci.dci-gitlab.cines.fr/webextranet/_images/pytorch_profile.PNG)

**Note**

A great PyTorch profiling introduction is given by Taylor Robie in On Hands Profiling <https://www.youtube.com/watch?v=SKV6kDk1s94>. This targets Nvidia GPUs but is also applicable to AMD GPUs.

<a id="scalene"></a>

### Scalene

Scalene is a low overhead CPU, GPU and memory profiler for Python that does a number of things that other Python profilers do not and cannot do. It runs orders of magnitude faster than many other profilers while delivering far more detailed information. It is also the first profiler ever to incorporate AI-powered proposed optimizations.

You can find the [Github repository](https://github.com/plasma-umass/scalene), or install the product via your typical Python packaged manager (say `pip`).

<a id="usr-bin-time"></a>

### `/usr/bin/time`

Most of use know about the `time` command. Fewer of us know that the `time` command is in fact a sort of intrinsic of Bash. But the GNU suite of utility tools also provide a `time` command with added features. You may access this command by specifying the whole path: `/usr/bin/time`.

The added value of this time, nd the reason it is in the profiling section is that it provides the following information:

```shell-session
$ /usr/bin/time --verbose -- <my_program>
    Command being timed: "<my_program>"
    User time (seconds): 121.01
    System time (seconds): 6.37
    Percent of CPU this job got: 123%
    Elapsed (wall clock) time (h:mm:ss or m:ss): 1:43.51
    Average shared text size (kbytes): 0
    Average unshared data size (kbytes): 0
    Average stack size (kbytes): 0
    Average total size (kbytes): 0
    Maximum resident set size (kbytes): 16706880
    Average resident set size (kbytes): 0
    Major (requiring I/O) page faults: 914
    Minor (reclaiming a frame) page faults: 3851913
    Voluntary context switches: 15500
    Involuntary context switches: 1524
    Swaps: 0
    File system inputs: 4720
    File system outputs: 3512
    Socket messages sent: 0
    Socket messages received: 0
    Signals delivered: 0
    Page size (bytes): 4096
    Exit status: 0
```

You may not the Maximum Resident Set Size (MaxRSS), the time (user and kernel), the context switch count, the input/output operation the filesystem had to do.

As such, it is a great all rounder tool to monitor memory operations.

**Warning**

`User time (seconds)` and `System time (seconds)` is in CPU time. `Elapsed (wall clock)` is the job duration (human time).

<a id="mallocprof"></a>

### `mallocprof`

A way to get a memory profile is given by [this homegrown tool](https://gitlab.com/cines/rnd/mallocprof).

To use it, simply clone the repository and run `bin/mallocprof ./my_program <arguments>`. The program will produce a trace and the plot in the working directory.

It produces the following traces, here, of the `ls` command.

![../../_images/mallocprof.ls.png](https://dci.dci-gitlab.cines.fr/webextranet/_images/mallocprof.ls.png)

<a id="python"></a>

<a id="adastra-software-stack-tools-python"></a>

## Python

**Note**

Python was not concieved to work in an HPC environment. If you are willing to put in the effort, you could try to switch to Julia <adastra_software_stack_tools_julia> instead.

<a id="cray-python-vs-python"></a>

### Cray-python vs Python:

Multiple Python environments are available:

- `cray-python`: Provided as part of the Cray Programming Environment (CPE).
- `python`: Python includes a collection of around 100 pre-installed packages, so you don’t have to create too many inodes for common python packages (check your `~/.local` )

The module `python` includes packages from various domains:

- **HPC**: Numba, mpi4py, PyMatGen, NumPy, …
- **Utilities**: ipython, notebook, cmake, virtualenv, …
- **Data Analysis**: Pandas, Dask, jupyter, …
- **Visualization**: Matplotlib, Plotly, Seaborn, …
- **Others**: Bioinformatics tools, geospatial data processing libraries, etc.

<a id="virtual-environment"></a>

<a id="adastra-software-stack-tools-python-virtual-environment"></a>

### Virtual environment

To avoid sullying your home with unrelated Python packages, you can make use of Python’s virtual environment concept. Here is a simple script showing you how to do that properly on Adastra:

```shell
#!/bin/bash

# Uncomment only if you do NOT source this script.
# set -eu

module purge

module load cpe/24.07
module load cray-python

module list

python3 -m pip install --user --upgrade pip
pip3 install --user --upgrade virtualenv
python3 -m virtualenv ./python_environment
chmod +x ./python_environment/bin/activate
source ./python_environment/bin/activate
python3 -m pip install --upgrade pip
```

Then to activate the virtual environment, do:

```shell-session
$ # If you use a Virtual Environment (VEnv):
$ # - deactivate it before loading modules;
$ # - activate it after loading modules like so:
$ source ./python_environment/bin/activate
```

When the virtual environment is activated you can freely install packages, for instance:

```shell-session
$ pip3 install transformers datasets
```

**Warning**

We recommend that you place your virtual environment in the *work* storage area or maybe, for very general and small environments, in the *home* storage area.

**Warning**

Generally, once the virtual environment is setup, you **DO NOT** want to load the module anymore.

**Note**

To deactivate the virtual environment, simply enter `deactivate` in the command line.

**Warning**

Be careful with the `cray-python` module, it defines the following variables: `${PYTHONPATH}`/`${PYTHON_PATH}` which changes some virtual environment library path.

<a id="r-project"></a>

## R (project)

R is a programming language for statistical computing and data visualization. It has been adopted in the fields of data mining, bioinformatics, and data analysis.

On Adastra, R is provided through the `r` module. A typical use of it would look like so:

```shell-session
$ module purge

$ module load cpe/24.07
$ module load craype-x86-trento
$ module load PrgEnv-gnu
$ module load r/4.4.0

$ R

R version 4.3.1 (2023-06-16) -- "Beagle Scouts"
Copyright (C) 2023 The R Foundation for Statistical Computing
Platform: x86_64-redhat-linux-gnu (64-bit)

R is free software and comes with ABSOLUTELY NO WARRANTY.
You are welcome to redistribute it under certain conditions.
Type 'license()' or 'licence()' for distribution details.

Natural language support but running in an English locale

R is a collaborative project with many contributors.
Type 'contributors()' for more information and
'citation()' on how to cite R or R packages in publications.

Type 'demo()' for some demos, 'help()' for on-line help, or
'help.start()' for an HTML browser interface to help.
Type 'q()' to quit R.

> print("Hello World!")
[1] "Hello World!"
```

<a id="installing-packages"></a>

### Installing packages

You should almost always use the GCC based Cray programming environment (`PrgEnv-gnu`) because it is likely that installing a package will require compiling files and that R packages assumes GCC.

Because we are using the Cray compiler wrappers, we need to tell R to use them, this is done by writing the following lines in the `~/.R/Makevars` file:

```make
CC=cc
CXX=CC
FC=ftn
```

For instance, lets take a look at the `bio3d` package. We know `bio3d` requires HDF5 through NetCDF, so we complete our environment with these dependencies.

```shell-session
$ module purge

$ module load cpe/24.07
$ module load craype-x86-trento
$ module load PrgEnv-gnu
$ module load r/4.4.0

$ # We satisfy Bio3D's requirements:
$ module load cray-hdf5
$ module load cray-netcdf

$ # We install the product:
$ R
> install.packages('bio3d', repos='https://cran.biotools.fr/', dependencies=TRUE)
> library(bio3d)
> example(plot.bio3d)
```

<a id="trivia"></a>

## Trivia

<a id="clangformat"></a>

### ClangFormat

[ClangFormat](https://clang.llvm.org/docs/ClangFormat.html) is a tool that enables automatic source code formatting. It is based on Clang (parsing).

<a id="clangtidy"></a>

### ClangTidy

[ClangTidy](https://clang.llvm.org/extra/clang-tidy/) is a clang-based C++ “linter” tool. Its purpose is to provide an extensible framework for diagnosing and fixing typical programming errors, like style violations, interface misuse, or bugs that can be deduced via static analysis. clang-tidy is modular and provides a convenient interface for writing new checks.

<a id="lfs-find"></a>

### `lfs find`

This tool provides a subset of the `find` command. This is the recommended alternative on Lustre based filesystems as it optimizes [MDS/MDT](../../data_storage_and_transfers/index.md#adastra-storage-and-transfer-storage-space-acronyms) usage.

```shell-session
$ lfs find <a_directory> -type f -print
```

<a id="numactl"></a>

### `numactl`

Control NUMA policy for processes or shared memory. Basically, allows you to bind ranks to a set of hardware thread. This is usually burrowed into *binding script* such as in [this one](../../porting_optimization/detailed_binding_script.md#porting-optimization-detailed-binding-script).

<a id="visit"></a>

<a id="adastra-software-stack-tools-visit"></a>

### VisIt

VisIt is an Open Source, interactive, *scalable*, visualization, animation and analysis tool.

VisIt is exposed through modules:

```shell-session
$ module spider visit
```

<a id="vscode-visual-studio-code"></a>

<a id="adastra-software-stack-tools-trivia-vscode"></a>

### VSCode (Visual Studio Code)

We propose two ways of using VSCode on Adastra.

- The **recommended** way is to use the `Remote - SSH` extension. It will allow you to open any folder on a remote machine using SSH and take advantage of VS Code’s full feature set. In practice a small server will be running on the login node and serve information to your client, running locally on your PC. We **strongly recommend** that you always connect to a [specific login node](../../user_support/index.md#adastra-accessing-connection) instead of a random one to avoid having multiple server running on different login nodes. Note that to use the `Remote - SSH` mode of operation, you should first contact [svp@cines.fr](mailto:svp%40cines.fr) and ask for VSCode access on the login nodes.
- The simplest way is using X11 forwarding. You would download the VSCode binaries and run them on Adastra. This is bad for many reason including high latency and bad usage of shared login node resources.

<a id="current-bash-script-directory"></a>

### Current `bash` script directory

Frequently the need arises to execute a script with a directory that is relative to the script source file. Using tools such as `${BASH_SOURCE[0]:-${0}}`, `dirname` and `realpath/readlink` we can achieve such goal.

In `bash` you can use:

```shell
# Or:
SCRIPT_DIRECTORY="$(dirname -- "$(readlink -f -- "${BASH_SOURCE[0]:-${0}}")")"
# Or:
SCRIPT_DIRECTORY="$(dirname -- "$(realpath -P -- "${BASH_SOURCE[0]:-${0}}")")"
```

**Warning**

You should place this line at the top of your shell script, if you change directory, the behavior is not guarentee anymore.

**Note**

Variants based on `pwd -P`, `/usr/bin/pwd` and `cd -P` such as, `SCRIPT_DIRECTORY="$(cd -- "$(dirname -- "${BASH_SOURCE[0]:-${0}}")" &>/dev/null && pwd -P)"` do work if the script being launched is itself a link.

<a id="source"></a>

### `source`

Read and execute commands from a file into the current shell environment and return the exit status of the last command executed from filename. This differs from when you run a shell script.

```shell-session
$ source ./environment.sh
```

<a id="xeyes"></a>

### `xeyes`

A Simple tool used to check if X11 forwarding is working. If X11 forwarding is properly setup you should see two eyes looking at your mouse cursor.

![../../_images/xeyes.PNG](https://dci.dci-gitlab.cines.fr/webextranet/_images/xeyes.PNG)

<a id="watch"></a>

### `watch`

Execute a program periodically, showing output fullscreen. This is useful to watch the result of a command evolves.

```shell-session
$ watch -n0 -- "rocm-smi"
```

<a id="wget"></a>

### `wget`

A non-interactive network downloader. It is useful to retrieve documents on a network and support many protocols (of which, http and ftp).

```shell-session
$ wget "https://github.com/ROCm/rccl/archive/refs/tags/rocm-6.0.0.zip"
```

**Note**

Put quotes around the URLs to avoid nasty issues.
