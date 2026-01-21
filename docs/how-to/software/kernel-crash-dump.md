---
myst:
  html_meta:
    description: Configure and analyze kernel crash dumps on Ubuntu Server using kdump and kexec to diagnose kernel panics and system failures.
---

(kernel-crash-dump)=
# Kernel crash dump

A 'kernel crash dump' refers to a portion of the contents of volatile memory (RAM) that is copied to disk whenever the execution of the kernel is disrupted. The following events can cause a kernel disruption:

  - Kernel panic

  - Non-maskable interrupts (NMI)

  - Machine check exceptions (MCE)

  - Hardware failure

  - Manual intervention

For some of these events (kernel panic, NMI) the kernel will react automatically and trigger the crash dump mechanism through *`kexec`*. In other situations a manual intervention is required in order to capture the memory. Whenever one of the above events occurs, it is important to find out the root cause in order to prevent it from happening again. The cause can be determined by inspecting the copied memory contents.

## Kernel crash dump mechanism

When a kernel panic occurs, the kernel relies on the *`kexec`* mechanism to quickly reboot a new instance of the kernel in a pre-reserved section of memory that had been allocated when the system booted (see below). This permits the existing memory area to remain untouched in order to safely copy its contents to storage.

## Installation

The kernel crash dump utility is installed by default in most Ubuntu environments, especially those designated for execution on bare metal.
In other cases it can be installed with following command:

```bash
sudo apt install kdump-tools
```

During the installation, you will be prompted with the following dialog:

```text
 |------------------------| Configuring kdump-tools |------------------------|
 |                                                                           |
 |                                                                           |
 | If you choose this option, the kdump-tools mechanism will be enabled.  A  |
 | reboot is still required in order to enable the crashkernel kernel        |
 | parameter.                                                                |
 |                                                                           |
 | Should kdump-tools be enabled be default?                                 |
 |                                                                           |
 |                    <Yes>                       <No>                       |
 |                                                                           |
 |---------------------------------------------------------------------------|
```

'Yes' should be selected to enable `kdump-tools`.  If you want to revisit your choice, you can use the `dpkg-reconfigure kdump-tools` command and answer 'Yes' or 'No'.

## `kdump` is enabled by default where applicable

On manual install the interactive question will define if it is enabled or not
and therefore depend on the users choice, but in cases when it is automatically
preinstalled there is a balance to strike.
The tool wants to be helpful by default, because when the crash happens it is
too late to enable crash dump functionality.
But at the same time it needs to reserve memory for the crash kernel to operate
and that might have too much impact to very small systems as well as consume
a lot of memory on systems with many devices.
Therefore starting in Oracular Oriole (24.10), the kernel crash dump facility
will be enabled by default during standard Ubuntu Desktop or Ubuntu Server
installations on systems that meet the following requirements:
 - the system has at least 4 CPU threads
 - the system has at least 6GB of RAM, and less than 2TB of RAM
 - the free space available in `/var` is more than 5 times the amount of RAM and swap space
 - and the CPU architecture is
   - amd64 or s390x, or
   - arm64 and UEFI is used

These conditions are evaluated at installation time by the tool `/usr/share/kdump-tools/kdump_set_default`.

On machines that do not meet these requirements and on pre-24.10 releases,
the kernel crash dump facility can be enabled manually by following the
installation instructions that follow.

## Disabling `kdump`

No matter which way it got enabled, to disable the function it can be either entirely removed via the command:

```bash
sudo apt remove kdump-tools
```

or by changing the config at `/etc/default/kdump-tools` to contain:

```text
USE_KDUMP=0
```

## Activating config changes

If a reboot has not been done since installation/removal of the `kdump-tools` package,
a reboot will be required in order to reconsider the `crashkernel= boot` parameter.

## Verify if kdump is ready

Upon reboot, the crashkernel memory will be reserved and the `kdump-tools` service will be enabled and active.

If you enable `kdump-tools` after a reboot, you will only need to issue the `kdump-config load` command to activate the `kdump` mechanism.

You can view the current status of `kdump` via the command `kdump-config show`.  This will display something like this:

```text
kdump-config show
DUMP_MODE:                kdump
USE_KDUMP:                1
KDUMP_COREDIR:                /var/crash
crashkernel addr: 0x60000000
   /var/lib/kdump/vmlinuz: symbolic link to /boot/vmlinuz-6.18.0-8-generic
kdump initrd:
   /var/lib/kdump/initrd.img: symbolic link to /var/lib/kdump/initrd.img-6.18.0-8-generic
current state:    ready to kdump

crashkernel suggested size: 417M

kexec command:
  /sbin/kexec -p -s --command-line="BOOT_IMAGE=/vmlinuz-6.18.0-8-generic root=UUID=0a86b691-f733-4cb0-9c5c-b88e0ef9e212 ro console=tty1 console=ttyS0 reset_devices systemd.unit=kdump-tools-dump.service nr_cpus=1 irqpoll usbcore.nousb" --initrd=/var/lib/kdump/initrd.img /var/lib/kdump/vmlinuz
```

This tells us that we will find core dumps in `/var/crash`.

## Reserving Memory

To operate kdump needs to pre-allocate a dedicated, isolated region of physical
memory that remains untouched by the main operating system, ensuring a safe
haven for the crash recovery process. When a kernel panic occurs, the running
system is considered unstable and its memory potentially corrupted, making it
unsafe to trust for saving diagnostic data. By reserving this memory at boot
time, kdump guarantees that a second, small "capture kernel" can load into this
pristine space without relying on the broken kernel's resources. This isolation
allows the capture kernel to reliably access the frozen, crashed memory and
write it to disk for analysis, functioning essentially like a fresh operating
system inside the crashed one.

To confirm that this allocation worked there are a few things to verify.
First, confirm that the `crashkernel` boot parameter is present.

```bash
$ cat /proc/cmdline
```

Which shows:

```text
BOOT_IMAGE=/vmlinuz-6.18.0-8-generic
 root=UUID=0a86b691-f733-4cb0-9c5c-b88e0ef9e212 ro console=tty1 console=ttyS0
 crashkernel=2G-4G:320M,4G-32G:512M,32G-64G:1024M,64G-128G:2048M,128G-:4096M
```

The `crashkernel` parameter has the following syntax:

```text
crashkernel=<range1>:<size1>[,<range2>:<size2>,...][@offset]
    range=start-[end] 'start' is inclusive and 'end' is exclusive.
```

So for the `crashkernel` parameter found in the `/proc/cmdline` example above we would have :

```text
crashkernel=2G-4G:320M,4G-32G:512M,32G-64G:1024M,64G-128G:2048M,128G-:4096M
```

The above values mean:

  - if the RAM is smaller than 2G, then don't reserve anything (this is to not impact small systems where it would take quite a share)

  - if the RAM size is between 2G and 4G (exclusive), then reserve 320M

  - ...

  - if the RAM size is larger than 128G, then reserve 4096M

Second, verify that the kernel has reserved the requested memory area for the `kdump` kernel by running `dmesg`:

```bash
dmesg | grep -i crash
```

Which shows:

```text
[    0.004623] crashkernel reserved: 0x0000000060000000 - 0x0000000074000000 (320 MB)
```

This example output is for a system with 3GB memory which correctly maps to 320 MB.

The defaults provided by the packaging try to be conservative to not waste too much.
But in some rare cases that might break when the dump process fails to initialized.
Only when a system is live can an estimation of the required memory be provided.
`kdump-config show` includes a line like `crashkernel suggested size: 417M`
based on what the current kernel consumed at boot time.

## Configuration

In addition to local dump, it is now possible to use the remote dump functionality to send the kernel crash dump to a remote server, using either the SSH or NFS protocols.

### Local kernel crash dumps

Local dumps are configured automatically and will remain in use unless a remote protocol is chosen. Many configuration options exist and are thoroughly documented in the `/etc/default/kdump-tools` file.

### Remote kernel crash dumps using the SSH protocol

To enable remote dumps using the SSH protocol, the `/etc/default/kdump-tools` must be modified in the following manner:

```text
# ---------------------------------------------------------------------------
# Remote dump facilities:
# SSH - username and hostname of the remote server that will receive the dump
#       and dmesg files.
# SSH_KEY - Full path of the ssh private key to be used to login to the remote
#           server. use kdump-config propagate to send the public key to the
#           remote server
# HOSTTAG - Select if hostname of IP address will be used as a prefix to the
#           timestamped directory when sending files to the remote server.
#           'ip' is the default.
SSH="ubuntu@kdump-netcrash"
```

The only mandatory variable to define is SSH. It must contain the username and {term}`hostname` of the remote server using the format `{username}@{remote server}`.

`SSH_KEY` may be used to provide an existing private key to be used. Otherwise, the `kdump-config propagate` command will create a new keypair. The `HOSTTAG` variable may be used to use the hostname of the system as a prefix to the remote directory to be created instead of the IP address.

The following example shows how `kdump-config propagate` is used to create and propagate a new keypair to the remote server:

```bash
sudo kdump-config propagate
```

Which produces an output like this:

```text
Need to generate a new ssh key...
The authenticity of host 'kdump-netcrash (192.168.1.74)' can't be established.
ECDSA key fingerprint is SHA256:iMp+5Y28qhbd+tevFCWrEXykDd4dI3yN4OVlu3CBBQ4.
Are you sure you want to continue connecting (yes/no)? yes
ubuntu@kdump-netcrash's password:
propagated ssh key /root/.ssh/kdump_id_rsa to server ubuntu@kdump-netcrash
```

The password of the account used on the remote server will be required in order to successfully send the public key to the server.

The `kdump-config show` command can be used to confirm that `kdump` is correctly configured to use the SSH protocol:

```bash
kdump-config show
```

Whose output appears like this:

```text
DUMP_MODE:        kdump
USE_KDUMP:        1
KDUMP_SYSCTL:     kernel.panic_on_oops=1
KDUMP_COREDIR:    /var/crash
crashkernel addr: 0x2c000000
   /var/lib/kdump/vmlinuz: symbolic link to /boot/vmlinuz-4.4.0-10-generic
kdump initrd:
   /var/lib/kdump/initrd.img: symbolic link to /var/lib/kdump/initrd.img-4.4.0-10-generic
SSH:              ubuntu@kdump-netcrash
SSH_KEY:          /root/.ssh/kdump_id_rsa
HOSTTAG:          ip
current state:    ready to kdump
```

### Remote kernel crash dumps using the NFS protocol

To enable remote dumps using the NFS protocol, the `/etc/default/kdump-tools` must be modified in the following manner:

```text
# NFS -     Hostname and mount point of the NFS server configured to receive
#           the crash dump. The syntax must be {HOSTNAME}:{MOUNTPOINT} 
#           (e.g. remote:/var/crash)
#
NFS="kdump-netcrash:/var/crash"
```

As with the SSH protocol, the `HOSTTAG` variable can be used to replace the IP address by the hostname as the prefix of the remote directory.

The `kdump-config show` command can be used to confirm that `kdump` is correctly configured to use the NFS protocol :

```bash
kdump-config show
```

Which produces an output like this:

```text
DUMP_MODE:        kdump
USE_KDUMP:        1
KDUMP_SYSCTL:     kernel.panic_on_oops=1
KDUMP_COREDIR:    /var/crash
crashkernel addr: 0x2c000000
   /var/lib/kdump/vmlinuz: symbolic link to /boot/vmlinuz-4.4.0-10-generic
kdump initrd:
   /var/lib/kdump/initrd.img: symbolic link to /var/lib/kdump/initrd.img-4.4.0-10-generic
NFS:              kdump-netcrash:/var/crash
HOSTTAG:          hostname
current state:    ready to kdump
```

## Troubleshooting

As seen previously, the `kdump-config show` command displays the current status of the `kdump-tools` configuration :
But in a system without sufficient memory (here 1 GB) it would not reserve memory,
due to that initialization would fail.

Such conditions can be seen in `kdump-config show` as well, the primary
value to check is `current state`.

```bash
kdump-config show
```

Which in this bad case would report

```text
DUMP_MODE:                kdump
USE_KDUMP:                1
KDUMP_COREDIR:                /var/crash
crashkernel addr:
   /var/lib/kdump/vmlinuz: symbolic link to /boot/vmlinuz-6.18.0-8-generic
kdump initrd:
   /var/lib/kdump/initrd.img: symbolic link to /var/lib/kdump/initrd.img-6.18.0-8-generic
current state:    Not ready to kdump

crashkernel suggested size: 329M

kexec command:
  no kexec command recorded
```

Such allocation errors can also be seen in the journal output as well as the
service status of kdump-tools:

```bash
systemctl status kdump-tools
```

Might then show:

```text
...
... kdump-tools[5348]: Memory for crashkernel is not reserved
... kdump-tools[5348]: Please reserve memory by passing"crashkernel=Y@X" parameter to kernel
... kdump-tools[5348]: Then try to loading kdump kernel
```

## Testing the crash dump mechanism

```{warning}
Testing the crash dump mechanism **will cause a system reboot**. In certain situations, this can cause data loss if the system is under heavy load. If you want to test the mechanism, make sure that the system is idle or under very light load.
```

Verify that the *SysRQ* mechanism is enabled by looking at the value of the `/proc/sys/kernel/sysrq` kernel parameter:

```bash
cat /proc/sys/kernel/sysrq
```

If a value of *0* is returned, the dump and then reboot feature is disabled. A value greater than *1* indicates that a sub-set of `sysrq` features is enabled. See `/etc/sysctl.d/10-magic-sysrq.conf` for a detailed description of the options and their default values. Enable dump then reboot testing with the following command:

```bash
sudo sysctl -w kernel.sysrq=1
```

Once this is done, you must become root, as just using `sudo` will not be sufficient. As the *root* user, you will have to issue the command `echo c > /proc/sysrq-trigger`. If you are using a network connection, you will lose contact with the system. This is why it is better to do the test while being connected to the system console. This has the advantage of making the kernel dump process visible.

A typical test output should look like the following :

```text
sudo -s
[sudo] password for ubuntu: 
# echo c > /proc/sysrq-trigger
[   31.659002] SysRq : Trigger a crash
[   31.659749] BUG: unable to handle kernel NULL pointer dereference at           (null)
[   31.662668] IP: [<ffffffff8139f166>] sysrq_handle_crash+0x16/0x20
[   31.662668] PGD 3bfb9067 PUD 368a7067 PMD 0 
[   31.662668] Oops: 0002 [#1] SMP 
[   31.662668] CPU 1 
....
```

The rest of the output is truncated, but you should see the system rebooting and somewhere in the log, you will see the following line :

```text
Begin: Saving vmcore from kernel crash ...
```

Once completed, the system will reboot to its normal operational mode. You will then find the kernel crash dump file, and related subdirectories, in the `/var/crash` directory by running, e.g. `ls /var/crash`, which produces the following:

```bash
201809240744  kexec_cmd  linux-image-4.15.0-34-generic-201809240744.crash
```

If the dump does not work due to an 'out of memory' (OOM) error, then try increasing the amount of reserved memory by editing `/etc/default/grub.d/kdump-tools.cfg`. For example, to reserve 512 megabytes:

```text
GRUB_CMDLINE_LINUX_DEFAULT="$GRUB_CMDLINE_LINUX_DEFAULT crashkernel=384M-:512M"
```

You can then run `sudo update-grub`, reboot afterwards, and then test again.

## Resources

Kernel crash dump is a vast topic that requires good knowledge of the Linux kernel. You can find more information on the topic here:

  - [`kdump` kernel documentation](https://www.kernel.org/doc/Documentation/kdump/kdump.txt).

  - [Analyzing Linux Kernel Crash](https://www.dedoimedo.com/computers/crash-analyze.html) (Based on Fedora, it still gives a good walk-through of kernel dump analysis)
