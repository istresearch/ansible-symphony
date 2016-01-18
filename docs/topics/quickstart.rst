Quickstart
==========

This guide will get you up and running in a test environment using Vagrant VM's and all the default options.

#.  Copy your **id_rsa.pub** file over to the base repository directory.  Typically this is in **~/.ssh/id_rsa.pub**.
#.  Run ``vagrant up`` in the base directory.  This will boot up your Vagrant machines.
#.  Add the machines to your ``/etc/hosts`` file.  For example,

    ::

        192.168.33.101   vagrant-as-01  vas01
        192.168.33.102   vagrant-as-02  vas02

#.  ``ssh vagrant@vas01`` and ``ssh vagrant@vas02`` to make sure you can successfully log into the machines.  This is required for Ansible provisioning.
#.  ``ansible-playbook site-infrastructure.yml -u vagrant`` to provision all of the infrastructure software.  Note: **staging** is used as the inventory by default.

That's it!  After the Ansible playbooks are complete, you should have a complete test environment with a smattering of the latest and greatest in big data and web scraping tools.

