.. _how-to-server-installation:

Server installation
********************

This list of installation guides contains installation instructions for
architecture-specific and more advanced setups. Select your preferred
architecture to see which guides are available.

.. tab-set::

   .. tab-item:: **amd64**

      * :ref:`Netboot install <how-to-netboot-the-server-installer-on-amd64>`

   .. tab-item:: **arm64**

      * :ref:`Netboot install <netboot-the-server-installer-via-uefi-pxe-on-arm-aarch64-arm64-and-x86-64-amd64>`
      * :ref:`Choose between the arm64 and arm64+largemem installer options <choosing-between-the-arm64-and-arm64-largemem-installer-options>`

   .. tab-item:: **ppc64el**

      * :ref:`Netboot install <netboot-the-live-server-installer-on-ibm-power-ppc64el-with-petitboot>`
      * :ref:`Virtual CD-ROM and Petitboot install <how-to-start-a-live-server-installation-on-ibm-power-ppc64el-with-a-virtual-cd-rom-and-petitboot>`

   .. tab-item:: **s390x**

      * :ref:`Install via z/VM <interactive-live-server-installation-on-ibm-z-vm-s390x>`
      * :ref:`Non-interactive IBM z/VM autoinstall <non-interactive-ibm-z-vm-autoinstall-s390x>`
      * :ref:`Install via LPAR <interactive-live-server-installation-on-ibm-z-lpar-s390x>`
      * :ref:`Non-interactive IBM Z LPAR autoinstall <non-interactive-ibm-z-lpar-autoinstall-s390x>`

If you are new to Ubuntu, we recommend our
:ref:`basic installation <basic-installation>` tutorial to get you started
instead.

**Automatic install**

The Ubuntu Installer has its own documentation for automatic (or "hands off")
installations. These guides from the Ubuntu Installer documentation are
available for automatic installations.

* `Introduction to Automated Server installer`_
* `Autoinstall quickstart`_
* `Autoinstall quickstart on s390x`_

**See also**

Reference: :ref:`System requirements <system-requirements>`

.. LINKS
.. _Introduction to Automated Server installer: https://canonical-subiquity.readthedocs-hosted.com/en/latest/intro-to-autoinstall.html
.. _Autoinstall quickstart: https://canonical-subiquity.readthedocs-hosted.com/en/latest/howto/autoinstall-quickstart.html
.. _Autoinstall quickstart on s390x: https://canonical-subiquity.readthedocs-hosted.com/en/latest/howto/autoinstall-quickstart-s390x.html

.. toctree::
    :hidden:

    amd64 netboot install <installation/how-to-netboot-the-server-installer-on-amd64>
    arm64 netboot install <installation/netboot-the-server-installer-via-uefi-pxe-on-arm-aarch64-arm64-and-x86-64-amd64>
    Choose between the arm64 and arm64+largemem installer options <installation/choosing-between-the-arm64-and-arm64-largemem-installer-options>
    ppc64el netboot install <installation/netboot-the-live-server-installer-on-ibm-power-ppc64el-with-petitboot>
    Virtual CD-ROM and Petitboot install on ppc64el <installation/how-to-start-a-live-server-installation-on-ibm-power-ppc64el-with-a-virtual-cd-rom-and-petitboot>
    s390x install via z/VM <installation/interactive-live-server-installation-on-ibm-z-vm-s390x>
    Non-interactive IBM z/VM autoinstall (s390x) <installation/non-interactive-ibm-z-vm-autoinstall-s390x>
    s390x install via LPAR <installation/interactive-live-server-installation-on-ibm-z-lpar-s390x>
    Non-interactive IBM Z LPAR autoinstall (s390x) <installation/non-interactive-ibm-z-lpar-autoinstall-s390x>
