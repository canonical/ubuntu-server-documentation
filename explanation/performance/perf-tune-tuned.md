(perf-tune-tuned)=
# TuneD

> Any tool related to system tuning is either about better understanding the
> system or after doing so applying this knowledge. See our common
> {ref}`system tuning thoughts<explanation-system-tuning-disclaimer>` for
> the general reasons for that.

The same is true for the TuneD profiles - they are only suggestions and starting
points for a few named workload categories that allow you to react dynamically.

[TuneD](https://tuned-project.org/)<sup>*1</sup> is a service used to tune your system and optimise the performance under certain workloads. At the core of TuneD are **profiles**, which tune your system for different use cases. TuneD is distributed with a number of predefined profiles for use cases such as:

* High throughput
* Low latency
* Saving power

It is possible to modify the rules defined for each profile and customise how to tune a particular device. When you switch to another profile or deactivate TuneD, all changes made to the system settings by the previous profile revert back to their original state.

You can also configure TuneD to dynamically react to changes in device usage and adjust settings to improve the performance of active devices and reduce the power consumption of inactive devices.

## Static vs. dynamic tuning

TuneD can perform two types of tuning: **static** and **dynamic**.

* Static tuning mainly consists of applying predefined `sysctl` and `sysfs` settings and the one-shot activation of several configuration tools such as `ethtool`.

* In dynamic tuning, it watches how various system components are used throughout the uptime of your system. TuneD then adjusts the system settings dynamically based on that monitoring information. For example, the hard drive is used heavily during startup and login, but is barely used later when the user is mainly working with applications (e.g. web browsers or email clients). Similarly, the CPU and network devices are used differently at different times. TuneD monitors the activity of these components and reacts to the changes in their use.

By default, dynamic tuning is enabled. To disable it, edit the `/etc/tuned/tuned-main.conf` file and change the `dynamic_tuning` option to `0`. TuneD then periodically analyses system statistics and uses them to update your system tuning settings. To configure the time interval in seconds between these updates, use the `update_interval` option. After any change in this configuration file, the systemd service needs to be restarted.

## Profiles

TuneD works with profiles, which are configuration files grouping tuning plugins and their options. Upon installation of the `tuned` package, a profile will be applied by default depending on the detected environment. These are the default profiles for each type of environment:

| Environment | Default profile |
| --- | --- |
| Compute nodes | `throughput-performance` |
| Virtual Machines | `virtual-guest` |
| Containers | `default` |
| Other cases | `balanced` |

### Anatomy of a profile

Predefined tuned profiles provided by the package are located in the directory `/usr/lib/tuned/<profile-name>`,
those added by the administrator should be placed in `/etc/tuned/<profile-name>`.

> In TuneD version 2.24 and thereby Ubuntu 25.04 Plucky (and later) the location
> of these files changed. An upgrade will migrate any custom profiles, however
> since most users are not yet on the new release, the rest of this page uses
> the old paths in the examples.
> Predefined profiles:
>   `/usr/lib/tuned/<profile-name>` -> `/usr/lib/tuned/profiles/<profile-name>`
> User defined profiles:
>   `/etc/tuned/<profile-name>` -> `/etc/tuned/profiles/<profile-name>`

In each of these `<profile-name>` directories a file `tuned.conf` defines that profile.
That file has an INI structure which looks like this:

```ini
[main]
include=PROFILE # if inheriting from another profile
summary=A short summary
description=A short description

[plugin instance]
type=TYPE
replace=REPLACE
enabled=ENABLED
devices=DEVICES

[another plugin instance]
type=TYPE
replace=REPLACE
enabled=ENABLED
devices=DEVICES
... other plugin-specific options ...

...
```

Here is a brief explanation of these configuration parameters:

* `type`: This is the plugin type. A list of all types can be obtained with the command `tuned-adm list plugins`.
* `replace`: This can take the values `true` or `false`, and is used to control what happens when two plugins of the same type are trying to configure the same devices. If `true`, then the plugin defined last replaces all options.
* `enabled`: This also accepts the values `true` or `false`, and is used to control if a plugin should remain enabled or disabled when inheriting from another profile.
* `devices`: A comma separated list of device names (without the `/dev/` prefix) which represents the devices this plugin should act on. If not specified, all compatible devices found, now or in the future, will be used. This parameter also accepts simple globbing and negation rules, so that you can specify `nvme*` for all `/dev/nvme*` devices, or `!sda` to not include `/dev/sda`.
* plugin-specific options: These can be seen in the output of the `tuned-adm list plugins -v` command, for each listed plugin.

See the [tuned.conf manpage](https://manpages.ubuntu.com/manpages/noble/en/man5/tuned.conf.5.html) for details on the syntax of this configuration file.

The plugin instance concept can be useful if you want to apply different tuning parameters to diferent devices. For example, you could have one plugin instance to take care of NVMe storage, and another one for spinning disks:
```ini
[fast_storage]
type=disk
devices=nvme0n*
... options for these devices

[slow_storage]
type=disk
devices=sda, sdb
... options for these devices
```

### Available profiles and plugins

The list of available profiles can be found using the following command:

    tuned-adm list profiles

Which will result in a long list (output truncated for brevity):

    Available profiles:
    - accelerator-performance     - Throughput performance based tuning with disabled higher latency STOP states
    - atomic-guest                - Optimize virtual guests based on the Atomic variant
    - atomic-host                 - Optimize bare metal systems running the Atomic variant
    (...)

Here are some useful commands regarding profiles:

* `tuned-adm active`: Shows which profile is currently enabled.
* `tuned-adm recommend`: Shows the recommended profile for this system.
* `tuned-adm profile <name>`: Switch to the named profile, applying its settings.

The list of plugin types can be obtained with the `tuned-adm list plugins`, and to see plugin-specific options, run `tuned-adm list plugins -v`. Unfortunately at the moment the documentation of those options is only present in the source code of each plugin.

For example, the `cpu` plugin options are:
```
cpu
	load_threshold
	latency_low
	latency_high
	force_latency
	governor
	sampling_down_factor
	energy_perf_bias
	min_perf_pct
	max_perf_pct
	no_turbo
	pm_qos_resume_latency_us
	energy_performance_preference
```
And their description can be found in `/usr/lib/python3/dist-packages/tuned/plugins/plugin_cpu.py`.

### Customising a profile

For some specific workloads, the predefined profiles might not be enough and you may want to customise your own profile. You may customise an existing profile, just overriding a few settings, or create an entirely new one.

Custom profiles live in `/etc/tuned/<profile-name>/tuned.conf` (Remember this location changed in 25.04 Plucky and later). There are 3 ways they can be created:

* Copy an existing profile from `/usr/lib/tuned/<profile-name>` to `/etc/tuned/<profile-name>`, and make changes to it in that location. A profile defined in `/etc/tuned` takes precedence over one from `/usr/lib/tuned` with the same name.
* Create an entirely new profile in `/etc/tuned/<new-profile-name>` from scratch.
* Create a new profile in `/etc/tuned/<new-profile-name>`, with a name that doesn't match an existing profile, and inherit from another profile. In this way you only have to specify the changes you want, and inherit the rest from the existing profile in `/usr/lib/tuned/<profile-name>`.

After that, the new profile will be visible by TuneD via the `tuned-adm list` command.

Here is a simple example of a customised profile named `mypostgresql` that is inheriting from the existing `/usr/lib/tuned/postgresql` profile. The child profile is defined in `/etc/tuned/mypostgresql/tuned.conf`:

```text
[main]
include=postgresql

[cpu]
load_threshold=0.5
latency_low=10
latency_high=10000
```

The inheritance is specified via the `include` option in the `[main]` section.

After the `[main]` section come the plugins that we want to override, and their new settings. Settings not specified here will take the value defined in the parent profile, `postgresql` in this case. If you want to completely ignore whatever the `cpu` plugin defined in the parent profile, use the `replace=true` setting.

### Merging profiles
There are some profiles that are neither a parent profile, nor a child profile. They only specify a few plugins and settings, and no inheritance relationship. By themselves, they are not useful, but they can be merged with an existing profile on-the-fly.

Here is an example which applies the base profile `cpu-partitioning` and then overlays `intel-sst` on top:

    sudo tuned-adm profile cpu-partitioning intel-sst

In a sense, it's like a dynamic inheritance: instead of having the `intel-sst` profile include `cpu-partitioning` in a hardcoded `include` statement, it can be used in this way and merge its settings to any other base profile on-the-fly, at runtime.

Another example of merging profiles is the combining of the `powersave` profile with another one:

    sudo tuned-adm profile virtual-guest powersave

This would optimise the system for a virtual guest, and then apply power saving parameters on top.

```{warning}
Just because `tuned-adm` accepted to merge two profiles doesn't mean it makes sense. There is no checking done on the resulting merged parameters, and the second profile could completely revert what the first profile adjusted.
```

## An example profile: hpc-compute

Let's take look at the predefined `hpc-compute` profile in more detail as an example. You can find the configuration of this profile in `/usr/lib/tuned/hpc-compute/tuned.conf`:

```ini
#
# tuned configuration
#

[main]
summary=Optimize for HPC compute workloads
description=Configures virtual memory, CPU governors, and network settings for HPC compute workloads.
include=latency-performance

[vm]
# Most HPC application can take advantage of hugepages. Force them to on.
transparent_hugepages=always

[disk]
# Increase the readahead value to support large, contiguous, files.
readahead=>4096

[sysctl]
# Keep a reasonable amount of memory free to support large mem requests
vm.min_free_kbytes=135168

# Most HPC applications are NUMA aware. Enabling zone reclaim ensures
# memory is reclaimed and reallocated from local pages. Disabling
# automatic NUMA balancing prevents unwanted memory unmapping.
vm.zone_reclaim_mode=1
kernel.numa_balancing=0

# Busy polling helps reduce latency in the network receive path
# by allowing socket layer code to poll the receive queue of a
# network device, and disabling network interrupts.
# busy_read value greater than 0 enables busy polling. Recommended
# net.core.busy_read value is 50.
# busy_poll value greater than 0 enables polling globally.
# Recommended net.core.busy_poll value is 50
net.core.busy_read=50
net.core.busy_poll=50

# TCP fast open reduces network latency by enabling data exchange
# during the sender's initial TCP SYN. The value 3 enables fast open
# on client and server connections.
net.ipv4.tcp_fastopen=3
```

The `[main]` section contains some metadata about this profile, a summary and description, and whether it includes other profiles. In this case, another profile *is* included; the `latency-performance` profile.

The sections that follow `[main]` represent the configuration of tuning plugins.

* The first one is the `vm` plugin, which is used to always make use of huge pages (useful in this {term}`HPC` scenario).
* The second plugin used is `disk`, which is used to set the `readahead` value to at least `4096`.
* Finally, the `sysctl` plugin is configured to set several variables in `sysfs` (the comments in the example explain the rationale behind each change).

> \*1: This is a universe package
> Ubuntu ships this software as part of its [universe repository](https://canonical-ubuntu-pro-client.readthedocs-hosted.com/en/latest/explanations/about_esm/#what-are-main-and-universe), which is maintained by volunteers from the Ubuntu community. Canonical also offers [Ubuntu Pro](https://ubuntu.com/pro) – a free-for-personal-use subscription that provides a 10 year [security maintenance commitment](https://ubuntu.com/security/esm).

## Further reading

* [TuneD website](https://tuned-project.org/)
* [tuned-adm manpage](https://manpages.ubuntu.com/manpages/noble/en/man8/tuned-adm.8.html)
* [TuneD profiles manpage](https://manpages.ubuntu.com/manpages/noble/en/man7/tuned-profiles.7.html)
* [TuneD daemon manpage](https://manpages.ubuntu.com/manpages/noble/en/man8/tuned.8.html)
* [TuneD configuration manpage](https://manpages.ubuntu.com/manpages/noble/en/man5/tuned.conf.5.html)
