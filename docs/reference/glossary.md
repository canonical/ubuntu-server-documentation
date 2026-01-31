---
myst:
  html_meta:
    description: "Comprehensive glossary of Ubuntu Server terminology, including definitions for common technical terms and concepts."
---

(reference-glossary)=
# Glossary

We are currently compiling and defining terms for this glossary. If you would
like to help, please visit our {ref}`contributions page <contribute>`
for details on how to get involved.

**Jump to:**

{ref}`A <terms_A>` -- {ref}`B <terms_B>` -- {ref}`C <terms_C>` --
{ref}`D <terms_D>` -- {ref}`E <terms_E>` -- {ref}`F <terms_F>` --
{ref}`G <terms_G>` -- {ref}`H <terms_H>` -- {ref}`I <terms_I>` --
{ref}`J <terms_J>` -- {ref}`K <terms_K>` -- {ref}`L <terms_L>` --
{ref}`M <terms_M>` -- {ref}`N <terms_N>` -- {ref}`O <terms_O>` --
{ref}`P <terms_P>` -- {ref}`Q <terms_Q>` -- {ref}`R <terms_R>` --
{ref}`S <terms_S>` -- {ref}`T <terms_T>` -- {ref}`U <terms_U>` --
{ref}`V <terms_V>` -- {ref}`W <terms_W>` -- {ref}`X <terms_X>` --
{ref}`Y <terms_Y>` -- {ref}`Z <terms_Z>`


(terms_A)=
## A

:::{glossary}

ABI
Application Binary Interface
    An ABI is an interface that defines how two modules interact with each other
    at the machine code level. Most often, these modules are applications using
    external libraries. An ABI defines a low-level and hardware-dependent
    interface compared to an {term}`API`, which is considered high-level and
    hardware-independent.

ACL
Access Control List
    An ACL is a list of access permissions that defines entities and their
    access rights to resources. ACLs can specify access with varying levels of
    granularity, ranging from full access to a resource, to permission for a
    specific operation.

    See also:
    * {manpage}`the ACL manual page <acl(5)>`

    Related topic(s):
    * Security, {term}`OpenLDAP`, and {term}`Kerberos`

AD
Active Directory
    An AD is a Microsoft service that acts as a central database storing and managing information about network objects (user accounts, groups, computers and shared resources) and their security in a Windows-based network.

ADSys
    ADSys is an Ubuntu-specific Active Directory ({term}`AD`) client developed by Canonical.
    ADSys complements System Security Services Daemon ({term}`SSSD`) by adding native
    Group Policy Object support, privilege management, and custom scripts
    execution.

    See also:
    * [the ADSys documentation](https://documentation.ubuntu.com/adsys/stable/)

    Related topic(s):
    * {term}`Group Policy Object` and {term}`SSSD`

AES
Advanced Encryption Standard
    An AES is a symmetric encryption algorithm designed to encrypt data securely
    into an unreadable format that can only be decrypted with the same key used
    for encryption.

    Related topic(s):
    * Security

Alertmanager
    Alertmanager is an open-source monitoring system developed by the Prometheus
    project to monitor and handle alerts. It offers several key features,
    including *Grouping* to combine alerts, *Inhibition* to suppress certain
    alerts when others are already firing, and *Silencing* to temporarily mute
    specific alerts.

    See also:
    * [the Alertmanager documentation](https://prometheus.io/docs/alerting/latest/alertmanager/)

    Related topic(s):
    * Observability and {term}`Prometheus`

ALUA
Asymmetric Logical Unit Access
    It is a storage concept used in Small Computer System Interface (SCSI)
    environments, particularly in Multi-Path Input/Output (MPIO) setups for
    shared storage systems like Storage Area Networks (SANs).
    ALUA informs a system about which paths to a storage device are optimal and
    which are non-optimal, enabling it to make smarter decisions about
    accessing shared disks.

    Related topic(s):
    * {term}`MPIO` {term}`SCSI`, {term}`SAN`

AMD
Advanced Micro Devices
    AMD can refer to:

    * The (AMD) company: semiconductor company that designs computer components
    * An AMD processor: a microprocessor designed and produced by the AMD company
    * All Intel/AMD 64-bit processors: the term "amd64" is commonly used to
      refer to 64-bit processors due to the company's role in developing this
      architecture.

    Related topic(s):
    * Networking

AMD-SME
AMD Secure Memory Encryption
    AMD-SME is a security technology that transparently encrypts all system memory
    to protect data at rest. It encrypts the entire memory address space of the system
    using a key derived from the processor, protecting against physical attacks on memory.

    Related topic(s):
    * Cryptography, Security

AMD-SEV
AMD Secure Encrypted Virtualization
    AMD-SEV is a security technology that encrypts the memory of virtual machines
    (guests) independently from the host system. It uses a dedicated memory encryption
    key for each guest VM, preventing the hypervisor from reading or modifying guest
    memory. This protects guest confidentiality even when the hypervisor is compromised.

    Related topic(s):
    * Cryptography, Security, Virtualization

AMD-SEV-ES
AMD Secure Encrypted Virtualization - Encrypted State
    AMD-SEV-ES extends {term}`AMD-SEV` by encrypting the entire VM state, including
    CPU register contents, in addition to guest memory. This provides enhanced protection
    against hypervisor-based attacks by preventing the hypervisor from reading or modifying
    sensitive VM state during execution.

    Related topic(s):
    * Cryptography, Security, Virtualization

AMD-SEV-SNP
AMD Secure Encrypted Virtualization - Secure Nested Paging
    AMD-SEV-SNP is an extension of {term}`AMD-SEV-ES` that adds integrity protection
    for guest memory using Secure Nested Paging. It prevents the hypervisor from modifying
    guest memory contents and provides cryptographic attestation of the VM's launch state,
    ensuring the integrity and confidentiality of guest data.

    Related topic(s):
    * Cryptography, Security, Virtualization

Ansible
    Ansible is an open-source IT automation tool developed by Red Hat. It offers
    several automation features, enabling developers and organizations to
    automate provisioning, configuration management, and application deployment.

    See also:
    * [The Ansible website](https://docs.ansible.com/)

    Related topic(s):
    * Automation

Apache2
    A robust, open-source HTTP server software designed for the deployment and
    delivery of web-based applications and content. Functioning as a
    request-response service, Apache 2 processes HTTP requests from client
    applications, facilitating the transmission of static and dynamic web
    resources. It has a modular architecture, supporting a wide array of
    extensions, enabling customizable functionality including security protocols
    (e.g., {term}`SSL`/{term}`TLS`), server-side scripting, and content
    management.

    Widely deployed in server environments, Apache 2 is a foundational
    component of numerous web infrastructure stacks, underpinning a substantial
    portion of internet-accessible services.

    See also:
    * [The Apache project documentation](https://httpd.apache.org/docs/2.4/)

    Related topic(s):
    * {term}`Web servers <Web server>`

API
Application Programming Interface
    An API is a type of software interface that acts as a connection between
    different software programs, allowing them to communicate and exchange data.
    APIs exist on multiple layers of abstraction, from low-level APIs closest
    to system hardware to high-level web APIs that enable clients and remote
    servers to communicate.

AppArmor
    AppArmor is a Linux security module that provides
    {term}`Mandatory Access Control (MAC) <MAC>` for programs. AppArmor
    restricts what applications can do, even when they are compromised. It
    enforces a set of security policies (called profiles) that define what
    files, capabilities, and system resources a given program is allowed to
    access.

    See also:
    * [The AppArmor website](https://apparmor.net/)

    Related topic(s):
    * Security

Apport
    Apport is a debugging tool and crash reporting system used in Ubuntu and
    Debian-based Linux distributions. It can automatically detect crashes in
    programs and system services, collect detailed diagnostic data, generate
    crash reports, and prompt the user to send the report to developers via
    systems like Launchpad. It is typically disabled by default on production
    systems because it can expose sensitive information in logs, but is used
    during development or testing.

    See also:
    * [The Apport Wiki Page](https://wiki.ubuntu.com/Apport)

    Related topic(s):
    * Debugging

APT
Advanced Package Tool
    APT is a package management system used by Debian and Debian-based Linux
    distributions like Ubuntu. APT helps install, update, upgrade, and remove
    software packages from the command line.

    See also:
    * {ref}`package-management`

armhf
ARM hard-float
    armhf is a designation used in Linux distributions to describe a 32-bit
    variant of the ARM architecture that has hardware-based floating-point
    support. armhf is typically used for lightweight systems or backward
    compatibility, especially in embedded environments.

    Related topic(s):
    * arm32, arm64

ARP
Address Resolution Protocol
    ARP is a network protocol used to map an IP address to a physical machine
    ({term}`MAC address`) on a local area network (LAN).

    Related topic(s):
    * Networking

ASCII
American Standard Code for Information Interchange
    A character encoding standard.

async
asynchronous
    A term commonly used in programming to describe operations that take place
    without blocking the main execution thread. Instead of waiting for a
    particular operation to finish (such as reading a file or making a network
    request), "async" programs can keep running other operations in the meantime.
    These operations are often dispatched to the background, allowing them to
    run in parallel. If needed, however, the program can still wait for the
    result of an asynchronous operation.

    Related topic(s):
    * Concurrency, parallelism, and threading

attestation
    In Confidential or Trusted Computing contexts, attestation refers both to
    the process of generating verifiable evidence about the trustworthiness of
    a system, and to the artifact produced by that process (commonly called an
    attestation report or quote).

    - As a process: A TEE or TPM measures critical system components (firmware,
      boot chain, enclave/VM code) and cryptographically signs these
      measurements with keys rooted in hardware trust. The evidence is then
      checked by a verifier against reference values or policies.

    - As a document: The signed report (attestation) is the concrete proof
      presented to a verifier. It contains the measurements and cryptographic
      signatures used to establish trust.

    Attestation may be local (between components on the same host) or remote
    (to an external verifier). It underpins measured boot, secure provisioning,
    and Confidential Computing workloads.

Authenticator
    An authenticator is any system, method, or mechanism used to verify a
    user's identity during the authentication process. It can range from
    something as simple as a password field (e.g., LDAP {term}`bind`) to more
    advanced tools like biometric scanners or one-time code generators.
    Authenticators are essential components of authentication protocols and can
    be used in both single-factor and multi-factor authentication setups.

    Related topic(s):
    * OpenLDAP, authentication

autocommit
    autocommit is a database feature that automatically commits every
    individual SQL statement as soon as it is executed. When autocommit is
    enabled, every SQL statement is treated as its own transaction and is
    applied immediately and permanently.

    This means it is impossible to undo or roll back a statement executed with
    autocommit enabled. While autocommit is a common default in many systems,
    behavior can vary depending on the database or language bindings. For
    example, in Python's `sqlite3` module, Python 3.12 introduces changes to
    transaction control, allowing explicit control over autocommit mode.

    See also:
    * [autocommit behavior in Python's `sqlite3` module](https://docs.python.org/3/library/sqlite3.html#transaction-control)

    Related topic(s):
    * Databases

autodetect
    autodetect is the ability of a system to automatically detect and configure
    hardware or settings without user input. In Ubuntu Server and other Linux
    systems, this is used during boot or installation to identify devices like
    disks, network interfaces, or keyboard layouts. The kernel, installers, and
    configuration tools rely on autodetection to simplify setup by loading the
    right drivers and defaults based on the system's hardware and environment.

    Related topic(s):
    * Kernel modules

autoinstall
    Autoinstall is a feature in Ubuntu Desktop and Ubuntu Server that provides
    fully automated installations using a pre-defined configuration file. This
    file describes how the system should be installed, including disk
    partitioning, user accounts, package selection, and network settings.

    See also:
    * [The Autoinstall documentation](https://canonical-subiquity.readthedocs-hosted.com/en/latest/intro-to-autoinstall.html)

    Related topic(s):
    * cloud-init

autorid
    autorid is a Samba ID mapping backend that automatically assigns
    {term}`UID` and {term}`GID` values to security identifiers (SIDs) when
    integrating with Active Directory (AD). It ensures consistent and persistent
    Unix ID mapping without requiring manual configuration for each domain or
    user/group.

    See also:
    * [The autorid Samba Wiki](https://wiki.samba.org/index.php/Idmap_config_autorid)

    Related topic(s):
    * Samba, Active Directory

AWS
Amazon Web Services
    AWS is a cloud computing platform that offers a wide range of on-demand
    services such as compute, storage, networking, machine learning, analytics
    and much more. It allows individuals and companies to run applications
    without owning physical hardware, to scale resources up or down as needed,
    and to pay only for what they use.

    See also:
    * [The AWS documentation](https://docs.aws.amazon.com/)

    Related topic(s):
    * Clouds

:::


(terms_B)=
## B

:::{glossary}

backend
    *Work in Progress*

Backports
    *Work in Progress*

Backtrace
    *Work in Progress*

BDC
Backup Domain Controller
    *Work in Progress*

bind
    *Work in Progress*

BindDN
    *Work in Progress*

BIOS
    *Work in Progress*

BMC
Baseboard Management Controller
    *Work in Progress*

bootloader
    *Work in Progress*

BOOTP
Bootstrap Protocol
    A network protocol that assigns IP addresses and boot information to a disk-less system.

bootstrap
    *Work in Progress*

btrfs
B-tree File System
    *Work in Progress*

:::


(terms_C)=
## C

:::{glossary}

CA
Certificate Authority
    *Work in Progress*

CAC
Common Access Card
    *Work in Progress*

CARP
Cache Array Routing Protocol
    *Work in Progress*

CCID
Chip Card Interface Device
    *Work in Progress*

CDB
Command Descriptor Block
    *Work in Progress*

CGNAT
Carrier-Grade Network Address Translation
    *Work in Progress*

CGI
Common Gateway Interface
    *Work in Progress*

checksums
    *Work in Progress*

chrony
    *Work in Progress*

chroot
    *Work in Progress*

CIDR
Classless Inter-Domain Routing
    *Work in Progress*

Command history
    Command history is a feature in terminals and shells (like Bash, Zsh, or PowerShell) that stores the commands you have previously typed, allowing you to recall and reuse them. Common ways to acccess this feature are:
    * Press the up arrow to cycle through previous commands
    * Type history to see a numbered list of past commands
    * Use Ctrl+R to search through your history
    * Re-run a specific command with !123 (where 123 is the command number)

    Related topic(s):
    * {term}`Scrollback`
    
CIFS
Common Internet File System
    *Work in Progress*

CIS
Center for Internet Security
    *Work in Progress*

CLVM
Clustered Logical Volume Manager
    *Work in Progress*

CMS
Configuration Management System
    *Work in Progress*

CN
Common Name
    *Work in Progress*

colocation
    *Work in Progress*

conffile
    *Work in Progress*

config
    *Work in Progress*

connectionless
    *Work in Progress*

containerization
    *Work in Progress*

CPU
Central Processing Unit
    *Work in Progress*

CRL
Certificate Revocation List
    *Work in Progress*

crypto
cryptographic
    *Work in Progress*

CSR
Certificate Signing Request
    *Work in Progress*

CVE
Common Vulnerabilities and Exposures
    *Work in Progress*

:::

(terms_D)=
## D

:::{glossary}

DAC
Discretionary access control
    A form of access control where the owner of a resource can grant/revoke
    permissions to other users.

    Related topic(s):
    * Security

daemonize
    The process of converting a program to run in the background as a service,
    independent of user sessions.

DARPA
Defense Advanced Research Projects Agency
    A research and development agency of the United States Department of Defense
    responsible for the development of emerging technologies for use in the
    military.

DAS
Direct Attached Storage
    DAS is storage that is physically and directly connected to one computer. DAS is not shared over a network and it is accessible ONLY to the host it is connected to.

    See also:
    * {term}`NAS`
    * {term}`SAN`


DASD
Direct Access Storage Device
    This term was coined by IBM to refer to a type of storage that allows random
    access to storage (hard-drives, optical discs, etc). It contrasts with
    sequential access storage such as magnetic tape or punched cards.

    Related topic(s):
    * Storage

Datagram
    In networking, a self contained, independent packet sent over a network. It
    can be routed from source to destination without relying on earlier or
    subsequent transfers.

    Related topic(s):
    * Networking

dblink
Database link
    A connection between two databases (mainly Oracle and PostgreSQL), allowing
    one database to query data from the other.

    Related topic(s):
    * Databases

DC
Domain Component
    *Work in progress*

DDNS
Dynamic Domain Name System
    A service that automatically updates DNS records when the underlying IP
    address changes (aka, dynamic IP).

    Related topic(s):
    * Networking

deb822
    A structured configuration format based on RFC822.

    See also:
    * [RFC 822](https://datatracker.ietf.org/doc/html/rfc822)
    * The {manpage}`deb822(5)` manual page

debconf
    A {term}`configuration management system <CMS>` handling the configuration
    of software packages during installation or upgrades by prompting users for
    necessary settings and storing them for subsequent installations or updates.

deduplication
    Process of removing duplicate copies of data in storage spaces. The
    redundant data is then replaced with a reference to the original.

denylist
    In cyber-security, a denylist is a list of entities (IP, domains, emails,
    etc), that are explicitly denied access to a system or service.

    Related topic(s):
    * Security

DER
Distinguished Encoding Rules
    A standardized encoding format for data (mostly cryptographic certificates
    and keys) for transmission and storage.

DGC
Distributed Garbage Collection
    A process used in distributed systems to manage memory across multiple
    interconnected computers allowing identification and reclaiming of unused
    memory across nodes.

DHCP
Dynamic Host Configuration Protocol
    A network protocol used to automatically assign network configuration
    details (IP, DNS, gateway, etc) to devices allowing for easy network
    management and connections within the network.

DHCPD
Dynamic Host Configuration Protocol Daemon
    Server software responsible for assigning the network configuration via
    DHCP.

DIT
Directory Information Tree
    In directory services (LDAP) this is a hierarchical tree-like structure
    used to organize and store information.

    Related topic(s):
    * OpenLDAP

DKMS
Dynamic Kernel Module Support
    A framework used in Linux systems to automatically rebuild and install
    kernel modules when the kernel is updated.

    Related topic(s):
    * Kernel

DMA
Direct Memory Access
    DMA is a technology that allows peripheral devices (hard drives, network
    cards, etc) to access the system's memory directly, bypassing the CPU and
    thus improving performance.

DMAR
Direct Memory Access Remapping
    DMAR is a technology used to control and secure
    {term}`Direct Memory Access <DMA>` operations and ensure that devices can
    only access memory regions they are authorized to. This helps to prevent
    unauthorized access, memory corruption, or security vulnerabilities. It is
    often used in virtualized environments to isolate devices between
    {term}`virtual machines (VMs) <VM>` and the host system.

dmesg
    A command in Linux systems that displays system logs related to hardware,
    drivers, and kernel events, such as system startup, device detection, and
    errors. It is commonly used for troubleshooting hardware issues and system
    diagnostics.

DN
Distinguished Name
    In directory services (LDAP), this is a unique identifier used to represent
    an entry in a directory, such as a user or a group. It's often composed of
    sub-components like {term}`CN`, {term}`OU`, or {term}`DC`.

DNS
Domain Name System
    A system that translates human-readable domain names (e.g. `ubuntu.com`)
    to their IP addresses (`185.125.190.20`).

    Related topic(s):
    * Networking

dnsmasq
    A lightweight, open-source {term}`DNS` and {term}`DHCP` server software.

DNSSEC
Domain Name System Security Extensions
    DNSSEC is a set of security extensions to {term}`DNS` which allow DNS data
    to be verified for authenticity and integrity.

    Related topic(s):
    * Security

Docker
    One of the most popular containerization platforms, which allows developers
    to package applications -- together with their dependencies -- into
    lightweight containers. This provides a consistently reproducible
    environment for deploying applications.

    Related topic(s):
    * Containers

DocumentRoot
    A directive in web server configuration files that specifies the directory
    on the server where web files are stored (root location).

DoT
DNS over TLS
    DNS over TLS utilizes {term}`Transport Layer Security (TLS) <TLS>` to encrypt the entire DNS connection, rather than just the payload. DoT servers listen on TCP port 853.

    See also:
    * [RFC 7858](https://datatracker.ietf.org/doc/html/rfc7858)

    Related topic(s):
    * Networking
    * Security

DoH
DNS over HTTPS
    DNS over HTTPS is tunneling DNS query data over encrypted {term}`HTTPS <HTTPS>` connections. It uses TCP port 443, and thus looks similar to web traffic.

    See also:
    * [RFC 8484](https://datatracker.ietf.org/doc/html/rfc8484)

    Related topic(s):
    * Networking
    * Security

dpkg
    `dpkg` is a package manager for Debian-based systems. It can install, remove,
    and build packages, but unlike other package management systems, it cannot
    automatically download and install packages -– or their dependencies.

DRBD
Distributed Replicated Block Device
    A software-based storage solution for Linux that allows for the mirroring of
    block devices between multiple hosts. The replication is transparent to
    other applications on the host systems. Any block device hard disks,
    partitions, RAID devices, logical volumes, etc can be mirrored.

    Related topic(s):
    * Storage

DTLS
Datagram Transport Layer Security
    A protocol that provides security for datagram-based communication, such as
    {term}`UDP`. It is designed to offer similar security features as {term}`TLS`
    but adapted for the connectionless nature of datagram protocols.

:::


(terms_E)=
## E

:::{glossary}

EAL
Environment Abstraction Layer
    A software layer that provides a standardized interface between an
    operating system and the underlying hardware. It abstracts hardware-specific
    details, allowing software to run on different hardware platforms without
    modification.

ECKD
Extended Count Key Data
    A disk storage format used by IBM mainframe systems, which provides advanced
    features such as better error detection and correction, as well as enhanced
    management of data records.

EFI
Extensible Firmware Interface
    A type of firmware interface designed to initialize hardware and load the
    operating system during the boot process of a computer. Replacement for the
    older {term}`BIOS` and ancestor of the {term}`UEFI`.

ELinks
    A text-based web browser for Unix-like operating systems. It allows users to
    browse the web in a terminal, making it ideal for environments without a
    {term}`GUI`.

Engenio
    A company that developed and manufactured storage systems including
    {term}`SAN` and {term}`NAS`. Later acquired by LSI Corporation and then by
    Seagate Technology.

EOL
End of life
    When a product, service, software is no longer supported or maintained.

ERD
Enterprise Ready Drivers
    Drivers that are specifically designed and optimized for use in enterprise
    environments, where stability, performance, and reliability are critical.

ESM
Expanded Security Maintenance
    A service provided by Canonical to extend security updates and patches for
    older {term}`LTS` releases of the Ubuntu operating system after the LTS
    standard support period has ended.

ESXi
    A bare-metal virtualization platform created by VMWare that enables
    multiple virtual machines to operate on a single physical server.

:::

(terms_F)=
## F

:::{glossary}

failover
    In a {term}`Storage Area Network (SAN) <SAN>` environment, this occurs when
    data flows into an alternative I/O path because a cable, switch, or
    controller in the current path failed.

    It is a common feature in high availability environments and is handled
    (usually automatically) by multipathing software.

fallbacks
    This is a manual or automatic switch to an alternative method, when the
    primary option fails or is less preferred.

FastCGI
Fast Common Gateway Interface
    FastCGI is an extension of the {term}`CGI` protocol that starts a persistent
    FastCGI application process, allowing it to handle multiple requests instead
    of starting a new process for each request as a traditional CGI does.

FC
Fiber Channel
    FC is a storage networking protocol used for low-latency communication
    between a storage device and a node in a
    {term}`Storage Area Network (SAN) <SAN>`.

FHS
Filesystem Hierarchy Standard
    FHS is a standard that defines the directory structure and contents in
    Linux and Unix-like operating systems.

Fileset
    A fileset defines a group of directories that will be included when
    performing a backup job using Bacula.

    Related topic(s):
    * Storage

filesystem
    A filesystem defines how data is organized, stored, and accessed on a
    storage device.

    Related topic(s):
    * Storage

FTP
File Transfer Protocol
    It is one of the tools used to move files between computers. FTP was created in 1970s. It is not secure as it transfers files, usernames, and passwords in plain text. It uses port 21.
    Use only with legacy systems. Avoid unless wrapped in a secure network.

    Related topic(s):
    * {term}`SFTP`
    * {term}`rsync`
    * {term}`SCP`

FIPS
Federal Information Processing Standard
    A set of publicly-announced US government standards for codes, data security and encryption.

    See also:
    * [NIST](https://en.wikipedia.org/wiki/National_Institute_of_Standards_and_Technology)

Fluentd
    Fluentd is a data collection platform that gathers events from a container
    for later analysis on other platforms.

    Related topic(s):
    * Observability, Containers

FQDN
Fully Qualified Domain Name
    A FQDN represents a complete name that specifies the exact location of a
    host within the {term}`DNS` hierarchy.

    Related topic(s):
    * Networking

FreeIPA
Free Identity, Policy, and Audit
    FreeIPA is an open-source security solution for Linux/Unix-like systems that
    stores user identities in an {term}`LDAP` directory, manages a {term}`CA`,
    and enables authentication, policy enforcement, and auditing through
    integrations with {term}`SSSD` and {term}`Kerberos`.

    Related topic(s):
    * Security, OpenLDAP

Freenode
    Freenode is an open-source {term}`Internet Relay Chat (IRC) <IRC>` platform
    used by many open-source communities for real-time discussions.

frontend
    A frontend is a user-friendly interface for managing a complex system.

    - In firewall management, a frontend like `ufw` simplifies configuring
      `iptables`.
    - In QEMU/KVM graphics, a frontend is the virtual graphic adapter presented
      to the guest {term}`OS`, allowing it to process and store graphical output
      in memory. The guest OS treats it like a {term}`GPU`, while the host
      determines how to display the output using the {term}`backend`.
    - In LDAP, the frontend is a unique database that defines global default
      settings, such as who the admin user is, who can access database entries,
      or the limit on the number of search results. These settings apply to all
      LDAP databases inside {term}`slapd`, unless overridden.

    Related topic(s):
    * Virtualization and containers, Security, OpenLDAP

fsck
File System Check
    fsck is a Linux/Unix-like system utility tool that checks for, and
    repairs, any {term}`filesystem` errors.

    Related topic(s):
    * Storage

FULLTEXT
    FULLTEXT is an index type that allows for fast indexing and searching large
    quantities of text. It takes a sentence, splits it into words, and links
    them to row IDs. When a search query for a word is made, MySQL quickly looks
    up the row the word appear in, and retrieves all matching row IDs, rather
    than scanning the entire table. It can also find similar words using natural
    language processing.

    See also:
    * [Full-Text Search Functions](https://dev.mysql.com/doc/refman/8.4/en/fulltext-search.html)

    Related topic(s):
    * Databases

FW
Firmware
    Firmware is a software that runs before an operating system (OS) boots.

    - When a QEMU microvm starts, the firmware initializes minimal virtual
      hardware like allocating {term}`RAM` to the OS, and then loads the Linux
      kernel into memory.

    - In a physical device, firmware configures {term}`PCIe` devices like
      {term}`GPUs <GPU>` or network cards.

:::

(terms_G)=
## G

:::{glossary}

gcplogs
    A logging driver that allows logs to be forwarded from a Docker container
    running in Google Cloud to the Google Cloud Logging service.

    Related topic(s):
    * Cloud, Containers, Observability

gcrypt
    A cryptographic library that supports encryption, hashing, etc. for
    applications.

    Related topic(s):
    * Cryptographic libraries

GDB
GNU Debugger
    GDB traces the current execution of a program, with the aim of identifying
    any issues.

    Related topic(s):
    * Debugging

GELF
Graylog Extended Log Format
    GELF is a logging driver that allow logs to be forwarded in {term}`JSON`
    format, but with extra unique fields. These logs are sent from a Docker
    container to a data collector platform like {term}`Graylog`, {term}`Logstash`, and
    {term}`Fluentd`.

    Related topic(s):
    * Containers, Observability

GFS2
    A shared-disk {term}`filesystem` that allows multiple servers to access a
    single disk. It uses a locking system to ensure that no two servers modify
    the same data simultaneously, thus preventing data corruption if one server
    fails. Additionally, fencing is used to isolate failed nodes, ensuring that
    their locks can be safely recovered.

    Related topic(s):
    * High availability, Storage

GB
    Gigabyte (unit of measurement)
    1 GB = 1024 bytes

GID
Group ID
    A GID is an identifier for a collection of users. It helps administrators
    enforce system or file access permissions on multiple users at once.

    Related topic(s):
    * Active Directory integration, Samba, Security, SSSD

gitolite
    {ref}`Gitolite <install-gitolite>` is a tool installed on a central server for managing git
    repositories and controlling access to them, all via the command line. The
    central server becomes a git server.

    Related topic(s):
    * Backups and version control

GKE
Google Kubernetes Engine
    GKE is a managed Kubernetes service provided by Google cloud.

GL
Graphics Library
    A GL is an {term}`API` for interacting with a graphics card, enabling it to
    perform better rendering.

    Related topic(s):
    * Graphics

GNU
GNU's Not Unix
    A recursive acronym, GNU, is an operating system containing several free
    software packages. It can be used in combination with the Linux kernel.

GnuTLS
GNU's Not Unix Transport Layer Security
    GnuTLS is a GNU software package that secures data-in-transit by
    implementing the {term}`SSL`, {term}`TLS` and {term}`DTLS` protocol.

    Related topic(s):
    * Cryptography, Web services, OpenLDAP

GPG
GNU Privacy Guard
    GPG is a GNU software package that secures data-at-rest before sending it
    to a recipient.

    Related topic(s):
    * Security, Cryptography

GPS
Global Positioning System
    GPS is a collection of satellites that provides accurate time using radio
    signals from their atomic clocks. A GPS receiver plugged into a computer
    can sync with these satellites and generate {term}`PPS` signal, which
    delivers ultra-accurate time that applications can use as a time source.

    Related topic(s):
    * Networking

GPSD
GPS daemon
    This reads data from a GPS receiver and makes it available as a shared
    resource to multiple applications (e.g., {term}`Chrony`) to use for precise
    time synchronization.

    Related topic(s):
    * Networking

GPU
Graphics Processing Unit
    A GPU enhances graphics rendering for a computer and any virtual machines
    running inside of it.

    Related topic(s):
    * Graphics, Virtualisation and containers

Graylog
    A data collector platform for storing, analysing, and interpreting logs.
    These logs are received from a {term}`gelf` logging driver in Docker.

    Related topic(s):
    * Containers

GPO
Group Policy Object
    A set of configuration rules used to manage and enforce security and system
    behaviours across users or computers within an Active Directory (AD) object.

    Related topic(s):
    * Active Directory integration

GRUB
GRand Unified Bootloader
    *Work in progress*

GSSAPI
Generic Security Services Application Program Interface
    GSSAPI is a vendor-agnostic {term}`API` that uses an existing communication
    protocol to establish a secure communication between applications. It does
    this securely by verifying user credentials, ensuring that data being
    transmitted remains unchanged, preventing unauthorized access, and securely
    negotiating encryption keys.

    Related topic(s):
    * Cryptography

GTK
GIMP Toolkit
    GTK is a library used to create {term}`graphical user interfaces (GUIs) <GUI>`.
    It provides a visual interface for interacting with the Bacula Director
    when managing backup-related operations.

    Related topic(s):
    * Graphics, Backups and version control

GUI
Graphical User Interface
    A GUI is a visual representation of operations within a computer. It is
    usually represented as icons rather than text only.

GZIP
GNU Zip
    GZIP is a {term}`GNU` software package used to reduce the file size of a
    backup.

    - When applied directly to files, it replaces the original file type with a
      `.gz` type.
    - When used in Bacula's {term}`fileset`, it reduces the storage size of
      backed-up directories within Bacula's storage volumes.
    - When used to reduce the size of a folder, it works in combination with a
      `tar` tool which first combines multiple files into a single archive,
      before applying GZIP's size-reduction technique.

    Related topic(s):
    * Backups and version control

:::


(terms_H)=
## H

:::{glossary}

HA
High Availability
    HA is the process of ensuring that a system is always up. To achieve this,
    a redundant system is set up that either takes over when the main system is
    down or runs alongside the main system to load-balance the workload.

    Related topic(s):
    * High availability

HBA
Host Bus Adapter
    HBAs are interface cards that connect a server to a storage device.

    Related topic(s):
    * Device mapper multipathing

HMAC
Hash-based Message Authentication Code
    A HMAC is a type of {term}`Message Authentication Code <MAC>`. While a
    general MAC may use various techniques during combination, HMAC follows a
    structured way. When a message and its HMAC are sent, the receiver verifies
    the integrity by computing the HMAC again -- if the message is altered, the
    value will differ.

    Related topic(s):
    * Cryptography, Security

HMC
Hardware Management Console
    A HMC is used to manage IBM servers. It can handle tasks like
    configuring network settings, loading Ubuntu installation files and
    installing the {term}`OS`.

hostgroup
    A group of backend web or database servers with similar configurations.

    Related topic(s):
    * Observability

hostname
    A hostname identifies a server using a word rather than an {term}`IP address`.
    This makes it easier to remember.

HOTP
HMAC-based One-Time Password
    HOTP generates a one-time password by using the {term}`HMAC` algorithm in
    combination with a counter. When a client presents the {term}`OTP`, the
    server compares it with OTPs generated within a specific counter window to
    find a match.

hotplug
    The process of adding or removing a device (USB, disks, etc.) while a
    virtual machine is running.

HPB
Host Physical Bits
    HPB are appended to the name of an Ubuntu machine type. It signifies that a
    virtual machine will use the same number of bits the host {term}`CPU` uses
    to point to physical memory.

HPC
High Performance Computing
    HPC is the use of multiple servers to improve the performance of a task.

HSG
High-availability Storage Group
    *Work in Progress*

HSV
Highly-available Storage Virtualization
    *Work in Progress*

HTCP
Hyper Text Caching Protocol
    *Work in Progress*

HTML
HyperText Markup Language
    *Work in Progress*

HTTP
HyperText Transfer Protocol
    *Work in Progress*

HTTPD
HyperText Transfer Protocol Daemon
    *Work in Progress*

HTTPS
HyperText Transfer Protocol Secure
    *Work in Progress*

hugepage
    A hugepage increases the page size on a host, and as a result, when virtual memory is allocated to an application, there are fewer page table entries required to map the virtual memory to physical memory. The page table entries are stored in Random Access Memory (RAM) and cached in the {term}`Translation Lookaside Buffer (TLB) <TLB>`.

HWE
Hardware Enablement
    *Work in Progress*

:::


(terms_I)=
## I

:::{glossary}

ICMP
Internet Control Message Protocol
    *Work in Progress*

ICP
Internet Cache Protocol
    *Work in Progress*

IDENT
Identification Protocol
    *Work in Progress*

IMAP
Internet Messages Access Protocol
    *Work in Progress*

init
initialization
    *Work in Progress*

I/O
Input/Output
    *Work in Progress*

IOMMU
Input-Output Memory Management Unit
    *Work in Progress*

IoT
Internet of Things
    *Work in Progress*

IP
Internet Protocol
    *Work in Progress*

IP address
    *Work in Progress*

IPC
Inter-Process Communication
    *Work in Progress*

IPL
Initial Program Load
    *Work in Progress*

IPMI
Intelligent Platform Management Interface
    *Work in Progress*

IPP
Internet Printing Protocol
    *Work in Progress*

IPSec
Internet Protocol Security
    *Work in Progress*

IPVS
IP Virtual Server
    *Work in Progress*

IQN
iSCSI Qualified Name
    *Work in Progress*

IRC
Internet Relay Chat
    *Work in Progress*

ISC
Internet Systems Consortium
    *Work in Progress*

iSCSI
Internet Small Computer System Interface
    *Work in Progress*

ISO
International Organization for Standardization
    *Work in Progress*

ISP
Internet Service Provider
    *Work in Progress*

:::


(terms_J)=
## J

:::{glossary}

jitter
    Jitter is the variation in delay or latency between when data packets are
    sent and when they are received over a network, causing irregular arrival
    times at the destination. This variation is often caused by network
    congestion, packet loss, poor hardware performance or differences in the
    path packets take. 

    Related topic(s):
    * Networking

journald
    journald, also known as systemd-journald, is a logging service
    developed by the {term}`systemd` project as part of the systemd suite. It
    collects and stores log messages from various sources, including systemd
    services, kernel messages, system logs, and application logs.
    journald stores logs in a binary format offering advantages, such as storage
    efficiency, searchability, and most especially structured logging. In
    containerized systems like Docker, it functions as a logging driver for
    containers.

    See also:
    * The {manpage}`journald.conf(5)` manual page
    * [Docker journald documentation](https://docs.docker.com/engine/logging/drivers/journald/) for details on using journald as a logging driver

    Related topic(s):
    * Logging, Observability

JSON
JavaScript Object Notation
    This is a language-independent text format that uses conventions familiar
    to programmers of the C-family of languages, including C, C++, C#, Java,
    JavaScript, Perl, Python, and many others. Due to its simplicity, it is an
    ideal lightweight data interchange language.

    See also:
    * [The JSON website](https://www.json.org/json-en.html)

:::


(terms_K)=
## K

:::{glossary}

KDC
Key Distribution Center
    *Work in Progress*

keepalive
    *Work in Progress*

Kerberos
    *Work in Progress*

keypair
    *Work in Progress*

keyring
    *Work in Progress*

keysalt
    *Work in Progress*

keyservers
    *Work in Progress*

keytab
    *Work in Progress*

keytool
    *Work in Progress*

KVM
Kernel-based Virtual Machine
    *Work in Progress*

:::


(terms_L)=
## L

:::{glossary}

LAN
Local Area Network
    *Work in Progress*

LDAP
Lightweight Directory Access Protocol
    *Work in Progress*

LDIF
LDAP Data Interchange Format
    *Work in Progress*

lightervisor
    *Work in Progress*

LinuxONE
    IBM Linux-only enterprise server platform.

Load-balancing
    *Work in Progress*

localhost
    *Work in Progress*

Log files
    *Work in Progress*

Logstash
    *Work in Progress*

Logwatch
    *Work in Progress*

LPAR
Logical Partition
    *Work in Progress*

LSI
Logic Systems Incorporated
    *Work in Progress*

LTS
Long-Term Support
    *Work in Progress*

LU
Logical Unit
    *Work in Progress*

LUA
Lua Scripting Language
    *Work in Progress*

LUN
Logical Unit Number
    *Work in Progress*

LV
Logical Volume
    *Work in Progress*

LVM
Logical Volume Manager
    A storage management framework in Linux that provides a layer of abstraction
    over physical storage devices. It allows disks or partitions to be pooled
    into a single storage space, enabling the creation of flexible logical
    volumes that can be easily resized or moved.

LXC
Linux Containers
    *Work in Progress*

LXD
Linux Container Daemon
    *Work in Progress*

:::


(terms_M)=
## M

:::{glossary}

MAAS
Metal as a Service
    *Work in Progress*

MAC
Message Authentication Code
    A MAC verifies that a message hasn't been modified during transmission by
    combining a shared secret key between the sender and receiver, and a hash
    function.

MAC address
    *Work in Progress*

{spellexception}`manpage`
manual page
    *Work in Progress*

MCE
Machine Check Exception
    *Work in Progress*

MD5
Message Digest Algorithm 5
    A cryptographic hash function producing a 128-bit checksum.

MDA
Mail Delivery Agent
    *Work in Progress*

`mdev`
Minimal Device Manager
    *Work in Progress*

metapackage
    *Work in Progress*

METAR
Meteorological Aerodrome Report
    *Work in Progress*

microservices
    *Work in Progress*

microVMs
    *Work in Progress*

MOTD
Message of the Day
    *Work in Progress*

mount points
    *Work in Progress*

MPIO
Multipath Input/Output
    *Work in Progress*

MSA
Modular Smart Array
    *Work in Progress*

MTA
Mail Transfer Agent
    *Work in Progress*

MTU
Maximum Transmission Unit
    *Work in Progress*

MUA
Mail User Agent
    *Work in Progress*

Multipass
    *Work in Progress*

Multipath
    *Work in Progress*

Multiview
    *Work in Progress*

MySQL
    *Work in Progress*

:::


(terms_N)=
## N

:::{glossary}

nameserver
    *Work in Progress*

namespace
    *Work in Progress*

NAS
Network Attached Storage
    NAS is a file-level computer data storage server connected to a computer network providing data access to a heterogeneous group of clients. In this context, the term "NAS" can refer to both the technology and systems involved, and a specialized computer appliance device unit built for such functionality, a NAS appliance or NAS box.

    See also:
    * {term}`DAS`
    * {term}`SAN`
  
NAT
Network Address Translation
    *Work in Progress*

Netboot
    *Work in Progress*

Netfilter
    *Work in Progress*

Netplan
    *Work in Progress*

NFS
Network File System
    *Work in Progress*

NFV
Network Functions Virtualization
    *Work in Progress*

nginx
    *Work in Progress*

NIC
Network Interface Card
    *Work in Progress*

NIS
Network Information Service
    *Work in Progress*

NMI
Non-Maskable Interrupt
    *Work in Progress*

NRPE
Nagios Remote Plugin Executor
    *Work in Progress*

NSCQ
Network System Configuration Queue
    *Work in Progress*

NSS
Name Service Switch
    *Work in Progress*

NTP
Network Time Protocol
    *Work in Progress*

NTS
Network Time Security
    *Work in Progress*

NUMA
Non-Uniform Memory Access
    *Work in Progress*

Nvidia
    *Work in Progress*

NVMe
Non-Volatile Memory Express
    *Work in Progress*

NVRAM
Non-Volative Random Access Memory
    *Work in Progress*

NVSwitch
NVIDIA NVLink Switch
    *Work in Progress*

:::


(terms_O)=
## O

:::{glossary}

OCF
Open Cluster Framework
    *Work in Progress*

OCFS
Oracle Cluster File System
    *Work in Progress*

OCI
Open Container Initiative
    *Work in Progress*

OCSP
Online Certificate Status Protocol
    *Work in Progress*

OpenLDAP
    *Work in Progress*

OpenSC
Open Smart Card
    *Work in Progress*

OpenSSH
    *Work in Progress*

OpenSSL
    *Work in Progress*

OpenStack
    *Work in Progress*

OpenSUSE
    *Work in Progress*

OpenVPN
    *Work in Progress*

OpenVZ
    *Work in Progress*

OpenWRT
    *Work in Progress*

OS
Operating System
    *Work in Progress*

OSA
Open Systems Adapter
    *Work in Progress*

OSI
Open Systems Interconnection
    *Work in Progress*

OSPF
Open Shortest Path First
    Open Shortest Path First (OSPF) is a widely used Interior Gateway Protocol (IGP) for IP networks, classifying as a link-state protocol that helps routers find the most efficient paths within a single Autonomous System (AS). It works by each router building a complete map (Link-State Database) of the network topology and using Dijkstra's algorithm to calculate the shortest path to all destinations, ensuring fast convergence and scalability, especially in large enterprise network.

    Related topic(s):
    * Networking

OTE
Operational Test and Evaluation
    *Work in Progress*

OTP
One-Time Password
    *Work in Progress*

OU
Organizational Unit
    *Work in Progress*

OverlayFS
    *Work in Progress*

OVS
Open vSwitch
    *Work in Progress*

:::


(terms_P)=
## P

:::{glossary}

PAM
Pluggable Authentication Module
    *Work in Progress*

passthrough
    *Work in Progress*

PB
    Petabyte (unit of measurement)
    1 PB = 1024 {term}`TB`

PCI
Peripheral Component Interconnect
    *Work in Progress*

PCIe
Peripheral Component Interconnect Express
    *Work in Progress*

PCS
Pacemaker/Corosync Stack
    *Work in Progress*

PDC
Primary Domain Controller
    *Work in Progress*

PEM
Privacy Enhanced Mail
    *Work in Progress*

Petitboot
    *Work in Progress*

PgSQL
    *Work in Progress*

PHP
PHP: HyperText Preprocessor
    *Work in Progress*

PID
Process Identifier
    *Work in Progress*

pingable
    *Work in Progress*

PIV
Personal Identity Verification
    *Work in Progress*

PKCS
Public-Key Cryptography Standards
    *Work in Progress*

PKI
Public Key Infrastructure
    *Work in Progress*

pluggable
    *Work in Progress*

PMD
Poll Mode Driver
    *Work in Progress*

pockets
    Sub-repositories within the Ubuntu Package Archive.

    See also:
    * [Ubuntu Project: pockets](https://documentation.ubuntu.com/project/how-ubuntu-is-made/concepts/package-archive/#pockets)

POSIX
Portable Operating System Interface (for UNIX)
    *Work in Progress*

Postcopy
    *Work in Progress*

Postfix
    *Work in Progress*

PostgreSQL
    *Work in Progress*

PostScript
    *Work in Progress*

Power 8
Power 9
    IMB POWER processor architectures used in enterprise servers.

PowerShell
    *Work in Progress*

PPA
Personal Package Archive
    *Work in Progress*

ppc
PowerPC
    *Work in Progress*

PPD
PostScript Printer Description
    *Work in Progress*

PPS
Pulse Per Second
    *Work in Progress*

Preboot
    *Work in Progress*

preseed
    *Work in Progress*

Prometheus
    *Work in Progress*

proxy
    *Work in Progress*

PTP
Precision Time Protocol
    *Work in Progress*

PTR
Pointer Record
    *Work in Progress*

PXE
Preboot Execution Environment
    *Work in Progress*

PXELINUX
PXE Linux Loader
    *Work in Progress*

:::


(terms_Q)=
## Q

:::{glossary}

QA
Quality Assurance
    *Work in Progress*

QDevice
Quorum Device
    *Work in Progress*

QEMU
Quick Emulator
    *Work in Progress*

QETH
QDIO Ethernet
    *Work in Progress*

quickstart
    *Work in Progress*

:::


(terms_R)=
## R

:::{glossary}

RAM
Random Access Memory
    *Work in Progress*

RangeSize
    *Work in Progress*

RDAC
Redundant Disk Array Controller
    *Work in Progress*

RDBMS
Relational Database Management System
    *Work in Progress*

RDN
Relative Distinguished Name
    *Work in Progress*

renderer
    *Work in Progress*

REXX
Restructured Extended Executor
    *Work in Progress*

RFC
Request For Comments
    *Work in Progress*

rid
Relative Identifier
    *Work in Progress*

RIP
Router Information Protocol
    Routing Information Protocol (RIP) is an older, simple distance-vector routing protocol that helps routers find the best path in small networks by counting "hops" (routers passed), using the Bellman-Ford algorithm, and periodically sending full routing tables to neighbors, though its 15-hop limit and bandwidth usage make it outdated for large networks, with OSPF or IS-IS being modern alternatives.

    Related topic(s):
    * Networking

RISC-V
Reduced Instruction Set Computing - Version Five
    *Work in Progress*

Rocks
    *Work in Progress*

ROM
Read-Only Memory
    *Work in Progress*

rootDN
Root Distinguished Name
    *Work in Progress*

rootfs
Root File System
    *Work in Progress*

routable
    *Work in Progress*

RSA
Rivest–Shamir–Adleman
    RSA is an asymmetric encryption algorithm.
    *Work in Progress*

rsync
Remote Sync
    Rsync is not strictly a protocol. Rsync is a file synchronization and transfer tool. It uses port 22, when over SSH, or 873 for rsync daemon. Rsync is the most efficient tool to synchronise backup tasks because it uses the Delta Transfer Algorithm method.

    See also:
    * {term}`FTP`
    * {term}`SCP`
    * {term}`SFTP`

RTC
Real-Time Clock
    *Work in Progress*

runtime
    *Work in Progress*

:::


(terms_S)=
## S

:::{glossary}

Samba
    Open source software that implements the SMB/CIFS protocol for file and printer sharing with Windows systems.

    See also:
    * {ref}`introduction-to-samba`

SAN
Storage Area Network
    A SAN is a dedicated network that connects servers to storage devices such as disk arrays and tape libraries. It is a specialized high-speed network that provides access to consolidated block-level data storage. It makes storage devices appear as locally attached to the operating system, even though they are on a separate network.

    See also:
    * {term}`NAS`

sandboxed
    Sandboxed means running software in an isolated environment where it cannot affect anything outside the sandbox.
    Sandboxing does two things:

    * Isolates: The sandboxed program cannot access:
        * Your files (unless explicitly allowed)
        * Other running programs
        * System settings
        * Network resources (in some cases)

    * Secures: If the sandboxed program is malicious or gets compromised, the damage is contained. It cannot spread to your whole system.

    Related topic(s):
    * Virtualization and containers

SANLOCK
Storage Area Network Locking Daemon
    SAN Locking Daemon is a lock manager designed for shared storage in {term}`SAN` environments.

SASL
Simple Authentication and Security Layer
    SASL is a framework that adds authentication and security to network protocols. SASL itself does not define how to authenticate. It defines how to negotiate and use authentication mechanisms.

SBD
Storage-Based Death
    SBD is a fencing mechanism used in high-availability (HA) Linux clusters to prevent split-brain scenarios and data corruption. SBD uses shared storage as a communication channel to coordinate cluster nodes and forcibly reboot ("fence") problematic nodes that might cause issues.

sbin
System Binaries
    `sbin/` is a directory in Unix/Linux systems that contains essential system administration commands and executables. It holds programs needed for system administration, booting, and repair.
    On many modern Linux distributions, `/sbin` is often symlinked to `/usr/sbin`, and both directories are merged as part of filesystem simplification efforts. The distinction is becoming less strict, but historically `/sbin` was for boot-essential tools.

schema
    Schema (plural: schemas or schemata) refers to a structured framework or blueprint that defines how data is organized. The meaning varies slightly depending on context.

SCP
Secure Copy Protocol
    SCP is a network protocol for securely transferring files between computers over {term}`SSH`. SCP allows you to copy files between a local and remote host, or between two remote hosts, with encryption to protect the data during transfer.

    See also:
    * {term}`FTP`
    * {term}`SFTP`
    * {term}`rsync`

Scrollback
    Scrollback refers to the ability to scroll back through previous content in a terminal or console window. Scrollback is the buffer that stores older content so you can scroll up to see it. Limitations are lost on close, not infinite, and the performance may suffer if the buffer is very large.

    Related topic(s):
    * {term}`Command history`

SCSI
Small Computer System Interface
    SCSI (pronounced "scuzzy") is both a physical interface (cables and connectors) and a command protocol (set of standards) for communicating with storage and peripheral devices like hard drives, tape drives, and scanners. Each device gets a unique ID number (0-7 or 0-15 depending on version). The last device in a SCSI chain needs a terminator to prevent signal reflection.
SDN
Software-Defined Networking
    *Work in Progress*

seccomp
Secure computing mode
    *Work in Progress*

SFTP
SSH File Transfer Protocol
    SFTP is a secure file transfer protocol that runs over {term}`SSH`. SFTP is fully encrypted. The port used is 22.

    See also:
    * {term}`FTP`
    * {term}`SCP`
    * {term}`rsync`

SGI
Silicon Graphics Inc.
    *Work in Progress*

SHA
Secure Hash Algorithm
    *Work in Progress*

sharding
    *Work in Progress*

Shell
    *Work in Progress*

SHM
Shared Memory
    *Work in Progress*

Shorewall
Shoreline Firewall
    *Work in Progress*

SIDs
Security Identifiers
    *Work in Progress*

SIMD
Single Instruction, Multiple Data
    *Work in Progress*

slapd
Standalone LDAP Daemon
    *Work in Progress*

SLAT
Second Level Address Translation
    *Work in progress*

smart card
    *Work in Progress*

SMB
Server Message Block
    *Work in Progress*

SMS
Short Message Service
    *Work in Progress*

SMTP
Simple Mail Transfer Protocol
    *Work in Progress*

SMTPS
SMTP Secure
    *Work in Progress*

Snap
    *Work in Progress*

snapd
    *Work in Progress*

snapshot
    *Work in Progress*

Snap store
    *Work in Progress*

SNMP
Simple Network Management Protocol
    *Work in Progress*

SOA
Start of Authority
    *Work in Progress*

Solaris
    *Work in Progress*

SPC
SCSI Primary Commands
    *Work in Progress*

Splunk
    *Work in Progress*

SRU
Stable Release Update
    *Work in Progress*

SSD
Solid State Drive
    *Work in Progress*

SSH
Secure Shell
    *Work in Progress*

SSH-key
Secure Shell Key
    A cryptographic encryption key pair for {term}`SSH`, usually used and created with {term}`OpenSSH`.
    It's split in two parts: a _public_ and a _private_ key files.
    The private key is secret and belongs to the owning user, and it's used to prove possession of that secret.
    The public key is not secret and is used to securely identify only the private key holder.
    That way, entering a public key on a server for {term}`SSH` access, only the private key holder can log in.

SSI
Server-Side Includes
    *Work in Progress*

SSL
Secure Sockets Layer
    *Work in Progress*

SSO
Single Sign-On
    *Work in Progress*

SSSD
System Security Services Daemon
    *Work in Progress*

stateful
    *Work in Progress*

STDIN
Standard Input
    *Work in Progress*

STDOUT
Standard Output
    *Work in Progress*

STDERR
Standard Error
    *Work in Progress*

STK
StorageTek
    *Work in Progress*

storage
    *Work in Progress*

subcommand
    *Work in Progress*

Subiquity
    *Work in Progress*

subnet
subnetwork
    *Work in Progress*

substring
    *Work in Progress*

subvolume
    *Work in Progress*

sudo
superuser do
    *Work in Progress*

superblock
    *Work in Progress*

symlink
    *Work in Progress*

syslog
    *Work in Progress*

systemctl
    *Work in Progress*

Systemd
    *Work in Progress*

:::


(terms_T)=
## T

:::{glossary}

tasksel
Task selector
     Tasksel is a Debian/Ubuntu tool that simplifies the installation of collections of related packages (called "tasks") for specific purposes, like setting up a mail server, LAMP stack, or desktop environment. Instead of manually installing dozens of packages, tasksel lets you install entire pre-configured software bundles with a single command.

TB
    Terabyte (unit of measurement)
    1 TB = 1024 {term}`GB`

TCP
Transmission Control Protocol
     TCP is one of the core protocols of the Internet Protocol Suite, providing reliable, ordered, and error-checked delivery of data between applications over a network. It is the "reliable" protocol that most internet applications depend on. You use {term}`TCP` whenever you need to be sure your data arrives intact and in order.

TDX
Trust domain extensions
    It is security technology from Intel that creates isolated, encrypted virtual machines called "Trust Domains".
    TDX:
    * Protects confidential workloads in cloud environments
    * Encrypts VM memory to protect it from the host system or hypervisor

TEE
Trusted Execution Environment
    A secure processor enclave that isolates code and data to ensure
    confidentiality, integrity, and verifiable trust, forming the foundation of
    Confidential Computing.

TFTP
Trivial File Transfer Protocol
   TFTP is a very simple, lightweight file transfer protocol that uses {term}`UDP` instead of {term}`TCP`, designed for basic file transfers where simplicity is more important than features or security. It is "trivial" because it has minimal functionality - no authentication, no encryption, no directory listing, just basic reading and writing of files.

TGS
Ticket Granting Service
    TGS is a credential issued by Kerberos used in the Kerberos authentication protocol, a key component of the Key Distribution Center (KDC) that issues service tickets to clients after initial authentication.

TGT
Ticket Granting Ticket
    TGT is a credential issued by Kerberos authentication systems. TGT allows users to request service tickets without re-entering their password.
    
TLB
Translation Lookaside Buffer
    TLB is a specialized cache in the {term}`CPU` that stores recent virtual-to-physical address translations, dramatically speeding up memory access by avoiding repeated page table lookups. It is a critical component of virtual memory systems that makes address translation fast enough to be practical. When the CPU translates a virtual address, it first checks the TLB. If the mapping is found, the translation is fast. If it is missing, the CPU retrieves the mapping from the page table in memory, which takes longer.

TLS
Transport Layer Security
    TLS is a cryptographic protocol that provides secure communication over a network by encrypting data transmitted between clients and servers. It is the successor to SSL (Secure Sockets Layer) and is what makes {term}`HTTPS` secure (the padlock icon in your browser).

tmpfs
Temporary Filesystem
    tmpfs is a filesystem that stores all files in virtual memory (RAM) instead of on a physical disk, making it fast but also volatile - data disappears when the system reboots or loses power.

tmux
Terminal Multiplexer
    tmux is a powerful command-line tool that allows you to manage multiple terminal sessions from a single window, with the ability to detach and reattach sessions. It is a way to have multiple terminal windows and split-screen layouts, all within a single terminal, with sessions that persist even when you disconnect.

topologies
    Topologies (in a networking context) refer to the physical or logical arrangement of devices and connections in a network - essentially how computers, switches, routers, and other devices are interconnected.

TOTP
Time-based One-Time Password
    TOTP is an algorithm that generates temporary, single-use passwords based on the current time and a shared secret key. It is one of the most common forms of two-factor authentication (2FA) used by apps like Google Authenticator, Microsoft Authenticator, and many others.

TPM
Trusted Platform Module
    A hardware security chip that securely stores cryptographic keys, measures system integrity during boot, and enables features such as secure storage,
 encryption, and attestation.

Traceback
    traceback is a term used in Python. Traceback is a report of the function call stack printed when an exception occurs. It shows the sequence of calls leading to the error, including file names, line numbers, and the exception type. It helps developers identify and debug issues by tracing execution backward from the failure point.

Traceroute
    Traceroute is a network diagnostic tool that shows the path packets take from your computer to a destination across the internet, revealing each hop (router) along the way.

TTYS
Teletype Terminals
    TTYS were electromechanical typewriter-like devices used as input/output terminals for telegraph networks and early computers. They sent and received text over serial lines, printing characters on paper instead of displaying them on a screen. Even though the physical machines are mostly gone, the term TTY still exists in Unix/Linux systems to represent:
    * A text-based input/output device
    * A terminal session
    * A console connection

TXT
Trusted Execution Technology
    TXT is Intel's hardware-based security technology that creates a trusted execution environment to protect systems from software-based attacks. In other words, TXT was designed to make sure that a computer boots into a trusted and verified state before loading the operating system or applications.
    It protects against:
    * Rootkits
    * Boot-level malware
    * Unauthorized changes to firmware or system software

:::

(terms_U)=
## U

:::{glossary}

UDA
Unified Data Architecture
   UDA is an approach that provides a unified framework for integrating and managing data across an organization in a cohesive, standardized manner.

UDP
User Datagram Protocol
    UDP is a network protocol used to send data between devices without creating or maintaining a connection. In other words, UDP is a connectionless transport layer protocol used for fast, low-overhead data transmission in iptables rules.

UEFI
Unified Extensible Firmware Interface
    UEFI is the modern replacement for BIOS (Basic Input/Output System). UEFI is the firmware interface between a computer's hardware and its operating system. UEFI initializes hardware during boot and hands control over to the operating system.

UFW
Uncomplicated Firewall
    UFW is a user-friendly command-line tool for managing netfilter firewalls on Linux systems, simplifying complex iptables commands.

UID
User Identifier
    UID known as User Identifier (in Unix/Linux contexts) or Unique Identifier (in general computing). In Unix-like systems, a UID is a numeric value assigned to each user account to uniquely identify them to the operating system.

UI
User Interface
    UI is the point of interaction between a user and a digital product, system, or application - essentially everything the user sees, touches, or interacts with when using software or hardware.

unicast
    Unicast is a one-to-one network communication method where data is sent from a single sender to a single specific receiver.

unmount
    Unmount is the process of safely detaching a filesystem from the system's directory tree, making it inaccessible until it is mounted again. Unmount is the opposite of mounting. Unmount is important for data integrity, file system consistency, and the safe removal of USB drives or SD cards.

untrusted
    Untrusted refers to:
    1. data coming from outside the system, such as files uploaded by users
    1. code coming from an external, unknown, or non-verified source, such as third-party plug-ins
    1. network that cannot be assumed secure, such as public WI-FI 

uptime
    Uptime is a measure of how long a system has been running continuously since its last boot, crash, or restart. Uptime indicates system stability and availability.

URI
Uniform Resource Identifier
    URI is a compact string of characters that uniquely identifies an abstract or physical resource, such as a webpage, file, email address, or concept, without specifying how to access it.

URL
Uniform Resource Locator
  URL is a standardized string that specifies the address of a web resource, such as webpages, image, or file, enabling browsers to locate and retrieve it over the internet.
userspace
    userspace (also appears as "user space" or "user-space") is the memory area and execution environment where normal applications and user programs run, as opposed to kernel space where the operating system kernel runs.

USN
Update Sequence Number
    USN is a 64-bit monotonically increasing integer in Windows NTFS file system used by the change journal to log and track file/directory modifications like creations, deletions, renames, or data changes.

usr
    Refers to the `/usr/` directory and stands for "Unix System Resources".

UUIDs
Universally Unique Identifiers
    UUIDs are 128-bit numbers (typically represented as 32 hexadecimal digits in groups like 8-4-4-4-12) designed to uniquely identify objects, resources, or entities across systems without requiring a central authority.

:::


(terms_V)=
## V

:::{glossary}

vCPU
Virtual Central Processing Unit
    vCPU is a virtualized processor core allocated to a virtual machine, representing the {term}`VM`'s share of the physical {term}`CPU` resources available on the host.

VCS
Version Control System
    VCS is a software tool that tracks, manages, and stores changes to files, over time, recording who made the modifications, when, and enabling reversion to prior versions. 

veth
Virtual Ethernet
   veth is a Linux networking feature that creates a pair of connected virtual network interfaces that act like a virtual cable - whatever goes into one end comes out of the other.

VFIO
Virtual Function I/O
   VFIO is a Linux kernel framework that allows safe, direct access to physical hardware devices (like GPUs, network cards, or storage controllers) from user space or {term}`VM`, using IOMMU ({term}`Input-Output Memory Management Unit`) hardware for security and isolation.
VFS
Virtual File System
    VFS is a kernel abstraction layer in operating systems like Linux that provides a uniform interface for applications to access diverse underlying file systems without needing to know their specifics.

VFs
Virtual Functions
   *Work in Progress*

VG
Volume Group
    VG is a key component of LVM ({term}`Logical Volume Manager`), which is a flexible storage management system for Linux. The VG is a pool created from one or more physical volumes (PVs).

vGPU
Virtual Graphics Processing Unit
    vGPU is a technology that allows a physical {term}`GPU` to be shared among multiple virtual machines, with each {term}`VM` getting its own portion of GPU resources for graphics rendering, compute tasks, or AI/ML workloads.

virsh
Virtual Shell
    virsh refers to '/usr/bin/virsh'. It is a command-line program (from the libvirt-clients software package) that lets you create, start, stop, and manage virtual machines on Linux.
VirtIO
Virtualization I/O
    VirtIO is a standardized, open-source framework for creating efficient virtual device drivers in virtualized environments. VirtIO is a specification that defines how virtual machines communicate with the hypervisor for I/O operations (disk, network, etc.) in a more efficient way than emulating real hardware.

virtual
    Virtual refers to something implemented in software or by abstraction rather than being a single, dedicated physical object or device. It behaves as if it were physical (from the user's or system's point of view), but it is created and controlled by software. 
    

virtualization
    Virtualization is the technology that creates software-based ({term}`virtual`) representations of physical computing resources like {term}`servers`, {term}`storage`, {term}`networks`, or {term}`operating systems`. Virtualization is the fundamental concept of abstracting physical hardware to create multiple simulated environments or dedicated resources from a single physical system.

VLAN
Virtual Local Area Network
    VLAN is a way to split one physical network (like a switch or group of switches) into multiple, separate logical networks at Layer 2. Each VLAN is its own broadcast domain. In other words, devices in different VLANs are isolated unless a router or Layer 3 switch is used between them.

VM
Virtual Machine
    VM is a software-based emulation of a physical computer that runs an operating system and applications just like a real computer, but it exists as a file or set of files on a host system. A hypervisor creates and manages the VMs by allocating portions of the physical hardware ({term}`CPU`, {term}`RAM`, {term}`storage`, {term}`network`) to each virtual machine. Each VM is isolated and thinks it has its own dedicated hardware.

VNC
Virtual Network Computing
    VNC is a system for remotely viewing and controlling another computer's graphical desktop over a network. VNC uses the remote frame buffer (RFB) to send screen updates from the remote machine and to receive keyboard and mouse input from the local machine.

VPN
Virtual Private Network
    VPN is a technology that creates an encrypted "tunnel" over a public network, such as the {term}`internet`, so that devices may communicate as if they were in a private network. It hides or masks your real {term}`IP`address and protects the data that travels between your device and the VPN end point. 


VRRP
Virtual Router Redundancy Protocol
    VRRP is a standard first-hop redundancy protocol that keeps a LAN's default gateway highly available. In other words, the VRRP is a router that lets multiple routers on the same subnet work together as a single "virtual" router with one shared IP or MAC address, so if one fails another can take over with minimal disruption, without changing host settings.

vsftpd
Very Secure FTP Daemon
    vsftpd is an FTP (File Transfer Protocol) server software for Unix-like systems (Linux, BSD) that is designed with security, performance, and stability as top priorities.

:::


(terms_W)=
## W

:::{glossary}

WAL
Write-Ahead Log
    WAL is a fundamental technique used in databases and storage systems to ensure data durability and consistency. The basic principle is simple: Write what you are going to do before you do it, so if things go wrong you can always know what was happening. In other words, before any changes are made to the actual database files, the system first writes a record of what it is about to do to a sequential log file. If the system crashes mid-operation, it can replay the log during recovery to complete interrupted operations or roll them back.

WAN
Wide Area Network
    WAN is a telecommunications network that extends over a large geographical area, typically connecting multiple smaller networks (like {term}`LANs`) across cities, countries, or even continents.

WCCP
Web Cache Communication Protocol
    WCCP is a Cisco-developed protocol used to transparently redirect network traffic (often web traffic) from routers or switches to caching or proxy devices. It is mainly used to improve performance, enable content filtering, and provide load balancing and fault tolerance for web or proxy services.
    

Web server
    A web server is software (and sometimes the hardware it runs on) that serves web content to clients over the {term} `internet` or an {term} `intranet`using {term} `HTTP/HTTPS` protocols.


winbind
Windows Bind
    winbind is a component of {term}`Samba` on Linux/UNIX systems that lets those systems use accounts from an {term}`AD` domain for logins and identity information. winbind makes a Linux machine "look like" a Windows client to AD, so the AD users and groups can log in to Linux and be resolved just like local Unix accounts.

WireGuard
    WireGuard is a modern, open-source {term}`VPN` protocol designed to create fast, secure, and simple encrypted tunnels between devices. It is now built into the Linux kernel and widely used by VPN providers because of its performance and small codebase.

WLAN
Wireless Local Area Network
    WLAN is a local area network that uses wireless communication (typically Wi-Fi) instead of physical cables to connect devices within a limited area.

WSGI
Web Server Gateway Interface
    WSGI is a specification that defines a standard interface between web servers and Python web applications or frameworks, creating portability and flexibility. It is a universal translator that allows any WSGI-compliant web server to communicate with any WSGI-compliant Python application.


WWID
World Wide Identifier
   WWID is a globally unique ID, long numeric/hex value, burned into or associated with a storage device like a disk or {term}`LUN`, so the system can recognize that device reliably, regardless of which cable, port, or path it is attached through.

:::


(terms_X)=
## X

:::{glossary}

X.509
    X.509 is a standard format for public key certificates used in cryptography and network security. It is a digital certificate that binds a public key to an identity (like a website, person, or organization). X.509 is signed by a trusted {term}`Certificate Authority <CA>` to verify authenticity.

xhtml
Extensible HyperText Markup Language
    xhtml is a stricter HTML language. It reformulates HTML as XML by combining HTML elements with XML's strict syntax rules, so documents are well-formed, more consistent across browsers, and easier to process with XML tools.

XML
Extensible Markup Language
   XML is a markup language designed to store and transport data in a format that is both human and machine readable. Unlike HTML which focuses on displaying data, XML focuses on describing and structuring data.

:::


(terms_Y)=
## Y

:::{glossary}

YAML
YAML Ain't Markup Language
    YAML is a data serialization language used mainly for configuration files and structured data exchange between programmes. YAML represents data as key-value pairs, lists, and nested structures, using indentation instead of brackets or tags, to show hierarchy.

Yubikey
    A YubiKey is a physical security key made by Yubico that provides hardware-based authentication for securing access to computers, networks, and online services. It is a small USB device (about the size of a USB stick) that acts as a second factor for two-factor authentication (2FA) or multi-factor authentication (MFA).

:::


(terms_Z)=
## Z

:::{glossary}

zFCP
zSeries Fibre Channel Protocol
    zFCP is a Linux device driver that enables IBM Z mainframes (formerly System z) to access storage devices over a Fibre Channel network using the {term}`SCSI` protocol.

ZFS
Zettabyte File System
    ZFS is an advanced 64-bit file system that also includes its own built-in volume manager. It is designed for high-capacity and reliable storage. It is known for its strong data-integrity features, easy pooling of disks, and convenient features like snapshots, compression, and built in RAID (RAID-Z).

z/VM
    z/VM is IBM's virtualization operating system for their mainframe computers (IBM Z systems, formerly known as System z). z/VM is a hypervisor that allows multiple operating systems to run simultaneously on a single mainframe, effectively turning one physical machine into many virtual machines.
:::

