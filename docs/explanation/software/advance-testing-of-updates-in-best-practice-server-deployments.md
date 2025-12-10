---
myst:
  html_meta:
    description: "Understand strategies for testing Ubuntu Server updates in advance using best practices for enterprise deployment environments."
---

(advance-testing-of-updates-in-best-practice-server-deployments)=
# Advance testing of updates in best-practice server deployments

If you manage production server deployments with demanding reliability needs, you probably follow best practices with automated testing of Ubuntu updates in your environment before you deploy them. If an update causes a problem for you, you can hold it back from your production deployments while the problem is resolved.

However, if a problem is identified with a package update *after* release, holding it back in a deployment also holds back security updates for that package. Fixing the issue can also take longer because we also have to consider users who *have* upgraded. Ideally, we would like to identify problems with an update before release, which would allow us to fix it more rapidly, keeping deployments more reliable and secure.

We usually make the final builds of our proposed updates publicly available for at least a week before we publish them. We therefore encourage you to test these proposed updates before we release them so that if you discover an unanticipated problem we can delay the release until the issue is fixed.

So, if you already have automated tests for your deployment, please help us to help you by also running your testing against our proposed updates!

## Information about proposed updates

The status of our proposed update pipeline is available on the [Pending SRU page](https://ubuntu-archive-team.ubuntu.com/pending-sru.html). This displays the packages with prepared updates, and links to the bugs they are intended to fix.

## Testing a single proposed update

Calls for testing are made on individual bugs that are being fixed by a proposed update. You can enable proposed testing as follows.

On Ubuntu 24.04 and later, run `sudo add-apt-repository -yp proposed`. This makes proposed updates visible to APT, but will not install them by default.

On releases prior to Ubuntu 23.04, in addition to `sudo add-apt-repository -yp proposed` it is also necessary to apply a "pin" to APT so that it does not attempt to automatically upgrade all packages to -proposed. See the [Enable proposed wiki page](https://wiki.ubuntu.com/Testing/EnableProposed) for instructions.

Once enabled, you can upgrade just the package `foo` and its necessary dependencies to a proposed update using, for example, `sudo apt-get install -t noble-proposed foo` for 24.04 "Noble Numbat".

After the appropriate packages are upgraded to their proposed versions, you can test your deployment as normal.

## Test all proposed updates together

**Warning:** in the general case, upgrading to "everything" in proposed is not considered safe. Dependencies may not be fully resolvable while an update is still being prepared, and this may lead to APT mistakenly removing packages to make everything resolved. For this reason, this method is not generally recommended.

Further, some packages in proposed may already have been reported to cause a regression and been left there pending a fix, in which case your time would be wasted on duplicate regression reports.

However, in the specific case of best practice automated testing of server deployments, we can assume that the testing is taking place in a sandboxed environment, so this caveat does not cause any damage. You may see intermittent CI failures, however, so we suggest only taking heed of a failure if it persists for more than a day or so. This still leaves plenty of time to alert us to a problem!

To upgrade to all of proposed, enable proposed as described above, then run (for example) `apt-get upgrade -t noble-proposed` for 24.04 "Noble Numbat".

After the appropriate packages are upgraded to their proposed versions, you can test your deployment as normal.

After testing, the test environment should be considered "spent" and not be used again. Instead, re-create and re-upgrade to proposed for any subsequent test run. This prevents proposed updates that were not ultimately released from accidentally being included, and minimizes occurrences of the "inconsistent pocket" problem as described above.

## How to report a regression

 * File a bug against the package if a suitable bug report doesn't already exist.
 * In your report, please specify the version that worked and the version that does not. The output of `apt policy some-package` is helpful to identify this.
 * If the regression is in an update that was already released, please tag the bug `regression-update`.
 * If the regression is caused by an update that was proposed to be released, but not yet released, please tag the bug `regression-proposed`. Please also identify one of the bugs being fixed by the update from the [pending SRU report](https://ubuntu-archive-team.ubuntu.com/pending-sru.html) and note the regression there.

[General information on reporting bugs](https://help.ubuntu.com/community/ReportingBugs) is also available.
