(install-etckeeper)=
# etckeeper

[etckeeper](https://etckeeper.branchable.com/) allows the contents of `/etc` to be stored in a Version Control System (VCS) repository. It integrates with APT and automatically commits changes to `/etc` when packages are installed or upgraded.

Placing `/etc` under version control is considered an industry best practice, and the goal of etckeeper is to make this process as painless as possible.

## Install etckeeper

Install etckeeper by entering the following in a terminal:

```bash
sudo apt install etckeeper
```

## Initialise etckeeper

The main configuration file, `/etc/etckeeper/etckeeper.conf`, is fairly simple. The main option defines which VCS to use, and by default etckeeper is configured to use git.

The repository is automatically initialised (and committed for the first time) during package installation. It is possible to undo this by entering the following command:

```bash
sudo etckeeper uninit
```

## Configure autocommit frequency

By default, etckeeper will commit uncommitted changes made to `/etc` on a daily basis. This can be disabled using the `AVOID_DAILY_AUTOCOMMITS` configuration option.

It will also automatically commit changes before and after package installation. For a more precise tracking of changes, it is recommended to commit your changes manually, together with a commit message, using:

```bash
sudo etckeeper commit "Reason for configuration change"
```

The `vcs` etckeeper command provides access to any subcommand of the VCS that etckeeper is configured to run. It will be run in `/etc`. For example, in the case of git:

```bash
sudo etckeeper vcs log /etc/passwd
```

To demonstrate the integration with the package management system (APT), install `postfix`:

```bash
sudo apt install postfix
```

When the installation is finished, all the `postfix` configuration files should be committed to the repository:

```text
[master 5a16a0d] committing changes in /etc made by "apt install postfix"
 Author: Your Name <xyz@example.com>
 36 files changed, 2987 insertions(+), 4 deletions(-)
 create mode 100755 init.d/postfix
 create mode 100644 insserv.conf.d/postfix
 create mode 100755 network/if-down.d/postfix
 create mode 100755 network/if-up.d/postfix
 create mode 100644 postfix/dynamicmaps.cf
 create mode 100644 postfix/main.cf
 create mode 100644 postfix/main.cf.proto
 create mode 120000 postfix/makedefs.out
 create mode 100644 postfix/master.cf
 create mode 100644 postfix/master.cf.proto
 create mode 100755 postfix/post-install
 create mode 100644 postfix/postfix-files
 create mode 100755 postfix/postfix-script
 create mode 100755 ppp/ip-down.d/postfix
 create mode 100755 ppp/ip-up.d/postfix
 create mode 120000 rc0.d/K01postfix
 create mode 120000 rc1.d/K01postfix
 create mode 120000 rc2.d/S01postfix
 create mode 120000 rc3.d/S01postfix
 create mode 120000 rc4.d/S01postfix
 create mode 120000 rc5.d/S01postfix
     create mode 120000 rc6.d/K01postfix
     create mode 100755 resolvconf/update-libc.d/postfix
     create mode 100644 rsyslog.d/postfix.conf
     create mode 120000 systemd/system/multi-user.target.wants/postfix.service
     create mode 100644 ufw/applications.d/postfix
```

For an example of how `etckeeper` tracks manual changes, add new a host to `/etc/hosts`. Using git you can see which files have been modified:

```bash
sudo etckeeper vcs status
```

and how:

```bash
sudo etckeeper vcs diff
```

If you are happy with the changes you can now commit them:

```bash
sudo etckeeper commit "added new host"
```

## Resources

- See the [etckeeper](https://etckeeper.branchable.com/) site for more details on using etckeeper.

- For documentation on the git VCS tool see [the Git website](https://git-scm.com/).
