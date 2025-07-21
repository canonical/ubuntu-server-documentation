.. _how-to-security:

Security
********

While a fresh Ubuntu installation is usually safe for immediate use, there are
some additional steps you can take to introduce a layered approach to your
system's security. If you are new to Ubuntu, you may want to refer to our
:ref:`Introduction to security <introduction-to-security>` first for a general
overview.

General configuration
=====================

* :ref:`Users and groups management <user-management>` for setting up user
  accounts, permissions and password policies
* :ref:`Firewalls <firewalls>` are recommended for network security
* :ref:`AppArmor <apparmor>` limits permissions and access for the software
  running on your system
* :ref:`Console security <console-security>` for an additional physical
  security barrier

.. toctree::
   :hidden:

   User management <security/user-management>
   Firewalls <security/firewalls>
   AppArmor <security/apparmor>
   Console security <security/console-security>

Authentication
==============

These tools are particularly useful for more advanced or complex setups.

* :ref:`how-to-kerberos` is a network authentication protocol providing
  identity verification for distributed systems
* :ref:`how-to-network-user-authentication-with-sssd` handles authentication,
  user/group information and authorisation from disparate network sources
* :ref:`Smart card authentication <smart-card-authentication>` provides a
  physical authentication method

.. toctree::
   :hidden:

   kerberos.rst
   sssd.rst
   Smart cards <security/smart-card-authentication>

Cryptography
============

The Secure Shell (SSH) cryptographic protocol that provides secure channels on
an unsecured network. In Ubuntu, OpenSSH is the most commonly used
implementation of SSH. It provides a suite of utilities for encrypting data
transfers and can also be used for remote login and authentication.

.. toctree::
   :titlesonly:

   OpenSSH <security/openssh-server>
   Install a root CA certificate <security/install-a-root-ca-certificate-in-the-trust-store>

Virtual Private Network (VPN)
=============================

VPNs are commonly used to provide encrypted, secure access to a network. Two
of the most popular choices in Ubuntu are OpenVPN and WireGuard VPN.
 
* :ref:`OpenVPN <install-openvpn>` is a well-established option that supports
  many platforms besides Linux
* :ref:`how-to-wireguard-vpn` is a modern and performant option that removes a
  lot of the complexity from configuring a VPN

.. toctree::
    :hidden:

    OpenVPN <security/install-openvpn>
    wireguard-vpn

See also
========

* Explanation: :ref:`Introduction to security <introduction-to-security>`
* Explanation: :ref:`Security topics <explanation-security>`

