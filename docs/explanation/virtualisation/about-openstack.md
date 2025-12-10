---
myst:
  html_meta:
    description: "Understand OpenStack cloud computing platform and its integration with Ubuntu Server for building private and public clouds."
---

(about-openstack)=
# About OpenStack

OpenStack is the most popular open source cloud computing platform that enables the management of distributed compute, network and storage resources in the data center.

While the reference virtualisation stack (consisting of {ref}`QEMU/KVM <qemu>` and {ref}`libvirt <libvirt>`) enables hardware virtualisation and the management of virtual machines (VMs) on a single host, in most cases the computing, network and storage resources are distributed across multiple hosts in the data center.

This creates an obvious challenge with centralised management of those resources, scheduling VMs, etc. OpenStack solves this problem by aggregating distributed pools of resources, allocating them to VMs on-demand and enabling automated VM provisioning through a self-service portal.

OpenStack consists of the following primary components:

* **Keystone**:
   Serves as an identity service, providing authentication and authorisation functions for the users and enabling multi-tenancy.

* **Glance**: 
   This is an image service, responsible for uploading, managing and retrieving cloud images for VMs running on OpenStack.

* **Nova**:
   This is the primary compute engine of OpenStack, responsible for VM scheduling, creation and termination.

* **Neutron**:
   Provides network connectivity between VMs, enabling multi-VM deployments.

* **Cinder**:
   This is a storage component that is responsible for provisioning, management and termination of persistent block devices.

* **Swift**:
   This is another storage component that provides a highly available and scalable object storage service.

There are also many other OpenStack components and supporting services available in the OpenStack ecosystem, enabling more advanced functions, such as load balancing, secrets management, etc.

## OpenStack installation

The most straightforward way to get started with OpenStack on Ubuntu is to use [MicroStack](https://microstack.run/docs/single-node) since the entire installation process requires only 2 commands and takes around 20 minutes.

Apart from MicroStack, multiple different installation methods for OpenStack on Ubuntu are available. These include:

* [OpenStack Charms](https://docs.openstack.org/project-deploy-guide/charm-deployment-guide/latest/)

* [OpenStack Ansible](https://docs.openstack.org/project-deploy-guide/openstack-ansible/latest/)

* [Manual Installation](https://docs.openstack.org/install-guide/)

* [DevStack](https://docs.openstack.org/devstack/latest/)
