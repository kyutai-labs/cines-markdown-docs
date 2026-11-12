<!-- Source: https://dci.dci-gitlab.cines.fr/webextranet/porting_optimization/detailed_binding_script.html -->
<!-- Title: Detailed (and more advanced) binding script -->

<a id="detailed-and-more-advanced-binding-script"></a>

<a id="porting-optimization-detailed-binding-script"></a>

# Detailed (and more advanced) binding script

This most verbose script provides many binding configurations. Each configuration is specified using a Bash function which should define the appropriate environment variables (if any), the `AFFINITY_NUMACTL` variable and optionally, in case of GPU binding, `AFFINITY_GPU`.

- `AFFINITY_NUMACTL` shall be a Bash array of string representing a range of hardware thread. Example are `0-7`, `5-5` or equivalently `5`. A rank N will be assigned the N th string of the array (modulo array size).
- `AFFINITY_GPU` shall be a `ROCR_VISIBLE_DEVICES`, `HIP_VISIBLE_DEVICES` or `CUDA_VISIBLE_DEVICES` compatible list of GPU device. A rank N will be assigned the N th string of the array (modulo array size).

The user should **always** either, **uncomment the binding variant** he wishes to use **or define** the `BINDING_VARIANT` environment variable to contain the name of the binding variant function to call. An example for the MI250X partition would look like so:

```shell
#!/bin/bash
#SBATCH --account=<account_to_charge>
#SBATCH --job-name="test_affinity"
#SBATCH --constraint=MI250
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=1:00:00

export BINDING_VARIANT="Adastra_MI250_8TasksWith8ThreadsAnd1GPU"
srun --ntasks-per-node=8 --cpu-bind=none --mem-bind=none -- ./adastra_acc_binding.sh <executable> <arguments>
```

Also, know that you could define you own binding function and export it like so:

```shell
function CustomBinding() {
    # Rank matching i % 2 = 0 gets AFFINITY_NUMACTL(0) = 0
    #               i % 2 = 1 gets AFFINITY_NUMACTL(1) = 191
    AFFINITY_NUMACTL=('0' '191')
}

export -f "CustomBinding"
export BINDING_VARIANT="CustomBinding"
```

**Note**

This script binds ranks to devices. The AMD `HSA_CU_MASK` and `ROC_GLOBAL_CU_MASK` environment variable can be tuned to [select Compute Unit (CU)](https://rocm.docs.amd.com/en/latest/how-to/setting-cus.html#setting-the-number-of-compute-units).

```shell
#!/bin/bash

set -eu

# NOTE: LOCAL_RANK: In [0, SLURM_TASKS_PER_NODE), uniquely identifies the tasks
# within a node. Under SLURM, we use SLURM_LOCALID. Depending on the batch
# scheduler, this may change.
LOCAL_RANK_INDEX="${SLURM_LOCALID}"

################################################################################
# Machine Configurations
################################################################################

########################################
# For Adastra's MI300 partition
########################################

function Adastra_MI300_4TasksWith24ThreadsAnd1GPU() {
    # Node local rank 0 gets GCD 0, is bound to cores [0-23] of NUMA domain 0, and uses NIC 0
    # Node local rank 1 gets GCD 1, is bound to cores [24-47] of NUMA domain 1, and uses NIC 1
    # Node local rank 2 gets GCD 2, is bound to cores [48-71] of NUMA domain 2, and uses NIC 2
    # Node local rank 3 gets GCD 3, is bound to cores [72-95] of NUMA domain 3, and uses NIC 3
    AFFINITY_NUMACTL=('0-23' '24-47' '48-71' '72-95')
    AFFINITY_GPU=('0' '1' '2' '3')
}

function Adastra_MI300_4TasksWith48ThreadsAnd1GPU() {
    AFFINITY_NUMACTL=('0-23,96-119' '24-47,120-143' '48-71,144-167' '72-95,168-191')
    AFFINITY_GPU=('0' '1' '2' '3')
}

########################################
# For Adastra's MI250 partition
########################################

function Adastra_MI250_4TasksWith32ThreadsAnd2GPU() {
    # Requires SMT to be enabled.
    AFFINITY_NUMACTL=('48-63,112-127' '16-31,80-95' '0-15,64-79' '32-39,96-103,40-47,104-111')
    AFFINITY_GPU=('0,1' '2,3' '4,5' '6,7')
}

function Adastra_MI250_8TasksWith8ThreadsAnd1GPU() {
    # Node local rank 0 gets GCD 0, is bound to cores [48-55] of NUMA domain 3, and uses NIC 0
    # Node local rank 1 gets GCD 1, is bound to cores [56-63] of NUMA domain 3, and uses NIC 0
    # Node local rank 2 gets GCD 2, is bound to cores [16-23] of NUMA domain 1, and uses NIC 1
    # Node local rank 3 gets GCD 3, is bound to cores [24-31] of NUMA domain 1, and uses NIC 1
    # Node local rank 4 gets GCD 4, is bound to cores [0-7] of NUMA domain 0, and uses NIC 2
    # Node local rank 5 gets GCD 5, is bound to cores [8-15] of NUMA domain 0, and uses NIC 2
    # Node local rank 6 gets GCD 6, is bound to cores [32-39] of NUMA domain 2, and uses NIC 3
    # Node local rank 7 gets GCD 7, is bound to cores [40-47] of NUMA domain 2, and uses NIC 3
    AFFINITY_NUMACTL=('48-55' '56-63' '16-23' '24-31' '0-7' '8-15' '32-39' '40-47')
    AFFINITY_GPU=('0' '1' '2' '3' '4' '5' '6' '7')
}

function Adastra_MI250_8TasksWith16ThreadsAnd1GPU() {
    # Requires SMT to be enabled.
    AFFINITY_NUMACTL=('48-55,112-119' '56-63,120-127' '16-23,80-87' '24-31,88-95' '0-7,64-71' '8-15,72-79' '32-39,96-103' '40-47,104-111')
    AFFINITY_GPU=('0' '1' '2' '3' '4' '5' '6' '7')
}

function Adastra_MI250_16TasksWith8ThreadsAnd1GPU() {
    # Requires SMT to be enabled.
    AFFINITY_NUMACTL=('48-51,112-115' '52-55,116-119' '56-59,120-123' '60-63,124-127' '16-19,80-83' '20-23,84-87' '24-27,88-91' '28-31,92-95' '0-3,64-67' '4-7,68-71' '8-11,72-75' '12-15,76-79' '32-35,96-99' '36-39,100-103' '40-43,104-107' '44-47,108-111')
    AFFINITY_GPU=('0' '0' '1' '1' '2' '2' '3' '3' '4' '4' '5' '5' '6' '6' '7' '7')
}

########################################
# For Adastra's GENOA partition
########################################

function Adastra_GENOA_192TasksWith1Core() {
    AFFINITY_NUMACTL=('0' '1' '2' '3' '4' '5' '6' '7' '8' '9' '10' '11' '12' '13' '14' '15' '16' '17' '18' '19' '20' '21' '22' '23' '24' '25' '26' '27' '28' '29' '30' '31' '32' '33' '34' '35' '36' '37' '38' '39' '40' '41' '42' '43' '44' '45' '46' '47' '48' '49' '50' '51' '52' '53' '54' '55' '56' '57' '58' '59' '60' '61' '62' '63' '64' '65' '66' '67' '68' '69' '70' '71' '72' '73' '74' '75' '76' '77' '78' '79' '80' '81' '82' '83' '84' '85' '86' '87' '88' '89' '90' '91' '92' '93' '94' '95' '96' '97' '98' '99' '100' '101' '102' '103' '104' '105' '106' '107' '108' '109' '110' '111' '112' '113' '114' '115' '116' '117' '118' '119' '120' '121' '122' '123' '124' '125' '126' '127' '128' '129' '130' '131' '132' '133' '134' '135' '136' '137' '138' '139' '140' '141' '142' '143' '144' '145' '146' '147' '148' '149' '150' '151' '152' '153' '154' '155' '156' '157' '158' '159' '160' '161' '162' '163' '164' '165' '166' '167' '168' '169' '170' '171' '172' '173' '174' '175' '176' '177' '178' '179' '180' '181' '182' '183' '184' '185' '186' '187' '188' '189' '190' '191')
}

function Adastra_GENOA_384TasksWith1Thread() {
    AFFINITY_NUMACTL=('0' '1' '2' '3' '4' '5' '6' '7' '8' '9' '10' '11' '12' '13' '14' '15' '16' '17' '18' '19' '20' '21' '22' '23' '24' '25' '26' '27' '28' '29' '30' '31' '32' '33' '34' '35' '36' '37' '38' '39' '40' '41' '42' '43' '44' '45' '46' '47' '48' '49' '50' '51' '52' '53' '54' '55' '56' '57' '58' '59' '60' '61' '62' '63' '64' '65' '66' '67' '68' '69' '70' '71' '72' '73' '74' '75' '76' '77' '78' '79' '80' '81' '82' '83' '84' '85' '86' '87' '88' '89' '90' '91' '92' '93' '94' '95' '96' '97' '98' '99' '100' '101' '102' '103' '104' '105' '106' '107' '108' '109' '110' '111' '112' '113' '114' '115' '116' '117' '118' '119' '120' '121' '122' '123' '124' '125' '126' '127' '128' '129' '130' '131' '132' '133' '134' '135' '136' '137' '138' '139' '140' '141' '142' '143' '144' '145' '146' '147' '148' '149' '150' '151' '152' '153' '154' '155' '156' '157' '158' '159' '160' '161' '162' '163' '164' '165' '166' '167' '168' '169' '170' '171' '172' '173' '174' '175' '176' '177' '178' '179' '180' '181' '182' '183' '184' '185' '186' '187' '188' '189' '190' '191' '192' '193' '194' '195' '196' '197' '198' '199' '200' '201' '202' '203' '204' '205' '206' '207' '208' '209' '210' '211' '212' '213' '214' '215' '216' '217' '218' '219' '220' '221' '222' '223' '224' '225' '226' '227' '228' '229' '230' '231' '232' '233' '234' '235' '236' '237' '238' '239' '240' '241' '242' '243' '244' '245' '246' '247' '248' '249' '250' '251' '252' '253' '254' '255' '256' '257' '258' '259' '260' '261' '262' '263' '264' '265' '266' '267' '268' '269' '270' '271' '272' '273' '274' '275' '276' '277' '278' '279' '280' '281' '282' '283' '284' '285' '286' '287' '288' '289' '290' '291' '292' '293' '294' '295' '296' '297' '298' '299' '300' '301' '302' '303' '304' '305' '306' '307' '308' '309' '310' '311' '312' '313' '314' '315' '316' '317' '318' '319' '320' '321' '322' '323' '324' '325' '326' '327' '328' '329' '330' '331' '332' '333' '334' '335' '336' '337' '338' '339' '340' '341' '342' '343' '344' '345' '346' '347' '348' '349' '350' '351' '352' '353' '354' '355' '356' '357' '358' '359' '360' '361' '362' '363' '364' '365' '366' '367' '368' '369' '370' '371' '372' '373' '374' '375' '376' '377' '378' '379' '380' '381' '382' '383')
}

function Adastra_GENOA_8TasksWith6ThreadsSparseOnL3() {
    AFFINITY_NUMACTL=('0-1,8-9,16-17' '24-25,32-33,40-41' '48-49,56-57,64-65' '72-73,80-81,88-89' '96-97,104-105,112-113' '120-121,128-129,136-137' '144-145,152-153,160-161' '168-169,176-177,184-185')
}

function Adastra_GENOA_8TasksWith6ThreadsDenseOnL3() {
    AFFINITY_NUMACTL=('0-5' '24-29' '48-53' '72-77' '96-101' '120-125' '144-149' '168-173')
}

function Adastra_GENOA_8TasksWith24Threads() {
    AFFINITY_NUMACTL=('0-23' '24-47' '48-71' '72-95' '96-119' '120-143' '144-167' '168-191')
}

function Adastra_GENOA_16TasksWith12Threads() {
    AFFINITY_NUMACTL=('0-11' '12-23' '24-35' '36-47' '48-59' '60-71' '72-83' '84-95' '96-107' '108-119' '120-131' '132-143' '144-155' '156-167' '168-179' '180-191')
}

function Adastra_GENOA_24TasksWith8Threads() {
    AFFINITY_NUMACTL=('0-7' '8-15' '16-23' '24-31' '32-39' '40-47' '48-55' '56-63' '64-71' '72-79' '80-87' '88-95' '96-103' '104-111' '112-119' '120-127' '128-135' '136-143' '144-151' '152-159' '160-167' '168-175' '176-183' '184-191')
}

function Adastra_GENOA_24TasksWith16Threads() {
    # Requires SMT to be enabled.
    AFFINITY_NUMACTL=('0-7,192-199' '8-15,200-207' '16-23,208-215' '24-31,216-223' '32-39,224-231' '40-47,232-239' '48-55,240-247' '56-63,248-255' '64-71,256-263' '72-79,264-271' '80-87,272-279' '88-95,280-287' '96-103,288-295' '104-111,296-303' '112-119,304-311' '120-127,312-319' '128-135,320-327' '136-143,328-335' '144-151,336-343' '152-159,344-351' '160-167,352-359' '168-175,360-367' '176-183,368-375' '184-191,376-383')
}

function Adastra_GENOA_32TasksWith4Threads() {
    AFFINITY_NUMACTL=('0-3' '4-7' '8-11' '16-19' '24-27' '28-31' '32-35' '40-43' '48-51' '52-55' '56-59' '64-67' '72-75' '76-79' '80-83' '88-91' '96-99' '100-103' '104-107' '112-115' '120-123' '124-127' '128-131' '136-139' '144-147' '148-151' '152-155' '160-163' '168-171' '172-175' '176-179' '184-187')
}

function Adastra_GENOA_32TasksWith6Threads() {
    AFFINITY_NUMACTL=('0-5' '6-11' '12-17' '18-23' '24-29' '30-35' '36-41' '42-47' '48-53' '54-59' '60-65' '66-71' '72-77' '78-83' '84-89' '90-95' '96-101' '102-107' '108-113' '114-119' '120-125' '126-131' '132-137' '138-143' '144-149' '150-155' '156-161' '162-167' '168-173' '174-179' '180-185' '186-191')
}

function Adastra_GENOA_48TasksWith4Threads() {
    AFFINITY_NUMACTL=('0-3' '4-7' '8-11' '12-15' '16-19' '20-23' '24-27' '28-31' '32-35' '36-39' '40-43' '44-47' '48-51' '52-55' '56-59' '60-63' '64-67' '68-71' '72-75' '76-79' '80-83' '84-87' '88-91' '92-95' '96-99' '100-103' '104-107' '108-111' '112-115' '116-119' '120-123' '124-127' '128-131' '132-135' '136-139' '140-143' '144-147' '148-151' '152-155' '156-159' '160-163' '164-167' '168-171' '172-175' '176-179' '180-183' '184-187' '188-191')
}

########################################
# For any node with CPUs
########################################

function Adastra_Oversubscribe() {
    LOCAL_RANK_COUNT="${SLURM_NTASKS_PER_NODE}"
    LOCAL_THREAD_COUNT="$(lscpu | grep "^CPU(s):" | awk '{print $2}')"
    LOCAL_THREAD_PER_CORE="$(lscpu | grep "^Thread(s) per core:" | awk '{print $4}')"
    LOCAL_CORE_COUNT="$((LOCAL_THREAD_COUNT / LOCAL_THREAD_PER_CORE))"
    CORE_PER_RANK="$((LOCAL_CORE_COUNT / LOCAL_RANK_COUNT))"
    if [[ "$((CORE_PER_RANK * LOCAL_RANK_COUNT))" -ne "${LOCAL_CORE_COUNT}" ]]; then
        echo "Your rank count per node does not map evenly to the hardware."
        exit 1
    fi
    MAIN_CORE=$((LOCAL_RANK_INDEX * CORE_PER_RANK))
    # The user can export the variable. It must be less than or equal to
    # CORE_PER_RANK. PRIVATE_CORE_COUNT=1
    if [[ "${PRIVATE_CORE_COUNT}" -gt "${CORE_PER_RANK}" ]]; then
        echo "Too many private cores: ${PRIVATE_CORE_COUNT} > ${CORE_PER_RANK}."
        exit 1
    fi
    if [[ "${PRIVATE_CORE_COUNT}" -lt "0" ]]; then
        # If < 0, assume the user wants spreading but no oversubscribing.
        PRIVATE_CORE_COUNT="${CORE_PER_RANK}"
    fi
    # The first N cores are given to only one rank.
    AFFINITY_NUMACTL="${MAIN_CORE}-$((MAIN_CORE + CORE_PER_RANK - 1))"
    AFFINITY_THREAD="{${MAIN_CORE}}$(seq -f ",{%g}" -s '' "$((MAIN_CORE + 1))" "$((MAIN_CORE + CORE_PER_RANK - 1))")"
    if [[ "${PRIVATE_CORE_COUNT}" -lt "${CORE_PER_RANK}" ]]; then
        for ((A_RANK_INDEX = 0; A_RANK_INDEX < LOCAL_RANK_COUNT; ++A_RANK_INDEX)); do
            # Offset
            CURRENT_RANK="$(((LOCAL_RANK_INDEX + A_RANK_INDEX) % LOCAL_RANK_COUNT))"
            if [[ "${CURRENT_RANK}" == "${LOCAL_RANK_INDEX}" ]]; then
                continue
            fi
            CURRENT_CORE="$((CURRENT_RANK * CORE_PER_RANK))"
            AFFINITY_NUMACTL+=",$((CURRENT_CORE + PRIVATE_CORE_COUNT))-$((CURRENT_CORE + CORE_PER_RANK - 1))"
            AFFINITY_THREAD+="$(seq -f ",{%g}" -s '' "$((CURRENT_CORE + PRIVATE_CORE_COUNT))" "$((CURRENT_CORE + CORE_PER_RANK - 1))")"
        done
    fi
    AFFINITY_NUMACTL=("${AFFINITY_NUMACTL}")
    export OMP_NUM_THREADS="$((CORE_PER_RANK + (LOCAL_RANK_COUNT - 1) * (CORE_PER_RANK - PRIVATE_CORE_COUNT)))"
    export OMP_PLACES="${AFFINITY_THREAD}"
    # export OMP_PLACES="THREADS"
    export OMP_PROC_BIND="CLOSE"
}

# NOTE: We default to NIC on safe NUMA binding.
export MPICH_OFI_NIC_POLICY="NUMA"
# NOTE: HW thread binding to process is powerful, but we also need to enforce
# software thread pinning to HW thread. This is done from the POV of a thread,
# and using OpenMP, it can be done like so:
export OMP_PROC_BIND="TRUE"

################################################################################
# Uncomment one of the following to set your binding variant:
# Adastra_MI300_4TasksWith24ThreadsAnd1GPU
# Adastra_MI250_8TasksWith8ThreadsAnd1GPU
# Adastra_MI250_8TasksWith16ThreadsAnd1GPU
# Adastra_MI250_16TasksWith8ThreadsAnd1GPU
# Adastra_GENOA_8TasksWith6ThreadsSparseOnL3
# Adastra_GENOA_8TasksWith6ThreadsDenseOnL3
# Adastra_GENOA_8TasksWith24Threads
# Adastra_GENOA_16TasksWith12Threads
# Adastra_GENOA_24TasksWith8Threads
# Adastra_GENOA_32TasksWith4Threads
# Adastra_GENOA_32TasksWith6Threads
# Adastra_GENOA_48TasksWith4Threads
# Adastra_Oversubscribe
#
# Alternatively, define your binding variant in the parent script via the
# "BINDING_VARIANT" environment variable:
#   $ export BINDING_VARIANT="Adastra_GENOA_192TasksWith1Core"
#   $ # Or, first Adastra_MI250_8TasksWith8ThreadsAnd1GPU then overwrite
#   $ export BINDING_VARIANT="Adastra_MI250_8TasksWith8ThreadsAnd1GPU;Adastra_Oversubscribe;"
eval "${BINDING_VARIANT}"

################################################################################
# Modulo arithmetic eases some corner use cases.
CPU_SET="${AFFINITY_NUMACTL[$((${LOCAL_RANK_INDEX} % ${#AFFINITY_NUMACTL[@]}))]}"
if [ ! -z ${AFFINITY_GPU+x} ]; then
    # Modulo arithmetic eases some corner use cases.
    GPU_SET="${AFFINITY_GPU[$((${LOCAL_RANK_INDEX} % ${#AFFINITY_GPU[@]}))]}"
    # For a CPU-only process, these environment variables are a NOOP.
    export ROCR_VISIBLE_DEVICES="${GPU_SET}"
fi
# echo "Starting local rank: ${LOCAL_RANK_INDEX} with: 'numactl --localalloc --physcpubind=${CPU_SET} --'"
# NOTE: We use numactl, but OpenMP, taskset, or hw-bind are alternatives.
exec numactl --localalloc --physcpubind="${CPU_SET}" -- "${@}"
```

<a id="significance-of-nic-binding"></a>

# Significance of NIC binding

If you take a look at [Adastra accelerated (MI250X) nodes](../architecture/index.md#architecture-adastra-accelerated-nodes) architecture diagram, you will notice that the Network Interface Card (NIC) indexing is not intuitive. On multi NIC nodes, proper binding is necessary to correctly bind a rank to it’s closest NIC. Not using the closest NIC will expose you to performance degradation on the order of 5% to 10%.

```shell-session
# Bad (wrong NIC):
$ MPICH_OFI_NIC_VERBOSE=2                                             srun --nodes=2 --ntasks-per-node=8 --cpus-per-task=16 --gpus-per-task=1 --gpu-bind=closest -- ~/bin/hellogpubinding

PE 0: Host g1067 selected NIC index=0, domain_name=cxi0, numa_node=3, address=[0x28e2]
PE 1: Host g1067 selected NIC index=0, domain_name=cxi0, numa_node=3, address=[0x28e2]
PE 2: Host g1067 selected NIC index=1, domain_name=cxi1, numa_node=1, address=[0x28e3]
PE 3: Host g1067 selected NIC index=1, domain_name=cxi1, numa_node=1, address=[0x28e3]
PE 4: Host g1067 selected NIC index=2, domain_name=cxi2, numa_node=0, address=[0x28a3]
PE 5: Host g1067 selected NIC index=2, domain_name=cxi2, numa_node=0, address=[0x28a3]
PE 6: Host g1067 selected NIC index=3, domain_name=cxi3, numa_node=2, address=[0x28a2]
PE 7: Host g1067 selected NIC index=3, domain_name=cxi3, numa_node=2, address=[0x28a2]

PE 8: Host g1068 selected NIC index=0, domain_name=cxi0, numa_node=3, address=[0x2870]
PE 9: Host g1068 selected NIC index=0, domain_name=cxi0, numa_node=3, address=[0x2870]
PE 10: Host g1068 selected NIC index=1, domain_name=cxi1, numa_node=1, address=[0x2871]
PE 11: Host g1068 selected NIC index=1, domain_name=cxi1, numa_node=1, address=[0x2871]
PE 12: Host g1068 selected NIC index=2, domain_name=cxi2, numa_node=0, address=[0x2831]
PE 13: Host g1068 selected NIC index=2, domain_name=cxi2, numa_node=0, address=[0x2831]
PE 14: Host g1068 selected NIC index=3, domain_name=cxi3, numa_node=2, address=[0x2830]
PE 15: Host g1068 selected NIC index=3, domain_name=cxi3, numa_node=2, address=[0x2830]

# Good (correct NIC):
$ MPICH_OFI_NIC_VERBOSE=2 MPICH_OFI_NIC_POLICY="NUMA" OMP_NUM_THREADS=1 srun --nodes=2 --ntasks-per-node=8 --cpus-per-task=16 --gpus-per-task=1 --gpu-bind=closest -- ~/bin/hellogpubinding

PE 0: Host g1067 selected NIC index=2, domain_name=cxi2, numa_node=0, address=[0x28a3]
PE 1: Host g1067 selected NIC index=2, domain_name=cxi2, numa_node=0, address=[0x28a3]
PE 2: Host g1067 selected NIC index=1, domain_name=cxi1, numa_node=1, address=[0x28e3]
PE 3: Host g1067 selected NIC index=1, domain_name=cxi1, numa_node=1, address=[0x28e3]
PE 4: Host g1067 selected NIC index=3, domain_name=cxi3, numa_node=2, address=[0x28a2]
PE 5: Host g1067 selected NIC index=3, domain_name=cxi3, numa_node=2, address=[0x28a2]
PE 6: Host g1067 selected NIC index=0, domain_name=cxi0, numa_node=3, address=[0x28e2]
PE 7: Host g1067 selected NIC index=0, domain_name=cxi0, numa_node=3, address=[0x28e2]

PE 8: Host g1068 selected NIC index=2, domain_name=cxi2, numa_node=0, address=[0x2831]
PE 9: Host g1068 selected NIC index=2, domain_name=cxi2, numa_node=0, address=[0x2831]
PE 10: Host g1068 selected NIC index=1, domain_name=cxi1, numa_node=1, address=[0x2871]
PE 11: Host g1068 selected NIC index=1, domain_name=cxi1, numa_node=1, address=[0x2871]
PE 12: Host g1068 selected NIC index=3, domain_name=cxi3, numa_node=2, address=[0x2830]
PE 13: Host g1068 selected NIC index=3, domain_name=cxi3, numa_node=2, address=[0x2830]
PE 14: Host g1068 selected NIC index=0, domain_name=cxi0, numa_node=3, address=[0x2870]
PE 15: Host g1068 selected NIC index=0, domain_name=cxi0, numa_node=3, address=[0x2870]
```
