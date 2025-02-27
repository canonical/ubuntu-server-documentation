(cloud-images)=
# Cloud images


Canonical produces a variety of cloud-specific images, which are available directly via the clouds themselves, as well as on [https://cloud-images.ubuntu.com](https://cloud-images.ubuntu.com).

For expanded documentation, please see the separate [public-cloud documentation.](https://documentation.ubuntu.com/public-cloud/en/latest/)

## Public clouds

### Compute offerings

Users can find Ubuntu images for virtual machines and bare-metal offerings published directly to the following clouds:

* [Amazon Elastic Compute Cloud (EC2)](https://canonical-aws.readthedocs-hosted.com/en/latest/aws-how-to/instances/find-ubuntu-images/)
* [Google Compute Engine (GCE)](https://canonical-gcp.readthedocs-hosted.com/en/latest/google-how-to/gce/find-ubuntu-images/)
* IBM Cloud
* [Microsoft Azure](https://canonical-azure.readthedocs-hosted.com/en/latest/azure-how-to/instances/find-ubuntu-images/)
* Oracle Cloud

### Container offerings

Ubuntu images are also produced for a number of container offerings:

* [Amazon Elastic Kubernetes Service (EKS)](https://cloud-images.ubuntu.com/docs/aws/eks/)
* {term}`Google Kubernetes Engine (GKE) <GKE>`

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

Some cloud image customisation must be applied during image creation, which would be missing if an in-place upgrade were performed. For that reason, in-place upgrades of cloud images are not recommended.
