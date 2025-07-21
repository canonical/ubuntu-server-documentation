(install-rsnapshot)=
# How to install and configure rsnapshot

[rsnapshot](https://rsnapshot.org/) is an rsync-based {term}`filesystem` snapshot utility. It can take incremental backups of local and remote filesystems for any number of machines. rsnapshot makes extensive use of hard links, so disk space is only used when absolutely necessary. It leverages the power of rsync to create scheduled, incremental backups.

## Install rsnapshot

To install `rsnapshot` open a terminal shell and run:

```bash
sudo apt-get install rsnapshot
```

If you want to backup a remote filesystem, the rsnapshot server needs to be able to access the target machine over SSH without password. For more information on how to enable this please see {ref}`OpenSSH documentation <openssh-server>`. If the backup target is a local filesystem there is no need to set up OpenSSH.
 
## Configure rsnapshot

The `rsnapshot` configuration resides in `/etc/rsnapshot.conf`. Below you can find some of the options available there.

The root directory where all snapshots will be stored is found at:

```bash
snapshot_root       /var/cache/rsnapshot/
```

### Number of backups to keep

Since `rsnapshot` uses incremental backups, we can afford to keep older backups for a while before removing them. You set these up under the `BACKUP LEVELS / INTERVALS` section. You can tell `rsnapshot` to retain a specific number of backups of each kind of interval. 

```bash
retain  daily   6
retain  weekly    7
retain  monthly   4
```

In this example we will keep 6 snapshots of our daily strategy, 7 snapshots of our weekly strategy, and 4 snapshots of our monthly strategy. These data will guide the rotation made by `rsnapshot`.

### Remote machine access

If you are accessing a remote machine over SSH and the port to bind is not the default (port `22`), you need to set the following variable with the port number:

```bash
ssh_args       -p 22222
```

### What to backup

Now the most important part; you need to decide what you would like to backup.

If you are backing up locally to the same machine, this is as easy as specifying the directories that you want to save and following it with `localhost/` which will be a sub-directory in the `snapshot_root` that you set up earlier.

```bash
backup  /home/          localhost/
backup  /etc/           localhost/
backup  /usr/local/     localhost/
```

If you are backing up a remote machine you just need to tell `rsnapshot` where the server is and which directories you would like to back up.

```bash
backup root@example.com:/home/ example.com/    +rsync_long_args=--bwlimit=16,exclude=core
backup root@example.com:/etc/  example.com/    exclude=mtab,exclude=core
```

As you can see, you can pass extra rsync parameters (the `+` appends the parameter to the default list -- if you remove the `+` sign you override it) and also exclude directories.

You can check the comments in `/etc/rsnapshot.conf` and the {manpage}`rsnapshot(1)` manual page for more options.

## Test configuration

After modifying the configuration file, it is good practice to check if the syntax is OK:

```bash
sudo rsnapshot configtest
```

You can also test your backup levels with the following command:

```bash
sudo rsnapshot -t daily
```

If you are happy with the output and want to see it in action you can run:

```bash
sudo rsnapshot daily
```

## Scheduling backups

With `rsnapshot` working correctly with the current configuration, the only thing left to do is schedule it to run at certain intervals. We will use cron to make this happen since `rsnapshot` includes a default cron file in `/etc/cron.d/rsnapshot`. If you open this file there are some entries commented out as reference.

```text
0 4  * * *           root    /usr/bin/rsnapshot daily
0 3  * * 1           root    /usr/bin/rsnapshot weekly
0 2  1 * *           root    /usr/bin/rsnapshot monthly
```

The settings above added to `/etc/cron.d/rsnapshot` run:

 * The **daily snapshot** everyday at 4:00 am
 * The **weekly snapshot** every Monday at 3:00 am
 * The **monthly snapshot** on the first of every month at 2:00 am

For more information on how to schedule a backup using cron please take a look at the `Executing with cron` section in {ref}`Backups - Shell Scripts <back-up-using-shell-scripts>`.

### Further reading

* [rsnapshot offical web page](https://rsnapshot.org/)
* {manpage}`rsnapshot(1)` manual page
* {manpage}`rsync(1)` manual page
