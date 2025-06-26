(back-up-using-shell-scripts)=
# How to back up using shell scripts

In general, a shell script configures which directories to backup, and passes those directories as arguments to the `tar` utility, which creates an archive file. The archive file can then be moved or copied to another location. The archive can also be created on a remote file system such as a {ref}`Network File System (NFS) <install-nfs>` mount.

The `tar` utility creates one archive file out of many files or directories. `tar` can also filter the files through compression utilities, thus reducing the size of the archive file.

In this guide, we will walk through how to use a shell script for backing up files, and how to restore files from the archive we create.
 
## The shell script

The following shell script uses `tar` to create an archive file on a remotely mounted NFS file system. The archive filename is determined using additional command line utilities. For more details about the script, check out the `basic backup shell script <https://discourse.ubuntu.com/t/basic-backup-shell-script/36419>`_.

```sh
#!/bin/bash
####################################
#
# Backup to NFS mount script.
#
####################################
    
# What to backup. 
backup_files="/home /var/spool/mail /etc /root /boot /opt"
    
# Where to backup to.
dest="/mnt/backup"
    
# Create archive filename.
day=$(date +%A)
hostname=$(hostname -s)
archive_file="$hostname-$day.tgz"
    
# Print start status message.
echo "Backing up $backup_files to $dest/$archive_file"
date
echo
    
# Backup the files using tar.
tar czf $dest/$archive_file $backup_files
    
# Print end status message.
echo
echo "Backup finished"
date
    
# Long listing of files in $dest to check file sizes.
ls -lh $dest
```

## Running the script

### Run from a terminal

The simplest way to use the above backup script is to copy and paste the contents into a file (called `backup.sh`, for example). The file must be made executable:

```bash
chmod u+x backup.sh
```

Then from a terminal prompt, run the following command:

```bash
sudo ./backup.sh
```

This is a great way to test the script to make sure everything works as expected.

### Run with `cron`

The `cron` utility can be used to automate use of the script. The `cron` daemon allows scripts, or commands, to be run at a specified time and date.

`cron` is configured through entries in a `crontab` file. `crontab` files are separated into fields:

```bash
# m h dom mon dow   command
```

Where:

- `m`: The minute the command executes on, between 0 and 59.

- `h`: The hour the command executes on, between 0 and 23.

- `dom`: The day of the month the command executes on.

- `mon`: The month the command executes on, between 1 and 12.

- `dow`: The day of the week the command executes on, between 0 and 7. Sunday may be specified by using 0 or 7, both values are valid.

- `command`: The command to run.

To add or change entries in a `crontab` file the `crontab -e` command should be used. Also note the contents of a `crontab` file can be viewed using the `crontab -l` command.

To run the `backup.sh` script listed above using `cron`, enter the following from a terminal prompt:

```bash
sudo crontab -e
```

```{note}
Using `sudo` with the `crontab -e` command edits the *root* user's `crontab`. This is necessary if you are backing up directories only the root user has access to.
```

As an example, if we add the following entry to the `crontab` file:

```bash
# m h dom mon dow   command
0 0 * * * bash /usr/local/bin/backup.sh
```

The `backup.sh` script would be run every day at 12:00 pm.

```{note}
The `backup.sh` script will need to be copied to the `/usr/local/bin/` directory in order for this entry to run properly. The script can reside anywhere on the file system, simply change the script path appropriately.
```

## Restoring from the archive

Once an archive has been created, it is important to test the archive. The archive can be tested by listing the files it contains, but the best test is to **restore** a file from the archive.

- To see a listing of the archive contents, run the following command from a terminal:

  ```bash
  tar -tzvf /mnt/backup/host-Monday.tgz
  ```

- To restore a file from the archive back to a different directory, enter:
  ```bash 
  tar -xzvf /mnt/backup/host-Monday.tgz -C /tmp etc/hosts
  ```
  
  The `-C` option to `tar` redirects the extracted files to the specified directory. The above example will extract the `/etc/hosts` file to `/tmp/etc/hosts`. `tar` recreates the directory structure that it contains. Also, notice the leading "`/`" is left off the path of the file to restore.

- To restore all files in the archive enter the following:

  ```bash
  cd /
  sudo tar -xzvf /mnt/backup/host-Monday.tgz
  ```

  ```{note}
  This will overwrite the files currently on the file system.
  ```

## Further reading

- For more information on shell scripting see the [Advanced Bash-Scripting Guide](http://tldp.org/LDP/abs/html/)

- The [Cron How-to Wiki Page](https://help.ubuntu.com/community/CronHowto) contains details on advanced cron options.

- See the [GNU tar Manual](http://www.gnu.org/software/tar/manual/index.html) for more tar options.

- The Wikipedia [Backup Rotation Scheme](http://en.wikipedia.org/wiki/Backup_rotation_scheme) article contains information on other backup rotation schemes.

- The shell script uses tar to create the archive, but there many other command line utilities that can be used. For example:
    
  - [`cpio`](http://www.gnu.org/software/cpio/): used to copy files to and from archives.
    
  - [`dd`](http://www.gnu.org/software/coreutils/): part of the coreutils package. A low level utility that can copy data from one format to another.
   
  - [`rsnapshot`](http://www.rsnapshot.org/): a file system snapshot utility used to create copies of an entire file system. Also check the {ref}`Tools - rsnapshot <install-rsnapshot>` for some information.
    
  - {manpage}`rsync(1)`: a flexible utility used to create incremental copies of files.
