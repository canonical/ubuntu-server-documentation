---
myst:
  html_meta:
    description: "Understand multipath configuration options and settings for device mapper multipathing on Ubuntu Server."
---

(configuring-multipath)=
# Multipath configuration options and overview

It is recommended that you first read the [device mapper multipathing introduction](introduction-to-multipath) if you are unfamiliar with the concepts and terms. For consistency, we refer to device mapper multipathing as **multipath**.

Multipath usually works out-of-the-box with most common storage. This doesn't mean the default configuration variables should be used in production: they don't treat important parameters your storage might need.

It's a good idea to consult your storage manufacturer's install guide for the Linux Multipath configuration options. Storage vendors often provide the most adequate options for Linux, including minimal versions required for kernel and multipath-tools.

Default multipath configuration values can be overridden by editing the `/etc/multipath.conf` file and restarting the `multipathd` service. This page provides information on parsing and modifying the `multipath.conf` file.

## Configuration file overview

The `multipath.conf` configuration file contains entries of the form:

```
<section> {
       <attribute> <value>
       ...
       <subsection> {
              <attribute> <value>
              ...
       }
}
```

The following keywords are recognized:

* **`defaults`**: Defines default values for attributes used whenever no values are given in the appropriate device or multipath sections.

* **`blacklist`**: Defines which devices should be excluded from the multipath topology discovery.

* **`blacklist_exceptions`**: Defines which devices should be included in the multipath topology discovery, despite being listed in the blocklist section.

* **`multipaths`**: Defines the multipath topologies. They are indexed by a World Wide Identifier (WWID). Attributes set in this section take precedence **over all others**.

* **`devices`**: Defines the device-specific settings. Devices are identified by vendor, product, and revision.

* **`overrides`**: This section defines values for attributes that should override the device-specific settings for all devices.

## Configuration file defaults

Currently, the multipath configuration file ONLY includes a minor `defaults` section that sets the `user_friendly_names` parameter to 'yes':

```text
defaults {
    user_friendly_names yes
}
```

This overwrites the default value of the `user_friendly_names` parameter.

All the multipath attributes that can be set in the `defaults` section of the `multipath.conf` file can be found {manpage}`in the manual pages <multipath.conf(5)>` with an explanation of what they mean. The attributes are:

* `verbosity`
* `polling_interval`
* `max_polling_interval`
* `reassign_maps`
* `multipath_dir`
* `path_selector`
* `path_grouping_policy`
* `uid_attrs`
* `uid_attribute`
* `getuid_callout`
* `prio`
* `prio_args`
* `features`
* `path_checker`
* `alias_prefix`
* `failback`
* `rr_min_io`
* `rr_min_io_rq`
* `max_fds`
* `rr_weight`
* `no_path_retry`
* `queue_without_daemon`
* `checker_timeout`
* `flush_on_last_del`
* `user_friendly_names`
* `fast_io_fail_tmo`
* `dev_loss_tmo`
* `bindings_file`
* `wwids_file`
* `prkeys_file`
* `log_checker_err`
* `reservation_key`
* `all_tg_pt`
* `retain_attached_hw_handler`
* `detect_prio`
* `detect_checker`
* `force_sync`
* `strict_timing`
* `deferred_remove`
* `partition_delimiter`
* `config_dir`
* `san_path_err_threshold`
* `san_path_err_forget_rate`
* `san_path_err_recovery_time`
* `marginal_path_double_failed_time`
* `marginal_path_err_sample_time`
* `marginal_path_err_rate_threshold`
* `marginal_path_err_recheck_gap_time`
* `delay_watch_checks`
* `delay_wait_checks`
* `marginal_pathgroups`
* `find_multipaths`
* `find_multipaths_timeout`
* `uxsock_timeout`
* `retrigger_tries`
* `retrigger_delay`
* `missing_uev_wait_timeout`
* `skip_kpartx`
* `disable_changed_wwids`
* `remove_retries`
* `max_sectors_kb`
* `ghost_delay`
* `enable_foreign`

```{note}
Previously, the `multipath-tools` project provided a complete configuration file with all the most commonly used options for each of the most-used storage devices. Currently, you can see all those default options by running `sudo multipath -t`. This will dump a used configuration file including all the embedded default options.
```

## Configuration file blocklist and exceptions

The blocklist section is used to exclude specific devices from the multipath topology. It is most commonly used to exclude local disks, non-multipathed devices, or non-disk devices.

### By `devnode`

The default blocklist consists of the regular expressions `"^(ram|zram|raw|loop|fd|md|dm-|sr|scd|st|dcssblk)[0-9]"` and `"^(td|hd|vd)[a-z]"`. This causes virtual devices, non-disk devices, and some other device types to be excluded from multipath handling by default.

```text
blacklist {
    devnode "^(ram|zram|raw|loop|fd|md|dm-|sr|scd|st|dcssblk)[0-9]"
    devnode "^(td|hd|vd)[a-z]"
    devnode "^cciss!c[0-9]d[0-9]*"
}
```

### By `wwid`

Regular expression for the World Wide Identifier of a device to be excluded/included

### By device

Subsection for the device description. This subsection recognizes the `vendor` and `product` keywords. Both are regular expressions.

```text
device {
    vendor "LENOVO"
    product "Universal Xport"
}
```

### By property

Regular expression for a `udev` property. All devices that have matching `udev` properties will be excluded/included. The handling of the property keyword is special, because devices must have at least one allowlisted `udev` property; otherwise they're treated as blocklisted, and the message "{spellexception}`blacklisted`, `udev` property missing" is displayed in the logs.

### Blocklist by protocol

The protocol strings that multipath recognizes are `scsi:fcp`, `scsi:spi`, `scsi:ssa`, `scsi:sbp`, `scsi:srp`, `scsi:iscsi`, `scsi:sas`, `scsi:adt`, `scsi:ata`, `scsi:unspec`, `ccw`, `cciss`, `nvme`, and `undef`. The protocol that a path is using can be viewed by running: 
   
```bash
multipathd show paths format "%d %P"
```

### Blocklist exceptions

The `blacklist_exceptions` section is used to revert the actions of the blocklist section. This allows one to selectively include ("{spellexception}`whitelist`") devices which would normally be excluded via the blocklist section.

```text
blacklist_exceptions {
    property "(SCSI_IDENT_|ID_WWN)"
}
```

```{note}
A common use is to blocklist "everything" using a catch-all regular expression, and create specific `blacklist_exceptions` entries for those devices that should be handled by `multipath-tools`.
```

## Configuration file multipath section

The `multipaths` section allows setting attributes of **multipath maps**. The attributes set via the multipaths section (see list below) take precedence over all other configuration settings, including those from the overrides section.

The only recognized attribute for the multipaths section is the multipath subsection. If there is more than one multipath subsection matching a given WWID, the contents of these sections are merged, and settings from later entries take precedence.

The multipath subsection recognizes the following attributes:

 * `wwid`: (Mandatory) World Wide Identifier. Detected multipath maps are matched against this attribute. Note that, unlike the `wwid` attribute in the blocklist section, this is not a regular expression or a sub-string; WWIDs must match exactly inside the multipaths section.

 * `alias`: Symbolic name for the multipath map. This takes precedence over an entry for the same WWID in the `bindings_file`.

### Optional attributes

The following attributes are optional; if not set, the default values are taken from the overrides, devices, or defaults section of the {manpage}`multipath.conf(5)` manual page:

 * `path_grouping_policy`
 * `path_selector`
 * `prio`
 * `prio_args`
 * `failback`
 * `rr_weight`
 * `no_path_retry`
 * `rr_min_io`
 * `rr_min_io_rq`
 * `flush_on_last_del`
 * `features`
 * `reservation_key`
 * `user_friendly_names`
 * `deferred_remove`
 * `san_path_err_threshold`
 * `san_path_err_forget_rate`
 * `san_path_err_recovery_time`
 * `marginal_path_err_sample_time`
 * `marginal_path_err_rate_threshold`
 * `marginal_path_err_recheck_gap_time`
 * `marginal_path_double_failed_time`
 * `delay_watch_checks`
 * `delay_wait_checks`
 * `skip_kpartx`
 * `max_sectors_kb`
 * `ghost_delay`

### Example

```text
multipaths {
    multipath {
        wwid                    3600508b4000156d700012000000b0000
        alias                   yellow
        path_grouping_policy    multibus
        path_selector           "round-robin 0"
        failback                manual
        rr_weight               priorities
        no_path_retry           5
    }
    multipath {
        wwid                    1DEC_____321816758474
        alias                   red
    }
}
```

## Configuration file devices section

`multipath-tools` has a built-in **device table** with reasonable defaults for more than 100 known multipath-capable storage devices. The `devices` section can be used to override these settings. If there are multiple matches for a given device, the attributes of all matching entries are applied to it. If an attribute is specified in several matching device subsections, later entries take precedence. 

The only recognized attribute for the `devices` section is the `device` subsection. Devices detected in the system are matched against the device entries using the vendor, product, and revision fields.

The vendor, product, and revision fields that multipath or `multipathd` detect for devices in a system depend on the device type. For SCSI devices, they correspond to the respective fields of the "SCSI INQUIRY" page. In general, the command `multipathd show paths format "%d %s"` command can be used to see the detected properties for all devices in the system.

The device subsection recognizes the following attributes:

1. **`vendor`**: (Mandatory) Regular expression to match the vendor name.
1. **`product`**: (Mandatory) Regular expression to match the product name.
1. **`revision`**: Regular expression to match the product revision.
1. **`product_blacklist`**: Products with the given vendor matching this string are blocklisted.
1. **`alias_prefix`**: The `user_friendly_names` prefix to use for this device type, instead of the default `mpath`.
1. **`hardware_handler`**: The hardware handler to use for this device type. The following hardware handlers are implemented (all of these are hardware-dependent):
   * **`1 emc`**: Hardware handler for {term}`DGC` class arrays as CLARiiON CX/AX and EMC VNX and Unity families.
   * **`1 rdac`**: Hardware handler for LSI / {term}`Engenio` / NetApp RDAC class as NetApp {spellexception}`SANtricity` E/EF Series, and OEM arrays from IBM DELL SGI STK and SUN.
   * **`1 hp_sw`**: Hardware handler for HP/COMPAQ/DEC HSG80 and MSA/HSV arrays with Active/Standby mode exclusively.
   * **`1 alua`**: Hardware handler for SCSI-3 ALUA-compatible arrays.
   * **`1 ana`**: Hardware handler for NVMe ANA-compatible arrays.

### Optional attributes

The following attributes are optional -- if not set, the default values are taken from the defaults section: 

 * `path_grouping_policy`
 * `uid_attribute`
 * `getuid_callout`
 * `path_selector`
 * `path_checker`
 * `prio`
 * `prio_args`
 * `features`
 * `failback`
 * `rr_weight`
 * `no_path_retry`
 * `rr_min_io`
 * `rr_min_io_rq`
 * `fast_io_fail_tmo`
 * `dev_loss_tmo`
 * `flush_on_last_del`
 * `user_friendly_names`
 * `retain_attached_hw_handler`
 * `detect_prio`
 * `detect_checker`
 * `deferred_remove`
 * `san_path_err_threshold`
 * `san_path_err_forget_rate`
 * `san_path_err_recovery_time`
 * `marginal_path_err_sample_time`
 * `marginal_path_err_rate_threshold`
 * `marginal_path_err_recheck_gap_time`
 * `marginal_path_double_failed_time`
 * `delay_watch_checks`
 * `delay_wait_checks`
 * `skip_kpartx`
 * `max_sectors_kb`
 * `ghost_delay`
 * `all_tg_pt`

### Example

```text
devices {
    device {
        vendor "3PARdata"
        product "VV"
        path_grouping_policy "group_by_prio"
        hardware_handler "1 alua"
        prio "alua"
        failback "immediate"
        no_path_retry 18
        fast_io_fail_tmo 10
        dev_loss_tmo "infinity"
    }
    device {
        vendor "DEC"
        product "HSG80"
        path_grouping_policy "group_by_prio"
        path_checker "hp_sw"
        hardware_handler "1 hp_sw"
        prio "hp_sw"
        no_path_retry "queue"
    }
}
```
