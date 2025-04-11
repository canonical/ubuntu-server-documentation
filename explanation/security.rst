.. _explanation-security:

Security
*********

There are many steps you can take to strengthen the security posture of your
system. In this section you will find explanations of various concepts related
to security.

* :ref:`security-suggestions` provides general recommendations for any
  Ubuntu system, from straightforward setups to more advanced and complex
  systems.

**Authentication**

* :ref:`About DNSSEC <dnssec>`, the security extension for the Domain Name
  System (DNS).

**Cryptography**

* :ref:`Certificates <certificates>` are issued, stored and signed by a
  Certificate Authority (CA) to create trusted connections.
* :ref:`Our cryptography section <explanation-cryptography>` explains more
  about the different cryptographic libraries and configurations you might
  encounter.

**Virtual Private Network (VPN)**

VPNs are commonly used to provide encrypted, secure access to a network. 

* :ref:`OpenVPN clients <openvpn-client-implementations>` provides a list of
  client implementations that can be used with a GUI across platforms.

**See also**

How-to: :ref:`how-to-security`

.. toctree::
    :hidden:

    security/security_suggestions
    Certificates <security/certificates>
    DNSSEC <dnssec/dnssec>
    cryptography
    OpenVPN clients <security/openvpn-client-implementations>

