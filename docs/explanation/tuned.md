(tuned)=
# TuneD

[TuneD](https://tuned-project.org/)<sup>*1</sup> is a service used to tune your system and optimise the performance under certain workloads. At the core of TuneD are **profiles**, which tune your system for different use cases. TuneD is distributed with a number of predefined profiles for use cases such as:

* High throughput
* Low latency
* Saving power

It is possible to modify the rules defined for each profile and customise how to tune a particular device. When you switch to another profile or deactivate TuneD, all changes made to the system settings by the previous profile revert back to their original state.

You can also configure TuneD to dynamically react to changes in device usage and adjust settings to improve the performance of active devices and reduce the power consumption of inactive devices.

Almost all tunable parameters can be good for one and bad for another type of workload or environment. Not even the goal of tuning is the same for everyone; do you want to improve latency, throughput, thermal or work-per-power? The system defaults generally aim for a good compromise on all of these, no matter what you will do with your system. The same is true for the TuneD profiles - they are only suggestions and starting points for a few named workload categories that allow you to react dynamically. But those can't be perfect either - the more you know about your workload, your system and what you want to achieve with your tuning, the more you'll be able to improve it to suit your needs.

## Static vs. dynamic tuning

TuneD can perform two types of tuning: **static** and **dynamic**. 

* Static tuning mainly consists of applying predefined `sysctl` and `sysfs` settings and the one-shot activation of several configuration tools such as `ethtool`.

* In dynamic tuning, it watches how various system components are used throughout the uptime of your system. TuneD then adjusts the system settings dynamically based on that monitoring information. For example, the hard drive is used heavily during startup and login, but is barely used later when the user is mainly working with applications (e.g. web browsers or email clients). Similarly, the CPU and network devices are used differently at different times. TuneD monitors the activity of these components and reacts to the changes in their use.

By default, dynamic tuning is enabled. To disable it, edit the `/etc/tuned/tuned-main.conf` file and change the `dynamic_tuning` option to `0`. TuneD then periodically analyses system statistics and uses them to update your system tuning settings. To configure the time interval in seconds between these updates, use the `update_interval` option. After any change in this configuration file, the systemd service needs to be restarted.

## Profiles

TuneD works with profiles, which are configuration files listing the tuning plugins and their options. Many predefined profiles are already shipped with the TuneD package, you can see them in `/usr/lib/tuned`. After installing the TuneD package, one can also use the `tuned-adm list` command to get a brief summary of all of the available profiles.

Once the package is installed in a system, a profile is activated by default depending on the environment. These are the default profiles for each type of environment:

| Environment | Default profile |
| --- | --- |
| Compute nodes | `throughput-performance` |
| Virtual Machines | `virtual-guest` |
| Containers | `default` |
| Other cases | `balanced` |

### Available profiles

The list of available profiles can be found using the following command:

```
root@tuned:~# tuned-adm list
Available profiles:
[...]
```

You can also check which profile is enabled:

```console
root@tuned:~# tuned-adm active
Current active profile: virtual-guest
```

You can see the recommended profile:

```console
root@tuned:~# tuned-adm recommend
virtual-guest
```

And you can switch to another profile:

```console
root@tuned:~# tuned-adm profile default
root@tuned:~# tuned-adm active
Current active profile: default
```

### Customising a profile 

For some specific workloads, the predefined profiles might not be enough and you may want to customise your own profile. In order to do that, you should follow these steps:

* Inside `/etc/tuned`, create a directory with the name of your new profile.
* Inside the newly created directory, create a file called `tuned.conf`.
* Write your custom configuration in the `tuned.conf` file.

After that, the new profile will be visible by TuneD via the `tuned-adm list` command. This is a simple example of a customised profile (it could be created in `/etc/tuned/custom-profile/tuned.conf`):

```text
[main]
include=postgresql

[cpu]
load_threshold=0.5
latency_low=10
latency_high=10000
```

In the `[main]` section, the `include` keyword can be used to include any other predefined profile (in this example we are including the `postgresql` one).

After the `[main]` section, the list of plugins (ways of tuning your system) can be introduced, with all the options (here, there is just one plugin called `cpu` being used). For more information about the syntax and the list of plugins and their options, please refer to the [upstream documentation](https://github.com/redhat-performance/tuned/tree/master/doc/manual/).


## An example profile: hpc-compute

Let's take look at the predefined `hpc-compute` profile in more detail as an example. You can find the configuration of this profile in `/usr/lib/tuned/hpc-compute/tuned.conf`:

```text
\#
\# tuned configuration
\#

[main]
summary=Optimize for HPC compute workloads
description=Configures virtual memory, CPU governors, and network settings for HPC compute workloads.
include=latency-performance

[vm]
\# Most HPC application can take advantage of hugepages. Force them to on.
transparent_hugepages=always

[disk]
\# Increase the readahead value to support large, contiguous, files.
readahead=>4096

[sysctl]
\# Keep a reasonable amount of memory free to support large mem requests
vm.min_free_kbytes=135168

\# Most HPC applications are NUMA aware. Enabling zone reclaim ensures
\# memory is reclaimed and reallocated from local pages. Disabling
\# automatic NUMA balancing prevents unwanted memory unmapping.
vm.zone_reclaim_mode=1
kernel.numa_balancing=0

\# Busy polling helps reduce latency in the network receive path
\# by allowing socket layer code to poll the receive queue of a
\# network device, and disabling network interrupts.
\# busy_read value greater than 0 enables busy polling. Recommended
\# net.core.busy_read value is 50.
\# busy_poll value greater than 0 enables polling globally.
\# Recommended net.core.busy_poll value is 50
net.core.busy_read=50
net.core.busy_poll=50

\# TCP fast open reduces network latency by enabling data exchange
\# during the sender's initial TCP SYN. The value 3 enables fast open
\# on client and server connections.
net.ipv4.tcp_fastopen=3
```

The `[main]` section contains some metadata about this profile, a summary and description, and whether it includes other profiles. In this case, another profile *is* included; the `latency-performance` profile.

The sections that follow `[main]` represent the configuration of tuning plugins.

* The first one is the `vm` plugin, which is used to always make use of huge pages (useful in this HPC scenario).
* The second plugin used is `disk`, which is used to set the `readahead` value to at least `4096`.
* Finally, the `sysctl` plugin is configured to set several variables in `sysfs` (the comments in the example explain the rationale behind each change).

The content of this profile can be overwritten if needed, by creating the file `/etc/tuned/hpc-compute/tuned.conf` with the desired content. The content in `/etc/tuned` always takes precedence over `/usr/lib/tuned`. One can also extend this profile by creating a custom profile and including `hpc-compute`.

## Known issue in Ubuntu

There is a known issue that a user should be aware of when using TuneD in Ubuntu:

* Any predefined or customised profile making use of the **scheduler** and the **irqbalance** tuning plugins will not work, because those two plugins depend on the `perf` Python module which is not provided by Ubuntu. There is a request to provide the needed Python module in [LP: #2051560](https://bugs.launchpad.net/ubuntu/+source/linux/+bug/2051560).

## <sup>*1</sup> This is a universe package

Ubuntu ships this software as part of its [universe repository](https://canonical-ubuntu-pro-client.readthedocs-hosted.com/en/latest/explanations/about_esm/#what-are-main-and-universe), which is maintained by volunteers from the Ubuntu community. Canonical also offers [Ubuntu Pro](https://ubuntu.com/pro) – a free-for-personal-use subscription that provides a 10 year [security maintenance commitment](https://ubuntu.com/security/esm).

## Further reading

* [TuneD website](https://tuned-project.org/)
* [tuned-adm manpage](https://manpages.ubuntu.com/manpages/noble/en/man8/tuned-adm.8.html)
* [TuneD profiles manpage](https://manpages.ubuntu.com/manpages/noble/en/man7/tuned-profiles.7.html)
* [TuneD daemon manpage](https://manpages.ubuntu.com/manpages/noble/en/man8/tuned.8.html)
* [TuneD configuration manpage](https://manpages.ubuntu.com/manpages/noble/en/man5/tuned.conf.5.html)
