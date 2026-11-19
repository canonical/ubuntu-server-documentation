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
mitigation of exploits. If you build a product with digital elements or a
solution with Ubuntu, or derive a flavor from it, this page describes the
security architecture that you build on and inherit.

The architecture separates five zones:

* untrusted external entities, such as network peers and attached devices
* external infrastructure services that Ubuntu relies on, such as the Ubuntu
  archive and the Snap Store
* userspace workloads: services and applications from `deb` packages and snaps
* the Linux kernel, which enforces access control and isolation
* hardware, firmware, and the boot chain, which anchor trust in the system

The mechanisms in this reference protect the system regardless of where its
software comes from: the kernel confines third-party services in the same way
as packages from the Ubuntu archive, and `snapd` confines third-party snaps in
the same way as any other snap. However, Canonical does not review, maintain,
or provide security updates for third-party software, so the protection that
such software itself provides is outside the scope of this reference. Packages from
third-party APT repositories also run their installation scripts as root,
without any security boundary between them and the rest of the system. See
{ref}`third-party-repository-usage`.

Canonical maintains a detailed threat model for the Ubuntu platform, which
lists the assets of the system, the data flows between them, and the controls
that mitigate threats to them. This page is a high-level view derived from
that threat model. It groups those assets, data flows, and controls by trust
boundary, so that you can see how they relate to one another.

This reference describes Ubuntu 26.04 LTS. Notes highlight where Ubuntu 24.04 LTS
differs. Ubuntu Core uses a different, all-snap architecture and is not
covered here. Components that only exist on Ubuntu Desktop, such as the display
server and desktop portals, are mentioned only where they change a trust
boundary.

(security-architecture-views)=
## Architecture views

The architecture is described in four views, from the outside of the system
to the hardware. Each view has its own page with diagrams.

{ref}`system-context`
: Trust boundaries between an Ubuntu system, untrusted entities, and the external infrastructure services that Ubuntu relies on.

{ref}`defense-in-depth-layers`
: The four layers of security mechanisms in Ubuntu, from the network to the hardware, and which of them are enabled by default.

{ref}`network-userspace-kernel-boundaries`
: How Ubuntu mediates network input, privilege elevation, and system calls at the network, userspace, and kernel boundaries.

{ref}`kernel-hardware-boundary`
: How Ubuntu verifies the boot chain, protects data at rest, and controls devices, kernel modules, and firmware.

```{toctree}
:hidden:

security-architecture/system-context
security-architecture/defense-in-depth-layers
security-architecture/network-userspace-kernel-boundaries
security-architecture/kernel-hardware-boundary
```

(security-architecture-controls)=
## Security controls reference

The following table lists the security mechanisms in this reference by boundary,
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

(security-architecture-legend)=
## Diagram conventions

The diagrams in this reference use the following conventions. Each diagram shows a
legend with the conventions that it uses. Every label that describes a
non-default state also carries a text tag, so the meaning does not depend on
color or line style alone.

| Element | Appearance | Meaning |
|---|---|---|
| Trust zone | Box with a thick black border | A region with a common trust level, for example `Outside — untrusted` |
| Untrusted actor | White box, dashed border | An entity outside the system that you cannot trust |
| External service | White box, solid border | Infrastructure outside the system that Ubuntu relies on |
| Component, layer, or upstream mechanism | Light gray box, solid border | A component or layer of the system, or a mechanism provided by the upstream Linux kernel or userspace |
| Ubuntu default | Black box, white text | A mechanism that Ubuntu enables or configures by default |
| Opt-in | Light gray box, dashed border, tagged `(opt-in)` | A mechanism that you need to choose and enable |
| Platform-dependent | Black box, dashed border, tagged `(platform-dependent)` | A mechanism that Ubuntu uses by default when the hardware or firmware supports and enables it |
| Data flow | Solid orange arrow | Data that crosses a boundary, in the direction of the arrow |
| Untrusted or optional flow | Dashed orange arrow | Untrusted input, or a flow that only exists when you enable an opt-in mechanism |

Boxes in the diagrams link to their explanation when it is on the same page.
Below a diagram, links point to the explanations of its other elements.

(security-architecture-further-reading)=
## Further reading

* [Ubuntu security documentation](https://documentation.ubuntu.com/security/)
* [Overview of security features by release](https://documentation.ubuntu.com/security/security-features/security-features-overview/)
