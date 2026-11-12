<!-- Source: https://dci.dci-gitlab.cines.fr/webextranet/user_support/index.html -->
<!-- Title: Accessing Adastra -->

<a id="accessing-adastra"></a>

# Accessing Adastra

This document is a quick start guide for the Adastra machine. You can find additional information on the [GENCI’s website](https://www.genci.fr/) and in this [`booklet`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/c48a5eb882d6e64c236f2b0e2521cf6f/Livret-information-Genci.pdf).

<a id="account-opening"></a>

<a id="adastra-accessing-account-opening"></a>

## Account opening

To access Adastra you need to have an account on the [Demande d’Attribution de Ressources Informatique (DARI)’s website](https://www.edari.fr/). Then, on eDARI, you need to ask to be associated to a research project with attributed Adastra compute hours. Following that, you can ask on eDARI for your personal account to be created on the machine (Adastra in this context). You will have to fill in a form, which to be valid, needs the three parties below have dated and electronically signed your account request:

- The person who made the request;
- the user’s security representative (often related to his laboratory);
- the laboratory director.

You will then receive, via email, the instructions containing your credentials.

<a id="connecting"></a>

<a id="adastra-accessing-connection"></a>

## Connecting

To connect to Adastra, `ssh` to `adastra.cines.fr`.

```shell-session
$ ssh <login>@adastra.cines.fr
```

**Warning**

Authenticating to Adastra using *ssh keys* **is not permitted**. You will have to enter your password.

To connect to a **specific** login node, use:

```shell-session
$ ssh <login>@adastra<login_node_number>.cines.fr
```

Where `<login_node_number>` represents a integer login node identifier. For instance, `ssh anusername@adastra5.cines.fr` will connect you to the login number 5.

<a id="x11-forwarding"></a>

<a id="adastra-x11-forwarding"></a>

### X11 forwarding

Automatic forwarding of the X11 display to a remote computer is possible with the use of SSH and a local (i.e., on your desktop) X server. To set up automatic X11 forwarding within SSH, you can do one of the following:

Invoke `ssh` with `-X`:

```shell-session
$ ssh -X <login>@adastra.cines.fr
```

Note that use of the `-x` flag (lowercase) will **disable** X11 forwarding. Users should **not** manually set the `${DISPLAY}` environment variable for X11 forwarding.

**Warning**

If you have issues when launching a GUI application, make sure this is not related to the `.Xauthority` file. If it is, or you are not sure it is, checkout the [.Xauthority file](index.md#adastra-file-layout-xauthority) document.

<a id="proxy"></a>

### Proxy

On Adastra, HTTP(S) accesses to the internet passes through a proxy which is defined at this URL (for both HTTP and HTTPS):

```
http://proxy-l-adastra.cines.fr:3128
```

For Conda you can use:

```shell-session
$ conda config --set proxy_servers.http "proxy-l-adastra.cines.fr:3128" --set proxy_servers.https "proxy-l-adastra.cines.fr:3128"
```

For SVN, in the `~/.subversion/servers` configuration file, add:

```
http-proxy-host = proxy-l-adastra.cines.fr http-proxy-port = 3128
```

On specific some nodes, you may want to disable proxying like so:

```shell-session
$ export NO_PROXY="${NO_PROXY},$(hostname)"
```

On Adastra, the default HTTP proxy related environment variables are:

```shell-session
export http_proxy=http://proxy-l-adastra.cines.fr:3128
export HTTP_PROXY=http://proxy-l-adastra.cines.fr:3128
export https_proxy=http://proxy-l-adastra.cines.fr:3128
export HTTPS_PROXY=http://proxy-l-adastra.cines.fr:3128
export FTP_PROXY=http://proxy-l-adastra.cines.fr:3128
export ftp_proxy=http://proxy-l-adastra.cines.fr:3128
export no_proxy=127.0.0.1,localhost,.cines.fr,admin,172.20.0.1
export NO_PROXY=127.0.0.1,localhost,.cines.fr,admin,172.20.0.1
```

For a reference on proxy environment variables (the Curl library), see: <https://curl.se/docs/tutorial.html#environment-variables>

<a id="login-unique"></a>

<a id="adastra-accessing-unique-login"></a>

## Login unique

The login unique (in english, *single sign on* or *unique login*) is a new feature of the CINES’ supercomputer that will enable a user to work on multiple projects using a single, *unique* login. These logins (also called username) will be valid the lifetime of the machine (though the data may not, see [Quotas](../data_storage_and_transfers/index.md#adastra-storage-and-transfer-policies-data-quota) for more details). This simplifies authentication over time. This procedure is already used in the other two national centres (IDRIS and TGCC). The method for logging into the machine remains the same as before and as described above. Once you are logged in, you get access to one of your *home* directory which is the *home* associated to your current project (if you have one). At this stage, you can adapt your environment to the project you wish to work on with the help of the command `myproject`.

The unique login tools will modify your Unix group and some environment variables. If you use scripts that are automatically loaded or that are expected in a specific location (say `.bashrc`) checkout the notes in the [Layout of common files and directories](index.md#adastra-file-layout) and [Accessing the storage areas](../data_storage_and_transfers/index.md#adastra-storage-and-transfer-storage-accessing) documents.

In this section we will present the `myproject` command. When freshly connected, your shell’s working directory will be your current **project’s personal** *home* directory or, if your account is not linked to any account, your **personal home**. Again refer to [Accessing the storage areas](../data_storage_and_transfers/index.md#adastra-storage-and-transfer-storage-accessing) for more details on the various storage areas. Your first step could be to list the flags `myproject` supports and that can be done like so:

```shell-session
$ myproject --help
usage: my_project.py [-h] [-s [project] | -S | -l | -a project | -c | -C | -m [project]]

Manage your hpc projects. The active project is the current project in your
session.

optional arguments:
-h, --help            show this help message and exit
-s [project], --state [project]
                        Get current HPC projects state
-S, --stateall        Get all HPC projects state
-l, --list            List all authorized HPC projects
-a project, --activate project
                        Activate the indicated project
-c, --cines           List projects directories CINES variables
-C, --ccfr            List projects directories CCFR variables
-m [project], --members [project]
                        List all members of a project
```

The most used commands are `-l` to list the project we are assigned to, `-a` to switch project and `-c` to list the environment variable described in [Accessing the storage areas](../data_storage_and_transfers/index.md#adastra-storage-and-transfer-storage-accessing).

<a id="listing-the-environment-variables-and-their-value"></a>

<a id="adastra-accessing-unique-login-listing-variable"></a>

### Listing the environment variables and their value

This is done like so (assuming a user with login `someuser`):

```shell-session
$ myproject -c
Liste des variables CINES permettant l'accès aux répertoires dans les différents espaces de stockage
----------------------------------------------------------------------------------------------------
Project actif: dci

OWN_HOMEDIR :     /lus/home/PERSO/grp_someuser/someuser

HOMEDIR :          /lus/home/BCINES/dci/someuser
SHAREDHOMEDIR :    /lus/home/BCINES/dci/SHARED
SCRATCHDIR :       /lus/scratch/BCINES/dci/someuser
SHAREDSCRATCHDIR : /lus/scratch/BCINES/dci/SHARED
WORKDIR :          /lus/work/BCINES/dci/someuser
SHAREDWORKDIR :    /lus/work/BCINES/dci/SHARED
STOREDIR :         /lus/store/BCINES/dci/someuser

gda2212_HOMEDIR :          /lus/home/NAT/gda2212/someuser
gda2212_SHAREDHOMEDIR :    /lus/home/NAT/gda2212/SHARED
gda2212_SCRATCHDIR :       /lus/scratch/NAT/gda2212/someuser
gda2212_SHAREDSCRATCHDIR : /lus/scratch/NAT/gda2212/SHARED
gda2212_WORKDIR :          /lus/work/NAT/gda2212/someuser
gda2212_SHAREDWORKDIR :    /lus/store/NAT/gda2212/SHARED
gda2212_STOREDIR :         /lus/store/NAT/gda2212/someuser

dci_HOMEDIR :          /lus/home/BCINES/dci/someuser
dci_SHAREDHOMEDIR :    /lus/home/BCINES/dci/SHARED
dci_SCRATCHDIR :       /lus/scratch/BCINES/dci/someuser
dci_SHAREDSCRATCHDIR : /lus/scratch/BCINES/dci/SHARED
dci_WORKDIR :          /lus/work/BCINES/dci/someuser
dci_SHAREDWORKDIR :    /lus/store/BCINES/dci/SHARED
dci_STOREDIR :         /lus/store/BCINES/dci/someuser
```

Observe that the `actif` project (*current project* in english) is `dci` in the example above. This should be interpreted as: the shell being currently setup so that the generic environment variables point to the project’s filesystem directories. For instance `${SHAREDSCRATCHDIR}` would point to the `actif` project’s group shared *scratch* space, in this case, `/lus/scratch/BCINES/dci/SHARED`. For more details on the file system spaces CINES offers, see [Accessing the storage areas](../data_storage_and_transfers/index.md#adastra-storage-and-transfer-storage-accessing).

As such, an `actif` project does **not relate** to a DARI related notion of activated, valid, ongoing, etc..

<a id="listing-associated-projects"></a>

### Listing associated projects

This is done like so (assuming a user with login `someuser`):

```shell-session
$ myproject -l
Projet actif: dci

Liste des projets de calcul associés à l'utilisateur 'someuser' : ['gda2212', 'dci']
```

<a id="switching-project"></a>

### Switching project

You can rely on the `${ACTIVE_PROJECT}` environment variable to obtain the currently used project:

```shell-session
$ echo ${ACTIVE_PROJECT}
dci
```

This is done like so (assuming a user with login `someuser`):

```shell-session
$ myproject -a gda2212
Projet actif :dci

Bascule du projet "dci" vers le projet "gda2212"
Projet " gda2212 " activé.
$ myproject -c
Liste des variables CINES permettant l'accès aux répertoires dans les différents espaces de stockage
----------------------------------------------------------------------------------------------------
Project actif: gda2212

OWN_HOMEDIR :     /lus/home/PERSO/grp_someuser/someuser

HOMEDIR :          /lus/home/NAT/gda2212/someuser
SHAREDHOMEDIR :    /lus/home/NAT/gda2212/SHARED
SCRATCHDIR :       /lus/scratch/NAT/gda2212/someuser
SHAREDSCRATCHDIR : /lus/scratch/NAT/gda2212/SHARED
WORKDIR :          /lus/work/NAT/gda2212/someuser
SHAREDWORKDIR :    /lus/work/NAT/gda2212/SHARED
STOREDIR :         /lus/store/NAT/gda2212/someuser

gda2212_HOMEDIR :          /lus/home/NAT/gda2212/someuser
gda2212_SHAREDHOMEDIR :    /lus/home/NAT/gda2212/SHARED
gda2212_SCRATCHDIR :       /lus/scratch/NAT/gda2212/someuser
gda2212_SHAREDSCRATCHDIR : /lus/scratch/NAT/gda2212/SHARED
gda2212_WORKDIR :          /lus/work/NAT/gda2212/someuser
gda2212_SHAREDWORKDIR :    /lus/store/NAT/gda2212/SHARED
gda2212_STOREDIR :         /lus/store/NAT/gda2212/someuser

dci_HOMEDIR :          /lus/home/BCINES/dci/someuser
dci_SHAREDHOMEDIR :    /lus/home/BCINES/dci/SHARED
dci_SCRATCHDIR :       /lus/scratch/BCINES/dci/someuser
dci_SHAREDSCRATCHDIR : /lus/scratch/BCINES/dci/SHARED
dci_WORKDIR :          /lus/work/BCINES/dci/someuser
dci_SHAREDWORKDIR :    /lus/store/BCINES/dci/SHARED
dci_STOREDIR :         /lus/store/BCINES/dci/someuser
```

As you can see, the `${HOMEDIR}`, `${SHAREDHOMEDIR}` etc. **have changed** when the user switched project (compared to the output presented [here](index.md#adastra-accessing-unique-login-listing-variable)). That said, the prefixed variables like `${dci_HOMEDIR}` **didn’t change** and using it is the recommended way to reference a directory assuming you do not know which project will be loaded when the variable will be used (say, in a script).

Some issues can be encountered when using tools that are unaware of the *many home* structure. Yat again, check the [Layout of common files and directories](index.md#adastra-file-layout) and [Accessing the storage areas](../data_storage_and_transfers/index.md#adastra-storage-and-transfer-storage-accessing) documents.

<a id="layout-of-common-files-and-directories"></a>

<a id="adastra-file-layout"></a>

## Layout of common files and directories

Due to new functionalities introduced through [Login unique](index.md#adastra-accessing-unique-login), you may find the [Accessing the storage areas](../data_storage_and_transfers/index.md#adastra-storage-and-transfer-storage-accessing) document useful. It describes the multiple *home* directories and how to access them through environment variable (`${HOMEDIR}`, `${OWN_HOMEDIR}` etc.).

Some subtleties needs addressing, see below.

<a id="bashrc-file"></a>

### `.bashrc` file

Your `.bashrc` file should be accessible in the `${HOMEDIR}` directory (project personal *home*).

Using symbolic links, you can prevent file redundancy by first, storing our `.bashrc` in your `${OWN_HOMEDIR}` and creating a link in your `${HOMEDIR}`. Effectively, you are factorizing the `.bashrc`:

```shell-session
$ ln -s "${OWN_HOMEDIR}/.bashrc" "${HOMEDIR}/.bashrc"
```

If you want your `.bashrc` to be loaded when you login to the machine you need to make sure a file called `.bash_profile` is present in your `${HOMEDIR}` directory (project personal *home*). This file, if not present, should thus be created to contain:

```shell
if [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi
```

Similarly to the `.bashrc` you can use links to factorize this file.

<a id="ssh-directory"></a>

### `.ssh` directory

Your `.ssh` directory should be accessible in the `${OWN_HOMEDIR}` directory (personal *home*).

**Optionally**, you can create link in your `${HOMEDIR}` to point to `${OWN_HOMEDIR}/.ssh`

<a id="xauthority-file"></a>

<a id="adastra-file-layout-xauthority"></a>

### `.Xauthority` file

Your `.Xauthority` file should be accessible in the `${HOMEDIR}` directory (project personal *home*).

In practice, this file gets created by the system in the `${OWN_HOMEDIR}` directory (personal *home*). You **need** to create a link like so:

```shell-session
$ ln -s "${OWN_HOMEDIR}/.Xauthority" "${HOMEDIR}/.Xauthority"
```

**Note**

Make sure your `${XAUTHORITY}` environment variable correctly points to `${OWN_HOMEDIR}/.Xauthority` or `${HOME}/.Xauthority`.

**Warning**

`xauth`’s error messages are often unclear and lacking in details. If you have an issue with X authentication, use `strace -- xauth` as a complement in the log you will provide to the support team.

<a id="programming-environment"></a>

<a id="adastra-programming-environment"></a>

# Programming environment

The programming environment includes compiler toolchains, libraries, performance analysis and debugging tools and optimized scientific libraries. Adastra, being a Cray machine, it uses the Cray Programming Environment abbreviated **CrayPE** or **CPE**. In practice a CrayPE is simply a set of module. This section tries to shed light on the subtleties of the system’s environment.

The Cray documentation is available in the man pages (prefixed with `intro_`) and is **starting** to be mirrored and enhanced at this URL <https://cpe.ext.hpe.com/docs/>.

<a id="module-why-and-how"></a>

<a id="adastra-programming-environment-module-concepts"></a>

## Module, why and how

Like on many HPC machines, the software is presented through modules. A module can be mostly seen as a set of [environment variable](https://en.wikipedia.org/wiki/Environment_variable). Variables such as the `${PATH}`, `${LD_LIBRARY_PATH}` are modified to introduce new tools in the environment. The software providing the module concept is [Lmod](https://github.com/TACC/Lmod/), a Lua-based module system for dynamically altering a shell environment.

<a id="general-usage"></a>

### General usage

The interface to Lmod is provided by the `module` command:

| Command | Description |
| --- | --- |
| `module list` | Shows the list of the currently loaded modules. |
| `module overview` | Shows a view of modules aggregated over the versions. |
| `module available` | Shows a table of the currently available modules. |
| `module --show_hidden available` | Shows a table of the currently available modules and also show hidden module (very useful !). |
| `module purge` | Unloads all modules. |
| `module show <modulename>` | Shows the environment changes made by the `<modulename>` modulefile. |
| `module load <modulename> [...]` | Loads the given `<modulename>`(s) into the current environment. |
| `module help <modulename>` | Shows help information about `<modulename>`. |
| `module spider <string>` | Searches all possible modules according to `<string>`. |
| `module use <path>` | Adds `<path>` to the modulefile search cache and `${MODULESPATH}`. |
| `module unuse <path>` | Removes `<path>` from the modulefile search cache and `${MODULESPATH}`. |
| `module update` | Reloads all currently loaded modules. |

Lmod introduces the concept of default and currently loaded modules. When the user enters the `module available` command, he may get something similar to the small example given below.

```shell-session
$ module available
---- /opt/cray/pe/lmod/modulefiles/comnet/crayclang/14.0/ofi/1.0 ----
cray-mpich/8.1.20 (L,D)    cray-mpich/8.1.21

Where:
 L:  Module is loaded
 D:  Default Module
```

Note the `L` and `D` described at the end of the example. It shows you what is loaded and what is loaded by default when you do not specify the version of a module (that is, you omit the `/8.1.21` for instance). Note that `D` does not mean it is loaded automatically but that, if a module is to be loaded (say `cray-mpich`) and the version is not specified, then, it’ll load the module marked by `D` (say `cray-mpich/8.1.20`). It is considered **good practice** to specify the full name to avoid issues related to more complicated and complex topics (compilation, linkage, etc.).

**Note**

By default some modules are loaded and this differs from older machines hosted at CINES such as Occigen.

**Note**

The `--terse` option can be useful when the output of the `module` command needs to be parsed in scripts.

<a id="looking-for-a-specific-module-or-an-already-installed-software"></a>

### Looking for a specific module or an already installed software

Modules with dependencies are only available (show in `module available`) when their dependencies, such as compilers, are loaded. To search the entire hierarchy across all possible dependencies, the `module spider` command can be used as summarized in the following table.

| Command | Description |
| --- | --- |
| `module spider` | Shows the entire possible graph of modules. |
| `module spider <modulename>` | Searches for modules named `<modulename>` in the graph of possible modules. |
| `module spider <modulename>/<version>` | Searches for a specific version of `<modulename>` in the graph of possible modules. |
| `module spider <string>` | Searches for modulefiles containing `<string>`. |

<a id="craype-basics"></a>

<a id="adastra-programming-environment-cray-pe-basics"></a>

## CrayPE basics

The CrayPE is often feared due to its apparent complexity. We will try to present the basic building blocs and show how assembling these blocs.

At a high level, the Cray environment is made up of:

- External libraries (such as the ones in ROCm);
- Cray libraries (MPICH, libsci);
- Architecture modules (`craype-accel-amd-gfx90a`);
- Compilers (`craycc` as the `cce` module, `amdclang` as the `amd` module, `gcc` as `gnu` module);
- The Cray compiler wrappers (`cc`, `CC`, `ftn`) offered by the `craype` module;
- The `PrgEnv` modules (`PrgEnv-cray`);
- And the `cpe/XX.YY`.

The **external libraries** refer to libraries the CrayPE requires but are not the property of Cray, AMD’s ROCm is such an example. The **Cray libraries** are closed source software, there are multiple variants of the same library to accommodate for the GPU and many compiler support. The **architecture modules** will change the wrapper’s behavior (see [Cray compiler wrapper](index.md#adastra-programming-environment-cray-wrapper)) by helping choosing which library to link against (say, the [MPICH GPU plugin](../software_stack/libraries/index.md#adastra-software-stack-libraries-mpi-cray-mpich-gpu-aware)), or modifying the flags such as `-march=zen4`. The **compilers** are not recommended to be directly used; they should instead be used through the **Cray compiler wrapper** which will interpret the `PrgEnv`, the loaded Cray library and architecture modules to handle the compatibility matrix transparently (with few visible artifacts). The `PrgEnv` are preset environments, you can choose to use them or cherry-pick you own set of module, at your own risk. The `cpe/XX.YY` modules are used to change the default version of the above mentioned modules and allows you to operate a set of intercompatible default modules.

[![../_images/craype_interactions.png](https://dci.dci-gitlab.cines.fr/webextranet/_images/craype_interactions.png)](https://dci.dci-gitlab.cines.fr/webextranet/_images/craype_interactions.png)

Graphical representation of the CrayPE component interactions.

**Note**

There is an order in which we recommend loading the modules. See the note in [Targeting an architecture](index.md#adastra-programming-environment-targeting-architecture).

**Important**

**Do not forget** to export the appropriate environment variable such as `CC`, `CXX` etc. and make them point to the correct compiler or Cray compiler wrapper by loading the correct `PrgEnv`. This is can be crucial for tools like CMake and Make.

<a id="changing-craype-version"></a>

## Changing CrayPE version

A Cray Programming Environment (CrayPE) can be simply viewed as a set of module (of a particular version). Switching CrayPE is like switching modules and defining new versions.

You can load a `cpe/XX.YY` module to prepare your environment with the modules associated to a specific `XX.YY` version of `cpe`. In practice, it will change the version of your loaded modules to match the version the `cpe/XX.YY` in question is expecting and, in addition, will **modify the default version of the Cray modules**.

**Warning**

If you use a `cpe/XX.YY` module, it must come first before you load any other Cray modules.

**Important**

You can **preload** a `cpe/XX.YY` module before preparing your environment to be sure you are using the correct version of the modules you load.

As an example:

```shell-session
 1$ module available cpe
 2-------------------- /opt/cray/pe/lmod/modulefiles/core --------------------
 3    cpe/22.11    cpe/22.12    cpe/23.02 (D)
 4$ module purge
 5-------------------- /opt/cray/pe/lmod/modulefiles/core --------------------
 6    cce/15.0.0    cce/15.0.1 (D)
 7$ module load PrgEnv-cray
 8$ module list
 9Currently Loaded Modules:
10    1) cce/15.0.1   2) craype/2.7.19   3) cray-dsmml/0.2.2
11    2) libfabric/1.15.2.0   5) craype-network-ofi   6) cray-mpich/8.1.24
12    3) cray-libsci/23.02.1.1   8) PrgEnv-cray/8.3.3
13$ module load cpe/22.12
14The following have been reloaded with a version change:
15  1) cce/15.0.1 => cce/15.0.0
16  2) cray-libsci/23.02.1.1 => cray-libsci/22.12.1.1
17  3) cray-mpich/8.1.24 => cray-mpich/8.1.23
18$ module available cce
19-------------------- /opt/cray/pe/lmod/modulefiles/core --------------------
20    cce/15.0.0 (L,D)    cce/15.0.1
21$ module load cpe/23.02
22Unloading the cpe module is insufficient to restore the system defaults.
23Please run 'source /opt/cray/pe/cpe/22.12/restore_lmod_system_defaults.[csh|sh]'.
24
25The following have been reloaded with a version change:
26  1) cce/15.0.0 => cce/15.0.1
27  2) cpe/22.12 => cpe/23.02
28  3) cray-libsci/22.12.1.1 => cray-libsci/23.02.1.1
29  4) cray-mpich/8.1.23 => cray-mpich/8.1.24
30$ module available cce
31-------------------- /opt/cray/pe/lmod/modulefiles/core --------------------
32    cce/15.0.0    cce/15.0.1 (L,D)
```

As we can see, the `cpe/22.12` changed the modules version and also changed the default modules version.

**Note**

Loading a `cpe` module will lead to a quirk which is shown line 22. The quirks comes from the fact that unloading a module that *switches* modules does not bring the environment back to it states before the *switching*, in fact, it does nothing. Once the module is unloaded, the default module version are restored but we have to load them back. This is the role of the above mentioned script (`restore_lmod_system_defaults.sh`).

<a id="cray-compiler-wrapper"></a>

<a id="adastra-programming-environment-cray-wrapper"></a>

## Cray compiler wrapper

As you may know, compatibilities between compilers and libraries is not always guaranteed and a compatibility matrix can be given to the user who are left to themselves to figure out how to combine the software components. Loading the `PrgEnv-<compiler>[-<compiler2>]` module introduces a compiler wrapper (also called *driver*) which will interpret environment variables introduced by other Cray modules such as `craype-accel-amd-gfx90a` (see [Targeting an architecture](index.md#adastra-programming-environment-targeting-architecture) for more details), `cray-mpich`, etc.. The driver creates the toolchain needed to satisfy the request (compilation, optimization, link, etc.). It also uses the information gathered in the environment to specify include paths, link flags, architecture specific flags, etc. that the underlying compiler needs to produce code. **Effectively, theses compiler wrappers abstract the compatibility matrix away from the user**; linking and providing the correct headers at compile and run time is only a subset of the features provided by the Cray compiler wrappers. If you do not use the wrappers, you will have to do more work and expose yourself to error prone manipulations.

<a id="default-libraries"></a>

## Default libraries

The Cray environment will rely on a directory containing all the libraries it requires along with the ld.so cache to point to it. This directory will always contain the latest version of the libraries and thus, regardless of the module loaded, it will be these library that will be loaded into your program. To change that behavior so that you always use the libraries that come with the module you load, and not the libraries in the directory mentioned above, you should, **after having loaded all your modules**, set:

```shell-session
$ export LD_LIBRARY_PATH="${CRAY_LD_LIBRARY_PATH}:${LD_LIBRARY_PATH}"
```

Or, **before loading the Cray environment modules**:

```shell-session
$ export PE_LD_LIBRARY_PATH=system
```

Or, **at build time, using the Cray wrappers**:

```shell-session
$ export CRAY_ADD_RPATH=yes
```

Additional information is given here: <https://cpe.ext.hpe.com/docs/latest/getting_started/CPE-General-User-Guide-HPCM.html#swapping-other-programming-environment-components>.

<a id="prgenv-and-compilers"></a>

<a id="adastra-programming-environment-prgenv-compiler"></a>

## `PrgEnv` and compilers

Avant-propos: NVHPC is Nvidia’s GPU software stack, ROCm is AMD’s GPU software stack (`amd-mixed` or `PrgEnv-amd`), CCE is part of CPE which is Cray’s CPU/GPU compiler toolchain (`PrgEnv-cray`), LLVM is your plain old LLVM toolchain, OneAPI is Intel’s new CPU/GPU Sycl based software stack (contains the DPC++ toolchain, aka Intel LLVM).

The compilers available on Adastra are provided through the Cray environment modules. Most of the readers already know about the GNU software stack. Adastra comes with three more supported compilers. The Cray, the AMD [Radeon Open Compute (ROCm)](https://github.com/RadeonOpenCompute), AMD AOCC and Intel LLVM compilers are all based on the state of the art [LLVM compiler infrastructure](https://llvm.org/). In fact you can treat these compilers as *vendor recompiled Clang/Flang LLVM compilers* with added optimization passes, vectorized `libm` or OpenMP backend in the case of the Cray compiler (but **not much** more). The AMD Optimizing C/C++ Compiler (AOCC) stack serves a similar role to the Intel classic/LLVM compilers, but for AMD. There is also a system (OS provided) versions of GCC available in `/usr/bin` (try not using it).

The `Programming environment` column of the table below represent the module to load to beneficiate from a specific environment. You can load a compiler module after loading a `PrgEnv` to choose a specific version of a compiler belonging to a given `PrgEnv`. That is, load `cce/15.0.0` after loading `PrgEnv-cray` to make sure you get the `cce/15.0.0` compiler. The modules loaded by a `PrgEnv` will change as the environment evolves. After the first load of a `PrgEnv`, you are recommended to save the module implicitly loaded (`module list`) and explicitly load them to avoid future breakage.

| Vendor | Programming environment | Compiler module | Language | Compiler wrapper | *Raw* compiler | Usage and notes |
| --- | --- | --- | --- | --- | --- | --- |
| Cray | `PrgEnv-cray` | `cce` | C | `cc` | `craycc` | For CPU and GPU compilations. `craycc` and `craycxx` are LLVM based while `crayftn` is entirely proprietary. `cce` means Cray Compiling Environment. |
| C++ | `CC` | `craycxx` or `crayCC` |
| Fortran | `ftn` | `crayftn` |
| AMD | `PrgEnv-amd` | `amd` | C | `cc` | `amdclang` | For CPU and GPU compilations. This module introduces the ROCm stack. ROCm is AMD’s **GPGPU** software stack. These compilers are open source and available on Github. You can contact AMD via Github issues. |
| C++ | `CC` | `amdclang++` |
| Fortran | `ftn` | `amdflang` (new Flang) |
| AMD | `PrgEnv-aocc` | `aocc` | C | `cc` | `clang` | For CPU compilations. These compilers are LLVM based but the LLVM fork are not open sourced. |
| C++ | `CC` | `clang++` |
| Fortran | `ftn` | `flang` (classic Flang) |
| GNU | `PrgEnv-gnu` | `gcc` | C | `cc` | `gcc` | For CPU compilations. |
| C++ | `CC` | `g++` |
| Fortran | `ftn` | `gfortran` |
| Intel | `PrgEnv-intel` | `intel` | C | `cc` | `icx` | For CPU compilations. The historical `ifort` compiler and the Intel LLVM `icx` and `icpx` compilers. |
| C++ | `CC` | `icpx` |
| Fortran | `ftn` | `ifort` |
| Intel | `PrgEnv-intel` | `intel-classic` | C | `cc` | `icc` | For CPU compilations. Intel’s historical toolchain. |
| C++ | `CC` | `icpc` |
| Fortran | `ftn` | `ifort` |
| Intel | `PrgEnv-intel` | `intel-oneapi` | C | `cc` | `icx` | For CPU compilations. Intel’s new toolchain based on LLVM and trying to democratize Sycl. |
| C++ | `CC` | `icpx` |
| Fortran | `ftn` | `ifx` |

**Note**

Reading (and understanding) the `craycc` or `crayftn` man pages will provide you with valuable knowledge on the usage of the Cray compilers.

**Important**

It is **highly recommended** to use the Cray compiler wrappers (`cc`, `CC`, and `ftn`) whenever possible. These are provided whichever programming environment is used. These wrappers are somewhat like the `mpicc` provided by other vendors.

Switching compiler is as *simple* as loading an other `PrgEnv`. The user only needs to recompile the software, assuming the build scripts or build script generator scripts (say CMake scripts) are properly engineered.

For **CPU** compilations:

> - C/C++ codes can rely on `PrgEnv-gnu`, `PrgEnv-aocc` or `PrgEnv-cray`;
> - Fortran codes can rely on `PrgEnv-gnu`, `PrgEnv-cray` or `PrgEnv-intel`.

**Note**

If you target the Genoa CPUs, **you must ensure** that the GCC version is more recent or equal to `gcc/13.2.0`.

For **GPU** compilations:

- C/C++ codes can rely `PrgEnv-amd`, `PrgEnv-cray` or potentially `PrgEnv-gnu` with `rocm`;
- Fortran codes can rely `PrgEnv-cray` (required for OpenMP target/OpenACC + Fortran).

To know which compiler/PrgEnv to use depending on the parallelization technology your program relies on (OpenMP, OpenACC, HIP, etc.), check [this table](index.md#adastra-programming-environment-intra-process-parallelization-technologies).

**Note**

Understand that while both AMD softwares, `PrgEnv-amd` and `PrgEnv-aocc` target a fundamentally different node kind, the first one is part of the ROCm stack (analogous to NVHPC), the second one is an historical CPU compiler (analogous to Intel’s ICC).

The `PrgEnv-cray` (CCE), `PrgEnv-amd` (ROCm), `PrgEnv-gnu`, `PrgEnv-aocc` and `PrgEnv-aocc` all support the following C++ standards (and implied C standards): `c++11`, `gnu++11`, `c++14`, `gnu++14`, `c++17`, `gnu++17`, `c++20`, `gnu++20`, `c++2b`, `gnu++2b`. Some caveats exist regarding C++ modules with C++20. All theses compilers (expect GNU), are based on Clang.

the Fortran compiler all support the following standards: `f90`, `f95`, `f03`.

**Warning**

If your code has, all along its life, relied on non standard, vendor specific extensions, you may have issues using an other compiler.

<a id="prgenv-mixing-and-subtleties"></a>

<a id="adastra-programming-environment-mixing-prgenv"></a>

## `PrgEnv` mixing and subtleties

Cray provides the `PrgEnv-<compiler>[-<compiler2>]` modules (say, `PrgEnv-cray-amd`) that load a given `<compiler>` and [toolchain](https://en.wikipedia.org/wiki/Toolchain) and optionally, if set, introduce an additional `<compiler2>`. In case a `<compiler2>` is specified, the Cray environment will use `<compiler>` to compile Fortran sources and `<compiler2>` for C and C++ sources. The user can then enrich his environment by loading other libraries through modules (though some of these libraries are loaded by default with the `PrgEnv`).

*Introducing an environment, toolchain or tool* through the use of modules means that [loading a module will modify](index.md#adastra-programming-environment-module-concepts) environment variables such as `${PATH}`, `${ROCM_PATH}`, `${LD_LIBRAY_PATH}` to make the tool or toolchain available to the user’s shell.

For example, say you wish to use the **Cray compiler** to compile CPU or GPU code, introduce CCE this way:

```shell-session
$ module load PrgEnv-cray
```

Say you want to use the **Cray compiler** to compile Fortran sources and use the **AMD compiler** for C and C++ sources, introduce CCE and ROCm this way:

```shell-session
$ module load PrgEnv-cray-amd
```

Say you want to use the **AMD compiler** to compile CPU or GPU code, introduce the ROCm stack this way:

```shell-session
$ module load PrgEnv-amd
```

<a id="mixing-prgenv-and-toolchain"></a>

<a id="adastra-programming-environment-mixing-toolchain"></a>

## Mixing `PrgEnv` and toolchain

Say you want to use the **Cray compiler** to compile CPU or GPU code and also have access to the **ROCm tools and libraries**, introduce CCE and ROCm this way:

```shell-session
$ module load PrgEnv-cray amd-mixed
```

Mixing compilers and tooling is achieved through the `*-mixed` modules. `*-mixed` modules do not significantly alter the Cray compiler wrapper’s behavior. They can be used to steer the compiler in using, say, the correct ROCm version instead of the default one (`/opt/rocm`).

`*-mixed` modules can be viewed as an alias to the underlying software. For instance, `amd-mixed` would be an alias for the `rocm` module.

<a id="targeting-an-architecture"></a>

<a id="adastra-programming-environment-targeting-architecture"></a>

## Targeting an architecture

In a Cray environment, one can load modules to target architectures instead of adding compiler flags explicitly.

On Adastra’s accelerated nodes, we have AMD-Trento (host CPU) and AMD-MI250X (accelerator) as the two target architectures. The command `module available craype-` will show all the installed modules for available target architectures. For AMD-Trento the module is `craype-x86-trento`, for AMD-MI250X it would be `craype-accel-amd-gfx90a` and for MI300A it is `craype-accel-amd-gfx942`. These modules add environment variables used by the Cray compiler wrapper to trigger flags used by the compilers to optimize or produce code for these two architectures.

**Warning**

If you load a non-cpu target module, say `craype-accel-amd-gfx90a`, please do also load the `*-mixed` or toolchain module (`rocm`) associated to the target device, else you expose yourself to a debugging penance.

For example, to setup a MI250X GPU programming environment:

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

You get a C/C++/Fortran compiler configured to compile for Trento CPUs and MI250X GPUs and automatically link with the appropriate Cray MPICH release, that is, if you use the Cray compiler wrappers.

**Warning**

If you get a warning such as this one `Load a valid targeting module or set CRAY_CPU_TARGET`, it is probably because you did not load a `craype-x86-<architecture>` module.

**Note**

Try to always load, first, the CPU and GPU architectures (say, `craype-x86-trento` for the GENOA partition and `craype-x86-trento`, `craype-accel-amd-gfx90a` for the MI250 partition), then the `PrgEnv` and the rest of your modules.

<a id="intra-process-parallelization-technologies"></a>

<a id="adastra-programming-environment-intra-process-parallelization-technologies"></a>

## Intra-process parallelization technologies

When you are not satisfied with the high level tools such as the vendor optimized BLAS, you have the option to program the machine by yourself. These technology are harder to use, more error prone but more versatile. Some technologies are given below, but the list is obviously not complete.

We could define at least two class of accelerator programming technologies. The ones based on directive (say, `pragma omp parallel for`) and the ones base on *kernels*. A kernel is a treatment, generally the inner loops or body of the inner loops of what you would write on a serial code. The kernel is given data to transform and is explicitly mapped to the hardware compute units.

**Note**

A memory bound code is less likely to need highly tuned code except for efficient loads. A compute bound code may have to rely on very specific hardware features (LDS swizzling, MMA cores, TMA, etc.). As such, for a memory bound code, it could be enough to rely on technologies limited to “medium” fine tuning so as to limit the complexity of the code.

<a id="for-c-c-codes"></a>

### For **C/C++** codes

| Class | Technology | Compiler support on AMD GPUs | Compiler support on Nvidia GPUs | Compiler support on Intel GPUs | Compiler support on x86 CPUs | Fine tuning | Implementation complexity/maintainability | Community support/availability (expected longevity in years) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Directive | OpenACC v2 | GCC~ | CUDA Toolkit/GCC~ |  | CUDA Toolkit/GCC~ | Low-medium | Low | Medium/high (+5 y) |
| OpenMP v5 | CCE/AMD LLVM | CUDA Toolkit/CCE | Intel LLVM | All | Low-medium | Low | High (+10 y) |
| Kernel | Sycl | Intel LLVM/AdaptiveCPP | Intel LLVM/AdaptiveCPP | Intel LLVM/AdaptiveCPP | Intel LLVM/AdaptiveCPP | High | Medium/high | High (+10 y) |
| CUDA/HIP | AMD LLVM/CCE | CUDA Toolkit/LLVM/CCE |  |  | High | Medium/high | High (+10 y) |
| Kokkos | All the above for AMD GPUs. | All the above for Nvidia GPUs. | All the above for Intel GPUs. | All | Medium/high | Low/medium | High (+10 y) |

Sycl, the Khronos consortium’ successor to OpenCL is quite complex, like its predecessor. Obviously, time will tell if it is worth investing in this technology but there is a significant ongoing *open* standardization effort.

Kokkos in itself is not on the same level as OpenACC, OpenMP, CUDA/HIP or Sycl because it serves as an abstraction of all theses.

**Note**

Cray’s CCE, AMD LLVM, Intel LLVM and LLVM’s Clang share the same front end (*what reads the code*). Most are just a recompiled/extended Clang. Cray’s C/C++ compiler is a LLVM compiler with a modified proprietary backend (*code optimization and library such as the OpenMP backend implementation*). Cray’s Fortran compiler is a proprietary frontend and LLVM backend. As such all these LLVM fork have some feature support commonalities.

<a id="for-fortran-codes"></a>

### For **Fortran** codes

| Class | Technology | Compiler support on AMD GPUs | Compiler support on Nvidia GPUs | Compiler support on Intel GPUs | Compiler support on x86 CPUs | Fine tuning | Implementation complexity/maintainability | Community support/availability (expected longevity in years) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Directive | OpenACC v2 | CCE/AMD LLVM/GCC~ | CUDA Toolkit/CCE/LLVM~/GCC~ |  | CUDA Toolkit/CCE/LLVM~/GCC~ | Low-medium | Low | Medium/High (+5 y) |
| OpenMP v5 | CCE/AMD LLVM/GCC~ | CUDA Toolkit/CCE/LLVM~/GCC~ | Intel LLVM | All. | Low-medium | Low | High (+10 y) |
| Kernel |  | | | | | | | |

<a id="some-wrapper-preprocessor-definitions-compiler-and-linker-flags"></a>

## Some wrapper, preprocessor definitions, compiler and linker flags

A very thorough list of compiler flag meaning across different vendor is given in [this document](https://flang.llvm.org/docs/OptionComparison.html).

<a id="flags-conversion-for-fortran-program"></a>

### Flags conversion for Fortran program

| Intel’s `ifort` | GCC’s `gfortran` | Cray’s `crayftn` | Note |
| --- | --- | --- | --- |
|  | `-g` |  | Embed debug info into the binary. Useful for stack trace and GDB. |
|  | `-Og` | `-eD` | Compile in debug mode. The `crayftn` option does a lot more than adding debug info though. |
| `-O1` | `-O1` | `-O1` |  |
| `-O2` | `-O2` | `-O1` |  |
| `-O3` | `-O3` | `-O2` |  |
| `-fast` | `-Ofast` | `-O3` |  |
| `-xHost` | `-march=native` | `-h cpu=<>` defined by the `craype-*` modules. | Careful, this flags assumes the machine on which you compile has similar CPUs to the one where your code run. |
| `-integer-size 32` |  | `-s integer32` |  |
| `-integer-size 64` | `-fdefault-integer-8` | `-s integer64` |  |
| `-real-size 64` | `-fdefault-real-8` | `-s real64` |  |
| `-ftz` | `ieee_support_underflow_control`/ `ieee_set_underflow_mode` | `ieee_support_underflow_control`/ `ieee_set_underflow_mode` | Flush denormal To Zero. If well designed, your code should not be very sensible to that. See the Fortran 2003 standard. |
| `-convert big_endian` | `-fconvert=big-endian` |  |  |
| `-fpe0` | `-ffpe-trap=invalid,zero,overflow` | ~ `-K trap=divz,inv,ovf` | For debug build only. |
|  | `-flto=thin` | `-hipa3` (bugged in cpe/23.03-24.07, use `-hipa0`) | Link Time Optimization (LTO) sometime called InterProcedural Optimization (IPO) or IPA. |

In case you use the GCC Fortran compiler and are subject to interface mismatch, use the `-fallow-argument-mismatch` flag. An interface mismatch, that is, when you pass arguments of different types to the same interface (subroutine) is not **standard conforming** Fortran code! Here is an excerpt of the GCC Fortran compiler manual: *Some code contains calls to external procedures with mismatches between the calls and the procedure definition, or with mismatches between different calls. Such code is non-conforming, and will usually be flagged with an error.* **Using** `-fallow-argument-mismatch` **is strongly discouraged. It is possible to provide standard-conforming code which allows different types of arguments by using an explicit interface and TYPE(*)**.

<a id="vectorizing-for-gcc-and-clang-based-compilers"></a>

### Vectorizing for GCC and Clang based compilers

To enable the vectorization of the multiply, add, div etc. and transcendental functions, we recommend the following flags:

| Compiler | Vectorizing flags | Vectorized `libm` flavor |
| --- | --- | --- |
| LLVM based | `-O3 -fno-math-errno` | [libmvec](https://sourceware.org/glibc/wiki/libmvec): `-fveclib=libmvec` |
| [AMDLIBM (libalm)](https://www.amd.com/en/developer/aocl/libm.html): `-fveclib=AMDLIBM -lamdlibm` (you may need to give the path to AMDLIBM) |
| [SVML](https://www.intel.com/content/www/us/en/docs/cpp-compiler/developer-guide-reference/2021-8/intrinsics-for-short-vector-math-library-ops.html): `-fveclib=SVML` |
| GCC based | `-O3 -fno-math-errno` | libmvec: `-funsafe-math-optimizations -ffinite-math-only` (**do not** specify the `-mveclibabi` flag) |
| (GCC >= 15) AMDLIBM (libalm): `-funsafe-math-optimizations -ffinite-math-only -mveclibabi=aocl` |
| (GCC >= 14, deprecated, low feature support) AMD Core Math: `-funsafe-math-optimizations -ffinite-math-only -mveclibabi=acml` |
| SVML: `-funsafe-math-optimizations -ffinite-math-only -mveclibabi=svml` |

Assuming the flags above, we have this table on Adastra:

| Compiler | Vector Library (option) | Language | | Vectorization (summary) | libm AVX Level / Notes |
| --- | --- | --- | --- | --- |
| **GCC 13** | default (none) | C / Fortran | None |  |
| **GCC 14** | libmvec (default) | C / Fortran | All vectorized except *erf* | AVX512 |
| acml (GCC ≥14) | C / Fortran | GCC uses libmvec instead of the one asked for | AVX512 |
| svml |
| aocl (GCC ≥15) |  |  |  |
| **AOCC** (clang, flang) (no specific flag for the fortran compiler) | default | C / Fortran | Only *sqrt* |  |
| svml | C | All vectorized | AVX512 |
| Fortran | None |  |
| libmvec | C | All vectorized | AVX512 |
| Fortran | None |  |
| AMDLIBM | C | All vectorized | AVX512 |
| Fortran | None |  |
| **Intel One API** (ifx, icpx) (no specific flag for the fortran compiler) | svml (default) | C | All vectorized | AVX512 |
| Fortran | None |  |
| libmvec | C | All vectorized except *erf* | AVX256 |
| Fortran | None |  |
| AMDLIBM | C / Fortran | None |  |
| **ROCm** (no specific flag for the fortran compiler) | default | C / Fortran | Only *sqrt* |  |
| libmvec | C | All vectorized except *erf* | AVX256 |
| Fortran | None |  |
| svml | C | All vectorized except *erf* | AVX512 |
| Fortran | None |  |
| AMDLIBM | C / Fortran | None |  |
| **Cray** (no specific flag for the fortran compiler) | default | C | Only *sqrt* |  |
| Fortran | All vectorized except *erf* (Cray libm) | AVX512 + Newton passes for sqrt |
| libmvec | C | All vectorized except *erf* | AVX256 |
| Fortran | All vectorized except *erf* (Cray libm) | AVX512 |
| svml | C | All vectorized except *erf* | AVX512 |
| Fortran | All vectorized except *erf* (Cray libm) | AVX512 |
| AMDLIBM | C | Only *sqrt* |  |
| Fortran | All vectorized except *erf* (Cray libm) | AVX512 |

Scarce documentation on the subject is available:

> - <https://gcc.gnu.org/onlinedocs/gcc/x86-Options.html#index-mveclibabi-1>
> - <https://clang.llvm.org/docs/ClangCommandLineReference.html#cmdoption-clang-fveclib>

**Note**

In GCC the default vectorized `libm` is `libmvec`. If you ask GCC to use an other vectorized `libm` it will first *check if the function exist in this library* and if not, fallback to `libmvec`.

**Note**

There are some inconsistencies between SVML/`libmvec` used by LLVM vs GCC. For instance, GCC’s `libmvec` will provide a vectorized `erfc` function while LLVM will not. The `libmvec` that LLVM uses only support up to AVX2 while the one GCC uses goes up to AVX512. Note that this is fixed if you use a recent GCC (and glibc/`libm`) or LLVM or AOCC etc..

**Warning**

When you choose a math library, it has to be linked with your product. `libmvec` is implied in GLIBC but SVML is not. If you use the Intel toolchain, it’ll link a static SVML ABI compatible library.

**Warning**

At least on `clang`, if you use LTO, the `libm` vectorizing flags must also be given at link time. This is a feature bug but understandable as machine code generation happens at link time when LTO is used. You are probably better of not using LTO and the flags given above.

Some LLVM vectorizer details are given in [this document](https://llvm.org/docs/Vectorizers.html). Some GCC vectorizer details are given in [this document](https://gcc.gnu.org/onlinedocs/gcc-14.2.0/gcc/x86-Options.html#index-mveclibabi-1).

<a id="examples"></a>

#### Examples

- LLVM (and derivative): using only `-O3`: <https://godbolt.org/z/v8KG8jvT1>, using vectorizing flags: <https://godbolt.org/z/KoYYWvnnx>, using vectorized `libm` `libmvec`: <https://godbolt.org/z/r4nj7EsWa>, using vectorized `libm` SVML: <https://godbolt.org/z/r7ePbnzdz>.
- GCC: using only `-O3`: <https://godbolt.org/z/415K6efeK>, using vectorizing flags: <https://godbolt.org/z/rGWsGqGMv>, using vectorized `libm` `libmvec`: <https://godbolt.org/z/dsEKK9KKd>, using vectorized `libm` AOCL: <https://godbolt.org/z/GqKzqM193>.

To showcase the vectorizer, take this simple C++ code:

```C++
#include <cmath>

void PackedSqrt(double* a) {
    for (int i = 0; i < 8; ++i) {
        a[i] = std::sqrt(a[i]);
    }
}
```

Without the above flags one would get this horrible code (some of it redacted for readability):

```
PackedSqrt(double*):
        sub     rsp, 24
        vxorpd  xmm1, xmm1, xmm1
        vmovsd  xmm0, QWORD PTR [rdi]
        vucomisd        xmm1, xmm0
        ja      .L23
        vsqrtsd xmm0, xmm0, xmm0
.L3:
        vmovsd  QWORD PTR [rdi], xmm0
        vmovsd  xmm0, QWORD PTR [rdi+8]
        vxorpd  xmm1, xmm1, xmm1
        vucomisd        xmm1, xmm0
        ja      .L24
        vsqrtsd xmm0, xmm0, xmm0
.L5:
        ...
        ...
.L26:
        mov     QWORD PTR [rsp+8], rdi
        call    sqrt
        mov     rdi, QWORD PTR [rsp+8]
        jmp     .L9
.L25:
        mov     QWORD PTR [rsp+8], rdi
        call    sqrt
        mov     rdi, QWORD PTR [rsp+8]
        jmp     .L7
.L24:
        mov     QWORD PTR [rsp+8], rdi
        call    sqrt
        mov     rdi, QWORD PTR [rsp+8]
        jmp     .L5
```

After adding the flags appropriate to the compiler you are using, it would look like so:

```
PackedSqrt(double*):
        vsqrtpd ymm0, ymmword ptr [rdi]
        vmovupd ymmword ptr [rdi], ymm0
        vsqrtpd ymm0, ymmword ptr [rdi + 32]
        vmovupd ymmword ptr [rdi + 32], ymm0
        vzeroupper
        ret
```

Some operations are not naturally vectorized by the hardware (no instruction for it, unlike the SQRT instruction `vsqrtpd` of the above example). In such case, a vectorized `libm` implementation is required. Observe what an improperly vectorized `sin` looks likes:

```C++
#include <cmath>

void PackedSin(double* a) {
    for (int i = 0; i < 8; ++i) {
        a[i] = std::sin(a[i]);
    }
}
```

Again, redacted for brevity:

```
PackedSin(double*):
        lea     r10, [rsp+8]
        and     rsp, -32
        push    QWORD PTR [r10-8]
        push    rbp
        mov     rbp, rsp
        push    r15
        push    r14
        push    r13
        push    r12
        push    r10
        push    rbx
        mov     rbx, rdi
        sub     rsp, 32
        vmovsd  xmm0, QWORD PTR [rdi]
        call    sin
        vmovq   r12, xmm0
        vmovsd  xmm0, QWORD PTR [rbx+8]
        call    sin
        vmovq   r14, xmm0
        vmovsd  xmm0, QWORD PTR [rbx+16]
        call    sin
        ...
        ...
        call    sin
        vmovsd  xmm7, QWORD PTR [rbp-72]
        vmovq   xmm3, r13
        vmovq   xmm4, r15
        vmovq   xmm5, r12
        vmovq   xmm6, r14
        vmovapd xmm2, xmm0
        vunpcklpd       xmm1, xmm3, xmm4
        vunpcklpd       xmm0, xmm5, xmm6
        vinsertf64x2    ymm0, ymm0, xmm1, 0x1
        vunpcklpd       xmm1, xmm7, xmm2
        vmovsd  xmm2, QWORD PTR [rbp-56]
        vmovupd YMMWORD PTR [rbx], ymm0
        vmovhpd xmm0, xmm2, QWORD PTR [rbp-64]
        vinsertf64x2    ymm0, ymm0, xmm1, 0x1
        vmovupd YMMWORD PTR [rbx+32], ymm0
        vzeroupper
        add     rsp, 32
        pop     rbx
        pop     r10
        pop     r12
        pop     r13
        pop     r14
        pop     r15
        pop     rbp
        lea     rsp, [r10-8]
        ret
```

After adding the flags appropriate to the compiler you are using, it could look like so (here we use the SVML vectorized `libm` implementation):

```
PackedSin(double*):
        push    rax
        vmovups ymm0, ymmword ptr [rdi]
        mov     rsi, qword ptr [rip + __svml_sin4_l9@GOTPCREL]
        call    rsi
        vmovups ymmword ptr [rdi], ymm0
        vmovups ymm0, ymmword ptr [rdi + 32]
        call    rsi
        vmovups ymmword ptr [rdi + 32], ymm0
        pop     rax
        vzeroupper
        ret
```

<a id="the-dread-of-ofast-ffast-math"></a>

#### The dread of `-Ofast`/`-ffast-math`

`-Ofast` implies `-O3 -ffast-math`.

The first thing to know about `-ffast-math` is that it is not magic, the reason why it is *faster* is because it is less exact (WRT the written code). This flag changes the optimization boundaries the compiler can apply. Less exact does not necessarily leads to a much *falser* [result](https://en.wikipedia.org/wiki/Fermi_problem). Typical HPC algorithms should be able to cope with denormal flushed to zero and should avoid having to deal with NaNs/Infs (lets say, it is too hard to get right for most).

Like `-OFast`, `-ffast-math` is an aggregate of other flags. These enable the compiler to disregard strict IEEE semantic.

The extent to which a compiler can change IEEE semantic is, from the user perspective, fuzzy to say the least. In this document <https://simonbyrne.github.io/notes/fastmath>, Simon Byrne has provided a summary of what `gcc` implies by `-ffast-math` and under which circumstances these optimizations can trigger.

Notably, `gcc`’s `-Ofast` is an aggregate of `-ffast-math -fallow-store-data-races`. `-ffast-math` is an aggregate of `` -fno-math-errno -funsafe-math-optimizations -ffinite-math-only -fno-rounding-math -fno-signaling-nans -fcx-limited-range -fexcess-precision=fast` ``. `-funsafe-math-optimizations` is an aggregate of `-fno-signed-zeros -fno-trapping-math -fassociative-math -freciprocal-math`. Additionally, `-ffast-math` adds the following preprocessor definition: `__FAST_MATH__`. `clang` being initially developed to match `gcc`’s most of this document is transferable.

The most dangerous out of `-ffast-math` are probably the `crtfastmath` shenanigans (see below) and the fact that it assume no NaNs or Infs (`-ffinite-math-only`). No NaNs implies that `std::isnan(x)` is always false. This can break an algorithm. But again, this should be rarely used in most HPC codes, and if used, it should be written by someone who knows what he’s doing and thus knows the extent of the compiler’s optimization boundaries.

`-fno-math-errno` is default in `gfortran` and (very) few HPC code care about `libm` + `errno`. It is safe to assume it can be enabled. The benefit is auto vectorization of `libm` functions. Indeed, without this flag, how would the `libm` report four (assuming double and AVX2) `errno` values in a single… `errno` variable.

All in all, the recommended flags would look like so:

`-fno-math-errno -fno-signed-zeros -fno-signaling-nans -fno-trapping-math -fassociative-math -freciprocal-math -fno-rounding-math -ffp-contract=fast`

Additionally resources:

- Towards Useful Fast-Math <https://www.youtube.com/watch?v=3Uf_3Su1NEc>;
- GCC flags details: <https://gcc.gnu.org/wiki/FloatingPointMath>, <https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html>;
- LLVM libc math library - Current status and future directions <https://www.youtube.com/watch?v=-8zb8rHbvcQ>;
- Floating Point in LLVM: the Good, the Bad, and the Absent <https://www.youtube.com/watch?v=sSNAGFXNXYU>;
- In addition to Simon Byrne’s post <https://kristerw.github.io/2021/10/19/fast-math>.

<a id="crtfastmath-c"></a>

##### `crtfastmath.c`

A note regarding `-funsafe-math-optimizations`. This option has nothing to do with fun and safe math optimization, especially when you use it at **link time** (not compile time). Note that this flag is implied by `-ffast-math` and thus `-Ofast`. If used at link time, `gcc`, up to version 13 and `clang`, will link a small object file that will end up changing the Floating Point Unit (FPU)’s IEEE denormal flushing mode (Flush to Zero (FTZ) and Denormal Are Zero (DAZ)). This file affects a *“thread local” global variable* (FPU control word) affecting for the whole main thread and its `clone()d` children. This behavior has been present since at least 2004 and is fixed in [this GCC bug report](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55522).

This is why you should never use `-Ofast`, instead stick to `-O3` which you can safely use at link time. And if you want the `-fast-math` benefit, just add the flag for compilation targets, and **not in the set of linker flags**.

<a id="intel-llvm-s-defaults"></a>

<a id="adastra-programming-environment-wrapper-flags-intel-llvm"></a>

### Intel LLVM’s defaults

Intel LLVM (and its predecessor toolchain Intel classic) is known to default to `clang`’s’ `-ffp-model=fast` which is roughly equivalent to `-funsafe-math-optimizations`, so the compiler will [sneakily](https://godbolt.org/z/o6Mrj3f9e) add the following flags:

`-fapprox-func -funsafe-math-optimizations -fno-signed-zeros -mreassociate -freciprocal-math -fdenormal-fp-math=preserve-sign,preserve-sign -ffp-contract=fast`

These flags are part of what is provided by `-ffast-math` (which you may know under the `-Ofast` option). This means is that Intel is close to `-Ofast` except for `-menable-unsafe-fp-math -menable-no-nans -menable-no-infs` which are missing in Intel LLVM’s `-O3` but present in `-Ofast`.

**Warning**

Do not worship Intel’s compiler performance. `icc`/`icpc` and now `icx`/`icpx` simply rely on optimization close to `-ffast-math` to improve vectorization at the cost of accuracy. Intel LLVM is but a glorified LLVM fork with modified default optimization level and a decent vectorized `libm` (SVML).

<a id="debugging-with-crayftn"></a>

### Debugging with `crayftn`

**Note**

To flush the output stream (stdout) is a **standard way**, use the `output_unit` named constant in the `ISO_Fortran_env` module. E.G.: `flush(output_unit)`. This is useful when debugging using the classic print/comment approach.

| Feature/flag/environment variable | Explanation |
| --- | --- |
| `-eD` | The -eD option enables all debugging options. This option is equivalent to specifying the -G0 option with the -m2, -rl, -R bcdsp, and -e0 options. |
| `-e0` | Initializes all undefined local stack, static, and heap variables to 0 (zero). If a user variable is of type character, it is initialized to NUL. If logical, initialized to false. The stack variables are initialized upon each execution of the procedure. When used in combination with -ei, Real and Complex variables are initialized to signaling NaNs, while all other typed objects are initialized to 0. Objects in common blocks will be initialized if the common block is declared within a BLOCKDATA program unit compiled with this option. |
| `-ei` | Initializes all undefined local stack, static, and heap variables of type REAL or COMPLEX to an invalid value (signaling NaN). |
| `-en` | Generates messages to note nonstandard Fortran usage. |
| `-hfp0=noapprox` | Controls the level of floating point optimizations, where n is a value between 0 and 4, with 0 giving the compiler minimum freedom to optimize floating point operations and 4 giving it maximum freedom. `noapprox` prevents rewrites of square root and divide expressions using hardware reciprocal approximations. |
| `-hflex_mp=intolerant` | Has the highest probability of repeatable results, but also the highest performance penalty. |
| `-hlist=m` | Produces a source listing with loopmark information. To provide a more complete report, this option automatically enables the -O negmsg option to show why loops were not optimized. If you do not require this information, use the -O nonegmsg option on the same command line. Loopmark information will not be displayed if the -d B option has been specified. |
| `-hlist=a` | Include all reports in the listing (including source, cross references, options, lint, loopmarks, common block, and options used during compilation). |
| `-hbounds` | Enable bound checking. |

A typical set of debugging flag could be `-eD -ei -en -hbounds -K trap=divz,inv,ovf`.

`crayftn` also offers sanitizers which turn on runtime checks for various forms of undefined or suspicious behavior. This is an **experimental feature** (in CrayFTN 17). If a check fails, a diagnostic message is produced at runtime explaining the problem.

| Feature/flag/environment variable | Explanation |
| --- | --- |
| `-fsanitize=address` | Enables a memory error detector. |
| `-fsanitize=thread` | Enables a data race detector. |

Further reading: `man crayftn`.

<a id="debugging-with-gfortran"></a>

### Debugging with `gfortran`

A typical set of debugging flag could be `-O1 -g -fcheck=all -ffpe-trap=invalid,zero,overflow -fbacktrace` or `-O1 -g -fcheck=all -ffpe-trap=invalid,zero,overflow -fbacktrace -finit-real=snan -finit-integer=42 -finit-logical=true -finit-character=0` (this set of option will silence `-Wuninitialized`).

<a id="making-the-cray-wrappers-spew-their-implicit-flags"></a>

<a id="adastra-programming-environment-wrapper-flags-spewing"></a>

### Making the Cray wrappers spew their implicit flags

**Warning**

If you do not rely on the wrappers (CC/cc/ftn), you will have to specify the architecture you are compiling for via, typically the `-march` flag.

Assuming you have loaded an environment such as:

```shell-session
$ module purge
$ # A CrayPE environment version
$ module load cpe/24.07
$ # An architecture
$ module load craype-accel-amd-gfx90a craype-x86-trento
$ # A compiler to target the architecture
$ module load PrgEnv-cray
$ module load amd-mixed/6.1.2
```

The `CC`, `cc` and `ftn` Cray wrappers imply a lot of flags that you may want to retrieve.

At least three flags are of significance, `-craype-verbose` which dumps all the flags the wrapper is going to forward to the underlying compiler driver. `--cray-bypass-pkgconfig` which prevent the Cray wrapper from discovering which library module are loaded (`cray-mpich`/`cray-libsci`) and only take architecture modules into account (say, `craype-x86-genoa`). Finally, `--cray-print-opts` which is the negation of `--cray-bypass-pkgconfig`, it prints only information related to library modules loaded.

This can be done like so:

```shell-session
$ CC -craype-verbose main.cc
clang++ -march=znver3 -dynamic -D__CRAY_X86_TRENTO -D__CRAY_AMD_GFX90A -D__CRAYXT_COMPUTE_LINUX_TARGET -isystem /opt/cray/pe/cce/18.0.0/cce-clang/x86_64/lib/clang/18/include -isystem /opt/cray/pe/cce/18.0.0/cce/x86_64/include/craylibs -Wl,-rpath=/opt/cray/pe/cce/18.0.0/cce/x86_64/lib main.cc -I/opt/cray/pe/libsci/24.07.0/CRAY/18.0/x86_64/include -I/opt/cray/pe/mpich/8.1.30/ofi/cray/18.0/include -I/opt/cray/pe/dsmml/0.3.0/dsmml/include -L/opt/cray/pe/libsci/24.07.0/CRAY/18.0/x86_64/lib -L/opt/cray/pe/mpich/8.1.30/ofi/cray/18.0/lib -L/opt/cray/pe/mpich/8.1.30/gtl/lib -L/opt/cray/pe/dsmml/0.3.0/dsmml/lib -Wl,--as-needed,-lsci_cray_mpi,--no-as-needed -lmpi_gtl_hsa -Wl,--as-needed,-lsci_cray,--no-as-needed -ldl -Wl,--as-needed,-lmpi_cray,--no-as-needed -lmpi_gtl_hsa -Wl,--as-needed,-ldsmml,--no-as-needed -L/opt/cray/pe/cce/18.0.0/cce/x86_64/lib/pkgconfig/../ -Wl,--as-needed,-lstdc++,--no-as-needed -Wl,--as-needed,-lpgas-shmem,--no-as-needed -lfi -lquadmath -lmodules -lfi -lcraymath -lf -lu -lcsup -Wl,--as-needed,-lpthread,-latomic,--no-as-needed -Wl,--as-needed,-lm,--no-as-needed -Wl,--disable-new-dtags
$ CC --cray-bypass-pkgconfig -craype-verbose main.cc
clang++ -march=znver3 -dynamic -D__CRAY_X86_TRENTO -D__CRAY_AMD_GFX90A -D__CRAYXT_COMPUTE_LINUX_TARGET -isystem /opt/cray/pe/cce/18.0.0/cce-clang/x86_64/lib/clang/18/include -isystem /opt/cray/pe/cce/18.0.0/cce/x86_64/include/craylibs -Wl,-rpath=/opt/cray/pe/cce/18.0.0/cce/x86_64/lib main.cc -L/opt/cray/pe/cce/18.0.0/cce/x86_64/lib/pkgconfig/../ -Wl,--as-needed,-lstdc++,--no-as-needed -Wl,--as-needed,-lpgas-shmem,--no-as-needed -lfi -lquadmath -lmodules -lfi -lcraymath -lf -lu -lcsup -Wl,--as-needed,-lpthread,-latomic,--no-as-needed -Wl,--as-needed,-lm,--no-as-needed -Wl,--disable-new-dtags
$ CC --cray-print-opts=cflags
-I/opt/cray/pe/libsci/24.07.0/CRAY/18.0/x86_64/include -I/opt/cray/pe/mpich/8.1.30/ofi/cray/18.0/include -I/opt/cray/pe/dsmml/0.3.0/dsmml/include
$ CC --cray-print-opts=libs
-L/opt/cray/pe/libsci/24.07.0/CRAY/18.0/x86_64/lib -L/opt/cray/pe/mpich/8.1.30/ofi/cray/18.0/lib -L/opt/cray/pe/mpich/8.1.30/gtl/lib -L/opt/cray/pe/dsmml/0.3.0/dsmml/lib -Wl,--as-needed,-lsci_cray_mpi,--no-as-needed -lmpi_gtl_hsa -Wl,--as-needed,-lsci_cray,--no-as-needed -ldl -Wl,--as-needed,-lmpi_cray,--no-as-needed -lmpi_gtl_hsa -Wl,--as-needed,-ldsmml,--no-as-needed -L/opt/cray/pe/cce/18.0.0/cce/x86_64/lib/pkgconfig/../ -Wl,--as-needed,-lstdc++,--no-as-needed -Wl,--as-needed,-lpgas-shmem,--no-as-needed -lfi -lquadmath -lmodules -lfi -lcraymath -lf -lu -lcsup
```

We observe the implied compile and link flags for Cray MPICH (the GTL is here too) and the LibSci. Had you used a `cray-hdf5` or some other Cray modules libraries, it would have been in commands’ output.

**Warning**

The `libs` option return a list of linker flags containing instances of `-Wl`. This can create serious CMake confusion. For this reason, we recommend that you strip them away like so: `CRAY_WRAPPER_LINK_FLAGS="$({ cc --cray-print-opts=libs; CC --cray-print-opts=libs; ftn --cray-print-opts=libs; } | tr '\n' ' ' | sed -e 's/-Wl,--as-needed,//g' -e 's/,--no-as-needed//g')"`.

**Once you have extracted the flags for a given CPE version you can store them in a machine/toolchain file.**

Say you use CMake, here is an example of what you could use the above for:

```shell-session
$ CRAY_WRAPPER_LINK_FLAGS="$({ cc --cray-print-opts=libs; CC --cray-print-opts=libs; ftn --cray-print-opts=libs; } | tr '\n' ' ' | sed -e 's/-Wl,--as-needed,//g' -e 's/,--no-as-needed//g')"
$ cmake \
    -DCMAKE_C_COMPILER=craycc \
    -DCMAKE_CXX_COMPILER=crayCC \
    -DCMAKE_Fortran_COMPILER=crayftn \
    -DCMAKE_C_FLAGS="$(cc --cray-print-opts=cflags)" \
    -DCMAKE_CXX_FLAGS="$(CC --cray-print-opts=cflags)" \
    -DCMAKE_Fortran_FLAGS="$(ftn --cray-print-opts=cflags)" \
    -DCMAKE_EXE_LINKER_FLAGS="${CRAY_WRAPPER_LINK_FLAGS}" \
    ..
```

Here we bypass all Cray wrappers (C/C++ and Fortran) and give CMake all the flags the wrapper would have implicitly added. This is clearly the recommended way in case the wrapper causes you problems. We give multiple examples for compilers other than Cray in [this document](../software_stack/tools/index.md#adastra-software-stack-tools-building-cmake-example-kk-hip-openmp) for a build of kokkos with a HIP and OpenMP CPU backend. the build is done using the Cray, `amdclang++` or `hipcc` drivers. The above is transposable to other build system/generator than CMake.

**Note**

The Cray wrappers use `-I` and not `-isystem` which is suboptimal for *strict* code using many warning flags (as it should be).

**Note**

Use the `-craype-verbose` flag to display the command line produced by the Cray wrapper. This must be called on a file to see the full output (i.e., `CC -craype-verbose test.cpp`). You may also try the `--verbose` flag to ask the underlying compiler to show the command it itself launches.

<a id="crayftn-optimization-level-details"></a>

### `crayftn` optimization level details

Now we provide a list of the differences between the flags implicitly enabled when either `-O1`, `-O2` or `-O3`. Understand that `-O3` under the `crayftn` compiler is very aggressive and could be said to at least *equate* `-Ofast` under your typical Clang or GCC when it comes to the floating point optimizations.

**Warning**

The `crayftn` compiler possess an extremely powerful optimizer which does of the most aggressive optimizations a compiler can afford to do. This means that using a high optimization level, the optimizer will assume your code has a **strong standard compliance**. Any slight deviation from the standard can lead to significant issue in the code, from crash to silent corruption. `crayftn`’s `-O2 -hipa0` is considered stable, safe and comparable to the `-O3` of other compilers. The `-hipaN` option has lead to issues in some codes.

**Warning**

Cray reserves the right to change, for a new `crayftn` version, the options enabled through `-On`.

The options given below are bound to `Cray Fortran : Version 15.0.1`. This may change with past and future versions.

`-O1` provides:

```
-h scalar1,vector1,unroll2,fusion2,cache0,cblock0,noaggress
-h ipa1,mpi0,pattern,modinline
-h fp2=approx,flex_mp=default,alias=default:standard_restrict
-h fma
-h autoprefetch,noconcurrent,nooverindex,shortcircuit2
-h noadd_paren,nozeroinc,noheap_allocate
-h align_arrays,nocontiguous,nocontiguous_pointer
-h nocontiguous_assumed_shape
-h fortran_ptr_alias,fortran_ptr_overlap
-h thread1,nothread_do_concurrent,noautothread,safe_addr
-h noomp -f openmp-simd
-h caf,noacc
-h nofunc_trace,noomp_analyze,noomp_trace,nopat_trace
-h nobounds
-h nomsgs,nonegmsgs,novector_classic
-h dynamic
-h cpu=x86-64,x86-trento,network=slingshot10
-h nofp_trap -K trap=none
-s default32
-d 0abcdefgijnpvxzBDEGINPQSZ
-e hmqwACFKRTX
```

The discrepancies shown between `-O1` and `-O2` are:

```
-h scalar2,vector2
-h ipa3
-h thread2
```

The discrepancies shown between `-O2` and `-O3` or `-Ofast` are:

```
-h scalar3,vector3
-h ipa4
-h fp3=approx
```

<a id="aocc-flags"></a>

### AOCC flags

AMD gives a detailed description of the CPU optimization flags here: <https://rocm.docs.amd.com/en/docs-5.5.1/reference/rocmcc/rocmcc.html#amd-optimizations-for-zen-architectures>.

<a id="understanding-your-compiler"></a>

### Understanding your compiler

GCC offers the following two flag combination that allows you to dig deeper into the default choices made to compiler for your architecture.

```shell-session
$ gcc -Q --help=target
$ # Works for clang too:
$ gcc -dM -E -march=znver3 - < /dev/null
```

<a id="predefined-preprocessor-definitions"></a>

#### Predefined preprocessor definitions

It can be useful to wrap code inside preprocessor control flow (`ifdef`). We provide some definitions that can help choose a path for workaround code.

| Feature/flag/environment variable | Explanation |
| --- | --- |
| `__INTEL_CLANG_COMPILER` | For the C/C++ languages, the compiler is Intel’s new compiler `icx/icpx` (Intel LLVM), a fork of clang. |
| `__INTEL_COMPILER` | For the C/C++ languages, the compiler is intel’s old compiler `icc/icpc` (Intel classic) or the new Intel LLVM toolchain. |
| `__clang__=1` | For the C/C++ languages, the compiler is Clang **or one of its downstream fork**. |
| `__GNUC__=1` | For the Fortran language, the compiler is GNU CC (GCC) **or a compiler mimicking it**. |
| `_MSC_VER=1` | For the C/C++ languages, the compiler is Microsoft MSVC **or a compiler mimicking it**. |
| `__cray__=1` | For the C/C++ languages, the compiler is Cray (a superset of clang). |
| `_CRAYFTN=1` | For the Fortran language, the compiler is Cray. |

<a id="advanced-tips-and-flags-and-environment-variable-for-debugging"></a>

### Advanced tips and flags and environment variable for debugging

See [LLVM Optimization Remarks](https://www.youtube.com/watch?v=qmEsx4MbKoc) by Ofek Shilon for more details on what Clang can tell you about how it optimizes you code and what tools are available to process that information.

These flags could be of help:

```
-Rpass=.*
-Rpass=openmp-opt -Rpass-analysis=openmp-opt -Rpass-missed=openmp-opt
-Rpass-missed=.*
-Rpass-analysis=.*
-Rpass-analysis=loop-vectorize
-Rpass-analysis=loop-distribute
-foptimization-record-file=<file>
(For AMD GPU targets) -Rpass-analysis=kernel-resource-usage
```

**Note**

The `crayftn` compiler does **not** provide an option to trigger debug info generation while also, not lowering optimization.

<a id="job-submission"></a>

<a id="adastra-running-jobs"></a>

# Job submission

[SLURM](https://slurm.schedmd.com/) is the workload manager used to interact with the compute nodes on Adastra. In the following subsections, the most commonly used SLURM commands for submitting, running, and monitoring jobs will be covered, but users are encouraged to visit the official documentation and man pages for more information. This section describes how to run programs on the Adastra compute nodes, including a brief overview of SLURM and also how to map processes and threads to CPU cores and GPUs.

<a id="the-slurm-batch-scheduler-and-job-launcher"></a>

<a id="adastra-running-jobs-slurm-scheduler-job-launch"></a>

## The SLURM batch scheduler and job launcher

SLURM provides multiple ways of submitting and launching jobs on Adastra’s compute nodes: batch scripts, interactive, and single-command. The SLURM commands allowing these methods are shown in the table below and examples of their use can be found in the related subsections. Please note that regardless of the submission method used, the job will launch on compute nodes, with the first node in the allocation serving as head-node.

With SLURM, you first ask for resources (a number of node, of GPU, of CPU) and then you distribute these resources on your tasks.

|  |  |
| --- | --- |
| `sbatch` | Used to submit a batch script. The batch script can contain information on the amount of resources to allocate and how to distribute them. Options can be specified when specifying the `sbatch` command flags or inside the script, at the top of the file after the following prefix `#SBATCH`. The `sbatch` options do not necessarily lead to the resource distribution per rank that you would expect (!). `sbatch` allocates, `srun` distributes.  See [Batch scripts](index.md#adastra-running-jobs-batch-scripts) for more details. |
| `srun` | Used to run a parallel job (job step) on the resources allocated with `sbatch` or `salloc`.  If necessary, `srun` will first create a resource allocation in which to run the parallel job(s). |
| `salloc` | Used to allocate an interactive SLURM job allocation, where one or more job steps (i.e., `srun` commands) can then be launched on the allocated resources (i.e., nodes).  See [Interactive jobs](index.md#adastra-running-jobs-interactive-jobs) for more details. |

<a id="batch-scripts"></a>

<a id="adastra-running-jobs-batch-scripts"></a>

## Batch scripts

A batch script can be used to submit a job to run on the compute nodes at a later time (the module used in the scripts below are here as an indication, you may not need them if you use PyTorch, Tensorflow or the [CINES Spack modules](../software_stack/cines_software_stack/spack.md#adastra-software-stack-cines-software-stack-spack-introduction)). In this case, stdout and stderr will be written to a file(s) that can be opened after the job completes. Here is an example of a simple batch script for the **GPU (MI250) partition**:

```shell
 1#!/bin/bash
 2#SBATCH --account=<account_to_charge>
 3#SBATCH --job-name="<job_name>"
 4#SBATCH --constraint=MI250
 5#SBATCH --nodes=1
 6#SBATCH --exclusive
 7#SBATCH --time=1:00:00
 8
 9module purge
10
11# A CrayPE environment version
12module load cpe/24.07
13# An architecture
14module load craype-accel-amd-gfx90a craype-x86-trento
15# A compiler to target the architecture
16module load PrgEnv-cray
17# Some architecture related libraries and tools
18module load amd-mixed
19
20module list
21
22export MPICH_GPU_SUPPORT_ENABLED=1
23
24# export OMP_<ICV=XXX>
25
26srun --ntasks-per-node=8 --cpus-per-task=8 --threads-per-core=1 --gpus-per-task=1 --gpu-bind=closest -- <executable> <arguments>
```

Here is an example of a simple batch script for the **GPU (MI300A) partition**:

```shell
 1#!/bin/bash
 2#SBATCH --account=<account_to_charge>
 3#SBATCH --job-name="<job_name>"
 4#SBATCH --constraint=MI300
 5#SBATCH --nodes=1
 6#SBATCH --exclusive
 7#SBATCH --time=1:00:00
 8
 9module purge
10
11# A CrayPE environment version
12module load cpe/24.07
13# An architecture
14module load craype-accel-amd-gfx942 craype-x86-genoa
15# A compiler to target the architecture
16module load PrgEnv-cray
17# Some architecture related libraries and tools
18module load amd-mixed
19
20module list
21
22export MPICH_GPU_SUPPORT_ENABLED=1
23# # If you used unified memory (HSA_XNACK=1), also define:
24# export MPICH_GPU_MANAGED_MEMORY_SUPPORT_ENABLED=1
25
26# export OMP_<ICV=XXX>
27
28srun --ntasks-per-node=4 --cpus-per-task=24 --threads-per-core=1 --gpus-per-task=1 --gpu-bind=closest -- <executable> <arguments>
```

Here is an example of a simple batch script for the **CPU (GENOA) partition**:

```shell
 1#!/bin/bash
 2#SBATCH --account=<account_to_charge>
 3#SBATCH --job-name="<job_name>"
 4#SBATCH --constraint=GENOA
 5#SBATCH --nodes=1
 6#SBATCH --exclusive
 7#SBATCH --time=1:00:00
 8
 9module purge
10
11# A CrayPE environment version
12module load cpe/24.07
13# An architecture
14module load craype-x86-genoa
15# A compiler to target the architecture
16module load PrgEnv-cray
17
18module list
19
20
21
22
23
24# export OMP_<ICV=XXX>
25
26srun --ntasks-per-node=24 --cpus-per-task=8 --threads-per-core=1 -- <executable> <arguments>
```

Assuming the file is called `job.sh` on the disk, you would launch it like so: `sbatch job.sh`.

Options encountered after the first non-comment line will not be read by SLURM. In the example script, the lines are:

| Line | Description |
| --- | --- |
| 1 | Shell interpreter line. |
| 2 | GENCI/DARI project to charge. More on that [below](index.md#adastra-running-jobs-resource-charging). |
| 3 | Job name. |
| 4 | Type of Adastra node requested (here, the GPU MI250 or CPU GENOA partition). |
| 5 | Number of compute nodes requested. |
| 6 | Ask SLURM to reserve whole nodes. If this is not wanted, see [Shared mode vs exclusive mode](index.md#adastra-running-jobs-shared-exclusive-mode). |
| 7 | Specify where the stderr and stdout streams should be saved to disk. |
| 8 | Wall time requested (`HH:MM:SS`). |
| 10-19 | Setup the module environment, always starting with a purge. |
| 21 | (For the MI250/MI300 partition script) Enable GPU aware MPI. You can pass GPU buffers directly to the MPI APIs. |
| 25 | Potentially, setup some OpenMP environment variables. |
| 27 | Implicitly ask to use all of the node allocated. Then we distribute the work on 8 or 24 tasks per node. We also specify that the tasks should be bound to 8 cores, without [Simultaneous Multithreading (SMT)](https://en.wikipedia.org/wiki/Simultaneous_multithreading) and to the closest GPU to these 8 cores. |

The SLURM submission options are preceded by `#SBATCH`, making them appear as comments to a shell (since comments begin with `#`). SLURM will look for submission options from the first line through the first non-comment line. The **mandatory** SLURM flags are, the account identifier (also called project ID or project name and specified via `--account=`), more on that [later](index.md#adastra-running-jobs-resource-charging), the type of node (via `--constraint=`), the maximal job runtime duration (via `--time=`) and the number of nodes (via `--nodes=`).

Some more advanced scripts are available in [this document](../software_stack/simulation_software/index.md#adastra-software-stack-simulation-software-script-and-tips) and [this repository](https://dci-gitlab.cines.fr/external/adastra-examples/-/tree/main/SLURM) (though, the scripts of this repository are quite old).

**Warning**

A proper binding is often critical for HPC applications (on MI300A you can expose yourself to x11-x27 slowdowns!). We strongly recommend that you either make sure your binding is correct (say, using this tool [hello_cpu_binding](https://dci-gitlab.cines.fr/external/adastra-examples/-/tree/main/hello_cpu_binding)) or that you take a look at the binding scripts presented in [Proper binding, why and how](../porting_optimization/index.md#porting-optimization-performance-tuning-monitoring-proper-binding-why-how).

**Note**

The binding `srun` does is only able to restrict a rank to a set of thread (process affinity towards hardware threads). It does not do what is called thread pinning/affinity. To exploit thread pinning, you may want to check OpenMP’s `${OMP_PROC_BIND}` and `${OMP_PLACES}` Internal Control Variables (ICVs)/environment variables. Bad thread pinning can be detrimental to performance. Check [this document](../porting_optimization/index.md#porting-optimization-performance-tuning-monitoring-proper-pinning-why-how) for more details.

The typical OpenMP ICVs used **prevent** and diagnose thread affinity issues rely on the following environment variable:

```shell
# Logs the rank to core/thread placement is correct.
export OMP_DISPLAY_AFFINITY=TRUE
export OMP_PROC_BIND=CLOSE
export OMP_PLACES=THREADS
# This should be redundant because srun already restrict the rank's CPU
# access.
export OMP_NUM_THREADS=<N>
```

**Note**

If you use a binding script such as [this one](../porting_optimization/detailed_binding_script.md#porting-optimization-detailed-binding-script), you do not need these, except maybe `OMP_DISPLAY_AFFINITY`.

<a id="shared-mode"></a>

### Shared mode

In [shared mode](index.md#adastra-running-jobs-shared-exclusive-mode), you will have to share resources with other users. That means you will likely be using a node with someone else (and potentially, suffer some performance degradation).

**Note**

For both CPU and GPU partitions, we recommend 3 additional `sbatch` flags: `--ntasks-per-node=`, `--cpus-per-task=` and `--threads-per-core=`. These describe the “sub node” amount of resource you whish to consume.

**Note**

For the GPU partitions, you also have to specify `--gpus-per-node=`.

Here is an example of a simple batch script for the **GPU (MI250) partition**, 2 tasks, 1 GPU and 8 threads (using 8 cores and **no** hyperthreading) per task:

```shell
#!/bin/bash
#SBATCH --account=<account_to_charge>
#SBATCH --job-name="<job_name>"
#SBATCH --constraint=MI250
#SBATCH --nodes=1
# #SBATCH --exclusive # Shared !
#SBATCH --ntasks-per-node=2
#SBATCH --gpus-per-node=2
#SBATCH --cpus-per-task=8
#SBATCH --threads-per-core=1
#SBATCH --time=1:00:00

module purge

# A CrayPE environment version
module load cpe/24.07
# An architecture
module load craype-accel-amd-gfx90a craype-x86-trento
# A compiler to target the architecture
module load PrgEnv-cray
# Some architecture related libraries and tools
module load amd-mixed

module list

export MPICH_GPU_SUPPORT_ENABLED=1

# export OMP_<ICV=XXX>

srun --ntasks-per-node=2 --cpus-per-task=8 --threads-per-core=1 --gpus-per-task=1 --gpu-bind=closest -- <executable> <arguments>
```

Here is an example of a simple batch script for the **CPU (GENOA) partition**, 20 tasks, 16 threads (using 8 cores and hyperthreading) per task:

```shell
#!/bin/bash
#SBATCH --account=<account_to_charge>
#SBATCH --job-name="<job_name>"
#SBATCH --constraint=GENOA
#SBATCH --nodes=1
# #SBATCH --exclusive # Shared !
#SBATCH --ntasks-per-node=20
#SBATCH --cpus-per-task=16 # 16 threads or 16/2 cores.
#SBATCH --threads-per-core=2
#SBATCH --time=1:00:00

module purge

# A CrayPE environment version
module load cpe/24.07
# An architecture
module load craype-x86-genoa
# A compiler to target the architecture
module load PrgEnv-cray

module list

# export OMP_<ICV=XXX>

srun --ntasks-per-node=20 --cpus-per-task=16 --threads-per-core=2 -- <executable> <arguments>
```

<a id="common-slurm-submission-options"></a>

<a id="adastra-running-jobs-common-slurm-options"></a>

## Common SLURM submission options

The table below summarizes commonly-used SLURM job submission options:

| Command (long or short) | Description |
| --- | --- |
| `--account=<account_to_charge>` or `-A <account_to_charge>` | Account identifier (also called project ID) to use and charge for the compute resources consumption. More on that [below](index.md#adastra-running-jobs-resource-charging). |
| `--constraint=<node_type>` | Type of Adastra node. The accepted values are `MI250`, `GENOA` and `HPDA`. The first two values represent the two main partitions of Adastra. |
| `--time=<maximum_duration>` or `-t <maximum_duration>` | Maximum duration as wall clock time `HH:MM:SS`. |
| `--nodes=<number_of_nodes>` or `-N <number_of_nodes>` | Number of compute nodes. |
| `--job-name="<job_name>"` or `-J <job_name>` | Name of job. |
| `--output=<file_name>` or `-o <file_name>` | Standard output file name. |
| `--error=<file_name>` or `-e <file_name>` | Standard error file name. |

For more information about these or other options, please see the `sbatch` man page.

<a id="resource-consumption-and-charging-accounting"></a>

<a id="adastra-running-jobs-resource-charging"></a>

## Resource consumption and charging (accounting)

French computing site resources are represented in hour of use of a given resource type. For instance, at CINES, if you have been given 100’000 hours on Adastra’s MI250X partition, it means that you could use a single unit of MI250X resource for 100’000 hours. It also means that you could use 400 units of MI250X resource for 250 hours. The units are given below:

| Computing resource | Unit description | Example |
| --- | --- | --- |
| MI250X partition | 2 GCD (GPU device) of an MI250X card, that is, a whole MI250X. | 1 hour on a MI250X node (exclusive) = 4 MI250X hours. |
| MI300A partition | 1 GPU device. | 1 hour on a MI300A node (exclusive) = 4 MI300A hours. |
| GENOA partition | 1 core (2 logical threads). | 1 hour on a GENOA node (exclusive) = 192 GENOA core hours. |

**Warning**

Due to an historical mistake, the eDARI website uses a unit for the MI250X partition that is a whole MI250X instead of the GCDs which is a half of an MI250X. If you ask for 50 MI250X hours on eDARI, you can in practice, use 100 MI250X GCD hours.

**Warning**

The CPU quantity reported by SLURM (for instance via `sacct -j <jome_name>`) is in hardware threads, not cores. We have 2 hardware threads per core on the CPUs of the Adastra partitions.

The resources you will consume **will have to be charged** to a project. Multiple times in this document have we invoked the `--account=<account_to_charge>` SLURM flag. Before submitting the job, make sure you have set a valid `<account_to_charge>`. You can obtain the list of account you are attached to by running the `myproject -l` command. The values representing the account name you can charge are on the last line of the command output (i.e.: `Liste des projets de calcul associés au user someuser : ['bae1234', 'eat4567', 'afk8901']`). More on `myproject` in the [Login unique](index.md#adastra-accessing-unique-login) section.

The maximum job duration, on all partitions except HPDA is 24 hours. Extensible on rare occasions, contact [svp@cines.fr](mailto:svp%40cines.fr). We do not limit the user’s job size, you can use as many nodes as you wish.

We do not charge for HPDA resources.

In addition, the `<constraint>` in `--constraint=<constraint>` should be set to [a proper value](index.md#adastra-running-jobs-common-slurm-options) as it is this SLURM flag that describes the kind of resource you will request and thus, that CINES will charge.

**Note**

To monitor your compute hours consumption, use the `myproject --state [project]` command or visit <https://reser.cines.fr/>.

**Warning**

The charging gets a little bit less simple when you use the [shared nodes](index.md#adastra-running-jobs-shared-exclusive-mode).

<a id="shared-mode-vs-exclusive-mode"></a>

<a id="adastra-running-jobs-shared-exclusive-mode"></a>

### Shared mode vs exclusive mode

Some nodes are reserved for what we call share mode, which **differs** from the exclusive mode found in many of the batch scripts presented in this documentation (observe the `--exclusive` SLURM flag). The role of theses shared nodes is the following: when a resource allocation, be it through `salloc` or `sbatch`, asks for less than what a whole node offers, your allocation will automatically be *rerouted* to the pool of shared nodes (the `[genoa|mi250]-shared` SLURM partitions). On these, you may have to share the node with other users. That said, **we maintain isolation** of the resources, one job can not access the resources (GPUs/cores/memory) allocated by an other job (or other user), even if both jobs reside on the same node. For now, the shared mechanism is available on **some nodes** of both the MI250 and GENOA partitions and active on the whole HPDA partition.

On the GENOA and MI250 partitions, the smallest amount of core you can get charged for is **8**. This is so that we map an allocation to a hardware resource (L3 cache or NUMA nodes), **limiting the impact on users sharing the same node**.

**Note**

Conceptually, if you ask for say, 2/4 of a node’s CPU cores and for 3/4 of a node’s memory we will charge you for 3/4 of a node’s CPU cores. In this case, note that you **will not** have access to 3/4 of the CPU cores even though we charge for it. To specify the amount of memory per node use `--mem=<N>G` where `<N>` is an amount in Gio. The same logic applies to GPUs.

**Warning**

When submitting a multi-node job, it will run in exclusive mode, billing for all allocated nodes regardless of actual resource use.

Lets have a practical example, say you want to schedule a very small job running **2 tasks**, each using **8 cores** of the GENOA partition. You could reserve a whole node via `--exclusive` but CINES would then **charge** you for all the 192 cores of the node, effectively wasting 176 cores; instead, to benefit from the shared nodes, you will **not** use the `--exclusive` flag:

```shell-session
$ salloc --account=<account_to_charge> --job-name="interactive" --constraint=GENOA --nodes=1 --ntasks-per-node=2 --cpus-per-task=8 --time=1:00:00
salloc: INFO : Considering its requirements, this job is treated in SHARED mode.
salloc: INFO : We cannot guarantee the performance reproducibility of such small jobs in this mode,
salloc: INFO : but they are only charged for the needed resources.
salloc:
salloc: INFO : As you didn't ask threads_per_core in your request: 2 was taken as default
salloc: INFO : This job requests 8 cores. Due to shared usage this job will be charged for 8 cores (of the 192 cores of the node)
salloc: Pending job allocation 41328
salloc: job 41328 queued and waiting for resources
salloc: job 41328 has been allocated resources
salloc: Granted job allocation 41328
```

Note the message written to your shell. We see that 8 cores will be allocated and charged, instead of the 192. Also, the shared mechanism informs us that we will have 2 threads per core (called hyperthreading or SMT) for a total of 16 threads available to your program. This may **not** be what one wants, indeed core and thread are different! In the textual description above, above we wanted 8 cores per rank, not 8 threads. We thus have to add the `--threads-per-core=1` SLURM flag, giving:

```shell-session
$ salloc --account=<account_to_charge> --job-name="interactive" --constraint=GENOA --nodes=1 --ntasks-per-node=2 --cpus-per-task=8 --time=1:00:00 --threads-per-core=1
salloc: INFO : Considering its requirements, this job is treated in SHARED mode.
salloc: INFO : We cannot guarantee the performance reproducibility of such small jobs in this mode,
salloc: INFO : but they are only charged for the needed resources.
salloc:
salloc: INFO : This job requests 16 cores. Due to shared usage this job will be charged for 16 cores (of the 192 cores of the node)
salloc: Pending job allocation 41342
salloc: job 41342 queued and waiting for resources
salloc: job 41342 has been allocated resources
salloc: Granted job allocation 41342
```

This time, we observe the 16 cores allocated corresponding to the number of task per node times the number of thread (one per core) per rank.

If we now seek to use hyperthreading (SMT), it would look like so:

```shell-session
$ salloc --account=<account_to_charge> --job-name="interactive" --constraint=GENOA --nodes=1 --ntasks-per-node=2 --cpus-per-task=16 --time=1:00:00 --threads-per-core=2
salloc: INFO : Considering its requirements, this job is treated in SHARED mode.
salloc: INFO : We cannot guarantee the performance reproducibility of such small jobs in this mode,
salloc: INFO : but they are only charged for the needed resources.
salloc:
salloc: INFO : This job requests 16 cores. Due to shared usage this job will be charged for 16 cores (of the 192 cores of the node)
salloc: Pending job allocation 41342
salloc: job 41342 queued and waiting for resources
salloc: job 41342 has been allocated resources
salloc: Granted job allocation 41342
```

Note that we **double the number of thread per core** and **per rank**.

Finally, understand that we recommend that you prepare your work so that it uses full nodes (exclusive mode). Then, all the charging complexity goes away:

```shell-session
$ salloc --account=<account_to_charge> --job-name="interactive" --constraint=GENOA --nodes=1 --ntasks-per-node=2 --cpus-per-task=8 --time=1:00:00 --exclusive
salloc: Pending job allocation 41382
salloc: job 41382 queued and waiting for resources
salloc: job 41382 has been allocated resources
salloc: Granted job allocation 41382
```

You can find ways to pack small amounts of work into one large node allocation in [this document](index.md#adastra-running-jobs-small-job-packing).

**Warning**

If a shared partition is completely exhausted your job will be pending. It may be that if you switch to exclusive mode, your job will start earlier due to the pool of non-shared node being less used. This differs from say, IDRIS’ JeanZay machine where all the GPU nodes are shared. We assume HPC is synonymous of large job, spanning and scaling over multiple nodes. The shared mode is for **debugging purposes**, code that **do not scale** and computation of short duration (some script or post processing). If you run many small jobs that can, put together, fill a whole node, you should use a whole node, not a shared one; check [this document](index.md#adastra-running-jobs-small-job-packing) to learn how.

<a id="shared-mode-charging-formula"></a>

### Shared mode charging formula

On the GENOA partition, the memory and core charging computation is roughly defined like that:

```
CORES_CHARGED = CEIL_TO_MULTIPLE[ MAX((MEMORY_PER_NODE_ASKED/MEMORY_PER_NODE)*CORE_PER_NODE; CORE_PER_NODE_ASKED) ; CORE_PHYSICAL_BOUNDARY]

With:
    MEMORY_PER_NODE_ASKED and CORE_PER_NODE_ASKED being the resource amount you wish to reserve.
    CORE_PHYSICAL_BOUNDARY=8 is a group a of core we do not whish to split (L3 cache).
    MEMORY_PER_NODE~=744 and CORE_PER_NODE=192 the amount of resource a node has.
    CEIL_TO_MULTIPLE[X; N] = ROUND_AWAY_FROM_ZERO(X/N)*N
```

Additionally to the core and the memory, the GPU nodes offer, well, GPUs. On theses nodes, we charge you, not CPUs hours, but GPUs hours. See the [Resource consumption and charging (accounting)](index.md#adastra-running-jobs-resource-charging) document.

On the MI250 partition, this means that we use this formula instead, given the number of GPU to charge for:

```
GPUS_CHARGED = CEIL_TO_MULTIPLE[ MAX((MEMORY_PER_NODE_ASKED/MEMORY_PER_NODE)*CORE_PER_NODE; CORE_PER_NODE_ASKED; GPU_PER_NODE_ASKED*CORE_PHYSICAL_BOUNDARY) ; CORE_PHYSICAL_BOUNDARY] / CORE_PHYSICAL_BOUNDARY

With:
    MEMORY_PER_NODE_ASKED and CORE_PER_NODE_ASKED being the resource amount you wish to reserve.
    CORE_PHYSICAL_BOUNDARY=8 is a group a of core we do not whish to split (GPU NUMA).
    MEMORY_PER_NODE~=232 and CORE_PER_NODE=64 the amount of resource a node has.
    CEIL_TO_MULTIPLE[X; N] = ROUND_AWAY_FROM_ZERO(X/N)*N
    GPU_PER_NODE_ASKED being the resource amount you wish to reserve.
```

**Note**

We allocate MI250X GCDs on the basis of 8 cores per GCD. So if you ask for 15 cores, we’ll charge you for 2 GCDs.

Now that we have the amount of resource (GPUs or CPU cores), we multiply that be the duration it is allocated for. If you job finishes early, we do not charge for the unused time.

<a id="quality-of-service-qos-queues"></a>

<a id="adastra-running-jobs-queues"></a>

## Quality Of Service (QoS) queues

CINES respects the SLURM scheduler fair share constraints described by GENCI and common to CINES, IDRIS and TGCC.

On Adastra, queues are transparent, CINES does not publicizes the QoS. The user should not try to specify anything related to that subject (such as `--qos=`). The SLURM scheduler will automatically place your job in the right QoS depending on the duration and resource quantity asked.

Queue priority rules are harmonized between the 3 computing centers (CINES, IDRIS and TGCC). We give a higher priority is given to large jobs, as Adastra is primarily dedicated to running large HPC jobs. The SLURM fairshare concept is up and running meaning that a user that assuming a linear consumption, if a user is above the line, its priority will be lower than a user ho is below the line. We may artificially lower a user’s priority if we notice bad practices (such as launching thousands of small jobs on an HPC machine).
Priorities are calculated over a sliding window of one week. With a little patience, your job will eventually be processed.

The best advice we can give you is to correctly size your jobs. First check which node configuration works best, adjust the number of MPI, OpenMP thread and binding on a single node. Then do some scaling tests. Finally, **do not specify a SLURM ``–time`` argument larger than what you really need**, this is the most common scheduler misconfiguration on the user’s side.

<a id="srun"></a>

## `srun`

The default job launcher for Adastra is [srun](https://slurm.schedmd.com/srun.html) . The `srun` command is used to execute an MPI enabled binary on one or more compute nodes in parallel. It is responsible for distributing the resources allocated by an `salloc` or `sbatch` command onto MPI ranks.

```shell-session
 $ # srun  [OPTIONS... [executable [args...]]]
 $ srun --ntasks-per-node=24 --cpus-per-task=8 --threads-per-core=1 -- <executable> <arguments>
<output printed to terminal>
```

The output options have been removed since stdout and stderr are typically desired in the terminal window in this usage mode.

`srun` accepts the following common options:

|  |  |
| --- | --- |
| `-N, --nodes` | Number of nodes |
| `-n, --ntasks` | Total number of MPI tasks (default is 1). |
| `-c, --cpus-per-task=<ncpus>` | Logical cores per MPI task (default is 1).  When used with `--threads-per-core=1`: `-c` is equivalent to *physical* cores per task.  We do not advise that you use this option when using `--cpu-bind=none`. |
| `--cpu-bind=threads` | Bind tasks to CPUs.  `threads` - (default, recommended) Automatically generate masks binding tasks to threads. |
| `--threads-per-core=<threads>` | In task layout, use the specified maximum number of hardware threads per core.  (default is 2; there are 2 hardware threads per physical CPU core).  Must also be set in `salloc` or `sbatch` if using `--threads-per-core=2` in your `srun` command.  `threads-per-core` should **always** be used instead of ``` hint=nomultithread `` or ``hint=multithread ```. |
| `--kill-on-bad-exit=1` | Try harder at killing the whole step if a process fails and return an error code different than 1. |
| `-m, --distribution=<value>:<value>:<value>` | Specifies the distribution of MPI ranks across compute nodes, sockets (L3 regions), and cores, respectively.  The default values are `block:cyclic:cyclic`, see `man srun` for more information.  Currently, the distribution setting for cores (the third `<value>` entry) has no effect on Adastra |
| `--ntasks-per-node=<ntasks>` | If used without `-n`: requests that a specific number of tasks be invoked on each node.  If used with `-n`: treated as a *maximum* count of tasks per node. |
| `--gpus` | Specify the number of GPUs required for the job (total GPUs across all nodes). |
| `--gpus-per-node` | Specify the number of GPUs per node required for the job. |
| `--gpu-bind=closest` | Binds each task to the GPU which is on the same L3 cache as the CPU core the MPI rank is running on.  See the `--gpu-bind=closest` example in [Proper binding, why and how](../porting_optimization/index.md#porting-optimization-performance-tuning-monitoring-proper-binding-why-how) for more details.  This option needs `--cpus-per-task=N --gpus-per-task=M` to correctly work. |
| `--gpu-bind=map_gpu:<list>` | Bind tasks to specific GPUs by setting GPU masks on tasks (or ranks) as specified where  `<list>` is `<gpu_id_for_task_0>,<gpu_id_for_task_1>,...`. If the number of tasks (or  ranks) exceeds the number of elements in this list, elements in the list will be reused as  needed starting from the beginning of the list. To simplify support for large task  counts, the lists may follow a map with an asterisk and repetition count. (For example  `map_gpu:0*4,1*4`). |
| `--ntasks-per-gpu=<ntasks>` | Request that there are ntasks tasks invoked for every GPU. |
| `--label` | Prefix every written lines from stderr or stdout with `<rank index>:` where `<rank index>` starts at zero  and matches the MPI rank index that the writing process *is*. |

<a id="interactive-jobs"></a>

<a id="adastra-running-jobs-interactive-jobs"></a>

## Interactive jobs

Most users will find batch jobs as an easy way to use the system. Indeed, they allow the user to *hand off* a job to the scheduler, allowing the user to focus on other tasks while the job waits in the queue and eventually runs. Occasionally, it is necessary to run interactively, especially when developing, testing, modifying or debugging a code.

Since all compute resources are managed and scheduled by SLURM, it is not possible to simply log into the system and immediately begin running parallel codes interactively. Rather, you must request the appropriate resources from SLURM and, if necessary, wait for them to become available. This is done through an **interactive batch job**. Interactive batch jobs are submitted with the `salloc` command. Resources are requested via the same options that are passed via `#SBATCH` in a regular batch script (but without the `#SBATCH` prefix). For example, to request an interactive batch job with MI250 resources, you would use:

```shell-session
$ salloc --account=<account_to_charge> --constraint=MI250 --job-name="<job_name>" --nodes=1 --time=1:00:00 --exclusive
```

Note that there is no option for an output file, you are running interactively, so standard output and standard error will be displayed to the terminal.

You can then run the command you would generally put in the batch script:

```shell-session
$ srun --ntasks-per-node=2 --cpus-per-task=8 --threads-per-core=1 --gpus-per-task=1 --gpu-bind=closest -- <executable> <arguments>
```

If you want to connect to the node, you can directly `ssh` on it, assuming you have allocated it:

```shell-session
$ ssh g1010
```

**Note**

In some cases, if you use for instance, the `ForwardAgent Yes` SSH option, you may endup with authentication issues such manifesting through the following error: `Received disconnect from 10.64.16.112 port 22:2: Too many authentication failures Disconnected from 10.64.16.112 port 22`. You may want to disable that SSH option.

You can also start a shell environment as a SLURM step (which on some machines is the only way to get interactive node access):

```shell-session
$ srun --pty -- "${SHELL}"
```

<a id="small-job"></a>

<a id="adastra-running-jobs-small-job"></a>

## Small job

<a id="allocating-a-single-gpu"></a>

### Allocating a single GPU

The line below will allocate 1 GPU and 8 cores (no SMT), for 60 minutes.

```shell-session
$ srun \
      --account=<account_to_charge> \
      --constraint=MI250 \
      --nodes=1 \
      --time=1:00:00 \
      --gpus-per-node=1 \
      --ntasks-per-node=1 \
      --cpus-per-task=8 \
      --threads-per-core=1 \
      -- <executable> <arguments>
```

**Note**

This is more of a hack than a serious usage of SLURM concepts or of HPC resources.

<a id="packing"></a>

<a id="adastra-running-jobs-small-job-packing"></a>

### Packing

**Note**

We strongly advise that you get familiar with [Adastra’s SLURM’s queuing concepts](index.md#adastra-running-jobs-queues).

If your workflow consist of many small jobs, you may rely on the [shared mode](index.md#adastra-running-jobs-shared-exclusive-mode). That said, if you run many small jobs that can, put together, fill a whole node, you should use a whole node, not a shared one. This may shorten your queue time as we have and want to keep a small shared node count.

This is how we propose you use a whole node:

```shell
#!/bin/bash
#SBATCH --account=<account_to_charge>
#SBATCH --job-name="<job_name>"
#SBATCH --constraint=GENOA
#SBATCH --nodes=4
#SBATCH --exclusive
#SBATCH --time=1:00:00

set -eu
set -x

# How many run your logic needs.
STEP_COUNT=128

# due to the parallel nature of the SLURM steps described below, we need a
# way to properly log each one of them. See the:
# 2>&1 | tee "StepLogs/${SLURM_JOB_ID}.${I}"
mkdir -p StepLogs

for ((I = 0; I < STEP_COUNT; I++)); do
    srun --exclusive --nodes=2 --ntasks-per-node=3 --cpus-per-task=4 --threads-per-core=1 --label \
        -- ./work.sh 2>&1 | tee "StepLogs/${SLURM_JOB_ID}.${I}" &
done

# We started STEP_COUNT steps AKA srun processes, wait for them.
wait
```

In the script above, the steps will all be initiated but will start only when enough resource is available on the set of allocated resources (here we asked for 4 nodes). Here `work.sh` represent your workload. This workload command would be executed as many times as `STEP_COUNT*nodes*ntask-per-node=128*2*3=768` each with 4 cores. SLURM will automatically fill the resource allocated (here 4 nodes), queue and start as needed.

<a id="chained-job"></a>

## Chained job

SLURM offers a feature allowing the user to chain job. The user can, in fact, define a dependency graph of the jobs.

As an example, we want to start a job represented by `my_first_job.sh` and start an other job `my_second_job.sh` which we want to start only when `my_first_job.sh` finished:

```shell-session
$ sbatch my_first_job.sh
Submitted batch job 189562
$ sbatch --dependency=afterok:189562 my_second_job.sh
Submitted batch job 189563
$ sbatch --dependency=afterok:189563 my_other_job.sh
Submitted batch job 189564
```

In this example we use the `afterok` *trigger* meaning that only if the **parent** job ends successfully (exit code `0`) will it start.

You will then see something like this in `squeue`:

```shell-session
$ squeue --me
JOBID  PARTITION NAME USER ST TIME NODES NODELIST(REASON)
189562 mi250     test bae  PD 0:00 1     (Dependency)
189563 mi250     test bae  PD 0:00 1     (Dependency)
189564 mi250     test bae  R  0:04 1     g1057
```

Note the `Dependency` status.

You can replace `afterok` by `after`, `afterany`, `afternotok` or `singleton`.
More information here: <https://slurm.schedmd.com/sbatch.html#OPT_dependency>

<a id="job-array"></a>

## Job array

**Warning**

If you launch job arrays, ensure that they do not contain more that 11 jobs or you will get an error related to `AssocMaxSubmitJobLimit`. We restrict the job array size due to a bug in SLURM that leads to incorect priority computation and unfair scheduling. This should be temporary. (Added 2025/12/02)

<a id="other-common-slurm-commands"></a>

## Other common SLURM commands

The table below summarizes commonly-used SLURM commands:

|  |  |
| --- | --- |
| `sinfo` | Used to view partition and node information.  i.e., to view user-defined details about the batch queue:  `sinfo -p batch -o "%15N %10D %10P %10a %10c %10z"` |
| `squeue` | Used to view job and job step information for jobs in the scheduling queue.  i.e., to see your own jobs:  `squeue -l --me` |
| `sacct` | Used to view accounting data for jobs and job steps in the job accounting log (currently in the queue or recently completed).  i.e., to see a list of specified information about all jobs submitted/run by a users since 1 PM on January 4, 2023:  `sacct -u <login> -S 2023-01-04T13:00:00 -o "jobid%5,jobname%25,user%15,nodelist%20" -X` |
| `scancel` | Used to signal or cancel jobs or job steps.  i.e., to cancel a job:  `scancel <job_id>` |

We describe some of the usage of these commands below in [Monitoring and modifying batch jobs](index.md#adastra-running-jobs-advanced-slurm-commands).

<a id="sequential-slurm-steps-in-a-slurm-allocation"></a>

## Sequential SLURM steps in a SLURM allocation

SLURM allows you to run `srun` multiple times. Each `srun` launch constitutes what is called a *step*. You can create a script that call `srun` multiple times like so:

```shell
1# Somewhere in you sbatch script, you could have:
2for ((i = 0; i < 500; ++i)); do
3    srun --ntasks-per-node=24 --cpus-per-task=8 --threads-per-core=1 -- <executable> <arguments>
4done
```

This would saturate the GENOA nodes, and launch 500 steps inside one allocation.

See also [Packing](index.md#adastra-running-jobs-small-job-packing).

<a id="embarrassingly-parallel-slurm-steps-in-a-slurm-allocation"></a>

## Embarrassingly parallel SLURM steps in a SLURM allocation

SLURM allows you to run `srun` multiple times. Each `srun` launch constitutes what is called a *step*. You can create a script that call `srun` multiple times but by default, the steps will be sequential. You can tell SLURM to run the steps in parallel like so:

```shell
 1#SBATCH --account=<account_to_charge>
 2#SBATCH --job-name="<job_name>"
 3#SBATCH --constraint=GENOA
 4#SBATCH --nodes=4
 5#SBATCH --exclusive
 6#SBATCH --time=1:00:00
 7
 8set -eu
 9
10TASK_PER_NODE="24"
11# NOTE: Ensure there is almost always one task waiting to be executed, reducing
12# inactivity for small task.
13STEP_OVER_SUBSCRIPTION="$((TASK_PER_NODE / 10))"
14MAXIMUM_CONCURRENT_STEP="$((SLURM_JOB_NUM_NODES * (TASK_PER_NODE + STEP_OVER_SUBSCRIPTION)))"
15NTASKS="500"
16
17for ((i = 0; i < NTASKS; ++i)); do
18    # Wait if we have too many background jobs.
19    while [ "$(jobs -r | wc -l)" -ge "${MAXIMUM_CONCURRENT_STEP}" ]; do
20        sleep 1
21    done
22
23    # NOTE: the '&' is significant! Do not remove it, this is what allows the steps
24    # to run in parallel.
25    srun --nodes="1" --ntasks="1" --cpus-per-task=8 --threads-per-core=1 -- <executable0> <arguments0> &
26done
27
28# NOTE: the 'wait' is significant! Do not remove it, this is what allows bash to
29# block waiting for the srun processes to end.
30wait
```

This would saturate the GENOA nodes, and launch 500 steps in total inside one allocation. The `<executable0>` would be run 500 times.

See also [Packing](index.md#adastra-running-jobs-small-job-packing).

<a id="embarrassingly-parallel-tasks-in-a-slurm-step"></a>

## Embarrassingly parallel tasks in a SLURM step

SLURM allows you, via `srun`, to launch a single executable (script or binary) multiple times with each instance of the executable associated to a different identifier, we call such an instance a **task**. To change the command that the task will execute we recommend that you use a small script:

```shell
1#!/bin/bash
2
3set -eu # Handles errors.
4
5# You can use the ${SLURM_PROCID} environment variable to know which task
6# indentifier the current script is being executed as. For instance:
7exec -- <executable0> <arguments0> "input_${SLURM_PROCID}.namelist"
```

This scripts is very similar to the ones we provide to restrict profilers to a single task (see for instance [the perf profiler script](../software_stack/tools/index.md#adastra-software-stack-tools-profiling-perf)).

Then to use the script (assuming it is called `run.sh`), simply do:

```shell
1srun --ntasks-per-node=192 --cpus-per-task=1 --threads-per-core=1 -- ./run.sh
```

Each instance of `run.sh` will have a unique identifier, and in the case above, assuming we use 1 GENOA node, it will in in the range `[0-192[` (192 excluded!).

<a id="job-state"></a>

## Job state

A job will transition through several states during its lifetime. Common ones include:

| State  Code | State | Description |
| --- | --- | --- |
| CA | Canceled | The job was canceled (could’ve been by the user or an administrator). |
| CD | Completed | The job completed successfully (exit code 0). |
| CG | Completing | The job is in the process of completing (some processes may still be running). |
| PD | Pending | The job is waiting for resources to be allocated. |
| R | Running | The job is currently running. |

<a id="job-reason-codes"></a>

## Job reason codes

In addition to state codes, jobs that are pending will have a *reason code* to explain why the job is pending. Completed jobs will have a reason describing how the job ended. Some codes you might see include:

| Reason | Meaning |
| --- | --- |
| Dependency | Job has dependencies that have not been met. |
| JobHeldUser | Job is held at user’s request. |
| JobHeldAdmin | Job is held at system administrator’s request. |
| Priority | Other jobs with higher priority exist for the partition/reservation. |
| Reservation | The job is waiting for its reservation to become available. |
| AssocMaxJobsLimit | The job is being held because the user/project has hit the limit on running jobs. |
| AssocMaxSubmitJobLimit | The limit on the number of jobs a user is allowed to have running or pending at a given time has been met for the requested association (array). |
| ReqNodeNotAvail | The user requested a particular node, but it is currently unavailable (it is in use, reserved, down, draining, etc.). |
| JobLaunchFailure | Job failed to launch (could due to system problems, invalid program name, etc.). |
| NonZeroExitCode | The job exited with some code other than 0. |

Many other states and job reason codes exist. For a more complete description, see the `squeue` man page (either on the system or online).

More reasons are given in the [official SLURM documentation](https://slurm.schedmd.com/resource_limits.html).

<a id="monitoring-and-modifying-batch-jobs"></a>

<a id="adastra-running-jobs-advanced-slurm-commands"></a>

## Monitoring and modifying batch jobs

<a id="scancel-cancel-or-signal-a-job"></a>

### `scancel`: Cancel or signal a job

SLURM allows you to signal a job with the `scancel` command. Typically, this is used to remove a job from the queue. In this use case, you do not need to specify a signal and can simply provide the jobid. For example, `scancel 12345`.

In addition to removing a job from the queue, the command gives you the ability to send other signals to the job with the `-s` option. For example, if you want to send `SIGUSR1` to a job, you would use `scancel -s USR1 12345`.

<a id="squeue-view-the-job-queue"></a>

<a id="adastra-running-jobs-advanced-slurm-commands-squeue"></a>

### `squeue`: View the job queue

The `squeue` command is used to show the batch queue. You can filter the level of detail through several command-line options. For example:

|  |  |
| --- | --- |
| `squeue --long` | Show all jobs currently in the queue. |
| `squeue --long --me` | Show all of *your* jobs currently in the queue. |
| `squeue --me --start` | Show all of *your* jobs that have yet to start and show their expected start time. |

<a id="sacct-get-job-accounting-information"></a>

### `sacct`: Get job accounting information

The `sacct` command gives detailed information about jobs currently in the queue and recently-completed jobs. You can also use it to see the various steps within a batch jobs.

|  |  |
| --- | --- |
| `sacct -a -X` | Show all jobs (`-a`) in the queue, but summarize the whole allocation instead of showing individual steps (`-X`). |
| `sacct -u ${USER}` | Show all of your jobs, and show the individual steps (since there was no `-X` option). |
| `sacct -j 12345` | Show all job steps that are part of job 12345. |
| `sacct -u ${USER} -S 2022-07-01T13:00:00 -o "jobid%5,jobname%25,nodelist%20" -X` | Show all of your jobs since 1 PM on July 1, 2022 using a particular output format. |

<a id="scontrol-show-job-get-detailed-job-information"></a>

### `scontrol show job`: Get Detailed Job Information

In addition to holding, releasing, and updating the job, the `scontrol` command can show detailed job information via the `show job` subcommand. For example, `scontrol show job 12345`.

**Note**

`scontrol show job` can only report information on a job that is in the queue. That is, **pending** or **running** (but there are more states). A finished job is not in the queue and not queryable with `scontrol show job`.

<a id="obtaining-the-energy-consumption-of-a-job"></a>

### Obtaining the energy consumption of a job

On Adastra, we enable the user to monitor the energy his job consumes.

```shell-session
$ sacct --format=JobID,ElapsedRaw,ConsumedEnergyRaw,NodeList --jobs=<job_id>
JobID          ElapsedRaw ConsumedEnergyRaw        NodeList
-------------- ---------- ----------------- ---------------
<job_id>              104          12934230 c[1000-1003,10+
<job_id>.batch        104             58961           c1000
<job_id>.0             85          12934230 c[1000-1003,10+
```

The user obtains, for a given `<job_id>`, the elapsed time in **secondes** and the energy consumption in **joules** for the whole job, the *execution of the batch script* and for each job steps. The job steps are suffixed with `\.[0-9]+` (in regex form).

Each time you execute the `srun` comment in a batch script, it creates a new job step. Here, there is only one `srun` *step* which took 85 secondes and 12934230 joules.

**Note**

The duration of the step as reported by SLURM is not reliable for a short step. There may be an additional ~10 secondes.

**Note**

You will only get meaningful values regarding a job step once the job step has ended.

**Note**

The energy returned represents the aggregated node consumption. We do not include the network and storage costs as these ones are trickier to get and consist in a near fixed cost anyway (that is, whether you run are not your code).

**Note**

Some compute node may not return an energy consumed value. This leads to a value of `0` or empty under `ConsumedEnergyRaw`. To workaround the issue, one can use the following command: `scontrol show node | grep -e "CurrentWatts=n/s" -e "CurrentWatts=0" -B15 | grep "NodeName=" | cut -d '=' -f 2 | awk '{print $1}' | tr '\n' ','` and feed the result to the SLURM commands’ `--exclude=` option. For instance: `sbatch --exclude="$(scontrol show node | grep -e "CurrentWatts=n/s" -e "CurrentWatts=0" -B15 | grep "NodeName=" | cut -d '=' -f 2 | awk '{print $1}' | tr '\n' ',')" job.sh`.

**Note**

More generally, the `sensors` command can be used to dump what the system reports in `/sys/class/hwmon`.

**Note**

The counters SLURM uses to compute the energy consumption come from the Baseboard Management Controller (BMC), not `/sys/cray/pm_counters/*` (these sysfs files come from the `bpmcdmod` kernel module, see [SLURM’s official documentation](https://slurm.schedmd.com/slurm.conf.html#OPT_AcctGatherEnergyType). The values are refreshed at 10 Hz. The PM Counters are mostly physical power/energy sensors collected directly from VRMs (Voltage Regulator Module) on the node cards. The measurment is taken just before the VRM of the cards. `rocm-smi` reports after the VRMs, so the delta is the convertion loss. The energy counters are 64 bits wide and count in joule. Details on PAPI integration are given by `man 5 cray_pm`. We provide a script to easily [`gather the energy`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/a1bc15446392c2d25f2b355484cb86d6/energy_sampling.py) with an [`example job script`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/4d0057f9a52a6a7161c98cff52023141/energy_sampling.sh).

**Note**

On MI300A, the `accel_energy` and `power` correspond to the power/energy of an APU taken at the input of the 48 VDC rail (Infineon XDP710) that feeds each APU socket (and HSN NIC when the socket has a Cassini NIC attached). In most cases the two APUs with NICs attached will see about 30 Watts of NIC power.

**Note**

We distributed additional documents like [`this Cray PM counter presentation`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/050f5a55c35be3690ad97d5ca5e28f43/pres127s2.pdf).

<a id="gpu-frequency-capping"></a>

### GPU frequency capping

You can cap the AMD GPUs using this SLURM flag:

```
#SBATCH --gpu-srange=800-1500
```

In this example the GPU frequency is capped at a maximum of 1500 MHz. Note that the lower bound is not always taken into account while the upper bound is.

It has been shown that lowering the clock even down to 1300 MHz on MI250X does not decrease the energy efficiency if the code is memory bound.

<a id="coredump-files"></a>

<a id="adastra-running-jobs-core-dump-files"></a>

## Coredump files

If you start a program through our batch scheduler (SLURM), and if your program crashes, you will find your coredump files in the `${SCRATCHDIR}/COREDIR/<job_id>/<hostname>` directory. The `${SCRATCHDIR}` correspond to the scratch directory associated to your user and project specified in the `#SBATCH --account=<account_to_charge>` batch script option. The files are stored in different folders depending on the `<job_id>`. Additionally, if your job ran on multiple nodes, it is useful to have a way to differentiate which coredump file originate from which node, thus, the `<hostname>` of the node is used to define a path for the coredump files.

The coredump filename has the following semantic: `core_<signal>_<timestamp>_<process_name>.dump.<process_identifier>` (the equivalent core pattern being `core_%s_%t_%e.dump`). As an example, you could have such coredump filename:

```
core_11_1693986879_segfault_testco.dump.2745754
```

You can then exploit a coredump file by using tools such as GDB like so:

```shell-session
$ gdb ./path/to/program.file ./path/to/coredump.file
```

You can find more information on GDB and coredump files [here](https://www.cse.unsw.edu.au/~learn/debugging/modules/gdb_coredumps/).

**Warning**

Be careful that you do not fill all your *scratch* space quota with coredump files. Notably, if you run a large job that crashes.

**Note**

On Adastra, `ulimit -c unlimited` is the default. The coredump placement to *scratch* works on the HPDA, MI250 and GENOA partitions. To deactivate the *core dumping*, run the following command in, say, your batch script: `ulimit -c 0`.

**Note**

Use `gcore <pid>` to explicitly generate a core file of a running program.

**Warning**

For the placement of the coredump to the *scratch* to work, one needs to use either a batch script or the `salloc` + `srun` commands. Simply allocating (`salloc`) and `ssh` ing to the node will not properly configure the coredump placement mechanism. Also, one needs to request nodes in **exclusive** mode for the placement to work (in shared mode it will **not** work).
