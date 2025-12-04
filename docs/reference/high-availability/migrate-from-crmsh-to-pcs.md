(migrate-from-crmsh-to-pcs)=
# Migrate from crmsh to pcs

From Ubuntu 23.04 Lunar Lobster onward, `pcs` is the recommended and supported tool for setting up and managing Corosync/Pacemaker clusters in Ubuntu. This is the final Ubuntu release where `crmsh` will be supported (but not recommended) so users will have time to migrate away from `crmsh`.

The migration from `crmsh` to `pcs` is not very complex since both have a similar command-line interface (CLI). Here is a direct mapping of some useful commands from `crmsh` to `pcs`.

| **Action** | **`crmsh`** | **`pcs`** |
| ---------------- | ------------------ | -------------- |
| Show configuration (raw XML) | `crm configure show xml` | `pcs cluster cib` |
| Show configuration (human-friendly) | `crm configure show` | `pcs config` |
| Show cluster status | `crm status` | `pcs status` |
| Put a node in standby mode | `crm node standby NODE` | `pcs node standby NODE` |
| Remove a node from standby mode | `crm node online NODE` | `pcs node unstandby NODE` |
| Set cluster property | `crm configure property PROPERTY=VALUE` | `pcs property set PROPERTY=VALUE` |
| List resource agent classes | `crm ra classes` | `pcs resource standards` |
| List available resource agents by standard | `crm ra list ocf` | `pcs resource agents ocf` |
| List available resource agents by OCF provider | `crm ra list ocf pacemaker` | `pcs resource agents ocf:pacemaker` |
| List available resource agent parameters | `crm ra info AGENT` | `pcs resource describe AGENT` |
| Show available fence agent parameters | `crm ra info stonith:AGENT` | `pcs stonith describe AGENT` |
| Create a resource | `crm configure primitive NAME AGENT params PARAMETERS` | `pcs resource create NAME AGENT PARAMETERS` |
| Show configuration of all resources | `crm configure show` | `pcs resource config` |
| Show configuration of one resource | `crm configure show RESOURCE` | `pcs resource config RESOURCE` |
| Show configuration of fencing resources | `crm resource status` | `pcs stonith config` |
| Start a resource | `crm resource start  RESOURCE` | `pcs resource enable RESOURCE` |
| Stop a resource | `crm resource stop RESOURCE` | `pcs resource disable RESOURCE` |
| Remove a resource | `crm configure delete RESOURCE` | `pcs resource delete RESOURCE` |
| Modify a resource’s instance parameters | `crm resource param RESOURCE set PARAMETER=VALUE` | `pcs resource update RESOURCE PARAMETER=VALUE` |
| Delete a resource’s instance parameters | `crm resource param RESOURCE delete PARAMETER` | `pcs resource update RESOURCE PARAMETER=` |
| List current resource defaults | `crm configure show type:rsc_defaults` | `pcs resource defaults` |
| Set resource defaults | `crm configure rsc_defaults OPTION=VALUE` | `pcs resource defaults OPTION=VALUE` |
| List current operation defaults | `crm configure show type:op_defaults` | `pcs resource op defaults` |
| Set operation defaults | `crm configure op_defaults OPTION=VALUE` | `pcs resource op defaults OPTION=VALUE` |
| Clear fail counts for a resource | `crm resource cleanup RESOURCE` | `pcs resource cleanup` |
| Create a colocation constraint | `crm configure colocation NAME INFINITY: RESOURCE_1 RESOURCE_2` | `pcs constraint colocation add RESOURCE_1 with RESOURCE_2 INFINITY` |
| Create an ordering constraint | `crm configure order NAME mandatory: RESOURCE_1 RESOURCE_2` | `pcs constraint order RESOURCE_1 then RESOURCE_2` |
| Create a location constraint | `crm configure location NAME RESOURCE 50: NODE` | `pcs constraint location RESOURCE prefers NODE=50` |
| Move a resource to a specific node | `crm resource move RESOURCE NODE` | `pcs resource move  RESOURCE NODE` |
| Move a resource away from its current node | `crm resource ban RESOURCE NODE` | `pcs resource ban RESOURCE NODE` |
| Remove any constraints created by moving a resource | `crm resource unmove RESOURCE` | `pcs resource clear RESOURCE` |
