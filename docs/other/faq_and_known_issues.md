<!-- Source: https://dci.dci-gitlab.cines.fr/webextranet/other/faq_and_known_issues.html -->
<!-- Title: FAQ & known issues -->

<a id="faq-known-issues"></a>

<a id="other-faq"></a>

# FAQ & known issues

<a id="faq"></a>

## FAQ

- **Can I share my login to my colleague ?**

They are strictly personal, as as specified in the [`user policy governing the use of computer resources of CINES`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/64d0992db9a2ff23f3f6ac17a3264b1e/charte_usage_ressources_informatiques_CINES.pdf).

- **Can I use ssh keys for my connections to Adastra ?**

SSH authentication using an SSH key pair (private key/public key) is not possible on Adastra. This security measure is a local decision at CINES, each institution is responsible for the security of its information system. Some users implement best practices in key management, but the community is very heterogeneous, so we have to take into account the worst cases to be able to ensure the security of our environments. We are aware that the rule is strict and can lead to difficulties in use.

- **Can I install graphics software on the Adastra computing partitions (MI250X and Genoa) ?**

We do **not** believe that it is appropriate to install graphical tools on standard compute nodes. The High Performance Data Analytic (HPDA) partition is dedicated to this type of load.

- **Why does my job sit in the queue for so long ?**

The machine is most likely loaded and other jobs may have higher priority than yours.

Priorities are calculated with:

> - the age of your job, an older job will see its priority increased;
> - the fairshare of your user and group, the more resources your group has used recently, the less priority you will get.

A rule of thumb is that if you wait a long time it is because the machine is quite loaded and we can’t do much about that. Check [this document](../user_support/index.md#adastra-running-jobs-queues) for more details.

Waiting for 1-2 hours to get a node is expected. It should be noted that Adastra tends to be populated by large, frequent or longer jobs and that, since ~2023. This can lead to longer queue times due to the lack of fast turn-over. The solution to enter in queue faster is to correctly define the job duration (that will give you more chance of filling a hole in the node schedule).

- **Can I compute more than 24 hours ?**

In order to have an optimal use of Adastra, the maximum standard duration of the jobs has been fixed at 24 hours. This allows a more efficient filling of the machine. It also forces the use of a **restart mechanism** in the user’s code leading to minimized losses in case of issues. On the HPDA partition, the limit is 6 hours.

- **A job interrupted due to a technical problem: is a refund possible ?**

If the loss of computation hours is due to a hardware problem, asking [svp@cines.fr](mailto:svp%40cines.fr) for a refund is possible.

- **Can I use ‘mpirun’ to start my parallel codes ?**

You should use SLURM’s `srun` command.

- **My program crashed in a job, where can I find the coredump files (memory dump) for each rank of a job ?**

See the [Coredump files](../user_support/index.md#adastra-running-jobs-core-dump-files) document.

- **Why I can no longer submit jobs ?**

You can start by making sure your compute hours, file and disk space quotas are not exceeded via the `myproject --state [project]`. Additionally, make sure the machine is available by connecting to <https://reser.cines.fr/> or checking your emails for Cines notifications. If the problem is not obvious, ask [svp@cines.fr](mailto:svp%40cines.fr).

- **My project has just finished and a new one is about to start. Do I need to move files from my *home*, *work*, *store* and *scratch* storage areas into the new project ?**

Yes. A project lasts for 1 year. After this year, Cines undertakes to keep the data for a further 6 months. If you set up a new project to use the machine, you’ll need to move your data from one project to another.

- **What are the QoS/class for jobs on Adastra (max job time, max number of nodes, etc.) ?**

Apart for the maximum job duration mentioned above, CINES does not disclose the QoS. The SLURM scheduler will automatically place your job in the right QoS depending on the duration and resource quantity asked.

- **I’d like to transfer data from the TGCC to the Cines via scp. How do I do this?**

You can either use the [CCFR network](../data_storage_and_transfers/index.md#adastra-storage-and-transfer-transfer-ccfr) or copy from login node to login node. In both cases, you can use tools such as `rsync` or `scp` but routing the traffic towards the CCFR network will be faster. You can find information on how to use these tools [in this document](../data_storage_and_transfers/index.md#adastra-storage-and-transfer-transfer-tools).

- **What are the CCFR FQDNs ?**

To route traffic towards the CCFR network, one must use specific nodes and their associated DNS names. The DNS address are given [in this document](../data_storage_and_transfers/index.md#adastra-storage-and-transfer-transfer-ccfr).

- **How should I debug a program ?**

We recommend that you first use the [sanitizer](../software_stack/tools/index.md#adastra-software-stack-tools-debugging-sanitizer) and `valgrind` like tools. Then rely on `printf` based debugging and finally parallel debugging tools such as DDT. Additionally, CINES allows you to save coredumps which you can analyze later using `gdb`. As of 2025, CINES offers the DDT OpenMP and MPI aware debugger.

- **Where can I find the user reports (compte rendu utilisateur du C4) ?**

You can find the user reports (compte rendu de C4) on the <https://reser.cines.fr/ccc/listC4File> webpage. You need an account at CINES to access these documents.

- **Where can I change my password ?**

First, connect to Adastra then use the `passwd` command. If you can not connect to Adastra, ask [svp@cines.fr](mailto:svp%40cines.fr). Password requirements are: a minimum of 12 characters, 1 uppercase, 1 lowercase, 1 digit, 1 special character and not using an older password. We recommend that you change the password before expiration (a password last 1 year).

- **Can I use remote VSCode or SSH port forwarding ?**

It is possible. Please refer to [this document](../software_stack/tools/index.md#adastra-software-stack-tools-trivia-vscode).

- **My code requires a dependency, can you build it for me ?**

You can always contact [svp@cines.fr](mailto:svp%40cines.fr).

**Warning**

Software that relies on more than it can afford is **bound to significantly break**. We strongly encourage you to reduce the number of dependencies you rely on and to clearly define what your code **requires** to work. Do not blindly add a dependency, it has a cost (human, time, headache, etc.). A dependency is not necessarily code, having `march=native`, auto detection is a form of dependency on the hardware or system. For instance, please **do not add** a dependency for a [better implementation of an assert](https://github.com/jeremy-rifkin/libassert). Spack or GUIX are not a universal solution, robust installation procedure and low dependency count however, is.

- **Can I expect a GPU on the login node ?**

No definitely not. This is a a bad practice to have auto detection of the hardware at compile time. Instead you should rely on machine file or CMake toolchains to describe for what kind of hardware you want to compile (never use the `-march=native` flag as a default). The Adastra login node’s CPUs are not the same as the CPUs on the GPU nodes. The login nodes do not have GPUs, so auto detection may fail. Module and compiler flags exist to properly define the target architecture. More details are given in [this document](../user_support/index.md#adastra-programming-environment-targeting-architecture).

- **Can I use LLM agents on Adastra ?**

Yes. You are responsible for the action of the agent.

<a id="known-issues"></a>

<a id="other-known-issues"></a>

## Known issues

- 2025/08/20: [SLURM] Using the `thread-per-core` option on SLURM allocations (`salloc` or `sbatch`) leads to `srun` misbehaving and launching only one rank with one core. The `thread-per-core` flag should be given to `srun` instead, which is semantically more correct as `srun` describes how the allocated resources should be used.
- 2025/07/17: [DDT] An error message appears when you launch DDT in your terminal, this error message should not be taken into account, as DDT is fully operationnal, and the communication with a proxy not in use in our configuration.

```
Error communicating with Licence Server slurm0.hsn0.adastra.cines.fr: The proxy type is invalid for this operation.
Attempting again while ignoring proxies.
Error communicating with Licence Server slurm0.hsn0.adastra.cines.fr: The proxy type is invalid for this operation.
Attempting again while ignoring proxies.
```

- 2025/06/20: [CONDA|PROXY] If you get a timeout or error such as `ProxyError: Conda cannot proceed due to an error in your proxy configuration.`, please configure `conda` like so: `conda config --set proxy_servers.http  "proxy-l-adastra.cines.fr:3128" --set proxy_servers.https  "proxy-l-adastra.cines.fr:3128"`.
- 2025/06/20: [SVN|PROXY] If you get a timeout while using svn, please ensure CINES’s proxy is well defined in your configuration file ~/.subversion/servers such as: `http-proxy-host = proxy-l-adastra.cines.fr http-proxy-port = 3128`.
- 2025/06/19: [SESSION|HPDA] If you get a black screen when opening a session, close the existing session before starting a new one.
- 2025/06/19: [JUPYTER|HPDA] Only one instance of JupyterLab can be launched on HPDA nodes. Attempting to open multiple sessions may result in the error: `Firefox is already running, but is not responding. To use Firefox, you must first close the existing Firefox process, restart your device, or use a different profile.`
- 2024/06/20: [CCE|ROCM] : If you encounter link error such as `lld: error: undefined symbol: llvm.amdgcn.readfirstlane.i32` this is probably because you tried mixing CCE 18 with ROCm 6.2.1. you should instead use ROCm 6.1.2.
- 2024/06/20: [LIBSTDC++] If you have libstdc++ version mismatch signaled by messages such as `` \`GLIBCXX_3.4.29' not found (required by ..) `` you can either load the `gcc/13.2.0` module or use `export LD_LIBRARY_PATH=/opt/cray/pe/gcc/12.2.0/snos/lib64:${LD_LIBRARY_PATH}`.
- 2024/06/07: [LIBFABRIC] The last SlingShot update (2.2.0) may have introduced a performance regression in some codes. We provide the following environment variable to fix the issue: `export FI_MR_CACHE_MONITOR=kdreg2`. (Typical performance regression or on the order of x1.1 to x2).
- 2024/03/01: [LIBSCI] Cray LibSci allocates internal buffers onto the stack and therefore expects an unlimited stack size. If your application segfaults when linked to Cray LibSci, try setting the stack size from the command line, using the `ulimit -s unlimited` command. If this is not possible, set the environment variable `CRAYBLAS_ALLOC_TYPE` to 2 on Cray platforms.
- 2024/03/01: [CCE] : The Cray OpenMP backend implementation does not define affinity until the first `omp parallel for` is reached. This is in opposition with the OpenMP standard chapter 6 section 4: `the initial thread is bound to the first place in the place-partition-var ICV prior to the first active parallel region`.
- 2024/01/20: [PYTHON|CRAYPE] The `cray-python` modules in version 3.10.10 and 3.11.5 do not define `${LD_LIBRARY_PATH}` towards the Python runtime library. Work around the issue by defining `export LD_LIBRARY_PATH="${CRAY_PYTHON_PREFIX}/lib:${LD_LIBRARY_PATH}"`.
- (**solved**) 2024/01/12: [ROCM] : Due to a bug introduced in January CPE update, loading a `PrgEnv-amd`, `amd` or `amd-mixed` module does NOT defined the `${ROCM_PATH}` environment variable. You can extend your environment by appending a `module load rocm/X.Y.Z` where the ROCm module version matches the one of your `amd` or `amd-mixed` module.
- 2024/01/12: [CLANG] : In january we update the software stack. This introduced the following error `` /lib64/libstdc++.so.6: version `GLIBCXX_3.4.26' not found (required by /opt/cray/pe/lib64/cce/libclang-cpp.so.15) `` when you use a system (`/usr/bin`) LLVM/Clang product. To work around the issue do: `export LD_LIBRARY_PATH="/usr/lib64:${LD_LIBRARY_PATH}"`
- 2024/01/01: [ROCm] : The ROCm layout changed. More details on <https://rocm.docs.amd.com/en/docs-6.0.0/conceptual/file-reorg.html>. Warning such as `warning: "XXX has moved to /opt/XXXX/include/XX and package include paths have changed. Provide include path as XXX when using cmake packages."` can be ignored as they are inherent to a small typo in the `rocm` modules.
- 2024/01/01: [GCC|GENOA] The GCC toolchain does not support Zen4 until version 13. If you load the `craype-x86-genoa` and use a `PrgEnv-gnu` you will get errors like this: `f951: Error: bad value 'znver4' for '-march=' switch`. To work around the issue, either your use `craype-x86-rome` instead, or after load `PrgEnv-gnu gcc/13.2.0`.
- 2024/01/01: [CRAYCLANG|CMAKE] Since CMake 3.28, CrayClang is recognized as CrayClang and not, Clang. You may have to check your script if you branch on that fact.
- 2023/11/01: [CRAYMPICH|CRAYPAT] If when profiling using CrayPAT you encounter unexpected MPI crashes, try using the following environment variable: `export PAT_RT_SAMPLING_MODE=bubble`.
- 2023/10/01: [SLURM|SHARED] If you encounter the following kind of SLURM error when using allocated resources `srun: fatal: SLURM_MEM_PER_CPU, SLURM_MEM_PER_GPU, and SLURM_MEM_PER_NODE are mutually`, you can work around the issue using the following `srun` flag: `--mem=0`.
- 2023/09/03: [UNIQUE_LOGIN|DATA_TRANSFER] The quota is computed based on the number (inode) and size (octet) of files belonging to a given project group. If a user moves files from one project, say project A, to another, say project B, without changing the files’ group (`chgrp`), then, even though the files now resides in a directory of project B, they contribute to quota of project A. To workaround this issue, use something like: `chgrp -R <project_B_group> <moved_folder>`.
- 2023/09/01: [CRAYMPICH] We are aware of `MPI_Iprobe` issues related to hanging. If you have a **small** reproducer with few MPI ranks and that does not need to run for 10 hours contact us at [svp@cines.fr](mailto:svp%40cines.fr) .
- 2023/09/01: [CRAYFTN] The Cray Fortran compiler is known to have a buggy implementation of Link Time Optimization (LTO) sometime called InterProcedural Optimization (IPO) or IPA. If you encounter a crash where the compiler produces a stacktrace and if you observe any sign of `ipa` in it or if at runtime you get nonsensical results or crash, try **lowering** the optimization level using the `-hipa0` flag.
- 2023/03/01: [CRAYFTN] For Fortran code, if one encounter crashes and the stacktrace (if any) contains `tcmalloc` related strings: try the `-hsystem_alloc` crayftn **link time** flag. Note that this error could also be a red flag for a memory management issues in your code. [More on Google’s TCMalloc](https://github.com/google/tcmalloc).
- 2023/01/01: [CRAYPE] The warning `Unloading the cpe module is insufficient to restore the system defaults. Please run 'source /opt/cray/pe/cpe/22.12/restore_lmod_system_defaults.[csh|sh]'.` can be safely ignored (for most purposes).
- 2023/01/01: [CRAYCC|HIP|C++|KOKKOS] There is a know performance issue on some heavily templatized C++ HIP code when one does **not** specify the following compilation option: `-mllvm -amdgpu-early-inline-all=true -mllvm -amdgpu-function-calls=false`. These flags are implicitly added by the `hipcc` amdclang compiler wrapper.
- 2023/01/01: [CRAYCLANG|CLANG] Clang now defaults to the [DWARF](https://en.wikipedia.org/wiki/DWARF) 5 format for debugging information. There are known issues with [GDB and recent DWARF format](https://sourceware.org/bugzilla/show_bug.cgi?id=29606). If you encounter such issues or if you get the `Dwarf Error: Cannot handle` error message, add the `-gdwarf-4` compiler flag to your compilation script.
- 2023/01/01: [ROCm|MPI] Having too many process hitting a single GPU may produce this kind of warning: `Expect reduced ROCm performance.`. This is due to having too many HAS hardware queues on a single GPU. Reduce the number of process on that GPU.
- (**solved**) 2022/09/01: [SLURM|BINDING|ROCm|CRAYMPICH] SLURM’s `gpu-bind` flag is known to cause issues with MPI communications. You can refer to the binding script presented in [Proper binding, why and how](../porting_optimization/index.md#porting-optimization-performance-tuning-monitoring-proper-binding-why-how) for a workaround.
- (**solved**) 2022/09/01: [CRAYMPICH|SLIGNSHOT] In case you are regularly subject to *sick* nodes that hangs your job (**not** RAM ECC issues), you may try defining **one of** the following environment variable before your `srun` command: `export FI_MR_CACHE_MONITOR=memhooks` or (exclusively) `export FI_MR_CACHE_MAX_COUNT=0`.
- 2022/09/01: [HARDWARE|CRAYMPICH|SLIGNSHOT] Some nodes are *sick*. They may *hang* your MPI communication (in barrier, or collective operations). Some node have RAM ECC issues which is expected for a new machine. Please report these faulty nodes at [svp@cines.fr](mailto:svp%40cines.fr).
- 2022/12/01: [ROCm|OOM] The GPU’s memory is known to easily fragment which is arguably a ROCm allocator issue. A solution is to use an ever growing memory chunk (*a la std::vector*) with a growth factor strictly inferior to the [golden ratio](https://en.wikipedia.org/wiki/Golden_ratio). A factor of 1.3 to 1.5 offers good memory chunk reuse, reducing fragmentation while also providing amortized constant back insertion complexity.
- 2022/12/01: [GENOA|TRENTO|CPU] If you get errors similar to: `srun: error: <node_name>: tasks xx : Illegal instruction (core dumped)`; make sure you used the right module for the harware partition you are targeting. `craype-x86-trento` for the AMD GPU MI250 partition and `craype-x86-genoa` for the AMD CPU GENOA partition.
- 2022/12/01: [LIBSCI] If you get errors similar to: `[CRAYBLAS_WARNING] Application linked against multiple cray-libsci libraries`; make sure your binary is not linked against two different LibSci (for instance, a serial an OpenMP variant). This issue can generally be safely dismissed if the user does not expect multithreaded BLAS.
- 2022/12/01: [SSH] If, for whatever reason, your SSH session gets closed due to inactivity, you may benefit from adding the following lines into your machine’s ssh config file (`~/.ssh/config`):

```
Host *
    ServerAliveInterval 69
```
