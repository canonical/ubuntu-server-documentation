---
myst:
  html_meta:
    description: "The four layers of security mechanisms in Ubuntu, from the network to the hardware, and which of them are enabled by default."
---

(security-architecture-layers)=
(defense-in-depth-layers)=
# Layered defense-in-depth architecture

Ubuntu protects the system with four layers of security mechanisms. Each layer
assumes that the layer above it can fail or be compromised, so an attacker
needs to defeat several independent mechanisms to compromise the system.

The diagrams on this page follow the
{ref}`diagram conventions <security-architecture-legend>`. To go to the
explanation of a box, select the box in the diagram.

Many of these mechanisms are part of the upstream Linux kernel and userspace,
and are available on any Linux distribution. Ubuntu adds its own defaults and
integrations on top of them. In the diagrams of each layer, light gray boxes
show upstream mechanisms, and black boxes show Ubuntu defaults.

```{mermaid}
:alt: Overview of the four security layers, from top to bottom: 1, network and perimeter; 2, userspace; 3, Linux kernel; 4, hardware, firmware, and boot chain. Accepted connections pass from the network layer to userspace, system calls pass from userspace to the kernel, and device and storage access passes from the kernel to the hardware.
:caption: The four security layers of Ubuntu

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
        L1["1 — Network and perimeter"]
        L2["2 — Userspace<br>(deb packages, systemd services, snaps)"]
        L3["3 — Linux kernel"]
        L4["4 — Hardware, firmware, and boot chain"]
        L1 -->|"Accepted connections"| L2
        L2 -->|"System calls"| L3
        L3 -->|"Device and storage access"| L4
    end

    subgraph LEG["Legend"]
        direction LR
        leg0["Layer"]
        leg1s[" "] --> leg1["Data flow"]
        leg0 ~~~ leg1s
    end
    MAIN ~~~ LEG

    classDef component fill:#F3F3F3,stroke:#000000,stroke-width:1px,color:#000000
    classDef hidden fill:none,stroke:none,color:#FFFFFF
    classDef note fill:#FFFFFF,stroke:none,color:#000000
    class L1,L2,L3,L4 component
    class leg0 component
    class leg1 note
    class leg1s hidden
    click L1 href "#security-architecture-layer-network"
    click L2 href "#security-architecture-layer-userspace"
    click L3 href "#security-architecture-layer-kernel"
    click L4 href "#security-architecture-layer-hardware"
    style LEG fill:#FFFFFF,stroke:#666666,stroke-width:1px
    style MAIN fill:none,stroke:none
```

(security-architecture-layer-network)=
## Network and perimeter

The network layer filters and authenticates traffic before it reaches a
service. The kernel's Netfilter framework, configured through `nftables`,
filters packets. Ubuntu installs {manpage}`ufw(8)` as a front end to
Netfilter, but does not enable it. TCP SYN cookies, enabled by default,
protect against SYN flood attacks. See {ref}`firewalls`.

```{mermaid}
:alt: Network and perimeter layer: Netfilter and nftables packet filtering, TCP SYN cookies, and the no open ports policy; ufw host firewall rules (opt-in), chrony with NTS, and DNSSEC validation (opt-in).
:caption: Mechanisms of the network and perimeter layer

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
        subgraph L1["1 — Network and perimeter"]
            direction LR
            nft["Netfilter and nftables<br>packet filtering"]
            syn["TCP SYN cookies"]
            ports["No open ports policy"]
            ufw["ufw host firewall rules<br>(opt-in)"]
            nts["chrony with NTS"]
            dnssec["DNSSEC validation<br>(opt-in)"]
            nft ~~~ syn ~~~ ports
            ufw ~~~ nts ~~~ dnssec
        end
        style L1 fill:#FFFFFF,stroke:#000000,stroke-width:2px
    end

    subgraph LEG["Legend"]
        direction LR
        leg0["Component"]
        leg1["Ubuntu default"]
        leg2["Opt-in"]
        leg0 ~~~ leg1
        leg1 ~~~ leg2
    end
    MAIN ~~~ LEG

    classDef component fill:#F3F3F3,stroke:#000000,stroke-width:1px,color:#000000
    classDef optin fill:#F3F3F3,stroke:#000000,stroke-width:1px,stroke-dasharray:4 4,color:#000000
    classDef ubuntu fill:#000000,stroke:#000000,stroke-width:1px,color:#FFFFFF
    class nft,syn component
    class ports,nts ubuntu
    class ufw,dnssec optin
    class leg0 component
    class leg1 ubuntu
    class leg2 optin
    style LEG fill:#FFFFFF,stroke:#666666,stroke-width:1px
    style MAIN fill:none,stroke:none
```

Other pages describe further elements of this diagram. See {ref}`security-architecture-packet-filtering`, {ref}`security-architecture-network-peers`, and {ref}`security-architecture-infrastructure-services`.

Connections that pass the network layer reach a service that listens in
userspace. Only services that you install listen on the network, and each
service authenticates its clients and validates their input itself, as
OpenSSH does. See {ref}`security-architecture-network-boundary`.

(security-architecture-layer-userspace)=
## Userspace

Userspace runs services and applications from `deb` packages and snaps.
Ubuntu verifies every package that it installs from the archive or the Snap
Store, and installs security updates automatically with
`unattended-upgrades`. Ubuntu builds packages with hardened compiler and linker
flags, and ships AppArmor profiles for many packaged services and
applications. `snapd` confines each strictly confined snap with several kernel
mechanisms at once. See {ref}`automatic-updates`.

```{mermaid}
:alt: Userspace layer: PAM and polkit, systemd service sandboxing, sudo-rs with the root account locked, APT signature verification and unattended security updates, AppArmor profiles for packaged software, snapd strict confinement, hardened compiler flags, and auditd and USG hardening profiles (opt-in).
:caption: Mechanisms of the userspace layer

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
        subgraph L2["2 — Userspace"]
            direction LR
            pam["PAM and polkit"]
            sysd["systemd service sandboxing"]
            sudo["sudo-rs, root account locked"]
            apt["APT signature verification,<br>unattended security updates"]
            aaprof["AppArmor profiles for<br>packaged software"]
            snap["snapd strict confinement<br>(AppArmor, seccomp, device<br>cgroup, mount namespace)"]
            flags["Hardened compiler flags<br>(PIE, stack protector, FORTIFY)"]
            audit["auditd, USG hardening profiles<br>(opt-in)"]
            pam ~~~ sysd ~~~ sudo ~~~ apt
            aaprof ~~~ snap ~~~ flags ~~~ audit
        end
        style L2 fill:#FFFFFF,stroke:#000000,stroke-width:2px
    end

    subgraph LEG["Legend"]
        direction LR
        leg0["Component"]
        leg1["Ubuntu default"]
        leg2["Opt-in"]
        leg0 ~~~ leg1
        leg1 ~~~ leg2
    end
    MAIN ~~~ LEG

    classDef component fill:#F3F3F3,stroke:#000000,stroke-width:1px,color:#000000
    classDef optin fill:#F3F3F3,stroke:#000000,stroke-width:1px,stroke-dasharray:4 4,color:#000000
    classDef ubuntu fill:#000000,stroke:#000000,stroke-width:1px,color:#FFFFFF
    class pam,sysd component
    class sudo,apt,aaprof,snap,flags ubuntu
    class audit optin
    class leg0 component
    class leg1 ubuntu
    class leg2 optin
    style LEG fill:#FFFFFF,stroke:#666666,stroke-width:1px
    style MAIN fill:none,stroke:none
```

Other pages describe further elements of this diagram. See {ref}`security-architecture-pam`, {ref}`security-architecture-service-sandboxing`, {ref}`security-architecture-sudo-rs`, {ref}`security-architecture-archive`, {ref}`security-architecture-apparmor`, and {ref}`security-architecture-snap-store`.

Userspace processes cannot access files, devices, the network, or other
processes directly. To do so, they make a system call: a request that switches
the CPU from user mode to the kernel at a fixed entry point. The kernel then
checks the request against the credentials of the process and the loaded
security policies before it acts on it. See
{ref}`security-architecture-syscall-boundary`.

(security-architecture-layer-kernel)=
## Linux kernel

The kernel enforces access control and isolation for every process. Upstream
Linux provides discretionary access control (DAC), capabilities, namespaces,
cgroups, and seccomp. Ubuntu enables AppArmor as its Linux Security Module
(LSM), restricts `ptrace` with the Yama LSM, restricts unprivileged user
namespaces through AppArmor, and configures the kernel to hide kernel
addresses and randomize the kernel's location in memory. See
[kernel protections](https://documentation.ubuntu.com/security/security-features/kernel-protections/).

```{mermaid}
:alt: Linux kernel layer: DAC, POSIX ACLs and capabilities, namespaces and cgroups v2, seccomp-bpf, AppArmor enforced, Yama ptrace scope, unprivileged user namespace restriction, kernel memory hardening, and lockdown with module signature enforcement (platform-dependent).
:caption: Mechanisms of the Linux kernel layer

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
        subgraph L3["3 — Linux kernel"]
            direction LR
            dac["DAC, POSIX ACLs,<br>capabilities"]
            nscg["Namespaces, cgroups v2"]
            seccomp["seccomp-bpf"]
            khard["Kernel memory hardening<br>(KASLR, kptr_restrict, RO/NX)"]
            aa["AppArmor LSM enforced"]
            yama["Yama ptrace scope"]
            userns["Unprivileged user<br>namespace restriction"]
            lockdown["Lockdown, module signature<br>enforcement (platform-dependent)"]
            dac ~~~ nscg ~~~ seccomp ~~~ khard
            aa ~~~ yama ~~~ userns ~~~ lockdown
        end
        style L3 fill:#FFFFFF,stroke:#000000,stroke-width:2px
    end

    subgraph LEG["Legend"]
        direction LR
        leg0["Component"]
        leg1["Ubuntu default"]
        leg2["Platform-dependent"]
        leg0 ~~~ leg1
        leg1 ~~~ leg2
    end
    MAIN ~~~ LEG

    classDef component fill:#F3F3F3,stroke:#000000,stroke-width:1px,color:#000000
    classDef platform fill:#000000,stroke:#666666,stroke-width:2px,stroke-dasharray:4 4,color:#FFFFFF
    classDef ubuntu fill:#000000,stroke:#000000,stroke-width:1px,color:#FFFFFF
    class dac,nscg,seccomp component
    class aa,yama,userns,khard ubuntu
    class lockdown platform
    class leg0 component
    class leg1 ubuntu
    class leg2 platform
    style LEG fill:#FFFFFF,stroke:#666666,stroke-width:1px
    style MAIN fill:none,stroke:none
```

Other pages describe further elements of this diagram. See {ref}`security-architecture-dac`, {ref}`security-architecture-namespaces`, {ref}`security-architecture-seccomp`, {ref}`security-architecture-apparmor`, {ref}`security-architecture-yama`, and {ref}`security-architecture-kernel-modules`.

Only the kernel accesses the hardware: it drives devices, manages memory, and
reads and writes storage on behalf of processes. In the other direction,
devices signal the kernel through interrupts, and can read and write memory
directly through direct memory access (DMA), which the IOMMU restricts. Which
kernel runs at all is decided earlier, by the boot chain. See
{ref}`security-architecture-lower-boundary`.

(security-architecture-layer-hardware)=
## Hardware, firmware, and boot chain

The lowest layer anchors trust in the hardware. When UEFI Secure Boot is
enabled, the firmware verifies the boot loader, and the boot loader verifies
the kernel. Ubuntu ships {manpage}`fwupdmgr(1)` to install signed firmware
updates. Full disk encryption protects data at rest, if you enable it during
installation.

```{mermaid}
:alt: Hardware, firmware, and boot chain layer: UEFI Secure Boot chain (platform-dependent), TPM 2.0 measured boot (platform-dependent), IOMMU DMA protection (platform-dependent), fwupd firmware updates, and LUKS full disk encryption (opt-in).
:caption: Mechanisms of the hardware, firmware, and boot chain layer

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
        subgraph L4["4 — Hardware, firmware, and boot chain"]
            direction LR
            sb["UEFI Secure Boot: shim, GRUB,<br>kernel (platform-dependent)"]
            tpm["TPM 2.0 measured boot<br>(platform-dependent)"]
            iommu["IOMMU DMA protection<br>(platform-dependent)"]
            fwupd["fwupd firmware updates"]
            fde["LUKS full disk encryption<br>(opt-in)"]
            sb ~~~ tpm ~~~ iommu
            fwupd ~~~ fde
        end
        style L4 fill:#FFFFFF,stroke:#000000,stroke-width:2px
    end

    subgraph LEG["Legend"]
        direction LR
        leg0["Ubuntu default"]
        leg1["Opt-in"]
        leg2["Platform-dependent"]
        leg0 ~~~ leg1
        leg1 ~~~ leg2
    end
    MAIN ~~~ LEG

    classDef optin fill:#F3F3F3,stroke:#000000,stroke-width:1px,stroke-dasharray:4 4,color:#000000
    classDef platform fill:#000000,stroke:#666666,stroke-width:2px,stroke-dasharray:4 4,color:#FFFFFF
    classDef ubuntu fill:#000000,stroke:#000000,stroke-width:1px,color:#FFFFFF
    class fwupd ubuntu
    class fde optin
    class sb,tpm,iommu platform
    class leg0 ubuntu
    class leg1 optin
    class leg2 platform
    style LEG fill:#FFFFFF,stroke:#666666,stroke-width:1px
    style MAIN fill:none,stroke:none
```

Other pages describe further elements of this diagram. See {ref}`security-architecture-boot`, {ref}`security-architecture-dma`, {ref}`security-architecture-firmware-updates`, and {ref}`security-architecture-full-disk-encryption`.

(security-architecture-defaults)=
## Default and configurable protections

The following table summarizes which protections are active on a new
installation of Ubuntu, and which you need to enable or configure.

| Protection | Default state | What you need to do |
|---|---|---|
| AppArmor enforced, with profiles for packaged software | Enabled by default | Do not disable AppArmor. Write profiles for your own services. See {ref}`apparmor`. |
| snap confinement | Enabled by default | Review the interfaces that snaps request, and avoid `classic` or `devmode` confinement for untrusted snaps. |
| Yama `ptrace` scope, kernel memory hardening, unprivileged user namespace restriction | Enabled by default | Avoid weakening these protections. See [dangerous sysctls](https://documentation.ubuntu.com/security/common-mistakes/dangerous-sysctls/). |
| Archive signature verification and unattended security updates | Enabled by default | Only add trusted package sources. Plan reboots for kernel updates. |
| Root account locked, administration through `sudo` | Enabled by default | Grant administrative rights only to users who need them. |
| Authenticated time synchronization (NTS) | Enabled by default | No action needed for new installations. |
| UEFI Secure Boot, kernel lockdown, module signature enforcement | Platform-dependent | Enable Secure Boot in the firmware. |
| TPM measured boot and IOMMU DMA protection | Platform-dependent | Use hardware that provides them, and enable them in the firmware. |
| Host firewall rules | Opt-in | Enable `ufw` or write `nftables` rules. See {ref}`firewalls`. |
| Full disk encryption | Opt-in | Select encryption during installation. To unlock with the TPM, use TPM-backed FDE on Ubuntu Desktop, or Clevis on Ubuntu Server. |
| DNSSEC validation | Opt-in | Enable validation in the resolver. See {ref}`install-dnssec`. |
| System auditing and compliance hardening | Opt-in | Install `auditd`, or apply a hardening profile with the [Ubuntu Security Guide (USG)](https://documentation.ubuntu.com/security/compliance/usg/). |

:::{note}
Ubuntu 24.04 LTS uses `sudo` instead of `sudo-rs` as the default `sudo`
provider. See {ref}`sudo-rs`.
:::
