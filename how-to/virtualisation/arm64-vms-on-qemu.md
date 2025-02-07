(boot-arm64-virtual-machines-on-qemu)=
# Boot ARM64 virtual machines on QEMU

```{include} notices/qemu-user-group-notice.txt
```


Ubuntu ARM64 images can run inside QEMU. You can either do this fully emulated (e.g. on an x86 host) or accelerated with KVM if you have an ARM64 host. This page describes how to do both.

> **Note**: 
> This requires Ubuntu 20.04 or greater

## Install QEMU

The first step is to install the `qemu-system-arm` package, which needs to be done regardless of where the ARM64 virtual machine will run:

```bash
sudo apt install qemu-system-arm
```

## Create necessary support files

Next, create a VM-specific flash volume for storing NVRAM variables, which are necessary when booting [EFI](https://documentation.ubuntu.com/server/reference/glossary/#term-EFI) firmware:

```bash
truncate -s 64m varstore.img
```

We also need to copy the ARM UEFI firmware into a bigger file:

```bash
truncate -s 64m efi.img
dd if=/usr/share/qemu-efi-aarch64/QEMU_EFI.fd of=efi.img conv=notrunc
```

## Fetch the Ubuntu cloud image

You need to fetch the ARM64 variant of the Ubuntu cloud image you would like to use in the virtual machine. You can go to the official [Ubuntu cloud image](https://cloud-images.ubuntu.com/) website, select the Ubuntu release, and then download the variant whose filename ends in `-arm64.img`. For example, if you want to use the latest Jammy cloud image, you should download the file named `jammy-server-cloudimg-arm64.img`.

## Run QEMU natively on an ARM64 host

If you have access to an ARM64 host, you should be able to create and launch an ARM64 virtual machine there. Note that the command below assumes that you have already set up a network bridge to be used by the virtual machine.

```bash
qemu-system-aarch64 \
 -enable-kvm \
 -m 1024 \
 -cpu host \
 -M virt \
 -nographic \
 -drive if=pflash,format=raw,file=efi.img,readonly=on \
 -drive if=pflash,format=raw,file=varstore.img \
 -drive if=none,file=jammy-server-cloudimg-arm64.img,id=hd0 \
 -device virtio-blk-device,drive=hd0 -netdev type=tap,id=net0 \
 -device virtio-net-device,netdev=net0
```

## Run an emulated ARM64 VM on x86

You can also emulate an ARM64 virtual machine on an x86 host. To do that:

```bash
qemu-system-aarch64 \
 -m 2048\
 -cpu max \
 -M virt \
 -nographic \
 -drive if=pflash,format=raw,file=efi.img,readonly=on \
 -drive if=pflash,format=raw,file=varstore.img \
 -drive if=none,file=jammy-server-cloudimg-arm64.img,id=hd0 \
 -device virtio-blk-device,drive=hd0 \
 -netdev type=tap,id=net0 \
 -device virtio-net-device,netdev=net0
```

## Troubleshooting

### No output and no response

If you get no output from the QEMU command above, aligning your host and guest release versions may help. For example, if you generated `efi.img` on Focal but want to emulate Jammy (with the Jammy cloud image), the firmware may not be fully compatible. Generating `efi.img` on Jammy when emulating Jammy with the Jammy cloud image may help.
