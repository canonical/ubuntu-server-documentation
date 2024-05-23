# How to install and configure gitolite

Gitolite provides a traditional source control management server for git, with multiple users and access rights management. 

## Install a gitolite server

Gitolite can be installed with the following command:

```bash
sudo apt install gitolite3
```

## Configure gitolite

Configuration of the gitolite server is a little different that most other servers on Unix-like systems, in that gitolite stores its configuration in a git repository rather than in files in `/etc/`. The first step to configuring a new installation is to allow access to the configuration repository.

First of all, let's create a user for gitolite to use for the service:

```bash
sudo adduser --system --shell /bin/bash --group --disabled-password --home /home/git git
```

Now we want to let gitolite know about the repository administrator's public SSH key. This assumes that the current user is the repository administrator. If you have not yet configured an SSH key, refer to the section on [SSH keys in our OpenSSH guide](openssh-server.md).

```bash
cp ~/.ssh/id_rsa.pub /tmp/$(whoami).pub
```

Let's switch to the git user and import the administrator's key into gitolite.

```bash
sudo su - git
gl-setup /tmp/*.pub
```

Gitolite will allow you to make initial changes to its configuration file during the setup process. You can now clone and modify the gitolite configuration repository from your administrator user (the user whose public SSH key you imported). Switch back to that user, then clone the configuration repository:

```bash
exit
git clone git@$IP_ADDRESS:gitolite-admin.git
cd gitolite-admin
```

The `gitolite-admin` contains two subdirectories:

- **`conf`** : contains the configuration files
- **`keydir`** : contains the list of user's public SSH keys

## Managing gitolite users and repositories

Adding a new user to gitolite is simple: just obtain their public SSH key and add it to the `keydir` directory as `$DESIRED_USER_NAME.pub`. Note that the gitolite usernames don't have to match the system usernames - they are only used in the gitolite configuration file to manage access control. 

Similarly, users are deleted by deleting their public key files. After each change, do not forget to commit the changes to git, and push the changes back to the server with:

```bash
git commit -a
git push origin master
```

Repositories are managed by editing the `conf/gitolite.conf` file. The syntax is space-separated, and specifies the list of repositories followed by some access rules. The following is a default example:

```text
repo    gitolite-admin
        RW+     =   admin
        R       =   alice
    
repo    project1
        RW+     =   alice
        RW      =   bob
        R       =   denise
```

## Using your server

Once a user's public key has been imported by the gitolite admin, granting the user authorisation to use one or more repositories, the user can access those repositories with the following command:

```bash
git clone git@$SERVER_IP:$PROJECT_NAME.git
```

To add the server as a new remote for an existing git repository:

```bash
git remote add gitolite git@$SERVER_IP:$PROJECT_NAME.git
```

## Further reading

- [Gitolite's code repository](https://github.com/sitaramc/gitolite) provides access to source code
- [Gitolite's documentation](https://gitolite.com/gitolite/) includes a "fool-proof setup" guide and a cookbook with recipes for common tasks
- Gitolite's maintainer has written a book, [Gitolite Essentials](https://www.packtpub.com/hardware-and-creative/gitolite-essentials), for more in-depth information about the software
- General information about git itself can be found at the [Git homepage](http://git-scm.com)
