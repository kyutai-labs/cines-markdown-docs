<!-- Source: https://dci.dci-gitlab.cines.fr/webextranet/porting_optimization/index.html -->
<!-- Title: Porting & optimization -->

<a id="porting-optimization"></a>

# Porting & optimization

Many programmers appreciate shiny new software, but few are prepared to start over or refactor. This is an expensive task in terms of human resources and time (and therefore money). The process of porting from a scalar architecture (say, CPU) to an *accelerated*/*vectorial* architecture (say, GPU) bears similarities to the reverse of what was asked of the simulation communities decades ago, when they had to move from a vector programming model (towards the 90s) to an SPMD model (mainly based on MPI or PVM). Today, we want to retain the SPMD model to distribute calculations, but within each program instance (for example, an MPI rank), we expect the program’s calculations to be compatible with a vector processor. Tools exist to avoid having two versions of the same code, one for CPUs and one for GPGPUs, see below.

This part has various guidelines for porting and optimizing code for Adastra, but in the end, what matters most after the method is your team’s ability to rewrite or modify your code so that it can exploit the vectorial nature of GPGPUs; and that is experience no set of guidelines can provide.

**Note**

As a TLDR; one can make a pretty bold yet educated assumption by saying that for most of HPC code, the time to solution is either bound by memory latency or memory throughput. *In fine*, making them a glorified or fancy version of `memcpy`.

<a id="porting-to-gpu"></a>

<a id="porting-optimization-porting-to-gpu"></a>

## Porting to GPU

The fact is that there is no platform independent program and thus no such thing as portable programs, only ported implementation of an algorithm. What exists though, is **platform commonalities**. The most ported algorithm generally emanate from or lead to a standard which tries to make use of these platform commonalities. Future proofing your implementations is impossible by definition but you can try to mitigate the problem by relying on a wildly used and successful standard. One should never go off the rails and disrespect the standard unless ones knows what he is doing. This happen often without one knowing it though! Thus the first step in porting an algorithm is making sure that in the first place, the program respects the standard (read books, do tests, attend or watch talks and read the full manual).

In this chapter we present some advantages and disadvantages to GPUs without going into the details of the Instruction Set Architecture (ISA) nor into the microarchitecture. We present technologies one can use to manipulate the GPU. Then we present the minimal speedup acceptable to make use of the GPUs. Finally we expose typical a porting process.

<a id="gpus-pros-and-cons"></a>

### GPUs, pros and cons

Nowadays, CPU manufacturer tend to stagnate on frequency but still succeeded in packing more cores and transistor on the die. CPU are historically and for practical purposes, heavily optimized machines that treat a single thread as fast as possible and aiming to provide somewhat low latencies on the instructions it executes. The modern CPU tries to master two fields, single thread latency and throughput.

In a purely single threaded environment, say Single instruction single Data (SISD) in Flynn’s taxonomy, latency is the inverse of throughput. That is not the case of multithreaded environment and as such, the CPU tries to do two different things well. Note that modern processor are absolutely not SISD as they notably contain instruction pipelines.

The GPU, conceptually simpler than the CPU, is conceived to execute a similar treatment on independent data. It maximizes operation throughput and is very efficient in doing so. But this behavior comes with a loss of (*performance*) generality, a CPU is versatile, a GPU kernel is resource sensitive.

**Important**

If you seek to do greener computations, **make good use of the GPUs**, especially in large or national sites where the energy efficiency is high.

If your algorithm exposes parallelism of treatment on independent data you may benefit significantly from using GPUs. The list below exposes more potential bottleneck potentially making a GPU implementation impractical:

> - low volume of data;
> - too many data dependency, data processing order (loop carried dependency, atomics, heavy synchronization);
> - unsupported data type (convoluted C++ object, large allocation inside kernels, too many temporary scratch buffers);
> - high code/algorithmic complexity;
> - too many copies between CPU and GPU memory;
> - low arithmetic density (time to solution dominated by memory access, too much random accesses);
> - need for bit reproducibility with CPU results;
> - the use of double precision IEEE 754 numbers (although high-end cards tend to lose this limitation). Also, GPUs do not necessarily provide a strict IEEE 754 standard implementation in all circumstances (see the respective ISA);
> - the organization of the data in Array Of Structure (AOS), as opposed to Structure Of Array (SOA) or Array Of Vectorized Struct (AOVS);
> - the use of non-scalable algorithms (as opposed to embarrassingly parallel algorithms);
> - computational kernels that are too large (too many temporary variables and registers used leading to spilling);
> - highly coupled code or functions with *large* side effects (as opposed to the pure functions of functional programming).

For each element given above, you may have to engineer a new solution which can range from a trivial loop interchange to a complete rewrite of the algorithm.

<a id="available-programming-technologies"></a>

### Available programming technologies

First and foremost, when a developer seek to solve a problem in a production code, he shouldn’t have to reimplement what already exist. His goal is in fact to produce a code made of component which he can assemble to solve a larger problem. This is the spirit that lead to, for instance, the Basic Linear Algebra Subroutines (BLAS) specification. This separation between the interface that is how the function modifies the *visible* state of the program and the implementation of this state transition is key to reusable software. In this section, we introduce some technologies available on Adastra. Not all the technologies require the same level of involvement in understanding the underlying hardware and usage nor does it provide the same feature set.

It is the job on the researcher and implementer to clearly define:

> 1. What problem are you solving ?
> 2. How will we do it (which algorithm will you use) ?
> 3. How will it be implemented ?

<a id="specialized-computation-libraries"></a>

#### Specialized computation libraries

When creating a code and the algorithm is known or, when porting a code, we generally start with a quick look at the last bullet, *how will it be implemented* and we search for the appropriate tool, decently available (ported) on the architectures we care about.

We provide a list of software that may satisfy your needs in [this document](../software_stack/libraries/index.md#adastra-software-stack-libraries-low-level-primitives). If your requirements are not met, you can install the software yourself or ask [svp@cines.fr](mailto:svp%40cines.fr) to provide it.

<a id="intra-process-parallelization-technologies"></a>

#### Intra-process parallelization technologies

We provide a list of compiler toolchain that may satisfy your needs in [this document](../user_support/index.md#adastra-programming-environment-intra-process-parallelization-technologies). If your requirements are not met, you can install the software yourself or ask [svp@cines.fr](mailto:svp%40cines.fr) to provide it.

<a id="opinionated-default-choice"></a>

##### Opinionated default choice

What would an ideal tool be like ? It would do the job, and last long. Potentially evolve as the job changes. *Doing the job* is a matter of feature offered and their state of implementation. *Lasting long* is a matter of how used is the technology, how does the community support materialize and where is the money coming from.

If your code is in Fortran, you have few viable choices when it comes to GPU programming. We would recommend **OpenMP** for the reason given above. Notably, Clang LLVM is getting a significant push thanks to US exascale projects and AMD’s open source contribution via [AOMP](https://github.com/ROCm-Developer-Tools/aomp). If your code is in C or C++, you have multiple choices ranging from handwritten GPU assembly or high level wrappers (or abstraction layers). Most scientific codes, say 80-90 % (anecdotal) of a code base can be written in term of a high level technology like **Kokkos** or **OpenMP**. Most loops are simple (or should be if you are familiar with HPC notions).

OpenMP has a long and great track record when it comes to parallelizing codes on shared memory, multithreaded systems. Since version 4.0, OpenMP has started gaining accelerator (say, GPU/FPGA) offloading capabilities. Today, well established compilers like Clang LLVM, support a lot of OpenMP v5.0 features providing a significant framework for parallelizing tasks both on the CPU and GPU.

OpenACC is also interesting but most of its support is only available on the NVIDIA **proprietary compiler**. The latest features are not implemented in the Cray compiler (currently there is full support for version 2 of the standard and mixed feature support up to version 3.1 for **Fortran code** only). As such, it **may** not be possible to run an OpenACC code developed for the NVIDIA compiler on a machine such as Adastra. Some modification are to be expected (this shouldn’t be hard as long as you are true to the standard).

It is safe to say that for simple loops, OpenMP give similar performance to simple HIP or CUDA code. On the other hand, for large loops, loops accessing the memory in a non trivial way or code that requires specific synchronization, OpenMP tends to under perform. This is due to the fact that OpenMP tries satisfy a lot of use cases through heavy use of abstractions. It has the side effect of adding a lot corner cases that the OpenMP implementation needs to account for to be compliant. These corner cases’ complexity leads to a very heavy burden left on the compiler’s optimizer. A non optimized OpenMP code will be slow, especially on GPU like accelerators. A **lot** of effort is going into optimizing OpenMP code (on the compiler side of thing), notably for use on GPUs.

**Important**

Most of the offloading can be done using a high level technology. Keep the platform specific implementation as small as possible. OpenMP is a great tool is reducing this platform specific surface.

**Important**

When choosing to add a technology to your code base, ask yourself, am I using this tool just because trendy. Be wary of exotic technologies. Know that hardware portability is not performance portability.

**Important**

Try to minimize trivial dependencies.

<a id="message-passing-library"></a>

#### Message passing library

MPI is the defacto standard for HPC message passing followed maybe by Communication Collective Libraries like NCCL/RCCL.

CINES provides a [document describing](../software_stack/libraries/index.md#adastra-software-stack-libraries-mpi-cray-mpich) the use of MPI implementation exposed on Adastra.

<a id="minimal-viable-speedup"></a>

<a id="porting-optimization-porting-to-gpu-minimal-viable-speedup"></a>

### Minimal viable speedup

<a id="how-to-compare-two-machines"></a>

#### How to compare two machines ?

Comparing two different hardware is not trivial, multiple metrics exist, different hardwares may require different algorithm with inherently different floating point and memory usage profiles.

In the following example, we will compare a CPU and a GPU node of similar generation (2022).

**The CPU node has the following specificities:**

- 192 cores able to reach a constant 2.4 GHz clock speed and an aggregated 7.37 TFlop64/s;
- An aggregated 768 Mio of L3 with (loosely computed) 0.921 To/s of write throughput at 2.4 GHz (16 bytes/cycle/L3 and 24 L3);
- An aggregated 192 Mio of L2 with (loosely computed) 14.7 To/s of write throughput at 2.4 GHz (32 bytes/cycle/L2 and 192 L2);
- An aggregated 6.1 Mio of L1 with (loosely computed) 29.5 To/s of write throughput at 2.4 GHz (64 bytes/cycle/L1 and 192 L1);
- An aggregated 768 Gio of DRAM with 921 Go/s R/W throughput;
- A peak power consumption at [945 W](../architecture/index.md#architecture-adastra-scalar-nodes) (peak) leading to 7.8 GFlop/J;
- A node density of 4 such CPU node per Cray Shasta 1U blade.

**Note**

On AMD Genoa, the L3 cache is shared by groups of 8 cores (one CCD), whereas L1 and L2 caches are private to each core. As a result, L3 throughput does not scale with the total number of cores in the same way L1 and L2 throughputs do.
With 16 bytes/cycle per L3 instance, the aggregate L3 throughput of a 192-core node is: (192/8) L3 * 16 bytes/cycle/L3 * 2.4 GHz = 921 Go/s.

**The GPU node has the following specificities:**

- We disregard the CPUs;
- 8 devices able to reach a constant 1.5 GHz clock speed and an aggregated 169 TFlop64/s;
- We disregard the GPU caches as not practical (SMEM is not considered here);
- An aggregated 512 Gio of HBM with 12.8 To/s R/W throughput;
- A peak power consumption at [2670 W](../architecture/index.md#architecture-adastra-scalar-nodes) (peak) leading to 63.2 GFlop/J;
- A node density of 2 such CPU node per Cray Shasta 1U blade.

<a id="hardware-efficiency-metrics"></a>

#### Hardware efficiency metrics

- Floating point computation throughput (Flop/s): the floating point operation per second, the Top500 metric of choice which tends to be less pertinent than memory throughput.
- Memory throughput (Go/s or Gio/s): the cache and global memory R/W throughput, most code are memory bound, this is crucial.
- Memory throughput (Go/s or Gio/s) per *node volume*: same as above, adjusted by the space a node physically take (CPU nodes are denser);
- Flop/J: the computation energy efficiency (disregarding cooling, network and storage).
- Space per node: here, do not understand space as memory, but as physical space taken in the data center;
- Buying cost per node, Flop/$, maintenance cost.

We wont expend on IO speeds (storage and network).

<a id="application-efficiency-metrics"></a>

#### Application efficiency metrics

- Flops to solution: assume that on machine A, we use an algorithm that is well suited to its hardware and needs and hypothetical 10 Flop per simulation. On machine B we use a different algorithm that is better suited to its architecture and need 15 Flop to reach a solution. Machine A has a better Flops to solution efficiency. (note: neural network people call that Hardware Flop Utilization (HFU)). A simple reason on why it this efficiency differs between machines could be due to a recomputation ([rematerialization](https://en.wikipedia.org/wiki/Rematerialization)) needed on machine B due to the algorithm used on it.
- Load to solution: similar to the one above, but for memory loads. Loads refer to the global memory loads (LLC <-> HBM/DRAM), or L3 loads (L2 <-> L3), etc.. A simple reason on why this efficiency differs between machines could be due to a use of cache blocking on machine A and a streaming algorithm on machine B. Streaming here, basically means disregarding the caches and going all out on saturating the HBM/DRAM throughput.
- Energy (J) To Solution (ETS): assume that machine A can do 10 Flop/J and machine B can do 100 Flop/J. Or that you need 10 J to solution or 100 J to solution.
- Time To Solution (TTS): assume that you need 10 seconds to get your result, or 100 seconds.

<a id="mixed-efficiency-metrics"></a>

#### *Mixed* efficiency metrics

- Power per *node volume* (power density): if blade of machine B consumes x4 what a blade of machine A needs, expect at least a x4 time to solution speedup;
- Buying cost per node: if node B costs x4 node A, expect at least a x4 time to solution speedup;
- Energy to solution per node (running cost): if node B needs x4 the energy of node A, expect at least a x4 time to solution speedup (compared to power density given above, this metric does not assume you reach the peak power the node consumes).

<a id="expecting-a-speedup"></a>

#### Expecting a speedup

We’ll assume we come with a code working on a CPU node and want to know the expected speedup one should obtain on a GPU node.

If you naively focus on the hardware efficiency metrics, then you can trivially say, that in our case, one should expect:

- A 169/7.37=22.9 Flop64/s speedup from CPU to GPU;
- A 63.2/7.8=8.1 Flop64 energy efficiency speedup from CPU to GPU;
- A 12.8/0.921=13.9 **global** memory R/W throughput speedup from CPU to GPU;
- A (2*12.8)/(4*0.921)=6.9 **global** memory R/W throughput speedup from CPU to GPU adjusted by node volume;
- A 12.8/14.7=0.87 R/W throughput speedup from CPU to GPU assuming nontrivial CPU **cache blocking** (see the aside below for details).
- A (2*12.8)/(4*14.7)=0.435 R/W throughput speedup from CPU to GPU assuming nontrivial CPU **cache blocking** (see the aside below for details) adjusted by node volume;
- A 2/4=0.5 space efficiency speedup from CPU to GPU (a GPU node take more physical space);

If you focus on the application efficiency metrics, things get more complicated. The R/W, FLop, integer operation count will change depending on the algorithm you use which itself should differ depending on the kind of device you use (GPUs are NOT CPUs). If you know theses metrics for both version of the code (which is possible using hardware counters), you can derive some fancy formula that models the TTS or ETS and extrapolate to new machine specificities.

If you assume the algorithm does not change, that you know the time spent in Flop/IntOp/memory read and write/IO so that you can model the TTS, you can simply divide each TTS contribution by the expected speedup. Say, you spend 40% of the time in Flop, you could do 40%/22.9=1.74%. Once thats done, you reconstruct the TTS. Note that this assumes you don’t change what you are bound by. It’s possible that going from CPU to GPU you go from compute bound to memory bound (GPU are over provisioned in Flop/s). Clearly this seems much to coarse to give reasonable insights except maybe for GEMM like operations.

Out of all these metrics, a few stand out:

- Power per *node volume*;
- Energy (J) To Solution.

These give a **lower bound** to the speedup you should get to legitimately use the device you want to port to.

For Power per *node volume*, we have two big assumptions, the first is that for each device we compare, we should have a code that is well enough tuned to able to burn as much power as the device can allow. The second is that the blades are of the same integration quality (cream fo the crop node density), same generation (do not compare Haswell with Genoa). Said an other way, use the best of the best that exists (in algorithm and node technology). Now we can compute (2*2670)/(4*945)=1.41. One should try to at **least** get a x1.41 speedup. Not taking node volume into account we get 2670/945=2.82. Taking only the CPU and GPU power (without the node overhead), we get (4*560)/(2*360)=3.11.

CPU cost less to buy, but are less energy efficient (looking only at Flop/J), GPU are the opposite. There is a crossing point at which the two lines cross (cost as a function of Flop ALU usage). At this point, the GPU becomes better. This assume that you can actually use the GPU correctly (if you don’t burn power, this does not work), and that the machines are not replaced too often.

For Energy (J) To Solution, you just want to follow the new device’s energy consumption and get the same speedup. If your ETS is 5x10^6 J on machine A and 10x10^6 J on machine B, you’ll want the TTS on machine B to be halved (10x10^6/5x10^6=1.5).

A reasonable lower bound speedup based on the node specificities above and memory bound codes that are well tuned (both on the CPU and GPU) would be between x4 and x6 node to node. Higher speedups are possible but would probably mean an imbalance of optimization across code versions.

**Warning**

When you see someone, a paper, a presentation showing speedup of x20, x50 or more, always ask what are they comparing. This makes no sense (NO SENSE) to get a x20 speed increase in anything other than raw Flop/s when going from a Genoa node to an MI250X node! If you encounter such numbers, its likely that incomparable things are compared (comparing a single CPU core vs a H100..), or that one of the code was not properly tuned for the hardware it was running on (comparing streaming instead of cache blocking on CPU vs streaming on GPU, see the aside below).

<a id="aside-on-cache-blocking-methods"></a>

##### Aside on cache blocking methods

Caches’ primary objective is to reduce latency by 2 orders of magnitude from the +100 ns of DRAM down to +1 ns. It depends on the microarchitecture, but throughput may not increase a lot going from L3 to L2, though latency will be reduced (remember that latency is inversely proportional to throughput only when everything is serial and a CPU core proposes a lot of means to have parallelism, namely: pipelining).

What is significant regarding memory R/W throughput of CPU caches is that while the LLC (L3) is shared, the L2 and L1 are often private to a core. Thus we get a very high aggregated R/W throughput. If cores do not share cache lanes, L2 and L1 serve as throughput multiplier, function of the core count.

Now an interesting fact must be noted, since at least 2008, computing center started spreading the gospel of cache blocking. In HPC at least two kinds of cache blocking exist. The first one, often taught in courses, is related to [stencils](https://en.wikipedia.org/wiki/Iterative_Stencil_Loops) and allows the operation to reuse the values it brought to L1.

[![../_images/cacheblocking.jpg](https://dci.dci-gitlab.cines.fr/webextranet/_images/cacheblocking.jpg)](https://dci.dci-gitlab.cines.fr/webextranet/_images/cacheblocking.jpg)

On the diagram above, the cross represents the loads done for each cell. If we assume that in the diagram above, the cache has space to store/remember 18 cells, we get the feeling that the cache blocking variant is going to reuse the top and bottom values leading to a net amount of read from global memory per block ~ equal to the block size. Where as the naive streaming method (a simple `omp parallel for collapse(2)`) will always have to bring back the top and bottom values needed for the stencil into cache because they will be evicted by the values read at the end of the precedent row. The streaming variant will read x3 more from global memory.

This kind of cache blocking should always be done as it is simple to implement and provides a definite TTS advantage on both CPU and GPU. That said, on GPU the L1 and L2 caches are shared by many thread blocks/wavefronts which definitely reduces their efficiency compared to the CPU where each core has its own L1/L2.

Now a second usage of cache blocking expends on the technique shown above and goes further.

[![../_images/cacheblocking_better.jpg](https://dci.dci-gitlab.cines.fr/webextranet/_images/cacheblocking_better.jpg)](https://dci.dci-gitlab.cines.fr/webextranet/_images/cacheblocking_better.jpg)

On the diagram above, the top schematic represents the cache blocking mentioned previously. A block of data is brought into the caches, worked on, and wrote back to global memory when the thread goes to the next block it needs to process. The drawing on the bottom is a very powerful alternative consisting in bringing the block once into the cache, then applying multiple operators on it before its eviction. This second technique is implemented in different ways depending on the hardware but in all cases it takes the form of a subprocess domain decomposition in say block/patches.

On CPU, an `omp parallel` is placed at the bottom of the call stack (near `main`, this is a [common practice](https://youtu.be/_JTIgnz9taU?list=PL20S5EeApOSsT03t7oLRhx7iCDf2ETFmO&t=2158)), and further up the stack, `omp for` is used to distribute the patch processing onto the cores and each thread will process its associated patches, one at a time, applying many (often thousands) lines of code onto this patch. Patches are often small, it depends on the application, but 8x8 in 2D is common (often small enough to fit a L2 cache ~1 Mio).

On GPU, due to the device queue concept that underlies the GPU programming model, each kernel/operator will have to read all the patches once and evict them all too. There is no viable cache reuse across kernel/operator (the programming model enforces the up>work>down mechanism shown above). The alternative is to create a bigger kernel that is the fusion of smaller ones. This is called operator fusion/kernel fusion/merging/fusing. This way, you avoid at least one “down” and one “up”. That said, note that GPU caches are small (very small on AMD), and that the purpose of caches on such devices is not the same as on CPU. If you merge a vector add operator with a vector multiply operator, you can assuredly gain a lot of time but, if each operator is 400 lines of code, loading a lot of data for each patch, the gain of GPU kernel fusing them may be scarce, or lead to worse performance due to GPU core (SM/CU) resource constraints or to the often necessity to have larger patch size compared to CPU (you want all your GPU *threads* to work). Lets call this method advanced *patch* cache blocking.

**Note**

One can’t reasonably write GPU code as if writing for CPUs. On GPU there is no system call, no reasonable use of malloc, no 20k lines of code operator, no reasonable large stack allocation, severe resource constraints (registers, LDS, wavefronts/warps).

To conclude, the CPU exposes caches that naturally fit its programming model. The GPU exposes smaller caches that are trickier to use, require code modification (or heavy template usage). The advanced *patch* cache blocking that made CPU codes of the last two decades shine is not as applicable to GPU. We should compare heavily cache blocked CPU code to their streaming optimized GPU alternative. Though stencil cache blocking is still viable on both devices.

<a id="porting-process"></a>

### Porting process

In this section we explore a porting process we use at CINES. We suppose theses cases where you possess a:

- C/C++/Fortran code with some or no OpenMP CPU pragmas (say, `pragma omp parallel for`).
- C/C++ code and OpenACC offloading.
- C++ code with CUDA.

We start by presenting a typical porting process for the first two cases, that is, going from a purely CPU code (C/C++/Fortran with potentially some OpenMP loops) or going from OpenACC offloading to OpenMP offloading. We will then describe how a CUDA code can mostly be automatically translated into HIP.

<a id="from-cpu-only-or-openacc-offloading-to-openmp-offloading"></a>

#### From CPU only or OpenACC offloading to OpenMP offloading

If your code is in Fortran and uses OpenACC you may want to try compiling your code using the Cray compiler. Else, if your C or C++ code uses OpenACC, know that there is no *viable* compilers that supports it on AMD GPUs. You will have to transcribe it to OpenMP.

The following diagram shows the stages one could go through to port a code. It is not set in stone but should provide a viable framework. We will go through each stage.

[![../_images/porting_process_en.jpg](https://dci.dci-gitlab.cines.fr/webextranet/_images/porting_process_en.jpg)](https://dci.dci-gitlab.cines.fr/webextranet/_images/porting_process_en.jpg)

An example of a porting process.

<a id="phase-1-planning"></a>

##### Phase 1: Planning

The stage can be anecdotal depending on the context. If you are to ask for an HPC sites’ help, please be careful in clearly defining a set of contact and creating a proper environment for the developers. This includes, access to the code repositories (prefer Git if possible) and **proper branch and code maintenance**.

By **branch maintenance**, understand usage of a git branching model like Gitflow. Remember to frequently, say each weeks (depending on the commit throughput), merge the *develop* branch into your own branch. That is, frequently retrieve the changes of the other developers to **avoid future merge conflicts** when you will merge your changes with the develop branch.

By **code maintenance**, understand code formatting, coding paradigm, sanitizer (leak, undefined behavior, address), Continuous Integration (CI) etc. (see [Code quality](../external_documentation_and_training_resources/index.md#learn-code-quality)).

It is crucial to define the concept of **branch and code maintenance** if not already done. It is better to have one, even imperfect, than having none.

Having OpenACC offloading coexist with OpenMP offloading is not recommended (they solve the same problem). Disabling OpenMP offloading is not supported (you either use OpenMP or you don’t). For theses reasons, we recommend an admittedly stylistically unsatisfactory but practical solution: the use of conditional compilation. One would wrap every OpenMP or OpenACC offloading pragmas and API calls like so:

```C++
#if defined( ACCELERATOR_GPU_OMP )
    // OpenMP offloading related API calls or pragmas
    #pragma omp <omp_offloading_construct>
#elif defined( ACCELERATOR_GPU_ACC )
    // OpenACC offloading related API calls or pragmas
    #pragma acc <acc_offloading_construct>
#else
    // OpenMP CPU related API calls or pragmas
    #pragma omp <omp_construct>
#endif
for(std::size_t i = 0; i < N; ++i) {
    // Computation
}
```

**Note**

It is a good practice to prefix your C definitions or preprocessor definitions with the name of your code so as to not risk mixing definitions from other codes. In C++ you should also use the concept of namespace. For a preprocessor definition `ACCELERATOR_GPU_OMP` defined by the `SUPERCFD` code you could have `SUPERCFD_ACCELERATOR_GPU_OMP`.

Finally, the researcher or implementer should define the subset of the features he wishes to be ported.

<a id="phase-2-test-cases-and-porting-the-compilation"></a>

##### Phase 2: Test cases and porting the compilation

The second phase starts by making sure the software to port is able to compile on CPU (without any GPU offloading). At this point may have to you modify your makefiles, machine files, CMakeLists files etc.

In practice the user should only have to load the appropriate modules, which in the case of the porting of the compilation towards a the use of AMD GPUs could like that:

```shell-session
$ module purge
$ # A CrayPE environment version
$ module load cpe/24.07
$ # An architecture
$ module load craype-accel-amd-gfx90a craype-x86-trento
$ # A compiler to target the architecture
$ module load PrgEnv-cray
$ # Some architecture related libraries and tools
$ module load amd-mixed
```

One would then make sure his compilation script uses the `cc`, `CC` or `ftn` compiler wrappers. One would define the preprocessor definition by adding this compiler flag `-DACCELERATOR_GPU_OMP=1` (**taken from the example above !**) and would enable the OpenMP functionalities with this compiler flag `` -fopenmp` ``.

Assuming a common makefile pattern, we could summarize the a C++ compilation with:

```shell-session
$ export CXX=CC
$ export CXXFLAGS="-fopenmp -DACCELERATOR_GPU_OMP=1"
$ export LDFLAGS="-fopenmp"
```

You shall find the information regarding the compiler available for you to use in the [Programming environment](../user_support/index.md#adastra-programming-environment) section. But know that the Cray and AMD compilers are Clang/Flang LLVM based and thus share most of their flags. For C and C++ code we **strongly** recommend using at least the following flags `-Wall -Wextra -pedantic -g` (`-g` has no overhead except for the file size).

Once the compilation succeeds, one should validates that the program behaves as expected. In software engineering eden, a bunch of so called unit tests, integration tests and system tests would be run. The HPC culture is somewhat lacking on the subject and often, only system testing (in the form of regression testing) is done.

Going with the strict minimum, we recommend that the user provide multiple test cases covering the code that needs to be ported. We expect:

- multiple short test cases (say, 2), on the order of tens of seconds in time to solution;
- at least one medium case with a TTS of a few 1000s of seconds;
- and a large test case with a TTS of a few hours.

**Note**

A test case in itself is useless as it only produces data. Please always provide test cases with the reference results one should expect and tools to compare the results.

**Important**

You may strongly consider investing a few hours into developing a validation script capable of, compiling, running and comparing the result of a test case with its reference value.

Theses test cases shall now be ran on CPU using the freshly added support for the Adastra machine. You must assure yourself that the CPU test cases results match the reference.

<a id="phase-3-cpu-profiling"></a>

##### Phase 3: CPU Profiling

<a id="cray-pat-s-perftools"></a>

###### Cray-PAT’s `perftools`

We now know that the compiler we will use to exploit the offloading capabilities of OpenMP did not break the CPU code.

We can proceed to do some profiling. This profiling may not be necessary if the implementer already knows which part of the code needs porting. For the unfamiliar though, it will give a direction on where to start.

Multiple profiling tools are available on Adastra. We will limit ourselves to the Cray Performance Analysis Tool (Cray-PAT). CrayPAT allows the collection of data on the whole application. One can restrict the profiling to a selection of predefined functions to be instrumented (MPI, HIP, BLAS, user only, etc.). An overall profile of the executable provides the total time consumed by the program and its functions. Samples can also be taken from the call stack. Sampling (that is, pausing the program, reading the stack and resuming the program) is typically the least intrusive profiling method. Unfortunately, in the case of Cray-PAT, most of the time the user will have to recompile his code.

We document its use in [this document](../software_stack/tools/index.md#adastra-software-stack-tools-profiling-perftools).

<a id="using-perf"></a>

###### Using `perf`

`perf` is the performance analysis tool for Linux. It is the bread and butter of C/C++ low level profiling by sampling. We provide an example on how using this tool in [this document](../software_stack/tools/index.md#adastra-software-stack-tools-profiling-perf).

<a id="phase-4-hot-spot-porting"></a>

##### Phase 4: Hot spot porting

Now knowing on which hot spot to start we can introduce OpenMP pragmas. Remember, until now, our code is CPU only, potentially with a flavor of OpenMP CPU. The idea is to progressively port the hot spots without caring about optimized memory transfers.

First, lets introduce some General Purpose computation on GPUs (GPGPU) programming notions. A common practice amongst accelerator manufacturer is to stitch multiple compute units together. These compute units are to work on ideally independent work-items (with low to no amount of synchronization needed). A work item is made of a treatment and the data the treatment manipulates. Independent work-item does not necessarily mean different treatment and for this reason, a similar data transformation can be used on different data, this is the concept of Single Instruction Multiple Data (SIMD). AMD GPUs are made of programmable SIMD Arithmetic and Logic Units (ALU) laid out in compute units. The compute units form a grid clearly visible on the chip’s die. The treatments executed inside a workgroup may rely on extensive synchronization though, at a performance cost. Heavy synchronization is **not viable** between workgroup. From this partial definition of an AMD GPU, we can already gain a lot of programming and performance insight.

Straightaway, we would like to expose you to the terminology used to describe accelerator concepts. Their definitions will come progressively as we introduce OpenMP offloading concepts.

| OpenMP | OpenACC | AMD hardware | HIP | CUDA |
| --- | --- | --- | --- | --- |
| SIMD | **None** | **None** (ambiguous) | **None** (ambiguous) | |
| Thread | **None** | SIMD lane/work-item/thread | Thread/work-item | Thread |
| **None** | | 16 SIMD lanes | Wave | |
| **None** | | Wavefront (64 threads/SIMD lanes) | | Warp (32 threads) |
| Team | Gang | Workgroup | | Thread block |
| **None** | | Compute unit (CU) | | Streaming Multiprocessor (SM) |
| thread_limit | vector_length * num_workers | Workgroup size | | Thread block size |
| num_teams | num_gangs | Workgroup count | | Thread block count |

**Note**

OpenACC’s `vector` and `worker` are often misunderstood. In practice, for most uses, you may safely ignore `worker` and rely only the `vector` as an alias for Thread in OpenMP, HIP or CUDA terminology. Assuming a worker count defaulting to 1, the vector width represents the number of thread in a thread block.

OpenMP is very declarative in its design, it is used to describe an end result (without much care for the implementation). It does not express technical details about *the how*, but a documentation of the *the what* (expected result). One could argue that, as long as the end result is correct as per the documentation, the implementation is valid. Though sometimes, very specific behaviors are expected behind vague OpenMP constructs. As such, it is very valuable to see how an OpenMP implementation works, some details can be read on the [GCC OpenMP implementation documentation](https://gcc.gnu.org/onlinedocs/libgomp) and the source code of the [GCC](https://github.com/gcc-mirror/gcc/tree/master/libgomp) or the [LLVM](https://github.com/llvm/llvm-project/tree/main/openmp) implementation.

**Note**

OpenMP runtime API apart, the standardization comity is introducing an increasing amount of tools in the form of directive which one can use to express assumptions (i.e., `order(concurrent)`, `schedule(nonmonotonic)`, `omp loop`, `omp allocate`, `omp assume`, etc.). Remember that OpenMP is declarative, so as long as the result is correct, the means can vary a lot, you can often only hint the compiler though of course, some behavior is *so* expected that you may rely on them, but at **your own risk of depending** on a specific implementation. The more declarative your pragmas are, the more subject to the implementation’s quality you are.

OpenMP is quite elegant in its handling of accelerator architecture. By default, OpenMP manipulates the shared virtual memory environment of a machine called the *host device*. The `target` clause allows the user to specify that for a code block (*scope* or *structured block*) the execution environment is that of a machine called the *target device*. The change of environment is also called control flow transfer. During this control flow transfer, the accelerator’s memory can be manipulated, memory copies can be done between the *host device* and the *target device* at the beginning and at the end of the code block. Copies of scalars like types are automatic (even C arrays of compile time known size). All code contained in this block is executed on the *target device* (careful with function not compilable on the accelerator, i.e. `malloc`).

**Note**

**The target can be the host itself**. In this case most copies, memory mapping and other behavior you would expect if the target as a GPU device, are almost **elided**. The code shown below should work well on both GPU and CPUs, the user only needs to ask its compiler to target either a GPU or a CPU (see [Targeting an architecture](../user_support/index.md#adastra-programming-environment-targeting-architecture)). *It’s elegant, isn’t it*? The `OMP_TARGET_OFFLOAD=[MANDATORY|DISABLED|DEFAULT]` environment variable (in OpenMP 5.0) can be used to chose between the host or target device (though the host may be the target).

OpenMP introduces its notion of thread. A thread is “an execution entity with a stack and an associated static memory”. A thread has an index. The thread with index 0 is the master thread. A team is a set of threads. A *league* is a set of teams created by the `teams` clause.

All threads are part of a team. When a master thread encounters a parallelization clause, zero or more threads are *generated* from the master thread. The threads of a team can be associated to unit of work defined by a worksharing clause. Such clause also specify how to distribute these units of work on the threads of a team to provide static or load balancing capabilities. So long as a parallelization clause is not encountered we can imagine the child threads as dormant and not participating in the program execution.

A contention group is a set of threads that can synchronize. The threads of a team form a contention group, but two threads from two different teams are not in contention.

Leagues can work on CPU (typically the host machine) but we have no particular advantage in using them. On GPU on the other hand, to exploit the large amount of threads and their hardware distribution in groups (*workgroup* or *thread block* in AMD and NVIDIA terminology), OpenMP implementations with GPU support associate a team (a group in contention) with a *workgroup* and create a league of theses teams which matches the concept of *grid* on the GPUs.

Some examples may help to understand.

In this first example, we see a loop of `N` iterations. The OpenMP directive states that this loop should be executed on the *target device*. The control flow is transferred to the *target device* and a new master thread is created. This thread executes the loop.

```C
const int N = 256;
#pragma omp target
for(int i = 0; i < N; ++i) {
    // Computation
}
```

In this second example, once the control flow is transferred, the new master thread meets the `teams` clause and a league (of teams) is created. The default number of leagues (grid size) and number of threads per team (thread block size) is implementation dependent, but these parameters can be specified by the programmer. For all team, the master thread will execute the loop, there is no distribution of work, but redundancy of work.

```C
const int N = 256;
#pragma omp target
#pragma omp teams
for(int i = 0; i < N; ++i) {
    // Computation
}
```

In this third example, once the league is created, the `distribute` clause declares that the iterations of the loop must be distributed to the teams. For example, for 32 teams, each team executes 8 iterations. For each team, only the master thread executes the iterations assigned to the team. The work is distributed to all the teams but not to all the threads of a team.

```C
const int N = 256;
#pragma omp target
#pragma omp teams distribute
for(int i = 0; i < N; ++i) {
    // Computation
}
```

In this fourth example, note the presence of the `parallel` and `for` clauses. The `parallel` clause wakes up the dormant threads of a team. The `for` clause distributes the work of a team over its threads. Each team executes all the iterations of the loop. There is a redundancy of work.

```C
const int N = 256;
#pragma omp target
#pragma omp teams parallel for
for(int i = 0; i < N; ++i) {
    // Computation
}
```

In this last example, a syntactic shortcut is used to express parallelism. Note the `distribute parallel for` clause assembly. This time, the work is distributed over the teams of the league, and over the threads of a team. There is no redundancy of work.

```C
const int N = 256;
#pragma omp target
#pragma omp teams distribute parallel for
for(int i = 0; i < N; ++i) {
    // Computation
}
```

The notion of team and league allow us to exploit the multi-level parallelism commonly seen in GPGPU. There is a last (debatable on GPU) level corresponding to the use of the `simd` clause. This level is debatable because the `simd` clause does not dictate to the compiler to generate SIMD instructions but rather, that a *group of iteration* (simd chunk) can be processed by a single thread through the use of SIMD instructions without potential side effect to the program’s correctness. On CPUs, this means telling the compiler that for instance, there is no dependency between iteration. But on GPUs, a thread is already a lane of SIMD instruction, it does not mean anything (later, it could be that `for` distributes on warps and `simd` on the lanes of the warps). We will not discuss the `simd` clause further in this document.

The `#pragma omp target loop` construct tells the compiler that the iterations can be run concurrently and may be scheduled as wanted by the compiler. This requires recent OpenMP implementation, so use with caution to avoid vendor/version locking.

**Note**

One should try to concatenate the `teams` clause and `distribute parallel for` construct into the `teams distribute parallel for` construct. Else, one exposes himself to bad code generation (what is called *generic mode* instead of *SPMD (SIMT/SIMD) mode* in LLVM terminology, see Flynn’s taxonomy). Now, **that issue is fading away** with recent compiler optimization (checkout some external LLVM documents in [Compiler infrastructure](../external_documentation_and_training_resources/index.md#learn-openmp-implementation-compiler)).

As an aside, one can try to mimic the OpenCL, HIP, CUDA and other accelerator programming model using the following OpenMP pattern:

```C
const int                 N          = ...;
static constexpr unsigned blockDim_x = 256; // Left to the user to tune.
static constexpr unsigned gridDim_x  = ...; // Left to the user to tune.

#pragma omp target teams num_teams(gridDim_x) thread_limit(blockDim_x)
#pragma omp parallel
{
    const unsigned grid_dimension = ::omp_get_num_teams() * ::omp_get_num_threads();

    for(unsigned i = ::omp_get_team_num() * ::omp_get_num_threads() + ::omp_get_thread_num();
        i < N;
        i += grid_dimension) {
        // Computation
    }
}
```

In the above code, we use teams (thread blocks), and ask OpenMP to run all the threads of the teams in parallel, there is no distribution of work, we have to do it ourselves using `omp_get_[thread|team]_num()` et al.

If one makes sure that `gridDim_x * gridDim_x >= N`, the code takes an other very common CUDA like form:

```C
const int                 N          = ...;
static constexpr unsigned blockDim_x = 256; // Left to the user to tune.
static constexpr unsigned gridDim_x  = (N + (blockDim_x - 1)) / blockDim_x;

#pragma omp target teams num_teams(gridDim_x) thread_limit(blockDim_x)
#pragma omp parallel
{
    const unsigned i = ::omp_get_team_num() * ::omp_get_num_threads() + ::omp_get_thread_num();

    if(i < N) {
        // Computation
    }
}
```

**Note**

In theory, on AMD GPUs, one should use the `omp simd` clause to use more than one thread per block (or per wavefront). This should be mandatory because AMD GPUs provide weak parallel forward-progress (for more detail, see [this document](../external_documentation_and_training_resources/index.md#learn-concurrency)). The `#pragma omp simd` implies weakly parallel forward-progress which the compiler may use to vectorize the code on SIMD ALUs. The OpenMP compiler may not transform an `omp parallel` which potentially implies locks, into an `omp parallel simd` which may livelock on AMD GPUs. On NVIDIA GPUs, since Volta, the compiler should be able to transform `omp parallel` into `omp parallel simd`. For now, on AMD GPUs, compilers assume that OpenMP kernels only need weakly parallel forward-progress, so `omp simd` is optional for full code vectorization.

These two code snippets would **not behave well on CPU**, but when it comes to GPU, a very similar machine code should be produced for the OpenMP version and say, an equivalent HIP version of this code. The table below continues on drawing a parallel between OpenMP and accelerator specific languages.

| OpenMP snippet | HIP or CUDA equivalent |
| --- | --- |
| `#pragma omp allocate(scratch_space) allocator(omp_cgroup_mem_alloc)` [[1]](index.md#f1) | `__shared__` memory (LDS) on LLVM [[1]](index.md#f1) based OpenMP implementations. |
| `#pragma omp allocate(value) allocator(omp_thread_mem_alloc)` | Thread local value (typically in registers). What you expect when you define a variable. |
| `#pragma omp barrier` | `__syncthreads()` |
| `::omp_get_num_teams();` | `gridDim.x` |
| `::omp_get_team_num();` | `blockIdx.x` |
| `::omp_get_num_threads();` | `blockDim.x` |
| `::omp_get_thread_num();` | `threadIdx.x` |

Footnotes

[1]
([1](index.md#id1),[2](index.md#id2))

The use of `allocator(omp_cgroup_mem_alloc)` by LLVM to represent shared memory is **an historical accident**. It should have been `allocator(omp_pteam_mem_alloc)`. For the moment, `omp_pteam_mem_alloc` does not do anything. In the future, it is *possible* that LLVM gives `pteam` and `cgroup` a similar shared memory meaning.

Now that you understand how to offload work with OpenMP, you need to understand how to copy data between the *host device* and the *target device*. On MI250X and Trento systems like Adastra, LUMI and Frontier, you will have access to a kind of unified memory that exempt you almost entirely from doing memory copies between the two spaces. Unified memory might or might not help you but what is certain is that making use of it in 2023 will prevent you from running your code on systems not providing this capability (most systems), you code will be working on less architectures, it will be less ported (*less portable*). Thus you must learn how to do memory copies with OpenMP. If in a few years, unified memory becomes ubiquitous, the code modifications to make use of it will only consist in removing the explicit copies (**easy**).

Observe the example below without bothering about the practical justification.

```C
void DoWork(int* input, size_t size) {
    for(size_t j = 0; j < 10; ++j) {
        #pragma omp target map(tofrom: input[42:size])
        #pragma omp teams distribute parallel for
        for(size_t i = 0; i < size; ++i) {
            input[i + 42] += 1;
        }
    }
}
```

We observe the `map` clause. It is made of two part, a memory operation, `tofrom` in this case, and *memory chunk declaration*, `input[42:size]`. First the *memory chunk declaration*, it should be interpreted as an interval of memory like so `[input + 42, input + 42 + size)`. Note the `)` meaning with are dealing with half open ranges (like in C, C++ but not Fortran, [see Dijkstra’s note on that point](https://www.cs.utexas.edu/users/EWD/transcriptions/EWD08xx/EWD831.html)). It is possible to use arithmetic like so: `map(tofrom: input[something / 2:(size * 3) - 12])`. Now, the `tofrom`. It is part of a set of operation that can be associated to the map clause, here is the list:

| Operation category | Operation | Before code-block execution | After code-block execution |
| --- | --- | --- | --- |
| Memory management | `alloc` | Increase the reference counter. If the reference counter is equal to one after the increment, allocate a memory chunk on the *target device* and associate it to the host memory chunk. | Behavior of `release`. |
| Memory management | `release` | - | Decrease the reference counter. |
| Memory management | `delete` | Sets the reference count to zero. The device memory chunk is released. | - |
| Copy | `to` | Behavior of `alloc` followed by a copy of the *host device* data `to` the `alloc` ated *target device* memory chunk **if and only if the reference is equal to one**. | Behavior of `release`. |
| Copy | `from` | Behavior of `alloc`. | Retrieval of the data `from` the *target device* to the *host device* **if and only if the reference is equal to one** followed by the behavior of `release`. |
| Copy | `tofrom` | Behavior of `to`. | Behavior of `from`. |

If you have never heard of the concept of reference counting in computer science, know that it is a technique used to keep track of the usage of a resource. It starts at zero when no resource is held, is incremented when resource allocation is requested (the resource is **allocated only when the counter is incremented to one** but **not necessarily when it is equal to one**), is decremented when resource release is requested (the resource is de-allocated when the counter equals zero).

OpenMP uses this very common concept to avoid redundant copies. This will be the subject of the following document.

<a id="phase-5-superfluous-memory-transfer-removal"></a>

##### Phase 5: Superfluous memory transfer removal

At this point, all the hot spots exposed by your test cases should have been offloaded on the GPU by doing explicit copies. Your code is probably slower than initially due to the redundant copies. We will now offer a way to progressively remove the redundant copies.

Now, the example given previously is clearly inefficient in multiple ways but note that for each call of `DoWork`, 18 unnecessary copies are done. Suppose we made it so only two copies are executed, one `to`, one `from` ? OpenMP offers an elegant solution not even requiring a modification of the `DoWork` function. `DoWorkLowCopy` is a caller of `DoWork`, if you observe correctly, you will notice a new construct: `target data`. This allows us to decorrelate the memory operations from a control flow transfer.

```C
void DoWork(int* input, size_t size) {
    for(size_t j = 0; j < 10; ++j) {
        #pragma omp target map(tofrom: input[42:size])
        #pragma omp teams distribute parallel for
        for(size_t i = 0; i < size; ++i) {
            input[i + 42] += 1;
        }
    }
}

void DoWorkLowCopy(int* input, size_t size) {
    #pragma omp target data map(tofrom: input[42:size])
    DoWork(input, size);
}
```

Assuming there is no OpenMP target memory related operations on `input[42:size]` prior to the `DoWorkLowCopy` call, what happens is that before calling `DoWork`, the `to` memory operation in the `target data` pragma of `DoWorkLowCopy` allocates the data and does the copy from the host to the device. The reference counter of the `input[42:size]` memory chunk is now equal to one. `DoWork` is called and when the thread encounters the *map* clause, OpenMP executes the `to` but will not allocate nor copy any data as the reference counter is now two. Then happen the control flow transfer, that is, a GPU kernel is launched. OpenMP waits for the kernel’s completion then execute the `from`, the reference is decremented, and is now equal to one. Nothing is done. So goes the 9 other iteration on `j` inside of `DoWork`. When `DoWork` returns, the `from` in `DoWorkLowCopy`’s body is executed and the reference counter being equal to one, the copy is executed, then the decrementation induces a release of the memory chunk from the *target device*’s memory. We just elided 18 copies! One can proceed in the same way for all memory allocations, trying to minimize their number when appropriate. Sometimes, the user will benefit from copying data as needed without touching the reference count. This can be done using the `target update` construct with the `to` or `from` clauses like so:

```C
#pragma omp target update                    to( byte_array [43:size] )
#pragma omp target update if(was_modified) from( byte_array [43:size] )
```

The meaning is quite obvious. Theses pragmas are *standalone*, they obviously do not need to be attached to a code block, scope, function call etc.. Note the `if` clause which is usable in multiple construct but would be too long to present. Just note that if `was_modified` is true (`!= 0`), the memory operation is executed.

Note however:

```C
#pragma omp target data map(to: A[0:n])
{
    // Host write of A is illegal, unless "update to()" is used next.
    #pragma omp target map(tofrom: A[0:n])
    {
        A[0] = 0.0;
    }
    // Host read of A is illegal unless update from().
}
```

**Note**

There is at least one major problem with the OpenMP *paradigm*. It *strongly* implies a buffer duplication, on the *host* and *target device*. This needs to be understood and taken care of because Adastra GPU nodes possess 512 Gio of RAM while the CPU part of this kind of nodes has 256 Gio. Now, there are technical tricks to avoid this limitation such as understanding that the virtual memory abstraction does not allocate anything physical as long as you do not touch a memory page.

**Note**

Ideally, you would allocate CPU memory arrays and **never** ever manipulate them on the CPU (not even zeroing), always using offloading. In some case this is exactly what you should do, in other case such as when you want to write your results to disk, this is still doable but less practical.

<a id="phase-6-performance-tuning"></a>

##### Phase 6: Performance tuning

Refer to the [Performance tuning and monitoring](index.md#porting-optimization-performance-tuning-monitoring) document.

<a id="from-cuda-to-hip"></a>

#### From CUDA to HIP

NVIDIA is known to offer great hardware coupled with great tooling. There is a hitch though, most of it is closed source. AMD is gaining ground by providing great hardware at lower cost while open sourcing a large part of the tooling. This partially pushes the burden of development on the open source community. There are multiple key technologies that have enabled this. Here we evoke the Heterogeneous-compute Interface for Portability (HIP), a CUDA like API that aim to provide support for at least AMD and NVIDIA GPUs. Most of the significant CUDA API is available. The key differences are that the API is prefixed with `hip` instead of `cuda`.

The APIs are so similar that a *simple* text replacement program like `hipify-perl` can be used. There is an alternative, more complex to setup named `hipify-clang` which we do not describe in this document but is available [here](https://github.com/ROCm/HIPIFY).

<a id="hipify-perl"></a>

##### hipify-perl

`hipify-perl`’s notable flags are:

```
-examine          - Combines -no-output and -print-stats options
-inplace          - Backup the input file in .prehip file, modify the input file inplace
```

The first option gives you a preview of what is going to happen for instance, given the code below in a file named `test.cu`:

```C++
cudaError_t error_code = cudaFreeHost(p);
error_code = cudaStreamCreateWithFlags(&shtns->xfer_stream, cudaStreamNonBlocking);
```

When using `-examine` we obtain:

```shell-session
$ hipify-perl -examine test.cu
[HIPIFY] info: file 'test.cu' statistics:
  CONVERTED refs count: 4
  TOTAL lines of code: 4
  WARNINGS: 0
[HIPIFY] info: CONVERTED refs by names:
  cudaError_t => hipError_t: 1
  cudaFreeHost => hipHostFree: 1
  cudaStreamCreateWithFlags => hipStreamCreateWithFlags: 1
  cudaStreamNonBlocking => hipStreamNonBlocking: 1
```

When using `-inplace` we obtain change `test.cu` and obtain:

```shell-session
$ hipify-perl -inplace test.cu
$ cat test.cu
hipError_t error_code = hipHostFree(p);
error_code = hipStreamCreateWithFlags(&shtns->xfer_stream, hipStreamNonBlocking);
$ cat test.cu.prehip
cudaError_t error_code = cudaFreeHost(p);
error_code = cudaStreamCreateWithFlags(&shtns->xfer_stream, cudaStreamNonBlocking);
```

**Warning**

Preprocessor directives that check for CUDA-specific functionality must be replaced with a portable HIP version of the preprocessor directive. For example, if the source code contains a preprocessor directive that checks for the presence of the CUDA FFT, it should be replaced with a check for the HIP FFT. When compiling in the HIP environment, HIP checks the available architecture (NVIDIA or AMD) and, as a result, HIP API calls are transparently directed to cuFFT or rocFFT.

**Warning**

You might need to produce different source code depending on the architecture you are targeting (say, for wavefront details). This can be done using preprocessor definition, see: [C preprocessor definitions](../software_stack/libraries/index.md#adastra-software-stack-libraries-rocm-cpreproc). For instance, the wavefront (or warp in NVIDIA terminology) is not the same on AMD and NVIDIA GPUs. For AMD GPUs, it is 64 work-items and on NVIDIA GPUs it is 32. You can obtain the warp size at runtime via `hipGetDeviceProperties` but this is undeniably less useful than knowing it at compile time.

The resulting HIP code can be compiled using the appropriate `CC` [compiler wrapper](../software_stack/libraries/index.md#adastra-software-stack-libraries-rocm-integration).

<a id="good-old-c-preprocessor"></a>

##### Good old C preprocessor

A more versatile and embed option is to rely on the kind of header shown below. One would include it into its code and it would automatically replace CUDA names with their HIP equivalent. This is lightweight, understandable and extensible. This works only because HIP aims to copy CUDA (one could say it wants to wrap it). For many codes, this approach is enough, in fact adding hipify as a stage in a build system, even if done correctly which is rare, is verbose, has high risk of breakage and you end up with *two sources of truth*, the CUDA code and the HIP code, making it harder to maintain.

```C++
/// @brief Does a compile time string replacement of acc_<xyz> into the proper
/// HIP or CUDA symbol. This can be used as a simpler hipify tool.
///

#ifndef HIPIFIER_H
#define HIPIFIER_H

#if defined(__CUDACC__)
    #include <cuda_runtime.h>
    #include <cufft.h>

    #define SIMD_WIDTH (32)
    #define CUDA_TRAP  __trap();

    // NOTE: We load the correct CUDA headers and do not do string replacement.
    // The user writes normal CUDA code.
#elif defined(__HIPCC__)
    #include <hip/hip_runtime.h>
    #include <hip/hip_runtime_api.h>
    #include <hipfft/hipfft.h>

    #define SIMD_WIDTH (warpSize)
    #define CUDA_TRAP  __builtin_trap();

    // NOTE: We load the correct HIP  headers and do string replacement.
    // The user writes normal CUDA code and this header will replace the CUDA
    // names with the HIP equivalent.

    #define cudaDeviceProp                                          hipDeviceProp_t
    #define cudaDeviceReset                                         hipDeviceReset
    #define cudaDeviceSetCacheConfig                                hipDeviceSetCacheConfig
    #define cudaDeviceSynchronize                                   hipDeviceSynchronize
    #define cudaError_t                                             hipError_t
    #define cudaFree                                                hipFree
    #define cudaFuncCachePreferL1                                   hipFuncCachePreferL1
    #define cudaFuncCachePreferNone                                 hipFuncCachePreferNone
    #define cudaGetDeviceCount                                      hipGetDeviceCount
    #define cudaGetDevice                                           hipGetDevice
    #define cudaGetDeviceFlags                                      hipGetDeviceFlags
    #define cudaGetDeviceProperties                                 hipGetDeviceProperties
    #define cudaGetErrorString                                      hipGetErrorString
    #define cudaGetLastError                                        hipGetLastError
    #define cudaMalloc3D                                            hipMalloc3D
    #define cudaMalloc                                              hipMalloc
    #define cudaMallocManaged                                       hipMallocManaged
    #define cudaMemAdvise                                           hipMemAdvise
    #define cudaMemAdviseSetReadMostly                              hipMemAdviseSetReadMostly
    #define cudaMemAdviseUnsetReadMostly                            hipMemAdviseUnsetReadMostly
    #define cudaMemcpy                                              hipMemcpy
    #define cudaMemcpy2DAsync                                       hipMemcpy2DAsync
    #define cudaMemcpyAsync                                         hipMemcpyAsync
    #define cudaMemcpyDeviceToDevice                                hipMemcpyDeviceToDevice
    #define cudaMemcpyDeviceToHost                                  hipMemcpyDeviceToHost
    #define cudaMemcpyHostToDevice                                  hipMemcpyHostToDevice
    #define cudaMemcpyHostToHost                                    hipMemcpyHostToHost
    #define cudaMemcpyKind                                          hipMemcpyKind
    #define cudaMemcpyToSymbol                                      hipMemcpyToSymbol
    #define cudaMemGetInfo                                          hipMemGetInfo
    #define cudaMemPrefetchAsync                                    hipMemPrefetchAsync
    #define cudaMemset                                              hipMemset
    #define cudaMemsetAsync                                         hipMemsetAsync
    #define cudaSetDevice                                           hipSetDevice
    #define cudaStreamCreate                                        hipStreamCreate
    #define cudaStreamCreateWithFlags                               hipStreamCreateWithFlags
    #define cudaStreamDestroy                                       hipStreamDestroy
    #define cudaStreamSynchronize                                   hipStreamSynchronize
    #define cudaStreamNonBlocking                                   hipStreamNonBlocking
    #define cudaStream_t                                            hipStream_t
    #define cudaOccupancyMaxPotentialBlockSizeVariableSMemWithFlags hipOccupancyMaxPotentialBlockSizeVariableSMemWithFlags
    #define cudaSuccess                                             hipSuccess
    #define __syncwarp()

    #define cuDoubleComplex hipDoubleComplex
    #define cuComplex       hipComplex

    #define cuCreal                hipCreal
    #define cuCimag                hipCimag
    #define make_cuDoubleComplex   make_hipDoubleComplex
    #define cuConj                 hipConj
    #define cuCadd                 hipCadd
    #define cuCsub                 hipCsub
    #define cuCmul                 hipCmul
    #define cuCdiv                 hipCdiv
    #define cuCabs                 hipCabs
    #define make_cuComplex         make_hipComplex
    #define cuComplexDoubleToFloat hipComplexDoubleToFloat
    #define cuComplexFloatToDouble hipComplexFloatToDouble
    #define cuCfmaf                hipCfmaf
    #define cuCfma                 hipCfma
    #define cufftResult            hipfftResult
    #define cufftHandle            hipfftHandle

    #define cufftDestroy hipfftDestroy
    #define cufftPlan2d  hipfftPlan2d
    #define cufftExecD2Z hipfftExecD2Z
    #define cufftExecZ2D hipfftExecZ2D

    #define cufftExecR2C hipfftExecR2C
    #define cufftExecC2R hipfftExecC2R

    #define CUFFT_SUCCESS HIPFFT_SUCCESS
    #define CUFFT_D2Z     HIPFFT_D2Z
    #define CUFFT_Z2D     HIPFFT_Z2D

    #define CUFFT_R2C     HIPFFT_R2C
    #define CUFFT_C2R     HIPFFT_C2R
#else
    #error "Unknown compiler."
#endif
#endif
```

<a id="performance-tuning-and-monitoring"></a>

<a id="porting-optimization-performance-tuning-monitoring"></a>

## Performance tuning and monitoring

Performance tuning is one of the very dark side of computer science where you are to rely on corner cases more than general truths. In this sub-section we present the basic features available to diagnostic a performance problem. We offer guidelines but do know that in practice, the golden word is it **depends**. That being said, there are some safe bets for performance improvement such as maximizing main memory manipulation efficiency.

*Surely there must be a less primitive way of making big changes in the store than by pushing vast numbers of words back and forth through the von Neumann bottleneck. […] programming is basically planning and detailing the enormous traffic of words through the von Neumann bottleneck, and much of that traffic concerns not significant data itself.* John Backus in his 1977 ACM Turing Award lecture.

<a id="proper-binding-why-and-how"></a>

<a id="porting-optimization-performance-tuning-monitoring-proper-binding-why-how"></a>

### Proper binding, why and how

First and foremost, we provide programs to test the if the binding is correct.

**Warning**

**You are strongly recommended to test your SLURM scripts using theses tool before running in production.**

- For the GENOA partition: A simple MPI+OpenMP based program ([hello_cpu_binding](https://dci-gitlab.cines.fr/external/adastra-examples/-/tree/main/hello_cpu_binding)) can be used to clarify the mappings.
- For the MI250 partition: An MPI+OpenMP+HIP based program ([hello_gpu_binding](https://dci-gitlab.cines.fr/external/adastra-examples/-/tree/main/hello_gpu_binding)) can be used to clarify the GPU mappings.

Then, we crudely define some often confusing terms:

| Term equivalence | Description |
| --- | --- |
| Socket | A place where the a CPU’s chips resides. Potentially comes with its own memory buses/channels, power lanes, PCIe lanes, etc.. It is possible to have more than one on a given motherboard. |
| CPU | A set of cores (potentially of different kinds) arranged in one or multiple chips, see AMD’s CoreCompleX (CCX). There is typically one per socket. |
| Core | A physical processing unit (PU). If SMT is disabled, **or not used**, a core is equivalent to a thread. There is generally multiple cores per CPU. |
| Simultaneous MultiThreading (SMT) thread, hyperthread, logical thread, hardware thread, thread | The abstraction of a compute resource executing *serialized* instructions (in appearance). If SMT is enabled, the core’s physical resources can be used by two or more logical threads, through its super-scalar (pipelined) capabilities. SMT cant be een as a way to better utilize the compute resources or to hide memory latency. |
| Software thread, kernel thread, native thread, thread | Yet an other abstraction above the core. Allows the operation system to [switch context](https://en.wikipedia.org/wiki/Context_switch). Not to mix with user land threads such as Microsoft’s [fibers](https://learn.microsoft.com/en-us/windows/win32/procthread/fibers). |

**Note**

Historically, the CPUs where single core and cores where called CPU. We prefer to clearly split the two concepts.

The *cost* of accessing shared resources often depends on *who* is accessing. This uneven *cost* is called Non Uniform *Memory* Access (NUMA) though the behavior does not limit itself to *Memory*. *Accessors* (say, processors) experiencing similar NUMA *cost* behaviors are grouped to form a NUMA node. The NUMA domain of a NUMA node represents the resources the NUMA node can access at a *cheaper cost* than other NUMA nodes. This introduces the notion of NUMA distance which is a metric describing the *cost* of accessing a domain from a node. In practice, NUMA distances are mostly referred to when talking about RAM access latency between cores or sockets. In this case, this gives a symmetric NxN matrix where N is the NUMA node count. The distances can be obtained with commands such as `numactl -H` or the [core-to-core latency](https://github.com/nviennot/core-to-core-latency).

For instance on an Adastra compute node we have:

```shell-session
$ numactl -H
available: 4 nodes (0-3)
node 0 cpus: 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79
node 0 size: 63273 MB
node 0 free: 59481 MB
node 1 cpus: 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95
node 1 size: 64462 MB
node 1 free: 61615 MB
node 2 cpus: 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111
node 2 size: 64503 MB
node 2 free: 61405 MB
node 3 cpus: 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127
node 3 size: 64487 MB
node 3 free: 61595 MB
node distances:
node   0   1   2   3
  0:  10  12  12  12
  1:  12  10  12  12
  2:  12  12  10  12
  3:  12  12  12  10
```

**Note**

Be careful with `numactl` and its usage of the CPU or physical CPU term. Here, CPU means hardware thread!

```shell-session
$ lscpu
Architecture:        x86_64
CPU op-mode(s):      32-bit, 64-bit
Byte Order:          Little Endian
CPU(s):              128
On-line CPU(s) list: 0-127
Thread(s) per core:  2
Core(s) per socket:  64
Socket(s):           1
NUMA node(s):        4
Vendor ID:           AuthenticAMD
CPU family:          25
Model:               48
Model name:          AMD EPYC 7A53 64-Core Processor
Stepping:            1
CPU MHz:             2000.000
CPU max MHz:         3541.0149
CPU min MHz:         1500.0000
BogoMIPS:            3992.66
Virtualization:      AMD-V
L1d cache:           32K
L1i cache:           32K
L2 cache:            512K
L3 cache:            32768K
NUMA node0 CPU(s):   0-15,64-79
NUMA node1 CPU(s):   16-31,80-95
NUMA node2 CPU(s):   32-47,96-111
NUMA node3 CPU(s):   48-63,112-127
Flags:               fpu vme de pse tsc msr pae mce [... redacted for brevity]
```

Note that SMT is enabled as shown by the line `Thread(s) per core:  2`. This needs to be taken into account when binding and choosing the number of thread per task and task per node for a given job.

Trans-NUMA memory transactions should be avoided. In practice, trans-cache memory transactions should also to be mitigated. That poses a new question: How to control or avoid accidental trans-NUMA memory access ? This leads us to the concept of memory placement policy which requires some basic knowledge on virtual memory. One key point to understand is that until memory is *touched* (written to or read from), no physical memory may actually be allocated. When a thread *touches* a memory page (a chunk of virtual memory), then the kernel will reserve some RAM for the page.

Their are multiple memory placement policy but the one you will see in use on machines such as Adastra is called *first touch*. The first touch policy gives predictable behavior by saying that when a thread touches a page until now never touched, then the kernel will allocate physical memory from the NUMA domain the touching thread is from (if enough memory is available).

To take advantage of the first touch policy, the programmer should make sure that the threads that initialize the memory or touches it for the first time, belong to the same NUMA domain of the threads that will do the computation. There is a problem tough, because the underlying hardware threads of your process’ threads can change during the program’s execution and potentially, you could end up running on the core of a different NUMA node at the operating system’s will (we could say that the process’ threads *move*). What we need is to bind or define the **affinity** of your process towards a set of hardware threads all close to the same hardware resource say a NUMA node or a Last Level Cache (LLC).

The NUMA behavior is also observable on Adastra’s accelerated nodes, where, due to the physical layout of the hardware, the *cost* of accessing GPU memory or even, to access a network interface not always the same.

**Note**

Binding software threads to hardware threads is more important on AMD CPUs than on Intel CPUs (that does not mean you shouldn’t do it on Intel CPUs). This can be observed with the `core-to-core latency` tool and by being aware of AMD’s design by stitching Core CompleX (CCX) arranged in Core Chiplet Die (CCD) for CPUs and stitching Graphic Complex Die (GCD) for GPUs.

**Note**

A good binding on MI300A nodes is very important if you use USM. Else, you expose yourself to performance regression on the order of x20 to x30 (because there is no page migration).

**Note**

Building a software to be NUMA aware is complex and intrusive in the algorithm. A good alternative is to use a mix of OpenMP and a message passing library say MPI (message passing which you are going to need anyway if you want to use multiple nodes). Then, being NUMA aware is *as easy as* running a process per NUMA, L3 cache, etc. and exchanging between processes using MPI.

**Warning**

The binding makes the most sense only if whole nodes are used!

After the *why* comes the *how*. The problem sorts of limits itself to defining *place partitions* that is, groups of hardware threads and assigning processes to these places. Multiple tools are available:

> - `numactl`
> - `hw-bind`
> - `taskset`
> - OpenMP
> - SLURM
> - MPI implementation (potentially)

To illustrate the binding tools and concepts, we will work with an example job supposing 8 tasks per node and 8 threads per task on an **Adastra accelerated node**. Each task gets its own L3 cache and GPU. We will assume SMT is not wanted. The NUMA domains we will use are given in the [Adastra accelerated (MI250X) nodes](../architecture/index.md#architecture-adastra-accelerated-nodes) subsections and summarized below:

```
# Node local rank 0 gets the GCD 0, is bound the cores [48-55] of NUMA domain 3
# Node local rank 1 gets the GCD 1, is bound the cores [56-63] of NUMA domain 3
# Node local rank 2 gets the GCD 2, is bound the cores [16-23] of NUMA domain 1
# Node local rank 3 gets the GCD 3, is bound the cores [24-31] of NUMA domain 1
# Node local rank 4 gets the GCD 4, is bound the cores [ 0- 7] of NUMA domain 0
# Node local rank 5 gets the GCD 5, is bound the cores [ 8-15] of NUMA domain 0
# Node local rank 6 gets the GCD 6, is bound the cores [32-39] of NUMA domain 2
# Node local rank 7 gets the GCD 7, is bound the cores [40-47] of NUMA domain 2
```

**Warning**

On the MI250 partition, the binding of a GPU to a set of core is most significant if the user does a lot for CPU to GPU copies.

**Note**

Although we present binding on an accelerated node, the concepts are similar on a scalar node (and simpler too).

OpenMP, `numactl` or `taskset` have a common major issue for our use case; they are not *task aware*. We are going to have multiple tasks per node and we do not want these processes to use the same hardware resources. If all the process had the same binding, they would use the same hardware threads leading to an oversubscription of the hardware threads by process threads. This issue can be circumvented using a small script.

With OpenMP, you can specify a set of place partitions explicitly, by listing the hardware threads in each place partition or, implicitly, by evoking an abstract name (`threads`, `cores`, etc.) in the `${OMP_PLACES}` environment variable. In practice, using only OpenMP places in a multi process software tends to be clunky and not general enough to work great on a wide range of machine.

We will show a way of hardcoding the binding using `numactl`. Hardcoding is often a bad practice, but in this case, remember that we are tuning to a specific architecture: the Adastra nodes. Below is an example script giving you near total control of your GPUs and cores and how to bind them to a process.

```shell
#!/bin/bash

set -eu

LOCAL_RANK_INDEX="${SLURM_LOCALID}"

function Adastra_MI300_4TasksWith24ThreadsAnd1GPU() {
    AFFINITY_NUMACTL=('0-23' '24-47' '48-71' '72-95')
    AFFINITY_GPU=('0' '1' '2' '3')
}

function Adastra_MI250_8TasksWith8ThreadsAnd1GPU() {
    AFFINITY_NUMACTL=('48-55' '56-63' '16-23' '24-31' '0-7' '8-15' '32-39' '40-47')
    AFFINITY_GPU=('0' '1' '2' '3' '4' '5' '6' '7')
}

function Adastra_GENOA_24TasksWith8Threads() {
    AFFINITY_NUMACTL=('0-7' '8-15' '16-23' '24-31' '32-39' '40-47' '48-55' '56-63' '64-71' '72-79' '80-87' '88-95' '96-103' '104-111' '112-119' '120-127' '128-135' '136-143' '144-151' '152-159' '160-167' '168-175' '176-183' '184-191')
}

function Adastra_GENOA_48TasksWith4Threads() {
    AFFINITY_NUMACTL=('0-3' '4-7' '8-11' '12-15' '16-19' '20-23' '24-27' '28-31' '32-35' '36-39' '40-43' '44-47' '48-51' '52-55' '56-59' '60-63' '64-67' '68-71' '72-75' '76-79' '80-83' '84-87' '88-91' '92-95' '96-99' '100-103' '104-107' '108-111' '112-115' '116-119' '120-123' '124-127' '128-131' '132-135' '136-139' '140-143' '144-147' '148-151' '152-155' '156-159' '160-163' '164-167' '168-171' '172-175' '176-179' '180-183' '184-187' '188-191')
}

export MPICH_OFI_NIC_POLICY="NUMA"
export OMP_PROC_BIND="TRUE"

Adastra_MI250_8TasksWith8ThreadsAnd1GPU
# Adastra_GENOA_24TasksWith8Threads
# Adastra_GENOA_48TasksWith4Threads

CPU_SET="${AFFINITY_NUMACTL[$((${LOCAL_RANK_INDEX} % ${#AFFINITY_NUMACTL[@]}))]}"
if [ ! -z ${AFFINITY_GPU+x} ]; then
    GPU_SET="${AFFINITY_GPU[$((${LOCAL_RANK_INDEX} % ${#AFFINITY_GPU[@]}))]}"
    export ROCR_VISIBLE_DEVICES="${GPU_SET}"
fi
exec numactl --localalloc --physcpubind="${CPU_SET}" -- "${@}"
```

**Note**

A more detailed script is given [here](detailed_binding_script.md#porting-optimization-detailed-binding-script). Simpler but **more volatile** SLURM based bindings are presented next.

A few notes:
:   - We define a configuration depending on the hardware, here for the accelerated nodes, it is recommended to use 8 cores per task, each task with its own GCD.
    - `${ROCR_VISIBLE_DEVICES}` or `${HIP_VISIBLE_DEVICES}` restrict the GPU visibility of the ROCm software stack (your software will see a subset of the node’s GPUs). `${ROCR_VISIBLE_DEVICES}` *operates* at the [Heterogenous System Architecture (HSA)](https://hsafoundation.com/standards/) interface level while `${HIP_VISIBLE_DEVICES}` *operates* at the HIP runtime level. The HSA is the interface used to drive the GPUs through the kernel’s AMD GPU driver. The AMD driver is called [ROCk](https://github.com/RadeonOpenCompute/ROCK-Kernel-Driver) while the AMD GPU HSA implementation is called [ROCt](https://github.com/RadeonOpenCompute/ROCT-Thunk-Interface). Both environment variables should work though, to minimize resource allocation, it **is generally more efficient to mask the GPUs that you do not want to use at the lowest level**.
    - In case you deem SMT (hyperthreading) worth, see [this script](detailed_binding_script.md#porting-optimization-detailed-binding-script).

Storing the script on disk as `adastra_acc_binding.sh`, using the script above is as simple as doing:

```shell
1#!/bin/bash
2#SBATCH --account=<account_to_charge>
3#SBATCH --job-name="test_affinity"
4#SBATCH --constraint=MI250
5#SBATCH --nodes=1
6#SBATCH --exclusive
7#SBATCH --time=1:00:00
8
9srun --ntasks-per-node=8 --cpu-bind=none --mem-bind=none -- ./adastra_acc_binding.sh <executable> <arguments>
```

| Line | Description |
| --- | --- |
| 1 | Shell interpreter line. |
| 2 | GENCI/DARI project to charge. More on that in [Resource consumption and charging (accounting)](../user_support/index.md#adastra-running-jobs-resource-charging). |
| 3 | Job name. |
| 4 | Type of Adastra node requested (here, the GPU MI250X partition). |
| 5 | Number of compute nodes requested (here, 1). |
| 6 | Make sure we allocate whole nodes, our binding requires it (actually it’s not necessary because we already request all the resources of a node). |
| 10 | Implicitly ask to use all of the node allocated. Then we distribute the work on 8 tasks per node. We disable the SLURM implicit binding and use the binding script. |

You can validate the binding using the tools given at the start of this section.

Now that you have read these lines we must confess that most of these issues can also be solved with SLURM but this solution may be less portable, less flexible, less obvious and more subject to subtle bug or breaking. It is based on `srun`’s `--gpu-bind=closest`.

**Note**

Until further notice, it is not advisable to use `gpu-bind`. Please use a binding script such as the one given above, and customize the functionalities to your need.

**Warning**

Do **not** use `--cpus-per-tasks=<N>` when using the aforementioned binding script. Else you may encounter the following `numactl` error message: `libnuma: Warning: cpu argument XXX is out of range`.

**Warning**

`--gpu-bind=closest` needs a GPU and CPU count per task to be specified (`--cpus-per-task=8 --gpus-per-task=1`). Also the CPU count (which actually is the hyperthread count) should divide the node thread count by the number of GPUs. On MI250X nodes, we have 64 cores, so eah rank should get 8 cores. If hyperthreading is used, then 16 threads per rank.

```shell
1#!/bin/bash
2#SBATCH --account=<account_to_charge>
3#SBATCH --job-name="test_affinity"
4#SBATCH --constraint=MI250
5#SBATCH --nodes=1
6#SBATCH --exclusive
7#SBATCH --time=1:00:00
8
9srun --ntasks-per-node=8 --cpus-per-task=8 --threads-per-core=1 --gpus-per-task=1 --gpu-bind=closest -- <executable> <arguments>
```

The **only** difference with the previous `sbatch` configuration is that we replaced the `--cpu-bind=none --mem-bind=none` with `--cpus-per-task=8 --threads-per-core=1 --gpus-per-task=1 --gpu-bind=closest`. This will give you the following binding:

```
# Node local rank 0 gets the GCD 4, is bound the cores [ 0- 7] of NUMA domain 0
# Node local rank 1 gets the GCD 5, is bound the cores [ 8-15] of NUMA domain 0
# Node local rank 2 gets the GCD 2, is bound the cores [16-23] of NUMA domain 1
# Node local rank 3 gets the GCD 3, is bound the cores [32-39] of NUMA domain 1
# Node local rank 4 gets the GCD 6, is bound the cores [24-31] of NUMA domain 2
# Node local rank 5 gets the GCD 7, is bound the cores [48-55] of NUMA domain 2
# Node local rank 6 gets the GCD 0, is bound the cores [40-47] of NUMA domain 3
# Node local rank 7 gets the GCD 1, is bound the cores [56-63] of NUMA domain 3
```

This binding should provide **similar performance** than the one present earlier, except that the GPUs index an MPI rank will see is not the same as his `${SLURM_LOCALID}`. If you seek this behavior, assuming you want one 1 core per task, the following `sbatch` configuration needs to be used (or you can simply rely on the binding script above):

<a id="proper-pinning-why-and-how"></a>

<a id="porting-optimization-performance-tuning-monitoring-proper-pinning-why-how"></a>

### Proper pinning, why and how

Once each rank uses a correct set of core you should already getting a good portion of what you hardware can give you (all other things being equal). Indeed, the threads spawned by a process are ensured to be on the correct NUMA/L3/meaningful hardware partition thanks to the affinity/binding masks (CPU mask). We have an affinity of our process’s software threads toward a **set** of hardware thread.

The next step would be to ensure that the software threads spawned by a process are *pinned* to an hardware thread and do not move inside the set of cores associated to the process. If not done, one exposes himself to issues exacerbated if you use a large amount of software thread per rank (say ~> 16) that crosses hardware boundary (say L2/L3). When a software thread moves from core to core, context switching cost and cache misses are small penalties payed that if repeated, can be detrimental to performance.

**Note**

Software thread pinning a finer level of affinity control. This can entirely supersede binding cores to rank but then becomes less portable.

OpenMP offers the `OMP_PLACES` and `OMP_PROC_BIND` environment variable (ICV) to control this pinning behavior. Here is an example on Adastra’s Genoa CPUs with the GCC OpenMP implementation. The text below represents the place partitions for multiple OpenMP configurations, in every case, we assume SMT/hyperthreading is enabled. If SMT was disabled, the places in the range [192, 384) would not exist.

```
Assuming the following OMP_PLACES values:
  `THREADS`: '{0},{192},{1},{193},{2},{194},{3},{195},{4},{196},{5},{197},{6},{198},{7},{199},{8},{200},{9},{201},{10},{202},{11},{203},{12},{204},{13},{205},{14},{206},{15},{207},{16},{208},{17},{209},{18},{210},{19},{211},{20},{212},{21},{213},{22},{214},{23},{215},{24},{216},{25},{217},{26},{218},{27},{219},{28},{220},{29},{221},{30},{222},{31},{223},{32},{224},{33},{225},{34},{226},{35},{227},{36},{228},{37},{229},{38},{230},{39},{231},{40},{232},{41},{233},{42},{234},{43},{235},{44},{236},{45},{237},{46},{238},{47},{239},{48},{240},{49},{241},{50},{242},{51},{243},{52},{244},{53},{245},{54},{246},{55},{247},{56},{248},{57},{249},{58},{250},{59},{251},{60},{252},{61},{253},{62},{254},{63},{255},{64},{256},{65},{257},{66},{258},{67},{259},{68},{260},{69},{261},{70},{262},{71},{263},{72},{264},{73},{265},{74},{266},{75},{267},{76},{268},{77},{269},{78},{270},{79},{271},{80},{272},{81},{273},{82},{274},{83},{275},{84},{276},{85},{277},{86},{278},{87},{279},{88},{280},{89},{281},{90},{282},{91},{283},{92},{284},{93},{285},{94},{286},{95},{287},{96},{288},{97},{289},{98},{290},{99},{291},{100},{292},{101},{293},{102},{294},{103},{295},{104},{296},{105},{297},{106},{298},{107},{299},{108},{300},{109},{301},{110},{302},{111},{303},{112},{304},{113},{305},{114},{306},{115},{307},{116},{308},{117},{309},{118},{310},{119},{311},{120},{312},{121},{313},{122},{314},{123},{315},{124},{316},{125},{317},{126},{318},{127},{319},{128},{320},{129},{321},{130},{322},{131},{323},{132},{324},{133},{325},{134},{326},{135},{327},{136},{328},{137},{329},{138},{330},{139},{331},{140},{332},{141},{333},{142},{334},{143},{335},{144},{336},{145},{337},{146},{338},{147},{339},{148},{340},{149},{341},{150},{342},{151},{343},{152},{344},{153},{345},{154},{346},{155},{347},{156},{348},{157},{349},{158},{350},{159},{351},{160},{352},{161},{353},{162},{354},{163},{355},{164},{356},{165},{357},{166},{358},{167},{359},{168},{360},{169},{361},{170},{362},{171},{363},{172},{364},{173},{365},{174},{366},{175},{367},{176},{368},{177},{369},{178},{370},{179},{371},{180},{372},{181},{373},{182},{374},{183},{375},{184},{376},{185},{377},{186},{378},{187},{379},{188},{380},{189},{381},{190},{382},{191},{383}'
  `CORES`:   '{0,192},{1,193},{2,194},{3,195},{4,196},{5,197},{6,198},{7,199},{8,200},{9,201},{10,202},{11,203},{12,204},{13,205},{14,206},{15,207},{16,208},{17,209},{18,210},{19,211},{20,212},{21,213},{22,214},{23,215},{24,216},{25,217},{26,218},{27,219},{28,220},{29,221},{30,222},{31,223},{32,224},{33,225},{34,226},{35,227},{36,228},{37,229},{38,230},{39,231},{40,232},{41,233},{42,234},{43,235},{44,236},{45,237},{46,238},{47,239},{48,240},{49,241},{50,242},{51,243},{52,244},{53,245},{54,246},{55,247},{56,248},{57,249},{58,250},{59,251},{60,252},{61,253},{62,254},{63,255},{64,256},{65,257},{66,258},{67,259},{68,260},{69,261},{70,262},{71,263},{72,264},{73,265},{74,266},{75,267},{76,268},{77,269},{78,270},{79,271},{80,272},{81,273},{82,274},{83,275},{84,276},{85,277},{86,278},{87,279},{88,280},{89,281},{90,282},{91,283},{92,284},{93,285},{94,286},{95,287},{96,288},{97,289},{98,290},{99,291},{100,292},{101,293},{102,294},{103,295},{104,296},{105,297},{106,298},{107,299},{108,300},{109,301},{110,302},{111,303},{112,304},{113,305},{114,306},{115,307},{116,308},{117,309},{118,310},{119,311},{120,312},{121,313},{122,314},{123,315},{124,316},{125,317},{126,318},{127,319},{128,320},{129,321},{130,322},{131,323},{132,324},{133,325},{134,326},{135,327},{136,328},{137,329},{138,330},{139,331},{140,332},{141,333},{142,334},{143,335},{144,336},{145,337},{146,338},{147,339},{148,340},{149,341},{150,342},{151,343},{152,344},{153,345},{154,346},{155,347},{156,348},{157,349},{158,350},{159,351},{160,352},{161,353},{162,354},{163,355},{164,356},{165,357},{166,358},{167,359},{168,360},{169,361},{170,362},{171,363},{172,364},{173,365},{174,366},{175,367},{176,368},{177,369},{178,370},{179,371},{180,372},{181,373},{182,374},{183,375},{184,376},{185,377},{186,378},{187,379},{188,380},{189,381},{190,382},{191,383}'
  `SOCKET`:  '{0:96,192:96},{96:96,288:96}'

OMP_PROC_BIND would associate the thread to partitions like so:
  `CLOSE`:  for each thread, allocate a place in a partition, trying to minimize the largest  distance between picked partitions.
      THREADS: t0 -> {0},           t1 -> {192},         t2 -> {1},             t3 -> {193} ...
      CORES:   t0 -> {0,192},       t1 -> {1,193},       t2  -> {2,194},        t3  -> {3,195} ...
      SOCKET:  t0 -> {0:96,192:96}, t1 -> {0:96,192:96}, t22 -> {96:96,288:96}, t23 -> {96:96,288:96} ...
  `SPREAD`: for each thread, allocate a place in a partition, trying to maximize the smallest distance between picked partitions.
      With OMP_NUM_THREADS=24 & modulo partition count.
      THREADS: t0 -> {0},           t1 -> {8},           t2  -> {16},           t3  -> {24} ...
      CORES:   t0 -> {0,192},       t1 -> {8,200},       t2  -> {16,208},       t3  -> {24,216} ...
      SOCKET:  t0 -> {0:96,192:96}, t1 -> {0:96,192:96}, t22 -> {96:96,288:96}, t23 -> {96:96,288:96} ...
```

What the above *slab* of text shows us is that depending on the chosen `OMP_PLACES`, different place partitions are created. The `threads` setting define a place per partition, the `cores` settings gives us a partition per core with one place for each hyperthread. Finally, the `sockets` gives us two partition, one per socket, with each partition containing as many thread (SMT included) as the cores of a socket offers.

If you use `cores` or `sockets` you give the OpenMP thread a chance to *move*. We **do not** want that. This leaves `threads` as the only valid choice.

We should now choose the `OMP_PROC_BIND` value. `close` picks one partition after the other while `spread`, knowing the number of thread the user asked for, try to maximize the smallest distance between the picked partitions.

Generally, whether your code is memory bound or not, you will benefit from using all the cores of the hardware (assuming you can scale!). Then, the recommended settings are:

```shell
export OMP_PROC_BIND=CLOSE
export OMP_PLACES=THREADS
```

This pinning will automatically adapt to the presence of hyperthreading if enabled or disabled. Yo can use the `--threads-per-core` SLURM option to control hyperthreading.

An other pinning worth investigating (assuming you have less threads than the number of core the node offers) is this one:

```shell
export OMP_PROC_BIND=SPREAD
export OMP_PLACES=THREADS
```

**Note**

If you use a binding script such as [this one](detailed_binding_script.md#porting-optimization-detailed-binding-script), you do not need these, except maybe `OMP_DISPLAY_AFFINITY`. Indeed, it’ll set `OMP_PROC_BIND=true` which basically, pin the software thread so they do not move. Which software thread ends up on which HW thread is under specified, but generally, it does not matter as the implementation does the *correct thing* and we already restricted the process’ affinity to a set of close cores.

<a id="scalar-cpu-vs-vectorial-gpgpu"></a>

### Scalar (CPU) vs vectorial (GPGPU)

Some people have expressed concern about not having a single “perfect” kernel. But note that in general you can’t write code in Fortran that will run at optimum speed on both vector and scalar/Cache machines without picking different code for the different architectures.

On **vector machines** (GPUs), you generally want to **stream** and maximize the memory operation throughput. On **scalar machines** (GENOA), enabled with large, multi tiered caches, you may want to do the same, but the approach you need to take is different, streaming wont get you far and instead, you need to use **blocked/tiled** algorithms, with blocks fitting inside the cache.

If you want the most portable code, **streaming kernels** are the way to go. If you want maximal performance, you will have to discriminate architectures.

<a id="gpu-specific"></a>

### GPU specific

<a id="monitoring-the-gpus"></a>

#### Monitoring the GPUs

One could use a mix of [htop](../software_stack/tools/index.md#adastra-software-stack-tools-monitoring-htop) and [rocmsmi](../software_stack/tools/index.md#adastra-software-stack-tools-monitoring-rocmsmi).

<a id="gpu-profiling"></a>

#### GPU profiling

One could reuse Cray’s `perftools` but we prefer describing an other tool dubbed `rocprof`. Check [this document](../software_stack/tools/index.md#adastra-software-stack-tools-profiling-rocprof) for more details.

<a id="guidelines"></a>

<a id="porting-optimization-performance-tuning-monitoring-gpu-specific-guidelines"></a>

#### Guidelines

Porting to a new, significantly different architecture might be long if you haven’t planned for it (on the order of months). That being said, if the tools you use allow it, say you use C++, you can rely on abstraction layer that can soothe the painful work. Always remember to break apart the data and its treatment (viewed as kernel/operators on the data) and use the Structure Of Array (SOA) or Array Of Vectorized Struct (AOVS) layouts. This will allow you to change at will the way your data is allocated and how it is manipulated giving you great flexibility. You may also find the [Algorithm and generic programming](../external_documentation_and_training_resources/index.md#learn-generic-programming) document interesting if you lack generic programming and algorithmic knowledge.

Now we present some guidelines which could help deduce a performance issue.

- **The thread concept is an illusion** - What exist, underlying AMD and past NVIDIA devices, is SIMD ALUs and SIMD lanes treated as threads. On NVIDIA Volta’s independent thread scheduling, SIMD is an *optimization* (PC on each lane, synchronization points and a beefier scheduler). Vector processor, GPUs, get their performance from SIMD.
- **Contiguous loads** - SIMD ALUs can do efficient, contiguous memory accesses, also called coalesced accesses (not specific to GPU, CPU also benefit fro such loads).
- **Cache discrepancy with NVIDIA GPUs** - While MI250X cards offer very large HBM throughput and a low amount of cache with large throughput, NVIDIA cards offer large amount of cache (> 40 Mio). Kernel doing lots of random access operations may find AMD GPU less performant. On CDNA3, kernels able to use caches can get crazy L1 and L2 throughput.
- **NUMA bindings** - MPI task, CPU core and GPUs need to be appropriately mapped to each others to reduce inter-ship communication. See the [Proper binding, why and how](index.md#porting-optimization-performance-tuning-monitoring-proper-binding-why-how) paragraph.
- **Beware of big kernels** - It is often seen that scientific code developers produce very long function that tend to be multipurpose. Try to split these functions.
- **Register spilling** - When the compiler can not afford to allocate more register for a given thread, the compiler will choose to dump a register’s content to the stack. Vaguely speaking, on GPU there is no *stack memory*, only registers, the stack is *mapped on registers*. Non inlined function calls for that matter, are not efficient. On AMD GPUs, a memory address space called *scratch* space is used to dump the data not fitting in the registers. This *scratch* space is part of the global memory and quite slow although it may fit in the cache. Try to reduce the usage of what would live on the stack, most of the time, static arrays are costly. Try to bring variable usage and definition close together. Spilling can be controlled with the `__launch_bounds__` compiler intrinsic.
- **Atomic operations** - Avoid global memory atomic operations (if you can). Be careful with LDS atomic operations. Atomic addition operations have hardware support on recent GPUs but it is not always used. See [CDNA1 & CDNA2 Atomics](index.md#porting-optimization-performance-tuning-monitoring-gpu-specific-cdna-atomics).
- **Instruction Level Parallelism (ILP)** - ILP takes at least two forms on GPU: wavefront scheduling (also called Thread Level Parallelism (TLP)), and instruction pipelining (but note that GPUs do not have ROB/OoO execution). Wavefront scheduling is linked to occupancy and is often glorified as **THE** way to improve kernel performance by hiding memory latencies. In practices, if your kernel can reuse its reserved resources (register, LDS, etc.) to process multiple inputs/outputs, to amortize setup and tear-down costs, it can achieve [`better performance at lower occupancy`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/67e2c082922ce6873166986cdad4ce70/perf_at_low_occupancy.pdf). The ILP concept of not stalling the pipeline due to dependency chains is similar to the one we know on CPUs and depends strongly on the instruction latency and throughput which depends on the microarchitecture. So if you have a kernel that has enough ILP and is bandwidth bound, you may want to experiment with lower occupancy.
- **Thread divergence** - AMD GPUs are more susceptible to thread divergence due to having 64 thread per wavefront/warp compared to 32 for NVIDIA. One could observe performance losses if threads take different execution paths.
- **Non coherent reads/nontemporal** (`__ldg`, `__builtin_nontemporal_store/load`) - Try to help the compiler generate better load/write instructions by specifying your buffer as [restricted](https://web.archive.org/web/20230107204001/https://cellperformance.beyond3d.com/articles/2006/05/demystifying-the-restrict-keyword.html). (On CDNA2, these loads have no special effects.)
- **Prefer constant to dynamic**, the GPU operations being executed under constrained resources (for instance, no Out of Order (OoO) execution); letting the compiler precompute and reorder instructions can produce large benefits (say, reducing *scoreboarding stalls*). C++’s template can definitely help you there.
- **Don’t forget about the Local Data Share (LDS) (shared memory)** - If you need caching, do not expect the GPU to do it for you, even if it somewhat succeed you are probably loosing on performance versus using the LDS. Also, as the roofline model presents, using faster memory allows you to reduce the operation intensity to reach peak Op/s.
- **Avoid LDS bank conflicts** - Optimal shared memory read and write patterns are non trivial both on AMD and NVIDIA devices. Knowing that the CDNA2 has 32 LDS banks per CU and that a bank holds values of 4 bytes and assuming you have an array like `__shared__ double scratch_pad[16][16];` and the threads all access it like so (or similarly) `scratch_pad[threadIdx.x][0];scratch_pad[threadIdx.x][1];...;scratch_pad[threadIdx.x][15];`, you will get poor performance (x16 slowdown maybe). You can easily fix the issue by adding a padding value like so: `__shared__ double scratch_pad[16][16 + 1];`. If the amount of LDS used is a limiting factor, a [swizzling pattern is needed to avoid conflicts](https://rocm.blogs.amd.com/software-tools-optimization/lds-bank-conflict/README.html#naive-solution).
- **Precompute indices**, scalar or vector integer operation often being done at a much lower rate than floating point operations. Compile time known extent will definitely help.
- **Prefetch data into LDS**, (1) start prefetching new data into **registers** while (2) working on the previous LDS data, (3) store the prefetched data from registers to LDS, repeat to (1).
- **Avoid passing** large arguments by-value to `__global__` functions.
- **Avoid excessive** unrolling via `#pragma unroll`.
- **Use GPU aware and direct** communication libraries, Cray MPICH support [such behaviors](../software_stack/libraries/index.md#adastra-software-stack-libraries-mpi-cray-mpich-gpu-aware).
- **Avoid excessive precision**. Most GPU can do Binary32 (float) operation at higher rate per clock than Binary64 (double). This is the case for the MI250X but also and most significantly for commodity hardware (gaming GPUs for which the rate is on the order of 1:16 ~~ in favor of Binary32). If your algorithm do not require the dynamic range (exponent) of Binary64 or the precision (mantissa) of Binary64, use Binary32. for some application, you can go as low as doing computation in Binary32 and storing the result in Binary16 or BF16.
- **Do not assume the compiler will unroll**.
- **Do not assume the compiler will avoid register reloads**. Mark your pointers `__restrict` or store loaded values in scalar to avoid unnecessary reloading.

<a id="hbm-is-not-dram"></a>

##### HBM is not DRAM

Observe, on this SK hynix slide, the different tradeoff that HBM and DRAM represent.

[![../_images/hbm_vs_dram.jpg](https://dci.dci-gitlab.cines.fr/webextranet/_images/hbm_vs_dram.jpg)](https://dci.dci-gitlab.cines.fr/webextranet/_images/hbm_vs_dram.jpg)

<a id="cdna-shenanigans"></a>

#### CDNA shenanigans

<a id="accumulator-gpr"></a>

##### Accumulator GPR

AGPR, a kind of register used for accumulating the intermediate multiplication resulting of a tensor contraction (basically `+=`). For kernels using MFMA these act as tensor memory for the result only. These registers are not usable for general computations but are often used for spilling true VGPR before having to definitely spill to GMEM.

Some relevant external documents [here](https://github.com/ROCm/ROCm/issues/1689#issuecomment-1553751913) and [here](https://rocm.docs.amd.com/projects/rocprofiler-compute/en/latest/conceptual/pipeline-descriptions.html#desc-agprs).

<a id="peak-binary32-flop-s-on-cdna2-with-v-pk-fma-f32"></a>

##### Peak Binary32 Flop/s on CDNA2 with `v_pk_fma_f32`

As mentioned in the [Adastra architecture document](../architecture/index.md#architecture-adastra-accelerated-nodes), it is possible to use SIMD operation inside a GPU thread (SIMD lane) to reach +40 Binary32 TFlop/s. Unfortunately, as of ROCm 5.7.1, `amdclang` does not generate the `v_pk_fma_f32` instruction allowing us to reach such throughput. Below is an inline assembly wrapper around this operation.

```c++
/// Compute x = x * y + y
///
__device__ static inline void
mad(float2& x, const float2& y) {
    asm volatile("v_pk_fma_f32 %0, %0, %2, %2"
                // %0
                : "=v"(x)
                // %1      %2
                : "0"(x), "v"(y));
}
```

<a id="gpu-page-migration"></a>

<a id="porting-optimization-performance-tuning-monitoring-gpu-specific-cdna-shena-page-migration"></a>

##### GPU Page Migration

Unified Virtual Addressing (UVA):

- Historically, the GPU had it’s address space and the CPU had its own.
  :   - Remember the theory of: memory is a big array ?
      - Well we had two big array, one for the CPU and one more per GPU.
      - Same pointers meant different things on different devices.
- Nowadays, they tend to be the same, they are Unified.
- This is not unified memory (UM)! But a requirement to implement Unified Memory (UM).

Then came Unified Shared Memory (USM), Unified Virtual Addressing (UVM), Unified Memory (UM), same thing:

- Assuming UVA, a device can read/write (RW) an other device’s memory without pointer shenanigans.
- UM allows an in memory value to be read everywhere **as if** it was resident on the device doing the access.
- How to ensure that some value say, in device A memory, will be available on the reading device B ?
  :   - Either you have only one memory (MI300A);
      - Or you do implicit copies.
- UM does not imply page migration from one device to another.
  :   - Under the **as if** rule, UM does not require page migration, this is an implementation detail.
      - The MI300A do note rely on page migration.

<a id="on-amd-s-cdna2-and-cdna3"></a>

###### On AMD’s CDNA2 and CDNA3

Some devices such as the MI250X and MI300A support hardware UM in two different ways. The MI250X does hardware backed page migration. The MI300A posses one NUMA for both the GPU and CPU devices, thus no copies are needed.

AMD offers [decent documentation](https://rocm.docs.amd.com/en/latest/conceptual/gpu-memory.html#gpu-memory), [here also](https://github.com/ROCm/HIP/blob/main/docs/markdown/hip_programming_guide.md), [here also](https://gpuopen.com/learn/amd-lab-notes/amd-lab-notes-mi200-memory-space-overview) on the subject of:

- which [kind of memory](https://rocm.docs.amd.com/en/latest/conceptual/gpu-memory.html#memory-allocation) exist (pinned, pageable, managed);
- which HIP API one should use to allocate which kind of memory;
- which kind memory implies which performance/copies under [XNACK](https://rocm.docs.amd.com/en/latest/conceptual/gpu-memory.html#xnack) and without XNACK <https://rocm.docs.amd.com/en/latest/conceptual/gpu-memory.html#access-behavior>;

XNACK enable a device’s capability to retry memory accesses after a page fault. When it retries, the device (CPU or GPU), expect the page to have been moved onto the accessing device. **XNACK on/off can be understood as enabling/disabling UM support**.

One can enable XNACK by defining the `HSA_XNACK` environment variable to `1` or disabling it by setting the variable to `0` en `unset` ting it. By default XNACK is disabled.

From <https://docs.olcf.ornl.gov/systems/frontier_user_guide.html#enabling-gpu-page-migration> we have:

- If `HSA_XNACK=0`, page faults in GPU kernels are not handled and will terminate the kernel. Therefore all memory locations accessed by the GPU must either be resident in the GPU HBM or mapped by the HIP runtime. Memory regions may be migrated between the host DDR4 and GPU HBM using explicit HIP library functions such as `hipMemAdvise` and `hipPrefetchAsync`, but memory will not be automatically migrated based on access patterns alone.
- If `HSA_XNACK=1`, page faults in GPU kernels will trigger a page table lookup. If the memory location can be made accessible to the GPU, either by being migrated to GPU HBM or being mapped for remote access, the appropriate action will occur and the access will be replayed. Page migration will happen between CPU DDR4 and GPU HBM according to page touch. The exceptions are if the programmer uses a HIP library call such as `hipPrefetchAsync` to request migration, or if a preferred location is set via `hipMemAdvise`, or if GPU HBM becomes full and the page must forcibly be evicted back to CPU DDR4 to make room for other data.
- CPU accesses to migratable memory may behave differently than other platforms you’re used to. On Adastra, pages will not migrate from GPU HBM to CPU DDR4 based on access patterns alone. Once a page has migrated to GPU HBM it will remain there even if the CPU accesses it, and all accesses which do not resolve in the CPU cache will occur over the Infinity Fabric between the AMD “Optimized 3rd Gen EPYC” CPU and AMD MI250X GPU. Pages will only *automatically* migrate back to CPU DDR4 if they are forcibly evicted to free HBM capacity, although programmers may use HIP APIs to manually migrate memory regions.
- Disabling XNACK will not necessarily result in an application failure, as most types of memory can still be accessed by the AMD “Optimized 3rd Gen EPYC” CPU and AMD MI250X GPU. In most cases, however, the access will occur in a zero-copy fashion over the Infinity Fabric. The exception is memory allocated through standard system allocators such as `malloc`, which cannot be accessed directly from GPU kernels without previously being registered via a HIP runtime call such as `hipHostRegister`. Access to malloc’ed and unregistered memory from GPU kernels will result in fatal unhandled page faults. The table below shows how common allocators behave with XNACK disabled.

**Warning**

On MI300A, XNACK should be defined if one intend to use UM. The overhead of UM enabled on MI300A has been measured as a x0.93 to x0.9 speedup on DGEMM kernels using memory allocated by `hipMalloc`.

The accessibility of memory from GPU kernels and whether pages may migrate depends three factors: how the memory was allocated; the XNACK operating mode of the GPU; whether the kernel was compiled to support page migration.

`HSA_XNACK=1` **Automatic Page Migration Enabled**

| Allocator | Initial Physical Location | CPU Access after GPU First Touch | Default Behavior for GPU Access |
| --- | --- | --- | --- |
| System Allocator (malloc,new,allocate, etc) | Determined by first touch | Zero copy read/write | Migrate to GPU HBM on touch, then local read/write |
| hipMallocManaged | GPU HBM | Zero copy read/write | Populate in GPU HBM, then local read/write |
| hipHostMalloc | CPU DDR4 | Local read/write | Zero copy read/write over Infinity Fabric |
| hipMalloc | GPU HBM | Zero copy read/write over Infinity Fabric | Local read/write |

Disabling XNACK will not necessarily result in an application failure, as most types of memory can still be accessed by the AMD “Optimized 3rd Gen EPYC” CPU and AMD MI250X GPU. In most cases, however, the access will occur in a zero-copy fashion over the Infinity Fabric. The exception is memory allocated through standard system allocators such as `malloc`, which cannot be accessed directly from GPU kernels without previously being registered via a HIP runtime call such as `hipHostRegister`. Access to malloc’ed and unregistered memory from GPU kernels will result in fatal unhandled page faults. The table below shows how common allocators behave with XNACK disabled.

`HSA_XNACK=0` **Automatic Page Migration Disabled**

| Allocator | Initial Physical Location | Default Behavior for CPU Access | Default Behavior for GPU Access |
| --- | --- | --- | --- |
| System Allocator (malloc,new,allocate, etc) | CPU DDR4 | Local read/write | Fatal Unhandled Page Fault |
| hipMallocManaged | CPU DDR4 | Local read/write | Zero copy read/write over Infinity Fabric |
| hipHostMalloc | CPU DDR4 | Local read/write | Zero copy read/write over Infinity Fabric |
| hipMalloc | GPU HBM | Zero copy read/write over Infinity Fabric | Local read/write |

In color this gives:

[![../_images/xnack.PNG](https://dci.dci-gitlab.cines.fr/webextranet/_images/xnack.PNG)](https://dci.dci-gitlab.cines.fr/webextranet/_images/xnack.PNG)

And out of this we can make some recommendations:

- avoid accessing CPU memory from the GPU;
- avoid accessing GPU memory from the CPU;
- avoid managed memory as most HPC implementations are impractically slow;
- use zero copy memory for mass loading of data (reloading a checkpoint into device memory, dumping data to disk).

In addition, on CDNA2, when memory other than global device memory is the target of an atomic operation the default is to use a CAS loop (because this is what PCIe/xGMI supports) which works on all kind of memory except for pinned memory. When more performance is asked by the user, an unsafe atomic operation, hardware based is used instead (say `unsafeAtomicAdd`). But these (hardware) atomic instructions only work for LDS or GMEM, not pinned or managed memory (with or without XNACK), and in addition, they flush denormals. Indeed, these hardware atomic, if operating on fine-grained memory (which is marked write-uncacheable through the page tables), and if the uncached data is stored in host memory on a PCIe system, the atomic will be forwarded from Infinity Fabric to PCIe. Any atomic not supported by the PCIe bus will be a NOP and give incorrect result. This behavior changes with CDNA3 where the PCIe control convert these atomics to PCIe a compatible CAS loop. Details are given [in the LLVM documentation](https://clang.llvm.org/docs/LanguageExtensions.html#extensions-for-controlling-atomic-code-generation) in [AMD’s ROCm hardware reference](https://rocm.docs.amd.com/en/docs-7.2.1/reference/gpu-atomics-operation.html) and in [AMD’s ROCm documentation](https://instinct.docs.amd.com/projects/amdgpu-docs/en/latest/conceptual/pcie-atomics.html#how-rocm-uses-pcie-atomics).

If performance is a must, managed memory is not viable on discreet AMD GPUs.

The platform one should aim for is a mix of the less forgiving architectures and in practice, it could give something like so:

[![../_images/common_denominator_target_platform.png](https://dci.dci-gitlab.cines.fr/webextranet/_images/common_denominator_target_platform.png)](https://dci.dci-gitlab.cines.fr/webextranet/_images/common_denominator_target_platform.png)

<a id="compiling-hip-kernels-for-specific-xnack-modes"></a>

###### Compiling HIP kernels for specific XNACK modes

Although XNACK is a capability of the MI250X GPU, it does require that kernels be able to recover from page faults. Both the ROCm and CCE HIP compilers will default to generating code that runs correctly with both XNACK enabled and disabled. Some applications may benefit from using the following compilation options to target specific XNACK modes. Note that when using the CCE compiler, do not try to fiddle with the `--offload-arch=gfx90a:xnack`, stay with the default `--offload-arch=gfx90a`. The examples below target `gfx90a` (MI250X).

`hipcc --offload-arch=gfx90a` or `CC --offload-arch=gfx90a -x hip`

Kernels are compiled to a single “xnack any” binary, which will run correctly with both XNACK enabled and XNACK disabled.

`hipcc --offload-arch=gfx90a:xnack+` or `CC --offload-arch=gfx90a:xnack+ -x hip`

Kernels are compiled in “xnack plus” mode and will *only* be able to run on GPUs with `HSA_XNACK=1` to enable XNACK. Performance may be better than “xnack any”, but attempts to run with XNACK disabled will fail.

`hipcc --offload-arch=gfx90a:xnack-` or `CC --offload-arch=gfx90a:xnack- -x hip`

Kernels are compiled in “xnack minus” mode and will *only* be able to run on GPUs with `HSA_XNACK=0` and XNACK disabled. Performance may be better than “xnack any”, but attempts to run with XNACK enabled will fail.

`hipcc --offload-arch=gfx90a:xnack- --offload-arch=gfx90a:xnack+ -x hip` or `CC --offload-arch=gfx90a:xnack- --offload-arch=gfx90a:xnack+ -x hip`

Two versions of each kernel will be generated, one that runs with XNACK disabled and one that runs if XNACK is enabled. This is different from “xnack any” in that two versions of each kernel are compiled and HIP picks the appropriate one at runtime, rather than there being a single version compatible with both. A “fat binary” compiled in this way will have the same performance of “xnack+” with `HSA_XNACK=1` and as “xnack-” with `HSA_XNACK=0`, but the final executable will be larger since it contains two copies of every kernel.

<a id="openmp-offloading"></a>

###### OpenMP offloading

As of 2025/04, the Cray OpenMP offload implementation prevent page migration on MI250X, instead, we get something close pinned CPU memory behavior. You will need `export CRAY_MALLOPT_OFF=1` to turn page migration on.
This does not affect MI300A because there is not page migration.

That said, we have similar problem with the ROCm (amdclang) OpenMP offloading implementation when USM is used. It seems to pin every pages it encounters in a map clause! We are not aware of a flag/environment variable working around that.

You may want to read the Cray OpenACC implementation’s documentation using the `man intro_openmp` command.

<a id="openacc-offloading"></a>

###### OpenACC offloading

You may want to read the Cray OpenACC implementation’s documentation using the `man intro_openacc` command. The `CRAY_ACC_USE_UNIFIED_MEM` variable may be of particular interest.

<a id="cdna1-cdna2-atomics"></a>

<a id="porting-optimization-performance-tuning-monitoring-gpu-specific-cdna-atomics"></a>

##### CDNA1 & CDNA2 Atomics

[![../_images/atomicavai.PNG](https://dci.dci-gitlab.cines.fr/webextranet/_images/atomicavai.PNG)](https://dci.dci-gitlab.cines.fr/webextranet/_images/atomicavai.PNG)

Note that some atomic operations can be implemented as Compare And Swap (CAS) loops. This is *can* be detrimental to performance but not always, se below.

On CDNA2, atomics are resolved at the L2 cache Level.

<a id="floating-point-atomic-on-lds"></a>

###### Floating point atomic on LDS

In uncontended situations, HIP’s `atomicAdd` on Binary32 will be slower than using a CAS loop. This does not apply to `atomicAdd` on Binary64.

<a id="cdna3-atomics"></a>

##### CDNA3 Atomics

The `-munsafe-fp-atomics` flag is not needed anymore to benefit from atomic hardware acceleration.

On CDNA3, atomics are resolved at the Infinity cache Level, the Memory Adjacent Last Level (MALL).
