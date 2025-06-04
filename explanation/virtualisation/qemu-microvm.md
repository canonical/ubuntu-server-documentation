(qemu-microvm)=
# QEMU microvm

QEMU microvm is a special case of virtual machine (VMs), designed to be
optimised for initialisation speed and minimal resource use.

The underlying concept of a microvm is based on giving up some capabilities of
standard QEMU in order to reduce complexity and gain speed. Maybe - for your
use-case - you do not need e.g. the hypervisor to be able to pretend to have a
network card from the 90s, nor to emulate a CPU of a foreign architecture,
nor live migrate with external I/O going on. In such cases, a lot of what QEMU
provides is not needed and a less complex approach like a microvm might be
interesting to you.

All of that is a balance that needs to be decided by the needs of your
use case. There will surely be arguments and examples going both ways - so be
careful. Giving up on unnecessary features to gain speed is great, but it is
not so great if - some time after deploying your project - you realise that you
now need a feature only available in the more complete solution.

QEMU provides additional components that were added to support this special use case:

1. The [`microvm` machine type](https://www.qemu.org/docs/master/system/i386/microvm.html)
1. Alternative simple {term}`firmware (FW) <FW>` that can boot Linux [called `qboot`](https://github.com/bonzini/qboot)
1. Ubuntu has a QEMU build with reduced features matching these use cases called `qemu-system-x86-microvm`

## Why a special workload?

One has to understand that minimising the QEMU initialisation time only yields a
small gain, by shaving off parts of a task that usually do not take a long time. That is only worth
it if the workload you run is not taking much longer anyway. For example, by
booting a fully generic operating system, followed by more time to completely
initialise your workload.

There are a few common ways to adapt a workload to match this:
- Use faster bootloaders and virtual firmware (see `qboot` below) with a reduced
  feature set, not as generally capable but sufficient for a particular use case.
- Even the fastest bootloader is slower than no bootloader, so often
  the kernel is directly passed from the host {term}`filesystem`.
  A drawback of this solution is the fact that the guest system will not have
  control over the kernel anymore, thus restricting what can be done inside the
  guest system.
- Sometimes a simpler user space like [busybox](https://www.busybox.net/) or a container-like environment
  is used.
- In a similar fashion, you could use a customised kernel build with a reduced feature set
  with only what is needed for a given use case.

A common compromise of the above options is aligning virtualization with
container paradigms. While behaving mostly like a container, those tools will
use virtualization instead of namespaces for the isolation.
Examples of that are:

- container-like, as in [kata containers](https://katacontainers.io/),
- function-based services as in [Firecracker](https://firecracker-microvm.github.io/),
- system containers as in {ref}`LXD <lxd-containers>`.

In particular, {ref}`LXD <lxd-containers>` added VM mode to allow the very same UX
with namespaces and virtualizaton.

Other related tools are more about creating VMs from containers like:

- [slim from dockerfiles](https://github.com/ottomatica/slim) or
- [krunvm from OCI images](https://github.com/containers/krunvm).

There are more of these out there, but the point is that one can mix and match
to suit their needs. At the end of the day, many of the above use the same
underlying technology of namespaces or QEMU/KVM.

This page tries to stick to the basics and not pick either higher level
system mentioned above. Instead, it sticks to just QEMU to show how it's
ideas of reduced firmware and microvms play into all of this.

## Create the example workload artifact

To create an example of such a small workload, we will follow the tutorial on
how to build a [sliced rock](https://documentation.ubuntu.com/rockcraft/en/stable/tutorial/hello-world/).

Out of these tutorials one gets an [OCI-compatible](https://github.com/opencontainers/image-spec/blob/main/spec.md)
artifact. It will be called `chiselled-hello_latest_amd64.rock`.
That is now converted to a disk image for use as virtual disk in our later
example.

```bash
# Convert the artifact of the ROCK tutorial into OCI format
$ sudo rockcraft.skopeo --insecure-policy copy oci-archive:chiselled-hello_latest_amd64.rock oci:chiselled-hello.oci:latest
# Unpack that to a local directory
$ sudo apt install oci-image-tool
$ oci-image-tool  unpack --ref name=latest chiselled-hello.oci /tmp/chiselled-hello
# Create some paths the kernel would be unhappy if they would be missing
$ mkdir /tmp/chiselled-hello/{dev,proc,sys,run,var}
# Convert the directory to a qcow2 image
$ sudo apt install guestfs-tools
$ sudo virt-make-fs --format=qcow2 --size=50M /tmp/chiselled-hello chiselled-hello.qcow2
```

## Run the stripped workload in QEMU

Now that we have a stripped-down workload as an example, we can run it
in standard QEMU and see that this is much quicker than booting a full
operating system.

```bash
$ sudo qemu-system-x86_64 -m 128M -machine accel=kvm \
    -kernel /boot/vmlinuz-$(uname -r) \
    -append 'console=ttyS0 root=/dev/vda fsck.mode=skip init=/usr/bin/hello' \
    -nodefaults -no-user-config \
    -display none -serial mon:stdio \
    -drive file=chiselled-hello.qcow2,index=0,format=qcow2,media=disk,if=none,id=virtio1 \
    -device virtio-blk-pci,drive=virtio1
...
[    2.116207] Run /usr/bin/hello as init process
Hello, world!
```

Breaking down the command-line elements and their purpose in this context:

| **command-line element** | **Explanation** |
| ----------------------- | --------------- |
| `sudo` | `sudo` is a simple way for this example to work, but not recommended. Scenarios outside of an example should use separate kernel images and a user that is a member of the `kvm` group to access `/dev/kvm`. |
| `qemu-system-x86_64` | Call the usual binary of QEMU used for system virtualization. |
| `-m 128M` | Allocate 128 megabytes of RAM for the guest. |
| `-machine accel=kvm` | Enable KVM. |
| `-kernel /boot/vmlinuz-$(uname -r)` | Load the currently running kernel for the guest. |
| `-append '...'` | This passes four arguments to the kernel explained one by one in the following rows. |
| `console=ttyS0` | Tells the kernel which serial console it should send its output to. |
| `root=/dev/vda` | Informs it where to expect the root device matching the `virtio-block` device we provide. |
| `fsck.mode=skip` | Instructs the kernel to skip filesystem checks, which saves time. |
| `init=/usr/bin/hello` | Tell the kernel to directly start our test workload. |
| `-nodefaults` | Do not create the default set of devices. |
| `-no-user-config` | Do not load any user provided config files. |
| `-display none` | Disable video output (due to `-nodefaults` and `-display none` we do not also need `-nographic`). |
| `-serial mon:stdio` | Map the virtual serial port and the monitor (for debugging) to stdio |
| `-drive ... -device ...` | Provide our test image as virtio based block device. |

After running this example we notice that, by changing the workload to something
small and streamlined, the execution time went down from about 1 minute (when
booting a bootloader into a full OS into a workload) to about 2 seconds (from
when the kernel started accounting time), as expected.

For the purpose of what this page wants to explain, it is not important to be
perfectly accurate and stable. We are now in the right order of magnitude
(seconds instead of a minute) in regard to the _overall time spent_ to begin
focusing on the time that the initialisation of firmware and QEMU consume.

## Using `qboot` and `microvm`

In the same way as `qemu-system-x86-microvm` is a reduced QEMU,
[qboot](https://github.com/bonzini/qboot) is a simpler variant to the
extended feature set of [seabios](https://www.seabios.org/SeaBIOS) or
[UEFI](https://github.com/tianocore/edk2) that can do less, but therefore is
faster at doing what it can.

If your system does not need the extended feature sets you can try
`qboot` if this gives you an improvement for your use case. To do so
add `-bios /usr/share/qemu/qboot.rom` to the QEMU command line.

[QEMU microvm](https://github.com/qemu/qemu/blob/master/docs/system/i386/microvm.rst)
is a machine type inspired by [Firecracker](https://firecracker-microvm.github.io/)
and constructed after its machine model.

In Ubuntu, we provide this on x86 as `qemu-system-x86_64-microvm` alongside the
_standard_ QEMU in the package `qemu-system-x86`.

Microvm aims for maximum compatibility by default; this means that you will
probably want to switch off some more legacy devices that are not shown in
this example. But for what is shown here, we want to keep it rather comparable
to the non-microvm invocation.
For more details on what else could be disabled see
[microvm](https://github.com/qemu/qemu/blob/master/docs/system/i386/microvm.rst#running-a-microvm-based-vm).

Run the guest in `qemu-system-x86_64-microvm`:

```bash
$ sudo qemu-system-x86_64-microvm -m 128M -machine accel=kvm,rtc=on \
    -bios /usr/share/qemu/qboot.rom \
    -kernel /boot/vmlinuz-$(uname -r) \
    -append 'console=ttyS0 root=/dev/vda fsck.mode=skip init=/usr/bin/hello' \
    -nodefaults -no-user-config \
    -display none -serial mon:stdio \
    -drive file=chiselled-hello.qcow2,index=0,format=qcow2,media=disk,if=none,id=virtio1 -device virtio-blk-device,drive=virtio1
```

Breaking down the changes to the command-line elements and their purpose:

| **command-line element** | **Explanation** |
| ----------------------- | --------------- |
| `qemu-system-x86_64-microvm` | Call the lighter, feature-reduced QEMU binary. |
| `-bios /usr/share/qemu/qboot.rom` | Running QEMU as `qemu-system-x86_64-microvm` will auto-select `/usr/share/seabios/bios-microvm.bin` which is a simplified SeaBIOS for this purpose. But, for the example shown here we want the even simpler `qboot`, so in addition we set `-bios /usr/share/qemu/qboot.rom`. |
| _info_ | QEMU will auto-select the microvm machine type, equivalent to `-M microvm` which therefore doesn't need to be explicitly included here. |
| `... virtio-blk-device ...` | This feature-reduced QEMU only supports `virtio-bus`, so we need to switch the type `virtio-blk-pci` to `virtio-blk-device`. |

> Sadly, polluting this nice showcase there is currently an issue with the
> RTC initialisation not working in this mode - which makes the guest
> kernel wait ~1.3 + ~1.4 seconds. See this
> [qemu bug](https://bugs.launchpad.net/ubuntu/+source/qemu/+bug/2074073)
> if you are curious about that.
>
> But these changes were not about making the guest faster once it runs, instead
> it mostly is about the initialisation time (and kernel init by having less
> virtual hardware). And that we can check despite this issue.

On average, across a few runs (albeit not in a very performance-controlled
environment) we can see the kernel start time to be 282ms faster
comparing _normal QEMU_ to `microvm` and another 526ms faster comparing `microvm`
to `microvm`+`qboot`.

As mentioned, one could go further from here by disabling more legacy devices,
using `hvcconsole`, customising the guest CPU, switching off more subsystems
like ACPI, or customising the kernel that is used. But this was meant to be an
example on how `microvm` can be used in general, so we won't make it more
complex for now.

## Alternative - using virtiofs

Another common path not fully explored in the example above is sharing the
content with the guest via `virtiofsd`.

Doing so for our example could start with a conversion of the container
artifact above to a shareable directory:

```bash
# Copy out the example the tutorial had in OCI format
$ sudo rockcraft.skopeo --insecure-policy copy oci-archive:chiselled-hello_latest_amd64.rock oci:chiselled-hello.oci:latest
# Unpack that to a directory
$ sudo apt install oci-image-tool
$ oci-image-tool  unpack --ref name=latest chiselled-hello.oci /tmp/chiselled-hello
```

Exposing that directory to a guest via `virtiofsd`:

```bash
$ sudo apt install virtiofsd
$ /usr/libexec/virtiofsd --socket-path=/tmp/vfsd.sock --shared-dir /tmp/chiselled-hello
...
[INFO  virtiofsd] Waiting for vhost-user socket connection...
```

To the QEMU command-line one would then add the following options:

```bash
...
-object memory-backend-memfd,id=mem,share=on,size=128M \
-numa node,memdev=mem -chardev socket,id=char0,path=/tmp/vfsd.sock \
-device vhost-user-fs-pci,queue-size=1024,chardev=char0,tag=myfs
...
```

Which allows the user to mount it from inside the guest via
`$ mount -t virtiofs myfs /mnt` or if you want to use it as root, you can pass
it via kernel parameter `rootfstype=virtiofs root=myfs rw`.
