---
myst:
  html_meta:
    description: "Reference documentation for high availability clustering and failover configurations on Ubuntu Server."
---

(reference-high-availability)=
# High availability

In Ubuntu 23.04 (Lunar) and onward, `pcs` became the recommended and supported tool for managing Pacemaker clusters. The 23.04 release is the last release where `crmsh` is available.

To migrate from `crmsh` to `pcs`, refer to our reference table of {ref}`corresponding commands <migrate-from-crmsh-to-pcs>`.

```{toctree}
:hidden:

Migrate from crmsh to pcs <high-availability/migrate-from-crmsh-to-pcs>
```

## See also

* How-to: {ref}`Set up a distributed replicated block device (DRBD) <install-drbd>`
* Explanation: {ref}`explanation-high-availability`
