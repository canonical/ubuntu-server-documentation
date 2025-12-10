---
myst:
  html_meta:
    description: "Understand Docker storage drivers, networking modes, and logging configuration options on Ubuntu Server."
---

(docker-storage-networking-and-logging)=
# Docker storage, networking, and logging

Containers are widely used across multiple server workloads (databases and web servers, for instance), and understanding how to properly set up your server to run them is becoming more important for systems administrators. In this explanatory page, we are going to discuss some of the most important factors a system administrator needs to consider when setting up the environment to run Docker containers.

Understanding the options available to run Docker containers is key to optimising the use of computational resources in a given scenario/workload, which might have specific requirements. Some aspects that are important for system administrators are: **storage**, **networking** and **logging**.

## Storage

The first thing we need to keep in mind is that containers are ephemeral, and unless configured otherwise, so are their data. Docker images are composed of one or more layers which are read-only, and once you run a container based on an image a new writable layer is
created on top of the topmost image layer; the container can manage any type of data there. The content changes in the writable container layer are not persisted anywhere, and once the container is gone all the changes disappear. This behavior presents some
challenges to us: How can the data be persisted? How can it be shared among containers? How can it be shared between the host and the containers?

There are some important concepts in the Docker world that are the answer for some of those problems: they are **volumes**, **bind mounts** and **tmpfs**. Another question is how all those layers that form Docker images and containers will be stored, and for that we are going to talk about **storage drivers** (more on that later).

When we want to persist data we have two options:

- Volumes are the preferred way to persist data generated and used by Docker containers if your workload will generate a high volume of data, such as a database.
- Bind mounts are another option if you need to access files from the host, for example system files.

If what you want is to store some sensitive data in memory, like credentials, and do not want to persist it in either the host or the container layer, we can use tmpfs mounts.

### Volumes

The recommended way to persist data to and from Docker containers is by using volumes. Docker itself manages them, they are not OS-dependent and they can provide some interesting features for system administrators:

- Easier to back up and migrate when compared to bind mounts;
- Managed by the Docker CLI or API;
- Safely shared among containers;
- Volume drivers allow one to store data in remote hosts or in public cloud providers (also encrypting the data).

Moreover, volumes are a better choice than persisting data in the container layer, because volumes do not increase the size of the container, which can affect the life-cycle management performance.

Volumes can be created before or at the container creation time. There are two CLI options you can use to mount a volume in the container during its creation (`docker run` or `docker create`):

- `--mount`: it accepts multiple key-value pairs (`<key>=<value>`). This is the preferred option to use.
  - `type`: for volumes it will always be `volume`;
  - `source` or `src`: the name of the volume, if the volume is anonymous (no name) this can be omitted;
  - `destination`, `dst` or `target`: the path inside the container where the volume will be mounted;
  - `readonly` or `ro` (optional): whether the volume should be mounted as read-only inside the container;
  - `volume-opt` (optional): a comma separated list of options in the format you would pass to the `mount` command.
- `-v` or `--volume`: it accepts 3 parameters separated by colon (`:`):
  - First, the name of the volume. For the default `local` driver, the name should use only: letters in upper and lower case, numbers, `.`, `_` and `-`;
  - Second, the path inside the container where the volume will be mounted;
  - Third (optional), a comma-separated list of options in the format you would pass to the `mount` command, such as `rw`.

### Bind mounts

Bind mounts are another option for persisting data, however, they have some limitations compared to volumes. Bind mounts are tightly associated with the directory structure and with the OS, but performance-wise they are similar to volumes in Linux systems.

In a scenario where a container needs to have access to any host system’s file or directory, bind mounts are probably the best solution. Some monitoring tools make use of bind mounts when executed as Docker containers.

Bind mounts can be managed via the Docker CLI, and as with volumes there are two options you can use:

- `--mount`: it accepts multiple key-value pairs (`<key>=<value>`). This is the preferred option to use.
  - `type`: for bind mounts it will always be `bind`;
  - `source` or `src`: path of the file or directory on the host;
  - `destination`, `dst` or `target`: container’s directory to be mounted;
  - `readonly` or `ro` (optional): the bind mount is mounted in the container as read-only;
  - `volume-opt` (optional): it accepts any `mount` command option;
  - `bind-propagation` (optional): it changes the bind propagation. It can be `rprivate`, `private`, `rshared`, `shared`, `rslave`, `slave`.
- `-v` or `--volume`: it accepts 3 parameters separated by colon (`:`):
  - First, path of the file or directory on the host;
  - Second, path of the container where the volume will be mounted;
  - Third (optional), a comma separated of option in the format you would pass to `mount` command, such as `rw`.

### Tmpfs

Tmpfs mounts allow users to store data temporarily in RAM memory, not in the host’s storage (via bind mount or volume) or in the container’s writable layer (with the help of storage drivers). When the container stops, the tmpfs mount will be removed and the data will not be persisted in any storage.

This is ideal for accessing credentials or security-sensitive information. The downside is that a tmpfs mount cannot be shared with multiple containers.

Tmpfs mounts can be managed via the Docker CLI with the following two options:

- `--mount`: it accepts multiple key-value pairs (`<key>=<value>`). This is the preferred option to use.
  - `type`: for volumes it will always be `tmpfs`;
  - `destination`, `dst` or `target`: container’s directory to be mounted;
  - `tmpfs-size` and `tmpfs-mode` options (optional). For a full list see the [Docker documentation](https://docs.docker.com/storage/tmpfs/#specify-tmpfs-options).
- `--tmpfs`: it accepts no configurable options, just mount the tmpfs for a standalone container.

### Storage drivers

Storage drivers are used to store image layers and to store data in the writable layer of a container. In general, storage drivers are implemented trying to optimize the use of space, but write speed might be lower than native {term}`filesystem` performance depending on the driver in use. To better understand the options and make informed decisions, take a look at the Docker documentation on [how layers, images and containers work](https://docs.docker.com/storage/storagedriver/#images-and-layers).

The default storage driver is the `overlay2` which is backed by `OverlayFS`. This driver is recommended by upstream for use in production systems. The following storage drivers are available and are supported in Ubuntu (as at the time of writing):

- **OverlayFS**: it is a modern union filesystem. The Linux kernel driver is called `OverlayFS` and the Docker storage driver is called `overlay2`. **This is the recommended driver**.
- **ZFS**: it is a next generation filesystem that supports many advanced storage technologies such as volume management, snapshots, checksumming, compression and {term}`deduplication`, replication and more. The Docker storage driver is called `zfs`.
- **Btrfs**: it is a copy-on-write filesystem included in the Linux kernel mainline. The Docker storage driver is called `btrfs`.
- **Device Mapper**: it is a kernel-based framework that underpins many advanced volume management technologies on Linux. The Docker storage driver is called `devicemapper`.
- **VFS**: it is not a union filesystem, instead, each layer is a directory on disk, and there is no copy-on-write support. To create a new layer, a "deep copy" is done of the previous layer. This driver does not perform well compared to the others, however, it is robust, stable and works in any environment. The Docker storage driver is called `vfs`.

The storage drivers accept some options via `storage-opts`, check [the storage driver documentation](https://docs.docker.com/storage/storagedriver/) for more information. Keep in mind that this is a {term}`JSON` file and all lines should end with a comma (`,`) except the last one.

## Networking

Networking in the context of containers refers to the ability of containers to communicate with each other and with non-Docker workloads. The Docker networking subsystem was implemented in a pluggable way, and we have different network drivers available to be used in different scenarios:

- **Bridge**: This is the default network driver. This is widely used when containers need to communicate among themselves in the same host.
- **Overlay**: It is used to make containers managed by different docker daemons (different hosts) communicate among themselves.
- **Host**: It is used when the networking isolation between the container and the host is not desired, the container will use the host’s networking capabilities directly.
- **IPvlan**: It is used to provide full control over the both IPv4 and IPv6 addressing.
- **Macvlan**: It is used to allow the assignment of Mac addresses to containers, making them appear as a physical device in the network.
- **None**: It is used to make the container completely isolated from the host.

## Logging

Monitoring what is happening in the system is a crucial part of systems administration, and with Docker containers it is no different. Docker provides the logging subsystem (which is pluggable) and there are many drivers that can forward container logs to a file, an external host, a database, or another logging back-end. The logs are basically everything written to `STDOUT` and `STDERR`. When building a Docker image, the relevant data should be forwarded to those I/O stream devices.

The following logging drivers are available (at the time of writing):

- **`json-file`**: it is the default logging driver. It writes logs in a file in JSON format.
- **`local`**: write logs to an internal storage that is optimized for performance and disk use.
- **{term}`journald`**: send logs to systemd journal.
- **`syslog`**: send logs to a syslog server.
- **`logentries`**: send container logs to the [Logentries](https://logentries.com/) server.
- **{term}`gelf`**: write logs in a {term}`Graylog` Extended Format which is understood by many tools, such as [Graylog](https://www.graylog.org/), [Logstash](https://www.elastic.co/products/logstash), and [Fluentd](https://www.fluentd.org).
- **`awslogs`**: send container logs to [Amazon CloudWatch Logs](https://aws.amazon.com/cloudwatch/details/#log-monitoring).
- **`etwlogs`**: forward container logs as ETW events. ETW stands for Event Tracing in Windows, and is the common framework for tracing applications in Windows. Not supported in Ubuntu systems.
- **{term}`fluentd`**: send container logs to the [Fluentd](https://www.fluentd.org) collector as structured log data.
- **{term}`gcplogs`**: send container logs to [Google Cloud Logging](https://cloud.google.com/logging/docs/) Logging.
- **`splunk`**: sends container logs to [HTTP Event Collector](https://dev.splunk.com/enterprise/docs/devtools/httpeventcollector/) in Splunk Enterprise and Splunk Cloud.

## Resources

To get a hands-on tutorial on using Docker for storage, networking, and logging, see:

- {ref}`Docker for system admins <docker-for-system-admins>`
