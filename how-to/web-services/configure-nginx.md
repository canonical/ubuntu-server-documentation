(configure-nginx)=
# How to configure nginx

Once you have {ref}`installed nginx <install-nginx>`, you can customise it for your use with the configuration options explained in this guide.

## Server blocks

nginx organises sets of site-specific configuration details into **server blocks**, and by default comes pre-configured for single-site operation. This can either be used "as-is", or as a starting template
for serving multiple sites.

The single-site configuration serves files out of `/var/www/html`, as defined by the server block and as provided by `/etc/nginx/sites-enabled/default`:

```text
server {
        listen 80 default_server;                                                                                    
        listen [::]:80 default_server;

        root /var/www/html;                                                                                          
                                                                                                                         
        # Add index.php to the list if you are using PHP                                                             
        index index.html index.htm index.nginx-debian.html;                                                          
                                                                                                                         
        server_name _;                                                                                               
                                                                                                                         
        location / {                                                                                                 
                # First attempt to serve request as file, then                                                       
                # as directory, then fall back to displaying a 404.                                                  
                try_files $uri $uri/ =404;                                                                           
        }
}
```

Even for a single-site configuration, while you can place your website at `/var/www/html`, you may want to place the website's files at a different location in your {term}`filesystem`. For example, if you were hosting `www.my-site.org` from `/srv/my-site/html` you might edit the above file to look like this:

```text
server {
        listen                80;
        root                  /srv/my-site/html;
        index                 index.html;
        server_name           my-site.org www.my-site.org;

        location / {                                                                                                 
                try_files $uri $uri/ =404;                                                                           
        }
}
```

Make sure to create your web root directory structure:

```bash
$ sudo mkdir -p /srv/my-site/html
$ sudo chmod -R 755 /srv/my-site/html
$ echo "<html><body><h1>My Site!</h1></body></html>" > /srv/my-site/html/index.html
```

Then, to make nginx reload its configuration, run:

```bash
$ sudo systemctl reload nginx
```

Check that the settings have taken effect using your web browser:

```bash
$ www-browser www.my-site.org
```

## Multi-site hosting

Similar to Apache, nginx uses the `sites-available` and `sites-enabled` directories for the configurations of multiple websites.  Unlike with Apache, you'll need to handle the enablement manually.

To do that, first create a new server block in a configuration file as above, and save it to `/etc/nginx/sites-available/<your-domain>`. Make sure to give each site a unique `server_name` and a different `listen` port number.

Next, enable the site by creating a symlink to it from the `sites-enabled` directory:

```bash
$ sudo ln -s /etc/nginx/sites-available/<your-domain> /etc/nginx/sites-enabled/
```

To disable a website, you can delete the symlink in `sites-enabled`. For example, once you have your new site(s) configured and no longer need the default site configuration:

```bash
$ sudo rm /etc/nginx/sites-enabled/default
```

## SSL and HTTPS 

While establishing an HTTP website on port 80 is a good starting point (and perhaps adequate for static content), production systems will want HTTPS, such as serving on port 443 with SSL enabled via `cert` files.  A server block with such a configuration might look like this, with HTTP-to-HTTPS redirection handled in the first block, and HTTPS in the second block:

```text
server {
        listen                80;
        server_name           our-site.org www.our-site.org;
        return                301 https://$host$request_uri;
}

server {
        listen                443 ssl;

        root                  /srv/our-site/html;
        index                 index.html;

        server_name           our-site.org www.our-site.org;
                                                   
        ssl_certificate       our-site.org.crt;
        ssl_certificate_key   our-site.org.key;
        ssl_protocols         TLSv1 TLSv1.1 TLSv1.2 TLSv1.3;
        ssl_ciphers           HIGH:!aNULL:!MD5;
        ssl_session_timeout   15m;

        location / {
                try_files $uri $uri/ =404;
        }
}
```

Thanks to the `return 301` line in the above configuration, anyone visiting the site on port 80 via an HTTP URL will get automatically redirected to the equivalent secure HTTPS URL.

Refer to the {ref}`security - certificates <certificates>` page in this manual for details on how to create and manage certificates, and the {ref}`OpenSSL <openssl>` page for additional details on configuring and using that service. The {ref}`GnuTLS <gnutls>` section explains how to configure different SSL protocol versions and their associated ciphers.

For example, to generate a self-signed certificate, you might run a set of commands similar to these:

```bash
$ sudo openssl genrsa -out our-site.org.key 2048                                                                   
$ openssl req -nodes -new -key our-site.org.key -out ca.csr                                                        
$ openssl x509 -req -days 365 -in our-site.org.csr -signkey our-site.org.key -out our-site.org.crt                 
$ mkdir /etc/apache2/ssl                                                                                           
$ cp our-site.org.crt our-site.org.key our-site.org.csr /etc/apache2/ssl/
```

## Setting up nginx

Beyond the settings outlined above, nginx can be further customised through the use of modules.  Please see the next guide in this series for details of how to do that.

* Part 3: {ref}`How to use nginx modules <use-nginx-modules>`


## Further reading

* [nginx's beginner's guide](https://nginx.org/en/docs/beginners_guide.html) covers use cases such as proxy servers, {term}`FastCGI` for use with PHP and other frameworks, and optimising the handling of static content.
* The [nginx documentation](https://nginx.org/en/docs/http/configuring_https_servers.html) describes HTTPS server configuration in greater detail, including certificate chains, disambiguating various multi-site certificate situations, performance optimisations and compatibility issues.
* For Ubuntu-specific nginx questions, ask in the `#ubuntu-server` IRC channel on <a>libera.chat</a>.
