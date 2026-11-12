<!-- Source: https://dci.dci-gitlab.cines.fr/webextranet/other/changelogs.html -->
<!-- Title: Adastra Update - Changelogs -->

<a id="adastra-update-changelogs"></a>

<a id="adastra-other-changelogs"></a>

# Adastra Update - Changelogs

Date:
:   February 13, 2026

RedHat Version:
:   9.6

HPE Supported Versions:
:   CPE/24.07, CPE/25.09

<a id="new-features-and-important-changes"></a>

## New Features and Important Changes

<a id="hpe-supported-versions"></a>

### HPE Supported Versions

- CPE/24.07 and CPE/25.09 are now the only versions supported by HPE.
- The CINES teams have made considerable efforts to keep versions prior to CPE/24.07 operational. Despite numerous tests ensuring compatibility, we strongly recommend migrating to the latest HPE-supported version.

<a id="non-functional-lammps-versions"></a>

### Non-functional LAMMPS Versions

The following LAMMPS builds can no longer be used due to their dependency on Python 3.6, which is unsupported under Red Hat 9.6 :

- `lammps/develop-mpi-omp-plumed-python3`
- `lammps/20220623.3-mpi-omp-plumed-python3`
- `lammps/20230802-plumed-rocm-kokkos-mpi-gpu`
- `lammps/20230802-mpi-omp-plumed-python3`
- `lammps/20231121-omp-plumed-kokkos-mpi`
- `lammps/20240207.1-plumed-rocm-kokkos-mpi-gpu`
- `lammps/20240207.1-omp-plumed-kokkos-mpi`

Please migrate to one of the following compatible versions, now available :

- `lammps/20240829.1-plumed-rocm-kokkos-mpi-gpu`
- `lammps/20240829.1-omp-plumed-kokkos-mpi`
- `lammps/20250612-plumed-rocm-kokkos-mpi-gpu`

<a id="opencl-modules"></a>

### OpenCL Modules

Users running OpenCL-based applications must now load the following module before launching their jobs:

```
module load opencl-icd-loader
```

Learn more about OpenCL modules here : [https://dci.dci-gitlab.cines.fr/webextranet/software_stack/libraries/index.html#opencl](../software_stack/libraries/index.md#opencl)

<a id="rocm-version-compatibility-with-cpe-25-09"></a>

### ROCm Version Compatibility with CPE/25.09

- The default ROCm version is now 6.4.3. Please update your environment if you use ROCm.
- Versions 7.0.0 and higher are available but **not compatible** with the Cray-mpich versions currently deployed on ADASTRA.

<a id="mpich-versions-8-1-28"></a>

### MPICH Versions < 8.1.28

- MPICH versions lower than 8.1.28 are not compatible with libfabric 2.2.0.
- This issue has been fixed in the current CINES software stack. To avoid similar issues, we recommend using the CPE module to ensure consistency between dependent modules.

Learn how to change CrayPE version : [https://dci.dci-gitlab.cines.fr/webextranet/user_support/index.html#changing-craype-version](../user_support/index.md#changing-craype-version)

<a id="graphics-libraries-on-login-nodes"></a>

### Graphics Libraries on Login Nodes

Some graphical libraries such as Wayland/OpenGL are no longer available on login nodes.

This is due to the removal of the `/opt/amdgpu/lib` path from the LD cache to prevent a conflict between the local `libLLVM.so` and the system version. A fix is currently in progress.

<a id="deployment-of-cines-software-stack-develop-5-0-0"></a>

### Deployment of CINES Software Stack (develop) 5.0.0

- The CINES 5.0.0 software stack is now in production on ADASTRA.
- The 3.2.0 stacks are archived but remain accessible using commands such as:

  ```
  module load archive
  module load CCE-GPU-3.2.0
  ```

<a id="additional-information"></a>

### Additional Information

<a id="hpe-documentation"></a>

### HPE Documentation

For detailed information about RedHat 9.6 update and bug fixes, please refer to :

HPE RedHat 9.6 Release Notes <https://cpe.ext.hpe.com/docs/latest/release_notes/rhel_9_6_release_notes.html>

<a id="migration-support"></a>

### Migration Support

If you encounter any issues during the migration process or have questions regarding this update, please contact us at `svp@cines.fr`.

We remain available to support you throughout this transition.
