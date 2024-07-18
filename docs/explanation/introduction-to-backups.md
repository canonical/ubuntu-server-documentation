(introduction-to-backups)=
# Introduction to backups

There are many ways to back up an Ubuntu installation. The most important thing about backups is to develop a backup plan that consists of:

* What should be backed up
* How often to back it up
* Where backups should be stored
* How to restore your backups

It is good practice to take backup media off-site in case of a disaster. For backup plans involving physical tape or removable hard drives, the tapes or drives can be manually taken off-site. However, in other cases this may not be practical and the archives will need to be copied over a WAN link to a server in another location.

## Backup options

On Ubuntu, two of the primary ways of backing up your system are through **backup utilities** and **shell scripts**. Wherever possible, it's better to build redundancy into your backup systems by combining backup methods so that you are not reliant on a single system.

### Backup utilities

The most straightforward way to create backups is through using a dedicated tool like [Bacula](http://www.bacula.org/) or [rsnapshot](https://rsnapshot.org/). These tools offer specialised features such as automation, compression, data recovery, encryption and incremental/differential backups -- but with an easy-to-use interface or CLI to help simplify the backup management process.

* **Bacula**
  This tool uses incremental backups, which only store changes made since the last backup. This can significantly decrease the storage space and backup time required. It can also manage backups of multiple systems over a network. With more advanced features and support for additional customisation, it is often used by users with more complex needs (e.g. in enterprise environments).

  * Find out [how to install and configure Bacula](../how-to/how-to-install-and-configure-bacula.md).
  
* **rsnapshot** uses rsync to take periodic "snapshots" of your files, which makes it easier to access previous versions. It's often used for local backups on a single system and is ideal for individual users or small-scale organisations who want a simpler and more efficient solution.

  * Find out [how to install and configure rsnapshot](../how-to/how-to-install-and-configure-rsnapshot.md).

### Shell scripts

Using shell scripts to manage your backups can be easy or complicated, depending on the complexity of your setup. However, the advantage of shell scripts over using backup utilities, is that they offer full flexibility and customisation. Through backup shell scripts, you can fully tailor the backup process to your specific requirements without using third-party tools.

Refer to this guide for instructions on [how to use shell scripts for backups](../how-to/how-to-back-up-using-shell-scripts.md) -- or you can take a look at our reference examples:
* [A basic backup shell script](../reference/basic-backup-shell-script.md)
* [An example of archive rotation with shell scripts](../reference/archive-rotation-shell-script.md)
