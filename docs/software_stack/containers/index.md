<!-- Source: https://dci.dci-gitlab.cines.fr/webextranet/software_stack/containers/index.html -->
<!-- Title: Containers -->

<a id="containers"></a>

<a id="adastra-software-stack-containers"></a>

# Containers

[Singularity/Apptainer](https://en.wikipedia.org/wiki/Apptainer) is a widely used open-source container system. It is designed to run applications with bare metal performance while being somewhat *secure*, *portable* and *repeatable*. With Singularity/Apptainer containers, users can work in reproducible environments of their choice and design. The main advantage of using a container is that it establishes a self-contained software environment for each application, which simplifies the installation of complex applications.

<a id="available-containers"></a>

## Available containers

The [AMD Infinity Hub](https://www.amd.com/fr/technologies/infinity-hub) contains a collection of software for AMD GPUs. The Infinity Hub images have been made available in this directory Adastra `/opt/software/containers/images/infinity-hub/`.

Additionally, if the user whishes to uses custom containers, he can run the command `container_submit.py path_to_container -P your_project` from a login node. This script will launch a pipeline scanning the container, if there is no Critical CVE, it will place the containers in `/opt/software/containers/images/users/<project_identifier>/<container_name>.sif`. In case of Critical CVE found, the user will receive a mail with the concerned components, feel free to open a ticket at [svp@cines.fr](mailto:svp%40cines.fr) for help.

<a id="using-a-container"></a>

## Using a container

The Singularity/Apptainer binary dedicated to image execution is accessible on all Adastra compute nodes but **not** on the login nodes.

<a id="running-as-a-slurm-batch-job"></a>

### Running as a SLURM batch job

Here is an example of a SLURM script to launch the LAMMPS application :

```shell
#!/bin/bash
#SBATCH --account=<account_to_charge>
#SBATCH --job-name="<job_name>"
#SBATCH --constraint=MI250
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=1:00:00

singularity run --writable-tmpfs -B</path/to/input> -B/sys -B/dev -B/proc -B/lus /opt/software/containers/images/<container>.sif <executable> <arguments>
```

Where :
:   - `--writable-tmpfs` makes the file system accessible as read-write with non persistent data (with overlay support only);
    - `-B, --bind strings` binds a path. Where `strings` has the format `src[:dest[:opts]]`, where `src` and `dest` are outside and inside paths. If `dest` is not given, it is set equal to `src`. Mount options (`opts`) may be specified as `ro` (read-only) or `rw` (read/write, which is the default). Multiple bind paths can be given by a comma separated list.

<a id="running-as-a-slurm-interactive-session"></a>

### Running as a SLURM interactive session

We start by allocating a whole node (note the `--exclusive`):

```shell-session
$ salloc --account=<account_to_charge> --job-name="interactive" --constraint=GENOA --nodes=1 --time=1:00:00 --exclusive
```

Get the name of the node with `squeue` and the `NODELIST` column:

```shell-session
$ squeue --me
```

Connect to the node:

```shell-session
$ ssh <node_hostname>
```

Then, repeat what was specified in the script above:

```shell-session
$ singularity run --writable-tmpfs -B</path/to/input> -B/sys -B/dev -B/proc -B/lus /opt/software/containers/images/<container>.sif <executable> <arguments>
```

You can run a shell in the container using the following command:

```shell-session
$ singularity shell --writable-tmpfs -B</path/to/input> -B/sys -B/dev -B/proc -B/lus /opt/software/containers/images/<container>.sif
```
