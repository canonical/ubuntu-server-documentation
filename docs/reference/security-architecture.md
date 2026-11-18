---
myst:
  html_meta:
    description: "Reference for the security architecture of Ubuntu: trust boundaries, layered defenses, boot chain, and the default state of each security mechanism."
---

(security-architecture)=
# System architecture from a security perspective

This page describes the security architecture of Ubuntu as a general-purpose
operating system: the platform that Ubuntu Server and Ubuntu Desktop share,
with software delivered as `deb` packages and snaps. The same architecture
largely applies to other forms of Ubuntu that build on this platform, such as
cloud images, Ubuntu on WSL, and Ubuntu container images, although some of
them omit or delegate components, for example the boot chain. It identifies the trust
boundaries of an Ubuntu system, the mechanisms that protect each boundary, and
which of those mechanisms are active by default and which you need to enable.

Use this page to:

* understand where untrusted input enters a system and what mediates it
* decide which additional protections your deployment needs
* support security assessments, such as the technical documentation required
  by the EU Cyber Resilience Act (CRA)

(security-architecture-purpose)=
## Purpose and scope

This page explains how Ubuntu achieves a secure-by-default configuration,
protection against unauthorized access, a limited attack surface, and
mitigation of exploits. If you build a product on top of Ubuntu, this page
describes the architecture that your product inherits.

The architecture separates five zones:

* untrusted external entities, such as network peers and attached devices
* external infrastructure services that Ubuntu relies on, such as the Ubuntu
  archive and the Snap Store
* userspace workloads: services and applications from `deb` packages and snaps
* the Linux kernel, which enforces access control and isolation
* hardware, firmware, and the boot chain, which anchor trust in the system

The mechanisms on this page protect the system regardless of where its
software comes from: the kernel confines third-party services in the same way
as packages from the Ubuntu archive, and `snapd` confines third-party snaps in
the same way as any other snap. However, Canonical does not review, maintain,
or provide security updates for third-party software, so the protection that
such software itself provides is outside the scope of this page. Packages from
third-party APT repositories also run their installation scripts as root,
without any security boundary between them and the rest of the system. See
{ref}`third-party-repository-usage`.

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

---
config:
  theme: base
  fontFamily: Ubuntu variable, Ubuntu, sans-serif
  themeCSS: 'svg, svg * { font-family: Ubuntu variable, Ubuntu, sans-serif !important; }'
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
mechanisms, and black boxes show Ubuntu defaults. The layers are arranged
clockwise, starting with the network layer at the top left.

```{mermaid}
:alt: Layered diagram with four layers arranged clockwise from the top left. Layer 1, network and perimeter: Netfilter and nftables, TCP SYN cookies, no open ports policy, ufw host firewall (opt-in), chrony with NTS, DNSSEC validation (opt-in). Layer 2, userspace: PAM and polkit, systemd service sandboxing, sudo-rs with the root account locked, APT signature verification and unattended security updates, AppArmor profiles for packaged software, snapd strict confinement, hardened compiler flags, auditd and USG hardening (opt-in). Layer 3, Linux kernel: DAC, ACLs and capabilities, namespaces and cgroups, seccomp-bpf, AppArmor enforced, Yama ptrace scope, unprivileged user namespace restriction, kernel memory hardening, lockdown and module signature enforcement (platform-dependent). Layer 4, hardware, firmware, and boot chain: UEFI Secure Boot chain (platform-dependent), TPM 2.0 measured boot (platform-dependent), IOMMU DMA protection (platform-dependent), fwupd firmware updates, LUKS full disk encryption (opt-in).
:caption: Layered security mechanisms in Ubuntu

---
config:
  theme: base
  fontFamily: Ubuntu variable, Ubuntu, sans-serif
  themeCSS: 'svg, svg * { font-family: Ubuntu variable, Ubuntu, sans-serif !important; }'
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
    subgraph TOP[" "]
        direction LR
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
        subgraph L2["2 — Userspace"]
            pam["PAM and polkit"]
            sysd["systemd service sandboxing"]
            sudo["sudo-rs, root account locked"]
            apt["APT signature verification,<br>unattended security updates"]
            aaprof["AppArmor profiles for<br>packaged software"]
            snap["snapd strict confinement<br>(AppArmor, seccomp, device<br>cgroup, mount namespace)"]
            flags["Hardened compiler flags<br>(PIE, stack protector, FORTIFY)"]
            audit["auditd, USG hardening profiles<br>(opt-in)"]
            pam ~~~ apt ~~~ flags
            sysd ~~~ aaprof ~~~ audit
            sudo ~~~ snap
        end
        L1 -->|"Accepted connections"| L2
    end

    subgraph BOT[" "]
        direction RL
        subgraph L3["3 — Linux kernel"]
            dac["DAC, POSIX ACLs,<br>capabilities"]
            nscg["Namespaces, cgroups v2"]
            seccomp["seccomp-bpf"]
            aa["AppArmor LSM enforced"]
            yama["Yama ptrace scope"]
            userns["Unprivileged user<br>namespace restriction"]
            khard["Kernel memory hardening<br>(KASLR, kptr_restrict, RO/NX)"]
            lockdown["Lockdown, module signature<br>enforcement (platform-dependent)"]
            dac ~~~ aa ~~~ khard
            nscg ~~~ yama ~~~ lockdown
            seccomp ~~~ userns
        end
        subgraph L4["4 — Hardware and boot"]
            sb["UEFI Secure Boot: shim, GRUB,<br>kernel (platform-dependent)"]
            tpm["TPM 2.0 measured boot<br>(platform-dependent)"]
            iommu["IOMMU DMA protection<br>(platform-dependent)"]
            fwupd["fwupd firmware updates"]
            fde["LUKS full disk encryption<br>(opt-in)"]
            sb ~~~ fwupd
            tpm ~~~ fde
            iommu
        end
        L3 -->|"Device and storage access"| L4
    end

    TOP -->|"System calls"| BOT

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
    style TOP fill:none,stroke:none
    style BOT fill:none,stroke:none
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
| Full disk encryption | Opt-in | Select encryption during installation. To unlock with the TPM, use TPM-backed FDE on Ubuntu Desktop, or Clevis on Ubuntu Server. |
| DNSSEC validation | Opt-in | Enable validation in the resolver. See {ref}`install-dnssec`. |
| System auditing and compliance hardening | Opt-in | Install `auditd`, or apply a hardening profile with the [Ubuntu Security Guide (USG)](https://documentation.ubuntu.com/security/compliance/usg/). |

:::{note}
Ubuntu 24.04 LTS uses `sudo` instead of `sudo-rs` as the default `sudo`
provider. See {ref}`sudo-rs`.
:::

(security-architecture-upper-boundaries)=
## Network, userspace, and kernel boundaries

This section looks at the two upper boundaries in more detail: where network
input enters userspace, and where userspace processes request services from
the kernel. It shows how Ubuntu validates untrusted input and mediates
privilege transitions at each boundary.

```{mermaid}
:alt: Diagram of the network to userspace and userspace to kernel boundaries. Untrusted packets pass Netfilter in the kernel before reaching network-facing services, which run in a systemd service sandbox. Services pass credentials to PAM, optionally with multi-factor authentication. Unprivileged users and applications elevate privileges through sudo-rs, which uses PAM, or call privileged daemons over D-Bus, which check authorization with polkit. All userspace processes enter the kernel through the system call interface, where seccomp-bpf, DAC and capabilities, and the AppArmor and Yama LSM hooks check each request before the kernel accesses kernel objects, which namespaces and cgroups scope and limit. Policy for AppArmor, seccomp, and nftables is stored in userspace and loaded into the kernel.
:caption: Mediation at the network, userspace, and kernel boundaries

---
config:
  theme: base
  fontFamily: Ubuntu variable, Ubuntu, sans-serif
  themeCSS: 'svg, svg * { font-family: Ubuntu variable, Ubuntu, sans-serif !important; }'
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
    subgraph NETZ["Outside — untrusted network"]
        pkt["Remote clients and<br>untrusted peers"]
    end

    subgraph US["Userspace"]
        subgraph SANDBOX["systemd sandbox"]
            svc["Network-facing services<br>(OpenSSH, TLS servers)"]
        end
        user["Unprivileged user session<br>or application"]
        pam["PAM"]
        mfa["Multi-factor authentication<br>(opt-in)"]
        sudo["sudo-rs"]
        daemon["Privileged daemon"]
        polkit["polkit"]
        policy[("Security policy<br>(AppArmor profiles, seccomp<br>filters, nftables rules)")]
    end

    subgraph KZ["Linux kernel"]
        nf["Netfilter hooks,<br>TCP SYN cookies"]
        sys["System call entry<br>(argument and user<br>memory checks)"]
        seccomp["seccomp-bpf filter"]
        dac["DAC (UID, GID, POSIX ACLs)<br>and capabilities"]
        subgraph LSM["LSM hooks"]
            aa["AppArmor MAC<br>(files, sockets,<br>capabilities)"]
            yama["Yama ptrace scope"]
        end
        nscg["Namespaces and cgroups"]
        obj[("Kernel objects<br>(files, sockets,<br>processes, devices)")]
    end

    pkt -.->|"Untrusted packets"| nf
    nf -->|"Accepted connections"| svc
    svc -->|"Credentials"| pam
    pam -.->|"Second factor"| mfa
    user -->|"Elevation request"| sudo
    sudo -->|"Authentication"| pam
    user -->|"D-Bus call"| daemon
    daemon -->|"Authorization check"| polkit
    policy -->|"Profiles"| aa
    policy -->|"Filters"| seccomp
    policy -.->|"Rules (opt-in)"| nf
    US -->|"System calls"| sys
    sys --> seccomp
    seccomp -->|"Allowed calls"| dac
    dac -->|"Permitted access"| LSM
    LSM -->|"Mediated access"| obj
    nscg -->|"Scope and limit"| obj

    classDef untrusted fill:#FFFFFF,stroke:#000000,stroke-width:1px,stroke-dasharray:4 4,color:#000000
    classDef component fill:#F3F3F3,stroke:#000000,stroke-width:1px,color:#000000
    classDef ubuntu fill:#000000,stroke:#000000,stroke-width:1px,color:#FFFFFF
    classDef optin fill:#F3F3F3,stroke:#000000,stroke-width:1px,stroke-dasharray:4 4,color:#000000
    class pkt untrusted
    class svc,user,pam,daemon,polkit,policy,nf,sys,seccomp,dac,nscg,obj component
    class sudo,aa,yama ubuntu
    class mfa optin
    style NETZ fill:#FFFFFF,stroke:#000000,stroke-width:2px
    style US fill:#FFFFFF,stroke:#000000,stroke-width:2px
    style KZ fill:#FFFFFF,stroke:#000000,stroke-width:2px
    style SANDBOX fill:#FFFFFF,stroke:#000000,stroke-width:1px
    style LSM fill:#FFFFFF,stroke:#000000,stroke-width:1px
```

(security-architecture-network-boundary)=
### Network to userspace

Packet filtering
: Netfilter processes every packet in the kernel before a service receives
  it. Rules defined with {manpage}`nft(8)` or `ufw` can drop or limit traffic.
  TCP SYN cookies keep services reachable during SYN flood attacks. See
  [SYN cookies](https://documentation.ubuntu.com/security/security-features/network/syn-cookies/).

Encrypted and authenticated access
: OpenSSH and Transport Layer Security (TLS) libraries protect remote sessions
  and service traffic. Ubuntu configures these libraries to reject legacy
  protocol versions and weak algorithms. See
  {ref}`explanation-cryptography`.

Service sandboxing
: Network-facing services run as `systemd` units. The unit file can drop
  privileges and restrict the service, for example with a dedicated user,
  `NoNewPrivileges=`, `ProtectSystem=`, and system call filters. See
  {manpage}`systemd.exec(5)`.

(security-architecture-privilege-boundary)=
### Privilege elevation and authentication

PAM
: Login services, such as the console login, SSH, and the display manager,
  use {manpage}`pam(7)` to authenticate users, check account restrictions,
  and set up sessions. PAM modules add
  multi-factor authentication, smart cards, or network identity providers if
  you configure them. See {ref}`two-factor-authentication-with-totp-or-hotp`,
  {ref}`smart-card-authentication`, and the
  [authd documentation](https://documentation.ubuntu.com/authd/).

`sudo-rs`
: Lets authorized users run commands as root with their own credentials. The
  root account has no usable password by default. See {ref}`user-management`
  and {ref}`sudo-rs`.

polkit
: Lets privileged daemons decide whether an unprivileged caller may perform an
  action, such as mounting a disk or changing network settings. See
  {manpage}`polkit(8)`.

:::{note}
Ubuntu 24.04 LTS uses `sudo` instead of `sudo-rs` by default.
:::

(security-architecture-syscall-boundary)=
### Userspace to kernel

Every request from a userspace process to the kernel passes through the system
call interface. The kernel validates the arguments of each system call, and
copies data from and to process memory only through dedicated functions, such
as `copy_from_user()`, which check that the memory belongs to the calling
process. The kernel then applies the following checks:

seccomp-bpf
: Rejects system calls that the process's filter does not allow. `snapd`,
  `systemd`, and many applications install filters. See
  [seccomp filtering](https://documentation.ubuntu.com/security/security-features/privilege-restriction/#seccomp-filtering)
  and {manpage}`seccomp(2)`.

Discretionary access control and capabilities
: Checks the process's user and group IDs against file permissions and
  {manpage}`acl(5)` entries, and checks {manpage}`capabilities(7)` for
  privileged operations.

AppArmor
: Restricts each confined program to the files, network access, and
  capabilities listed in its profile, even if the program runs as root.
  AppArmor also restricts the use of unprivileged user namespaces. See
  {ref}`apparmor` and
  [AppArmor](https://documentation.ubuntu.com/security/security-features/privilege-restriction/apparmor/).

Yama
: Allows a process to attach to another process with `ptrace` only if it is
  an ancestor of that process, or has the required capability. See
  [`ptrace` scope](https://documentation.ubuntu.com/security/security-features/process-memory/#ptrace-scope).

Namespaces and cgroups
: Limit which resources a process can see, and how much of them it can use.
  Containers and snaps build on them. See {manpage}`namespaces(7)` and
  [cgroups](https://documentation.ubuntu.com/security/security-features/privilege-restriction/cgroups/).

Policies for these mechanisms, such as AppArmor profiles, seccomp filters, and
`nftables` rules, are written and managed in userspace. Once loaded, the kernel
enforces them, and a process cannot bypass them without the privileges to
replace the policy.

(security-architecture-lower-boundary)=
## Kernel, hardware, boot, and storage boundary

This section looks at the lower boundary: how Ubuntu establishes trust in the
code that runs at boot, how it protects data at rest, and how the running
kernel deals with hardware and firmware.

```{mermaid}
:alt: Diagram of the boot chain and the kernel to hardware boundary. UEFI firmware verifies shim, which is signed by the Microsoft UEFI CA. shim verifies GRUB, and GRUB verifies the Linux kernel through shim; both are signed by Canonical. GRUB loads the locally built initramfs, which is measured but not signed. The firmware and boot chain extend measurements into TPM 2.0 PCRs. The running kernel enforces lockdown and module signatures. An optional LUKS encrypted volume is unlocked with a passphrase, Clevis, or TPM-backed FDE, and dm-crypt holds the volume key in the kernel keyring. Peripherals and removable media are handled by kernel drivers and udev, and their DMA is restricted by the IOMMU. fwupd installs signed firmware from the LVFS.
:caption: Boot chain, data at rest, and the hardware boundary

---
config:
  theme: base
  fontFamily: Ubuntu variable, Ubuntu, sans-serif
  themeCSS: 'svg, svg * { font-family: Ubuntu variable, Ubuntu, sans-serif !important; }'
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
    subgraph OUTSIDE["Outside — untrusted"]
        dev["Peripherals and<br>removable media"]
    end

    subgraph EXTSVC["External services"]
        lvfs["LVFS<br>(firmware updates)"]
    end

    subgraph HW["Hardware and firmware"]
        uefi["UEFI firmware, Secure Boot<br>(platform-dependent)"]
        tpm["TPM 2.0 PCRs<br>(platform-dependent)"]
        iommu["IOMMU<br>(platform-dependent)"]
        fw["Device and system firmware"]
    end

    subgraph BOOT["Boot chain"]
        shim["shim<br>(signed by Microsoft UEFI CA)"]
        grub["GRUB<br>(signed by Canonical)"]
        kernel["Linux kernel<br>(signed by Canonical)"]
        initrd["initramfs<br>(built locally, not signed)"]
    end

    subgraph RUN["Running system"]
        lockdown["Lockdown, module signature<br>enforcement (platform-dependent)"]
        drivers["Kernel drivers and udev"]
        dmcrypt["dm-crypt"]
        keyring[("Kernel keyrings<br>(keyctl)")]
        fwupd["fwupd"]
    end

    subgraph UNLOCK["Disk unlock methods"]
        pass["Passphrase<br>(opt-in)"]
        clevis["Clevis TPM unlock<br>(opt-in)"]
        tpmfde["TPM-backed FDE<br>(opt-in, Desktop)"]
    end

    luks[("LUKS encrypted volume<br>(opt-in)")]

    uefi -->|"Verifies"| shim
    shim -->|"Verifies"| grub
    grub -->|"Verifies through shim"| kernel
    grub -->|"Loads"| initrd
    BOOT -->|"Measurements"| tpm
    kernel -->|"Enforces at runtime"| lockdown
    pass -.->|"Passphrase"| initrd
    tpm -.->|"Unseals key if<br>PCRs match"| clevis
    tpm -.->|"Unseals key if<br>PCRs match"| tpmfde
    clevis -.->|"Key"| initrd
    tpmfde -.->|"Key"| dmcrypt
    initrd -.->|"Volume key"| dmcrypt
    dmcrypt -.->|"Volume key"| keyring
    dmcrypt -.->|"Encrypted blocks"| luks
    dev -.->|"Device attach"| drivers
    dev -.->|"DMA requests"| iommu
    lvfs -->|"Signed firmware<br>and metadata"| fwupd
    fwupd -->|"Verified update"| fw

    classDef untrusted fill:#FFFFFF,stroke:#000000,stroke-width:1px,stroke-dasharray:4 4,color:#000000
    classDef external fill:#FFFFFF,stroke:#000000,stroke-width:1px,color:#000000
    classDef component fill:#F3F3F3,stroke:#000000,stroke-width:1px,color:#000000
    classDef ubuntu fill:#000000,stroke:#000000,stroke-width:1px,color:#FFFFFF
    classDef optin fill:#F3F3F3,stroke:#000000,stroke-width:1px,stroke-dasharray:4 4,color:#000000
    classDef platform fill:#000000,stroke:#666666,stroke-width:2px,stroke-dasharray:4 4,color:#FFFFFF
    class dev untrusted
    class lvfs external
    class fw,initrd,drivers,dmcrypt,keyring component
    class shim,grub,kernel,fwupd ubuntu
    class uefi,tpm,iommu,lockdown platform
    class pass,clevis,tpmfde,luks optin
    style OUTSIDE fill:#FFFFFF,stroke:#000000,stroke-width:2px
    style EXTSVC fill:#FFFFFF,stroke:#000000,stroke-width:2px
    style HW fill:#FFFFFF,stroke:#000000,stroke-width:2px
    style BOOT fill:#FFFFFF,stroke:#000000,stroke-width:2px
    style RUN fill:#FFFFFF,stroke:#000000,stroke-width:2px
    style UNLOCK fill:#FFFFFF,stroke:#000000,stroke-width:1px,stroke-dasharray:4 4
```

(security-architecture-boot)=
### Verified and measured boot

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
### Data at rest and key protection

Full disk encryption
: Both the Ubuntu Server and the Ubuntu Desktop installers can encrypt the
  disk with Linux Unified Key Setup (LUKS) and `dm-crypt`, for example by
  encrypting the Logical Volume Manager (LVM) volume group. By default, you
  unlock the disk at boot with a passphrase. See
  [full disk encryption](https://documentation.ubuntu.com/security/security-features/storage/encryption-full-disk/)
  and [encrypted LVM](https://documentation.ubuntu.com/security/security-features/storage/encrypted-lvm/).

TPM-backed unlocking
: On supported hardware, which provides UEFI Secure Boot, a TPM 2.0, and an
  IOMMU, the Ubuntu Desktop installer offers TPM-backed full disk encryption.
  The kernel and `initramfs` are then delivered as a single signed image, so
  that Secure Boot verifies both, and the TPM releases the disk key only if
  the measured boot state matches the expected state. On Ubuntu Server, and
  on any existing LUKS installation, you can bind the encrypted volume to the
  TPM with Clevis to unlock it without a passphrase, which suits unattended
  systems. See {ref}`tpm-backed-luks-decryption-with-clevis`.

Kernel keyrings
: Hold keys, such as disk encryption keys and authentication tokens, in
  kernel memory with per-key access control. Processes access them with
  {manpage}`keyctl(1)`. See {manpage}`keyrings(7)`.

:::{note}
In Ubuntu 24.04 LTS, TPM-backed FDE in the Desktop installer is an
experimental feature.
:::

(security-architecture-hardware-boundary)=
### Runtime hardware and firmware boundary

Kernel modules
: With Secure Boot enabled, the kernel only loads modules signed by
  Canonical or with an enrolled MOK. When you install a third-party driver
  with DKMS, Ubuntu signs the module with a MOK, which you enroll at the next
  boot.

Devices and removable media
: The kernel drivers and {manpage}`udev(7)` handle every new device. Data on
  removable media is untrusted input. To control which USB devices the system
  accepts, you can install {manpage}`usbguard-daemon(8)`. See
  [devices](https://documentation.ubuntu.com/security/security-features/platform-protections/devices/).

DMA protection
: An Input-Output Memory Management Unit (IOMMU) restricts which memory a
  device can access through direct memory access (DMA). This protects against
  malicious peripherals, such as Thunderbolt devices. The protection depends
  on hardware support and firmware settings.

Firmware updates
: `fwupd` downloads firmware from the LVFS, verifies the signed metadata, and
  installs the update through the device's or system's update mechanism.

(security-architecture-controls)=
## Security controls reference

The following table lists the security mechanisms on this page by boundary,
with their default state in Ubuntu 26.04 LTS. The default state is one of:

* **Enabled by default**: active on a new installation
* **Opt-in**: you need to choose and enable the mechanism
* **Platform-dependent**: active by default if the hardware or firmware
  supports and enables it

| Boundary | Mechanism | Purpose and function | Default state | Details |
|---|---|---|---|---|
| {ref}`Network to userspace <security-architecture-network-boundary>` | Host firewall (Netfilter, `nftables`, `ufw`) | Blocks or limits network traffic to and from the system before it reaches a service. | Opt-in | {ref}`firewalls`, [firewall](https://documentation.ubuntu.com/security/security-features/network/firewall/) |
| {ref}`Network to userspace <security-architecture-network-boundary>` | No open ports policy | Keeps a new installation free of listening network services, with few documented exceptions. | Enabled by default | [No open ports](https://documentation.ubuntu.com/security/security-features/network/open-ports/) |
| {ref}`Network to userspace <security-architecture-network-boundary>` | TCP SYN cookies | Keeps TCP services reachable during SYN flood attacks. | Enabled by default | [SYN cookies](https://documentation.ubuntu.com/security/security-features/network/syn-cookies/) |
| {ref}`Network to userspace <security-architecture-network-boundary>` | Encrypted and authenticated communications | Protects remote sessions and service traffic with SSH and TLS, using modern protocol versions and algorithms. | Enabled by default | {ref}`openssh-server`, {ref}`explanation-cryptography` |
| {ref}`Network to userspace <security-architecture-network-boundary>` | Service sandboxing (`systemd`) | Drops privileges and restricts filesystem, device, and kernel access for services whose unit file configures it. | Enabled by default | {manpage}`systemd.exec(5)` |
| {ref}`Outbound <security-architecture-context>` | Authenticated time synchronization (NTS) | Prevents attackers on the network from changing the system time. | Enabled by default | {ref}`about-time-synchronisation` |
| {ref}`Outbound <security-architecture-context>` | DNSSEC validation | Rejects forged DNS answers for signed domains. | Opt-in | {ref}`dnssec`, {ref}`install-dnssec` |
| {ref}`Outbound <security-architecture-context>` | Entropy seeding (Pollinate) | On Ubuntu Server and cloud images, seeds the random number generator from Ubuntu's entropy service on first boot. Removal from the default installation is proposed in {lpbug}`2158262`. | Enabled by default | [Cloud PRNG seed](https://documentation.ubuntu.com/security/security-features/cryptography/cloud-prng-seed/), [Pollinate analysis](https://discourse.ubuntu.com/t/ubuntu-server-gazette-issue-16-does-pollinate-still-earn-its-place-on-every-ubuntu-boot-in-2026/84735/1) |
| {ref}`Outbound <security-architecture-context>` | System telemetry (Ubuntu Desktop) | Shares non-identifying system information with Canonical only after you consent, and keeps a local copy of each report for inspection. | Opt-in | [Product data collection notice](https://canonical.com/legal/systems-information-notice), [Ubuntu Insights](https://discourse.ubuntu.com/t/ubuntu-insights-how-telemetry-is-changing-on-ubuntu-desktop/73442) |
| {ref}`Privilege elevation <security-architecture-privilege-boundary>` | Authentication (PAM) | Verifies user identity for all login paths, with optional multi-factor authentication, smart cards, or network identity providers. | Enabled by default | {ref}`explanation-security`, {ref}`smart-card-authentication`, [authd](https://documentation.ubuntu.com/authd/) |
| {ref}`Privilege elevation <security-architecture-privilege-boundary>` | Locked root account | Prevents direct logins as root, so that administrative actions are tied to a user account. | Enabled by default | {ref}`user-management` |
| {ref}`Privilege elevation <security-architecture-privilege-boundary>` | `sudo-rs` and polkit | Lets authorized users run administrative tasks with their own credentials, and lets privileged daemons authorize unprivileged callers. | Enabled by default | {ref}`sudo-rs`, {manpage}`polkit(8)` |
| {ref}`Userspace to kernel <security-architecture-syscall-boundary>` | File permissions and ACLs | Restricts access to files and devices based on owner, group, and access control lists. | Enabled by default | [File handling](https://documentation.ubuntu.com/security/security-features/process-memory/file-handling/), {manpage}`acl(5)` |
| {ref}`Userspace to kernel <security-architecture-syscall-boundary>` | Capabilities | Splits root privileges into separate units, so that a process holds only the privileges it needs. | Enabled by default | [Filesystem capabilities](https://documentation.ubuntu.com/security/security-features/privilege-restriction/#filesystem-capabilities), {manpage}`capabilities(7)` |
| {ref}`Userspace to kernel <security-architecture-syscall-boundary>` | seccomp-bpf | Limits the system calls that a process can make. | Enabled by default | [Seccomp filtering](https://documentation.ubuntu.com/security/security-features/privilege-restriction/#seccomp-filtering) |
| {ref}`Userspace to kernel <security-architecture-syscall-boundary>` | AppArmor | Confines programs to the resources listed in their profile, even when they run as root, and restricts unprivileged user namespaces. | Enabled by default | {ref}`apparmor`, [AppArmor](https://documentation.ubuntu.com/security/security-features/privilege-restriction/apparmor/) |
| {ref}`Userspace to kernel <security-architecture-syscall-boundary>` | Yama `ptrace` scope | Prevents a process from inspecting or modifying the memory of processes other than its descendants. | Enabled by default | [`ptrace` scope](https://documentation.ubuntu.com/security/security-features/process-memory/#ptrace-scope) |
| {ref}`Userspace to kernel <security-architecture-syscall-boundary>` | Namespaces and cgroups | Isolate processes from each other and limit their resource use. | Enabled by default | [cgroups](https://documentation.ubuntu.com/security/security-features/privilege-restriction/cgroups/), {manpage}`namespaces(7)` |
| {ref}`Userspace to kernel <security-architecture-syscall-boundary>` | Snap confinement | Combines AppArmor, seccomp, device cgroups, and mount namespaces to isolate each strictly confined snap. | Enabled by default | [Snap confinement](https://documentation.ubuntu.com/security/security-features/privilege-restriction/snap-confinement/) |
| {ref}`Userspace to kernel <security-architecture-syscall-boundary>` | Kernel memory hardening | Makes kernel exploits harder by hiding kernel addresses, randomizing the kernel location, and write-protecting kernel code and data. | Enabled by default | [Kernel protections](https://documentation.ubuntu.com/security/security-features/kernel-protections/) |
| {ref}`Userspace to kernel <security-architecture-syscall-boundary>` | Process memory protections | Makes exploits of applications harder with hardened compiler flags and address space layout randomization (ASLR). | Enabled by default | [Compiler flags](https://documentation.ubuntu.com/security/security-features/process-memory/compiler-flags/), [ASLR](https://documentation.ubuntu.com/security/security-features/process-memory/aslr/) |
| {ref}`Kernel to hardware <security-architecture-lower-boundary>` | UEFI Secure Boot | Verifies the signatures of the boot loader and kernel before running them. | Platform-dependent | [UEFI Secure Boot](https://documentation.ubuntu.com/security/security-features/platform-protections/secure-boot/) |
| {ref}`Kernel to hardware <security-architecture-lower-boundary>` | Kernel lockdown and module signatures | Prevents root from modifying the running kernel, and rejects unsigned kernel modules. | Platform-dependent | [Kernel lockdown](https://documentation.ubuntu.com/security/security-features/kernel-protections/#kernel-lockdown) |
| {ref}`Kernel to hardware <security-architecture-lower-boundary>` | TPM measured boot | Records each boot stage in the TPM, so that secrets are only released to an unmodified system. | Platform-dependent | [Trusted Platform Module](https://documentation.ubuntu.com/security/security-features/platform-protections/trusted-platform-module/) |
| {ref}`Kernel to hardware <security-architecture-lower-boundary>` | Full disk encryption | Protects data at rest if a disk is lost or stolen. | Opt-in | [Full disk encryption](https://documentation.ubuntu.com/security/security-features/storage/encryption-full-disk/), {ref}`tpm-backed-luks-decryption-with-clevis` |
| {ref}`Kernel to hardware <security-architecture-lower-boundary>` | Kernel keyrings | Hold keys in kernel memory with per-key access control. | Enabled by default | {manpage}`keyrings(7)`, [kernel key retention service](https://docs.kernel.org/security/keys/core.html) |
| {ref}`Kernel to hardware <security-architecture-lower-boundary>` | IOMMU DMA protection | Restricts the memory that devices can access through DMA. | Platform-dependent | [Devices](https://documentation.ubuntu.com/security/security-features/platform-protections/devices/), [x86 IOMMU support](https://docs.kernel.org/arch/x86/iommu.html) |
| {ref}`Kernel to hardware <security-architecture-lower-boundary>` | USB device authorization (`usbguard`) | Blocks USB devices that are not on an allow list. | Opt-in | [`usbguard`](https://documentation.ubuntu.com/security/security-features/platform-protections/devices/#usbguard) |
| {ref}`Kernel to hardware <security-architecture-lower-boundary>` | Memory encryption (AMD SEV, Intel TDX) | Encrypts the memory of virtual machines, to protect it from the host. | Platform-dependent | [CPU features](https://documentation.ubuntu.com/security/security-features/platform-protections/cpu/) |
| {ref}`Kernel to hardware <security-architecture-lower-boundary>` | Firmware updates (`fwupd`) | Installs signed firmware updates from the LVFS. | Enabled by default | {manpage}`fwupdmgr(1)` |
| {ref}`Kernel to hardware <security-architecture-lower-boundary>` | Physical access control | Restricts physical and console access to the system. | Opt-in | {ref}`console-security` |
| {ref}`Whole system <security-architecture-layers>` | Signed packages and images | Verifies the integrity of packages, snaps, and installation images, independently of the download source. | Enabled by default | [Archive verification](https://documentation.ubuntu.com/security/software-integrity/archive-verification/), [image verification](https://documentation.ubuntu.com/security/software-integrity/image-verification/) |
| {ref}`Whole system <security-architecture-layers>` | Security updates | Installs security updates automatically, and keeps the system on a supported release. | Enabled by default | {ref}`automatic-updates`, {ref}`upgrade-your-release`, [security updates](https://documentation.ubuntu.com/security/security-updates/) |
| {ref}`Whole system <security-architecture-layers>` | Monitoring and alerting | Collects metrics and logs, and alerts operators to unexpected behavior. | Opt-in | {ref}`how-to-observability`, {ref}`set-up-your-lma-stack`, [Landscape](https://ubuntu.com/landscape/docs/) |
| {ref}`Whole system <security-architecture-layers>` | Auditing and compliance hardening | Records security-relevant events, and applies and audits hardening profiles such as CIS Benchmarks. | Opt-in | {manpage}`auditd(8)`, [Ubuntu Security Guide](https://documentation.ubuntu.com/security/compliance/usg/) |

(security-architecture-further-reading)=
## Further reading

* [Ubuntu security documentation](https://documentation.ubuntu.com/security/)
* [Overview of security features by release](https://documentation.ubuntu.com/security/security-features/security-features-overview/)
