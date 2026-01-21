---
myst:
  html_meta:
    description: "Explore container tools available on Ubuntu Server, including Docker, LXD, and other containerisation technologies."
---

(container-tools-in-the-ubuntu-space)=
# Container tools in the Ubuntu space

Let's take a look at some of the most commonly used tools and technologies available in the Ubuntu container space.

## LXC

**Container type**: System containers

[Linux Containers, or LXC](https://linuxcontainers.org/) (pronounced "lex-see"), is a program that creates and administers containers on your local system. It is the foundation of several other system container technologies and provides both an API (to allow higher-level managers like LXD to administer containers), and an interface through which the user can interact with kernel containment features (often called the "userspace interface"). LXC interacts directly with the kernel to isolate processes, resources, etc, and provides the necessary tools - and a container runtime - for creating and managing system containers.

To get started with LXC containers, check out the [LXC Introduction](https://linuxcontainers.org/lxc/introduction/) and [LXC Getting started](https://linuxcontainers.org/lxc/getting-started/) pages.

## LXD

**Container type**: System containers

The [Linux Containers Daemon, or LXD](https://canonical.com/lxd) (pronounced "lex-dee") is the lightervisor, or lightweight container hypervisor. It is a system container management tool built on top of LXC. Since it is an abstraction layer away from LXC it offers a more user-friendly interface, including both a REST API and a command-line interface. The LXD API deals with "remotes", which serve images and containers. In fact, it comes with a built-in image store, so that containers can be created more quickly. 

To get started with LXD from an Ubuntu Server administrator's point of view, check out our {ref}`how to get started with LXD <lxd-containers>` guide. For a more general beginner's introduction to LXD, we [recommend this tutorial](https://documentation.ubuntu.com/lxd/latest/tutorial/) from the LXD team.

In addition to creating and managing containers, LXD can also be [used to create virtual machines](https://documentation.ubuntu.com/lxd/latest/howto/instances_create/#create-a-virtual-machine).

## Docker

**Container type**: Application containers

Docker is one of the most popular containerization platforms, which allows developers to package applications - together with their dependencies - into lightweight containers. This provides a consistently reproducible environment for deploying applications, which makes it easy to build, ship, and run them even in different environments. Docker includes a command-line interface and a daemon to create and manage containers.

Although Docker is widely used by developers, it can also be used by system administrators to manage resources and applications. For instance, by encapsulating applications (and their libraries and dependencies) in a single package, and providing version control, deployment of software and updates can be simplified. It also helps to optimize resource use - particularly through its alignment with microservices architecture.

To get started with Docker from a system administrator's point of view, check out our {ref}`Docker guide for sysadmins <docker-for-system-admins>`.
