(set-up-your-lma-stack)=
# [Logging

Distributed Replicated Block Device (DRBD) mirrors block devices between multiple hosts. The replication is transparent to other applications on the host systems. Any block device hard disks, partitions, RAID devices, logical volumes, etc can be mirrored.

## Install DRBD

To get started using DRBD, first install the necessary packages. In a terminal window, run the following command:

```bash
sudo apt install drbd-utils
```

> **Note**:
> If you are using the **virtual kernel** as part of a virtual machine you will need to manually compile the `drbd` module. It may be easier to install the `linux-modules-extra-$(uname -r)` package inside the virtual machine.

## Configure DRBD

This section covers setting up a DRBD to replicate a separate `/srv` partition, with an `ext3` filesystem between two hosts. The partition size is not particularly relevant, but both partitions need to be the same size.

The two hosts in this example will be called **`drbd01`** and **`drbd02`**. They will need to have name resolution configured either through DNS or the `/etc/hosts` file. See our [guide to DNS](domain-name-service-dns.md) for details.

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

> **Note**:
> There are many other options in `/etc/drbd.conf`, but for this example the default values are enough.

Now copy `/etc/drbd.conf` to the second host:

```bash
scp /etc/drbd.conf drbd02:~
```

And, on `drbd02`, move the file to `/etc`:

```bash
sudo mv drbd.conf /etc/
```

Now using the `drbdadm` utility, initialise the meta data storage. On both servers, run:

```bash
sudo drbdadm create-md r0
```

Next, on both hosts, start the `drbd` daemon:

```bash
sudo systemctl start drbd.service
```

On `drbd01` (or whichever host you wish to be the primary), enter the following:

```bash
sudo drbdadm -- --overwrite-data-of-peer primary all
```

After running the above command, the data will start syncing with the secondary host. To watch the progress, on `drbd02` enter the following:

```bash
watch -n1 cat /proc/drbd
```

To stop watching the output press <kbd>Ctrl</kbd> + <kbd>C</kbd>.

Finally, add a filesystem to `/dev/drbd0` and mount it:

```bash
sudo mkfs.ext3 /dev/drbd0
sudo mount /dev/drbd0 /srv
```

## Testing

To test that the data is actually syncing between the hosts copy some files on `drbd01`, the primary, to `/srv`:

```bash
sudo cp -r /etc/default /srv
```

Next, unmount `/srv`:

```bash
sudo umount /srv
```

Now demote the **primary** server to the **secondary** role:

```bash
sudo drbdadm secondary r0
```

Now on the **secondary** server, promote it to the **primary** role:

```bash
sudo drbdadm primary r0
```

Lastly, mount the partition:

```bash
sudo mount /dev/drbd0 /srv
```

Using `ls` you should see `/srv/default` copied from the former primary host `drbd01`.

## Further reading

- For more information on DRBD see the [DRBD web site](http://www.drbd.org/).

- The [drbd.conf manpage](http://manpages.ubuntu.com/manpages/en/man5/drbd.conf.5.html) contains details on the options not covered in this guide.

- Also, see the [drbdadm manpage](http://manpages.ubuntu.com/manpages/en/man8/drbdadm.8.html).
