(samba-file-server)=
# Set up Samba as a file server

One of the most common ways to network Ubuntu and Windows computers is to configure Samba as a *file server*. It can be set up to share files with Windows clients, as we'll see in this section. 

The server will be configured to share files with any client on the network without prompting for a password. If your environment requires stricter Access Controls see [Share Access Control](share-access-controls.md).

```{warning}
If you use **Samba and authd** at the same time, you must specify user and group mapping. Otherwise, you will encounter permission issues due to mismatched user and group identifiers.

If you *are* using Samba with authd, you should follow the instructions in the [steps for the server](https://documentation.ubuntu.com/authd/en/latest/howto/use-with-samba/#steps-for-the-server) guide in the authd documentation instead.
```

## Install Samba

The first step is to install the `samba` package. From a terminal prompt enter:

```bash
sudo apt install samba
```

That's all there is to it; you are now ready to configure Samba to share files.

## Configure Samba as a file server

The main Samba configuration file is located in `/etc/samba/smb.conf`. The default configuration file contains a significant number of comments, which document various configuration directives.

> **Note**:
> Not all available options are included in the default configuration file. See the [`smb.conf` man page](https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html) or the [Samba HOWTO Collection](https://www.samba.org/samba/docs/old/Samba3-HOWTO/) for more details.

First, edit the `workgroup` parameter in the *\[global\]* section of `/etc/samba/smb.conf` and change it to better match your environment:

```text
workgroup = EXAMPLE
```

Create a new section at the bottom of the file, or uncomment one of the examples, for the directory you want to share:

```text
[share]
    comment = Ubuntu File Server Share
    path = /srv/samba/share
    browsable = yes
    guest ok = yes
    read only = no
    create mask = 0755
```

- **`comment`**
A short description of the share. Adjust to fit your needs.

- **`path`**
The path to the directory you want to share.
    
  > **Note**:
  > This example uses `/srv/samba/sharename` because, according to the {term}`Filesystem Hierarchy Standard (FHS) <FHS>`, [`/srv`](http://www.pathname.com/fhs/pub/fhs-2.3.html#SRVDATAFORSERVICESPROVIDEDBYSYSTEM) is where site-specific data should be served. Technically, Samba shares can be placed anywhere on the {term}`filesystem` as long as the permissions are correct, but adhering to standards is recommended.

- **`browsable`**
Enables Windows clients to browse the shared directory using Windows Explorer.

- **`guest ok`**
Allows clients to connect to the share without supplying a password.

- **`read only`** determines if the share is read only or if write privileges are granted. Write privileges are allowed only when the value is *no*, as is seen in this example. If the value is *yes*, then access to the share is read only.

- **`create mask`**
Determines the permissions that new files will have when created.

### Create the directory

Now that Samba is configured, the directory needs to be created and the permissions changed. From a terminal, run the following commands:

```bash
sudo mkdir -p /srv/samba/share
sudo chown nobody:nogroup /srv/samba/share/
```

The `-p` switch tells `mkdir` to create the entire directory tree if it doesn't already exist.

### Enable the new configuration

Finally, restart the Samba services to enable the new configuration by running the following command:

```bash
sudo systemctl restart smbd.service nmbd.service
```

> **Warning**:
> Once again, the above configuration gives full access to any client on the local network. For a more secure configuration see [Share Access Control](share-access-controls.md).

From a Windows client you should now be able to browse to the Ubuntu file server and see the shared directory. If your client doesn't show your share automatically, try to access your server by its IP address, e.g. `\\192.168.1.1`, in a Windows Explorer window. To check that everything is working try creating a directory from Windows.

To create additional shares simply create new `[sharename]` sections in `/etc/samba/smb.conf`, and restart Samba. Just make sure that the directory you want to share actually exists and the permissions are correct.

The file share named `[share]` and the path `/srv/samba/share` used in this example can be adjusted to fit your environment. It is a good idea to name a share after a directory on the file system. Another example would be a share name of `[qa]` with a path of `/srv/samba/qa`.

## Further reading

  - For in-depth Samba configurations see the [Samba how-to collection](https://www.samba.org/samba/docs/old/Samba3-HOWTO/)

  - The guide is also available [in printed format](http://www.amazon.com/exec/obidos/tg/detail/-/0131882228).

  - O'Reilly's [Using Samba](http://www.oreilly.com/catalog/9780596007690/) is another good reference.

  - The [Ubuntu Wiki Samba](https://help.ubuntu.com/community/Samba) page.
