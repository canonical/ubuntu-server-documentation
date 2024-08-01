(openvpn-client-implementations)=
# OpenVPN client implementations


## Linux Network-Manager GUI for OpenVPN

Many Linux distributions (including Ubuntu Desktop variants) come with Network Manager; a GUI to configure your network settings. It also can manage your VPN connections. It is the default, but if in doubt make sure you have the `network-manager-openvpn` package installed.

- Open the Network Manager GUI, select the VPN tab and then the 'Add' button
- Select OpenVPN as the VPN type in the opening requester and press 'Create'
- In the next window, add the OpenVPN's server name as the 'Gateway'
  - Set 'Type' to 'Certificates (TLS)'
  - Point 'User Certificate' to your user certificate
  - Point 'CA Certificate' to your CA certificate
  - Point 'Private Key' to your private key file.
- Use the 'advanced' button to enable compression (e.g. `comp-lzo`), dev tap, or other special settings you want to set on the server. Now try to establish your VPN.

## OpenVPN with GUI for Mac OS X

[Tunnelblick](https://tunnelblick.net) is an excellent free, open source implementation of a GUI for OpenVPN for OS X. Download the latest OS X installer from there and install it.

It also is [recommended by upstream](https://openvpn.net/vpn-server-resources/connecting-to-access-server-with-macos/#alternative-openvpn-open-source-tunnelblick-program), which [has an alternative](https://openvpn.net/vpn-server-resources/installation-guide-for-openvpn-connect-client-on-macos/) of their own.

Then put your `client.ovpn` config file together with the certificates and keys in `/Users/username/Library/Application Support/Tunnelblick/Configurations/` and launch Tunnelblick from your 'Application' folder.

Instead of downloading manually, if you have brew set up on MacOS this is as easy as running:

`brew cask install tunnelblick`

## OpenVPN with GUI for Win

First, download and install the latest [OpenVPN Windows Installer](https://openvpn.net/community-downloads/). As of this writing, the management GUI is included with the Windows binary installer.

You need to start the OpenVPN service. Go to Start \> Computer \> Manage \> Services and Applications \> Services. Find the OpenVPN service and start it. Set its startup type to 'automatic'.

When you start the OpenVPN MI GUI the first time you need to run it as an administrator. You have to right click on it and you will see that option.

There is an [updated guide by the upstream](https://community.openvpn.net/openvpn/wiki/Easy_Windows_Guide) project for the client on Windows.

## Further reading

- See the [OpenVPN](http://openvpn.net/) website for additional information.

- [OpenVPN hardening security guide](http://openvpn.net/index.php/open-source/documentation/howto.html#security)

- Also, Packt's [OpenVPN: Building and Integrating Virtual Private Networks](http://www.packtpub.com/openvpn/book) is a good resource.
