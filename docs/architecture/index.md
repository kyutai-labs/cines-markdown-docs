<!-- Source: https://dci.dci-gitlab.cines.fr/webextranet/architecture/index.html -->
<!-- Title: Adastra’s architecture -->

<a id="adastra-s-architecture"></a>

<a id="architecture-adastra"></a>

# Adastra’s architecture

<a id="system-overview"></a>

<a id="architecture-adastra-overview"></a>

## System overview

Adastra is a French supercomputer hosted at CINES, a Tier 1 computing site located in Montpellier. The Adastra supercomputer is an HPE-Cray EX system, combined with two ClusterStor E1000 storage systems. A simple architectural diagram is shown below:

[![Adastra system architecture sketch](https://dci.dci-gitlab.cines.fr/webextranet/_images/schema-archi-ADASTRA.png)](https://dci.dci-gitlab.cines.fr/webextranet/_images/schema-archi-ADASTRA.png)

<a id="adastra-s-hardware"></a>

## Adastra’s hardware

From the application developer’s point of view, a HPE-Cray system is a tightly integrated network of thousands of nodes. Some are dedicated to administrative or networking functions and therefore off-limits to application programmers. Programmers typically use the following node types:

- Login nodes: The node you access when you first log in to the system. Login nodes offer the full HPE-Cray Programming Environment (CrayPE or CPE) operating system and are used for basic development tasks such as editing files and compiling code. the login nodes are a shared resources that may be used concurrently by multiple users. Login nodes are also sometimes called service nodes.
- Compute nodes: The nodes on which production jobs are executed. Compute nodes can be accessed only by submitting jobs through a batch management system (i.e., SLURM, PBS, LSF). They generally have access to a high-performance parallel file system and can be dedicated resources, exclusively yours for the duration of the batch reservation. When new users first begin working on the such system, this difference between login and compute nodes can be confusing. Remember, when you first log in to the system, you are placed on a login node. You cannot execute parallel programs on the login node. Instead, use Adastra’s batch system to place parallel programs on the compute nodes.

Below is a list of the hardware Adastra is made of:

- 544 scalar nodes (2 AMD Genoa EPYC 9654 96 cores 2.4 GHz processors (no turbo/boost), 768 Gio of DDR5-4800 MHz memory per node (4 Gio/core), 1 Slingshot 200 Gb/s Network Interface Card (NIC));
- 356 accelerated nodes specialized for General Purpose computation on GPUs (GPGPU) computations (1 AMD Trento EPYC 7A53 64 cores 2.0 GHz processor (3.5 GHz turbo/boost) with 256 Gio of DDR4-3200 MHz CPU memory per node, 4 Slingshot 200 Gb/s NICs, 8 GPUs devices (4 AMD MI250X accelerator, each with 2 GPUs) with a total of 512 Gio of HBM2 per node);
- 28 accelerated nodes specialized for General Purpose computation on GPUs (GPGPU) computations (4 Slingshot 200 Gb/s NICs, 4 APU devices (4 AMD MI300A accelerator) with a total of 512 Gio of HBM2 per node);
- 12 visualization and pre/post processing nodes (2 Genoa 96 cores 2.4 GHz processors, 2048 Gio of DDR5-4800 MHz memory per node, 1 Slingshot 200 Gb/s NICs and 2 NVIDIA L40 graphic cards);
- A Slingshot interconnection network;
- 10 front-end and transfer nodes (2 AMD Genoa EPYC 9654 96 cores 2.4 GHz processors (3.7 GHz turbo/boost), 512 Gio of DDR5-4800 MHz memory per node, 1 Slingshot 200 Gb/s NICs and 4 x 1.6 Tio SAS MU SSDs configured in RAID10);
- 1 ClusterStor E1000 SSD for LUSTRE storage space *home*: 125 Tio capacity; 77 Gio/s read and 34 Gio/s write throughput;
- 1 ClusterStor E1000 SSD for LUSTRE storage space *scratch*: 4.71 Pio capacity; 1086 Gio/s read and 786 Gio/s write throughput.

**Note**

Scalar node refers to a CPU only node. An accelerated node contains accelerators (MI250X or MI300A in the case of Adastra) and potentially also a CPU (which may be part of the same chip than the accelerator leading to something like an [APU](https://en.wikipedia.org/wiki/AMD_APU)).

The compute nodes are housed in water-cooled HPE-Cray EX4000 cabinets. These cabinets carry the compute blades which, depending on the technology it contains, includes either:

- 4 scalar compute nodes (CPU only nodes);
- 2 accelerated compute nodes (CPU host + accelerator).

[![Adastra HPE-Cray EX4000 rack diagram](https://dci.dci-gitlab.cines.fr/webextranet/_images/rack-Cray.png)](https://dci.dci-gitlab.cines.fr/webextranet/_images/rack-Cray.png)

The HPE-Cray EX4000 cabinet also includes network modules that connect the compute nodes to the Slingshot network. Each HPE-Cray EX4000 cabinet contains a maximum of 64 modules (i.e., a maximum of 256 scalar nodes and a maximum of 128 accelerated nodes). The dragonfly topology of the Slingshot interconnect reduces the adverse effects of bad process placement that can occur due to SLURM allocation fragmentation.

The Adastra has four cabinets with 64 accelerated nodes and 128 scalar nodes. The last cabinet contains the remaining accelerated nodes and scalar nodes. This makes 356 accelerated nodes and 544 scalar nodes. An other cabinet stores the 28 APU nodes.

<a id="adastra-partitions-summary"></a>

## Adastra partitions summary

| Characteristic | Adastra Scalar (Genoa) | Adastra Accelerated (MI250X) | Adastra Accelerated (MI300A) |
| --- | --- | --- | --- |
| Processor per node | 2 AMD EPYC 9654 (Genoa, Zen 4) | 1 AMD EPYC 7A53 (Trento, Zen 3) + 4 AMD Instinct MI250X (CDNA 2) | 4 AMD Instinct MI300A APUs (Zen 4 cores and CDNA 3) |
| CPU core per node | 192 (2 * 96 @ 2.4 GHz) | 64 (1 * 64 @ 2.0 GHz) | 96 (4 * 24 @ 2.6 GHz) |
| Non host processing device per node | (none) | 8 GCDs (4 MI250X cards, each with 2 accelerators) | 4 (1 integrated per MI300A APU) |
| Memory per node | 768 Gio DDR5-4800 | 256 Gio DDR4-3200 (CPU) + 512 Gio HBM2e (GPU) | 512 Gio HBM3 shared with CPU and GPU |
| Theoretical memory throughput per device (per node) | 0.429 Tio/s (0.858 Tio/s) | 1.526 Tio/s (12.2 Tio/s) | 4.959 Tio/s (19.8 Tio/s) |
| Interconnect link per node | 1 Slingshot 200 Gb/s NIC | 4 Slingshot 200 Gb/s NICs | 4 Slingshot 200 Gb/s NICs |
| Theoretical Binary64 Flop/s per node, host + device | 7.37 + 0.0 TFlop/s | 2.04 + 191.5 TFlop/s | 3.99 + 245.2 TFlop/s |
| Node count per partition | 544 | 356 | 28 |
| Theoretical Binary64 Flop/s per partition | 4.01 PFlop/s | 68.9 PFlop/s | 6.98 PFlop/s |

<a id="adastra-accelerated-mi250x-nodes"></a>

<a id="architecture-adastra-accelerated-nodes"></a>

## Adastra accelerated (MI250X) nodes

Each accelerated (MI250X) node consists of **1** AMD EPYC 7A53 (Trento) **processor** with **64 cores** at 2.0 GHz and **4** AMD Instinct **MI250X accelerators** (code name gfx90a, Aldebaran, CDNA 2 microarchitecture) as shown in the figure below. This provides 64 cores (with **2 hardware threads per core**) attached to **256 Gio** of DDR4-3200 MHz memory and **8 Graphics Compute Dies** (GCD) per node. The MI250X accelerator is a Multi-Chip Module (MCM) and comes with 2 GCDs. **A GCD can be seen as a GPU**. The user can think of the 8 GCDs as 8 separate GPUs. On Adastra The MI250X is [OAM packaged](https://www.nextplatform.com/2019/03/15/inside-facebooks-future-machine-learning-platforms/).

[![An MI250X accelerator, exposing the two GCDs.](https://dci.dci-gitlab.cines.fr/webextranet/_images/mi250x_die.jpg)](https://dci.dci-gitlab.cines.fr/webextranet/_images/mi250x_die.jpg)

<a id="theoretical-flop-performance"></a>

### Theoretical Flop performance

The theoretical Binary64 Flop/s per MI250X GCD is given using vector ALUs an no Matrix Fused Multiply Add (MFMA). Each MI250X CU has 4 SIMD ALUs processing 1 wavefront of 64 threads every 4 cycles.

- **Theoretical Binary64 Flop/s per MI250X GCD**:
  `1.7 GHz * 1 FMA/cycle * 2 SIMD operations/FMA * 16 scalar Binary64 operations/SIMD operation * 4 SIMD ALU * 110 CUs =` 23.93 TFlop/s.
- **Theoretical MI250X GCD Binary64 Flop/s per node**: `8 * 23.93 =` 191.5 TFlop/s.
- **Theoretical Binary64 Flop/s per core**:
  `2.0 GHz * 2 FMA/cycle * 2 SIMD operations/FMA * 4 scalar Binary64 operations/SIMD operation =` 32 GFlop/s.

**Note**

If your code can exploit packed single-precision floating-point operations (`float2`, `float4`), performance reaches 47.86 TFlop/s per GCD.

<a id="memory-and-throughput"></a>

### Memory and throughput

The host has a total of 256 Gio of main memory and each GCD has 64 Gio of HBM2e. The HBM2e is provided by 4 SK Hynix stacks visible on the picture below. HBM memories are basically stacked DDR chips. As such, we should double the transaction per second. So, if say, `rocm-smi` reports a memory frequency of 1.6 GHz, the chips are able to provide signaling at two times this rate.

- **Theoretical memory throughput per device**: `3.2 GTransaction/second * 1024/8 bytes bus width * 4 HBM2e stack =` 1638.4 Go/s or 1.526 Tio/s.
- **Per node**: 12.2 Tio/s.

On the MI250X, the total amount of L2 cache is 8 MiB (8192 KiB / 4 memory controllers per GCD = 2 MiB for ~27 CUs), with an overall read/write throughput of around 7 TiB/s. The L1 cache provides 16 KiB per CU, for a total of about 1.7 MiB. There is no L3 cache on the MI250X (unlike the MI300A, which includes one). This small L2 cache is a significant characteristic of AMD GPUs at large, which differs with slower but larger Nvidia caches. This should be taken into consideration when writing kernels. Memory access patterns that are decent on NVidia may not perform as well on AMD datacenter GPUs.

<a id="architecture-and-interconnect"></a>

### Architecture and interconnect

The IO die’s Global Memory Interface (GMI) links are used by the Core Chiplet Dies (CCDs) of the Trento CPU to communicate and maintain cache coherency. The [eXternal GMI](https://www.kernel.org/doc/html/latest/gpu/amdgpu/xgmi.html) (or Inter-chip Global Memory Interconnect, xGMI) links are used for chip peer to peer communications (GPU/GPU, GPU/CPU CPU/GPU or CPU/CPU). The GMI and xGMI are the backbone of AMD’s [Infinity Fabric](https://en.wikichip.org/wiki/amd/infinity_fabric) (IF). A fabric can be seen as an abstraction of the underlying communication hardware. AMD’s IF consists of two separate communication planes, the Infinity Scalable Data Fabric (SDF) and the Infinity Scalable Control Fabric (SCF). xGMI can be seen as a pumped up PCIe. It provides, at equivalent PCIe generation, slightly better transaction per second and (seemingly) better line code efficiency. xGM2 is ~ 18 GT/s, xGMI3 is ~ 25 GT/s and xGMI 4 ~ 32 GT/s. Similarly, the PCIe [Extended Speed Mode](https://www.synopsys.com/blogs/chip-design/ccix-pcie-ai-networking-storage.html) (ESM) allows for higher throughput over similar PCIe 4 lane count and hardware due to higher PCIe clock. In fact, ESM is a *side effect* of the [Cache Coherent Interconnect for Accelerators](https://www.ccixconsortium.com/) (CCIX) protocol which is used by AMD and HPE-Cray on Adastra’s nodes. The CCIX consortium standardized ESM to achieve up to 25 GT/s over traditional PCIe 4 (16 GT/s) lanes.

The CPU socket is connected to each GCD via Infinity Fabric over x16 xGMI2, allowing a theoretical host-to-device (H2D) and device-to-host (D2H) throughput of 36 Go/s (33.53 Gio/s). The 2 GCDs on the same MI250X are connected via Infinity Fabric over 4 x16 xGMI3 links for a theoretical throughput of 200 Go/s (186.3 Gio/s) (in each directions simultaneously). The GCDs on different MI250X are connected with Infinity Fabric GPU-GPU in the arrangement shown in the Adastra MI250X node diagram below. The MI250X are each connected to one NIC via PCIe4 + ESM.

**Note**

We use the Graphic Processing Unit (GPU) term where in fact, we should really use the accelerator term or in the specific case of the MI250X, the GCD term instead. Indeed, the MI250X accelerated nodes use accelerators which can be seen as GPU without the graphic specific parts (so not a Graphic PU..).

Binding can be extremely significant on Adastra (especially if you do a lot of CPU/GPU copy or use Unified Shared Memory (USM)) and the user should understand how to properly define it. For this reason understanding the diagram below is crucial to correctly using the hardware. We provide many rank to core and GPU binding configurations in [this document](../porting_optimization/detailed_binding_script.md#porting-optimization-detailed-binding-script) and explain how to make use of them in [this document](../porting_optimization/index.md#porting-optimization-performance-tuning-monitoring-proper-binding-why-how-binding-simple-script). Also, see the [Understanding the AMD MI250X GPU](../external_documentation_and_training_resources/index.md#learn-mi250x) and [Proper binding, why and how](../porting_optimization/index.md#porting-optimization-performance-tuning-monitoring-proper-binding-why-how) documents. The detailed NUMA diagram shown below can be used to manage the CPU-GPU binding of MPI tasks on a node.

[![Adastra MI250X node architecture diagram](https://dci.dci-gitlab.cines.fr/webextranet/_images/adastra_mi250x_simplified_diagram.jpg)](https://dci.dci-gitlab.cines.fr/webextranet/_images/adastra_mi250x_simplified_diagram.jpg)

[![../_images/adastra_mi250x_diagram.png](https://dci.dci-gitlab.cines.fr/webextranet/_images/adastra_mi250x_diagram.png)](https://dci.dci-gitlab.cines.fr/webextranet/_images/adastra_mi250x_diagram.png)

The CPUs and GPUs NUMA node latency is given below. These numbers do not represent the throughput, they can be compared relatively but a number x2 larger than another does not necessarily mean the latency is two times larger.

![../_images/bardpeak_numa_latency.png](https://dci.dci-gitlab.cines.fr/webextranet/_images/bardpeak_numa_latency.png)

The throughput measured **using** the [System Direct Memory Access](https://rocm.docs.amd.com/en/latest/conceptual/gpu-memory.html#system-direct-memory-access) (SDMA) engines (`export HSA_ENABLE_SDMA=1`).

![../_images/bardpeak_throughput_sdma.png](https://dci.dci-gitlab.cines.fr/webextranet/_images/bardpeak_throughput_sdma.png)

The throughput measured **without** the SDMA engines (`export HSA_ENABLE_SDMA=0`).

![../_images/bardpeak_throughput_no_sdma.png](https://dci.dci-gitlab.cines.fr/webextranet/_images/bardpeak_throughput_no_sdma.png)

<a id="adastra-accelerated-mi300a-nodes"></a>

## Adastra accelerated (MI300A) nodes

Each accelerated (MI300A) node consists of **four AMD Instinct MI300A accelerators** (code name *gfx942*, CDNA 3 microarchitecture). Each MI300A is an **Accelerated Processing Unit (APU)** that integrates both:

- **24 CPU cores** (Zen 4-based);
- **228 CDNA 3 Compute Units (CU)**.

The GPU and CPU shared a unified HBM memory pool. The MI300A is a natural extension to the MCM which is the MI250X. While for the MI250X, producing an IO die that was fast enough to fuse the two GCDs as if they were one big GPU was not feasible, this was rectified on the MI300A/X. Each MI300A is shown as one GPU by `rocm-smi`.

<a id="id1"></a>

### Theoretical Flop performance

The theoretical Binary64 Flop/s per MI300A is given using vector ALUs an no Matrix Fused Multiply Add (MFMA). Each MI300A CU has 4 SIMD ALUs processing 1 wavefront of 64 threads every 4 cycles.

- **Theoretical Binary64 Flop/s per MI300A GPU**:
  `2.1 GHz * 1 FMA/cycle * 2 SIMD operations/FMA * 16 scalar Binary64 operations/SIMD operation * 4 SIMD ALUs * 228 CUs =` 61.3 TFlop/s (x2 using `float2`).
- **Theoretical MI300A GPU Binary64 Flop/s per node**: `4 * 61.3 =` 245.2 TFlop/s.
- **Theoretical Binary64 Flop/s per core**:
  `2.6 GHz * 2 FMA/cycle * 0.5 AVX2 emulation * 2 SIMD operations/FMA * 8 scalar Binary64 operations/SIMD operation =` 41.6 GFlop/s.

<a id="id2"></a>

### Memory and throughput

The GPU and CPU share an HBM3 pool of 128 Gio per MI300A or 512 Gio in total. No explicit copy needed for the GPU to access CPU memory.

- **Theoretical memory throughput per device**: `5.2 GTransaction/second * 1024/8 bytes bus width * 8 HBM3 stack =` 5324.8 Go/s or 4.96 Tio/s.
- **Per node**: 19.84 Tio/s.

Note that in practice, the MI300A’s IO die struggles to funnel all the signal at full rate. The GPU chiplets are close to 6 out of the 8 stacks and in practice we get ~x0.75 peak throughput.

Unified memory simplifies heterogeneous programming and can reduces overhead compared to discrete CPU/GPU architectures but the user must be careful that the code would also work on discreet GPUs are theses are much more common.

<a id="architecture"></a>

### Architecture

Binding can be extremely significant on Adastra (especially if you do a lot of CPU/GPU copy or use Unified Shared Memory (USM)) and the user should understand how to properly define it. For this reason understanding the diagram below is crucial to correctly using the hardware. We provide many rank to core and GPU binding configurations in [this document](../porting_optimization/detailed_binding_script.md#porting-optimization-detailed-binding-script) and explain how to make use of them in [this document](../porting_optimization/index.md#porting-optimization-performance-tuning-monitoring-proper-binding-why-how-binding-simple-script). Also, see [Proper binding, why and how](../porting_optimization/index.md#porting-optimization-performance-tuning-monitoring-proper-binding-why-how) documents.

[![../_images/adastra_mi300a_diagram.png](https://dci.dci-gitlab.cines.fr/webextranet/_images/adastra_mi300a_diagram.png)](https://dci.dci-gitlab.cines.fr/webextranet/_images/adastra_mi300a_diagram.png)

The CPUs and GPUs NUMA node latency is given below. These numbers do not represent the throughput, they can be compared relatively but a number x2 larger than another does not necessarily mean the latency is two times larger.

![../_images/mi300a_numa_latency.png](https://dci.dci-gitlab.cines.fr/webextranet/_images/mi300a_numa_latency.png)

<a id="adastra-scalar-nodes-genoa"></a>

<a id="architecture-adastra-scalar-nodes"></a>

## Adastra scalar nodes (GENOA)

Each scalar (GENOA) node is equipped with **two AMD EPYC 9654 processors**, each providing **96 cores at 2.4 GHz** (192 cores per node). Compared to Zen 3, the Zen 4 architecture now supports AVX-512 though not at full speed (it *emulates* AVX-512 using AVX2).

<a id="id3"></a>

### Theoretical Flop performance

- **Theoretical Binary64 Flop/s per core**:
  `2.4 GHz * 2 FMA/cycle * 0.5 AVX2 emulation * 2 SIMD operations/FMA * 8 scalar Binary64 operations/SIMD operation =` 38.4 GFlop/s.
- **Per node**: `2 * 96 * 38.4 =` 7.37 TFlop/s.

<a id="id4"></a>

### Memory and throughput

Each socket handles 12 DDR5-4800 memory channels each fitted with 32 Gio DIMMs for a total of 768 Gio of main memory.

- **Theoretical memory throughput per device**:
  `4800 MTransaction/second * 12 channel/socket * 8 byte/transaction =` 460800 Mo/s or 429.1 Gio/s.
- **Per node**: 858 Gio/s.

In practice we reach 704 Gio/s (82% of peak) on AVX512 using at least 48 cores spread over the two sockets’ L3. Transparent Huge Pages (THP) is enabled, as visible using the `grep AnonHugePages /proc/meminfo` and `egrep 'trans|thp' /proc/vmstat` commands.

<a id="id5"></a>

### Architecture

- Each CPU integrates 4 Core Chiplet Dies (CCDs) interconnected with a central IO die.
- Each CCD contains 3 Core CompleXes (CCXs), each with 8 cores.
- Each core supports 2 hardware threads (SMT).
- Cache hierarchy:

  > - 32 Mio of L3 cache per CCX.
  > - 1024 Kio of private L2 cache per core.

**Note**

Assuming 100 W for the DRAM, 360 W per socket and 125 W for other components, we have 100 + 125 + 360 * 2 = 945 W per scalar node. We obtain a maximum efficiency of **7.373 TFlop/s / 945 W = 7.8 GFlop/J**. Assuming 70 W for the DRAM, 180 W per socket, 560 W for each MI250 and 180 W for other components, we have 70 + 180 + 180 + 560 * 4 = 2670 W per accelerated node. We obtain a maximum efficiency of **191.6 TFlop/s / 2670 W = 71.8 GFlop/J**. One could argue the accelerated nodes are 9 times more efficient than their same generation scalar node equivalent.

**Note**

Do use Flop/J or Flop/s/W but not Flop/s/J.

The diagram below (click on the picture to see it more clearly) represents the arrangement of the cores and caches hierarchy for the 2 AMD Genoa EPYC 9654 making each of Adastra’s Genoa nodes. Note that the number of core is not a power of two, which for some core may lead to imbalance. We provide many rank to core binding configurations in [this document](../porting_optimization/detailed_binding_script.md#porting-optimization-detailed-binding-script) and explain how to make use of them in [this document](../porting_optimization/index.md#porting-optimization-performance-tuning-monitoring-proper-binding-why-how-binding-simple-script). Also, see the [Understanding the Zen 4 Genoa CPU](../external_documentation_and_training_resources/index.md#learn-zen4-genoa) and [Proper binding, why and how](../porting_optimization/index.md#porting-optimization-performance-tuning-monitoring-proper-binding-why-how) documents.

[![Adastra Genoa node architecture diagram](https://dci.dci-gitlab.cines.fr/webextranet/_images/adastra_genoa_diagram.png)](https://dci.dci-gitlab.cines.fr/webextranet/_images/adastra_genoa_diagram.png)

The relationship between core, CCX and CCDs is given on the figure below.

[![../_images/core_ccx_ccd.png](https://dci.dci-gitlab.cines.fr/webextranet/_images/core_ccx_ccd.png)](https://dci.dci-gitlab.cines.fr/webextranet/_images/core_ccx_ccd.png)

<a id="the-preprocessing-and-postprocessing-nodes-hpda"></a>

## The preprocessing and postprocessing nodes (HPDA)

The 12 preprocessing and postprocessing nodes also called High Performance Data Analytics (HPDA) are based on 2U HPE-Cray Proliant DL385 Gen11 servers with 2 AMD Genoa processors. Each processor has 96 cores @ 2.4 GHz. Each node has 2 NVIDIA L40 graphics cards attached for handling the pre/post processing workloads. Every such node has 2048 Gio of RAM configured in 16 memory channels with 2 x 64 Gio DDR5-4800 MHz memory arrays per channel. For inter-node communications, each node has 1 Slingshot 200 Gb/s network interfaces and a dual-port 10 Gb/s Ethernet card. Theses nodes will be connected to the rest of the machine via the Slingshot fabric and to the CINES facilities via Arista *edge routers* (see the [diagram above](index.md#architecture-adastra-overview)).

<a id="system-interconnect"></a>

## System interconnect

The Adastra accelerated nodes are connected with 4 HPE-Cray Slingshot 200 Gb/s (25 Go/s, 23.3 Gio/s) NICs providing a total node-injection bandwidth of 800 Gb/s (100 Go/s, 93.1 Gio/s). Thus, each MI250X accelerator is connected to a NIC to facilitate GPU-GPU Remote Direct Memory Access (RDMA). The GPUs are directly connected to HPE-Cray’s Slingshot fabric which allows MPI communications operations such as send or receive to be executed directly from the GPU memory and across the network directly without interaction with the host CPU thus, improving throughput and latency by reducing redundant copies for codes that communicates intensively with other nodes.

<a id="operating-system"></a>

## Operating system

Adastra runs on the Red Hat Enterprise Linux (RHEL) 8.8 (Ootpa) (`cat /etc/os-release`) operating system. We use the Linux 4.18.0 kernel (`uname -a`).

<a id="file-systems"></a>

## File systems

Adastra is connected to the site-wide *scratch* LUSTRE filesystem providing 1.9 Pio of storage capacity with a measured peak read speed of 1086 Gio/s. It also has access to a *home* LUSTRE filesystem which provides and also to a *work* LUSTRE filesystem to keep data between jobs and a *store* LUSTRE filesystem to keep data and programs for a longer time (between allocation). See [Accessing the storage areas](../data_storage_and_transfers/index.md#adastra-storage-and-transfer-storage-accessing) for more details.

<a id="how-many-hours-to-ask-for"></a>

## How many hours to ask for

Depending on your computation, you may be bound by the half precision, Binary32 or Binary64 floating point ALU throughput or by the HBM throughput. Below, we offer a comparison of the commonly found GPU resources as of 2024/04.

[![../_images/node_normalized_performance.png](https://dci.dci-gitlab.cines.fr/webextranet/_images/node_normalized_performance.png)](https://dci.dci-gitlab.cines.fr/webextranet/_images/node_normalized_performance.png)

For instance, we observe that a MI250X GCD’s Binary64 throughput is 23.95 TFlop/s and that it consumes 280 W. Also, for the node normalized values, we assume we can pack 8 of such MI250X GCD in one node (which is what we have on Adastra).

As another example, for the node normalized values, we observe that an A100 equipped node is offering x1.24 the bandwidth of a node equipped with MI250Xs. Also, a H100 node’s Binary16 throughput is x3.16 that of a A100 node.

From this, assuming your code is memory bound, running on V100 and that you want to run MI250X, you can expect a x1.82 node-to-node memory throughput speedup. All things being equals, if you used to ask for 100000 V100 GPU hours, you would ask for 100000/1.82~=55000 MI250X GPU hours.

**Note**

This computation does not take the DARI’s normalization factors into account as from a technical standpoint, they are debatable.

We recommend that you familiarize yourself with the concept of [Minimal viable speedup](../porting_optimization/index.md#porting-optimization-porting-to-gpu-minimal-viable-speedup). This could help you choose how to compare a CPU node versus a GPU node. This comparison is often badly done and biased toward the GPUs being much better than what they can actually provide (for a well made CPU code).
