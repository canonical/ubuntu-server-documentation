(how-to-install-and-configure-nagios-core-3)=
# Install Nagios Core 3

> **Note**:
> Nagios Core 3 has been deprecated and is now replaced by Nagios Core 4. The `nagios3` package was last supported in Bionic, so subsequent releases should use `nagios4` instead.

The monitoring of essential servers and services is an important part of system administration. This guide walks through how to install and configure Nagios Core 3 for availability monitoring.

The example in this guide uses two servers with hostnames: **`server01`** and **`server02`**. 

`Server01` will be configured with Nagios to monitor services on itself and on `server02`, while `server02` will be configured to send data to `server01`.

## Install `nagios3` on `server01`

First, on `server01`, install the `nagios3` package by entering the following command into your terminal:

```bash
sudo apt install nagios3 nagios-nrpe-plugin
```

You will be asked to enter a password for the **nagiosadmin** user. The user's credentials are stored in `/etc/nagios3/htpasswd.users`. To change the nagiosadmin password, or add more users to the Nagios CGI scripts, use the `htpasswd` that is part of the `apache2-utils` package.

For example, to change the password for the nagiosadmin user, enter:

```bash
sudo htpasswd /etc/nagios3/htpasswd.users nagiosadmin
```

To add a user:

```bash
sudo htpasswd /etc/nagios3/htpasswd.users steve
```

## Install `nagios-nrpe-server` on `server02`

Next, on `server02` install the `nagios-nrpe-server` package. From a terminal on `server02` enter:

```bash
sudo apt install nagios-nrpe-server
```

> **Note**:
> NRPE allows you to execute local checks on remote hosts. There are other ways of accomplishing this through other Nagios plugins, as well as other checks.

## Configuration overview

There are a couple of directories containing Nagios configuration and check files.

- `/etc/nagios3`: Contains configuration files for the operation of the Nagios daemon, CGI files, hosts, etc.

- `/etc/nagios-plugins`: Contains configuration files for the service checks.

- `/etc/nagios`: On the remote host, contains the `nagios-nrpe-server` configuration files.

- `/usr/lib/nagios/plugins/`: Where the check binaries are stored. To see the options of a check use the `-h` option. For example: `/usr/lib/nagios/plugins/check_dhcp -h`

There are multiple checks Nagios can be configured to execute for any given host. For this example, Nagios will be configured to check disk space, DNS, and a MySQL hostgroup. The DNS check will be on `server02`, and the MySQL hostgroup will include both `server01` and `server02`.

> **Note**:
> See these guides for details on [setting up Apache](https://discourse.ubuntu.com/t/web-servers-apache/11510), [Domain Name Service](https://discourse.ubuntu.com/t/service-domain-name-service-dns/11318), and [MySQL](https://discourse.ubuntu.com/t/databases-mysql/11515).

Additionally, there are some terms that once explained will hopefully make understanding Nagios configuration easier:

- *Host*: A server, workstation, network device, etc. that is being monitored.

- *Host Group*: A group of similar hosts. For example, you could group all web servers, file server, etc.

- *Service*: The service being monitored on the host, such as HTTP, DNS, NFS, etc.

- *Service Group*: Allows you to group multiple services together. This is useful for grouping multiple HTTP for example.

- *Contact*: Person to be notified when an event takes place. Nagios can be configured to send emails, SMS messages, etc.

By default, Nagios is configured to check HTTP, disk space, SSH, current users, processes, and load on the **localhost**. Nagios will also ping check the **gateway**.

Large Nagios installations can be quite complex to configure. It is usually best to start small, with one or two hosts, to get things configured the way you want before expanding.

## Configure Nagios

### Create host config file for server02

First, create a **host** configuration file for `server02`. Unless otherwise specified, run all these commands on `server01`. In a terminal enter:

```bash
sudo cp /etc/nagios3/conf.d/localhost_nagios2.cfg \
/etc/nagios3/conf.d/server02.cfg
    
> **Note**:
> In all command examples, replace "`server01`", "`server02`", `172.18.100.100`, and `172.18.100.101` with the host names and IP addresses of your servers.

### Edit the host config file    

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

### Add service definition

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

A **mysql-servers** hostgroup now needs to be defined. Edit `/etc/nagios3/conf.d/hostgroups_nagios2.cfg` and add the following:

```text
# MySQL hostgroup.
define hostgroup {
        hostgroup_name  mysql-servers
                alias           MySQL servers
                members         localhost, server02
        }
```

The Nagios check needs to authenticate to MySQL. To add a `nagios` user to MySQL enter:

```bash    
mysql -u root -p -e "create user nagios identified by 'secret';"
```

> **Note**:
> The `nagios` user will need to be added to all hosts in the **mysql-servers** hostgroup.
    
Restart nagios to start checking the MySQL servers.
    
sudo systemctl restart nagios3.service

### Configure NRPE

Lastly configure NRPE to check the disk space on *server02*.
    
On `server01` add the service check to `/etc/nagios3/conf.d/server02.cfg`:

```text    
# NRPE disk check.
define service {
        use                     generic-service
        host_name               server02
        service_description     nrpe-disk
        check_command           check_nrpe_1arg!check_all_disks!172.18.100.101
}
```

Now on `server02` edit `/etc/nagios/nrpe.cfg` changing:

```text    
allowed_hosts=172.18.100.100
```

And below, in the command definition area, add:

```text
command[check_all_disks]=/usr/lib/nagios/plugins/check_disk -w 20% -c 10% -e
```
    
Finally, restart `nagios-nrpe-server`:

```bash
sudo systemctl restart nagios-nrpe-server.service
```
    
Also, on `server01` restart Nagios:

```bash    
sudo systemctl restart nagios3.service
```

You should now be able to see the host and service checks in the Nagios CGI files. To access them, point a browser to `http://server01/nagios3`. You will then be prompted for the **nagiosadmin** username and password.

## Further reading

This section has just scratched the surface of Nagios' features. The `nagios-plugins-extra` and `nagios-snmp-plugins` contain many more service checks.

- For more information about Nagios, see [the Nagios website](https://www.nagios.org/).

- The [Nagios Core Documentation](https://library.nagios.com/library/products/nagios-core/documentation/) and [Nagios Core 3 Documentation](https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/3/en/toc.html) may also be useful.

- They also provide a [list of books](https://www.nagios.org/propaganda/books/) related to Nagios and network monitoring.

- The [Nagios Ubuntu Wiki](https://help.ubuntu.com/community/Nagios3) page also has more details.
