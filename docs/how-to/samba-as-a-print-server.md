(samba-as-a-print-server)=
# Samba as a print server

Another common way to network Ubuntu and Windows computers is to configure Samba as a *print server*. This will allow it to share printers installed on an Ubuntu server, whether locally or over the network.

Just as we did in [using Samba as a file server](https://ubuntu.com/server/docs/samba-file-server), this section will configure Samba to allow any client on the local network to use the installed printers without prompting for a username and password.

If your environment requires stricter Access Controls see [Share Access Control](https://ubuntu.com/server/docs/samba-share-access-control).

## Install and configure CUPS

Before installing and configuring Samba as a print server, it is best to already have a working CUPS installation. See [our guide on CUPS](https://ubuntu.com/server/docs/service-cups) for details.

## Install Samba

To install the `samba` package, run the following command in your terminal:

```bash
sudo apt install samba
```

## Configure Samba

After installing `samba`, edit `/etc/samba/smb.conf`. Change the *workgroup* attribute to what is appropriate for your network:

```text
workgroup = EXAMPLE
```

In the *\[printers\]* section, change the *guest ok* option to 'yes':

```text 
browsable = yes
guest ok = yes
```

After editing `smb.conf`, restart Samba:

```bash
sudo systemctl restart smbd.service nmbd.service
```

The default Samba configuration will automatically share any printers installed. Now all you need to do is install the printer locally on your Windows clients.

## Further reading

  - For in-depth Samba configurations see the [Samba HOWTO Collection](http://samba.org/samba/docs/man/Samba-HOWTO-Collection/).

  - The guide is also available in [printed format](http://www.amazon.com/exec/obidos/tg/detail/-/0131882228).

  - O'Reilly's [Using Samba](http://www.oreilly.com/catalog/9780596007690/) is another good reference.

  - Also, see the [CUPS Website](http://www.cups.org/) for more information on configuring CUPS.

  - The [Ubuntu Wiki Samba](https://help.ubuntu.com/community/Samba) page.
