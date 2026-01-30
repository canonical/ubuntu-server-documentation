---
myst:
  html_meta:
    description: Understanding Device Mapper Multipathing for aggregating I/O paths between server nodes and storage arrays on Ubuntu Server.
---

(explanation-multipath)=
# Multipath

Device Mapper Multipathing (which we call "Multipath") allows you to create a single virtual device to aggregate different input/output (I/O) paths between server nodes and storage arrays.

## Introduction

* {ref}`Introduction to Device mapper multipathing <introduction-to-multipath>`

## Configuration

* {ref}`Configuration options and overview <configuring-multipath>`
* {ref}`Configuration examples <multipath-configuration-examples>`
* {ref}`Common tasks and procedures <common-multipath-tasks-and-procedures>`

```{toctree}
:hidden:

intro-to/multipath
Configuration options and overview <multipath/configuring-multipath>
Configuration examples <multipath/multipath-configuration-examples>
Common tasks and procedures <multipath/common-multipath-tasks-and-procedures>
```
