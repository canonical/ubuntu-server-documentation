---
myst:
  html_meta:
    description: "Understand configuration management tools like Ansible and Puppet, for automating Ubuntu Server configuration and deployment."
---

(config-managers)=
# Configuration managers

There are several configuration management tools that can help manage IT
infrastructure, typically through automating configuration and deployment
processes. The most popular options are Ansible and Puppet.

Although they can be complex to set up initially, they have a clear advantage
in environments where scalability and consistency are important. Both of
these tools are available from the Universe repository. This page will give a
short overview of each of them, along with their suggested use cases.

## Ansible

{term}`Ansible` remains one of the most popular options
due to its simplicity. It uses SSH to orchestrate nodes rather than through an
installed agent. It is therefore most often used in cases where an agentless
architecture is desired, or in small to medium-sized environments where the
use of easy-to-write YAML playbooks can reduce the steepness of the initial
learning curve, and requirements may be less complex. 
 
* **Language**: YAML (for playbooks) and Python.

## Puppet

[Puppet](https://www.puppet.com/) uses a client-server architecture; the
Puppet server (the "{spellexception}`master`") is installed one one or more servers, and the
client (Puppet Agent) is installed on every machine Puppet is to manage. It's
most often used to manage IT infrastructure lifecycles; although it can be
complicated to set up, it is useful in particularly complex or large-scale
environments where detailed reporting is desired.

* **Language**: Puppet domain-specific language (DSL), based on Ruby.

## Further reading

* For a comparison of all open source configuration management software, refer
  to [this Wikipedia table](https://en.wikipedia.org/wiki/Comparison_of_open-source_configuration_management_software).
