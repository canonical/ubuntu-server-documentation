# Attach your Ubuntu Pro subscription

Attaching the [Ubuntu Pro](https://ubuntu.com/pro) subscription to Ubuntu brings you the [enterprise lifecycle](https://ubuntu.com/about/release-cycle), including [Linux kernel livepatching](https://ubuntu.com/security/livepatch), access to [FIPS-validated packages](https://ubuntu.com/security/fips), and [compliance with security profiles](https://ubuntu.com/security/certifications) such as CIS. This is not required for [Ubuntu Pro](https://ubuntu.com/public-cloud) instances through public clouds such as [AWS](https://ubuntu.com/aws/pro), [Azure](https://ubuntu.com/azure/pro) or [GCP](https://ubuntu.com/gcp/pro), since these are automatically attached from launch.

> **Νote**:
> Subscriptions are not just for enterprise customers. Anyone can get [a personal subscription](https://ubuntu.com/pro) for free on up to 5 machines, or 50 if you are an [official Ubuntu Community member](https://wiki.ubuntu.com/Membership).

The following instructions explain how to attach your subscription to your Ubuntu systems.

## Step 1: Install the Ubuntu Pro Client

This step is necessary for Ubuntu Pro users or holders of personal subscriptions. If you are an Ubuntu Pro user through a public cloud offering, your subscription is already attached and you may skip these instructions.

We first need to make sure that we have the latest version of the Ubuntu Pro Client running. The package used to access the Pro Client (`pro`) is `ubuntu-advantage-tools`:

```
sudo apt update 
sudo apt install ubuntu-advantage-tools
```

If you already have `ubuntu-advantage-tools` installed, this install command will upgrade the package to the latest version.

## Step 2: Attach your subscription

Once you have the latest version of the Pro Client installed, you need to attach the Ubuntu Pro token to your Pro Client to gain access to the services provided under Ubuntu Pro.

First you need to retrieve your Ubuntu Pro token from the [Ubuntu Pro dashboard](https://ubuntu.com/pro). To access your dashboard, you need an [Ubuntu One account](https://login.ubuntu.com/). If you still need to create one, be sure to sign up using the email address used to create your subscription.

The Ubuntu One account functions as a single-sign-on (SSO), so once logged in we can go straight to the Ubuntu Pro dashboard at [ubuntu.com/pro](http://ubuntu.com/pro). Then click on the ‘Machines’ column in the 'Your Paid Subscriptions' table to reveal your token. 

Now we’re ready to attach our Ubuntu Pro token to the Pro Client:

```
sudo pro attach <your_pro_token>
```

You will know that the token has been successfully attached when you see the list of services, descriptions and their enabled/disabled status in a table similar to this:

```
SERVICE          ENTITLED  STATUS    DESCRIPTION
esm-apps         yes       enabled   Expanded Security Maintenance for Applications
esm-infra        yes       enabled   Expanded Security Maintenance for Infrastructure
livepatch        yes       enabled   Canonical Livepatch service
realtime-kernel  yes       disabled  Ubuntu kernel with PREEMPT_RT patches integrated
```

Note that Extended Security Maintenance (ESM) and Livepatch will auto-enable once your token has been attached to your machine.

After attaching the Pro Client with your token you can also use the Pro Client to activate most of the Ubuntu Pro services, including Livepatch, FIPS, and the CIS Benchmark tool.

## Further reading
- For more information about the Ubuntu Pro Client, you can [read our documentation](https://canonical-ubuntu-pro-client.readthedocs-hosted.com/en/latest/).

- For a guided tour through the most commonly-used commands available through the Ubuntu Pro Client, [check out this tutorial](https://canonical-ubuntu-pro-client.readthedocs-hosted.com/en/latest/tutorials/basic_commands.html).
