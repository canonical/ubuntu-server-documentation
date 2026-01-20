---
myst:
  html_meta:
    description: Create automated backups using shell scripts with tar to archive files; Optionally do so to NFS-mounted file systems, file rotation and tape.
---

(back-up-using-shell-scripts)=
# How to back up using shell scripts

In general, a shell script configures which directories to backup, and passes those directories as arguments to the `tar` utility, which creates an archive file. The archive file can then be moved or copied to another location. The archive can also be created on a remote file system such as a {ref}`Network File System (NFS) <install-nfs>` mount.

The `tar` utility creates one archive file out of many files or directories. `tar` can also filter the files through compression utilities, thus reducing the size of the archive file.

In this guide, we will walk through how to use a shell script for backing up files, and how to restore files from the archive we create.
The later sections will modify it to rotate archives or use tape.

## The shell script

The following example shell script uses `tar` to create an archive file on a remotely mounted NFS file system. The archive filename is determined using additional command line utilities.

This example is for the purpose of this explanation intentionally rather brief; however there are many options that can be included in such a script. For more information on shell scripting see the [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/).

Conceptually this example uses:

- `$backup_files`: A variable listing which directories you would like to backup. The list should be customized to fit your needs.

- `$day`: A variable holding the day of the week (Monday, Tuesday, Wednesday, etc). This is used to create an archive file for each day of the week, giving a backup history of seven days. There are other ways to accomplish this including using the `date` utility.

- `$hostname`: A variable containing the *short* hostname of the system. Using the hostname in the archive filename gives you the option of placing daily archive files from multiple systems in the same directory.

- `$archive_file`: The full archive filename.

- `$dest`: Destination of the archive file. The directory needs to be created and in this case *mounted* before executing the backup script. See {ref}`install-nfs` for details of using NFS.

- `status messages`: Optional messages printed to the console using the `echo` utility.

- `tar czf $dest/$archive_file $backup_files`: The tar command used to create the archive file.

  - `c`: Creates an archive.

  - `z`: Filter the archive through the `gzip` utility, compressing the archive.

  - `f`: Output to an archive file. Otherwise the `tar` output will be sent to STDOUT.

- `ls -lh $dest`: Optional statement prints a `-l` long listing in `-h` human-readable format of the destination directory. This is useful for a quick file size check of the archive file. This check should not replace testing the archive file.

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

(backup-run-the-script)=
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

(archive-rotation-shell-script)=
## Archive rotation shell script

The {ref}`simple backup shell script <back-up-using-shell-scripts>` above only allows for seven different archives to be retained, afterwards the weekdays will repeat and overwrite the former content.
For a server whose data doesn't change often or needs no long term retention, this may be enough.
One could use the date instead of a weekday, but that would create and retain a lot of backup files.
To get such potentially large amounts of data under control, a more complex rotation scheme should be considered.

### Rotating NFS archives

Here, the shell script is slightly modified to implement a grandparent-parent-child rotation scheme (monthly-weekly-daily):

- The rotation will do a *daily* backup from Sunday to Friday.

- On Saturday, a *weekly* backup is done -- giving four weekly backups per month.

- The *monthly* backup is done on the first day of the month, rotating two monthly backups based on whether the month is odd or even.

Here is the new script:

```sh
#!/bin/bash
####################################
#
# Backup to NFS mount script with
# grandparent-parent-child rotation.
#
####################################

# What to backup.
backup_files="/home /var/spool/mail /etc /root /boot /opt"

# Where to backup to.
dest="/mnt/backup"

# Setup variables for the archive filename.
day=$(date +%A)
hostname=$(hostname -s)

# Find which week of the month 1-4 it is.
day_num=$(date +%-d)
if (( $day_num <= 7 )); then
        week_file="$hostname-week1.tgz"
elif (( $day_num > 7 && $day_num <= 14 )); then
        week_file="$hostname-week2.tgz"
elif (( $day_num > 14 && $day_num <= 21 )); then
        week_file="$hostname-week3.tgz"
elif (( $day_num > 21 && $day_num < 32 )); then
        week_file="$hostname-week4.tgz"
fi

# Find if the Month is odd or even.
month_num=$(date +%m)
month=$(expr $month_num % 2)
if [ $month -eq 0 ]; then
        month_file="$hostname-month2.tgz"
else
        month_file="$hostname-month1.tgz"
fi

# Create archive filename.
if [ $day_num == 1 ]; then
        archive_file=$month_file
elif [ $day != "Saturday" ]; then
        archive_file="$hostname-$day.tgz"
else
        archive_file=$week_file
fi

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
ls -lh $dest/
```

This modified script can be executed using the same methods already outlined in section {ref}`backup-run-the-script`.

## Backing up to tape drives

A tape drive attached to the server can be used instead of an NFS share. Using a tape drive simplifies archive rotation, and makes taking the media off-site easier as well.

When using a tape drive, the filename portions of the script aren't needed because the data is sent directly to the tape device. Some commands to manipulate the tape *are* needed, however. This is accomplished using `mt`, a magnetic tape control utility -- part of the `cpio` package.

Here is the shell script modified to use a tape drive:

```sh
#!/bin/bash
####################################
#
# Backup to tape drive script.
#
####################################

# What to backup.
backup_files="/home /var/spool/mail /etc /root /boot /opt"

# Where to backup to.
dest="/dev/st0"

# Print start status message.
echo "Backing up $backup_files to $dest"
date
echo

# Make sure the tape is rewound.
mt -f $dest rewind

# Backup the files using tar.
tar czf $dest $backup_files

# Rewind and eject the tape.
mt -f $dest rewoffl

# Print end status message.
echo
echo "Backup finished"
date
```

```{note}
The default device name for a SCSI tape drive is `/dev/st0`. Use the appropriate device path for your system.
```

Restoring from a tape drive is basically the same as restoring from a file. Simply rewind the tape and use the device path instead of a file path. For example, to restore the `/etc/hosts` file to `/tmp/etc/hosts`:

```bash
mt -f /dev/st0 rewind
tar -xzf /dev/st0 -C /tmp etc/hosts
```

## Further reading

- For more information on shell scripting see the [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/).

- The [`cron` how-to wiki page](https://help.ubuntu.com/community/CronHowto) contains details on advanced `cron` options.

- See the [GNU `tar` manual](http://www.gnu.org/software/tar/manual/index.html) for more `tar` options.

- The Wikipedia [Backup Rotation Scheme](http://en.wikipedia.org/wiki/Backup_rotation_scheme) article contains information on other backup rotation schemes.

- The shell script uses `tar` to create the archive, but there many other command line utilities that can be used. For example:

  - [`cpio`](http://www.gnu.org/software/cpio/): used to copy files to and from archives.

  - [`dd`](http://www.gnu.org/software/coreutils/): part of the `coreutils` package. A low level utility that can copy data from one format to another.

  - [`rsnapshot`](https://rsnapshot.org/): a file system snapshot utility used to create copies of an entire file system. Also check the {ref}`Tools - rsnapshot <install-rsnapshot>` for some information.

  - {manpage}`rsync(1)`: a flexible utility used to create incremental copies of files.
