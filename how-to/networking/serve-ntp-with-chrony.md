(serve-ntp-with-chrony)=
# How to serve the Network Time Protocol with Chrony

`timesyncd` and `timedatectl` will generally do the right thing in keeping your time in sync. However, if you also want to serve NTP information then you need an NTP server. 

Between `chrony`, the now-deprecated `ntpd`, and `open-ntp`, there are plenty of options. The solution we recommend is `chrony`.

The NTP daemon `chronyd` calculates the drift and offset of your system clock and continuously adjusts it, so there are no large corrections that could lead to inconsistent logs, for instance. The cost is a little processing power and memory, but for a modern server this is usually negligible.

## Install `chronyd`

To install `chrony`, run the following command from a terminal prompt:

```bash
sudo apt install chrony
```

This will provide two binaries:

- `chronyd` - the actual daemon to sync and serve via the Network Time Protocol

- `chronyc` - command-line interface for the `chrony` daemon

## Configure `chronyd`

Firstly, edit `/etc/chrony/chrony.conf` to add/remove server lines. By default these servers are configured:

```text
# Use servers from the NTP Pool Project. Approved by Ubuntu Technical Board
# on 2011-02-08 (LP: #104525). See http://www.pool.ntp.org/join.html for
# more information.
pool 0.ubuntu.pool.ntp.org iburst
pool 1.ubuntu.pool.ntp.org iburst
pool 2.ubuntu.pool.ntp.org iburst
pool 3.ubuntu.pool.ntp.org iburst
```

See `man chrony.conf` for more details on the configuration options available. After changing any part of the config file you need to restart `chrony`, as follows:

```bash
sudo systemctl restart chrony.service
```

Of the pool, `2.ubuntu.pool.ntp.org` and `ntp.ubuntu.com` also support IPv6, if needed. If you need to force IPv6, there is also `ipv6.ntp.ubuntu.com` which is not configured by default.

## Enable serving the Network Time Protocol

You can install `chrony` (above) and configure special Hardware (below) for a local synchronisation
and as-installed that is the default to stay on the secure and conservative side. But if you want to *serve* NTP you need adapt your configuration.

To enable serving NTP you'll need to at least set the `allow` rule. This controls which clients/networks you want `chrony` to serve NTP to.

An example would be:

```text
allow 1.2.3.4
```

See the section "NTP server" in the [man page](http://manpages.ubuntu.com/manpages/jammy/man5/chrony.conf.5.html) for more details on how you can control and restrict access to your NTP server.

## View `chrony` status

You can use `chronyc` to see query the status of the `chrony` daemon. For example, to get an overview of the currently available and selected time sources, run `chronyc sources`, which provides output like this:

```text
MS Name/IP address         Stratum Poll Reach LastRx Last sample
===============================================================================
^+ gamma.rueckgr.at              2   8   377   135  -1048us[-1048us] +/-   29ms
^- 2b.ncomputers.org             2   8   377   204  -1141us[-1124us] +/-   50ms
^+ www.kashra.com                2   8   377   139  +3483us[+3483us] +/-   18ms
^+ stratum2-4.NTP.TechFak.U>     2   8   377   143  -2090us[-2073us] +/-   19ms
^- zepto.mcl.gg                  2   7   377     9   -774us[ -774us] +/-   29ms
^- mirrorhost.pw                 2   7   377    78   -660us[ -660us] +/-   53ms
^- atto.mcl.gg                   2   7   377     8   -823us[ -823us] +/-   50ms
^- static.140.107.46.78.cli>     2   8   377     9  -1503us[-1503us] +/-   45ms
^- 4.53.160.75                   2   8   377   137    -11ms[  -11ms] +/-  117ms
^- 37.44.185.42                  3   7   377    10  -3274us[-3274us] +/-   70ms
^- bagnikita.com                 2   7   377    74  +3131us[+3131us] +/-   71ms
^- europa.ellipse.net            2   8   377   204   -790us[ -773us] +/-   97ms
^- tethys.hot-chilli.net         2   8   377   141   -797us[ -797us] +/-   59ms
^- 66-232-97-8.static.hvvc.>     2   7   377   206  +1669us[+1686us] +/-  133ms
^+ 85.199.214.102                1   8   377   205   +175us[ +192us] +/-   12ms
^* 46-243-26-34.tangos.nl        1   8   377   141   -123us[ -106us] +/-   10ms
^- pugot.canonical.com           2   8   377    21    -95us[  -95us] +/-   57ms
^- alphyn.canonical.com          2   6   377    23  -1569us[-1569us] +/-   79ms
^- golem.canonical.com           2   7   377    92  -1018us[-1018us] +/-   31ms
^- chilipepper.canonical.com     2   8   377    21  -1106us[-1106us] +/-   27ms
```    

You can also make use of the `chronyc sourcestats` command, which produces output like this:

```text
210 Number of sources = 20
Name/IP Address            NP  NR  Span  Frequency  Freq Skew  Offset  Std Dev
==============================================================================
gamma.rueckgr.at           25  15   32m     -0.007      0.142   -878us   106us
2b.ncomputers.org          26  16   35m     -0.132      0.283  -1169us   256us
www.kashra.com             25  15   32m     -0.092      0.259  +3426us   195us
stratum2-4.NTP.TechFak.U>  25  14   32m     -0.018      0.130  -2056us    96us
zepto.mcl.gg               13  11   21m     +0.148      0.196   -683us    66us
mirrorhost.pw               6   5   645     +0.117      0.445   -591us    19us
atto.mcl.gg                21  13   25m     -0.069      0.199   -904us   103us
static.140.107.46.78.cli>  25  18   34m     -0.005      0.094  -1526us    78us
4.53.160.75                25  10   32m     +0.412      0.110    -11ms    84us
37.44.185.42               24  12   30m     -0.983      0.173  -3718us   122us
bagnikita.com              17   7   31m     -0.132      0.217  +3527us   139us
europa.ellipse.net         26  15   35m     +0.038      0.553   -473us   424us
tethys.hot-chilli.net      25  11   32m     -0.094      0.110   -864us    88us
66-232-97-8.static.hvvc.>  20  11   35m     -0.116      0.165  +1561us   109us
85.199.214.102             26  11   35m     -0.054      0.390   +129us   343us
46-243-26-34.tangos.nl     25  16   32m     +0.129      0.297   -307us   198us
pugot.canonical.com        25  14   34m     -0.271      0.176   -143us   135us
alphyn.canonical.com       17  11  1100     -0.087      0.360  -1749us   114us
golem.canonical.com        23  12   30m     +0.057      0.370   -988us   229us
chilipepper.canonical.com  25  18   34m     -0.084      0.224  -1116us   169us
```

Certain `chronyc` commands are privileged and cannot be run via the network without explicitly allowing them. See the **Command and monitoring access** section in `man chrony.conf` for more details. A local admin can use `sudo` since this will grant access to the local admin socket `/var/run/chrony/chronyd.sock`.

## Pulse-Per-Second (PPS) support

`Chrony` supports various PPS types natively. It can use kernel PPS API as well as Precision Time Protocol (PTP) hardware clocks. Most general GPS receivers can be leveraged via GPSD. The latter (and potentially more) can be accessed via **SHM** or via a **socket** (recommended). All of the above can be used to augment `chrony` with additional high quality time sources for better accuracy, jitter, drift, and longer- or shorter-term accuracy. Usually, each kind of clock type is good at one of those, but non-perfect at the others. For more details on configuration see some of the external PPS/GPSD resources listed below.

> **Note**:
> As of the release of 20.04, there was a bug which - until fixed - you might want to [add this content](https://bugs.launchpad.net/ubuntu/+source/gpsd/+bug/1872175/comments/21)  to your `/etc/apparmor.d/local/usr.sbin.gpsd`.

### Example configuration for GPSD to feed `chrony`

For the installation and setup you will first need to run the following command in your terminal window:

```bash
sudo apt install gpsd chrony
```

However, since you will want to test/debug your setup (especially the GPS reception), you should also install:

```
sudo apt install pps-tools gpsd-clients
```

GPS devices usually communicate via serial interfaces. The most common type these days are USB GPS devices, which have a serial converter behind USB. If you want to use one of these devices for PPS then please be aware that the majority do not signal PPS via USB. Check the [GPSD hardware](https://gpsd.gitlab.io/gpsd/hardware.html) list for details. The examples below were run with a Navisys GR701-W.

When plugging in such a device (or at boot time) {term}`dmesg` should report a serial connection of some sort, as in this example:

```text
[   52.442199] usb 1-1.1: new full-speed USB device number 3 using xhci_hcd
[   52.546639] usb 1-1.1: New USB device found, idVendor=067b, idProduct=2303, bcdDevice= 4.00
[   52.546654] usb 1-1.1: New USB device strings: Mfr=1, Product=2, SerialNumber=0
[   52.546665] usb 1-1.1: Product: USB-Serial Controller D
[   52.546675] usb 1-1.1: Manufacturer: Prolific Technology Inc. 
[   52.602103] usbcore: registered new interface driver usbserial_generic
[   52.602244] usbserial: USB Serial support registered for generic
[   52.609471] usbcore: registered new interface driver pl2303
[   52.609503] usbserial: USB Serial support registered for pl2303
[   52.609564] pl2303 1-1.1:1.0: pl2303 converter detected
[   52.618366] usb 1-1.1: pl2303 converter now attached to ttyUSB0
```

We see in this example that the device appeared as `ttyUSB0`. So that `chrony` later accepts being fed time information by this device, we have to set it up in `/etc/chrony/chrony.conf` (please replace `USB0` with whatever applies to your setup):

```
refclock SHM 0 refid GPS precision 1e-1 offset 0.9999 delay 0.2
refclock SOCK /var/run/chrony.ttyUSB0.sock refid PPS
```

Next, we need to restart `chrony` to make the socket available and have it waiting.

```
sudo systemctl restart chrony
```

We then need to tell `gpsd` which device to manage. Therefore, in `/etc/default/gpsd` we set:

```
DEVICES="/dev/ttyUSB0"
```

It should be noted that since the *default* use-case of `gpsd` is, well, for *gps position tracking*, it will normally not consume any CPU since it is just waiting on a **socket** for clients. Furthermore, the client will tell `gpsd` what it requests, and `gpsd` will only provide what is asked for.

For the use case of `gpsd` as a PPS-providing-daemon, you want to set the option to:

 - Immediately start (even without a client connected). This can be set in `GPSD_OPTIONS` of `/etc/default/gpsd`: 
   - `GPSD_OPTIONS="-n"`

 - Enable the service itself and not wait for a client to reach the socket in the future:
   - `sudo systemctl enable /lib/systemd/system/gpsd.service`

Restarting `gpsd` will now initialize the PPS from GPS and in `dmesg` you will see:

```text
 pps_ldisc: PPS line discipline registered
 pps pps0: new PPS source usbserial0
 pps pps0: source "/dev/ttyUSB0" added
```

If you have multiple PPS sources, the tool `ppsfind` may be useful to help identify which PPS belongs to which GPS. In our example, the command `sudo ppsfind /dev/ttyUSB0` would return the following:

```text
pps0: name=usbserial0 path=/dev/ttyUSB0
```

Now we have completed the basic setup. To proceed, we now need our GPS to get a lock. Tools like `cgps` or `gpsmon` need to report a 3D "fix" in order to provide accurate data. Let's run the command `cgps`, which in our case returns:

```text
...
│ Status:         3D FIX (7 secs) ...
```

You would then want to use `ppstest` in order to check that you are really receiving PPS data. So, let us run the command `sudo ppstest /dev/pps0`, which will produce an output like this:

```text
trying PPS source "/dev/pps0"
found PPS source "/dev/pps0"
ok, found 1 source(s), now start fetching data...
source 0 - assert 1588140739.099526246, sequence: 69 - clear  1588140739.999663721, sequence: 70
source 0 - assert 1588140740.099661485, sequence: 70 - clear  1588140739.999663721, sequence: 70
source 0 - assert 1588140740.099661485, sequence: 70 - clear  1588140740.999786664, sequence: 71
source 0 - assert 1588140741.099792447, sequence: 71 - clear  1588140740.999786664, sequence: 71
```

Ok, `gpsd` is now running, the GPS reception has found a fix, and it has fed this into `chrony`. Let's check on that from the point of view of `chrony`.

Initially, before `gpsd` has started or before it has a lock, these sources will be new and "untrusted" - they will be marked with a "?" as shown in the example below. If your devices remain in the "?" state (even after some time) then `gpsd` is not feeding any data to `chrony` and you will need to debug why.

```text
chronyc> sources
210 Number of sources = 10
MS Name/IP address         Stratum Poll Reach LastRx Last sample               
===============================================================================
#? GPS                           0   4     0     -     +0ns[   +0ns] +/-    0ns
#? PPS                           0   4     0     -     +0ns[   +0ns] +/-    0ns
```

Over time, `chrony` will classify all of the unknown sources as "good" or "bad".
In the example below, the raw GPS had too much deviation (+- 200ms) but the PPS is good (+- 63us).

```text
chronyc> sources
210 Number of sources = 10
MS Name/IP address        Stratum Poll Reach LastRx Last sample
===============================================================================
#x GPS                         0    4   177    24 -876ms[ -876ms] +/- 200ms
#- PPS                         0    4   177    21 +916us[ +916us] +/- 63us
^- chilipepper.canonical.com   2    6    37    53  +33us[ +33us]  +/- 33ms
```

Finally, after a while it used the hardware PPS input (as it was better):

```text
chronyc> sources
210 Number of sources = 10
MS Name/IP address         Stratum Poll Reach LastRx Last sample
===============================================================================
#x GPS                           0   4   377    20   -884ms[ -884ms] +/-  200ms
#* PPS                           0   4   377    18  +6677ns[  +52us] +/-   58us
^- alphyn.canonical.com          2   6   377    20  -1303us[-1258us] +/-  114ms
```

The PPS might also be OK -- but used in a combined way with the selected server, for example. See `man chronyc` for more details about how these combinations can look:

```text
chronyc> sources
210 Number of sources = 11
MS Name/IP address         Stratum Poll Reach LastRx Last sample               
===============================================================================
#? GPS                           0   4     0     -     +0ns[   +0ns] +/-    0ns
#+ PPS                           0   4   377    22   +154us[ +154us] +/- 8561us
^* chilipepper.canonical.com     2   6   377    50   -353us[ -300us] +/-   44ms
```

If you're wondering if your SHM-based GPS data is any good, you can check on that as well. `chrony` will not only tell you if the data is classified as good or bad -- using `sourcestats` you can also check the details:

```text
chronyc> sourcestats
210 Number of sources = 10
Name/IP Address            NP  NR  Span  Frequency  Freq Skew  Offset  Std Dev
==============================================================================
GPS                        20   9   302     +1.993     11.501   -868ms  1208us
PPS                         6   3    78     +0.324      5.009  +3365ns    41us
golem.canonical.com        15  10   783     +0.859      0.509   -750us   108us
```

You can also track the raw data that `gpsd` or other `ntpd`-compliant reference clocks are sending via shared memory by using `ntpshmmon`. Let us run the command `sudo ntpshmmon -o`, which should provide the following output:

```text
ntpshmmon: version 3.20
#      Name          Offset       Clock                 Real                 L Prc
sample NTP1          0.000223854  1588265805.000223854  1588265805.000000000 0 -10
sample NTP0          0.125691783  1588265805.125999851  1588265805.000308068 0 -20
sample NTP1          0.000349341  1588265806.000349341  1588265806.000000000 0 -10
sample NTP0          0.130326636  1588265806.130634945  1588265806.000308309 0 -20
sample NTP1          0.000485216  1588265807.000485216  1588265807.000000000 0 -10
```

## NTS Support

In Chrony 4.0 (which first appeared in Ubuntu 21.04 Hirsute) support for [Network Time Security "NTS"](https://www.networktimesecurity.org/) was added.

### NTS server

To set up your server with NTS you'll need certificates so that the server can authenticate itself and, based on that, allow the encryption and verification of NTP traffic.

In addition to the `allow` statement that any `chrony` (while working as an NTP server) needs there are two mandatory config entries that will be needed. Example certificates for those entries would look like:

```text
ntsservercert /etc/chrony/fullchain.pem
ntsserverkey /etc/chrony/privkey.pem
```

It is important to note that for isolation reasons `chrony`, by default, runs as user and group `_chrony`. Therefore you need to grant access to the certificates for that user, by running the following command:.

```bash
sudo chown _chrony:_chrony /etc/chrony/*.pem
```

Then restart `chrony` with `systemctl restart chrony` and it will be ready to provide NTS-based time services.

A running `chrony` server measures various statistics. One of them counts the number of NTS connections that were established (or dropped) -- we can check this by running `sudo chronyc -N serverstats`, which shows us the statistics:

```text
NTP packets received       : 213
NTP packets dropped        : 0
Command packets received   : 117
Command packets dropped    : 0
Client log records dropped : 0
NTS-KE connections accepted: 2
NTS-KE connections dropped : 0
Authenticated NTP packets  : 197
```

There is also a per-client statistic which can be enabled by the `-p` option of the `clients` command.

```bash
sudo chronyc -N clients -k
```

This provides output in the following form:

```text
    Hostname                      NTP   Drop Int IntL Last  NTS-KE   Drop Int  Last
    ===============================================================================
    10.172.196.173                197      0  10   -   595       2      0   5   48h
    ...
```

For more complex scenarios there are many more advanced options for configuring NTS. These are documented in [the `chrony` man page](https://manpages.ubuntu.com/manpages/en/man5/chrony.conf.5.html).

> **Note**: *About certificate placement*
> Chrony, by default, is isolated via AppArmor and uses a number of `protect*` features of `systemd`. Due to that, there are not many paths `chrony` can access for the certificates. But `/etc/chrony/*` is allowed as read-only and that is enough.
>  Check `/etc/apparmor.d/usr.sbin.chronyd` if you want other paths or allow custom paths in `/etc/apparmor.d/local/usr.sbin.chronyd`.

### NTS client

The client needs to specify `server` as usual (`pool` directives do not work with NTS). Afterwards, the server address options can be listed and it is there that `nts` can be added. For example:

```text
server <server-fqdn-or-IP> iburst nts
```

One can check the `authdata` of the connections established by the client using `sudo chronyc -N authdata`, which will provide the following information:

```text
Name/IP address             Mode KeyID Type KLen Last Atmp  NAK Cook CLen
=========================================================================
<server-fqdn-or-ip>          NTS     1   15  256  48h    0    0    8  100
```

Again, there are more advanced options documented in [the man page](https://manpages.ubuntu.com/manpages/en/man5/chrony.conf.5.html). Common use cases are specifying an explicit trusted certificate.

> **Bad Clocks and secure time syncing - "A Chicken and Egg" problem**
> There is one problem with systems that have very bad clocks. NTS is based on TLS, and TLS needs a reasonably correct clock. Due to that, an NTS-based sync might fail. On hardware affected by this problem, one can consider using the `nocerttimecheck` option which allows the user to set the number of times that the time can be synced without checking validation and expiration.

## References

  - [Chrony FAQ](https://chrony.tuxfamily.org/faq.html)

  - [ntp.org: home of the Network Time Protocol project](http://www.ntp.org/)

  - [pool.ntp.org: project of virtual cluster of timeservers](http://www.pool.ntp.org/)

  - [Freedesktop.org info on timedatectl](https://www.freedesktop.org/software/systemd/man/timedatectl.html)

  - [Freedesktop.org info on systemd-timesyncd service](https://www.freedesktop.org/software/systemd/man/systemd-timesyncd.service.html#)

  - [Feeding chrony from GPSD](https://gpsd.gitlab.io/gpsd/gpsd-time-service-howto.html#_feeding_chrony_from_gpsd) 

  - See the [Ubuntu Time](https://help.ubuntu.com/community/UbuntuTime) wiki page for more information.
