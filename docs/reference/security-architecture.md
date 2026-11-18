---
myst:
  html_meta:
    description: "Reference for the security architecture of Ubuntu: trust boundaries, layered defenses, boot chain, and the default state of each security mechanism."
---

(security-architecture)=
# System architecture from a security perspective

This page describes the security architecture of Ubuntu as a general-purpose
operating system: the platform that Ubuntu Server and Ubuntu Desktop share,
with software delivered as `deb` packages and snaps. It identifies the trust
boundaries of an Ubuntu system, the mechanisms that protect each boundary, and
which of those mechanisms are active by default and which you need to enable.

Use this page to:

* understand where untrusted input enters a system and what mediates it
* decide which additional protections your deployment needs
* support security assessments, such as the technical documentation required
  by the EU Cyber Resilience Act (CRA)

(security-architecture-purpose)=
## Purpose and scope

The CRA, Regulation (EU) 2024/2847, requires manufacturers of products with
digital elements to describe the system architecture of their product,
including how its software components build on each other (Annex VII). It also
requires them to show how the product meets essential cybersecurity
requirements (Annex I), such as a secure-by-default configuration, protection
against unauthorized access, a limited attack surface, and exploitation
mitigation. If you build a product on top of Ubuntu, this page describes the
architecture that your product inherits.

The architecture separates five zones:

* untrusted external entities, such as network peers and attached devices
* external infrastructure services that Ubuntu relies on, such as the Ubuntu
  archive and the Snap Store
* userspace workloads: services and applications from `deb` packages and snaps
* the Linux kernel, which enforces access control and isolation
* hardware, firmware, and the boot chain, which anchor trust in the system

Canonical maintains a detailed threat model for the Ubuntu platform, which
lists the assets of the system, the data flows between them, and the controls
that mitigate threats to them. This page is a high-level view derived from
that threat model. It groups those assets, data flows, and controls by trust
boundary, so that you can see how they relate to one another.

This page describes Ubuntu 26.04 LTS. Notes highlight where Ubuntu 24.04 LTS
differs. Ubuntu Core uses a different, all-snap architecture and is not
covered here. Components that only exist on Ubuntu Desktop, such as the display
server and desktop portals, are mentioned only where they change a trust
boundary.

(security-architecture-legend)=
## How to read the diagrams

The diagrams on this page use the following conventions. Every label that
describes a non-default state also carries a text tag, so the meaning does not
depend on color or line style alone.

| Element | Appearance | Meaning |
|---|---|---|
| Trust zone | Box with a thick black border | A region with a common trust level, for example `Outside — untrusted` |
| Untrusted actor | White box, dashed border | An entity outside the system that you cannot trust |
| External service | White box, solid border | Infrastructure outside the system that Ubuntu relies on |
| System component or upstream mechanism | Light gray box, solid border | A component of the system, or a mechanism provided by the upstream Linux kernel or userspace |
| Ubuntu default | Black box, white text | A mechanism that Ubuntu enables or configures by default |
| Opt-in | Light gray box, dashed border, tagged `(opt-in)` | A mechanism that you need to choose and enable |
| Platform-dependent | Black box, dashed border, tagged `(platform-dependent)` | A mechanism that Ubuntu uses by default when the hardware or firmware supports and enables it |
| Data flow | Solid orange arrow | Data that crosses a boundary, in the direction of the arrow |
| Untrusted or optional flow | Dashed orange arrow | Untrusted input, or a flow that only exists when you enable an opt-in mechanism |

(security-architecture-context)=
## System context and external trust boundaries

An Ubuntu system interacts with two kinds of external entity. Untrusted
entities, such as users, network peers, and attached devices, can send
arbitrary input to the system. External infrastructure services, such as the
Ubuntu archive, provide content that the system depends on. Ubuntu does not
trust the transport to these services: it verifies the content it receives
from them with cryptographic signatures.

```{mermaid}
:alt: Context diagram. Three zones: Outside — untrusted (users and administrators, untrusted network peers, removable media and peripherals), External infrastructure services (Ubuntu archive and mirrors, Snap Store, LVFS, time, name, and identity services), and Inside — Ubuntu system (network-facing services, services and applications, outbound system clients, privileged components, and secrets and configuration). Arrows show the data flows that cross the zone boundaries.
:caption: System context and trust boundaries of an Ubuntu system

%%{init: {"theme": "base", "themeVariables": {"fontFamily": "Ubuntu Sans, Ubuntu, sans-serif", "lineColor": "#E95420", "primaryColor": "#F3F3F3", "primaryBorderColor": "#000000", "primaryTextColor": "#000000", "clusterBkg": "#FFFFFF", "clusterBorder": "#000000", "titleColor": "#000000", "edgeLabelBackground": "#FFFFFF"}, "flowchart": {"curve": "linear"}}}%%
flowchart TB
    subgraph OUT["Outside — untrusted"]
        users["Remote and local users<br>and administrators"]
        peers["Untrusted network peers<br>(LAN, internet, DHCP)"]
        media["Removable media and peripherals<br>(USB, Thunderbolt, wireless)"]
    end

    subgraph EXT["External infrastructure services (outside boundary)"]
        archive["Ubuntu archive and mirrors"]
        store["Snap Store"]
        lvfs["LVFS<br>(firmware updates)"]
        infra["Time, name, and identity services<br>(NTP, DNS, identity providers)"]
    end

    subgraph IN["Inside — Ubuntu system"]
        net["Network-facing services<br>(SSH and other daemons)"]
        apps["Services and applications<br>(deb packages and snaps)"]
        clients["Outbound system clients<br>(APT, snapd, fwupd, chrony, resolver)"]
        priv["Privileged components<br>(kernel, udev, PAM, root daemons)"]
        data[("Secrets and configuration<br>(keys, /etc, user data)")]
    end

    users -->|"SSH and service requests<br>(encrypted, authenticated)"| net
    peers -.->|"Untrusted traffic<br>(kernel network stack)"| net
    media -.->|"Device attach and data<br>(udev, kernel drivers)"| priv
    archive -->|"Packages<br>(GPG-signed metadata)"| clients
    store -->|"Snaps<br>(signed assertions)"| clients
    lvfs -->|"Firmware<br>(signed metadata)"| clients
    infra -->|"Time (NTS), DNS answers,<br>authentication results"| clients
    net -->|"Requests"| apps
    net -->|"Authentication"| priv
    apps -->|"System calls, D-Bus"| priv
    priv -->|"Key and file access"| data

    classDef untrusted fill:#FFFFFF,stroke:#000000,stroke-width:1px,stroke-dasharray:4 4,color:#000000
    classDef external fill:#FFFFFF,stroke:#000000,stroke-width:1px,color:#000000
    classDef component fill:#F3F3F3,stroke:#000000,stroke-width:1px,color:#000000
    class users,peers,media untrusted
    class archive,store,lvfs,infra external
    class net,apps,clients,priv,data component
    style OUT fill:#FFFFFF,stroke:#000000,stroke-width:2px
    style EXT fill:#FFFFFF,stroke:#000000,stroke-width:2px
    style IN fill:#FFFFFF,stroke:#000000,stroke-width:2px
```

The diagram shows the following boundary crossings:

Users and administrators
: Reach the system through network-facing services, such as
  {manpage}`sshd(8)`, or through a local console. Network-facing services hand
  credentials to privileged components, such as Pluggable Authentication
  Modules (PAM), to authenticate users. See
  {ref}`openssh-server` and {ref}`user-management`.

Untrusted network peers
: Can send arbitrary traffic, which the kernel network stack handles
  before it reaches a service. Firewall rules, if you configure them, filter
  this traffic in the kernel. A default installation follows a
  [no open ports](https://documentation.ubuntu.com/security/security-features/network/open-ports/)
  policy, so only explicitly installed services listen on the network. Network
  configuration received from a Dynamic Host Configuration Protocol (DHCP)
  server is also untrusted input.

Removable media and peripherals
: Attach directly to privileged components: the kernel and `udev` handle every
  new device. Data on removable media is untrusted, even when a trusted local
  user mounts it.

Ubuntu archive and mirrors
: APT verifies packages against signed archive metadata, so mirrors and
  proxies do not need to be trusted. See
  [Ubuntu archive integrity verification](https://documentation.ubuntu.com/security/software-integrity/archive-verification/).

Snap Store
: `snapd` verifies each snap against assertions signed by the store before it
  installs the snap.

Linux Vendor Firmware Service (LVFS)
: `fwupd` downloads firmware metadata and updates from the LVFS and verifies
  their signatures before it applies an update.

Time, name, and identity services
: Ubuntu synchronizes time with `chrony`, which uses Network Time Security
  (NTS) to authenticate Ubuntu's time servers. DNS answers are not
  authenticated unless you enable DNS Security Extensions (DNSSEC)
  validation. Identity providers, such as LDAP, Kerberos, or Active Directory,
  are only used if you configure them.

:::{note}
Ubuntu 24.04 LTS synchronizes time with `systemd-timesyncd`, which does not
support NTS. Starting with Ubuntu 25.10, new installations use `chrony` with
NTS. See {ref}`about-time-synchronisation`.
:::

On Ubuntu Desktop, further data flows cross the boundary: the display server
receives input events from keyboards and pointing devices, wireless stacks
communicate with access points and Bluetooth devices, and desktop applications
open untrusted documents and web content.

(security-architecture-layers)=
## Layered defense-in-depth architecture

Ubuntu protects the system with four layers of security mechanisms. Each layer
assumes that the layer above it can fail or be compromised, so an attacker
needs to defeat several independent mechanisms to compromise the system.

Many of these mechanisms are part of the upstream Linux kernel and userspace,
and are available on any Linux distribution. Ubuntu adds its own defaults and
integrations on top of them. In the diagram, light gray boxes show upstream
mechanisms, and black boxes show Ubuntu defaults.

```{mermaid}
:alt: Layered diagram with four stacked layers. Layer 1, network and perimeter: Netfilter and nftables, TCP SYN cookies, no open ports policy, ufw host firewall (opt-in), chrony with NTS, DNSSEC validation (opt-in). Layer 2, userspace: PAM and polkit, systemd service sandboxing, sudo-rs with the root account locked, APT signature verification and unattended security updates, AppArmor profiles for packaged software, snapd strict confinement, hardened compiler flags, auditd and USG hardening (opt-in). Layer 3, Linux kernel: DAC, ACLs and capabilities, namespaces and cgroups, seccomp-bpf, AppArmor enforced, Yama ptrace scope, unprivileged user namespace restriction, kernel memory hardening, lockdown and module signature enforcement (platform-dependent). Layer 4, hardware, firmware, and boot chain: UEFI Secure Boot chain (platform-dependent), TPM 2.0 measured boot (platform-dependent), IOMMU DMA protection (platform-dependent), fwupd firmware updates, LUKS full disk encryption (opt-in).
:caption: Layered security mechanisms in Ubuntu

%%{init: {"theme": "base", "themeVariables": {"fontFamily": "Ubuntu Sans, Ubuntu, sans-serif", "lineColor": "#E95420", "primaryColor": "#F3F3F3", "primaryBorderColor": "#000000", "primaryTextColor": "#000000", "clusterBkg": "#FFFFFF", "clusterBorder": "#000000", "titleColor": "#000000", "edgeLabelBackground": "#FFFFFF"}, "flowchart": {"curve": "linear"}}}%%
flowchart TB
    subgraph L1["1 — Network and perimeter"]
        nft["Netfilter and nftables<br>packet filtering"]
        syn["TCP SYN cookies"]
        ports["No open ports policy"]
        ufw["ufw host firewall rules<br>(opt-in)"]
        nts["chrony with NTS"]
        dnssec["DNSSEC validation<br>(opt-in)"]
        nft ~~~ ufw
        syn ~~~ nts
        ports ~~~ dnssec
    end

    subgraph L2["2 — Userspace: deb packages, systemd services, snaps"]
        pam["PAM and polkit"]
        sysd["systemd service sandboxing"]
        sudo["sudo-rs, root account locked"]
        apt["APT signature verification,<br>unattended security updates"]
        aaprof["AppArmor profiles for<br>packaged software"]
        snap["snapd strict confinement<br>(AppArmor, seccomp, device<br>cgroup, mount namespace)"]
        flags["Hardened compiler flags<br>(PIE, stack protector, FORTIFY)"]
        audit["auditd, USG hardening profiles<br>(opt-in)"]
        pam ~~~ apt
        sysd ~~~ aaprof
        sudo ~~~ snap
        flags ~~~ audit
    end

    subgraph L3["3 — Linux kernel"]
        dac["DAC, POSIX ACLs,<br>capabilities"]
        nscg["Namespaces, cgroups v2"]
        seccomp["seccomp-bpf"]
        aa["AppArmor LSM enforced"]
        yama["Yama ptrace scope"]
        userns["Unprivileged user<br>namespace restriction"]
        khard["Kernel memory hardening<br>(KASLR, kptr_restrict, RO/NX)"]
        lockdown["Lockdown, module signature<br>enforcement (platform-dependent)"]
        dac ~~~ aa
        nscg ~~~ yama
        seccomp ~~~ userns
        khard ~~~ lockdown
    end

    subgraph L4["4 — Hardware, firmware, and boot chain"]
        sb["UEFI Secure Boot: shim, GRUB,<br>kernel (platform-dependent)"]
        tpm["TPM 2.0 measured boot<br>(platform-dependent)"]
        iommu["IOMMU DMA protection<br>(platform-dependent)"]
        fwupd["fwupd firmware updates"]
        fde["LUKS full disk encryption<br>(opt-in)"]
        sb ~~~ fwupd
        tpm ~~~ fde
        tpm ~~~ iommu
    end

    L1 -->|"Accepted connections"| L2
    L2 -->|"System calls"| L3
    L3 -->|"Device, memory, and storage access"| L4

    classDef component fill:#F3F3F3,stroke:#000000,stroke-width:1px,color:#000000
    classDef ubuntu fill:#000000,stroke:#000000,stroke-width:1px,color:#FFFFFF
    classDef optin fill:#F3F3F3,stroke:#000000,stroke-width:1px,stroke-dasharray:4 4,color:#000000
    classDef platform fill:#000000,stroke:#666666,stroke-width:2px,stroke-dasharray:4 4,color:#FFFFFF
    class nft,syn,pam,sysd,dac,nscg,seccomp component
    class ports,nts,sudo,apt,aaprof,snap,flags,aa,yama,userns,khard,fwupd ubuntu
    class ufw,dnssec,audit,fde optin
    class lockdown,sb,tpm,iommu platform
    style L1 fill:#FFFFFF,stroke:#000000,stroke-width:2px
    style L2 fill:#FFFFFF,stroke:#000000,stroke-width:2px
    style L3 fill:#FFFFFF,stroke:#000000,stroke-width:2px
    style L4 fill:#FFFFFF,stroke:#000000,stroke-width:2px
```

The four layers are:

Network and perimeter
: Filters and authenticates traffic before it reaches a service. The kernel's
  Netfilter framework, configured through `nftables`, filters packets. Ubuntu
  installs {manpage}`ufw(8)` as a front end to Netfilter, but does not enable
  it. TCP SYN cookies, enabled by default, protect against SYN flood attacks.
  See {ref}`firewalls`.

Userspace
: Runs services and applications from `deb` packages and snaps. Ubuntu
  verifies every package that it installs from the archive or the Snap Store,
  and installs security updates automatically with `unattended-upgrades`.
  Ubuntu builds packages with hardened compiler and linker flags, and ships
  AppArmor profiles for many packaged services and applications. `snapd`
  confines each strictly confined snap with several kernel mechanisms at once.
  See {ref}`automatic-updates` and
  [snap confinement](https://documentation.ubuntu.com/security/security-features/privilege-restriction/snap-confinement/).

Linux kernel
: Enforces access control and isolation for every process. Upstream Linux
  provides discretionary access control (DAC), capabilities, namespaces,
  cgroups, and seccomp. Ubuntu enables AppArmor as its Linux Security Module
  (LSM), restricts `ptrace` with the Yama LSM, restricts unprivileged user
  namespaces through AppArmor, and configures the kernel to hide kernel
  addresses and randomize the kernel's location in memory. See
  [kernel protections](https://documentation.ubuntu.com/security/security-features/kernel-protections/).

Hardware, firmware, and boot chain
: Anchors trust in the hardware. When UEFI Secure Boot is enabled, the
  firmware verifies the boot loader, and the boot loader verifies the kernel. Ubuntu ships
  {manpage}`fwupdmgr(1)` to install signed firmware updates. Full disk
  encryption protects data at rest, if you enable it during installation.

(security-architecture-defaults)=
### Default and configurable protections

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
| Full disk encryption | Opt-in | Select encryption during installation. |
| DNSSEC validation | Opt-in | Enable validation in the resolver. See {ref}`install-dnssec`. |
| System auditing and compliance hardening | Opt-in | Install `auditd`, or apply a hardening profile with the [Ubuntu Security Guide (USG)](https://documentation.ubuntu.com/security/compliance/usg/). |

:::{note}
Ubuntu 24.04 LTS uses `sudo` instead of `sudo-rs` as the default `sudo`
provider. See {ref}`sudo-rs`.
:::
