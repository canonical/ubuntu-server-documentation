(how-to-install-nginx)=
# Install nginx

The nginx HTTP server is a powerful alternative to [Apache](how-to-install-apache2.md). In this guide, we will demonstrate how to install and use nginx for web services.

## Install nginx

To install nginx, enter the following command at the terminal prompt:

```bash
$ sudo apt update
$ sudo apt install nginx
```

This will also install any required dependency packages, and some common mods for your server, and then start the nginx web server.

### Verify nginx is running

You can verify that nginx is running via this command:

```bash
$ sudo systemctl status nginx
  ● nginx.service - A high performance web server and a reverse proxy server
       Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
       Active: active (running) since Sun 2023-08-20 01:04:22 UTC; 53s ago
         Docs: man:nginx(8)
      Process: 28210 ExecStartPre=/usr/sbin/nginx -t -q -g daemon on; master_process on; (code=exited, status=0/SU\
    CCESS)                                                                                                               
      Process: 28211 ExecStart=/usr/sbin/nginx -g daemon on; master_process on; (code=exited, status=0/SUCCESS)
     Main PID: 28312 (nginx)
        Tasks: 13 (limit: 76969)
       Memory: 13.1M
          CPU: 105ms
       CGroup: /system.slice/nginx.service
               ├─28312 "nginx: master process /usr/sbin/nginx -g daemon on; master_process on;"
               ├─28314 "nginx: worker process" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" ""
               ...
```

### Restarting nginx

To restart nginx, run:

```bash
$ sudo systemctl restart nginx
```

### Enable/disable nginx manually

By default, Nginx will automatically start at boot time.  To disable this behaviour so that you can start it up manually, you can disable it:

```bash
$ sudo systemctl disable nginx
```

Then, to re-enable it, run:

```bash
$ sudo systemctl enable nginx
```

### The default nginx homepage

A default nginx home page is also set up during the installation process. You can load this page in your web browser using your web server's IP address; http://<i>your_server_ip</i>.

The default home page should look similar to:

```text
                                                                                        Welcome to nginx!        
                                              Welcome to nginx!

If you see this page, the nginx web server is successfully installed and working. Further configuration is
required.

For online documentation and support please refer to nginx.org.
Commercial support is available at nginx.com.

Thank you for using nginx.
```

### Setting up nginx

For more information on customising nginx for your needs, see these follow-up guides:

  * Part 2: [How to configure nginx](how-to-configure-nginx.md)
  * Part 3: [How to use nginx modules](how-to-use-nginx-modules.md)


### Further reading

  * The [nginx documentation](https://nginx.org/en/docs/) provides detailed explanations of configuration directives.

  * O'Reilly's nginx cookbook provides guidance on solving specific needs

  * For Ubuntu-specific nginx questions, ask in the `#ubuntu-server` IRC channel on <a>libera.chat</a>.
