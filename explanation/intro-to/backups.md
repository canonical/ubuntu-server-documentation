(introduction-to-backups)=
# Introduction to backups

It is important to develop a backup plan that consists of:

* What should be backed up
* How often to back it up
* Where backups should be stored
* How to restore your backups

It is good practice to store important backup media off-site in case of a disaster. Physical backup media like removable hard drives or tape can be moved off-site manually. When this is not possible, backups can be copied over a WAN link to a server in another location.

## Backup options

There are many ways to back up an Ubuntu installation. On Ubuntu, two primary ways to back up your system are **backup utilities** and **shell scripts**. For additional protection, you can combine back up methods so you don't rely on a single system.

### Backup utilities

The easiest way to create backups is to use dedicated tools like [Bacula](http://www.bacula.org/) or [rsnapshot](https://rsnapshot.org/). These tools have easy-to-use interfaces or a CLI to help simplify the backup management process. They have powerful features such as automation, compression, data recovery, encryption and incremental backups.

* **Bacula**
  Bacula's advanced features and support for additional customization make it a good choice for enterprise systems or users with complex needs. Bacula can manage backups of multiple systems over a network. Bacula uses incremental backups which only store changes made since the last backup. This can significantly decrease storage space needs and backup time. 

    * Find out {ref}`how to install and configure Bacula <install-bacula>`.
  
* **rsnapshot** is ideal for individual users or small-scale organizations who want a simple and efficient solution. **rsnapshot** uses `rsync` to take periodic "snapshots" of your files so it is easy to access earlier versions. It's often used for local backups on a single system.

  * Find out {ref}`how to install and configure rsnapshot <install-rsnapshot>`.

### Shell scripts

You can tailor the backup process to your specific requirements with shell scripts. The advantage of shell scripts over backup utilities is they offer full flexibility and customization. 

Refer to this guide for instructions on {ref}`how to use shell scripts for backups <back-up-using-shell-scripts>` -- or you can take a look at our reference examples:
  * {ref}`A basic backup shell script <basic-backup-shell-script>`
  * {ref}`An example of archive rotation with shell scripts <archive-rotation-shell-script>`
