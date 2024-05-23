# How to install and configure isc-kea

In this guide we show how to install and configure `isc-kea` in Ubuntu 23.04
or greater. [Kea](https://www.isc.org/kea/) is the DHCP server developed by ISC to replace `isc-dhcp`. It is newer and designed for more modern network environments.

For `isc-dhcp-server` instructions, [refer to this guide instead](how-to-install-and-configure-isc-dhcp-server.md).

## Install isc-kea

At a terminal prompt, enter the following command to install `isc-kea`:

```bash
sudo apt install kea
```

This will also install a few binary packages, including

* `kea-dhcp4-server`: The IPv4 DHCP server (the one we will configure in this guide).
* `kea-dhcp6-server`: The IPv6 DHCP server.
* `kea-ctrl-agent`: A REST API service for Kea.
* `kea-dhcp-ddns-server`: A Dynamic DNS service to update DNS based on DHCP lease events.

Since the `kea-ctrl-agent` service has some administrative rights to the Kea
services, we need to ensure regular users are not allowed to use the API
without permissions. Ubuntu does it by requiring user authentication to access
the `kea-ctrl-agent` API service ([LP: #2007312 has more details on this](https://bugs.launchpad.net/ubuntu/+source/isc-kea/+bug/2007312)).

Therefore, the installation process described above will get a debconf "high"
priority prompt with 3 options:

* no action (default);
* configure with a random password; or
* configure with a given password.

If there is no password, the `kea-ctrl-agent` will **not** start.

The password is expected to be in `/etc/kea/kea-api-password`, with ownership
`root:_kea` and permissions `0640`. To change it, run `dpkg-reconfigure kea-ctrl-agent`
(which will present the same 3 options from above again), or just edit the file
manually.

## Configure kea-dhcp4

The `kea-dhcp4` service can be configured by editing `/etc/kea/kea-dhcp4.conf`.

Most commonly, what you want to do is let Kea assign an IP address from a
pre-configured IP address pool. This can be done with settings as follows:

```json
{
  "Dhcp4": {
	"interfaces-config": {
  	"interfaces": [ "eth4" ]
	},
	"control-socket": {
    	"socket-type": "unix",
    	"socket-name": "/run/kea/kea4-ctrl-socket"
	},
	"lease-database": {
    	"type": "memfile",
    	"lfc-interval": 3600
	},
	"valid-lifetime": 600,
	"max-valid-lifetime": 7200,
	"subnet4": [
  	{
    	"id": 1,
    	"subnet": "192.168.1.0/24",
    	"pools": [
      	{
        	"pool": "192.168.1.150 - 192.168.1.200"
      	}
    	],
    	"option-data": [
      	{
        	"name": "routers",
        	"data": "192.168.1.254"
      	},
      	{
        	"name": "domain-name-servers",
        	"data": "192.168.1.1, 192.168.1.2"
      	},
      	{
        	"name": "domain-name",
        	"data": "mydomain.example"
      	}
    	]
  	}
	]
  }
}
```

This will result in the DHCP server listening on interface "eth4", giving clients an IP address from the range `192.168.1.150 - 192.168.1.200`. It will lease an IP address for 600 seconds if the client doesn't ask for a specific time frame. Otherwise the maximum (allowed) lease will be 7200 seconds. The server will also "advise" the client to use `192.168.1.254` as the default-gateway and `192.168.1.1` and `192.168.1.2` as its DNS servers.

After changing the config file you can reload the server configuration through `kea-shell` with the following command (considering you have the `kea-ctrl-agent` running as described above):

```bash
kea-shell --host 127.0.0.1 --port 8000 --auth-user kea-api --auth-password $(cat /etc/kea/kea-api-password) --service dhcp4 config-reload
```

Then, press <kbd>ctrl</kbd>-<kbd>d</kbd>. The server should respond with:

```json
[ { "result": 0, "text": "Configuration successful." } ]
```

meaning your configuration was received by the server.

The `kea-dhcp4-server` service logs should contain an entry similar to:

```
DHCP4_DYNAMIC_RECONFIGURATION_SUCCESS dynamic server reconfiguration succeeded with file: /etc/kea/kea-dhcp4.conf
```

signaling that the server was successfully reconfigured.

You can read `kea-dhcp4-server` service logs with `journalctl`:

```bash
journalctl -u kea-dhcp4-server
```

Alternatively, instead of reloading the DHCP4 server configuration through
`kea-shell`,  you can restart the `kea-dhcp4-service` with:

```bash
systemctl restart kea-dhcp4-server
```

## Further reading

- [ISC Kea Documentation](https://kb.isc.org/docs/kea-administrator-reference-manual)
