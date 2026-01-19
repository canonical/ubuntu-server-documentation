---
myst:
  html_meta:
    description: "Learn about Energy Performance Preference (EPP) settings for optimizing power consumption and performance on Ubuntu Server."
---

(perf-p-states)=
# CPU Power states

> System tuning tools are either about better understanding the system's
> performance, or applying such knowledge to improve it. See our common
> {ref}`system tuning thoughts<explanation-system-tuning-disclaimer>` for
> some generally applicable considerations about that.

A modern CPU usually can be in one of many P-states (mostly controlling
voltage and frequency) when working as well as C-states (mostly defining how
much of the chip elements are turned off) when idle.
Controlling these has direct influence to performance, but also power
consumption and is therefore considered to be part of
[Power Management](https://docs.kernel.org/admin-guide/pm/working-state.html)

Depending on manufacturer and chip generation different systems might be
active - here we outline some common ones, but actually most others still
share a lot of the same aspects.

Below we will outline the direct access via sysfs, but there are tools that
can inspect and manipulate such settings like EPP or scaling governors on
Ubuntu. Please have a look at {ref}`perf-tune-cpupower` as well.

(perf-cpu-governors)=
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

### Setting CPU Governors

```bash
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
```

This file will normally contain one of the following named profiles:

   * `performance` - Prioritize responsiveness and raw performance.
   * `powersave` - Prioritize a reduction in power consumption.

The full list of options is provided in:

```bash
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors
```

The value can be set via sysfs as well:

```bash
echo performance | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
```

(perf-epp)=
## Energy Performance Preference

Energy Performance Preference (EPP) is a CPU power-management feature available on many modern processors (particularly Intel and AMD). It allows the operating system or user to influence the CPU's balance between performance and power consumption. Instead of forcing a strict maximum performance or minimum power mode, EPP provides a hint to the processor’s hardware power control logic about the desired balance.
Consider it to be quite similar to scaling_governors, but partially handled in a harware/firmware assisted way.

The actual effect depends on the CPU model and firmware, but in general, lower EPP values tell a processor to favor performance while higher values tell it to favor lower power consumption.

### Caveats

* EPP is only a *preference* or hint to the hardware. It does not guarantee that the CPU will behave in a precise or deterministic way.

* EPP value interpretations will often vary between different CPUs.

* Hardware support is required. On some processors, EPP may have no effect even if it appears to be configurable in the OS.

* Some systems may require an update to BIOS settings to allow OS control of power regulation.

### EPP values on Ubuntu

On Ubuntu, the EPP for each core on a CPU is stored in `/sys/devices/system/cpu/cpu#/cpufreq/energy_performance_preference`. To check the current status on cpu0, for example, you can run:

```bash
cat /sys/devices/system/cpu/cpu0/cpufreq/energy_performance_preference
```

This file will normally contain one of the following named profiles:

   * `performance` - Prioritize responsiveness and raw performance.
   * `balance_performance` - Lean toward performance, with lower power consumption.
   * `balance_power` - Lean toward reduced power, with some additional performance.
   * `power` - Prioritize a reduction in power consumption.
   * `default` - Use the default mix of power and performance as recommended by Ubuntu.

The full list of options is provided in `/sys/devices/system/cpu/cpu#/cpufreq/energy_performance_available_preferences`. To see them, run:

```bash
cat /sys/devices/system/cpu/cpu0/cpufreq/energy_performance_available_preferences
```

which will display something like:

```text
default performance balance_performance balance_power power
```

For more specificity, a raw numeric value from **0-255** can also be provided in the `energy_performance_preference` file. In general, a value closer to `0` will prioritize performance and a value closer to `255` will prioritize efficiency.

### Setting EPP values

EPP values are managed through each core's `energy_performance_preference` file, so the EPP values can be updated manually by overriding the contents of that file. For example, to set cpu0 to the `performance` profile, run the following:

```bash
echo performance | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/energy_performance_preference
```

On Ubuntu Desktop, GNOME provides a power management menu in settings with options that may modify EPP values.

![Power mode settings section](../images/power-mode-settings.png)

These settings will normally map to the following EPP profiles:

| Power Mode setting | EPP profile          |
| ------------------ | -------------------- |
| Performance        | performance          |
| Balanced           | balance\_performance |
| Power Saver        | power                |
