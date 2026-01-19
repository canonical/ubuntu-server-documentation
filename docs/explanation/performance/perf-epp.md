---
myst:
  html_meta:
    description: "Learn about Energy Performance Preference (EPP) settings for optimizing power consumption and performance on Ubuntu Server."
---

(perf-epp)=
# Energy Performance Preference

> System tuning tools are either about better understanding the system's
> performance, or applying such knowledge to improve it. See our common
> {ref}`system tuning thoughts<explanation-system-tuning-disclaimer>` for
> some generally applicable considerations about that.

Energy Performance Preference (EPP) is a CPU power-management feature available on many modern processors (particularly Intel and AMD). It allows the operating system or user to influence the CPU's balance between performance and power consumption. Instead of forcing a strict maximum performance or minimum power mode, EPP provides a hint to the processor’s hardware power control logic about the desired balance.

The actual effect depends on the CPU model and firmware, but in general, lower EPP values tell a processor to favor performance while higher values tell it to favor lower power consumption.

## Caveats

* EPP is only a *preference* or hint to the hardware. It does not guarantee that the CPU will behave in a precise or deterministic way.

* EPP value interpretations will often vary between different CPUs.

* Hardware support is required. On some processors, EPP may have no effect even if it appears to be configurable in the OS.

* Some systems may require an update to BIOS settings to allow OS control of power regulation.

## EPP values on Ubuntu

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

## Setting EPP values

EPP values are managed through each core's `energy_performance_preference` file, so the EPP values can be updated manually by overriding the contents of that file. For example, to set cpu0 to the `performance` profile, run the following:

```bash
echo performance | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/energy_performance_preference
```

There are several additional tools that can manipulate EPP values on Ubuntu too.

{ref}`cpupower <perf-tune-cpupower>` will likely override the value to `performance` on all cores when swapping to the `performance` governor with:

```bash
sudo cpupower frequency-set -g performance
```

On Ubuntu Desktop, GNOME provides a power management menu in settings with options that may modify EPP values.

![Power mode settings section](../images/power-mode-settings.png)

These settings will normally map to the following EPP profiles:

| Power Mode setting | EPP profile          |
| ------------------ | -------------------- |
| Performance        | performance          |
| Balanced           | balance\_performance |
| Power Saver        | power                |
