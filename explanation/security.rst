.. _explanation-security:

Security
*********

There are many steps you can take to strengthen the security posture of your
system. In this section you will find explanations of various concepts related
to security.

General configuration
=====================

* :ref:`Introduction to security <introduction-to-security>` for a high-level
  overview of security in Ubuntu
* :ref:`security-suggestions` provides general recommendations for any
  Ubuntu system, from straightforward setups to more advanced and complex
  systems

.. toctree::
   :hidden:

   intro-to/security
   security/security_suggestions

Authentication
==============

* :ref:`Introduction to Kerberos <introduction-to-kerberos>`, the network
  authentication system
* :ref:`Introduction to SSSD <introduction-to-network-user-authentication-with-sssd>`,
  the collection of daemons that handle authentication from various network sources
* :ref:`About DNSSEC <dnssec>`, the security extension for the Domain Name
  System (DNS).

.. toctree::
   :hidden:

   intro-to/kerberos
   intro-to/sssd
   DNSSEC <dnssec/dnssec>

Cryptography
============

* :ref:`Our cryptography section <explanation-cryptography>` explains in detail
  about the different cryptographic libraries and configurations you might
  encounter.
* :ref:`Certificates <certificates>` are issued, stored and signed by a
  Certificate Authority (CA) to create trusted connections.

.. toctree::
   :hidden:

   cryptography
   Certificates <security/certificates>

Virtual Private Network (VPN)
=============================

VPNs are commonly used to provide encrypted, secure access to a network. 

* :ref:`Introduction to WireGuard VPN <introduction-to-wireguard-vpn>`, a
  popular and modern VPN implementation
* :ref:`OpenVPN clients <openvpn-client-implementations>` provides a list of
  client implementations that can be used with a GUI across platforms.

.. toctree::
   :hidden:

   intro-to/wireguard-vpn
   OpenVPN clients <security/openvpn-client-implementations>

See also
========

How-to: :ref:`how-to-security`



