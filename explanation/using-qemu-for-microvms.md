(using-qemu-for-microvms)=
# Using QEMU for microVMs

MicroVMs are a special case of virtual machines (VMs), which were designed to be used in a container-like way to provide better isolation than containers, but which are optimised for initialisation speed and minimal resource use. 

Because they are so lightweight, they are particularly useful in dynamic workload situations where demands change rapidly and new resources need to be quickly provisioned or de-provisioned to meet those demands.

They are also useful in situations where resources are limited (e.g. in IoT devices), or where the cost of using resources is a factor, thanks to their small footprint and overall efficiency.

## QEMU microVMs

QEMU provides additional components that were added to support this special use case:

1. The [`microvm` machine type](https://www.qemu.org/docs/master/system/i386/microvm.html)
1. Alternative simple firmware (FW) that can boot linux [called `qboot`](https://github.com/bonzini/qboot)
1. QEMU build with reduced features matching these use cases called `qemu-system-x86-microvm` (we will call this "minimised `qemu`")

## Basic command

As an example, if you happen to already have a stripped-down workload that has all it would execute contained in an initrd, you might run it like this:

```console
sudo qemu-system-x86_64 \
 -M ubuntu-q35 \
 -cpu host \
 -m 1024 \
 -enable-kvm \
 -serial mon:stdio \
 -nographic \
 -display curses \
 -append 'console=ttyS0,115200,8n1' \
 -kernel vmlinuz-5.4.0-21 \
 -initrd /boot/initrd.img-5.4.0-21-workload
```

### The `microvm` case

To run the same basic command with `microvm` you would run it with with type `microvm`, so we change `-M` to `-M microvm`.

Our command then becomes:

```console
sudo qemu-system-x86_64 \
 -M microvm ubuntu-q35 \
 -cpu host \
 -m 1024 \
 -enable-kvm \
 -serial mon:stdio \
 -nographic \
 -display curses \
 -append 'console=ttyS0,115200,8n1' \
 -kernel vmlinuz-5.4.0-21 \
 -initrd /boot/initrd.img-5.4.0-21-workload
```

### The `qboot` case

To run the basic command with `qboot` instead, we would use the `qboot bios` by adding `-bios /usr/share/qemu/bios-microvm.bin`.

```console
sudo qemu-system-x86_64 \
 -M ubuntu-q35 \
 -cpu host \
 -m 1024 \
 -enable-kvm \
 -serial mon:stdio \
 -nographic \
 -display curses \
 -append 'console=ttyS0,115200,8n1' \
 -kernel vmlinuz-5.4.0-21 \
 -initrd /boot/initrd.img-5.4.0-21-workload \
 -bios /usr/share/qemu/bios-microvm.bin
```

### The minimised `qemu` case

To run the the basic command instead using the minimised `qemu`, you would first need to install the feature-minimised `qemu-system` package, with:

```bash
sudo apt install qemu-system-x86-microvm
```

Then, our basic command will look like this:

```console
sudo qemu-system-x86_64 \
 -M microvm \
 -bios /usr/share/qemu/bios-microvm.bin \
 -cpu host \
 -m 1024 \
 -enable-kvm \
 -serial mon:stdio \
 -nographic \
 -display curses \
 -append 'console=ttyS0,115200,8n1' \
 -kernel vmlinuz-5.4.0-21 \
 -initrd /boot/initrd.img-5.4.0-21-workload
```

This will cut down the `qemu`, `bios` and `virtual-hw` initialisation time a lot. You will now -- more than you already were before -- spend the majority of time inside the guest, which implies that further tuning probably has to go into that kernel and user-space initialisation time.

## Further considerations

For now, `microvm`, the `qboot` BIOS, and other components of this are rather new upstream and not  as verified as many other parts of the virtualisation stack.

Therefore, none of the above options are the default. Being the default would mean many upgraders would regress upon finding a QEMU that doesn't have most of the features they are accustomed to using. 

Because of that the `qemu-system-x86-microvm` package (the minimised `qemu` option) is intentionally a strong opt-in that conflicts with the normal `qemu-system-x86` package.
