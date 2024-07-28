(how-to-install-and-use-puppet)=
# How to install and use Puppet

Puppet is a cross-platform framework for system administrators to perform common tasks using code.

The code can perform a variety of tasks, from installing new software, to checking file permissions, to updating user accounts. Puppet is used from the initial installation of a system and throughout the system's life cycle. In most circumstances, Puppet will be used in a client/server configuration.

This page will demonstrate how to install and configure Puppet in a client/server configuration, with the simple example of installing Apache using Puppet.

## Pre-configuration

Before configuring Puppet, you may want to add a DNS `CNAME` record for `puppet.example.com`, where `example.com` is your domain.

By default, Puppet clients check DNS for `puppet.example.com` as the puppet server name, or **Puppet Master**. See [Domain Name Server](../docs/how-to/domain-name-service-dns.md) for more details.

If you do not want to use DNS, you can add entries to the server and client `/etc/hosts` file. For example, in the Puppet server's `/etc/hosts` file add:

```text
127.0.0.1 localhost.localdomain localhost puppet
192.168.1.17 puppetclient.example.com puppetclient
```

On each Puppet client, add an entry for the server:

```text
192.168.1.16 puppetmaster.example.com puppetmaster puppet
```

> **Note**:
> Replace the example IP addresses and domain names above with your actual server and client addresses and domain names.

## Install Puppet

To install Puppet, run the following command in a terminal on the **server**:

```bash
sudo apt install puppetmaster
```

On the **client** machine, or machines, enter:

```bash
sudo apt install puppet
```

## Configure Puppet

Create a folder path for the Apache2 class:

```bash
sudo mkdir -p /etc/puppet/modules/apache2/manifests
```

Now setup some resources for Apache2. Create a file `/etc/puppet/modules/apache2/manifests/init.pp` containing the following:

```
class apache2 {
  package { 'apache2':
    ensure => installed,
  }

  service { 'apache2':
    ensure  => true,
    enable  => true,
    require => Package['apache2'],
  }
}
```

Next, create a node file `/etc/puppet/code/environments/production/manifests/site.pp` with:

```
node 'puppetclient.example.com' {
   include apache2
}
```

> **Note**:
> Replace `puppetclient.example.com` with your Puppet client's host name.

The final step for this simple Puppet server is to restart the daemon:

```bash
sudo systemctl restart puppetmaster.service
```

Now everything is configured on the Puppet server, it is time to configure the client.

First, configure the Puppet agent daemon to start. Edit `/etc/default/puppet`, changing `START` to `yes`:

```
START=yes
```

Then start the service:

```bash
sudo systemctl start puppet.service
```

View the client cert fingerprint:

```bash
sudo puppet agent --fingerprint
```

Back on the Puppet server, view pending certificate signing requests:

```bash
sudo puppet cert list
```

On the Puppet server, verify the fingerprint of the client and sign the `puppetclient` cert:

```bash
sudo puppet cert sign puppetclient.example.com
```

On the Puppet client, run the puppet agent manually in the foreground. This step isn't strictly necessary, but it is the best way to test and debug the puppet service.

```bash
sudo puppet agent --test
```

Check `/var/log/syslog` on both hosts for any errors with the configuration. If all goes well the Apache2 package and it's dependencies will be installed on the Puppet client.

## Further reading

The example presented in this page is simple and does not highlight many of Puppet's features and benefits. For more information on Puppet's extended features, these resources may be of interest.

- The [Official Puppet Documentation](http://docs.puppetlabs.com/) web site
- The [Puppet forge](http://forge.puppetlabs.com/) online repository of Puppet modules
