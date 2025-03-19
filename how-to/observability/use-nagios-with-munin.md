(use-nagios-with-munin)=
# How to use Nagios with Munin

> **Note**:
> Nagios Core 3 has been deprecated and is now replaced by Nagios Core 4. The `nagios3` package was last supported in Bionic, so subsequent releases should use `nagios4` instead.

The monitoring of essential servers and services is an important part of system administration. Most network services are monitored for performance, availability, or both. This section will cover installation and configuration of Nagios 3 for availability monitoring alongside Munin for performance monitoring.

The examples in this section will use two servers with hostnames **`server01`** and **`server02`**. `Server01` will be configured with Nagios 3 to monitor services on both itself and `server02`. `Server01` will also be set up with the Munin package to gather information from the network. Using the `munin-node` package, `server02` will be configured to send information to `server01`.

## Install Nagios 3

### On server01

First, on `server01`, install the `nagios3` package. In a terminal, enter:

```bash
sudo apt install nagios3 nagios-nrpe-plugin
```

You will be asked to enter a password for the `nagiosadmin` user. The user's credentials are stored in `/etc/nagios3/htpasswd.users`. To change the `nagiosadmin` password, or add additional users to the Nagios CGI scripts, use the `htpasswd` that is part of the `apache2-utils` package.

For example, to change the password for the `nagiosadmin` user enter:

```bash
sudo htpasswd /etc/nagios3/htpasswd.users nagiosadmin
```

To add a user:

```bash
sudo htpasswd /etc/nagios3/htpasswd.users steve
```

### On server02

Next, on `server02` install the `nagios-nrpe-server` package. From a terminal on `server02`, enter:

```bash
sudo apt install nagios-nrpe-server
```

> **Note**:
> NRPE allows you to run local checks on remote hosts. There are other ways of accomplishing this, including through other Nagios plugins.

### Configuration overview

There are a few directories containing Nagios configuration and check files.

- `/etc/nagios3`: contains configuration files for the operation of the Nagios daemon, CGI files, hosts, etc.

- `/etc/nagios-plugins`: houses configuration files for the service checks.

- `/etc/nagios`: is located on the remote host and contains the `nagios-nrpe-server` configuration files.

- `/usr/lib/nagios/plugins/`: where the check binaries are stored. To see the options of a check use the `-h` option.
    
  For example: `/usr/lib/nagios/plugins/check_dhcp -h`

There are many checks Nagios can be configured to run for any particular host. In this example, Nagios will be configured to check disk space, {term}`DNS`, and a MySQL {term}`host group <hostgroup>`. The DNS check will be on `server02`, and the MySQL host group will include both `server01` and `server02`.

> **Note**:
> See these additional guides for details on setting up {ref}`Apache <install-apache2>`, {ref}`Domain Name Service (DNS) <install-dns>`, and {ref}`MySQL <install-mysql>`.

Additionally, there are some terms that once explained will hopefully make understanding Nagios configuration easier:

- **Host**: a server, workstation, network device, etc that is being monitored.

- **Host group**: a group of similar hosts. For example, you could group all web servers, file servers, etc.

- **Service**: the service being monitored on the host, such as HTTP, DNS, NFS, etc.

- **Service group**: allows you to group multiple services together. This is useful for grouping, e.g.,  multiple HTTP.

- **Contact**: the person to be notified when an event takes place. Nagios can be configured to send emails, SMS messages, etc.

By default Nagios is configured to check HTTP, disk space, SSH, current users, processes, and load on the **localhost**. Nagios will also ping-check the **gateway**.

Large Nagios installations can be quite complex to configure. It is usually best to start small (i.e. with one or two hosts), get things configured the way you like, and then expand.

## Configure Nagios

First, create a **host** configuration file for `server02`. Unless otherwise specified, run all these commands on `server01`. In a terminal enter:

```bash
sudo cp /etc/nagios3/conf.d/localhost_nagios2.cfg \
/etc/nagios3/conf.d/server02.cfg
```
    
> **Note**:
> In the above and following command examples, replace "`server01`", "`server02`", `172.18.100.100`, and `172.18.100.101` with the host names and IP addresses of your servers.

Next, edit `/etc/nagios3/conf.d/server02.cfg`:

```text    
define host{
        use                     generic-host  ; Name of host template to use
        host_name               server02
        alias                   Server 02
        address                 172.18.100.101
}
        
# check DNS service.
define service {
        use                             generic-service
        host_name                       server02
        service_description             DNS
        check_command                   check_dns!172.18.100.101
}
```

Restart the Nagios daemon to enable the new configuration:

```bash
sudo systemctl restart nagio3.service
```

Now add a service definition for the MySQL check by adding the following to `/etc/nagios3/conf.d/services_nagios2.cfg`:

```text
# check MySQL servers.
define service {
        hostgroup_name        mysql-servers
        service_description   MySQL
        check_command         check_mysql_cmdlinecred!nagios!secret!$HOSTADDRESS
        use                   generic-service
        notification_interval 0 ; set > 0 if you want to be renotified
}
```

A **mysql-servers** host group now needs to be defined. Edit `/etc/nagios3/conf.d/hostgroups_nagios2.cfg` adding:

```text
# MySQL hostgroup.
define hostgroup {
        hostgroup_name  mysql-servers
                alias           MySQL servers
                members         localhost, server02
}

The Nagios check needs to authenticate to MySQL. To add a `nagios` user to MySQL, enter:

```bash
mysql -u root -p -e "create user nagios identified by 'secret';"
    
> **Note**:
> The `nagios` user will need to be added all hosts in the `mysql-servers` host group.
    
Restart Nagios to start checking the MySQL servers.

```bash
sudo systemctl restart nagios3.service
```

Lastly, configure NRPE to check the disk space on `server02`. On `server01` add the service check to `/etc/nagios3/conf.d/server02.cfg`:

```text    
# NRPE disk check.
define service {
        use                     generic-service
        host_name               server02
        service_description     nrpe-disk
        check_command           check_nrpe_1arg!check_all_disks!172.18.100.101
}
```

Now on `server02` edit `/etc/nagios/nrpe.cfg`, changing:

```text
allowed_hosts=172.18.100.100
```

And below in the command definition area add:

```text
command[check_all_disks]=/usr/lib/nagios/plugins/check_disk -w 20% -c 10% -e
```

Finally, restart `nagios-nrpe-server`:

```bash    
sudo systemctl restart nagios-nrpe-server.service
```

Also, on `server01` restart `nagios3`:

```bash
sudo systemctl restart nagios3.service
```

You should now be able to see the host and service checks in the Nagios CGI files. To access them, point a browser to `http://server01/nagios3`. You will then be prompted for the `nagiosadmin` username and password.

## Install Munin

Before installing Munin on `server01` Apache2 will need to be installed. The default configuration is fine for running a Munin server. For more information see {ref}`setting up Apache <install-apache2>`.

### On server01

First, on `server01` install `munin` by running the following command in a terminal:

```bash
sudo apt install munin
```

### On server02

Now on `server02` install the `munin-node` package:

```bash
sudo apt install munin-node
```

### Configure Munin on server01

On `server01` edit the `/etc/munin/munin.conf` to add the IP address for `server02`:

```text
## First our "normal" host.
[server02]
       address 172.18.100.101
```

> **Note**:
> Replace `server02` and `172.18.100.101` with the actual hostname and IP address of your server.

### Configure munin-node on server02

To configure `munin-node` on `server02`, edit `/etc/munin/munin-node.conf` to allow access by `server01`:

```text
allow ^172\.18\.100\.100$
```

> **Note**:
> Replace `^172\.18\.100\.100$` with IP address for your Munin server.

Now restart `munin-node` on `server02` for the changes to take effect:

```bash
sudo systemctl restart munin-node.service
```

Finally, in a browser go to `http://server01/munin`, and you should see links to some graphs displaying information from the standard `munin-plugins` for disk, network, processes, and system.

> **Note**:
> Since this is a new install it may take some time for the graphs to display anything useful.

### Additional plugins

The `munin-plugins-extra` package contains performance checks and additional services such as DNS, {term}`DHCP`, Samba, etc. To install the package, from a terminal enter:

```bash
sudo apt install munin-plugins-extra
```

Be sure to install the package on both the server and node machines.

## Further reading

- See the [Munin](http://munin-monitoring.org/) and [Nagios](https://www.nagios.org/) websites for more details on these packages.
- The [Munin Documentation](https://munin.readthedocs.io/en/latest/) page includes information on additional plugins, writing plugins, etc.
- The [Nagios Online Documentation](https://www.nagios.org/documentation/) site.
- There is also a [list of books](https://www.nagios.org/propaganda/books/) related to Nagios and network monitoring.
- The [Nagios Ubuntu Wiki](https://help.ubuntu.com/community/Nagios3) page also has more details.
