.. image:: https://travis-ci.org/istresearch/ansible-symphony.svg?branch=master
    :target: https://travis-ci.org/istresearch/ansible-symphony


Quickstart
==========

Requirements
------------

The software requirements to run this Ansible code are:

- Unix based machine (Linux, MacOSx)
- Ansible version 2.x
- Vagrant >= 1.8.1
- VirtualBox >= 5.0.12
  
Everything may also work with VMWare as a VM provider for Vagrant, although it has not been tested.

**Ubuntu Trusty 14.04** is used as the default base image for VM creation.  Support for **CentOS 6.5** is deprecated, although the code for RedHat based Linux variants is still available in some roles for reference.

Steps
-----

#.  Copy your **id_rsa.pub** file over to the base repository directory.  Typically this is in **~/.ssh/id_rsa.pub**.
#.  Run ``vagrant up`` in the base directory.  This will boot up your Vagrant machines.
#.  Add the machines to your ``/etc/hosts`` file.  For example,

    ::

        192.168.33.101   vagrant-as-01  vas01
        192.168.33.102   vagrant-as-02  vas02

#.  ``ssh vagrant@vas01`` and ``ssh vagrant@vas02`` to make sure you can successfully log into the machines.  This is required for Ansible provisioning.
#.  ``ansible-playbook site-infrastructure.yml -u vagrant`` to provision all of the infrastructure software.  Note: **staging** is used as the inventory by default.

That's it!  After the Ansible playbooks are complete, you should have a complete test environment with a smattering of the latest and greatest in big data and web scraping tools.

