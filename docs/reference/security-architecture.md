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
