---
myst:
  html_meta:
    description: Ubuntu Server explanation guides covering security, networking, virtualization, storage, performance, cryptography, and system concepts.
---

(explanation)=
# Ubuntu Server explanation guides

Our explanatory and conceptual guides are written to provide a better understanding of how Ubuntu Server works and how it can be used and configured. They enable you to expand your knowledge, making the operating system easier to use.

If you're not sure how or where to get started with a topic, each section has "introduction to" pages to give you a high-level overview and relevant links to help you navigate to the guides and other materials of most interest to you.

## Security

{ref}`Our security explanations <explanation-security>` include high-level overviews of security configuration and good practices, and discussion of key concepts in the following topics:

* **Authentication**, with introductions to Kerberos and SSSD
* **Cryptography** and cryptographic libraries
* **Virtual Private Networks (VPNs)** with introductions to WireGuard VPN and its related concepts

```{toctree}
:hidden:
:titlesonly:

security
```

## Networking

{ref}`Our networking section <explanation-networking>` will give you an introduction to networking and details on some of the key topics, such as:

* **Network tooling and configuration**
* **Network shares**

```{toctree}
:hidden:
:titlesonly:

networking
```

## Managing software

{ref}`Managing software <explanation-managing-software>` is an integral part of system maintenance. In this section we discuss the following topics in detail:

* **Software updates**, why updates are sometimes phased, and testing updates before they're released in your production environment
* **Third party repositories**
* **Changing package files**

```{toctree}
:hidden:
:titlesonly:

software
```

## Storage

{ref}`In data and storage <explanation-data-and-storage>` we discuss:

* **Managing data**
* **Storage and backups**

```{toctree}
:hidden:
:titlesonly:

data-and-storage
```

## Web services

Our {ref}`explanation-web-services` section includes details about web servers and how they work, as well as related topics like Squid proxy servers.

```{toctree}
:hidden:
:titlesonly:

web-services
```

## Virtualisation and containers

Our {ref}`Virtualisation and containers <explanation-virtualisation>` section includes overviews of the available virtualisation and container tooling in the Ubuntu space, as well as more detail about topics like rock images, Docker, eBPF and more!

```{toctree}
:hidden:
:titlesonly:

virtualisation
```

## Clouds

Our {ref}`clouds section <explanation-cloud-images>` provides details on finding cloud images for various public clouds, and about the popular cloud initialization tool, cloud-init.

```{toctree}
:hidden:
:titlesonly:

clouds
```

## High Availability

{ref}`High Availability <explanation-high-availability>` is a method for clustering resources to ensure minimal downtime if a particular component fails.

In this section we provide an introduction to High Availability and explain some of the key concepts.

```{toctree}
:hidden:
:titlesonly:

high-availability
```

## System tuning

{ref}`Our system tuning <explanation-system-tuning>` section provides details on system performance and optimization, covering concepts like Profile-Guided Optimization (PGO) and some common tooling.

```{toctree}
:hidden:
:titlesonly:

performance
```

## Debugging

{ref}`These debugging pages <explanation-debugging>` are for readers interested in packaging and Ubuntu development.

```{toctree}
:hidden:
:titlesonly:

debugging
```
