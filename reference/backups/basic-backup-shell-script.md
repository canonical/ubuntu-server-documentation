(basic-backup-shell-script)=
# Basic backup shell script

The following shell script uses tar to create an archive file on a remotely mounted NFS file system. The archive filename is determined using additional command line utilities.

Either copy the code into a file, or for instructions of how to use the script, {ref}`refer to this guide <back-up-using-shell-scripts>`.

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

- `$backup_files`: A variable listing which directories you would like to backup. The list should be customized to fit your needs.

- `$day`: A variable holding the day of the week (Monday, Tuesday, Wednesday, etc). This is used to create an archive file for each day of the week, giving a backup history of seven days. There are other ways to accomplish this including using the `date` utility.

- `$hostname`: A variable containing the *short* hostname of the system. Using the hostname in the archive filename gives you the option of placing daily archive files from multiple systems in the same directory.

- `$archive_file`: The full archive filename.

- `$dest`: Destination of the archive file. The directory needs to be created and in this case *mounted* before executing the backup script. See {ref}`Network File System (NFS) <install-nfs>` for details of using NFS.

- `status messages`: Optional messages printed to the console using the `echo` utility.

- `tar czf $dest/$archive_file $backup_files`: The tar command used to create the archive file.

  - `c`: Creates an archive.

  - `z`: Filter the archive through the `gzip` utility, compressing the archive.

  - `f`: Output to an archive file. Otherwise the `tar` output will be sent to STDOUT.

- `ls -lh $dest`: Optional statement prints a `-l` long listing in `-h` human-readable format of the destination directory. This is useful for a quick file size check of the archive file. This check should not replace testing the archive file.

This is a simple example of a backup shell script; however there are many options that can be included in such a script. For more information on shell scripting see the [Advanced Bash-Scripting Guide](http://tldp.org/LDP/abs/html/).

## Further reading

- The [CronHowto Wiki Page](https://help.ubuntu.com/community/CronHowto) contains details on advanced `cron` options.

- See the [GNU tar Manual](http://www.gnu.org/software/tar/manual/index.html) for more `tar` options.

- The Wikipedia [Backup Rotation Scheme](http://en.wikipedia.org/wiki/Backup_rotation_scheme) article contains information on other backup rotation schemes.

- The shell script uses `tar` to create the archive, but there many other command line utilities that can be used. For example:

  - [`cpio`](http://www.gnu.org/software/cpio/): Used to copy files to and from archives.

  - [`dd`](http://www.gnu.org/software/coreutils/): Part of the `coreutils` package. A low level utility that can copy data from one format to another.

  - [`rsnapshot`](http://www.rsnapshot.org/): A filesystem snapshot utility used to create copies of an entire file system. Also check the {ref}`Install rsnapshot guide <install-rsnapshot>` for more information.

  - [`rsync`](http://manpages.ubuntu.com/manpages/focal/man1/rsync.1.html): A flexible utility used to create incremental copies of files.
