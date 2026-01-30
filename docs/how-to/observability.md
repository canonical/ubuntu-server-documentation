---
myst:
  html_meta:
    description: Monitor Ubuntu Server with Canonical Observability Stack, LMA stack, Logwatch, Munin, and Nagios installation guides.
---

(how-to-observability)=
# Observability

In Ubuntu, it is recommended to use the [Canonical Observability Stack](https://documentation.ubuntu.com/observability/track-2/) to monitor your infrastructure. For more information, see the following links:

* [How to migrate from LMA to COS Lite](https://documentation.ubuntu.com/observability/track-2/how-to/migrate-lma-to-cos-lite/)
* [Integrate COS Lite with un-charmed applications](https://documentation.ubuntu.com/observability/track-2/how-to/integrating-cos-lite-with-uncharmed-applications/)
* [The OpenTelemetry Collector snap](https://snapcraft.io/opentelemetry-collector)


## Classical options

While the classic Logging, Monitoring and Alerting (LMA) stack still works, it is no longer recommended. The documentation in this section will be deprecated for Ubuntu 26.04 LTS and onward.

If you do not need a full LMA stack, there are some other supported tools that can provide similar capabilities.

```{toctree}
:titlesonly:

Set up your LMA stack <observability/set-up-your-lma-stack>
Install Logwatch <observability/install-logwatch>
Install Munin <observability/install-munin>
Install Nagios Core 3 <observability/install-nagios>
Use Nagios with Munin <observability/use-nagios-with-munin>
```
