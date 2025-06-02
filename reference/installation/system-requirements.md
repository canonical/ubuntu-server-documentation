(system-requirements)=
# System requirements

Ubuntu Server provides a flexible base for your solution that can run on a wide range of hardware, from small virtual machines to enterprise-scale computing. 

Hard requirements depend on the scenario, but they're generally constrained by the following recommended values.

## Architecture

Ubuntu Server supports various 64-bit architectures and 32-bit arm.

- amd64 (64-bit Intel/{term}`AMD`)
- arm64 (64-bit Arm)
- armhf (32-bit Arm)
- ppc64el (64-bit Power)
- riscv64 (64-bit RISC-V)
- s390x (64-bit Mainframe)

For specific platforms, see our list of [Ubuntu certified servers](https://ubuntu.com/certified/servers).

The numbers below are true for Ubuntu 24.04 Noble amd64. Other releases and architectures might differ slightly.

## Memory

**Minimum RAM**: 1.5 GB (ISO installs)
**Minimum RAM**: 1 GB (cloud images)

It's likely that your system might need more memory than that if you, for instance, have more hardware to initialise, have more complex setup plans, or are using other architectures. To cover better for any of those scenarios:

**Suggested minimum RAM**: 3 GB or more

Upper limits depend on the system hardware and setup.

## Storage

**Minimum storage**: 5 GB (ISO installs)
**Minimum storage**: 4 GB (cloud images)

In theory you could go even lower, like 2.5 GB for cloud image installs, but in practise it's quite likely that your system will need more disk storage than that to be really useful. Your setup plans could be more complex or you need more software to be installed, that could lead to increased storage needs. To cover better for any of those scenarios:

**Suggested minimum storage**: 25 GB or more
