---
myst:
  html_meta:
    description: Step-by-step guide to attaching Ubuntu Pro subscription for enterprise lifecycle support, livepatch, FIPS packages, and security compliance.
---

(attach-your-ubuntu-pro-subscription)=
# Attach your Ubuntu Pro subscription

Attaching the [Ubuntu Pro](https://ubuntu.com/pro) subscription to Ubuntu brings you the [enterprise lifecycle](https://ubuntu.com/about/release-cycle), including [Linux kernel livepatching](https://ubuntu.com/security/livepatch), access to [FIPS-validated packages](https://ubuntu.com/security/fips), and [compliance with security profiles](https://ubuntu.com/security/security-standards) such as CIS. This is not required for Ubuntu Pro instances [through public clouds](https://ubuntu.com/cloud/public-cloud) such as [AWS](https://ubuntu.com/aws/pro), [Azure](https://ubuntu.com/azure/pro) or [GCP](https://ubuntu.com/gcp/pro), since these are automatically attached from launch.

```{note}
Subscriptions are not just for enterprise customers. Anyone can get [a personal subscription](https://ubuntu.com/pro) for free on up to 5 machines, or 50 if you are an [official Ubuntu Community member](https://wiki.ubuntu.com/Membership).
```

The following instructions explain how to attach your subscription to your Ubuntu systems.

## Step 1: Install the Ubuntu Pro Client

This step is necessary for Ubuntu Pro users or holders of personal subscriptions. If you are an Ubuntu Pro user through a public cloud offering, your subscription is already attached and you can skip these instructions.

First, make sure that you have the latest version of the Ubuntu Pro Client running. The package used to access the Pro Client (`pro`) is `ubuntu-advantage-tools`:

```bash
sudo apt update && sudo apt install ubuntu-advantage-tools
```

If you already have `ubuntu-advantage-tools` installed, this install command will upgrade the package to the latest version.

## Step 2: Attach your subscription

To attach your machine to a subscription, run the following command in your terminal:

```bash
sudo pro attach
```

You should see output like this, giving you a link and a code:

```bash
ubuntu@test:~$ sudo pro attach
Initiating attach operation...

Please sign in to your Ubuntu Pro account at this link:
https://ubuntu.com/pro/attach
And provide the following code: H31JIV
```

Open the link without closing your terminal window.

In the field that asks you to enter your code, copy and paste the code shown in the terminal. Then, choose which subscription you want to attach to. By default, the Free Personal Token will be selected.

If you have a paid subscription and want to attach to a different token, you may want to log in first so that your additional tokens will appear.

Once you have pasted your code and chosen the subscription you want to attach your machine to, click on the “Submit” button.

The attach process will then continue in the terminal window, and you should eventually be presented with the following message:

```
Attaching the machine...
Enabling default service esm-apps
Updating Ubuntu Pro: ESM Apps package lists
Ubuntu Pro: ESM Apps enabled
Enabling default service esm-infra
Updating Ubuntu Pro: ESM Infra package lists
Ubuntu Pro: ESM Infra enabled
Enabling default service livepatch
Installing snapd snap
Installing canonical-livepatch snap
Canonical Livepatch enabled
This machine is now attached to 'Ubuntu Pro - free personal subscription'
```

When the machine has successfully been attached, you will also see a summary of which services are enabled and information about your subscription.

Available services can be enabled or disabled on the command line with `pro enable <service name>` and `pro disable <service name>` after you have attached.

## Next steps

- For more information about the Ubuntu Pro Client, you can [read our documentation](https://canonical-ubuntu-pro-client.readthedocs-hosted.com/en/latest/).

- For a guided tour through the most commonly-used commands available through the Ubuntu Pro Client, [check out this tutorial](https://documentation.ubuntu.com/pro-client/en/latest/tutorials/basic_commands/).
