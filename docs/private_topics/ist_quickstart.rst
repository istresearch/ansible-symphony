IST Site Quickstart
===================

This guide is about software deployment that is specific to IST's development and production environments.  For building your own custom deployment from scratch, please look at the "Forking this repository" section of the :doc:`../topics/customization` guide in the main **ansible-symphony** documentation.

.. note:: Before running anything, you will need to download the "Ansible vault" password from Last Pass.  Copy-paste that password into a file called **vault.passwd** inside your Ansible repo.  By default this file will not be included in Git since it is in the .gitignore file.

Site Infrastructure
-------------------

This section talks about deploying site infrastructure software.  This typically includes any 3rd party tech-stack tools that we use.  Examples include Hadoop, Elastic Search, Redis.

Follow the steps in the main :doc:`../topics/quickstart` guide to get your VM's provisioned with the basic big data stack that we use at IST.  The only difference is that you will have to run the command with ``--vault-password-file vault.passwd`` at the end of it.

If you wish to deploy a specific tag to production, do this::

    ansible-playbook -i production.inventory site-infrastructure.yml --tags <site-app> --vault-password-file vault.passwd

Fill in the ``--tags <site-app>`` with the tag of the infrastructure that you want to run.  For example, ``--tags site-kafka`` or ``--tags ELK``.  You can also limit by server group by using ``--limit aws`` or ``--limit internap``.

Site Applications
-----------------

This section talks about deploying site application software.  This typically includes custom applications that we have developed.  Examples include Cooper, Traptor, Scrapy-Cluster, custom Elastic Search mappings or code.

Typically the **site-infrastructure.yml** top level playbook is run first to provision the software suites needed.  After that is run you can similarly run the **site-applications.yml** playbook by running::

    ansible-playbook -i production.inventory site-applications.yml --tags <site-app> --vault-password-file vault.passwd

Fill in the ``--tags <site-app>`` with the tag of the application that you want to run.  For example, ``--tags site-cooper``.

By default this will deploy to the **staging.inventory** inventory.  If you want to deploy to production, add a ``-i production.inventory`` tag in there.

Differences from public deployments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Even though the commands are the same as in the public **ansible-symphony** repository, they are doing slightly different things in this repository vs. the public one due to custom **group_vars**, **host_vars**, and inventories in this private repository.  Some notable differences:

- **Private accounts** - To work with custom accounts and API keys, we take advantage of group_vars.  Variables that are sensitive are encrypted with ``ansible-vault``, so you need to use a password to run Ansible with these encrypted variables.
- **Private repos** - (http://repo.istresearch.com/infrastructure) and custom pip packages (http://repo.istresearch.com/pip).  In the pubic repo, it grabs everything from public mirrors.
- **Custom inventories** - The inventory files for **staging,inventory** and **production.inventory** are different.  For **staging.inventory** the main difference is the VM's are named differently. The **production.inventory** inventory is completely customized per our AWS and Internap production servers.
- **private_roles** - These are Ansible roles that are not included in the public ansible-symphony repository and for internal IST use only.
- **private_topics** - This is the folder that this document lives in.  These are docs that are specific also for IST use and not available in the public ansible-symphony repository.

FAQ
---

How to I deploy a testing environment?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The **staging.inventory** file is used for this.  Follow :doc:`../topics/quickstart` to get some VM's set up for testing purposes.

How do I run individual roles or only on AWS/Internap, etc?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To run only Internap plays, run::

    ansible-playbook -i production.inventory site-infrastructure.yml --limit internap --vault-password-file vault.passwd

To run only the roles that will be installed on the Internap servers.  Of course you can combine this with ``--tags`` also to limit by tag and server group.

The **production.inventory** file is set up to break up the hosts into groups such as **kafka-nodes**, **storm-nodes**, etc.  There are also "parent group" like **aws-nodes** and **internap-nodes** that include all of the children groups that are in either AWS or Internap.

Each large group of machines is under its own ``.inventory`` file, in order to specify more granular provisioning of the ansible roles.

.. tip:: Check out the :doc:`../topics/customization` guide for some background information.

How do I update the **add-users** role to add new users?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Since this role is custom for IST, it is located in the **private_roles** folder.  It is also encrypted with ``ansible-vault``.  To edit the file, run::

    ansible-vault edit private_roles/add-users/tasks/main.yml --vault-password-file vault.passwd

and the save it with ZZ, :x, or :wq in vim.

How do I add a new role?
^^^^^^^^^^^^^^^^^^^^^^^^
See options below.

Is your new role for a generic software suite?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Submit a pull request to the **ansible-symphony** repo, and then do ``git pull upstream/master`` to get it into the private repository.

Is your new role custom for IST Site deployment?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add it to the **private_roles** directory.  After you do that you will need to add your role to the **site-infrastructure.yml** or **site-applications.yml** main playbook.

Is your new role customer specific and not part of overall IST site deployment?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a new branch off of the master branch in **ansible-symphony-ist** and add your private roles to the **private_roles** folder.
