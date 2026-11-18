---
myst:
  html_meta:
    description: "Trust boundaries between an Ubuntu system, untrusted entities, and the external infrastructure services that Ubuntu relies on."
---

(security-architecture-context)=
(system-context)=
# System context and external trust boundaries

An Ubuntu system interacts with two kinds of external entity. Untrusted
entities, such as users, network peers, and attached devices, can send
arbitrary input to the system. External infrastructure services, such as the
Ubuntu archive, provide content that the system depends on. Ubuntu does not
trust the transport to these services: it verifies the content it receives
from them with cryptographic signatures.

The diagrams on this page follow the
{ref}`diagram conventions <security-architecture-legend>`. To go to the
explanation of a box, select the box in the diagram.

```{mermaid}
:alt: Context diagram. Three zones: Outside — untrusted (users and administrators, untrusted network peers, removable media and peripherals), External infrastructure services (Ubuntu archive and mirrors, Snap Store, LVFS, time, name, and identity services), and Inside — Ubuntu system (network-facing services, services and applications, outbound system clients, privileged components, and secrets and configuration). Arrows show the data flows that cross the zone boundaries. A legend explains the box and arrow styles.
:caption: System context and trust boundaries of an Ubuntu system

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
    style OUT fill:#FFFFFF,stroke:#000000,stroke-width:2px
    style EXT fill:#FFFFFF,stroke:#000000,stroke-width:2px
    style IN fill:#FFFFFF,stroke:#000000,stroke-width:2px

    subgraph LEG["Legend"]
        direction LR
        leg0["Trust zone"]
        leg1["Untrusted"]
        leg2["External service"]
        leg3["Component"]
        leg4s[" "] --> leg4["Data flow"]
        leg5s[" "] -.-> leg5["Untrusted or<br>optional flow"]
        leg0 ~~~ leg1
        leg1 ~~~ leg2
        leg2 ~~~ leg3
        leg3 ~~~ leg4s
        leg4 ~~~ leg5s
    end

    classDef component fill:#F3F3F3,stroke:#000000,stroke-width:1px,color:#000000
    classDef external fill:#FFFFFF,stroke:#000000,stroke-width:1px,color:#000000
    classDef hidden fill:none,stroke:none,color:#FFFFFF
    classDef note fill:#FFFFFF,stroke:none,color:#000000
    classDef untrusted fill:#FFFFFF,stroke:#000000,stroke-width:1px,stroke-dasharray:4 4,color:#000000
    classDef zone fill:#FFFFFF,stroke:#000000,stroke-width:2px,color:#000000
    class users,peers,media untrusted
    class archive,store,lvfs,infra external
    class net,apps,clients,priv,data component
    class leg0 zone
    class leg1 untrusted
    class leg2 external
    class leg3 component
    class leg4 note
    class leg4s hidden
    class leg5 note
    class leg5s hidden
    click users href "#security-architecture-users"
    click peers href "#security-architecture-network-peers"
    click media href "#security-architecture-removable-media"
    click archive href "#security-architecture-archive"
    click store href "#security-architecture-snap-store"
    click lvfs href "#security-architecture-lvfs"
    click infra href "#security-architecture-infrastructure-services"
    click clients href "#security-architecture-archive"
    style LEG fill:#FFFFFF,stroke:#666666,stroke-width:1px
```

Other pages describe further elements of this diagram. See {ref}`security-architecture-network-boundary`, {ref}`security-architecture-layer-userspace`, {ref}`security-architecture-privilege-boundary`, and {ref}`security-architecture-data-at-rest`.

The following sections describe the entities and the data flows that cross
the system boundary.

(security-architecture-users)=
## Users and administrators

Users and administrators reach the system through network-facing services,
such as {manpage}`sshd(8)`, or through a local console. Network-facing services
hand credentials to privileged components, such as Pluggable Authentication
Modules (PAM), to authenticate users. See {ref}`openssh-server` and
{ref}`user-management`.

(security-architecture-network-peers)=
## Untrusted network peers

Network peers can send arbitrary traffic, which the kernel network stack
handles before it reaches a service. Firewall rules, if you configure them,
filter this traffic in the kernel. A default installation follows a
[no open ports](https://documentation.ubuntu.com/security/security-features/network/open-ports/)
policy, so only explicitly installed services listen on the network. Network
configuration received from a Dynamic Host Configuration Protocol (DHCP)
server is also untrusted input.

(security-architecture-removable-media)=
## Removable media and peripherals

Removable media and peripherals attach directly to privileged components: the
kernel and `udev` handle every new device. Data on removable media is
untrusted, even when a trusted local user mounts it.

(security-architecture-archive)=
## Ubuntu archive and mirrors

APT verifies packages against signed archive metadata, so mirrors and proxies
do not need to be trusted. See
[Ubuntu archive integrity verification](https://documentation.ubuntu.com/security/software-integrity/archive-verification/).

(security-architecture-snap-store)=
## Snap Store

`snapd` verifies each snap against assertions signed by the store before it
installs the snap. Once installed, a strictly confined snap runs with
AppArmor, seccomp, device cgroup, and mount namespace restrictions that
`snapd` sets up for it. See
[snap confinement](https://documentation.ubuntu.com/security/security-features/privilege-restriction/snap-confinement/).

(security-architecture-lvfs)=
## Linux Vendor Firmware Service (LVFS)

`fwupd` downloads firmware metadata and updates from the LVFS and verifies
their signatures before it applies an update.

(security-architecture-infrastructure-services)=
## Time, name, and identity services

Ubuntu synchronizes time with `chrony`, which uses Network Time Security (NTS)
to authenticate Ubuntu's time servers. DNS answers are not authenticated
unless you enable DNS Security Extensions (DNSSEC) validation. Identity
providers, such as LDAP, Kerberos, or Active Directory, are only used if you
configure them.

:::{note}
Ubuntu 24.04 LTS synchronizes time with `systemd-timesyncd`, which does not
support NTS. Starting with Ubuntu 25.10, new installations use `chrony` with
NTS. See {ref}`about-time-synchronisation`.
:::

On Ubuntu Desktop, further data flows cross the boundary: the display server
receives input events from keyboards and pointing devices, wireless stacks
communicate with access points and Bluetooth devices, and desktop applications
open untrusted documents and web content.
