(how-to-install-and-configure-logwatch)=
# Install Logwatch

Logs are an invaluable source of information about problems that may arise in your server.  [Logwatch](https://sourceforge.net/projects/logwatch/) keeps an eye on your logs for you, flags items that may be of interest, and reports them via email.

## Install Logwatch

Install `logwatch` using the following command:

```bash
sudo apt install logwatch
```

You will also need to manually create a temporary directory in order for it to work:

```bash
sudo mkdir /var/cache/logwatch
```

## Configure `logwatch`

Logwatch's default configuration is kept in` /usr/share/logwatch/default.conf/logwatch.conf`. However, configuration changes made directly to that file can be overwritten during updates, so instead the file should be copied into `/etc` and modified there:

```
sudo cp /usr/share/logwatch/default.conf/logwatch.conf /etc/logwatch/conf/
```

With your favorite editor, open `/etc/logwatch/conf/logwatch.conf`.  The uncommented lines indicate the default configuration values.  First, lets customise some of the basics:

```text
Output = mail
MailTo = me@mydomain.org
MailFrom = logwatch@host1.mydomain.org
Detail = Low
Service = All
```

This assumes you've already set up mail services on `host1` that will allow mail to be delivered to your `me@mydomain.org` address. These emails will be addressed from `logwatch@host1.mydomain.org`.

The **Detail** level defines how much information is included in the reports. Possible values are: `Low`, `Medium`, and `High`.

Logwatch will then monitor logs for all services on the system, unless specified otherwise with the **Service** parameter.  If there are undesired services included in the reports, they can be disabled by removing them with additional **Service** fields. E.g.:

```text
Service = "-http"
Service = "-eximstats"
```

Next, run `logwatch` manually to verify your configuration changes are valid:

```bash
sudo logwatch --detail Low --range today
```

The report produced should look something like this:

```text
################### Logwatch 7.4.3 (12/07/16) ####################
       Processing Initiated: Fri Apr 24 16:58:14 2020
       Date Range Processed: today
                             ( 2020-Apr-24 )
                             Period is day.
       Detail Level of Output: 0
       Type of Output/Format: stdout / text
       Logfiles for Host: `host1.mydomain.org`
##################################################################
 
--------------------- pam_unix Begin ------------------------
 
sudo:
   Sessions Opened:
      bryce -> root: 1 Time(s)
 
 