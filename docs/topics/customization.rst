Customization
=============

This section explains how to customize your testing environment by:

- Forking this repository
- Adding more machines
- Editing the inventory file
- Running specific roles
- Overriding the defaults
- Writing custom playbooks

Forking this repository
-----------------------

This repository serves as a base to get you started setting up the environment for your project.  All of the roles and tasks are meant to be agnostic and use default settings that should apply to most projects.  To customize the plays and add private roles for your own project, follow these steps first:

#. Create a new repository with your project name such as **ansible-masterblaster**.
#. ``git clone git@github.com:you/ansible-masterblaster``
#. ``cd ansible-masterblaster``
#. ``git remote add upstream git@github.com:istresearch/ansible-symphony``
#. ``git fetch upstream``
#. ``git merge upstream/master``

Now you should have the master code in your private repo.  Run ``git remote -v`` to make sure that the origin is your private repo and the upstream is **ansible-symphony** like this::
    
    origin  git@github.com:you/ansible-masterblaster (fetch)
    origin  git@github.com:you/ansible-masterblaster (push)
    upstream    git@github.com:istresearch/ansible-symphony (fetch)
    upstream    git@github.com:istresearch/ansible-symphony (push)

#. ``mkdir private_roles`` to house your project specific roles.  If you are adding a role that can apply to other projects, please submit a pull request to the upstream repository.
#. In the **ansible.cfg** file, add a line under [defaults], ``roles_path = private_roles/``
#. Modify the repository at the top of the **staging** and **production** inventories if you are using a private repository.
#. ``touch site-applications.yml`` to create your custom applications playbook.

Adding more machines
--------------------

To add more VM's to your test cluster, add a new line to the **vagrant_hosts** file.  The format of the line must match the previous ones because the **Vagrantfile** actually parses the file to know which VM's to spin up.  For example, you can add another infrastructure VM by adding::

    192.168.33.103   vagrant-as-03    vas03    ubuntu

Be sure to also update your **/etc/hosts** file so that you can reference the machine in your Ansible inventory file, **staging**.  Like this::

    192.168.33.103   vagrant-as-03    vas03

Now, run ``vagrant up`` and your new machine should boot.

Editing the inventory file
--------------------------

This repository comes with two inventories, **staging** and  **production**.  The former is used for the Vagrant VM's, and is the default.  The **production** inventory is only a sample and will vary based on your specific site deployment.

As an example, if you wanted to use your new machine as a Storm Supervisor node, change this line in the **staging** file::

    [storm-supervisor-nodes]
    vagrant-as-03

That's it!  When you Ansible from a fresh VM, **vagrant-as-03** will now be used as a Storm Supervisor.

.. note:: Ansible does not have the ability to "delete" configurations, unless specifically tasked to do so.  Start from a new VM for this configuration change to work properly.

Running specific roles
----------------------

Thw **site-infrastructure.yml** playbook has embedded tags in each play to allow the ability to only run specific tasks or groups of tasks.  For example, if you only want the ELK stack, run::

    ansible-playbook site-infrastructure.yml --tags ELK -u vagrant

This will install Elasticsearch, Logstash, and Kibana.

If you only want Zookeeper and Kafka, run::

    ansible-playbook site-infrastructure.yml --tags site-zookeeper,site-kafka -u vagrant

Overriding the defaults
-----------------------

You can override the default Ansible role variables a number of ways.  In order of precedence, **group_vars**, **host_vars**, and ``--extra-vars`` are the easiest ways to do this.

For Vagrant testing, I recommend using **host_vars**, since there are likely only two VM's running and it's a convenient place to store your "test" settings.

If you like the settings and wish to move them into production, add them to a **group_vars** file.  Since **group_vars** has a lower priority than **host_vars**, your test settings will always override your production settings, but only for your VM hosts.

For example, if you want to change some settings for Kafka and Zookeeper, take a look at the **defaults.yml** file for each role.  Copy-paste the variables you wish to change into a file called **host_vars/vagrant-as-01**.  Change to the values you want, and now you have overridden the defaults::

    # New Zookeeper settings
    zookeeper_client_port: 2182

    # New Kafka settings
    kafka_port: 9093

Now re-provision your VM and it should update Zookeeper and Kafka with your new settings.

Writing custom playbooks
------------------------

If you wish to set up your own environment with different roles, it is easy to roll your own top level playbook.  Figure out which roles you want to run, and create a new ``site-custom.yml`` file that has the roles you need.  I recommend giving all plays a tag, and a group level tag like ``ELK``, or ``Webapps`` so you can pick and choose which plays you want to run.