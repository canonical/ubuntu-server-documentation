---
myst:
  html_meta:
    description: "How Ubuntu verifies the boot chain, protects data at rest, and controls devices, kernel modules, and firmware."
---

(kernel-hardware-boundary)=
# Kernel, hardware, boot, and storage boundary

This page looks at the lower boundary: how Ubuntu establishes trust in the
code that runs at boot, how it protects data at rest, and how the running
kernel deals with hardware and firmware.

The diagrams on this page follow the
{ref}`diagram conventions <security-architecture-legend>`. To go to the
explanation of a box, select the box in the diagram.

(security-architecture-boot)=
## Verified and measured boot

The boot chain decides which kernel runs. Each stage either verifies or
measures the next one.

```{mermaid}
:alt: Verified and measured boot. With Secure Boot (platform-dependent), the UEFI firmware verifies shim, which is signed by the Microsoft UEFI CA. shim verifies GRUB, and GRUB verifies the Linux kernel through shim; both are signed by Canonical. GRUB also loads the initramfs, which is built locally and not signed. Through the firmware, each stage extends measurements into the TPM 2.0 PCRs (platform-dependent). The running kernel enforces lockdown and module signatures (platform-dependent).
:caption: Verified and measured boot chain

---
config:
  theme: base
  fontFamily: Ubuntu variable, Ubuntu, sans-serif
  themeCSS: 'svg, svg * { font-family: Ubuntu variable, Ubuntu, sans-serif !important; } .flowchart-link { stroke-width: 3px !important; } .edge-pattern-dotted { stroke-dasharray: 8 5 !important; }'
  flowchart:
    curve: linear
  themeVariables:
    fontFamily: Ubuntu variable, Ubuntu, sans-serif
    lineColor: "#E95420"
    primaryColor: "#F3F3F3"
    primaryBorderColor: "#000000"
    primaryTextColor: "#000000"
    clusterBkg: "#FFFFFF"
    clusterBorder: "#000000"
    edgeLabelBackground: "#FFFFFF"
---
flowchart TB
    subgraph MAIN[" "]
        direction TB
        subgraph HW["Hardware and firmware"]
            uefi["UEFI firmware, Secure Boot<br>(platform-dependent)"]
            tpm["TPM 2.0 PCRs<br>(platform-dependent)"]
        end
        subgraph BOOT["Boot chain"]
            shim["shim<br>(signed by Microsoft UEFI CA)"]
            grub["GRUB<br>(signed by Canonical)"]
            kernel["Linux kernel<br>(signed by Canonical)"]
            initrd["initramfs<br>(built locally, not signed)"]
        end
        lockdown["Lockdown, module signature<br>enforcement (platform-dependent)"]
        uefi -->|"Verifies"| shim
        shim -->|"Verifies"| grub
        grub -->|"Verifies through shim"| kernel
        grub -->|"Loads"| initrd
        uefi -->|"Extends measurements<br>of each stage"| tpm
        kernel -->|"Enforces at runtime"| lockdown
        style HW fill:#FFFFFF,stroke:#000000,stroke-width:2px
        style BOOT fill:#FFFFFF,stroke:#000000,stroke-width:2px
    end

    subgraph LEG["Legend"]
        direction LR
        leg0["Trust zone"]
        leg1["Component"]
        leg2["Ubuntu default"]
        leg3["Platform-dependent"]
        leg4s[" "] --> leg4["Data flow"]
        leg0 ~~~ leg1
        leg1 ~~~ leg2
        leg2 ~~~ leg3
        leg3 ~~~ leg4s
    end
    MAIN ~~~ LEG

    classDef component fill:#F3F3F3,stroke:#000000,stroke-width:1px,color:#000000
    classDef hidden fill:none,stroke:none,color:#FFFFFF
    classDef note fill:#FFFFFF,stroke:none,color:#000000
    classDef platform fill:#000000,stroke:#666666,stroke-width:2px,stroke-dasharray:4 4,color:#FFFFFF
    classDef ubuntu fill:#000000,stroke:#000000,stroke-width:1px,color:#FFFFFF
    classDef zone fill:#FFFFFF,stroke:#000000,stroke-width:2px,color:#000000
    class initrd component
    class shim,grub,kernel ubuntu
    class uefi,tpm,lockdown platform
    class leg0 zone
    class leg1 component
    class leg2 ubuntu
    class leg3 platform
    class leg4 note
    class leg4s hidden
    click uefi href "#security-architecture-boot"
    click tpm href "#security-architecture-boot"
    click shim href "#security-architecture-boot"
    click grub href "#security-architecture-boot"
    click kernel href "#security-architecture-boot"
    click initrd href "#security-architecture-boot"
    click lockdown href "#security-architecture-kernel-modules"
    style LEG fill:#FFFFFF,stroke:#666666,stroke-width:1px
    style MAIN fill:none,stroke:none
```

When UEFI Secure Boot is enabled, each boot stage verifies the signature of
the next one before running it:

1. The UEFI firmware verifies `shim`, which is signed by the Microsoft UEFI
   certificate authority (CA).
1. `shim` verifies GRUB, which is signed by Canonical. `shim` also accepts
   code signed with a Machine Owner Key (MOK) that you enrolled.
1. GRUB asks `shim` to verify the Linux kernel, which is signed by Canonical.
1. The kernel enables lockdown in integrity mode, and only loads kernel
   modules with a valid signature.

GRUB also loads the initial RAM file system (`initramfs`). Ubuntu generates
the `initramfs` on the system when you install or update a kernel, so it is not
signed, and Secure Boot does not verify it.

If the system has a Trusted Platform Module (TPM) 2.0, the firmware and the
boot chain extend a measurement of each stage, its configuration, and the
`initramfs` into the TPM's Platform Configuration Registers (PCRs). The PCR
values do not stop a modified system from booting, but the TPM only releases
secrets sealed to the expected PCR values. See
[UEFI Secure Boot](https://documentation.ubuntu.com/security/security-features/platform-protections/secure-boot/)
and
[Trusted Platform Module](https://documentation.ubuntu.com/security/security-features/platform-protections/trusted-platform-module/).

(security-architecture-data-at-rest)=
## Data at rest and key protection

Encryption protects data on disk, and the kernel protects the keys in memory.

```{mermaid}
:alt: Data at rest and key protection. An optional LUKS encrypted volume on disk is unlocked at boot by one of three methods, all opt-in: a passphrase entered in the initramfs, Clevis, or TPM-backed FDE. Clevis and TPM-backed FDE ask the TPM to unseal the key, which it does only if the PCR values match. dm-crypt receives the volume key, keeps it in the kernel keyrings, and encrypts and decrypts the blocks of the volume.
:caption: Unlocking encrypted storage

---
config:
  theme: base
  fontFamily: Ubuntu variable, Ubuntu, sans-serif
  themeCSS: 'svg, svg * { font-family: Ubuntu variable, Ubuntu, sans-serif !important; } .flowchart-link { stroke-width: 3px !important; } .edge-pattern-dotted { stroke-dasharray: 8 5 !important; }'
  flowchart:
    curve: linear
  themeVariables:
    fontFamily: Ubuntu variable, Ubuntu, sans-serif
    lineColor: "#E95420"
    primaryColor: "#F3F3F3"
    primaryBorderColor: "#000000"
    primaryTextColor: "#000000"
    clusterBkg: "#FFFFFF"
    clusterBorder: "#000000"
    edgeLabelBackground: "#FFFFFF"
---
flowchart TB
    subgraph MAIN[" "]
        direction TB
        subgraph UNLOCK["Disk unlock methods"]
            pass["Passphrase<br>(opt-in)"]
            clevis["Clevis TPM unlock<br>(opt-in)"]
            tpmfde["TPM-backed FDE<br>(opt-in, Desktop)"]
        end
        subgraph RUN["Running system"]
            initrd["initramfs"]
            dmcrypt["dm-crypt"]
            keyring[("Kernel keyrings<br>(keyctl)")]
        end
        subgraph HW["Hardware"]
            tpm["TPM 2.0<br>(platform-dependent)"]
            luks[("LUKS encrypted volume<br>(opt-in)")]
        end
        tpm -.->|"Unseals key if<br>PCRs match"| clevis
        tpm -.->|"Unseals key if<br>PCRs match"| tpmfde
        pass -.->|"Passphrase"| initrd
        clevis -.->|"Key"| initrd
        tpmfde -.->|"Key"| dmcrypt
        initrd -.->|"Volume key"| dmcrypt
        dmcrypt -.->|"Volume key"| keyring
        dmcrypt -.->|"Encrypted blocks"| luks
        style UNLOCK fill:#FFFFFF,stroke:#000000,stroke-width:1px,stroke-dasharray:4 4
        style RUN fill:#FFFFFF,stroke:#000000,stroke-width:2px
        style HW fill:#FFFFFF,stroke:#000000,stroke-width:2px
    end

    subgraph LEG["Legend"]
        direction LR
        leg0["Trust zone"]
        leg1["Component"]
        leg2["Opt-in"]
        leg3["Platform-dependent"]
        leg4s[" "] -.-> leg4["Untrusted or<br>optional flow"]
        leg0 ~~~ leg1
        leg1 ~~~ leg2
        leg2 ~~~ leg3
        leg3 ~~~ leg4s
    end
    MAIN ~~~ LEG

    classDef component fill:#F3F3F3,stroke:#000000,stroke-width:1px,color:#000000
    classDef hidden fill:none,stroke:none,color:#FFFFFF
    classDef note fill:#FFFFFF,stroke:none,color:#000000
    classDef optin fill:#F3F3F3,stroke:#000000,stroke-width:1px,stroke-dasharray:4 4,color:#000000
    classDef platform fill:#000000,stroke:#666666,stroke-width:2px,stroke-dasharray:4 4,color:#FFFFFF
    classDef zone fill:#FFFFFF,stroke:#000000,stroke-width:2px,color:#000000
    class initrd,dmcrypt,keyring component
    class tpm platform
    class pass,clevis,tpmfde,luks optin
    class leg0 zone
    class leg1 component
    class leg2 optin
    class leg3 platform
    class leg4 note
    class leg4s hidden
    click pass href "#security-architecture-full-disk-encryption"
    click clevis href "#security-architecture-tpm-unlock"
    click tpmfde href "#security-architecture-tpm-unlock"
    click initrd href "#security-architecture-boot"
    click dmcrypt href "#security-architecture-full-disk-encryption"
    click keyring href "#security-architecture-keyrings"
    click tpm href "#security-architecture-boot"
    click luks href "#security-architecture-full-disk-encryption"
    style LEG fill:#FFFFFF,stroke:#666666,stroke-width:1px
    style MAIN fill:none,stroke:none
```

(security-architecture-full-disk-encryption)=
### Full disk encryption

Both the Ubuntu Server and the Ubuntu Desktop installers can encrypt the disk
with Linux Unified Key Setup (LUKS) and `dm-crypt`, for example by encrypting
the Logical Volume Manager (LVM) volume group. By default, you unlock the disk
at boot with a passphrase. See
[full disk encryption](https://documentation.ubuntu.com/security/security-features/storage/encryption-full-disk/)
and [encrypted LVM](https://documentation.ubuntu.com/security/security-features/storage/encrypted-lvm/).

(security-architecture-tpm-unlock)=
### TPM-backed unlocking

On supported hardware, which provides UEFI Secure Boot, a TPM 2.0, and an
IOMMU, the Ubuntu Desktop installer offers TPM-backed full disk encryption.
The kernel and `initramfs` are then delivered as a single signed image, so
that Secure Boot verifies both, and the TPM releases the disk key only if the
measured boot state matches the expected state. On Ubuntu Server, and on any
existing LUKS installation, you can bind the encrypted volume to the TPM with
Clevis to unlock it without a passphrase, which suits unattended systems. See
{ref}`tpm-backed-luks-decryption-with-clevis`.

:::{note}
In Ubuntu 24.04 LTS, TPM-backed FDE in the Desktop installer is an
experimental feature.
:::

(security-architecture-keyrings)=
### Kernel keyrings

Kernel keyrings hold keys, such as disk encryption keys and authentication
tokens, in kernel memory with per-key access control. Processes access them
with {manpage}`keyctl(1)`. See {manpage}`keyrings(7)`.

(security-architecture-hardware-boundary)=
## Runtime hardware and firmware boundary

At runtime, the kernel controls which code it loads, which devices it accepts,
and which memory devices can reach.

```{mermaid}
:alt: Runtime hardware and firmware boundary. Peripherals and removable media from outside the system attach to the kernel drivers and udev, optionally filtered by a usbguard allow list (opt-in). Their DMA requests pass the IOMMU (platform-dependent). Kernel modules, including third-party modules built with DKMS and signed with a MOK, are loaded only after the module signature check (platform-dependent). fwupd downloads signed firmware and metadata from the LVFS and installs verified updates into the device and system firmware.
:caption: Devices, kernel modules, and firmware at runtime

---
config:
  theme: base
  fontFamily: Ubuntu variable, Ubuntu, sans-serif
  themeCSS: 'svg, svg * { font-family: Ubuntu variable, Ubuntu, sans-serif !important; } .flowchart-link { stroke-width: 3px !important; } .edge-pattern-dotted { stroke-dasharray: 8 5 !important; }'
  flowchart:
    curve: linear
  themeVariables:
    fontFamily: Ubuntu variable, Ubuntu, sans-serif
    lineColor: "#E95420"
    primaryColor: "#F3F3F3"
    primaryBorderColor: "#000000"
    primaryTextColor: "#000000"
    clusterBkg: "#FFFFFF"
    clusterBorder: "#000000"
    edgeLabelBackground: "#FFFFFF"
---
flowchart TB
    subgraph MAIN[" "]
        direction TB
        subgraph OUTSIDE["Outside — untrusted"]
            dev["Peripherals and<br>removable media"]
        end
        subgraph EXTSVC["External services"]
            lvfs["LVFS<br>(firmware updates)"]
        end
        subgraph RUN["Running system"]
            usbguard["usbguard allow list<br>(opt-in)"]
            drivers["Kernel drivers and udev"]
            dkms["Third-party modules<br>(DKMS, signed with MOK)"]
            modsig["Module signature check<br>(platform-dependent)"]
            fwupd["fwupd"]
        end
        subgraph HW["Hardware and firmware"]
            iommu["IOMMU<br>(platform-dependent)"]
            fw["Device and system firmware"]
        end
        dev -.->|"Device attach"| drivers
        usbguard -.->|"Allow or block"| drivers
        dev -.->|"DMA requests"| iommu
        dkms -->|"Load request"| modsig
        modsig -->|"Signed modules"| drivers
        lvfs -->|"Signed firmware<br>and metadata"| fwupd
        fwupd -->|"Verified update"| fw
        style OUTSIDE fill:#FFFFFF,stroke:#000000,stroke-width:2px
        style EXTSVC fill:#FFFFFF,stroke:#000000,stroke-width:2px
        style RUN fill:#FFFFFF,stroke:#000000,stroke-width:2px
        style HW fill:#FFFFFF,stroke:#000000,stroke-width:2px
    end

    subgraph LEG["Legend"]
        direction LR
        leg0["Trust zone"]
        leg1["Untrusted"]
        leg2["External service"]
        leg3["Component"]
        leg4["Ubuntu default"]
        leg5["Opt-in"]
        leg6["Platform-dependent"]
        leg7s[" "] --> leg7["Data flow"]
        leg8s[" "] -.-> leg8["Untrusted or<br>optional flow"]
        leg0 ~~~ leg1
        leg1 ~~~ leg2
        leg2 ~~~ leg3
        leg3 ~~~ leg4
        leg5 ~~~ leg6
        leg6 ~~~ leg7s
        leg7 ~~~ leg8s
    end
    MAIN ~~~ LEG

    classDef component fill:#F3F3F3,stroke:#000000,stroke-width:1px,color:#000000
    classDef external fill:#FFFFFF,stroke:#000000,stroke-width:1px,color:#000000
    classDef hidden fill:none,stroke:none,color:#FFFFFF
    classDef note fill:#FFFFFF,stroke:none,color:#000000
    classDef optin fill:#F3F3F3,stroke:#000000,stroke-width:1px,stroke-dasharray:4 4,color:#000000
    classDef platform fill:#000000,stroke:#666666,stroke-width:2px,stroke-dasharray:4 4,color:#FFFFFF
    classDef ubuntu fill:#000000,stroke:#000000,stroke-width:1px,color:#FFFFFF
    classDef untrusted fill:#FFFFFF,stroke:#000000,stroke-width:1px,stroke-dasharray:4 4,color:#000000
    classDef zone fill:#FFFFFF,stroke:#000000,stroke-width:2px,color:#000000
    class dev untrusted
    class lvfs external
    class drivers,dkms,fw component
    class fwupd ubuntu
    class iommu,modsig platform
    class usbguard optin
    class leg0 zone
    class leg1 untrusted
    class leg2 external
    class leg3 component
    class leg4 ubuntu
    class leg5 optin
    class leg6 platform
    class leg7 note
    class leg7s hidden
    class leg8 note
    class leg8s hidden
    click dev href "#security-architecture-devices"
    click usbguard href "#security-architecture-devices"
    click drivers href "#security-architecture-devices"
    click dkms href "#security-architecture-kernel-modules"
    click modsig href "#security-architecture-kernel-modules"
    click fwupd href "#security-architecture-firmware-updates"
    click fw href "#security-architecture-firmware-updates"
    click iommu href "#security-architecture-dma"
    style LEG fill:#FFFFFF,stroke:#666666,stroke-width:1px
    style MAIN fill:none,stroke:none
```

Other pages describe further elements of this diagram. See {ref}`security-architecture-lvfs`.

(security-architecture-kernel-modules)=
### Kernel modules

With Secure Boot enabled, the kernel only loads modules signed by Canonical or
with an enrolled MOK. When you install a third-party driver with DKMS, Ubuntu
signs the module with a MOK, which you enroll at the next boot.

(security-architecture-devices)=
### Devices and removable media

The kernel drivers and {manpage}`udev(7)` handle every new device. Data on
removable media is untrusted input. To control which USB devices the system
accepts, you can install {manpage}`usbguard-daemon(8)`. See
[devices](https://documentation.ubuntu.com/security/security-features/platform-protections/devices/).

(security-architecture-dma)=
### DMA protection

An Input-Output Memory Management Unit (IOMMU) restricts which memory a device
can access through DMA. This protects against malicious peripherals, such as
Thunderbolt devices. The protection depends on hardware support and firmware
settings.

(security-architecture-firmware-updates)=
### Firmware updates

`fwupd` downloads firmware from the LVFS, verifies the signed metadata, and
installs the update through the device's or system's update mechanism.
