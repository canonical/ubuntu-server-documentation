.. _how-to-observability:

Observability
**************

In Ubuntu, it is recommended to use the
`Canonical Observability Stack <https://documentation.ubuntu.com/observability/>`_
to monitor your infrastructure. For more information, see the following links:

* `Getting started with COS Lite <https://documentation.ubuntu.com/observability/tutorial/installation/getting-started-with-cos-lite/>`_
* `How to integrate COS Lite with un-charmed applications <https://documentation.ubuntu.com/observability/how-to/integrating-cos-lite-with-uncharmed-applications/>`_
* `The OpenTelemetry Collector snap <https://snapcraft.io/opentelemetry-collector>`_

Classical options
=================

While the classic Logging, Monitoring and Alerting (LMA) stack still works, it
is no longer recommended. The documentation in this section will be deprecated
for Ubuntu 26.04 LTS and onward.

.. toctree::
   :titlesonly:

   Set up your LMA stack <observability/set-up-your-lma-stack>
   Install Logwatch <observability/install-logwatch>
   Install Munin <observability/install-munin>
   Install Nagios Core 4 <observability/install-nagios>
   Use Nagios with Munin <observability/use-nagios-with-munin>
