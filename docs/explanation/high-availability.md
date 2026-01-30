---
myst:
  html_meta:
    description: Understanding High Availability concepts including redundancy, failover, load balancing, and DRBD for minimal downtime in Ubuntu Server.
---

(explanation-high-availability)=
# High Availability

High Availability is a way to ensure minimal downtime if and when system failures occur by using redundancy, failover and load balancing to keep services running.

## Introduction

* {ref}`Introduction to High Availability <introduction-to-high-availability>`

## Key concepts

* {ref}`Pacemaker resource agents <pacemaker-resource-agents>`
* {ref}`Pacemaker fence agents <pacemaker-fence-agents>`

```{toctree}
:hidden:

Introduction to HA <intro-to/high-availability>
Pacemaker resource agents <high-availability/pacemaker-resource-agents>
Pacemaker fence agents <high-availability/pacemaker-fence-agents>
```

## See also

* How-to: {ref}`Set up a Distributed Replicated Block Device (DRBD) <install-drbd>`
* Reference: {ref}`reference-high-availability`
