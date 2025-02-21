(docker-for-system-admins)=
# Docker for system admins


Containers are widely used across multiple server workloads (databases and web servers, for instance), and understanding how to properly set up your server to run them is becoming more important for systems administrators. In this explanatory page, we are going to discuss some of the most important factors a system administrator needs to consider when setting up the environment to run Docker containers.

Understanding the options available to run Docker containers is key to optimising the use of computational resources in a given scenario/workload, which might have specific requirements. Some aspects that are important for system administrators are: **storage**, **networking** and **logging**. We are going to discuss each of these in the subsequent sections, presenting how to configure them and interact with the Docker command line interface (CLI).

## Storage

The first thing we need to keep in mind is that containers are ephemeral, and, unless configured otherwise, so are their data. Docker images are composed of one or more layers which are read-only, and once you run a container based on an image a new writable layer is created on top of the topmost image layer; the container can manage any type of data there. The content changes in the writable container layer are not persisted anywhere, and once the container is gone all the changes disappear. This behaviour presents some challenges to us: How can the data be persisted? How can it be shared among containers? How can it be shared between the host and the containers?

There are some important concepts in the Docker world that are the answer for some of those problems: they are **volumes**, **bind mounts** and **tmpfs**. Another question is how all those layers that form Docker images and containers will be stored, and for that we are going to talk about **storage drivers** (more on that later).

When we want to persist data we have two options:
* Volumes are the preferred way to persist data generated and used by Docker containers if your workload will generate a high volume of data, such as a database.
* Bind mounts are another option if you need to access files from the host, for example system files.

If what you want is to store some sensitive data in memory, like credentials, and do not want to persist it in either the host or the container layer, we can use tmpfs mounts.

### Volumes

The recommended way to persist data to and from Docker containers is by using volumes. Docker itself manages them, they are not OS-dependent and they can provide some interesting features for system administrators:

 * Easier to back up and migrate when compared to bind mounts;
 * Managed by the Docker CLI or API;
 * Safely shared among containers;
 * Volume drivers allow one to store data in remote hosts or in public cloud providers (also encrypting the data).

Moreover, volumes are a better choice than persisting data in the container layer, because volumes do not increase the size of the container, which can affect the life-cycle management performance.

Volumes can be created before or at the container creation time. There are two CLI options you can use to mount a volume in the container during its creation (`docker run` or `docker create`):

 * `--mount`: it accepts multiple key-value pairs (`<key>=<value>`). This is the preferred option to use.
    - `type`: for volumes it will always be `volume`;
    - `source` or `src`: the name of the volume, if the volume is anonymous (no name) this can be omitted;
    - `destination`, `dst` or `target`: the path inside the container where the volume will be mounted;
    - `readonly` or `ro` (optional): whether the volume should be mounted as read-only inside the container;
    - `volume-opt` (optional): a comma separated list of options in the format you would pass to the `mount` command.
 * `-v` or `--volume`: it accepts 3 parameters separated by colon (`:`):
    - First, the name of the volume. For the default `local` driver, the name should use only: letters in upper and lower case, numbers, `.`, `_` and `-`;
    - Second, the path inside the container where the volume will be mounted;
    - Third (optional), a comma-separated list of options in the format you would pass to the `mount` command, such as `rw`.

Here are a few examples of how to manage a volume using the Docker CLI:

```
# create a volume
$ docker volume create my-vol
my-vol
# list volumes
$ docker volume ls
DRIVER	VOLUME NAME
local 	my-vol
# inspect volume
$ docker volume inspect my-vol
[
	{
    	"CreatedAt": "2023-10-25T00:53:24Z",
    	"Driver": "local",
    	"Labels": null,
    	"Mountpoint": "/var/lib/docker/volumes/my-vol/_data",
    	"Name": "my-vol",
    	"Options": null,
    	"Scope": "local"
	}
]
# remove a volume
$ docker volume rm my-vol
my-vol
```

Running a container and mounting a volume:

```
$ docker run –name web-server -d \
    --mount source=my-vol,target=/app \
    ubuntu/apache2
0709c1b632801fddd767deddda0d273289ba423e9228cc1d77b2194989e0a882
```

After that, you can inspect your container to make sure the volume is mounted correctly:

```
$ docker inspect web-server --format '{{ json .Mounts }}' | jq .
[
  {
	"Type": "volume",
	"Name": "my-vol",
	"Source": "/var/lib/docker/volumes/my-vol/_data",
	"Destination": "/app",
	"Driver": "local",
	"Mode": "z",
	"RW": true,
	"Propagation": ""
  }
]
```

By default, all your volumes will be stored in `/var/lib/docker/volumes`.

### Bind mounts

Bind mounts are another option for persisting data, however, they have some limitations compared to volumes. Bind mounts are tightly associated with the directory structure and with the OS, but performance-wise they are similar to volumes in Linux systems.

In a scenario where a container needs to have access to any host system’s file or directory, bind mounts are probably the best solution. Some monitoring tools make use of bind mounts when executed as Docker containers.

Bind mounts can be managed via the Docker CLI, and as with volumes there are two options you can use:

 * `--mount`: it accepts multiple key-value pairs (`<key>=<value>`). This is the preferred option to use.
    - `type`: for bind mounts it will always be `bind`;
    - `source` or `src`: path of the file or directory on the host;
    - `destination`, `dst` or `target`: container’s directory to be mounted;
    - `readonly` or `ro` (optional): the bind mount is mounted in the container as read-only;
    - `volume-opt` (optional): it accepts any `mount` command option;
    - `bind-propagation` (optional): it changes the bind propagation. It can be `rprivate`, `private`, `rshared`, `shared`, `rslave`, `slave`.
 *  `-v` or `--volume`: it accepts 3 parameters separated by colon (`:`):
    - First, path of the file or directory on the host;
    - Second, path of the container where the volume will be mounted;
    - Third (optional), a comma separated of option in the format you would pass to `mount` command, such as `rw`.

An example of how you can create a Docker container and bind mount a host directory:

```
$ docker run -d \
    --name web-server \
    --mount type=bind,source="$(pwd)",target=/app \
    ubuntu/apache2
6f5378e34d6c6811702e16d047a5a80f18adbd9d8a14b11050ae3c3353bf8d2a
```

After that, you can inspect your container to check for the bind mount:

```
$ docker inspect web-server --format '{{ json .Mounts }}' | jq .
[
  {
	"Type": "bind",
	"Source": "/root",
	"Destination": "/app",
	"Mode": "",
	"RW": true,
	"Propagation": "rprivate"
  }
]
```

### Tmpfs

Tmpfs mounts allow users to store data temporarily in RAM memory, not in the host’s storage (via bind mount or volume) or in the container’s writable layer (with the help of storage drivers). When the container stops, the tmpfs mount will be removed and the data will not be persisted in any storage.

This is ideal for accessing credentials or security-sensitive information. The downside is that a tmpfs mount cannot be shared with multiple containers.

Tmpfs mounts can be managed via the Docker CLI with the following two options:

 * `--mount`: it accepts multiple key-value pairs (`<key>=<value>`). This is the preferred option to use.
    - `type`: for volumes it will always be `tmpfs`;
    - `destination`, `dst` or `target`: container’s directory to be mounted;
    - `tmpfs-size` and `tmpfs-mode` options (optional). For a full list see the [Docker documentation](https://docs.docker.com/storage/tmpfs/#specify-tmpfs-options).
  * `--tmpfs`: it accepts no configurable options, just mount the tmpfs for a standalone container.

An example of how you can create a Docker container and mount a tmpfs:

```
$ docker run --name web-server -d \
    --mount type=tmpfs,target=/app \
    ubuntu/apache2
03483cc28166fc5c56317e4ee71904941ec5942071e7c936524f74d732b6a24c
```

After that, you can inspect your container to check for the tmpfs mount:

```
$ docker inspect web-server --format '{{ json .Mounts }}' | jq .
[
  {
    "Type": "tmpfs",
    "Source": "",
    "Destination": "/app",
    "Mode": "",
    "RW": true,
    "Propagation": ""
  }
]
```

### Storage drivers

Storage drivers are used to store image layers and to store data in the writable layer of a container. In general, storage drivers are implemented trying to optimise the use of space, but write speed might be lower than native {term}`filesystem` performance depending on the driver in use. To better understand the options and make informed decisions, take a look at the Docker documentation on [how layers, images and containers work](https://docs.docker.com/storage/storagedriver/#images-and-layers).

The default storage driver is the `overlay2` which is backed by `OverlayFS`. This driver is recommended by upstream for use in production systems. The following storage drivers are available and are supported in Ubuntu (as at the time of writing):

 * **OverlayFS**: it is a modern union filesystem. The Linux kernel driver is called `OverlayFS` and the Docker storage driver is called `overlay2`. **This is the recommended driver**.
 * **ZFS**: it is a next generation filesystem that supports many advanced storage technologies such as volume management, snapshots, checksumming, compression and {term}`deduplication`, replication and more. The Docker storage driver is called `zfs`.
 * **Btrfs**: it is a copy-on-write filesystem included in the Linux kernel mainline. The Docker storage driver is called `btrfs`. 
 * **Device Mapper**: it is a kernel-based framework that underpins many advanced volume management technologies on Linux. The Docker storage driver is called `devicemapper`.
 * **VFS**: it is not a union filesystem, instead, each layer is a directory on disk, and there is no copy-on-write support. To create a new layer, a "deep copy" is done of the previous layer. This driver does not perform well compared to the others, however, it is robust, stable and works in any environment. The Docker storage driver is called `vfs`. 

If you want to use a different storage driver based on your specific requirements, you can add it to `/etc/docker/daemon.json` like in the following example:

```
{
  "storage-driver": "vfs"
}
```

The storage drivers accept some options via `storage-opts`, check [the storage driver documentation](https://docs.docker.com/storage/storagedriver/) for more information. Keep in mind that this is a {term}`JSON` file and all lines should end with a comma (`,`) except the last one.

Before changing the configuration above and restarting the daemon, make sure that the specified filesystem (zfs, btrfs, device mapper) is mounted in `/var/lib/docker`. Otherwise, if you configure the Docker daemon to use a storage driver different from the filesystem backing `/var/lib/docker` a failure will happen. The Docker daemon expects that `/var/lib/docker` is correctly set up when it starts.

## Networking

Networking in the context of containers refers to the ability of containers to communicate with each other and with non-Docker workloads. The Docker networking subsystem was implemented in a pluggable way, and we have different network drivers available to be used in different scenarios:

 * **Bridge**: This is the default network driver. This is widely used when containers need to communicate among themselves in the same host.
 * **Overlay**: It is used to make containers managed by different docker daemons (different hosts) communicate among themselves.
 * **Host**: It is used when the networking isolation between the container and the host is not desired, the container will use the host’s networking capabilities directly.
 * **IPvlan**: It is used to provide full control over the both IPv4 and IPv6 addressing.
 * **Macvlan**: It is used to allow the assignment of Mac addresses to containers, making them appear as a physical device in the network.
 * **None**: It is used to make the container completely isolated from the host.

This is how you can create a user-defined network using the Docker CLI:

```
# create network
$ docker network create --driver bridge my-net
D84efaca11d6f643394de31ad8789391e3ddf29d46faecf0661849f5ead239f7
# list networks
$ docker network ls
NETWORK ID 	NAME  	DRIVER	SCOPE
1f55a8891c4a   bridge	bridge	local
9ca94be2c1a0   host  	host  	local
d84efaca11d6   my-net	bridge	local
5d300e6a07b1   none  	null  	local
# inspect the network we created
$ docker network inspect my-net
[
	{
    	"Name": "my-net",
    	"Id": "d84efaca11d6f643394de31ad8789391e3ddf29d46faecf0661849f5ead239f7",
    	"Created": "2023-10-25T22:18:52.972569338Z",
    	"Scope": "local",
    	"Driver": "bridge",
    	"EnableIPv6": false,
    	"IPAM": {
        	"Driver": "default",
        	"Options": {},
        	"Config": [
            	{
                	"Subnet": "172.18.0.0/16",
                	"Gateway": "172.18.0.1"
            	}
        	]
    	},
    	"Internal": false,
    	"Attachable": false,
    	"Ingress": false,
    	"ConfigFrom": {
        	"Network": ""
    	},
    	"ConfigOnly": false,
    	"Containers": {},
    	"Options": {},
    	"Labels": {}
	}
]
```

Containers can connect to a defined network when they are created (via `docker run`) or can be connected to it at any time of its lifecycle:

```
$ docker run -d --name c1 --network my-net ubuntu/apache2
C7aa78f45ce3474a276ca3e64023177d5984b3df921aadf97e221da8a29a891e
$ docker inspect c1 --format '{{ json .NetworkSettings }}' | jq .
{
  "Bridge": "",
  "SandboxID": "ee1cc10093fdfdf5d4a30c056cef47abbfa564e770272e1e5f681525fdd85555",
  "HairpinMode": false,
  "LinkLocalIPv6Address": "",
  "LinkLocalIPv6PrefixLen": 0,
  "Ports": {
	"80/tcp": null
  },
  "SandboxKey": "/var/run/docker/netns/ee1cc10093fd",
  "SecondaryIPAddresses": null,
  "SecondaryIPv6Addresses": null,
  "EndpointID": "",
  "Gateway": "",
  "GlobalIPv6Address": "",
  "GlobalIPv6PrefixLen": 0,
  "IPAddress": "",
  "IPPrefixLen": 0,
  "IPv6Gateway": "",
  "MacAddress": "",
  "Networks": {
	"my-net": {
  	"IPAMConfig": null,
  	"Links": null,
  	"Aliases": [
    	"c7aa78f45ce3"
  	],
  	"NetworkID": "d84efaca11d6f643394de31ad8789391e3ddf29d46faecf0661849f5ead239f7",
  	"EndpointID": "1cb76d44a484d302137bb4b042c8142db8e931e0c63f44175a1aa75ae8af9cb5",
  	"Gateway": "172.18.0.1",
  	"IPAddress": "172.18.0.2",
  	"IPPrefixLen": 16,
  	"IPv6Gateway": "",
  	"GlobalIPv6Address": "",
  	"GlobalIPv6PrefixLen": 0,
  	"MacAddress": "02:42:ac:12:00:02",
  	"DriverOpts": null
	}
  }
}
# make a running container connect to the network
$ docker run -d --name c2 ubuntu/nginx
Fea22fbb6e3685eae28815f3ad8c8a655340ebcd6a0c13f3aad0b45d71a20935
$ docker network connect my-net c2
$ docker inspect c2 --format '{{ json .NetworkSettings }}' | jq .
{
  "Bridge": "",
  "SandboxID": "82a7ea6efd679dffcc3e4392e0e5da61a8ccef33dd78eb5381c9792a4c01f366",
  "HairpinMode": false,
  "LinkLocalIPv6Address": "",
  "LinkLocalIPv6PrefixLen": 0,
  "Ports": {
	"80/tcp": null
  },
  "SandboxKey": "/var/run/docker/netns/82a7ea6efd67",
  "SecondaryIPAddresses": null,
  "SecondaryIPv6Addresses": null,
  "EndpointID": "490c15cf3bcb149dd8649e3ac96f71addd13f660b4ec826dc39e266184b3f65b",
  "Gateway": "172.17.0.1",
  "GlobalIPv6Address": "",
  "GlobalIPv6PrefixLen": 0,
  "IPAddress": "172.17.0.3",
  "IPPrefixLen": 16,
  "IPv6Gateway": "",
  "MacAddress": "02:42:ac:11:00:03",
  "Networks": {
	"bridge": {
  	"IPAMConfig": null,
  	"Links": null,
  	"Aliases": null,
  	"NetworkID": "1f55a8891c4a523a288aca8881dae0061f9586d5d91c69b3a74e1ef3ad1bfcf4",
  	"EndpointID": "490c15cf3bcb149dd8649e3ac96f71addd13f660b4ec826dc39e266184b3f65b",
  	"Gateway": "172.17.0.1",
  	"IPAddress": "172.17.0.3",
  	"IPPrefixLen": 16,
  	"IPv6Gateway": "",
  	"GlobalIPv6Address": "",
  	"GlobalIPv6PrefixLen": 0,
  	"MacAddress": "02:42:ac:11:00:03",
  	"DriverOpts": null
	},
	"my-net": {
  	"IPAMConfig": {},
  	"Links": null,
  	"Aliases": [
    	"fea22fbb6e36"
  	],
  	"NetworkID": "d84efaca11d6f643394de31ad8789391e3ddf29d46faecf0661849f5ead239f7",
  	"EndpointID": "17856b7f6902db39ff6ab418f127d75d8da597fdb8af0a6798f35a94be0cb805",
  	"Gateway": "172.18.0.1",
  	"IPAddress": "172.18.0.3",
  	"IPPrefixLen": 16,
  	"IPv6Gateway": "",
  	"GlobalIPv6Address": "",
  	"GlobalIPv6PrefixLen": 0,
  	"MacAddress": "02:42:ac:12:00:03",
  	"DriverOpts": {}
	}
  }
}
```

The default network created by the Docker daemon is called `bridge` using the bridge network driver. A system administrator can configure this network by editing `/etc/docker/daemon.json`:

```
{
  "bip": "192.168.1.1/24",
  "fixed-cidr": "192.168.1.0/25",
  "fixed-cidr-v6": "2001:db8::/64",
  "mtu": 1500,
  "default-gateway": "192.168.1.254",
  "default-gateway-v6": "2001:db8:abcd::89",
  "dns": ["10.20.1.2","10.20.1.3"]
}
```

After deciding how you are going to manage the network and selecting the most appropriate driver, there are some specific deployment details that a system administrator has to bear in mind when running containers.

Exposing ports of any system is always a concern, since it increases the surface for malicious attacks. For containers, we also need to be careful, analysing whether we really need to publish ports to the host. For instance, if the goal is to allow containers to access a specific port from another container, there is no need to publish any port to the host. This can be solved by connecting all the containers to the same network. You should publish ports of a container to the host only if you want to make it available to non-Docker workloads. When a container is created no port is published to the host, the option `--publish` (or `-p`) should be passed to `docker run` or `docker create` listing which port will be exposed and how.

The `--publish` option of Docker CLI accepts the following options:

* First, the host port that will be used to publish the container’s port. It can also contain the IP address of the host. For example, `0.0.0.0:8080`.
* Second, the container’s port to be published. For example, `80`.
* Third (optional), the type of port that will be published which can be TCP or UDP. For example, `80/tcp` or `80/udp`.

An example of how to publish port `80` of a container to port `8080` of the host:

```
$ docker run -d --name web-server --publish 8080:80 ubuntu/nginx
f451aa1990db7d2c9b065c6158e2315997a56a764b36a846a19b1b96ce1f3910
$ docker inspect web-server --format '{{ json .NetworkSettings.Ports }}' | jq .
{
  "80/tcp": [
	{
  	"HostIp": "0.0.0.0",
  	"HostPort": "8080"
	},
	{
  	"HostIp": "::",
  	"HostPort": "8080"
	}
  ]
}
```

The `HostIp` values are `0.0.0.0` (IPv4) and `::` (IPv6), and the service running in the container is accessible to everyone in the network (reaching the host), if you want to publish the port from the container and let the service be available just to the host you can use `--publish 127.0.0.1:8080:80` instead. The published port can be TCP or UDP and one can specify that passing `--publish 8080:80/tcp` or `--publish 8080:80/udp`.

The system administrator might also want to manually set the IP address or the hostname of the container. To achieve this, one can use the `--ip` (IPv4), `--ip6` (IPv6), and `--hostname` options of the `docker network connect` command to specify the desired values.

Another important aspect of networking with containers is the {term}`DNS` service. By default containers will use the DNS setting of the host, defined in `/etc/resolv.conf`. Therefore, if a container is created and connected to the default `bridge` network it will get a copy of host’s `/etc/resolv.conf`. If the container is connected to a user-defined network, then it will use Docker's embedded DNS server. The embedded DNS server forwards external DNS lookups to the DNS servers configured on the host. In case the system administrator wants to configure the DNS service, the `docker run` and `docker create` commands have options to allow that, such as `--dns` (IP address of a DNS server) and `--dns-opt` (key-value pair representing a DNS option and its value). For more information, check the manpages of those commands.

## Logging

Monitoring what is happening in the system is a crucial part of systems administration, and with Docker containers it is no different. Docker provides the logging subsystem (which is pluggable) and there are many drivers that can forward container logs to a file, an external host, a database, or another logging back-end. The logs are basically everything written to `STDOUT` and `STDERR`. When building a Docker image, the relevant data should be forwarded to those I/O stream devices.

The following storage drivers are available (at the time of writing):

 * **json-file**: it is the default logging driver. It writes logs in a file in JSON format.
 * **local**: write logs to an internal storage that is optimised for performance and disk use.
 * **{term}`journald`**: send logs to systemd journal.
 * **syslog**: send logs to a syslog server.
 * **logentries**: send container logs to the [Logentries](https://logentries.com/) server.
 * **gelf**: write logs in a Graylog Extended Format which is understood by many tools, such as [Graylog](https://www.graylog.org/), [Logstash](https://www.elastic.co/products/logstash), and [Fluentd](https://www.fluentd.org).
 * **awslogs**: send container logs to [Amazon CloudWatch Logs](https://aws.amazon.com/cloudwatch/details/#log-monitoring).
 * **etwlogs**: forward container logs as ETW events. ETW stands for Event Tracing in Windows, and is the common framework for tracing applications in Windows. Not supported in Ubuntu systems.
 * **{term}`fluentd`**: send container logs to the [Fluentd](https://www.fluentd.org) collector as structured log data.
 * **gcplogs**: send container logs to [Google Cloud Logging](https://cloud.google.com/logging/docs/) Logging.
 * **splunk**: sends container logs to [HTTP Event Collector](https://dev.splunk.com/enterprise/docs/devtools/httpeventcollector/) in Splunk Enterprise and Splunk Cloud.

The default logging driver is `json-file`, and the system administrator can change it by editing the `/etc/docker/daemon.json`:

```
{
  "log-driver": "journald"
}
```

Another option is specifying the logging driver during container creation time:

```
$ docker run -d --name web-server --log-driver=journald ubuntu/nginx
1c08b667f32d8b834f0d9d6320721e07de5f22168cfc8a024d6e388daf486dfa
$ docker inspect web-server --format '{{ json .HostConfig.LogConfig }}' | jq .
{
  "Type": "journald",
  "Config": {}
}
$ docker logs web-server
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
```

Depending on the driver you might also want to pass some options. You can do that via the CLI, passing `--log-opt` or in the daemon config file adding the key `log-opts`. For more information check the logging driver documentation.

Docker CLI also provides the `docker logs` and `docker service logs` commands which allows one to check for the logs produced by a given container or service (set of containers) in the host. However, those two commands are functional only if the logging driver for the containers is `json-file`, `local` or `journald`. They are useful for debugging in general, but there is the downside of increasing the storage needed in the host.

The remote logging drivers are useful to store data in an external service/host, and they also avoid spending more disk space in the host to store log files. Nonetheless, sometimes, for debugging purposes, it is important to have log files locally. Considering that, Docker has a feature called “dual logging”, which is enabled by default, and even if the system administrator configures a logging driver different from `json-file`, `local` and `journald`, the logs will be available locally to be accessed via the Docker CLI. If this is not the desired behaviour, the feature can be disabled in the `/etc/docker/daemon.json` file:

```
{
  "log-driver": "syslog",
  "log-opts": {
            “cache-disabled”: “true”,
	"syslog-address": "udp://1.2.3.4:1111"
  }
}
```

The option `cache-disabled` is used to disable the “dual logging” feature. If you try to run `docker logs` with that configuration you will get the following error:

```
$ docker logs web-server
Error response from daemon: configured logging driver does not support reading
```
