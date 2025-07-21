.. _explanation-cloud-images:

Clouds
******

Clouds are networks of remote servers providing services via the internet. They
have become a popular way to manage storage, software and processing without
the need to host physical servers yourself.

Cloud-init
==========

Cloud-init is the industry standard tool for provisioning clouds and is
supported by most cloud providers. Here we provide a high-level introduction to
the tool.

.. toctree::
   :titlesonly:

   About cloud-init <intro-to/cloud-init>

Cloud images
============

Whichever cloud you use, you will need to use images compatible with that
cloud. We call these **cloud images**.

* :ref:`Cloud images overview <cloud-images>` provides a high level
  introduction to the concept, along with links to the official sources of
  cloud images.

For information related to public clouds in Ubuntu, you may also want to refer
to the official
`Public Cloud documentation <https://documentation.ubuntu.com/public-cloud/en/latest/>`_.

For ease of reference, these links in the Public Cloud documentation will take
you to the cloud images for:

* `Amazon EC2`_ | `Google Compute Engine (GCE)`_ | `Microsoft Azure`_

.. toctree::
   :hidden:

   Cloud images <clouds/find-cloud-images>



.. LINKS
.. _Amazon EC2: https://canonical-aws.readthedocs-hosted.com/en/latest/aws-how-to/instances/find-ubuntu-images/
.. _Google Compute Engine (GCE): https://canonical-gcp.readthedocs-hosted.com/en/latest/google-how-to/gce/find-ubuntu-images/
.. _Microsoft Azure: https://canonical-azure.readthedocs-hosted.com/en/latest/azure-how-to/instances/find-ubuntu-images/

