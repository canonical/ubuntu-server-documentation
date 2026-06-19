---
myst:
  html_meta:
    description: Install and configure DRBD (Distributed Replicated Block Device) for transparent block device mirroring between multiple Ubuntu hosts.
---

(install-drbd)=
# Distributed Replicated Block Device (DRBD)

Distributed Replicated Block Device (DRBD) mirrors block devices between multiple hosts. The replication is transparent to other applications on the host systems. Any block device hard disks, partitions, RAID devices, logical volumes, etc can be mirrored.

## Install DRBD

To get started using DRBD, first install the necessary packages. In a terminal window, run the following command:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo apt install drbd-utils
```

:::{note}
If you are using the **virtual kernel** as part of a virtual machine you will need to manually compile the `drbd` module. It may be easier to install the `linux-modules-extra-$(uname -r)` package inside the virtual machine.
:::

## Configure DRBD

This section covers setting up a DRBD to replicate a separate `/srv` partition, with an `ext3` {term}`filesystem` between two hosts. The partition size is not particularly relevant, but both partitions need to be the same size.

The two hosts in this example will be called **`drbd01`** and **`drbd02`**. They will need to have name resolution configured either through {term}`DNS` or the `/etc/hosts` file. See our {ref}`guide to DNS <install-dns>` for details.

On the first host, edit `/etc/drbd.conf` as follows:

```
global { usage-count no; }
common { syncer { rate 100M; } }
resource r0 {
        protocol C;
        startup {
                wfc-timeout  15;
                degr-wfc-timeout 60;
        }
        net {
                cram-hmac-alg sha1;
                shared-secret "secret";
        }
        on drbd01 {
                device /dev/drbd0;
                disk /dev/sdb1;
                address 192.168.0.1:7788;
                meta-disk internal;
        }
        on drbd02 {
                device /dev/drbd0;
                disk /dev/sdb1;
                address 192.168.0.2:7788;
                meta-disk internal;
        }
} 
```

:::{note}
There are many other options in `/etc/drbd.conf`, but for this example the default values are enough.
:::

Now copy `/etc/drbd.conf` to the second host:

```{terminal}
:copy:
:user:
:host:
:dir:
scp /etc/drbd.conf drbd02:~
```

And, on `drbd02`, move the file to `/etc`:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo mv drbd.conf /etc/
```

Now using the `drbdadm` utility, initialize the meta data storage. On both servers, run:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo drbdadm create-md r0
```

Next, on both hosts, start the `drbd` daemon:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo systemctl start drbd.service
```

On `drbd01` (or whichever host you wish to be the primary), enter the following:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo drbdadm -- --overwrite-data-of-peer primary all
```

After running the above command, the data will start syncing with the secondary host. To watch the progress, on `drbd02` enter the following:

```{terminal}
:copy:
:user:
:host:
:dir:
watch -n1 cat /proc/drbd
```

To stop watching the output press {kbd}`Ctrl` + {kbd}`C`.

Finally, add a filesystem to `/dev/drbd0` and mount it:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo mkfs.ext3 /dev/drbd0
```
```{terminal}
:copy:
:user:
:host:
:dir:
sudo mount /dev/drbd0 /srv
```

## Testing

To test that the data is actually syncing between the hosts copy some files on `drbd01`, the primary, to `/srv`:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo cp -r /etc/default /srv
```

Next, unmount `/srv`:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo umount /srv
```

Now demote the **primary** server to the **secondary** role:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo drbdadm secondary r0
```

Now on the **secondary** server, promote it to the **primary** role:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo drbdadm primary r0
```

Lastly, mount the partition:

```{terminal}
:copy:
:user:
:host:
:dir:
sudo mount /dev/drbd0 /srv
```

Using `ls` you should see `/srv/default` copied from the former primary host `drbd01`.

## Further reading

- For more information on DRBD see the [DRBD web site](https://linbit.com/linbit-software-download-page-for-linstor-and-drbd-linux-driver/).

- The {manpage}`drbd.conf(5)` manual page contains details on the options not covered in this guide.

- Also, see the {manpage}`drbdadm(8)` manual page.
