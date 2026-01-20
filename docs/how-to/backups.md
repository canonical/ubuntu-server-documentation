---
myst:
  html_meta:
    description: Backup solutions for Ubuntu Server including Bacula, rsnapshot, shell scripts, and etckeeper for version control.
---

(how-to-backups-and-version-control)=
# Backups and version control

On Ubuntu, two primary ways of backing up your system are **backup utilities** and **shell scripts**. For additional protection, you can combine backup methods.

## Backup utilities

backup utilities provide a better UX, but define some concepts and assumptions that the user will have to follow.

* {ref}`Bacula <install-bacula>` has advanced features and customization support, which makes it a good choice for enterprise systems or complex setups.
* {ref}`rsnapshot <install-rsnapshot>` is a simple and efficient solution, well suited to individual users or small-scale organizations.

```{toctree}
:hidden:

Install Bacula <backups/install-bacula>
Install rsnapshot <backups/install-rsnapshot>
```

## Shell scripts

Usually laying out such base concepts as the *Backup utilities* above do, forces the implementation to follow some best practises and generally is recommended.
But if you are looking for full flexibility and customization, another option is to use shell scripts around the most basic tools.

* {ref}`back-up-using-shell-scripts` contains shell script based examples for general backup, rotation and tape usage

```{toctree}
:hidden:

Backup with shell scripts <backups/back-up-using-shell-scripts>
```

## Version control

* {ref}`install-etckeeper` stores the contents of `/etc` in a Version Control System (VCS) repository
* {ref}`Install gitolite <install-gitolite>` for a traditional source control management server for git, including multiple users and access rights management

```{toctree}
:hidden:

etckeeper <backups/install-etckeeper>
Install gitolite <backups/install-gitolite>
```

## See also

* Explanation: {ref}`introduction-to-backups`
