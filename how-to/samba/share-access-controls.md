(share-access-controls)=
# Share access controls


There are several options available to control access for each individual shared directory. Using the *\[share\]* example, this section will cover some common options.

## Groups

*Groups* define a collection of users who have a common level of access to particular network resources. This provides granularity in controlling access to such resources. For example, let's consider a group called "qa" is defined to contain the users *Freda*, *Danika*, and *Rob*,  and then a group called "support" is created containing the users *Danika*, *Jeremy*, and *Vincent*. Any network resources configured to allow access by the "qa" group will be available to Freda, Danika, and Rob, but not Jeremy or Vincent. Danika can access resources available to both groups since she belongs to both the "qa" and "support" groups. All other users only have access to resources explicitly allowed to the group they are part of.

When mentioning groups in the Samba configuration file, `/etc/samba/smb.conf`, the recognized syntax is to preface the group name with an "@" symbol. For example, if you wished to use a group named *sysadmin* in a certain section of the `/etc/samba/smb.conf`, you would do so by entering the group name as `@sysadmin`. If a group name has a space in it, use double quotes, like `"@LTS Releases"`.

## Read and write permissions

Read and write permissions define the explicit rights a computer or user has to a particular share. Such permissions may be defined by editing the `/etc/samba/smb.conf` file and specifying the explicit permissions inside a share.

For example, if you have defined a Samba share called *share* and wish to give read-only permissions to the group of users known as "qa", but wanted to allow writing to the share by the group called "sysadmin" *and* the user named "vincent", then you could edit the `/etc/samba/smb.conf` file and add the following entries under the *\[share\]* entry:

```text 
read list = @qa
write list = @sysadmin, vincent
```

Another possible Samba permission is to declare *administrative* permissions to a particular shared resource. Users having administrative permissions may read, write, or modify any information contained in the resource the user has been given explicit administrative permissions to.

For example, if you wanted to give the user *Melissa* administrative permissions to the *share* example, you would edit the `/etc/samba/smb.conf` file, and add the following line under the *\[share\]* entry:

```text 
admin users = melissa
```

After editing `/etc/samba/smb.conf`, reload Samba for the changes to take effect by running the following command:

```bash
sudo smbcontrol smbd reload-config
```

## Filesystem permissions

Now that Samba has been configured to limit which groups have access to the shared directory, the {term}`filesystem` permissions need to be checked.

Traditional Linux file permissions do not map well to Windows NT Access Control Lists ({term}`ACL`s). Fortunately POSIX ACLs are available on Ubuntu servers, which provides more fine-grained control. For example, to enable ACLs on `/srv` in an EXT3 filesystem, edit `/etc/fstab` and add the *acl* option:

```text
UUID=66bcdd2e-8861-4fb0-b7e4-e61c569fe17d /srv  ext3    noatime,relatime,acl 0       1
```

Then remount the partition:

```bash
sudo mount -v -o remount /srv
```

> **Note**:
> This example assumes `/srv` is on a separate partition. If `/srv`, or wherever you have configured your share path, is part of the `/` partition then a reboot may be required.

To match the Samba configuration above, the "sysadmin" group will be given read, write, and execute permissions to `/srv/samba/share`, the "qa" group will be given read and execute permissions, and the files will be owned by the username "Melissa". Enter the following in a terminal:

```bash
sudo chown -R melissa /srv/samba/share/
sudo chgrp -R sysadmin /srv/samba/share/
sudo setfacl -R -m g:qa:rx /srv/samba/share/
```

> **Note**:
> The `setfacl` command above gives *execute* permissions to all files in the `/srv/samba/share` directory, which you may or may not want.

Now from a Windows client you should notice the new file permissions are implemented. See [the `acl`](https://manpages.ubuntu.com/manpages/trusty/man5/acl.5.html) and [`setfacl`](https://manpages.ubuntu.com/manpages/trusty/man1/setfacl.1.html) man pages for more information on POSIX ACLs.

## Further reading

  - For in-depth Samba configurations see the [Samba HOWTO Collection](https://www.samba.org/samba/docs/old/Samba3-HOWTO/).

  - The guide is also available in [printed format](http://www.amazon.com/exec/obidos/tg/detail/-/0131882228).

  - O'Reilly's [Using Samba](http://www.oreilly.com/catalog/9780596007690/) is also a good reference.

  - [Chapter 18](https://www.samba.org/samba/docs/old/Samba3-HOWTO/securing-samba.html) of the Samba HOWTO Collection is devoted to security.

  - For more information on Samba and ACLs see the [Samba ACLs page](https://www.samba.org/samba/docs/old/Samba3-HOWTO/AccessControls.html).

  - The [Ubuntu Wiki Samba](https://help.ubuntu.com/community/Samba) page.
