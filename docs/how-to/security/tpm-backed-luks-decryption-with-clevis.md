---
myst:
  html_meta:
    description: Learn how to integrate Clevis with Dracut for automated TPM-backed LUKS decryption on Ubuntu Server.
---

(tpm-backed-luks-decryption-with-clevis)=
# TPM-based LUKS decryption with Clevis

[Clevis](https://github.com/latchset/clevis) is a pluggable framework for
automated decryption. When combined with {term}`TPM` and {term}`FDE` via
{term}`LUKS`, Clevis can automatically unlock encrypted drives during boot
without user intervention.

This guide targets systems that use {manpage}`dracut(8)` as the initramfs
generator. 

:::{note}
The Clevis tooling is currently provided via the `universe` archive. While
functional, it serves as a community-supported fallback for TPM-bound
encryption until a fully integrated server FDE solution lands in a future LTS
release.
:::

:::{warning}
Keep at least one known-good LUKS passphrase for recovery. TPM measurements can
change after firmware updates, Secure Boot state changes, or some bootloader
changes, which can prevent automatic unlock until you rebind Clevis.
:::

## Prerequisites

* An Ubuntu Server installation with LVM over LUKS.
* A system with a TPM 2.0 module.
* Root or `sudo` privileges.

## Install Clevis and Dracut integration

To install the necessary packages from a terminal prompt:

```bash
sudo apt update && sudo apt install clevis clevis-tpm2 clevis-dracut clevis-luks
```

## Binding a LUKS volume

Before Dracut can auto-unlock a drive, the drive must be bound to the TPM. Use
Clevis to add a new key to the LUKS header, sealed against the TPM.

Identify the encrypted partition before binding:

```bash
lsblk -f
```

Look for the partition with `FSTYPE` set to `crypto_LUKS`, then use that path
in the following command as `<encrypted_partition>`.

Bind against Platform Configuration Register (PCR) 7, which tracks secure boot
state. If your environment requires different trust guarantees, choose PCR
values that match your threat model.

```bash
sudo clevis luks bind -d <encrypted_partition> tpm2 '{"pcr_ids": "7"}'
```

You will be prompted to enter the LUKS passphrase you created during
installation. Clevis will generate a new cryptographic token and store it in
the LUKS header.

## Updating the initial ramdisk

The `clevis-dracut` package provides the necessary Dracut modules to include
Clevis decryption hooks in the early boot environment. After binding your root
disk, you must regenerate the initial ramdisk.

To force a rebuild of the initial ramdisk for the current kernel, use:

```bash
sudo dracut -f
```

You can verify that the Clevis modules were successfully included with
{manpage}`lsinitrd(1)` by inspecting the generated image:

```bash
lsinitrd | grep clevis
```

You can also verify that a Clevis token exists in the LUKS metadata:

```bash
sudo clevis luks list -d <encrypted_partition>
```

For a lower-level check, inspect LUKS token metadata with
{manpage}`cryptsetup(8)`:

```bash
sudo cryptsetup luksDump <encrypted_partition> | grep -A5 -i Tokens
```

After rebooting, confirm the root volume unlocks automatically and the system
reaches the login prompt without asking for the LUKS passphrase.

## Advanced usage

### Unlocking secondary disks

If your server has secondary encrypted data disks, you do not need to use
`dracut` to unlock them, as they are unlocked later in the boot process by
{manpage}`systemd(1)`.

To do so, you must first bind the secondary disk to the TPM. Replace
`<secondary_encrypted_partition>` with your secondary encrypted partition.

```bash
sudo clevis luks bind -d <secondary_encrypted_partition> tpm2 '{"pcr_ids": "7"}'
```

Then, get the UUID of the locked LUKS partition:

```
blkid -s UUID -o value <secondary_encrypted_partition>
```

Add the disk to {manpage}`crypttab(5)`, using `none` for the password file so
{manpage}`systemd(1)` automatically intercepts the prompt and recognizes the
Clevis binding.

```
data_vol UUID=<UUID> none luks
```

Then add the decrypted mapper device (`/dev/mapper/data_vol`) to
{manpage}`fstab(5)` as usual.

### Removing a TPM binding

If you need to remove a Clevis binding (for example, if you are decommissioning
a server or moving the drive), you can unbind it. First, list the active Clevis tokens
to find the correct LUKS slot:

```bash
sudo clevis luks list -d <encrypted_partition>
```

Then, unbind the specific slot (replacing `1` with the slot number identified above).

```bash
sudo clevis luks unbind -d <encrypted_partition> -s 1
```
