---
myst:
  html_meta:
    description: "Learn how to find and use Ubuntu cloud images for AWS, Azure, Google Cloud, and other cloud platforms."
---

(cloud-images)=
# Cloud images


Canonical produces a variety of cloud-specific images, which are available directly via the clouds themselves, as well as on [https://cloud-images.ubuntu.com](https://cloud-images.ubuntu.com).

For expanded documentation, please see the separate [public-cloud documentation.](https://documentation.ubuntu.com/public-cloud/)

## Public clouds

### Compute offerings

Users can find Ubuntu images for virtual machines and bare-metal offerings published directly to the following clouds:

* [Amazon Elastic Compute Cloud (EC2)](https://documentation.ubuntu.com/aws/aws-how-to/instances/find-ubuntu-images/)
* [Google Compute Engine (GCE)](https://documentation.ubuntu.com/gcp/google-how-to/gce/find-ubuntu-images/)
* [IBM Cloud](https://canonical-ibm.readthedocs-hosted.com/ibm-how-to/find-ubuntu-images/)
* [Microsoft Azure](https://documentation.ubuntu.com/azure/azure-how-to/instances/find-ubuntu-images/)
* [Oracle Cloud](https://documentation.ubuntu.com/oracle/oracle-how-to/find-ubuntu-images/)

### Container offerings

Ubuntu images are also produced for a number of container offerings:

* [Amazon Elastic Kubernetes Service (EKS)](https://cloud-images.ubuntu.com/docs/aws/eks/)
* Google Kubernetes Engine (GKE) works differently as it has no portfolio of images to start. For each [release of GKE](https://docs.cloud.google.com/kubernetes-engine/docs/release-schedule#schedule-for-release-channels) it will select the appropriate image.

## Private clouds

On [cloud-images.ubuntu.com](https://cloud-images.ubuntu.com), users can find standard and minimal images for the following:

* Hyper-V
* KVM
* OpenStack
* Vagrant
* VMware

## Release support

Cloud images are published and supported throughout the [lifecycle of an Ubuntu release](https://ubuntu.com/about/release-cycle). During this time images can receive all published security updates and bug fixes.

For users wanting to upgrade from one release to the next, the recommended path is to launch a new image with the desired release and then migrate any workload or data to the new image.

Some cloud image customization must be applied during image creation, which would be missing if an in-place upgrade were performed. For that reason, in-place upgrades of cloud images are not recommended.
