<!-- Source: https://dci.dci-gitlab.cines.fr/webextranet/data_visualization_and_analytics/index.html -->
<!-- Title: Data visualization and analytics -->

<a id="data-visualization-and-analytics"></a>

<a id="visualization"></a>

# Data visualization and analytics

<a id="accessing-the-hpda-hardware"></a>

## Accessing the HPDA hardware

The 12 visualization and pre/post processing nodes provide 2048 Gio RAM per node and 2 NVIDIA L40 graphics cards. The operating system is RHEL8 and the default CUDA version >= 11.2.

The CINES proposes two ways to access the HPDA nodes; via the NiceDCV **remote desktop** facilities or, **through SLURM**.

**Note**

Be well aware that the HPDA nodes possess NVIDIA L40 GPU and the compute nodes possess AMD MI250X GPUs, they work differently.

**Warning**

The maximum allocation duration is 6 hours (via SLURM or the remote desktop).

<a id="slurm-reservation"></a>

### SLURM reservation

To reserve an HPDA node, simply specify the `--constraint=` flag to `HPDA`. For more details on how to reserve a node, you can refer to the [Job submission](../user_support/index.md#adastra-running-jobs) section.

Example script to request a whole HPDA node (2 Tio of RAM and 2 NVidia L40 GPUs):

```shell
#!/bin/bash
#SBATCH --account=<account_to_charge>
#SBATCH --job-name="hello_world_hpda"
#SBATCH --constraint=HPDA
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=1:00:00

# # With    HyperThreading (SMT), 192 cores and 384 hardware threads.
# srun --ntasks-per-node=24 --cpus-per-task=16 --threads-per-core=2 -- ./hello_world
# Without HyperThreading (SMT), 192 cores and 192 hardware threads.
srun --ntasks-per-node=24 --cpus-per-task=8  --threads-per-core=1 -- ./hello_world
```

<a id="remote-desktop"></a>

<a id="visualization-hpda-remote-desktop"></a>

### Remote desktop

<a id="through-a-web-service"></a>

#### Through a web service

You may require visualizing data which may need large amount of RAM (to avoid stuttering) and powerful GPUs. We provide a remote desktop service through a website accessible under the following URL: <https://adastra.cines.fr/enginframe/>.

When on the portal, you will be presented this web page:

[![../_images/nicedcv_portal_connection.PNG](https://dci.dci-gitlab.cines.fr/webextranet/_images/nicedcv_portal_connection.PNG)](https://dci.dci-gitlab.cines.fr/webextranet/_images/nicedcv_portal_connection.PNG)

Enter you username and password, the same one you use to connect to Adastra. After login in, you should land on this page:

[![../_images/nicedcv_portal_home.PNG](https://dci.dci-gitlab.cines.fr/webextranet/_images/nicedcv_portal_home.PNG)](https://dci.dci-gitlab.cines.fr/webextranet/_images/nicedcv_portal_home.PNG)

You can click on `Desktop_Users` which will redirect you to this page:

[![../_images/nicedcv_portal_new_session.PNG](https://dci.dci-gitlab.cines.fr/webextranet/_images/nicedcv_portal_new_session.PNG)](https://dci.dci-gitlab.cines.fr/webextranet/_images/nicedcv_portal_new_session.PNG)

You can then specify the account on which you wish to charge the HPDA hour consumption. After a little while depending on the HPDA resource availability, you will be presented this web page (also accessible by clicking the `Sessions` button on the left of the web page):

[![../_images/nicedcv_portal_starting_session.PNG](https://dci.dci-gitlab.cines.fr/webextranet/_images/nicedcv_portal_starting_session.PNG)](https://dci.dci-gitlab.cines.fr/webextranet/_images/nicedcv_portal_starting_session.PNG)

[![../_images/nicedcv_portal_session.PNG](https://dci.dci-gitlab.cines.fr/webextranet/_images/nicedcv_portal_session.PNG)](https://dci.dci-gitlab.cines.fr/webextranet/_images/nicedcv_portal_session.PNG)

**Note**

Behind the web interface, a SLURM job is scheduled and started. This can be observed via the typical `squeue` command (see the [squeue: View the job queue](../user_support/index.md#adastra-running-jobs-advanced-slurm-commands-squeue) document).

As soon as the session is started, CINES will monitor the HPDA hours consumed. As the resource is relatively scarce, we ask the user to be particularly aware of the duration of their session. We forcefully kill the session after a 6 h duration. To explicitly release a session you can click on the cross as shown below:

[![../_images/nicedcv_portal_release_session.PNG](https://dci.dci-gitlab.cines.fr/webextranet/_images/nicedcv_portal_release_session.PNG)](https://dci.dci-gitlab.cines.fr/webextranet/_images/nicedcv_portal_release_session.PNG)

to access the remote desktop, simply click on the small (*black*) rectangle representing the screenshot of the remote desktop:

[![../_images/nicedcv_portal_open_session.PNG](https://dci.dci-gitlab.cines.fr/webextranet/_images/nicedcv_portal_open_session.PNG)](https://dci.dci-gitlab.cines.fr/webextranet/_images/nicedcv_portal_open_session.PNG)

A new tab should open in you browser, giving you access to the HPDA remote desktop.

[![../_images/nicedcv_portal_desktop.PNG](https://dci.dci-gitlab.cines.fr/webextranet/_images/nicedcv_portal_desktop.PNG)](https://dci.dci-gitlab.cines.fr/webextranet/_images/nicedcv_portal_desktop.PNG)

**Note**

If you obtains a black screen when opening a session, please close the old session and start a new one to workaround the bug.

<a id="hpda-related-software"></a>

## HPDA related software

- [ParaView & VTK](../software_stack/tools/index.md#adastra-software-stack-tools-paraview);
- [Jupyter](../software_stack/tools/index.md#adastra-software-stack-tools-jupyter);
- [VisIt](../software_stack/tools/index.md#adastra-software-stack-tools-visit);
- More but undocumented (yet).
