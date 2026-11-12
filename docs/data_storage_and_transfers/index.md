<!-- Source: https://dci.dci-gitlab.cines.fr/webextranet/data_storage_and_transfers/index.html -->
<!-- Title: Data storage and transfers -->

<a id="data-storage-and-transfers"></a>

<a id="adastra-storage-and-transfer"></a>

# Data storage and transfers

<a id="data-and-storage"></a>

## Data and storage

<a id="accessing-the-storage-areas"></a>

<a id="adastra-storage-and-transfer-storage-accessing"></a>

### Accessing the storage areas

Every storage area of Adastra is based on the [LUSTRE filesystem](https://en.wikipedia.org/wiki/Lustre_(file_system)).

On Adastra, we distinguish four main storage areas:

- **Home** Long-term data (with a need for backups for the project’s duration ~ 12 months); for **scripts and tools** related to a project.
- **Scratch** Short-term data (<= 30 days); for **fast**, batch-job access. **Purged** based on the age of the file (see below).
- **Work** Mid-term data (few months); to store data one wishes to **postprocess**.
- **Store** Long-term data (with a need for cold storage and backups); to keep in a **secure** manner.

The table below shows the environment variable set by the [Login unique](../user_support/index.md#adastra-accessing-unique-login) tool and gives additional details regarding the characteristics of the storage area.

| Area | Sub-area | Paths or environment variables | Permissions | Default space quota ([Gio/Tio](https://en.wikipedia.org/wiki/Octet_(computing)) [[3]](index.md#f3)) | Default inode quota | Backups | Purged | Retention | Via compute nodes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Home | Personal | `/home/<login>`, `${OWN_HOMEDIR}` or `${OWN_CCFRHOME}` | umask 0022  u=rwx  g=rx  o=rx | 20 Gio | 30000 | Yes (bacula) | Never | > 6 months | Read-write |
| Project personal | `~`, `${HOME}`, `${HOMEDIR}` or `${CCFRHOME}` | 100 Gio | 300000 |
| Project shared | `${SHAREDHOMEDIR}` or `${ALL_CCFRHOME}` |
| Store | Project personal | `${STOREDIR}` or `${CCFRSTORE}` [[2]](index.md#f2) | 1.5 Tio [[4]](index.md#f4) | 9000 | Yes (HSM) | **Not** mounted |
| Scratch | Project personal | `${SCRATCHDIR}` or `${CCFRSCRATCH}` | 20 Tio | 1000000 | No | Yes (30 days) [[1]](index.md#f1) | Read-write |
| Project shared | `${SHAREDSCRATCHDIR}` or `${ALL_CCFRSCRATCH}` |
| Work | Project personal | `${WORKDIR}` or `${CCFRWORK}` | 15 Tio | 250000 | Never |
| Project shared | `${SHAREDWORKDIR}` or `${ALL_CCFRWORK}` |

**Area** - The general name of the storage area.

**Sub-area** - Disk space reserved for a specific usage.

**Environment variable** - The shell environment variable one should use to access the storage resource.

**Permissions** - Default permission (`umask`).

**Space quota** - The maximum total number of bytes in your storage area (be careful with Go and Gio).

**Inode quota** - The maximum total number of inodes (which one could approximate as files) in your storage area.

**Backups** - States if the data is automatically duplicated for disaster recovery purposes.

**Purged** - Period of time, post-file-access, after which a file will be marked as eligible for permanent deletion.

**Retention** - Period of time, post-account-deactivation or post-project-end, after which data will be marked as eligible for permanent deletion.

**Via compute nodes** - In which way the filesystem can be accessed.

Footnotes

[[1](index.md#id4)]

This implies there is no data retention policies.

[[2](index.md#id2)]

CINES does not support the `${ALL_CCFRSTORE}` environment variable.

[[3](index.md#id1)]

When you run the `ls -alh` command, it gives you the size of the files in Kio/Mio/Gio etc.. We give the quota in this same unit. Take care of the [differences between Go/GB and Gio/GiB](https://en.wikipedia.org/wiki/Octet_(computing)).

[[4](index.md#id3)]

We offer a small *store* area quota, enough for most users. See the [Quotas](index.md#adastra-storage-and-transfer-policies-data-quota) subsection for more details on how to increase it.

**Warning**

Quota are **always** defined *per group* except for the **personal** *home*. This means that wether you are 2 or 10 in a GENCI/DARI project, you get the same amount of space. Contact [svp@cines.fr](mailto:svp%40cines.fr) to ask for a quota reevaluation.

**Note**

The `CCFR` and `ALL_CCFR` prefixed variables, while being a bit of misnomer, have the benefit of being available (same name) on all three of the french computing sites while also carrying a similar meaning.

**Important**

Files within the *scratch* area are **not** backed up and are **purged** on a regular basis.

**Important**

Storage areas have their own specific use, try to respect the usage concept of the area. The *store* space may have long latencies thus it is not intended to be used during computations, actually, **store is not available on compute nodes**.

We now describe the specificities of a *personal*, *project personal* and *project shared* sub-area.

- **Personal** or simply, **non project** related - Thanks to the *unique login* functionalities you can *work* on multiple projects through a single user account. This account has a dedicated *home* (`${OWN_HOMEDIR}`), the only strictly personal area which is not shared with other users nor specific to a project. It has its **own quota counters**. This is the *home* you see when doing an `scp` and also the one which contains the `.Xauthority` file. Note that the `${HOME}` environment variable should never be set to point to this personal *home* by the *unique login* tool **unless** the user does not have a project.
- **Project personal** - A user account is attached to a project and is given a personal area using the **project’s quota counters**. You can change where this environment variable points to when manipulating the *unique login* tool.
- **Project shared** - To ease data movements between users of a same project (say, avoid UNIX permissions issues), the **project shared** sub-area can be used. It shares the same quota counters as the **project personal** sub-area. You can change where this environment variable points to when manipulating the *unique login* tool.

We also give the user a way to exchange data between projects via an inter-project **work** sub-area.

**Note**

**Project personal** and **Project shared** have a similar meaning to what used to exist on Occigen (CINES’ previous machine).

**Note**

If an user is not linked to any project, its `${HOMEDIR}` will point to its personal *home*.

**Note**

You may find complementary information in [Layout of common files and directories](../user_support/index.md#adastra-file-layout).

**Warning**

Be careful of what ends up in your **personal** *home* instead of your **project personal** *home*. For instance your `.ssh` is expected by some tools to be in your **personal** *home* directory. You can work around these issues using links via the `ln -s` command.

<a id="additional-storage-characteristics"></a>

<a id="adastra-storage-and-transfer-storage-space-acronyms"></a>

### Additional storage characteristics

Some more advanced technical details are given in two tables below:

| Mount point | MDT count | OST count | Cumulated OST space | SSD backed | Maximal practical throughput (read / write) in Gio/s |
| --- | --- | --- | --- | --- | --- |
| `/lus/home` | 2 | 2 | 125 Tio | OST/MDT | 77 / 34 |
| `/lus/scratch` | 2 | 40 (4 backup) | 1.9 Pio | OST/MDT | 1310 / 786 |
| `/lus/store` | 2 | 16 | 9.1 Pio | MDT | - |
| `/lus/work` | 2 | 24 | 13.6 Pio | MDT | 175 / ~100 |

The acronyms exposed in the table above are LUSTRE slang and defined in the table below. It’s largely optional to the typical user to know any of them.

| Name | Acronym | Meaning |
| --- | --- | --- |
| MetaData | MD | Data attached to a file a POSIX file system should expose (say rights, date, etc.). |
| Object Storage | OS | Object Storage is used to store the data contained in a file (if any or if large enough). |
| MD Server | MDS | Handle and distributes the requests to the MDT. |
| OS Server | OSS | Handle and distributes the read, write, etc. requests to the OST. |
| MD Target | MDT | Block device used to store MetaData. |
| OS Target | OST | Block device representing the Object Storage. |
| MD Client | MDC | Queries the MDS. |
| OS Client | OSC | Queries the OSS. |

The *store* area exposes a LUSTRE filesystem with a [Hierarchical Storage Management (HSM)](https://en.wikipedia.org/wiki/Hierarchical_storage_management) functionality. This HSM filesystem means that long left untouched data might migrate on tapes for long term storage. Accessing this long term stored data (on tapes), will take a long time.

<a id="data-storage-good-practices"></a>

### Data storage good practices

<a id="user-home-directories"></a>

#### User *home* directories

Users should note that the *home* performance will not be as high as the *scratch* filesystem.

<a id="permissions"></a>

#### Permissions

Users have the ability to change permissions on their *home* directories. It is recommended that permissions be set to be as restrictive as possible (without interfering with your work).

<a id="lustre-specific-lfs-find-command"></a>

#### Lustre-specific lfs find command

When looking for a file, instead of using the traditional `find` command, prefer the `lfs find` variant.

Somme example are given below:

```shell-session
$ lfs find ./ -type f -print
.//.python_history-69887.tmp
$ ls -la ./.python_history-69887.tmp
-rw-------. 1 user dci 124 Dec 13 16:26 ./.python_history-69887.tmp
$ lfs find ./ -type f -size +1M -print
```

<a id="lustre-file-striping"></a>

#### LUSTRE file striping

Supposing one care about performing IO (read/write) operations (say via MPI-IO, HDF5 parallel, NetCDF parallel, *tarballing*, etc.) on large files and at high throughput, then, one should consider striping his files. This operation will spread the data and the load across multiple drives (Object Storage Target in LUSTRE’s terminology) which can then be used in parallel. A file is then described as *striped*. This *striping* is transparent to the user. So if you have multiple threads or ranks accessing the same file at different offsets, they may in fact access data on different drives. Once defined, the striping is transparent to the user, the benefits are provided by the filesystem.

This is how you obtain the number of stripes on a `<directory/file>` and set the stripe count for all the **upcoming new files** in a `<directory>` to be equal the number of available OST (note the `--stripe-count -1`):

```shell-session
$ lfs getstripe <directory/file>
$ lfs setstripe --stripe-count <stripe-count> --stripe-index <starting-OST-index> --stripe-size <stripe-size> <directory>
```

Where the some `<stripe-count>` are given in the table below, `<starting-OST-index>` is highly recommended to be `-1` and `<stripe-size>` is highly recommended to be `1M` or `2M`.

**You should stripe your directories before creating files inside it**. Else you wont benefit from the feature. Some recommended stripe count are given below as a function of the file’s size:

| File size in Gio | Recommended stripe count |
| --- | --- |
| [0, 1) | 1 |
| [1, 8) | 8 |
| [8-128) | 24 |
| [128-infinity) | 24+ |

The above table can be represented in one command which the user is recommended to use on his simulation result folder:

```shell-session
$ lfs setstripe -E 1G --stripe-count  1 \
                -E 8G --stripe-count  8 \
                -E -1 --stripe-count 24 \
                <directory>
```

**Note**

Enabling striping on small files **may degrade performance**.

**Note**

Striping over all the OSTs **may not lead to the best performance**, so you may want to adjust the stripe count downward. Also, if your code assumes one or more file per process and the IOs of a process does not extend past its *own files*, we do not recommend stripping but only making sure the files will be spread all the OSTs (default behavior). Indeed the files will already reside on multiple OSTs and stripping would only add overhead (again, assuming all the processes read or write at the same time).

<a id="other"></a>

#### Other

> - Before copying data to the *store*, make **sure** you compact your data in, say, a [tarball](https://en.wikipedia.org/wiki/Tar_(computing)). This will reduce your data store and retrieval times (only big files are suited for HSM);
> - The *scratch* area is a **temporary** storage, move the important files produced by jobs on one of the other areas (*work* or *store*);
> - Repatriate your files to a remote site (i.e., your lab) using, say `scp`, `rsync`, etc. see [Tools to transfer Data](index.md#adastra-storage-and-transfer-transfer-tools) for more details;
> - Delete unnecessary files;
> - Prefer `lfs find` over `find` and `lfs df` over `df`.

**Note**

Compressing your data (say, *gzip*’ing it) in *store* is not necessary as the **HSM will do it for you**. That being said, your file sizes wont appear smaller like what you would expect after compression, that is because the compression is transparent to the user (that is, there are few visible artifacts). We would prefer the user to ask for more *store* quota rather than he compresses his data himself. If user compression is not recommended, packing your data (say, in a tarball) in as few file as possible is **good practice** and will largely decrease the retrieval time of old files. If you need more *store* area quota ask [svp@cines.fr](mailto:svp%40cines.fr).

<a id="datasets"></a>

<a id="adastra-storage-and-transfer-storage-datasets"></a>

### Datasets

In order to avoid duplication of datasets, CINES provides the `${DSDIR}` environment variable. If you do not find a dataset in what we currently provide, you You can ask [svp@cines.fr](mailto:svp%40cines.fr) to add it to the set.

You list the dataset provided, simply do:

```shell-session
$ ls -- "${DSDIR}"
AlphaFold-2.3.1  cc12m  coco       GQA         kinetics  nuscenes  ONCE      openimage  sbu      visual_genome
AudioSet         cc3m   freesound  ImageNet1k  MSRVTT    once      ONCE.tar  pile       VideoCC  WebVid
```

**Note**

The list above is subject to change. Notably, we will add new datasets.

<a id="data-policies"></a>

## Data policies

<a id="quotas"></a>

<a id="adastra-storage-and-transfer-policies-data-quota"></a>

### Quotas

You can check your quota usage for the current project via the `myproject -s <project_identifier>` commands. To show the state of all your projects, use `myproject -S`.

If you need an exception to the limits listed in the table above, such as temporary higher quotas in your *home*, *work*, *scratch* and *store* areas or a delay before a purge, contact [svp@cines.fr](mailto:svp%40cines.fr) with a summary of the exception that you need.

In case you start getting close to the hard quota, you should be notified via email. If you try to go past your inode or block quota you will receive an error message similar to:

```
Disk quota exceeded
```

If you do not whish to use the CINES specific `myproject` command, you can use `lfs quota` like so:

```shell-session
$ lfs quota -gh -- "grp_${USER}" "${HOMEDIR}"
$ lfs quota -gh -- "grp_${USER}" "${WORKDIR}"
$ lfs quota -gh -- "grp_${USER}" "${SCRATCHDIR}"
$ lfs quota -gh -- "grp_${USER}" "${STOREDIR}"
```

**Note**

We do not guarantee that the above (`lfs quota`) commands will always work. You should prefer `myproject`.

<a id="purge"></a>

<a id="adastra-storage-and-transfer-policies-data-purge"></a>

### Purge

To keep enough space for big jobs on the *scratch* file system, files that have not been accessed (i.e., read) or modified in the project and user areas are purged at the intervals shown in the [Accessing the storage areas](index.md#adastra-storage-and-transfer-storage-accessing) above. Please make sure that valuable data are moved off the *scratch* file system regularly.

**Note**

When the data is deleted due to the purging process, the directories are not removed.

<a id="data-retention"></a>

### Data retention

After a user account deactivation or when a project ends, the user and project data in non-purged areas will be retained for 6 months. After this time frame, CINES has the reserved right to delete the data. Data in purged areas remain subject to normal purge policies.

<a id="retrieving-from-backups"></a>

### Retrieving from backups

If you accidentally delete files from your *home* or *store* directory, you may be able to retrieve them. Online backups are performed at regular intervals. **Daily backups for the last 10 days**. You can ask [svp@cines.fr](mailto:svp%40cines.fr) to retrieve your lost files.

<a id="archives-on-store"></a>

### Archives on STORE

It is **highly recommended** that you save your data in **archive format** on the *store* filesystem. The *store* filesystem uses Lustre and HSM technologies. Data is migrated to tapes, which are have highly inefficient meta data handling and are thus sensitive to the number of file. To improve the archiving and restoration process from these tapes, please store your data in an archive format such as `tar`. For instance, use the command :

```shell-session
tar -cvf "${STOREDIR}/<mydir>.tar" "<mydir>"
```

<a id="data-transfer"></a>

## Data transfer

<a id="between-adastra-filesystems"></a>

### Between Adastra filesystems

`wdcp` is a tool based on [mpiFileUtils](https://mpifileutils.readthedocs.io/) that allows you to copy a directory using a dedicated node kind called *transfer node*.

<a id="between-cines-and-your-laboratory"></a>

### Between CINES and your laboratory

Taking into account the note just above means that you must **initiate** the data transfer from your laboratory **towards Adastra**. You may be able to use it the other way around **if**, your laboratory’s machine’s IP is allowed.

<a id="between-computing-site-ccfr"></a>

<a id="adastra-storage-and-transfer-transfer-ccfr"></a>

### Between computing site (CCFR)

Communication between french computing sites can rely the Centres de Calcul FRançais (CCFR) network. This network is relatively fast (10 Gb/s between CINES, IDRIS and TGCC, 100 Gb/s Soon™). Using CCFR is **NOT** mandatory you can use the traditional FQDN endpoints but this kind of transfer will be slower.

To use the network user needs to do theses things:

- first, ask both the source and destination computing site for the authorization to use the CCFR resources (node and network);
- second, connect to the site’s login node (slight twist at CINES and IDRIS, see below);
- and third, initiate the transfer using the right tools.

The first part is a per site specific operation and is summarized in the table below, assuming you want to connect **to** the site show in the first column of the table below.

| Site to connect to | Process specificities |
| --- | --- |
| CINES | The user requests at [svp@cines.fr](mailto:svp%40cines.fr) that his account be allowed to use CCFR resources. |
| IDRIS | The user fills the [`2nd form at page 2 of this document`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/5e4db4ef99d7fc1132c1604eeee4995b/idris_fgc.pdf) dubbed *Accéder au réseau CCFR* and asks [gestutil@idris.fr](mailto:gestutil%40idris.fr) to accept his request. **Optionally**: The user adds his CCFR public key to the `~/.ssh/authorized_keys` file on his IDRIS machine account. |
| TGCC | The user requests at [hotline.tgcc@cea.fr](mailto:hotline.tgcc%40cea.fr) that his account be allowed to use CCFR resources. |

**Note**

To check if you have access to the **CINES** CCFR node, you may connect to Adastra, use the `id` command and look for the `cinesccfr` group. If you have it then you are good to go on CINES’ side. You still have to make sure that the other site’s CCFR node access request was processed.

The second part’s procedure is then as follows:

- You `ssh` to the computing site which will initiate the transfer. You land on a login node.

  > - Then, at CINES and IDRIS, you `ssh` *again*, to the initiating CCFR node FQDN (table below) associated to the computing site you have just logged on.
  > - At TGCC, you stay on the login node.
- You are now on a *CCFR node*, ready to initiate a transfer towards the **receiving** computing site’s CCFR node FQDN (table below).

| Site | Sending CCFR node [FQDN](https://en.wikipedia.org/wiki/Fully_qualified_domain_name) | Receiving CCFR node FQDN |
| --- | --- | --- |
| CINES | adastra-ccfr.cines.fr (aka login1) | adastra-ccfr.cines.fr |
| IDRIS | jean-zay-ccfr.idris.fr | jean-zay-ccfr.idris.fr |
| TGCC | Any login node. | irene-fr-ccfr-gw.ccc.cea.fr |

Renater allocated 60 Gbit/s out of 100 Gbit/s between Marseille and Montpellier to traffic from Adastra to IDRIS or TGCC.

Now as **an example**, say you want to transfer 50 Tio of data from the Adastra machine (at CINES, Montpellier) to the Jean-Zay machine (at IDRIS, Paris). The user needs to have an account on both Adastra and Jean-Zay and have request to use the CCFR network. Then, to initiate a connection **from Adastra** towards an other site, you **first** need to connect to a site’s login node (say, to Adastra, `adastra.cines.fr`) and **then**, connect from the login node to the sending CCFR node `adastra-ccfr.cines.fr` endpoint using `ssh <login>@adastra-ccfr.cines.fr` command. **Finally**, you can initiate connections towards the other sites which, following our previous Adastra and Jean-Zay example, would look like so:

```shell-session
$ scp -r my_adastra_directory <login>@jean-zay-ccfr.idris.fr:/path/to/my_directory
```

The traffic is automatically routed through the CCFR network and you can benefit from the faster interconnections.

In addition to using the CCFR endpoints explicitly, the national sites (but not CINES as of 2023/01/01) provide a module named `ccfr`. It exposes the following commands: `ccfr_cp`, `ccfr_ssh`, `ccfr_sync` and `ccfr_mycert`. The first three commands respectively wrap `rsync`, `ssh` and `rsync` to *simplify* the authentication via a process called *Single Sign-On* (which is different from [Login unique](../user_support/index.md#adastra-accessing-unique-login)). This authentication is setup using certificates and `ccfr_mycert`. More details on these commands in [`this slightly outdated document`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/b2ca7be2836be4860b085c6166331163/ccfr_userdoc_fr.pdf). You can use the CCFR network without this module.

<a id="ccfr-module-and-tools"></a>

#### CCFR module and tools

As a tentative to homogenize user experience across the 3 national computing centers, the CCFR module was created. It provides a uniform interface for account resource management.

For instance:

```shell-session
$ module load ccfr
$ ccfr_quota
Disk quotas for grp grp_<username> (gid 0123):
     Filesystem  kbytes   quota   limit   grace   files   quota   limit   grace
          /home   83624  29000000 30000000       -    5743   30000   33000       -
<project>
Disk quotas for grp <project> (gid 0124):
     Filesystem    used   quota   limit   grace   files   quota   limit   grace
          /home  20.35T  23.19T  23.28T       - 43079113  49500000 50000000       -
Disk quotas for grp <project> (gid 0124):
     Filesystem    used   quota   limit   grace   files   quota   limit   grace
       /scratch  73.47T   92.2T  93.13T       - 46018879  59500000 60000000       -
Disk quotas for grp <project> (gid 0124):
     Filesystem    used   quota   limit   grace   files   quota   limit   grace
          /work  102.4T  465.7T  512.2T       - 27434281  60000000 65000000       -
Disk quotas for grp <project> (gid 0124):
     Filesystem    used   quota   limit   grace   files   quota   limit   grace
         /store  30.73T  42.27T  45.06T       -  107914  170000 1800000       -
```

For instance to get the project’s compute and storage resource consumption:

```shell-session
$ module load ccfr
$ ccfr_project
Active project: proj_id

========================================================================================
Personal directory state of the user someuser0  (at 2026-09-17 11:48:14.986284 )

************************************************************************************************
|   SPACE    |  MODE     | TYPE  |         ID      |       USAGE     |      LIMIT      | UNIT  |
************************************************************************************************
|  Personal  | Space     | User  |       someuser0 |          176.00 |           29000 |    MB |
|            |----------------------------------------------------------------------------------
|            | Files     | User  |       someuser0 |             133 |           30000 | Files |
------------------------------------------------------------------------------------------------

========================================================================================
Project usage                        proj_id on cluster adastra (at 2026-09-16 00:00:00)

TITLE : [ <Some project name> ]

*******************************
|       PROJECT NAME          |
**********************************************************************************************************************
|   CINES    |      DARI      | PARTITION |     START    |      END     |      USAGE   |  ALLOCATION  |    ROOFTOP   |
**********************************************************************************************************************
----------------------------------------------------------------------------------------------------------------------
|   proj_id  |     ... CINES  |    mi250  |  2026-01-01  |  2026-12-31  |       43034  |       30000  |       37500  |   EXCEEDED
----------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------
|   proj_id  |     ... CINES  |    genoa  |  2026-01-01  |  2026-12-31  |     1353265  |      500000  |      625000  |   EXCEEDED
----------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------
|   proj_id  |     ... CINES  |    mi300  |  2026-01-01  |  2026-12-31  |       13552  |        1000  |        1250  |   EXCEEDED
----------------------------------------------------------------------------------------------------------------------

========================================================================================
File systems status for project   proj_id  (at 2026-09-17 11:48:15.018813 )

********************************************************************************************************************
| FILESYSTEM   |  MODE     | TYPE  |         ID      |           CURRENT USAGE           |      LIMIT      | UNIT  |
********************************************************************************************************************
|        /home | Space     | Group |         proj_id |        19845.50 |                 |           24900 |   GB  |
|              |           | Cnt(1)|         proj_id |          169.00 |                 |                 |   GB  |
|              |====================================================================================================
|              | Files     | Group |         proj_id |        37788142 |                 |                 | Files |
********************************************************************************************************************
|     /scratch | Space     | Group |         proj_id |       101043.23 |                 |          400000 |   GB  |
|              |====================================================================================================
|              | Files     | Group |         proj_id |        69419520 |                 |                 | Files |
********************************************************************************************************************
|        /work | Space     | Group |         proj_id |        92343.78 |                 |          200000 |   GB  |
|              |====================================================================================================
|              | Files     | Group |         proj_id |        31675504 |                 |                 | Files |
********************************************************************************************************************
|       /store | Space D   | Group |         proj_id |        34073.10 |                 |           50000 |   GB  |
|              |====================================================================================================
|              | Space D+T | Group |         proj_id |  not available  |                 |  not available  |  ---  |
|              |----------------------------------------------------------------------------------------------------
|              | Files     | Group |         proj_id |          348860 |                 |                 | Files |
********************************************************************************************************************

Note :
-----------
(1) Cnt : Part of the singularity container usage in the project
(2) USAGE BLK : size measured in the same way as the 'du' command
    -  Files in shared spaces $dci_SHAREDHOMEDIR et $dci_SHAREDSCRATCHDIR are also accounted

You can check on web site https://reser.cines.fr to have the detail on project usage.

D   = disks only
D+T = disks + tapes
Default projet set to dci
```

<a id="tools-to-transfer-data"></a>

<a id="adastra-storage-and-transfer-transfer-tools"></a>

### Tools to transfer Data

**Note**

Standard File Transfer Protocol (FTP) and Remote Copy (RCP) should **not** be used to transfer files due to security concerns.

**Warning**

Before reading this subsections, understand that due to the *unique login* functionalities implementation, the remote *home* directory may **not** be what you expect. Indeed, it may point to your **personal home** instead of your **project personal home**. You are thus recommended to work with absolute paths.

If moving many small files, it can be beneficial to compress them into a single archive file, then transfer just the one archive file. When using command-line tools, you should use the login nodes.

`wdcp` can be used to copy data **across the Adastra filesystems**. It takes the source directory and a destination directory:

```shell-session
$ wdcp <source_directory> <destination_directory>
```

To get information about your ongoing copies, use the `--show` flag. To get information about all your previous transfer jobs, use the `--list-all` flag.

Command-line tools such as `parallel-sftp`, `scp` and `rsync` can be used to transfer data **to and from CINES** (via the *internet*).

- `psftp` or `parallel-sftp` - [parallel-sftp](https://github.com/cea-hpc/openssh-portable) can be used to saturate the bandwidth when one copying thread is not enough (typically on the CCFR network)
  :   Its usage is identical as `sftp`, except the option `-n` which let you choose the number of ssh connections used for the parallel transfer. Sending a file from CINES to IDRIS:

      ```shell-session
      $ parallel-sftp -n 5 <login>@jean-zay-ccfr.idris.fr
      ```

      Once logged in, retrieving a file or directory from the remote host (IDRIS in this example) to the local host is done like so:

      ```
      sftp> get [options] <remote_path> <local_path>
      ```

      And to transfer data from the local host to the remote host (IDRIS in this example):

      ```
      sftp> put [options] <local_path> <remote_path>
      ```

      If you haven’t used the `-r` (recursive) option with the `sftp` command, you can use it directly with get and put. For more information, type `help` from the `sftp` prompt, or `man sftp` from the command line.
- `scp` - secure copy, a remote file-copying tool
  :   Sending a local file `my_file` to `/path/to/` on Adastra:

      ```shell-session
      $ scp my_file <login>@adastra.cines.fr:/path/to/
      ```

      Retrieving a remote file at `/path/to/my_file` on Adastra to the local directory `./`:

      ```shell-session
      $ scp <login>@adastra.cines.fr:/path/to/my_file ./
      ```

      Sending a local directory `my_directory` to `/path/to/` on Adastra:

      ```shell-session
      $ scp -r my_directory <login>@adastra.cines.fr:/path/to/
      ```
- `rsync` - a fast, versatile, remote (and local) file-copying tool
  :   Synchronize a remote directory `/path/to/` on Adastra with a local directory `my_directory` (readonly):

      ```shell-session
      $ rsync -avz my_directory <login>@adastra.cines.fr:/path/to/
      ```

      **Note**

      Where `a` is for archive mode, `v` is for verbose mode and `z` is for compressed mode. There is no `/` after `my_directory`. This will produce a `my_directory` folder at `adastra.cines.fr:/path/to/` (so we end up with `adastra.cines.fr:/path/to/my_directory`).

      Synchronize a local directory `./` with a remote directory `/path/to/my_directory` on Adastra (readonly):

      ```shell-session
      $ rsync -avz <login>@adastra.cines.fr:/path/to/my_directory ./
      ```

      Synchronize a remote directory `/path/to/` on Adastra with a local directory `my_directory` (readonly) and show progress:

      ```shell-session
      $ rsync -avz --progress my_directory <login>@adastra.cines.fr:/path/to/
      ```

      Synchronize a remote directory `/path/to/` on Adastra with a local directory `my_directory` (readonly), show progress, include files or directories starting with T and exclude all others

      ```shell-session
      $ rsync -avz --progress --include 'T*' --exclude '*' my_directory <login>@adastra.cines.fr:/path/to/
      ```

      Synchronize a local directory `./` with a remote directory `/path/to/my_directory` on Adastra (readonly), if the file or directory exists at the target (local) but not on the source (CINES), then delete it:

      ```shell-session
      $ rsync -avz --delete <login>@adastra.cines.fr:/path/to/my_directory ./
      ```

      Synchronize a remote directory `/path/to/` on Adastra with a local directory `my_directory` (readonly), transfer only the files that are smaller than 1 Mio:

      ```shell-session
      $ rsync -avz --max-size='1m' my_directory <login>@adastra.cines.fr:/path/to/
      ```

      If you want to verify the behavior is as intended, execute a dry-run:

      ```shell-session
      $ rsync -avz --dry-run my_directory <login>@adastra.cines.fr:/path/to/
      ```

See the manual pages for more information:

```shell-session
$ man sftp
$ man scp
$ man rsync
```

- Differences:
  :   - `scp` carry a similar semantic to the traditional `cp` with extended remote exchange functionalities. It cannot continue where it left if the transfer is interrupted.
      - `rsync` allows you to restart interrupted transfers (see the `--partial` or `-P` flags). By default, `rsync` checks if the transfer of the data was successful (no data corruption).
      - [FileZilla](https://filezilla-project.org/) starts multiple `sftp` processes and uses them parallel. Can be used to reach high throughput.
      - `parallel-sftp` is similar to [FileZilla](https://filezilla-project.org/) but uses multiple SSH channels instead of multiple `sftp` processes. It does not come with a GUI.

<a id="chaining-wdcp-data-transfer-and-job"></a>

### Chaining `wdcp` data transfer and job

You simply need to start an asynchronous `wdcp` copy, and chain your work to the copy job (note that `wdcp` prints the job identifier).

```shell-session
$ wdcp <source_directory> <destination_directory>
Dest dir doesn't exist, creating it
source path is <source_directory>
dest path is <destination_directory>
sbatch: INFO : As you didn't ask threads_per_core in your request: 2 was taken as default
sbatch: INFO : As you didn't ask cpus_per_task in your request: 2 was taken as default
Submitted batch job 2512458
            JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
          2512458 transfert dcp_tran   <user>  R       0:03      1 login1
$ sbatch --dependency=afterok:2512458 my_first_job.sh
Submitted batch job 2512459
```

Also, note that `wdcp` can be executed from the inside of the batch script. This means that you could have a workflow where you work on the scratch, and if everything goes well, after the last srun, you launch an asynchronous `wdcp` to copy your result files from the scratch area into, say, the work area.
