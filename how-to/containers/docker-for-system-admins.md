(docker-for-system-admins)=
# Docker for system admins

We are going to explore set-ups for configuring storage, networking, and logging in the subsequent sections. This will also help you get familiarized with Docker command line interface (CLI).

## Installation

First, install Docker if it’s not already installed:

```bash
$ sudo apt-get install -y docker.io docker-compose-v2
```

## Configuring storage

### How to configure volumes

- Create a volume

  ```bash
  $ docker volume create my-vol
  my-vol
  ```

- List volumes

  ```bash
  $ docker volume ls

  DRIVER	VOLUME NAME
  local 	my-vol
  ```

- Inspect volume

  ```bash
  $ docker volume inspect my-vol
  ```

  ```json
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
  ```

- Running a container and mounting a volume:

  ```bash
  $ docker run –name web-server -d \
  	--mount source=my-vol,target=/app \
  	ubuntu/apache2

  0709c1b632801fddd767deddda0d273289ba423e9228cc1d77b2194989e0a882
  ```

- Inspect your container to make sure the volume is mounted correctly:

  ```bash
  $ docker inspect web-server --format '{{ json .Mounts }}' | jq .
  ```

  ```json
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

- Stop the container and remove its volume

  ```bash
  $ docker stop web-server
  $ docker volume rm my-vol

  my-vol
  ```

### How to configure bind mounts

- Create a Docker container and bind mount a host directory:

  ```bash
  $ docker run -d \
  	--name web-server \
  	--mount type=bind,source="$(pwd)",target=/app \
  	ubuntu/apache2

  6f5378e34d6c6811702e16d047a5a80f18adbd9d8a14b11050ae3c3353bf8d2a
  ```

- Inspect your container to check for the bind mount:

  ```bash
  $ docker inspect web-server --format '{{ json .Mounts }}' | jq .
  ```

  ```json
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

### How to configure Tmpfs

- How you can create a Docker container and mount a tmpfs:

  ```bash
  $ docker run --name web-server -d \
  	--mount type=tmpfs,target=/app \
  	ubuntu/apache2

  03483cc28166fc5c56317e4ee71904941ec5942071e7c936524f74d732b6a24c
  ```

- Inspect your container to check for the tmpfs mount:

  ```bash
  $ docker inspect web-server --format '{{ json .Mounts }}' | jq .
  ```

  ```json
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

### Choosing the right storage drivers

- Check the current storage driver

  ```bash
  $ docker info | grep "Storage Driver"

  Storage Driver: overlay2
  ```

- Change the storage driver

  1.  Stop the docker daemon

      ```bash
      systemctl stop docker
      ```

  1.  Edit `/etc/docker/daemon.json`

      ```json
      {
        "storage-driver": "ZFS"
      }
      ```

  1.  Restart the docker daemon

      ```bash
      systemctl start docker
      ```

Before changing the configuration above and restarting the daemon, make sure that the specified filesystem (zfs, btrfs, device mapper) is mounted in `/var/lib/docker`. Otherwise, if you configure the Docker daemon to use a storage driver different from the filesystem backing `/var/lib/docker` a failure will happen. The Docker daemon expects that `/var/lib/docker` is correctly set up when it starts.

## Configuring networking

This is how you can create a user-defined network using the Docker CLI:

- Create network

  ```bash
  $ docker network create --driver bridge my-net

  D84efaca11d6f643394de31ad8789391e3ddf29d46faecf0661849f5ead239f7
  ```

- List networks

  ```bash
  $ docker network ls

  NETWORK ID 	NAME  	DRIVER	SCOPE
  1f55a8891c4a   bridge	bridge	local
  9ca94be2c1a0   host  	host  	local
  d84efaca11d6   my-net	bridge	local
  5d300e6a07b1   none  	null  	local
  ```

- Inspect the network we created

  ```bash
  $ docker network inspect my-net
  ```

  ```json
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

- Containers can connect to a defined network when they are created (via `docker run`) or can be connected to it at any time of its lifecycle.

  ```bash
  $ docker run -d --name c1 --network my-net ubuntu/apache2

  C7aa78f45ce3474a276ca3e64023177d5984b3df921aadf97e221da8a29a891e
  ```

- View the network connected to the container

  ```bash
  $ docker inspect c1 --format '{{ json .NetworkSettings }}' | jq .
  ```

  ```json
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
        "Aliases": ["c7aa78f45ce3"],
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
  ```

- Make a running container connect to the existing network

  1.  Create the container

      ```bash
      $ docker run -d --name c2 ubuntu/nginx

      Fea22fbb6e3685eae28815f3ad8c8a655340ebcd6a0c13f3aad0b45d71a20935
      ```

  1.  Connect the running container to the network and verify that it's connected.

      ```bash
      $ docker network connect my-net c2
      $ docker inspect c2 --format '{{ json .NetworkSettings }}' | jq .
      ```

      ```json
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
            "Aliases": ["fea22fbb6e36"],
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

The default network created by the Docker daemon is called `bridge` using the bridge network driver. A system administrator can modify this default network by editing `/etc/docker/daemon.json`:

```json
{
  "bip": "192.168.1.1/24",
  "fixed-cidr": "192.168.1.0/25",
  "fixed-cidr-v6": "2001:db8::/64",
  "mtu": 1500,
  "default-gateway": "192.168.1.254",
  "default-gateway-v6": "2001:db8:abcd::89",
  "dns": ["10.20.1.2", "10.20.1.3"]
}
```

After deciding how you are going to manage the network and selecting the most appropriate driver, there are some specific deployment details that a system administrator has to bear in mind when running containers.

Exposing ports of any system is always a concern, since it increases the surface for malicious attacks. For containers, we also need to be careful, analysing whether we really need to publish ports to the host. For instance, if the goal is to allow containers to access a specific port from another container, there is no need to publish any port to the host. This can be solved by connecting all the containers to the same network. You should publish ports of a container to the host only if you want to make it available to non-Docker workloads. When a container is created no port is published to the host, the option `--publish` (or `-p`) should be passed to `docker run` or `docker create` listing which port will be exposed and how.

The `--publish` option of Docker CLI accepts the following options:

- First, the host port that will be used to publish the container’s port. It can also contain the IP address of the host. For example, `0.0.0.0:8080`.
- Second, the container’s port to be published. For example, `80`.
- Third (optional), the type of port that will be published which can be TCP or UDP. For example, `80/tcp` or `80/udp`.

An example of how to publish port `80` of a container to port `8080` of the host:

```bash
$ docker run -d --name web-server --publish 8080:80 ubuntu/nginx

f451aa1990db7d2c9b065c6158e2315997a56a764b36a846a19b1b96ce1f3910

$ docker inspect web-server --format '{{ json .NetworkSettings.Ports }}' | jq .
```

```json
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

## Managing logs

The default logging driver is specified in a json file, and the system administrator can change it by editing the `/etc/docker/daemon.json` file.

```json
{
  "log-driver": "journald"
}
```

Another option is specifying the logging driver during container creation time:

```bash
$ docker run -d --name web-server --log-driver=journald ubuntu/nginx

1c08b667f32d8b834f0d9d6320721e07de5f22168cfc8a024d6e388daf486dfa

$ docker inspect web-server --format '{{ json .HostConfig.LogConfig }}' | jq .
```

```json
{
  "Type": "journald",
  "Config": {}
}
```

```bash
$ docker logs web-server

/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
```

Depending on the driver you might also want to pass some options. You can do that via the CLI, passing `--log-opt` or in the daemon config file adding the key `log-opts`. For more information check the logging driver documentation.

Docker CLI also provides the `docker logs` and `docker service logs` commands which allows one to check for the logs produced by a given container or service (set of containers) in the host. However, those two commands are functional only if the logging driver for the containers is `json-file`, `local` or `journald`. They are useful for debugging in general, but there is the downside of increasing the storage needed in the host.

The remote logging drivers are useful to store data in an external service/host, and they also avoid spending more disk space in the host to store log files. Nonetheless, sometimes, for debugging purposes, it is important to have log files locally. Considering that, Docker has a feature called “dual logging”, which is enabled by default, and even if the system administrator configures a logging driver different from `json-file`, `local` and `journald`, the logs will be available locally to be accessed via the Docker CLI. If this is not the desired behaviour, the feature can be disabled in the `/etc/docker/daemon.json` file:

```json
{
  "log-driver": "syslog",
  "log-opts": {
    "cache-disabled": "true",
    "syslog-address": "udp://1.2.3.4:1111"
  }
}
```

The option `cache-disabled` is used to disable the “dual logging” feature. If you try to run `docker logs` with that configuration you will get the following error:

```bash
$ docker logs web-server

Error response from daemon: configured logging driver does not support reading
```
