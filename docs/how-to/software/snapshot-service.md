---
myst:
  html_meta:
    description: Use the Ubuntu snapshot service to install historical package versions, ensure reproducible deployments, and manage structured update workflows.
---

(snapshot-service)=
# How to use the Ubuntu snapshot service

The Ubuntu snapshot service allows you to access old packages in the Ubuntu
archive based on past dates. Some of the use cases for this service include:

* Installing a superseded version of a package as it existed at a particular
  date and time, which is useful to troubleshoot bugs or regressions, or to
  allow reproducibility.
* Setting upgrades to known states, which can be useful to ensure homogeneity
  for a fleet of Ubuntu installations and to ensure predictability upon package
  upgrades (including unattended upgrades).
* Support a structured update workflow by validating snapshots in different
  environments or by rolling out package upgrades in stages for a large set of
  machines.

Here we show how to set up and use the snapshot service.

## Prerequisites

Snapshots are supported in Ubuntu 23.10 onward and on updated installations of
Ubuntu 20.04 LTS (starting from `apt` 2.0.10) and Ubuntu 22.04 LTS (starting
from `apt` 2.4.11).

In Ubuntu 24.04 LTS and later, `apt` will automatically detect whether a
repository supports snapshots. Therefore, there is no need for additional
configuration before you can start using the Ubuntu snapshot service. For
Ubuntu versions lower than 24.04, you need to set a `snapshot` option in the
relevant entries of the `/etc/apt/sources.list` file. For instance:

If you have the following contents in the `/etc/apt/sources.list` file

```
deb http://archive.ubuntu.com/ubuntu jammy main universe restricted multiverse
deb http://archive.ubuntu.com/ubuntu jammy-updates main universe restricted multiverse
deb http://archive.ubuntu.com/ubuntu jammy-backports main restricted universe multiverse
deb http://security.ubuntu.com/ubuntu jammy-security main restricted universe multiverse
```

you can enable the snapshot service for [all components in all
pockets](https://documentation.ubuntu.com/project/how-ubuntu-is-made/concepts/package-archive/#pockets)
by changing it to

```
deb [snapshot=yes] http://archive.ubuntu.com/ubuntu jammy main universe restricted multiverse
deb [snapshot=yes] http://archive.ubuntu.com/ubuntu jammy-updates main universe restricted multiverse
deb [snapshot=yes] http://archive.ubuntu.com/ubuntu jammy-backports main restricted universe multiverse
deb [snapshot=yes] http://security.ubuntu.com/ubuntu jammy-security main restricted universe multiverse
```

Without the setup shown above, `apt` will simply ignore snapshot related
command line options in Ubuntu releases lower than 24.04.

The following table describes whether the snapshot service can be used with
each supported Ubuntu release, and whether or not it is necessary to configure
the `snapshot` option in the `sources.list` file.

| Ubuntu Release       | Supports Snapshot Service?   | Need to configure `sources.list`? |
|----------------------|------------------------------|-----------------------------------|
| Next Ubuntu releases | Yes                          | No                                |
| Ubuntu 25.10         | Yes                          | No                                |
| Ubuntu 25.04         | Yes                          | No                                |
| Ubuntu 24.04 LTS     | Yes                          | No                                |
| Ubuntu 22.04 LTS     | Yes (with `apt` >= `2.4.11`) | Yes                               |
| Ubuntu 20.04 LTS     | Yes (with `apt` >= `2.0.10`) | Yes                               |

## Quick start

You can start using the snapshot service right away by passing the `--snapshot`
option to `apt` followed by a timestamp in the format shown below.

```
$ sudo apt install hello --update --snapshot 20240301T030400Z
```

The `--snapshot` option and the the timestamp format are discussed with more
details in the next sections.

## Using the snapshot service

There are several options when it comes to setting up Ubuntu snapshot services.
Here we present the most relevant, supported ones.

Below, we refer to the snapshot ID as `$SNAPSHOT_ID`. This is a UTC date and
time formatted as YYYYMMDDTHHMMSSZ, e.g., 20240430T214500Z, which refers to the
snapshot that represents the state of the Ubuntu archive on April 30th, 2024,
at 21:45:00 UTC.

Currently, the Ubuntu snapshot service provides snapshots for any date and time
**after 1 March 2023**.

### The `--snapshot` CLI option

The snapshot service can be used through the `--snapshot` (or `-S`) CLI option
for `apt`, which receives a snapshot ID argument.

```
$ sudo apt update --snapshot $SNAPSHOT_ID
$ sudo apt install $PACKAGE_NAME --snapshot $SNAPSHOT_ID
```

You can also use the short, atomic version to merge the two actions above in a
single command, which will download the package information from the
repository, then download and install the package:

```
$ sudo apt install $PACKAGE_NAME --update --snapshot $SNAPSHOT_ID
```

or using the short version of the snapshot option:

```
$ sudo apt install $PACKAGE_NAME --update -S $SNAPSHOT_ID
```

For instance, if you want to install Docker as it was released when Ubuntu
24.04 LTS first came out, you could try a snapshot from May 2025:

```
$ sudo apt update --snapshot 20240501T120000Z
```

Note that you will need to keep using the snapshot option to let `apt` operate
over the snapshot repositories. For example, if you want to check what versions
of Docker are available with the snapshot:

```
$ apt policy docker.io --snapshot 20240501T120000Z
docker.io:
  Installed: (none)
  Candidate: 24.0.7-0ubuntu4
  Version table:
     24.0.7-0ubuntu4 500
        500 https://snapshot.ubuntu.com/ubuntu/20240501T120000Z noble/universe amd64 Packages
```

If you forget to use the snapshot option, `apt` will operate over the regular archive:

```
$ apt policy docker.io
docker.io:
  Installed: (none)
  Candidate: 28.2.2-0ubuntu1~24.04.1
  Version table:
     28.2.2-0ubuntu1~24.04.1 500
        500 http://archive.ubuntu.com/ubuntu noble-updates/universe amd64 Packages
     27.5.1-0ubuntu3~24.04.2 500
        500 http://security.ubuntu.com/ubuntu noble-security/universe amd64 Packages
     24.0.7-0ubuntu4 500
        500 http://archive.ubuntu.com/ubuntu noble/universe amd64 Packages
```

Then, you can install Docker from that snapshot:

```
$ sudo apt install docker.io --snapshot 20240501T120000Z
...
$ docker --version
Docker version 24.0.7, build 24.0.7-0ubuntu4
```

Now, let's say you checked the [Docker package publishing history in
Launchpad](https://launchpad.net/ubuntu/+source/docker.io-app/+publishinghistory)
and (for some reason) decided you want to install version
`26.1.3-0ubuntu1~24.04.1`, which, as inferred from the publishing history,
superseded `docker.io` `24.0.7-0ubuntu4.1` in `noble-updates` on `2024-11-25`.
Then, `24.0.7-0ubuntu4.1` was removed from the `-updates` pocket on `2024-11-26`.

You could then use `20241126T230000Z` as the snapshot ID to get the target
package (`26.1.3-0ubuntu1~24.04.1`):

```
$ sudo apt install docker.io --update --snapshot 20241126T230000Z
...
$ docker --version
Docker version 26.1.3, build 26.1.3-0ubuntu1~24.04.1
```

```{note}
Note that, at the time of writing, the version of docker.io in the
`noble-security` pocket is `27.5.1-0ubuntu3~24.04.2`, i.e., the version used in
the example above may be affected by known vulnerabilities. When using the
snapshot service, do make sure to check the latest version available in your
Ubuntu release's `-security` pocket to make sure you are not installing a vulnerable
package.
```

### Configuring the snapshot service for specific repositories

In your `apt` repositories configuration files, it is possible to specify
snapshots to be used for each specific repository.

For Ubuntu 24.04 LTS and later, which uses the deb822 style by default, we add
a `Snapshot` option to the relevant sources file in the following format:

```
Snapshot: $SNAPSHOT_ID
```

For Ubuntu series lower than 24.04, you change the value of the `snapshot`
option in your sources file, i.e., if you had the following entry in your `/etc/apt/sources.list` file

```
deb [snapshot=yes] http://archive.ubuntu.com/ubuntu ...
```

you replace the `yes` value with the snapshot ID:

```
deb [snapshot=$SNAPSHOT_ID] http://archive.ubuntu.com/ubuntu ...
```

Let's say you want to pin a specific snapshot for all the pockets in your Ubuntu
24.04 LTS server. Then, you add the `Snapshot` options to
`/etc/apt/sources.list.d/ubuntu.sources`:

```
Types: deb
URIs: http://archive.ubuntu.com/ubuntu
Suites: noble noble-updates noble-backports
Components: main universe restricted multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
Snapshot: 20250530T223000Z

Types: deb
URIs: http://security.ubuntu.com/ubuntu
Suites: noble-security
Components: main universe restricted multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
Snapshot: 20250530T223000Z
```

Afterwards, you can run the following commands to install the Docker version
present in that snapshot:

```
$ sudo apt install --update docker.io
```

to install the Docker version present in that snapshot.

```
$ docker --version
Docker version 27.5.1, build 27.5.1-0ubuntu3~24.04.1
```

Note that, when you configure a repository to use a snapshot using the method
described above, `apt` will always ignore the `--snapshot` option:

```
$ sudo apt install --update docker.io --snapshot 20251013T2300Z
...
Hit:5 https://snapshot.ubuntu.com/ubuntu/20250530T223000Z noble InRelease
Hit:6 https://snapshot.ubuntu.com/ubuntu/20250530T223000Z noble-updates InRelease
Hit:7 https://snapshot.ubuntu.com/ubuntu/20250530T223000Z noble-backports InRelease
Hit:8 https://snapshot.ubuntu.com/ubuntu/20250530T223000Z noble-security InRelease
...
docker.io is already the newest version (27.5.1-0ubuntu3~24.04.1).
0 upgraded, 0 newly installed, 0 to remove and 3 not upgraded.
```

As you can see from the logs above, `apt` is still using the snapshot
configured in `/etc/apt/sources.list.d/ubuntu.sources`, ignoring the
`--snapshot` CLI option.

### Configuring the snapshot service globally

As an alternative to configuring a specific snapshot for each individual
repository, as described in the previous section, you can configure a snapshot
globally for all repositories that have snapshots enabled.

```{warning}
If you are following these examples until here, make sure to revert the changes
to the sources configuration file made in the previous section.
```

Let's configure `apt` to default to a specific snapshot by setting the
`APT::Snapshot` option:

```
$ echo 'APT::Snapshot "20250801T111111Z";' | sudo tee /etc/apt/apt.conf.d/50snapshot
```

The system will now default to fetching packages from the configured snapshot:

```
$ sudo apt install docker.io --update
...
$ docker --version
Docker version 27.5.1, build 27.5.1-0ubuntu3~24.04.2
```

Note that, in contrast to repositories with snapshots configured in the
sources file as shown in the previous section, configuring a snapshot globally
will not make `apt` ignore the `--snapshot` CLI option:

```
$ sudo apt install docker.io --update --snapshot 20251013T120000Z
$ docker --version
Docker version 28.2.2, build 28.2.2-0ubuntu1~24.04.1
```

You can revert the global configuration by removing the file which added it:

```
$ sudo rm /etc/apt/apt.conf.d/50snapshot
```

## Further reading

* [The Ubuntu snapshot service official page and documentation](https://snapshot.ubuntu.com/)
* [Securing multiple Ubuntu instances while maximising uptime](https://ubuntu.com/blog/securing-multiple-ubuntu-instances-while-maximising-uptime)
* [Integrating the Ubuntu Snapshot Service into systems management and update tools](https://ubuntu.com/blog/integrating-the-ubuntu-snapshot-service-into-systems-management-and-update-tools)

