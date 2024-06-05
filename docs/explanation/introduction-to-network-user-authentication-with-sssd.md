(introduction-to-network-user-authentication-with-sssd)=
# Introduction to network user authentication with SSSD

The [System Security Services Daemon (SSSD)](https://sssd.io/) is actually a collection of daemons that handle authentication, authorisation, and user and group information from a variety of network sources. It's a useful tool for administrators of Linux and UNIX-based systems, particularly in enterprise systems which may need to integrate with other directory, access control and authentication services. 

## Common deployment scenarios

At its core, SSSD has support for a variety of authorisation and identity services, such as Active Directory, LDAP, and Kerberos. See the following guides to discover how to set up SSSD with...

- [Active Directory](../how-to/how-to-set-up-sssd-with-active-directory.md)
- [LDAP](../how-to/how-to-set-up-sssd-with-ldap.md)
- [LDAP and Kerberos](../how-to/how-to-set-up-sssd-with-ldap-and-kerberos.md)

## Integration with PAM and NSS

SSSD provides Pluggable Authentication Modules (PAM) and Name Service Switch (NSS) modules to integrate these remote sources into your system. This allows remote users to login and be recognised as valid users, including group membership. To allow for disconnected operation, SSSD also can also cache this information, so that users can continue to login in the event of a network failure, or other problems of the same sort.

## Troubleshooting

If you have problems with your SSSD setup, you can use some of the tips contained in our [SSSD troubleshooting guide](../how-to/troubleshooting-sssd.md) to discover the cause.
