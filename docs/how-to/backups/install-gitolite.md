---
myst:
  html_meta:
    description: Set up Gitolite for centralized git hosting with fine-grained access control, SSH key authentication, and bare repository management.
---

(install-gitolite)=
# How to set up Gitolite

{term}`Gitolite` Gitolite allows you to setup git hosting on a central server, with fine-grained access control and many more powerful features.

You can use your served repositories as `git remote` in the form of `git@yourserver:some/repo/path`.

Gitolite stores ["bare git"](https://git-scm.com/docs/gitglossary#Documentation/gitglossary.txt-aiddefbarerepositoryabarerepository) repositories at a location of your choice, usually `/home/git`.
It has its independent user realm, each user is created by assigning their {term}`SSH-key`.
The repositories itself are owned by one system user of your choice, usually `git`.

## Install a Gitolite server

Gitolite can be installed with the following command.

The install automation will ask for a path or content of your `admin` ssh key.
For a better understanding of your setup we recommend to leave the prompt empty for full control of your setup (so you can use `git` as the username, and customize the storage path).

```bash
sudo apt install gitolite3
```

## Configure Gitolite

Gitolite stores its configuration in a git repository (called `gitolite-admin`), so there's no configuration in `/etc`.
This configuration repository manages all other git repositories, users and their permissions.

Create a `git` user for Gitolite to use for the service (you can adjust the git repository storage path as the `--home` directory):

```bash
sudo useradd --system --home /home/git git
```

To access the config repository, we now add the administrator's public {term}`SSH-key`.
If you have not yet configured an SSH key, refer to the section on {ref}`SSH keys in our OpenSSH guide <openssh-server>`.

We copy it to `/tmp` so our `git` user can read the file to import it.
Please adjust the path to the desired admin user's {term}`SSH-key` (and algorithm, like `id_rsa.pub`).


```bash
cp ~/.ssh/id_ed25519.pub /tmp/admin.pub
```

As the `git` user, let's import the administrator's key into Gitolite (it will get the `admin` username due to that key's filename).

```bash
sudo -i -u git gitolite setup -pk /tmp/admin.pub
```

What this creates:
- The management repository in `~git/repositories/gitolite-admin.git`
- A global config in `~git/.gitolite.rc`
- `~git/projects.list` as repository overview
- `~git/.ssh/authorized_keys` with `command=` to force Gitolite over `ssh`
  - Later it will contain the `ssh` public key for each user you configured

To try if the setup worked, try `ssh` as the user owning the admin key we just added, so see the _Gitolite repository overview_:

```bash
ssh git@yourserver
```
```
hello admin, this is git@your-gitolite-server running gitolite3

 R W	gitolite-admin
 R W	testing
```


## Managing Gitolite users and repositories

To configure Gitolite users, repositories and permissions, clone the configuration repository.
`$yourserver` can be an IP address, hostname, or just `localhost` for your current machine.

```bash
git clone git@$yourserver:gitolite-admin.git
```

To apply configuration change, commit them in the repository and **push the changes** back to the server with:

```bash
git commit -a
git push origin master
```

The `gitolite-admin` contains two subdirectories: **`keydir`** (which contains the list of users' public SSH keys) and **`conf`** (which contains configuration files).
To **add a Gitolite user** (it's virtual - not a system username), obtain their SSH public key (from `~user/.ssh/id_<name>.pub`) and add it to the `keydir` directory as `<desired-username>.pub`.
To **delete a Gitolite user**, you only need to delete their public key files.
To manage repositories and groups in `conf/gitolite.conf`, specify the the list of repositories followed by some access rules.


Have an example:

```text
# Gitolite config
# Users are created by their public key in keydir/$username.pub

# Group creation
@bestproject          = name1 name2
@projectwatchers      = name3 @bestproject

# This repo itself
repo    gitolite-admin
        RW+     =   admin
        R       =   alice

# A repo with access to anybody
repo    testing
        RW+     = @all

# A repo with special privileges, to tags and branches
repo    some/awesome/project
        RW                      =   alice @bestproject
        RW+                     =   bob
        RW+   dev/              =   @bestproject
        R                       =   @projectwatchers carol
# bestproject members and alice can push code (but not force-push)
# bestproject members can force-push branches starting with dev/
# bob can forcepush anything
# projectwatchers and carol have readonly access
```

For more advanced permission configuration (restricting tags, branches, ...), please see the examples in the upstream documentation [page 1](https://gitolite.com/gitolite/conf.html) and [page 2](https://gitolite.com/gitolite/conf-2.html).


## Using your server

Now you can use your newly set up Gitolite server as a regular `git remote`.

Once a user is created and has permissions, they can access the repositories.

As a fresh clone:

```bash
git clone git@$server:some/awesome/project.git
```

Or as a remote to an existing repository:

```bash
git remote add gitolite git@$server:some/awesome/project.git
```

## Further reading

- [Gitolite's code repository](https://github.com/sitaramc/gitolite) provides access to source code
- [Gitolite's documentation](https://gitolite.com/gitolite/) includes more detailed configuration guides and a "fool-proof setup", with how-tos for common tasks
- Gitolite's maintainer has written a book, [Gitolite Essentials](https://www.packtpub.com/hardware-and-creative/gitolite-essentials), for more in-depth information about the software
- General information about `git` itself can be found at the [Git homepage](https://git-scm.com/)
