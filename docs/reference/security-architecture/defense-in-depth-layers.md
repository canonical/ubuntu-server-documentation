---
myst:
  html_meta:
    description: "The four layers of security mechanisms in Ubuntu, from the network to the hardware, and which of them are enabled by default."
---

(layered-defense-in-depth-architecture)=
# Layered defense-in-depth architecture

Ubuntu protects the system with four layers of security mechanisms. Each layer
assumes that the layer above it can fail or be compromised, so an attacker
needs to defeat several independent mechanisms to compromise the system.

The diagram on this page follows the
{ref}`diagram conventions <security-architecture-legend>`. To go to the
description of a layer, select the layer in the diagram.

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

Many of these mechanisms are part of the upstream Linux kernel and userspace,
and are available on any Linux distribution. Ubuntu adds its own defaults and
integrations on top of them. Each mechanism below states its default state as
one of the following:

* **Ubuntu default**: Ubuntu enables or configures the mechanism, beyond what
  upstream Linux does
* **Upstream, enabled by default**: an upstream Linux mechanism that is active
  on a new installation of Ubuntu
* **Opt-in**: Ubuntu provides the mechanism, but you need to choose and enable
  it
* **Platform-dependent**: Ubuntu can use the mechanism when the
  hardware or firmware supports and enables it.

(security-architecture-layer-network)=
## Network and perimeter

The network layer filters and authenticates traffic before it reaches a
service, and authenticates the network services that the system itself relies
on.

(security-architecture-netfilter)=
### Netfilter and `nftables`

**Default state:** Upstream, enabled by default, with no filtering rules

Netfilter is the packet filtering framework of the Linux kernel. Every packet
that the system receives, sends, or forwards passes its hooks, where rules can
accept, drop, or rate-limit it. You manage the rules with {manpage}`nft(8)`.
Without rules, Netfilter accepts all traffic, so the
{ref}`no open ports policy <security-architecture-no-open-ports>` is what
limits exposure on a new installation. See
{ref}`security-architecture-packet-filtering`.

(security-architecture-syn-cookies)=
### TCP SYN cookies

**Default state:** Upstream, enabled by default

In a SYN flood attack, an attacker opens many half-completed TCP connections
to exhaust the connection queue of a service. With SYN cookies, the kernel
encodes the connection state in its reply instead of storing it, so legitimate
clients can still connect while the queue is full. Ubuntu has set
`net.ipv4.tcp_syncookies` to `1` since Ubuntu 9.04. See
[SYN cookies](https://documentation.ubuntu.com/security/security-features/network/syn-cookies/).

(security-architecture-no-open-ports)=
### No open ports policy

**Default state:** Ubuntu default

A new installation of Ubuntu has no listening network services, with a small
number of documented exceptions that must follow strict guidelines, such as
not exposing application data to the network. A service only listens on the
network after you install it, which keeps the attack surface of a new system
small. To list the services that listen on your system, use {manpage}`ss(8)`.
See
[no open ports](https://documentation.ubuntu.com/security/security-features/network/open-ports/).

(security-architecture-ufw)=
### `ufw` host firewall

**Default state:** Opt-in

Ubuntu installs {manpage}`ufw(8)`, the Uncomplicated Firewall, as a front end
that writes Netfilter rules from short commands, but does not enable it. To
restrict which traffic reaches the services that you install, enable `ufw` and
add rules for those services, or write `nftables` rules directly. See
{ref}`firewalls` and
[netfilter subsystem](https://documentation.ubuntu.com/security/security-features/network/firewall/).

(security-architecture-nts)=
### Authenticated time synchronization

**Default state:** Ubuntu default

Correct time is a security property: certificate validity, Kerberos tickets,
and log timestamps all depend on it. Ubuntu synchronizes time with `chrony`,
configured to use Ubuntu's time servers with Network Time Security (NTS), which
authenticates the time servers so that an attacker on the network cannot
change the system time. See {ref}`about-time-synchronisation` and
{ref}`security-architecture-infrastructure-services`.

:::{note}
Ubuntu 24.04 LTS synchronizes time with `systemd-timesyncd`, which does not
support NTS. New installations use `chrony` with NTS starting with Ubuntu
25.10.
:::

(security-architecture-dnssec-validation)=
### DNSSEC validation

**Default state:** Opt-in

DNS Security Extensions (DNSSEC) let a resolver verify that DNS answers for a
signed domain come from the domain owner and were not modified. Ubuntu's stub
resolver, `systemd-resolved`, supports DNSSEC validation but ships with it
disabled, because validation can affect name resolution in some environments,
for example with DNS servers that do not fully follow the specification. For
background, see
[testing the waters with DNSSEC](https://discourse.ubuntu.com/t/ubuntu-server-gazette-issue-9-testing-the-waters-with-dnssec/72073).
To reject forged answers for signed domains, enable validation in the
resolver. See {ref}`dnssec` and {ref}`install-dnssec`.

Connections that pass the network layer reach a service that listens in
userspace. Only services that you install listen on the network, and each
service authenticates its clients and validates their input itself, as
OpenSSH does. See {ref}`security-architecture-network-boundary`.

(security-architecture-layer-userspace)=
## Userspace

Userspace runs services and applications from `deb` packages and snaps. The
mechanisms in this layer control which software is installed, how it was
built, what it can access, and who can act with administrative privileges.

(security-architecture-pam-polkit)=
### PAM and polkit

**Default state:** Upstream, enabled by default

Pluggable Authentication Modules (PAM) authenticate users for every login
service, and polkit lets privileged daemons decide whether an unprivileged
caller may perform an action. Both are upstream components that Ubuntu
configures for its login services and desktop. See
{ref}`security-architecture-pam` and {ref}`security-architecture-polkit`.

(security-architecture-systemd-sandboxing)=
### `systemd` service sandboxing

**Default state:** Upstream, enabled by default for services whose unit file
configures it

`systemd` can start each service with a dedicated user, without the ability to
gain privileges, and with restricted access to the file system, devices, and
kernel interfaces. Which restrictions apply depends on the unit file of each
service. To check a service, run `systemd-analyze security <unit>`. See
{ref}`security-architecture-service-sandboxing`.

(security-architecture-sudo-root)=
### `sudo-rs` and the locked root account

**Default state:** Ubuntu default

The root account of a new installation has no usable password, so nobody can
log in as root directly. Administrators run commands as root through
`sudo-rs`, a memory-safe implementation of `sudo`, using their own
credentials, so that administrative actions are tied to a user account. Grant
administrative rights only to users who need them. See and {ref}`user-management`.

:::{note}
Ubuntu 24.04 LTS uses `sudo` instead of `sudo-rs` as the default `sudo`
provider. See the sudo-rs {ref}`replacement <sudo-rs>` and [announcement](https://discourse.ubuntu.com/t/sudo-rs-is-now-default-for-questing-quokka/66497) pages.
:::

(security-architecture-apt-updates)=
### Package signature verification and automatic security updates

**Default state:** Ubuntu default

APT verifies every package that it installs from a configured repository
against signed repository metadata, and `snapd` verifies every snap against
signed assertions. Ubuntu also installs and enables `unattended-upgrades`,
which installs security updates automatically. Only add package sources that
you trust, because packages run their installation scripts as root. Plan your scheduled
reboots, because kernel updates take effect after a reboot. See
{ref}`automatic-updates`, {ref}`third-party-repository-usage`, and
{ref}`security-architecture-archive`.

(security-architecture-apparmor-profiles)=
### AppArmor profiles for packaged software

**Default state:** Ubuntu default

Ubuntu enforces AppArmor, and ships AppArmor profiles for many services and
applications in the archive, to confine them even when they run as root.
Each release adds more profiles. Do not disable AppArmor, and write profiles
for the services that you add yourself. See {ref}`apparmor`,
[disabling AppArmor](https://documentation.ubuntu.com/security/common-mistakes/disabling-apparmor/),
and {ref}`security-architecture-apparmor`.

(security-architecture-snap-confinement)=
### Snap strict confinement

**Default state:** Ubuntu default

`snapd` runs each strictly confined snap with its own AppArmor profile,
seccomp filter, device cgroup, and mount namespace, so that the snap can only
access the resources that its connected interfaces allow. Review the
interfaces that a snap requests, and avoid `classic` or `devmode` confinement
for snaps that you do not trust, because they turn off this confinement. See
[snap confinement](https://documentation.ubuntu.com/security/security-features/privilege-restriction/snap-confinement/)
and {ref}`security-architecture-snap-store`.

(security-architecture-compiler-flags)=
### Hardened compiler and linker flags

**Default state:** Ubuntu default

Ubuntu builds the packages in its archive as position-independent executables
(PIE), which take full advantage of address space layout randomization, with
stack protection, and with checks of buffer sizes in common C library
functions (`_FORTIFY_SOURCE`). These make memory corruption bugs harder to
exploit. Ubuntu configures its compiler to enable many of these flags by
default, so they also apply to software that you build on Ubuntu. See
[default compiler and linker flags](https://documentation.ubuntu.com/security/security-features/process-memory/compiler-flags/).

(security-architecture-auditing)=
### Auditing and compliance hardening

**Default state:** Opt-in

Ubuntu does not record security-relevant events, such as file access or
privilege changes, unless you install the {manpage}`auditd(8)` audit daemon.
To apply and audit a hardening profile, such as the CIS Benchmarks or
DISA-STIG, use the
[Ubuntu Security Guide (USG)](https://documentation.ubuntu.com/security/compliance/usg/),
which is available with an Ubuntu Pro subscription.

Userspace processes cannot access files, devices, the network, or other
processes directly. To do so, they make a system call: a request that switches
the CPU from user mode to the kernel at a fixed entry point. The kernel then
checks the request against the credentials of the process and the loaded
security policies before it acts on it. See
{ref}`security-architecture-syscall-boundary`.

(security-architecture-layer-kernel)=
## Linux kernel

The kernel enforces access control and isolation for every process, and
protects itself against exploitation.

(security-architecture-dac-capabilities)=
### Discretionary access control and capabilities

**Default state:** Upstream, enabled by default

The kernel checks every access attempt against the owner, group, and permissions of
the file or device, and its access control lists. Capabilities split the
privileges of root into separate units, so that a process can hold only the
privileges that it needs. See {ref}`security-architecture-dac`.

(security-architecture-namespaces-cgroups)=
### Namespaces and cgroups

**Default state:** Upstream, enabled by default

Namespaces limit which resources a process can see, such as other processes,
mounts, and network interfaces, and cgroups limit how much CPU, memory, and
I/O the process can use. Containers, snaps, and `systemd` services build on them. See
{ref}`security-architecture-namespaces`.

(security-architecture-seccomp-filtering)=
### seccomp-bpf

**Default state:** Upstream, enabled by default for processes that install a
filter

A seccomp filter limits which system calls a process can make, which reduces
the kernel attack surface that a compromised process can reach. `snapd`,
`systemd`, container runtimes, and many applications install filters. See
{ref}`security-architecture-seccomp`.

(security-architecture-apparmor-lsm)=
### AppArmor

**Default state:** Ubuntu default

Ubuntu enables AppArmor as its Linux Security Module (LSM). AppArmor enforces
mandatory access control: it restricts each confined program to the files,
network access, and capabilities listed in its profile, regardless of the
permissions of the user that runs it. See {ref}`security-architecture-apparmor`.

(security-architecture-yama-ptrace)=
### Yama `ptrace` scope

**Default state:** Ubuntu default

Normally a process can inspect and modify the memory of any other process
of the same user with `ptrace`, so one compromised application could read the
secrets of all others. Ubuntu enables the Yama LSM and limits `ptrace` to a
process's own descendants. See {ref}`security-architecture-yama`.

(security-architecture-userns-restriction)=
### Unprivileged user namespace restriction

**Default state:** Ubuntu default

Unprivileged user namespaces let a process gain capabilities inside a
namespace, which exposes kernel code that otherwise only root can reach.
Starting with Ubuntu 24.04 LTS, the kernel and AppArmor restrict them:
unconfined, unprivileged applications can still create user namespaces, but
cannot use capabilities inside them. AppArmor profiles allow full use for
applications that need it, such as browsers and container tools. See
[AppArmor unprivileged user namespace restrictions](https://documentation.ubuntu.com/security/security-features/privilege-restriction/apparmor/#apparmor-unprivileged-user-namespace-restrictions).

(security-architecture-kernel-hardening)=
### Kernel memory hardening

**Default state:** Ubuntu default

Ubuntu configures its kernel to make kernel exploits harder. Kernel address
space layout randomization (KASLR) places the kernel at a different address on
every boot, `kernel.kptr_restrict` and `kernel.dmesg_restrict` hide kernel
addresses and messages from unprivileged users, and kernel code and read-only
data are write-protected. Avoid weakening these protections with sysctl
settings. See
[kernel protections](https://documentation.ubuntu.com/security/security-features/kernel-protections/)
and
[dangerous sysctls](https://documentation.ubuntu.com/security/common-mistakes/dangerous-sysctls/).

(security-architecture-lockdown)=
### Kernel lockdown and module signatures

**Default state:** Platform-dependent

When UEFI Secure Boot is enabled, the kernel enables lockdown in integrity
mode, which prevents even root from modifying the running kernel, and only
loads signed kernel modules. This extends the verified boot chain into the
running system. See [Kernel protections](https://documentation.ubuntu.com/security/security-features/kernel-protections/#kernel-protections),
[kernel lockdown](https://documentation.ubuntu.com/security/security-features/kernel-protections/#kernel-lockdown) and {ref}`module-signature-check`).

Only the kernel accesses the hardware: it drives devices, manages memory, and
reads and writes storage on behalf of processes. In the other direction,
devices signal the kernel through interrupts, and can read and write memory
directly through direct memory access (DMA), which the IOMMU restricts. Which
kernel runs at all is decided earlier, by the boot chain. See
{ref}`kernel-hardware-boundary`.

(security-architecture-layer-hardware)=
## Hardware, firmware, and boot chain

The lowest layer anchors trust in the hardware: it decides which code runs at
boot, protects data at rest, and keeps firmware up to date.

(security-architecture-secure-boot)=
### UEFI Secure Boot

**Default state:** Platform-dependent

When Secure Boot is enabled in the firmware, the firmware verifies the boot
loader, and the boot loader verifies the kernel, so that only signed code runs
at boot. Ubuntu ships a signed boot chain, so Secure Boot works without
changes. Enable Secure Boot in the firmware of your system. See
{ref}`security-architecture-boot`.

(security-architecture-measured-boot)=
### TPM measured boot

**Default state:** Platform-dependent

If the system has a Trusted Platform Module (TPM) 2.0, the firmware records a
measurement of each boot stage in the TPM. The TPM can then release secrets,
such as a disk encryption key, only to a system that booted the expected
software. See {ref}`security-architecture-boot`.

(security-architecture-iommu)=
### IOMMU DMA protection

**Default state:** Platform-dependent

An Input-Output Memory Management Unit (IOMMU) restricts which memory a device
can access through DMA, which protects against malicious peripherals. Use
hardware that provides an IOMMU, and enable it in the firmware. See
{ref}`security-architecture-dma`.

(security-architecture-fwupd)=
### Firmware updates

**Default state:** Ubuntu default

Ubuntu ships `fwupd`, which downloads firmware updates from the Linux Vendor
Firmware Service (LVFS), verifies their signatures, and installs them. Firmware
vulnerabilities can undermine every layer above, so keep firmware up to date
with {manpage}`fwupdmgr(1)`. See {ref}`security-architecture-firmware-updates`.

(security-architecture-fde)=
### Full disk encryption

**Default state:** Opt-in

Full disk encryption with LUKS protects data at rest if a disk is lost or
stolen. Select encryption during installation. To unlock the disk with the
TPM instead of a passphrase, use TPM-backed full disk encryption on Ubuntu
Desktop, or Clevis on Ubuntu Server. See
{ref}`security-architecture-full-disk-encryption` and
{ref}`security-architecture-tpm-unlock`.
