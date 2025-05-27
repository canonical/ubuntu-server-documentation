(introduction-to-backups)=
# Introduction to backups

It's important to back up your Ubuntu installation so you can recover quickly if you experience data loss. You can create redundancy by using multiple back-up methods. Redundant data is useful if the primary back-up fails. 

It is important to develop a backup plan that consists of:

* What should be backed up
* How often to back it up
* Where backups should be stored
* How to restore your backups

It is good practice to store important backup media off-site in case of a disaster. Physical backup media like removable hard drives or tape can be moved off-site manually. When it is either impossible or impractical to move media, backups can be copied over a WAN link to a server in another location.

## Backup options

There are many ways to back up an Ubuntu installation. On Ubuntu, two primary ways of backing up your system are **backup utilities** and **shell scripts**. For additional protection, you can combine backup methods so you don't rely on a single system.

### Backup utilities

The easiest way to create backups is to use a dedicated tool like [Bacula](http://www.bacula.org/) or [rsnapshot](https://rsnapshot.org/). These tools have easy-to-use interface or CLI to help simplify the backup management process. They have powerful features such as automation, compression, data recovery, encryption and incremental backups. Incremental backups only store changes made since the last backup which can significantly decrease storage space needs and backup time. 

Bacula's advanced features and support for additional customization make it a good choice for enterprise systems or users with complex needs. rsnapshot is ideal for individual users or small-scale organizations who want a simple and efficient solution. 

| **Tool** | **Back up** | **Backup Method** | **Install and configure** |
|------|--------|---------------|----------------|
|**Bacula**| Multiple systems over a network | Incremental backups | {ref}`how to install and configure Bacula <install-bacula>` |
|**rsnapshot**| Single system | Periodic "snapshots" of files locally or remotely with SSH | {ref}`how to install and configure rsnapshot <install-rsnapshot>` |


### Shell scripts

You can fully tailor the backup process to your specific requirements with shell scripts. The advantage of shell scripts over using backup utilities is they offer full flexibility and customization. 

Refer to this guide for instructions on {ref}`how to use shell scripts for backups <back-up-using-shell-scripts>` -- or you can take a look at these examples:
  * [Basic backup shell script](https://discourse.ubuntu.com/t/basic-backup-shell-script/36419)
  * {ref}`An example of archive rotation with shell scripts <archive-rotation-shell-script>`
