---
myst:
  html_meta:
    description: System performance tuning concepts and tools for Ubuntu Server including CPU power management, hardware locality, and workload optimization.
---

(explanation-system-tuning)=
# Performance

This area of the documentation is about system tuning and will list various tools that can either help to determine the state of the system or to tune it for a given workload.

(explanation-system-tuning-disclaimer)=
:::{note}
Disclaimer - To tune you need to know your system and workload

Almost all tunable parameters can be good for one and bad for another type of workload or environment. If the system could do it for you, it probably would be the default setting already.

Not even the goal of tuning is the same for everyone; do you want to improve latency, throughput, thermal or work-unit-per-power? But those default settings generally have to aim for a good compromise on all of these aspects, no matter what you will do with your system.

Therefore you have to know your workload, your system and the important metrics of what you want to achieve. The more you know, the more you'll be able to improve your system it to suit your needs by:

* Identifying bottlenecks as unblocking them usually has the biggest impact for your workload
* Identifying where your needs are different from the generic assumptions to change related tunables
* Identifying architectural mismatches between the solution and your needs to allow adapting
:::

(end-system-tuning-intro)=
To identify those aspects and to then apply static or dynamic tuning Ubuntu carries various tools, a few of them are outlined in more detail in the following sections.

* Profile-Guided Optimization {ref}`PGO <perf-pgo>`
* Obtain the hierarchical map of key computing elements using {ref}`hwloc and lstopo <perf-tune-hwloc>`
* Understand and directly influence {ref}`perf-p-states`
* Monitori, analyze and control CPU governors, power and frequency with {ref}`cpupower <perf-tune-cpupower>`
* Dynamic, adaptive system tuning {ref}`with TuneD <perf-tune-tuned>`

```{toctree}
:hidden:

Profile-Guided Optimization <performance/perf-pgo>
hwloc <performance/perf-tune-hwloc>
CPU Power (states) <performance/perf-p-states>
cpupower (tool) <performance/perf-tune-cpupower>
TuneD <performance/perf-tune-tuned>
```
