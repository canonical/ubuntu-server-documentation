---
myst:
  html_meta:
    description: "How Ubuntu mediates network input, privilege elevation, and system calls at the network, userspace, and kernel boundaries."
---

(security-architecture-upper-boundaries)=
(network-userspace-kernel-boundaries)=
# Network, userspace, and kernel boundaries

This page looks at the two upper boundaries in more detail: where network
input enters userspace, and where userspace processes request services from
the kernel. It shows how Ubuntu validates untrusted input and mediates
privilege transitions at each boundary, in three steps: from the network to a
service, from an unprivileged user to privileged actions, and from a process
to the kernel.

The diagrams on this page follow the
{ref}`diagram conventions <security-architecture-legend>`. To go to the
explanation of a box, select the box in the diagram.

(security-architecture-network-boundary)=
## Network to userspace

Three mechanisms protect the path from the network to a service.

```{mermaid}
:alt: Network to userspace. Untrusted packets from remote clients and peers reach Netfilter hooks in the kernel, which apply TCP SYN cookies and any firewall rules loaded from nftables or ufw (opt-in). Accepted connections reach a network-facing service, such as OpenSSH or a TLS server, which runs inside a systemd service sandbox and encrypts and authenticates the session.
:caption: From the network to a service

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
    subgraph NETZ["Outside — untrusted"]
        pkt["Remote clients and<br>untrusted peers"]
    end
    subgraph KZ["Linux kernel"]
        nf["Netfilter hooks,<br>TCP SYN cookies"]
    end
    subgraph US["Userspace"]
        rules["nftables or ufw rules<br>(opt-in)"]
        subgraph SANDBOX["systemd service sandbox"]
            svc["Network-facing service<br>(OpenSSH, TLS server)"]
        end
    end
    pkt -.->|"Untrusted packets"| nf
    rules -.->|"Loaded rules"| nf
    nf -->|"Accepted connections"| svc
    svc -->|"Encrypted, authenticated<br>session"| pkt
    style NETZ fill:#FFFFFF,stroke:#000000,stroke-width:2px
    style KZ fill:#FFFFFF,stroke:#000000,stroke-width:2px
    style US fill:#FFFFFF,stroke:#000000,stroke-width:2px
    style SANDBOX fill:#FFFFFF,stroke:#000000,stroke-width:1px

    subgraph LEG["Legend"]
        direction LR
        leg0["Trust zone"]
        leg1["Untrusted"]
        leg2["Component"]
        leg3["Opt-in"]
        leg4s[" "] --> leg4["Data flow"]
        leg5s[" "] -.-> leg5["Untrusted or<br>optional flow"]
        leg0 ~~~ leg1
        leg1 ~~~ leg2
        leg3 ~~~ leg4s
        leg4 ~~~ leg5s
    end
    US ~~~ LEG

    classDef component fill:#F3F3F3,stroke:#000000,stroke-width:1px,color:#000000
    classDef hidden fill:none,stroke:none,color:#FFFFFF
    classDef note fill:#FFFFFF,stroke:none,color:#000000
    classDef optin fill:#F3F3F3,stroke:#000000,stroke-width:1px,stroke-dasharray:4 4,color:#000000
    classDef untrusted fill:#FFFFFF,stroke:#000000,stroke-width:1px,stroke-dasharray:4 4,color:#000000
    classDef zone fill:#FFFFFF,stroke:#000000,stroke-width:2px,color:#000000
    class pkt untrusted
    class nf,svc component
    class rules optin
    class leg0 zone
    class leg1 untrusted
    class leg2 component
    class leg3 optin
    class leg4 note
    class leg4s hidden
    class leg5 note
    class leg5s hidden
    click nf href "#security-architecture-packet-filtering"
    click rules href "#security-architecture-packet-filtering"
    click svc href "#security-architecture-encrypted-access"
    style LEG fill:#FFFFFF,stroke:#666666,stroke-width:1px
```

Other pages describe further elements of this diagram. See {ref}`security-architecture-network-peers`.

(security-architecture-packet-filtering)=
### Packet filtering

Netfilter processes every packet in the kernel before a service receives it.
Rules defined with {manpage}`nft(8)` or `ufw` can drop or limit traffic. TCP
SYN cookies keep services reachable during SYN flood attacks. See
[SYN cookies](https://documentation.ubuntu.com/security/security-features/network/syn-cookies/).

(security-architecture-encrypted-access)=
### Encrypted and authenticated access

OpenSSH and Transport Layer Security (TLS) libraries protect remote sessions
and service traffic. Ubuntu configures these libraries to reject legacy
protocol versions and weak algorithms. See {ref}`explanation-cryptography`.

(security-architecture-service-sandboxing)=
### Service sandboxing

Network-facing services run as `systemd` units. The unit file can drop
privileges and restrict the service, for example with a dedicated user,
`NoNewPrivileges=`, `ProtectSystem=`, and system call filters. See
{manpage}`systemd.exec(5)`.

(security-architecture-privilege-boundary)=
## Privilege elevation and authentication

Three components mediate the transition from an unprivileged user or service
to privileged actions.

```{mermaid}
:alt: Privilege elevation and authentication. Users log in through login services, such as the console, SSH, or the display manager, which pass credentials to PAM. PAM can add multi-factor authentication, smart cards, or network identity providers (opt-in). An unprivileged session or application elevates privileges through sudo-rs, which authenticates the user with PAM, or calls a privileged daemon over D-Bus, which checks the authorization of the caller with polkit.
:caption: From an unprivileged user to privileged actions

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
        users["Remote and local users"]
    end
    subgraph UNPRIV["Unprivileged"]
        user["User session<br>or application"]
    end
    subgraph PRIV["Privileged (root)"]
        login["Login services<br>(console, SSH, display manager)"]
        sudo["sudo-rs"]
        daemon["Privileged daemon"]
        polkit["polkit"]
        pam["PAM"]
        mfa["Multi-factor, smart card,<br>network identity (opt-in)"]
    end
    users -->|"Credentials"| login
    login -->|"Authentication"| pam
    login -->|"Starts session"| user
    user -->|"Elevation request"| sudo
    sudo -->|"Authentication"| pam
    user -->|"D-Bus call"| daemon
    daemon -->|"Authorization check"| polkit
    pam -.->|"Additional factors"| mfa
    style OUT fill:#FFFFFF,stroke:#000000,stroke-width:2px
    style UNPRIV fill:#FFFFFF,stroke:#000000,stroke-width:2px
    style PRIV fill:#FFFFFF,stroke:#000000,stroke-width:2px

    subgraph LEG["Legend"]
        direction LR
        leg0["Trust zone"]
        leg1["Untrusted"]
        leg2["Component"]
        leg3["Ubuntu default"]
        leg4["Opt-in"]
        leg5s[" "] --> leg5["Data flow"]
        leg6s[" "] -.-> leg6["Untrusted or<br>optional flow"]
        leg0 ~~~ leg1
        leg1 ~~~ leg2
        leg2 ~~~ leg3
        leg4 ~~~ leg5s
        leg5 ~~~ leg6s
    end
    PRIV ~~~ LEG

    classDef component fill:#F3F3F3,stroke:#000000,stroke-width:1px,color:#000000
    classDef hidden fill:none,stroke:none,color:#FFFFFF
    classDef note fill:#FFFFFF,stroke:none,color:#000000
    classDef optin fill:#F3F3F3,stroke:#000000,stroke-width:1px,stroke-dasharray:4 4,color:#000000
    classDef ubuntu fill:#000000,stroke:#000000,stroke-width:1px,color:#FFFFFF
    classDef untrusted fill:#FFFFFF,stroke:#000000,stroke-width:1px,stroke-dasharray:4 4,color:#000000
    classDef zone fill:#FFFFFF,stroke:#000000,stroke-width:2px,color:#000000
    class users untrusted
    class user,login,daemon,polkit,pam component
    class sudo ubuntu
    class mfa optin
    class leg0 zone
    class leg1 untrusted
    class leg2 component
    class leg3 ubuntu
    class leg4 optin
    class leg5 note
    class leg5s hidden
    class leg6 note
    class leg6s hidden
    click login href "#security-architecture-pam"
    click user href "#security-architecture-privilege-boundary"
    click sudo href "#security-architecture-sudo-rs"
    click daemon href "#security-architecture-polkit"
    click polkit href "#security-architecture-polkit"
    click pam href "#security-architecture-pam"
    click mfa href "#security-architecture-pam"
    style LEG fill:#FFFFFF,stroke:#666666,stroke-width:1px
```

Other pages describe further elements of this diagram. See {ref}`security-architecture-users`.

(security-architecture-pam)=
### PAM

Login services, such as the console login, SSH, and the display manager, use
{manpage}`pam(7)` to authenticate users, check account restrictions, and set up
sessions. PAM modules add multi-factor authentication, smart cards, or network
identity providers if you configure them. See
{ref}`two-factor-authentication-with-totp-or-hotp`,
{ref}`smart-card-authentication`, and the
[authd documentation](https://documentation.ubuntu.com/authd/).

(security-architecture-sudo-rs)=
### `sudo-rs`

`sudo-rs` lets authorized users run commands as root with their own
credentials. The root account has no usable password by default. See
{ref}`user-management` and {ref}`sudo-rs`.

:::{note}
Ubuntu 24.04 LTS uses `sudo` instead of `sudo-rs` by default.
:::

(security-architecture-polkit)=
### polkit

polkit lets privileged daemons decide whether an unprivileged caller may
perform an action, such as mounting a disk or changing network settings. See
{manpage}`polkit(8)`.

(security-architecture-syscall-boundary)=
## Userspace to kernel

Every request from a userspace process to the kernel passes through the system
call interface. The kernel validates the arguments of each system call, and
copies data from and to process memory only through dedicated functions, such
as `copy_from_user()`, which check that the memory belongs to the calling
process. The kernel then applies the following checks.

```{mermaid}
:alt: Userspace to kernel. A userspace process makes a system call. The kernel checks the system call entry, its arguments, and access to process memory, then applies the seccomp-bpf filter of the process, discretionary access control and capabilities, and the AppArmor and Yama Linux Security Module hooks, before it accesses kernel objects such as files, sockets, processes, and devices. Namespaces and cgroups scope and limit these objects. AppArmor profiles and seccomp filters are managed in userspace and loaded into the kernel.
:caption: From a process to the kernel

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
    subgraph US["Userspace"]
        proc["Userspace process"]
        policy[("Security policy<br>(AppArmor profiles,<br>seccomp filters)")]
    end
    subgraph KZ["Linux kernel"]
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
    proc -->|"System call"| sys
    sys --> seccomp
    seccomp -->|"Allowed calls"| dac
    dac -->|"Permitted access"| LSM
    LSM -->|"Mediated access"| obj
    nscg -->|"Scope and limit"| obj
    policy -->|"Profiles"| aa
    policy -->|"Filters"| seccomp
    style US fill:#FFFFFF,stroke:#000000,stroke-width:2px
    style KZ fill:#FFFFFF,stroke:#000000,stroke-width:2px
    style LSM fill:#FFFFFF,stroke:#000000,stroke-width:1px

    subgraph LEG["Legend"]
        direction LR
        leg0["Trust zone"]
        leg1["Component"]
        leg2["Ubuntu default"]
        leg3s[" "] --> leg3["Data flow"]
        leg0 ~~~ leg1
        leg1 ~~~ leg2
        leg2 ~~~ leg3s
    end
    KZ ~~~ LEG

    classDef component fill:#F3F3F3,stroke:#000000,stroke-width:1px,color:#000000
    classDef hidden fill:none,stroke:none,color:#FFFFFF
    classDef note fill:#FFFFFF,stroke:none,color:#000000
    classDef ubuntu fill:#000000,stroke:#000000,stroke-width:1px,color:#FFFFFF
    classDef zone fill:#FFFFFF,stroke:#000000,stroke-width:2px,color:#000000
    class proc,policy,sys,seccomp,dac,nscg,obj component
    class aa,yama ubuntu
    class leg0 zone
    class leg1 component
    class leg2 ubuntu
    class leg3 note
    class leg3s hidden
    click policy href "#security-architecture-policy"
    click sys href "#security-architecture-syscall-boundary"
    click seccomp href "#security-architecture-seccomp"
    click dac href "#security-architecture-dac"
    click aa href "#security-architecture-apparmor"
    click yama href "#security-architecture-yama"
    click nscg href "#security-architecture-namespaces"
    style LEG fill:#FFFFFF,stroke:#666666,stroke-width:1px
```

Other pages describe further elements of this diagram. See {ref}`security-architecture-layer-userspace`.

(security-architecture-seccomp)=
### seccomp-bpf

seccomp-bpf rejects system calls that the process's filter does not allow.
`snapd`, `systemd`, and many applications install filters. See
[seccomp filtering](https://documentation.ubuntu.com/security/security-features/privilege-restriction/#seccomp-filtering)
and {manpage}`seccomp(2)`.

(security-architecture-dac)=
### Discretionary access control and capabilities

The kernel checks the process's user and group IDs against file permissions
and {manpage}`acl(5)` entries, and checks {manpage}`capabilities(7)` for
privileged operations.

(security-architecture-apparmor)=
### AppArmor

AppArmor restricts each confined program to the files, network access, and
capabilities listed in its profile, even if the program runs as root.
AppArmor also restricts the use of unprivileged user namespaces. See
{ref}`apparmor` and
[AppArmor](https://documentation.ubuntu.com/security/security-features/privilege-restriction/apparmor/).

(security-architecture-yama)=
### Yama

Yama allows a process to attach to another process with `ptrace` only if it is
an ancestor of that process, or has the required capability. See
[`ptrace` scope](https://documentation.ubuntu.com/security/security-features/process-memory/#ptrace-scope).

(security-architecture-namespaces)=
### Namespaces and cgroups

Namespaces and cgroups limit which resources a process can see, and how much
of them it can use. Containers and snaps build on them. See
{manpage}`namespaces(7)` and
[cgroups](https://documentation.ubuntu.com/security/security-features/privilege-restriction/cgroups/).

(security-architecture-policy)=
### Security policy

Policies for these mechanisms, such as AppArmor profiles, seccomp filters, and
`nftables` rules, are written and managed in userspace. Once loaded, the kernel
enforces them, and a process cannot bypass them without the privileges to
replace the policy.
