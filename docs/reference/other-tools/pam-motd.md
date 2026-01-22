---
myst:
  html_meta:
    description: "Reference documentation for pam_motd, the PAM infrastructure that generates and displays message-of-the-day on login at an Ubuntu Server."
---

(pam-motd)=
# pam_motd


When logging into an Ubuntu server you may have noticed the informative Message Of The Day (MOTD). This information is obtained and displayed using a couple of packages:

  - *`landscape-common`:* provides the core libraries of `landscape-client`, which is needed to manage systems with [Landscape](https://landscape.canonical.com/) (proprietary). Yet the package also includes the `landscape-sysinfo` utility which is responsible for displaying core system data involving CPU, memory, disk space, etc. For instance:
    
    ``` 
    
          System load:  0.0               Processes:           76
          Usage of /:   30.2% of 3.11GB   Users logged in:     1
          Memory usage: 20%               IP address for eth0: 10.153.107.115
          Swap usage:   0%
    
          Graph this data and manage this system at https://landscape.canonical.com/
    ```
    
    ```{note}
    You can run `landscape-sysinfo` manually at any time.
    ```

  - *`update-notifier-common`:* provides information on available package updates, impending {term}`filesystem checks (fsck) <fsck>`, and required reboots (e.g.: after a kernel upgrade).

`pam_motd` executes the scripts in `/etc/update-motd.d` in order based on the number prepended to the script. The output of the scripts is written to `/var/run/motd`, keeping the numerical order, then concatenated with `/etc/motd.tail`.

You can add your own dynamic information to the MOTD. For example, to add local weather information:

  - First, install the `weather-util` package:
    
        sudo apt install weather-util

  - The weather utility uses METAR data from the National Oceanic and Atmospheric Administration and forecasts from the National Weather Service. In order to find local information you will need the 4-character ICAO location indicator. This can be determined by browsing to the [National Weather Service](https://www.weather.gov/tg/siteloc) site.
    
    Although the National Weather Service is a United States government agency there are weather stations available world wide. However, local weather information for all locations outside the U.S. may not be available.

  - Create `/usr/local/bin/local-weather`, a simple shell script to use weather with your local ICAO indicator:
    
        #!/bin/sh
        #
        #
        # Prints the local weather information for the MOTD.
        #
        #
        
        # Replace KINT with your local weather station.
        # Local stations can be found here: http://www.weather.gov/tg/siteloc.shtml
        
        echo
        weather KINT
        echo

  - Make the script executable:
    
        sudo chmod 755 /usr/local/bin/local-weather

  - Next, create a symlink to `/etc/update-motd.d/98-local-weather`:
    
        sudo ln -s /usr/local/bin/local-weather /etc/update-motd.d/98-local-weather

  - Finally, exit the server and re-login to view the new MOTD.

You should now be greeted with some useful information, and some information about the local weather that may not be quite so useful. Hopefully the local-weather example demonstrates the flexibility of `pam_motd`.

## Resources

  - See the {manpage}`update-motd(5)` manual page for more options available to update-motd.

  - The Debian Package of the Day [weather](https://debaday.debian.net/2007/10/04/weather-check-weather-conditions-and-forecasts-on-the-command-line/) article has more details about using the weather utility.
