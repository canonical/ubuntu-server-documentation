---
myst:
  html_meta:
    description: "Explore practical multipath configuration examples for different storage scenarios on Ubuntu Server."
---

(multipath-configuration-examples)=
# Multipath configuration examples

Before moving on with this section we suggesting reading or being familiar with the topics covered in:

1. {ref}`Introduction to device mapper multipathing <introduction-to-multipath>`
2. {ref}`Configuration options and overview <configuring-multipath>`

For consistency with those sections, we will refer here to device mapper multipathing as **multipath**.

## Basic setup

Before setting up multipath on your system, ensure that your system has been updated and includes the `multipath-tools` package. If you want to boot from the storage area network (SAN), then the `multipath-tools-boot` package is also required.

A very simple `/etc/multipath.conf` file exists, as explained in {ref}`the configuration overview <configuring-multipath>`. All attributes not declared in `multipath.conf` are taken from the `multipath-tools` internal database and its internal blocklist.

The **internal attributes** database can be acquired by running the following on the command line:

```bash
sudo multipath -t
```

Multipath usually works out-of-the-box with most common storage. This **does not mean** the default configuration variables should be used in production: the default variables don’t treat important parameters your storage might need.

With the internal attributes (described above), and the example below, you will likely be able to create your `/etc/multipath.conf` file by squashing the code blocks below. Make sure to read the `defaults` section attribute comments and make any changes based on what your environment needs.

### Example of a defaults section

```
defaults {
    #
    # name    : polling_interval
    # scope   : multipathd
    # desc    : interval between two path checks in seconds. For
    #           properly functioning paths, the interval between checks
    #           will gradually increase to (4 * polling_interval).
    # values  : n > 0
    # default : 5
    #
    polling_interval 10
    
    #
    # name    : path_selector
    # scope   : multipath & multipathd
    # desc    : the default path selector algorithm to use
    #           these algorithms are offered by the kernel multipath target
    # values  : "round-robin 0"  = Loop through every path in the path group,
    #                              sending the same amount of IO to each.
    #           "queue-length 0" = Send the next bunch of IO down the path
    #                              with the least amount of outstanding IO.
    #           "service-time 0" = Choose the path for the next bunch of IO
    #                              based on the amount of outstanding IO to
    #                              the path and its relative throughput.
    # default : "service-time 0"
    #
    path_selector "round-robin 0"
    
    #
    # name    : path_grouping_policy
    # scope   : multipath & multipathd
    # desc    : the default path grouping policy to apply to unspecified
    #           multipaths
    # values  : failover           = 1 path per priority group
    #           multibus           = all valid paths in 1 priority group
    #           group_by_serial    = 1 priority group per detected serial
    #                                number
    #           group_by_prio      = 1 priority group per path priority
    #                                value
    #           group_by_node_name = 1 priority group per target node name
    # default : failover
    #
    path_grouping_policy multibus
    
    #
    # name    : uid_attribute
    # scope   : multipath & multipathd
    # desc    : the default udev attribute from which the path
    #       identifier should be generated.
    # default : ID_SERIAL
    #
    uid_attribute "ID_SERIAL"
        
    #
    # name    : getuid_callout
    # scope   : multipath & multipathd
    # desc    : the default program and args to callout to obtain a unique
    #           path identifier. This parameter is deprecated.
    #           This parameter is deprecated, superseded by uid_attribute
    # default : /lib/udev/scsi_id --whitelisted --device=/dev/%n
    #
    getuid_callout "/lib/udev/scsi_id --whitelisted --device=/dev/%n"
        
    #
    # name    : prio
    # scope   : multipath & multipathd
    # desc    : the default function to call to obtain a path
    #           priority value. The ALUA bits in SPC-3 provide an
    #           exploitable prio value for example.
    # default : const
    #
    # prio "alua"
        
    #
    # name    : prio_args
    # scope   : multipath & multipathd
    # desc    : The arguments string passed to the prio function
    #           Most prio functions do not need arguments. The
    #       datacore prioritizer need one.
    # default : (null)
    #
    # prio_args "timeout=1000 preferredsds=foo"
        
    #
    # name    : features
    # scope   : multipath & multipathd
    # desc    : The default extra features of multipath devices.
    #           Syntax is "num[ feature_0 feature_1 ...]", where `num' is the
    #           number of features in the following (possibly empty) list of
    #           features.
    # values  : queue_if_no_path = Queue IO if no path is active; consider
    #                              using the `no_path_retry' keyword instead.
    #           no_partitions    = Disable automatic partitions generation via
    #                              kpartx.
    # default : "0"
    #
    features    "0"
    #features   "1 queue_if_no_path"
    #features   "1 no_partitions"
    #features   "2 queue_if_no_path no_partitions"
        
    #
    # name    : path_checker, checker
    # scope   : multipath & multipathd
    # desc    : the default method used to determine the paths' state
    # values  : readsector0|tur|emc_clariion|hp_sw|directio|rdac|cciss_tur
    # default : directio
    #
    path_checker directio
        
    #
    # name    : rr_min_io
    # scope   : multipath & multipathd
    # desc    : the number of IO to route to a path before switching
    #           to the next in the same path group for the bio-based
    #           multipath implementation. This parameter is used for
    #           kernels version up to 2.6.31; newer kernel version
    #           use the parameter rr_min_io_rq
    # default : 1000
    #
    rr_min_io 100
        
    #
    # name    : rr_min_io_rq
    # scope   : multipath & multipathd
    # desc    : the number of IO to route to a path before switching
    #           to the next in the same path group for the request-based
    #           multipath implementation. This parameter is used for
    #           kernels versions later than 2.6.31.
    # default : 1
    #
    rr_min_io_rq 1
        
    #
    # name    : flush_on_last_del
    # scope   : multipathd
    # desc    : If set to "yes", multipathd will disable queueing when the
    #           last path to a device has been deleted.
    # values  : yes|no
    # default : no
    #
    flush_on_last_del yes
        
    #
    # name    : max_fds
    # scope   : multipathd
    # desc    : Sets the maximum number of open file descriptors for the
    #           multipathd process.
    # values  : max|n > 0
    # default : None
    #
    max_fds 8192
        
    #
    # name    : rr_weight
    # scope   : multipath & multipathd
    # desc    : if set to priorities the multipath configurator will assign
    #           path weights as "path prio * rr_min_io"
    # values  : priorities|uniform
    # default : uniform
    #
    rr_weight priorities
        
    #
    # name    : failback
    # scope   : multipathd
    # desc    : tell the daemon to manage path group failback, or not to.
    #           0 means immediate failback, values >0 means deffered
    #           failback expressed in seconds.
    # values  : manual|immediate|n > 0
    # default : manual
    #
    failback immediate
        
    #
    # name    : no_path_retry
    # scope   : multipath & multipathd
    # desc    : tell the number of retries until disable queueing, or
    #           "fail" means immediate failure (no queueing),
    #           "queue" means never stop queueing
    # values  : queue|fail|n (>0)
    # default : (null)
    #
    no_path_retry fail
        
    #
    # name    : queue_without_daemon
    # scope   : multipathd
    # desc    : If set to "no", multipathd will disable queueing for all
    #           devices when it is shut down.
    # values  : yes|no
    # default : yes
    queue_without_daemon no
        
    #
    # name    : user_friendly_names
    # scope   : multipath & multipathd
    # desc    : If set to "yes", using the bindings file
    #           /etc/multipath/bindings to assign a persistent and
    #           unique alias to the multipath, in the form of mpath<n>.
    #           If set to "no" use the WWID as the alias. In either case
    #           this be will be overriden by any specific aliases in this
    #           file.
    # values  : yes|no
    # default : no
    user_friendly_names yes
        
    #
    # name    : mode
    # scope   : multipath & multipathd
    # desc    : The mode to use for the multipath device nodes, in octal.
    # values  : 0000 - 0777
    # default : determined by the process
    mode 0644
        
    #
    # name    : uid
    # scope   : multipath & multipathd
    # desc    : The user id to use for the multipath device nodes. You
    #           may use either the numeric or symbolic uid
    # values  : <user_id>
    # default : determined by the process
    uid 0
        
    #
    # name    : gid
    # scope   : multipath & multipathd
    # desc    : The group id to user for the multipath device nodes. You
    #           may use either the numeric or symbolic gid
    # values  : <group_id>
    # default : determined by the process
    gid disk
       
    #
    # name    : checker_timeout
    # scope   : multipath & multipathd
    # desc    : The timeout to use for path checkers and prioritizers
    #           that issue scsi commands with an explicit timeout, in
    #           seconds.
    # values  : n > 0
    # default : taken from /sys/block/sd<x>/device/timeout
    checker_timeout 60
      
    #
    # name    : fast_io_fail_tmo
    # scope   : multipath & multipathd
    # desc    : The number of seconds the scsi layer will wait after a
    #           problem has been detected on a FC remote port before failing
    #           IO to devices on that remote port.
    # values  : off | n >= 0 (smaller than dev_loss_tmo)
    # default : determined by the OS
    fast_io_fail_tmo 5
       
    #
    # name    : dev_loss_tmo
    # scope   : multipath & multipathd
    # desc    : The number of seconds the scsi layer will wait after a
    #           problem has been detected on a FC remote port before
    #           removing it from the system.
    # values  : infinity | n > 0
    # default : determined by the OS
    dev_loss_tmo 120
        
    #
    # name    : bindings_file
    # scope   : multipath
    # desc    : The location of the bindings file that is used with
    #           the user_friendly_names option.
    # values  : <full_pathname>
    # default : "/var/lib/multipath/bindings"
    # bindings_file "/etc/multipath/bindings"
     
    #
    # name    : wwids_file
    # scope   : multipath
    # desc    : The location of the wwids file multipath uses to
    #           keep track of the created multipath devices.
    # values  : <full_pathname>
    # default : "/var/lib/multipath/wwids"
    # wwids_file "/etc/multipath/wwids"
      
    #
    # name    : reservation_key
    # scope   : multipath
    # desc    : Service action reservation key used by mpathpersist.
    # values  : <key>
    # default : (null)
    # reservation_key "mpathkey"
      
    #
    # name    : force_sync
    # scope   : multipathd
    # desc    : If set to yes, multipath will run all of the checkers in
    #           sync mode, even if the checker has an async mode.
    # values  : yes|no
    # default : no
    force_sync yes
        
    #
    # name    : config_dir
    # scope   : multipath & multipathd
    # desc    : If not set to an empty string, multipath will search
    #           this directory alphabetically for files ending in ".conf"
    #           and it will read configuration information from these
    #           files, just as if it was in /etc/multipath.conf
    # values  : "" or a fully qualified pathname
    # default : "/etc/multipath/conf.d"
       
    #
    # name    : delay_watch_checks
    # scope   : multipathd
    # desc    : If set to a value greater than 0, multipathd will watch
    #           paths that have recently become valid for this many
    #           checks.  If they fail again while they are being watched,
    #           when they next become valid, they will not be used until
    #           they have stayed up for delay_wait_checks checks.
    # values  : no|<n> > 0
    # default : no
    delay_watch_checks 12
        
    #
    # name    : delay_wait_checks
    # scope   : multipathd
    # desc    : If set to a value greater than 0, when a device that has
    #           recently come back online fails again within
    #           delay_watch_checks checks, the next time it comes back
    #           online, it will marked and delayed, and not used until
    #           it has passed delay_wait_checks checks.
    # values  : no|<n> > 0
    # default : no
    delay_wait_checks 12
    }
```

### Example of a multipaths section

```{note}
You can obtain the WWIDs for your LUNs by running: `multipath -ll`
after the service `multipath-tools.service` has been restarted.
```

```
multipaths {
    multipath {
        wwid 360000000000000000e00000000030001
        alias yellow
    }
    multipath {
        wwid 360000000000000000e00000000020001
        alias blue
    }
    multipath {
        wwid 360000000000000000e00000000010001
        alias red
    }
    multipath {
        wwid 360000000000000000e00000000040001
        alias green
    }
    multipath {
        wwid 360000000000000000e00000000050001
        alias purple
    }
}
```

### Example of a devices section

```
# devices {
#     device {
#         vendor "IBM"
#         product "2107900"
#         path_grouping_policy group_by_serial
#     }
# }
#
```

### Example of a blacklist section

```
# name    : blacklist
# scope   : multipath & multipathd
# desc    : list of device names to discard as not multipath candidates 
#
# Devices can be identified by their device node name "devnode",
# their WWID "wwid", or their vender and product strings "device"
# default : fd, hd, md, dm, sr, scd, st, ram, raw, loop, dcssblk
#
# blacklist {
#     wwid 26353900f02796769
#     devnode "^(ram|raw|loop|fd|md|dm-|sr|scd|st)[0-9]\*"
#     devnode "^hd[a-z]"
#     devnode "^dcssblk[0-9]\*"
#     device {
#         vendor DEC.\*
#         product MSA[15]00
#     }
# }
```

### Example of a blacklist exception section

```
# name    : blacklist_exceptions
# scope   : multipath & multipathd
# desc    : list of device names to be treated as multipath candidates
#           even if they are on the blacklist.
#
# Note: blacklist exceptions are only valid in the same class.
# It is not possible to blacklist devices using the devnode keyword
# and to exclude some devices of them using the wwid keyword.
# default : -
#
# blacklist_exceptions {
#        devnode "^dasd[c-d]+[0-9]\*"
#        wwid    "IBM.75000000092461.4d00.34"
#        wwid    "IBM.75000000092461.4d00.35"
#        wwid    "IBM.75000000092461.4d00.36"
# }
```
