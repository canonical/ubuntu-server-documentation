(kernel-crash-dump)=
# Kernel crash dump


A 'kernel crash dump' refers to a portion of the contents of volatile memory (RAM) that is copied to disk whenever the execution of the kernel is disrupted. The following events can cause a kernel disruption:

  - Kernel panic

  - Non-maskable interrupts (NMI)

  - Machine check exceptions (MCE)

  - Hardware failure

  - Manual intervention

For some of these events (kernel panic, NMI) the kernel will react automatically and trigger the crash dump mechanism through *kexec*. In other situations a manual intervention is required in order to capture the memory. Whenever one of the above events occurs, it is important to find out the root cause in order to prevent it from happening again. The cause can be determined by inspecting the copied memory contents.

## Kernel crash dump mechanism

When a kernel panic occurs, the kernel relies on the *kexec* mechanism to quickly reboot a new instance of the kernel in a pre-reserved section of memory that had been allocated when the system booted (see below). This permits the existing memory area to remain untouched in order to safely copy its contents to storage.

## Installation

The kernel crash dump utility is installed with the following command:

```bash
sudo apt install linux-crashdump
```

> **Note**:
> Starting with 16.04, the kernel crash dump mechanism is enabled by default.

During the installation, you will be prompted with the following dialogs.

```text
 |------------------------| Configuring kexec-tools |------------------------|
 |                                                                           |
 |                                                                           |
 | If you choose this option, a system reboot will trigger a restart into a  |
 | kernel loaded by kexec instead of going through the full system boot      |
 | loader process.                                                           |
 |                                                                           |
 | Should kexec-tools handle reboots (sysvinit only)?                        |
 |                                                                           |
 |                    <Yes>                       <No>                       |
 |                                                                           |