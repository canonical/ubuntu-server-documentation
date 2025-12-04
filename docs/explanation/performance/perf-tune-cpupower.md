(perf-tune-cpupower)=
# CPU Governors and the cpupower tool

> System tuning tools are either about better understanding the system's
> performance, or applying such knowledge to improve it. See our common
> {ref}`system tuning thoughts<explanation-system-tuning-disclaimer>` for
> the general reasons for that.

## CPU governors

The kernel provides several CPU governors which can be configured, per core, to
optimize for different needs.

| **Governor**   | Design philosophy   |
| -------------- | ------------------- |
| `ondemand`     | This sets the CPU frequency depending on the current system load. This behavior is usually a good balance between the more extreme options. |
| `conservative` | Similar to `ondemand`, but adapting CPU speed more gracefully rather than jumping to max speed the moment there is any load on the CPU. This behavior is more suitable in a battery-powered environment. |
| `performance` | This sets the CPU statically to the highest frequency. This behavior is best to optimize for speed and latency, but might waste power if being under-used. |
| `powersave`   | Sets the CPU statically to the lowest frequency, essentially locking it to P2. This behavior is suitable to save power without compromises. |
| `userspace`   | Allows a user-space program to control the CPU frequency. |

See the [Linux {spellexception}`CPUFreq` Governors Documentation](https://www.kernel.org/doc/Documentation/cpu-freq/governors.txt)
for a more extensive discussion and explanation of the available Linux CPU governors.

While these governors can be checked and changed directly in `sysfs` at
`/sys/devices/system/cpu/cpu*/cpufreq/scaling_governor`, the command `cpupower`
which comes with the package `linux-tools-common` makes this easier by providing
a command line interface and providing access to several related values.

## Monitor CPU frequency

Before changing anything, look at the current frequencies via `cpupower monitor`.
Many systems have various potential monitors, and by default one sees
all of them which can be quite confusing. Therefore start with looking at
the available power monitors.

Command (list all available `cpupower` monitors available on the system):

```bash
sudo cpupower monitor -l
```

Output (An example from a common consumer laptop):

```bash
Monitor "Nehalem" (4 states) - Might overflow after 922000000 s
  C3	[C] -> Processor Core C3
  C6	[C] -> Processor Core C6
  PC3	[P] -> Processor Package C3
  PC6	[P] -> Processor Package C6
Monitor "Mperf" (3 states) - Might overflow after 922000000 s
  C0	[T] -> Processor Core not idle
  Cx	[T] -> Processor Core in an idle state
  Freq	[T] -> Average Frequency (including boost) in MHz
Monitor "RAPL" (4 states) - Might overflow after 8640000 s
  pack	[M] -> 
  dram	[M] -> 
  core	[M] -> 
  unco	[M] -> 
Monitor "Idle_Stats" (9 states) - Might overflow after 4294967295 s
  POLL	[T] -> CPUIDLE CORE POLL IDLE
  C1	[T] -> MWAIT 0x00
  C1E	[T] -> MWAIT 0x01
  C3	[T] -> MWAIT 0x10
  C6	[T] -> MWAIT 0x20
  C7s	[T] -> MWAIT 0x33
  C8	[T] -> MWAIT 0x40
  C9	[T] -> MWAIT 0x50
  C10	[T] -> MWAIT 0x60
```

Here we can see that the machine has four available monitors shown in `"`.

* `Nehalem` - Hardware specific C states.
* `Mperf` - Average of frequencies and time in active (`C0`) or sleep (`Cx`) states.
* `RAPL` - Running Average Power Limit covering different system elements.
* `Idle_Stats` - Statistics of the `cpuidle` kernel subsystem (software based).

Those counters can represent different system units:

* [T] -> Thread
* [C] -> Core
* [P] -> Processor Package (Socket)
* [M] -> Machine/Platform wide counter

So if we want to know what frequency the CPU threads were in (`Mperf`) and
what was consumed at the different system levels of package, dram, core and
{spellexception}`uncore` (RAPL) averages over a minute (`-i <seconds>`) we would run:

Command:

```bash
sudo cpupower monitor -i 60 -m Mperf,RAPL
```

Output:

```bash
    | Mperf              || RAPL
 CPU| C0   | Cx   | Freq || pack    | dram    | core    | unco
   0| 61,83| 38,17|  1850||616950936|145911797|375373063|71556823
   1| 62,03| 37,97|  1848||616950936|145911797|375373063|71556823
   2| 65,51| 34,49|  1852||616950936|145911797|375373063|71556823
   3| 62,04| 37,96|  1852||616950936|145911797|375373063|71556823
```

## Get details about the boundaries for the CPU frequency

There are more details influencing the CPU frequency, such as the driver used to control the hardware, the min and max frequencies, and potential
boost states. These can be collected with `cpupower frequency-info`

Command:

```bash
cpupower frequency-info
```

Output:

```bash
analyzing CPU 3:
  driver: intel_pstate
  CPUs which run at the same hardware frequency: 3
  CPUs which need to have their frequency coordinated by software: 3
  maximum transition latency:  Cannot determine or is not supported.
  hardware limits: 400 MHz - 4.00 GHz
  available cpufreq governors: performance powersave
  current policy: frequency should be within 400 MHz and 4.00 GHz.
                  The governor "powersave" may decide which speed to use
                  within this range.
  current CPU frequency: Unable to call hardware
  current CPU frequency: 1.80 GHz (asserted by call to kernel)
  boost state support:
    Supported: yes
    Active: yes
```

By default this checks the CPU it is executed on. The argument `-c` can be set
to either a number representing a core or `all` to get the info for all
available CPUs.

## Get details about the idle states

[Idle states](https://docs.kernel.org/admin-guide/pm/cpuidle.html)
represent situations when a CPU enters a state of suspension to save power.
The tool `cpupower idle-info` reports about the available idle states, their
description and attributes. These can be useful when debugging CPU performance
if one is curious about the details of a given state after running
`cpupower monitor` above.

Command:

```bash
cpupower idle-info
```

Output:

```bash
CPUidle driver: intel_idle
CPUidle governor: menu
analyzing CPU 0:

Number of idle states: 9
Available idle states: POLL C1 C1E C3 C6 C7s C8 C9 C10
POLL:
Flags/Description: CPUIDLE CORE POLL IDLE
Latency: 0
Usage: 26053898
Duration: 695768311
C1:
Flags/Description: MWAIT 0x00
Latency: 2
Usage: 263751626
Duration: 21296361635
C1E:
Flags/Description: MWAIT 0x01
Latency: 10
Usage: 1071864698
Duration: 122465703132
C3:
Flags/Description: MWAIT 0x10
Latency: 70
Usage: 941753727
Duration: 117177626397
C6:
Flags/Description: MWAIT 0x20
Latency: 85
Usage: 2580936435
Duration: 1258804567087
C7s:
Flags/Description: MWAIT 0x33
Latency: 124
Usage: 2946723
Duration: 1783856599
C8:
Flags/Description: MWAIT 0x40
Latency: 200
Usage: 1580297534
Duration: 1234136981613
C9:
Flags/Description: MWAIT 0x50
Latency: 480
Usage: 2015405
Duration: 3198208930
C10:
Flags/Description: MWAIT 0x60
Latency: 890
Usage: 511786893
Duration: 1546264384800
```

After reading a bit (much more in the _Further reading_ section) into C-states,
P-states and Idle states we can also re-run `cpupower monitor` without
filtering as now the further columns can be related to the above output.

Command:

```bash
sudo cpupower monitor
```

Output:

```bash
    | Nehalem                   || Mperf              || RAPL                           || Idle_Stats
 CPU| C3   | C6   | PC3  | PC6  || C0   | Cx   | Freq || pack | dram | core | unco      || POLL | C1   | C1E  | C3   | C6   | C7s  | C8   | C9   | C10
   0|  2,99| 11,92|  0,00|  0,00|| 70,98| 29,02|  1991||13733058|2706597|7438396|3080986||  0,05|  1,84|  5,01|  3,87| 14,05|  0,06|  3,81|  0,00|  0,04
   1|  3,58| 14,84|  0,00|  0,00|| 67,65| 32,35|  1991||13733058|2706597|7438396|3080986||  0,07|  1,87|  5,42|  4,46| 17,21|  0,36|  2,73|  0,00|  0,00
   2|  3,99|  7,15|  0,00|  0,00|| 73,25| 26,75|  1990||13733058|2706597|7438396|3080986||  0,09|  1,95|  8,76|  5,20|  9,44|  0,01|  1,12|  0,04|  0,00
   3|  3,86| 13,68|  0,00|  0,00|| 68,40| 31,60|  1990||13733058|2706597|7438396|3080986||  0,03|  2,52|  6,35|  4,92| 15,97|  0,00|  1,52|  0,00|  0,00
```

## What should I do with all of this?

All this information is usually only _data_ without any insight until you
either:

* compare them with historical data (it is generally recommended to gather performance and power metrics regularly to be able to compare them to the healthy state in case of any debugging scenario), or
* compare them with your expectations and act on any mismatch

## Does it match what you expect?

One might have expectations about the behavior of a system. Examples are:

* I'm not doing much -- it should be idling most of the time
* I have a very busy workload, I expect it to run at highest frequency
* I do not expect my workload to allow the system to go into low power states

You can hold any of these assumptions against the output of `cpupower monitor`
and verify that they are true. If they are not, use `cpupower frequency-info` to
check if the current constraints match what you think. And use
`cpupower frequency-set` (below) to set a different governor if needed.

## Control the CPU governors and CPU frequency

An administrator can execute the `cpupower` command to set the CPU governor.

Command (set the CPU governor to `performance` mode on all CPUs):

```bash
cpupower frequency-set -g performance
```

Since all commands of `cpupower` can be for a sub-set of CPUs, one can use `-c` here
as well if that matches what is needed for more complex scenarios.

Command (Set `conservative` on the first 8 cores in a system):
```bash
cpupower -c 0-7 frequency-set -g conservative
```

## Powertop

`powertop` supports the user in identifying reasons for unexpected high power
consumption by listing reasons to wake up from low power states.
The look and feel aligns with the well known `top`.
`powertop` is not installed by default, before trying run `sudo apt install powertop`.
This command needs elevated permissions, so run it with `sudo`.

```bash
sudo powertop
```

It has six tabs for the various areas of interest:

* Overview - frequency and reason for activity
* Idle stats - time spent in the different idle states
* Frequency stats - current frequency per core
* Device stats - activity of devices
* Tunables - a list of system tunables related to power (ratings are to save power, you might have some `Bad` for that being considered better for performance)
* WakeUp - device wake-up status

## Further reading

* [Intel Frequency scaling](https://docs.kernel.org/admin-guide/pm/intel_uncore_frequency_scaling.html)
* [Idle states](https://docs.kernel.org/admin-guide/pm/cpuidle.html)
* [C-states](https://docs.kernel.org/admin-guide/pm/intel_idle.html)
