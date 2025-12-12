---
myst:
  html_meta:
    description: Install Apache2 HTTP web server on Ubuntu and learn about its configuration files and directives for LAMP stack deployment.
---

(install-apache2)=
# How to install Apache2

[The Apache HTTP Server](https://httpd.apache.org/) ("httpd") is the most commonly used web server on Linux systems, and is often used as part of the LAMP configuration. In this guide, we will show you how to install and configure Apache2, which is the current release of "httpd".

## Install `apache2`

To install Apache2, enter the following command at the terminal prompt:

```bash
sudo apt install apache2
```

## Configure `apache2`

Apache2 is configured by placing **directives** in plain text configuration files in `/etc/apache2/`. These *directives* are separated between the following files and directories:

### Files

- `apache2.conf`
  The main Apache2 configuration file. Contains settings that are **global** to Apache2.

  ```{note}
  Historically, the main Apache2 configuration file was `httpd.conf`, named after the "httpd" daemon. In other distributions (or older versions of Ubuntu), the file might be present. In modern releases of Ubuntu, all configuration options have been moved to `apache2.conf` and the below referenced directories and `httpd.conf` no longer exists.
  ```

- `envvars`
  File where Apache2 **environment** variables are set.

- `magic`
  Instructions for determining MIME type based on the first few bytes of a file.

- `ports.conf`
  Houses the directives that determine which TCP ports Apache2 is listening on.

In addition, other configuration files may be added using the **Include** directive, and wildcards can be used to include many configuration files. Any directive may be placed in any of these configuration files. Changes to the main configuration files are only recognized by Apache2 when it is started or restarted.

The server also reads a file containing MIME document types; the filename is set by the **`TypesConfig`** directive, typically via `/etc/apache2/mods-available/mime.conf`, which might also include additions and overrides, and is `/etc/mime.types` by default.

### Directories

- `conf-available`
  This directory contains available configuration files. All files that were previously in `/etc/apache2/conf.d` should be moved to `/etc/apache2/conf-available`.

- `conf-enabled`
  Holds **symlinks** to the files in `/etc/apache2/conf-available`. When a configuration file is symlinked, it will be enabled the next time Apache2 is restarted.

- `mods-available`
  This directory contains configuration files to both load **modules** and configure them. Not all modules will have specific configuration files, however.

- `mods-enabled`
  Holds symlinks to the files in `/etc/apache2/mods-available`. When a module configuration file is symlinked it will be enabled the next time Apache2 is restarted.

- `sites-available`
  This directory has configuration files for Apache2 **Virtual Hosts**. Virtual Hosts allow Apache2 to be configured for multiple sites that have separate configurations.

- `sites-enabled`
  Like `mods-enabled`, `sites-enabled` contains symlinks to the `/etc/apache2/sites-available` directory. Similarly, when a configuration file in `sites-available` is symlinked, the site configured by it will be active once Apache2 is restarted.

## Detailed configuration

For more detailed information on configuring Apache2, check out our follow-up guides.
- Part 2: {ref}`Apache2 configuration settings <configure-apache2-settings>`
- Part 3: {ref}`how to extend Apache2 <use-apache2-modules>` with modules.

## Further reading

- [Apache2 Documentation](https://httpd.apache.org/docs/2.4/) contains in depth information on Apache2 configuration directives. Also, see the `apache2-doc` package for the official Apache2 docs.

- O'Reilly's [Apache Cookbook](https://www.oreilly.com/library/view/apache-cookbook-2nd/9780596529949/) is a good resource for accomplishing specific Apache2 configurations.

- For Ubuntu-specific Apache2 questions, ask in the *\#ubuntu-server* IRC channel on [libera.chat](https://libera.chat/).
