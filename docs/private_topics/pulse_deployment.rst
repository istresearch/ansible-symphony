Pulse Deployment
===================

This guide is about deploying Pulse to development and GDK environments. The deployment process uses Ansible playbooks in the **ansible-symphony-ist** repository. To better understand how software deployments using the playbooks in this repository work, please look at the :doc:`ist_quickstart` guide in the **ansible-symphony-ist** documentation.

The Ansible playbooks will be run from a server or computer which we call the **Deployment Machine**. The Pulse platform is installed and configured on a server or computer which we call the **Pulse Host**. 

Requirements
--------------

For the deployment to work correctly, a passwordless SSH connection between the Deployment Machine and the Pulse Host must exist. Additionally, if you choose to run the playbooks with a user other than the *vagrant* user, that user must be part of the sudo group.

Both virtual machines created by the *Vagrantfile* install the necessary Ubuntu 14.04.3 OS by default.

Deployment Machine
^^^^^^^^^^^^^^^^^^^

Please see the requirements for the Deployment Machine in the :doc:`../topics/quickstart` guide.

Pulse Host
^^^^^^^^^^^
The OS for the Pulse Host must be Ubuntu 14.04.3 LTS (GNU/Linux 3.13.0-63-generic x86_64).

Configuration
--------------

You will need to update your machine's *hosts* file with the correct IP addresses and machine names to match the below values. You can also see this information in the *vagrant_hosts* file in the **ansible-symphony-ist** repository.

::

    192.168.33.111     vagrant-ist-01
    192.168.33.112     vagrant-ist-02

You will have to copy your **id_rsa.pub** file to the base directory of the checked out **ansible-symphony-ist** repo on your computer.

Lastly, before running anything you will need to download the "Ansible vault" password from Last Pass and set up the **vault.passwd** file inside your Ansible repo. You an read more about this in the :doc:`ist_quickstart` guide.

VM Creation
------------

The Vagrantfile and playbooks have been configured for immediate deployment. There are three different deployment configurations you may use. 

::

    Deployment Machine     Pulse Host       
    -------------------    --------------
    Your computer          vagrant-ist-01
    vagrant-ist-01         vagrant-ist-01
    vagrant-ist-02         vagrant-ist-01

Depending on which configuration you will be deploying with, you will need to start one or two virtual machines. To start a virtual machine, first navigate to the main directory of the checked out **ansible-symphony-ist** repo on your computer. From this directory, you can start the **vagrant-ist-01** vm with the following command: ::

    $ vagrant up vagrant-ist-01

If you want to start both vm's, run the following command: ::

    $ vagrant up

Running the Playbooks
----------------------

This section talks about deploying site infrastructure software.  This typically includes any 3rd party tech-stack tools that we use.  Examples include Hadoop, Elastic Search, Redis.

Follow the steps in the main :doc:`../topics/quickstart` guide to get your VM's provisioned with the basic big data stack that we use at IST.  The only difference is that you will have to run the command with ``--vault-password-file vault.passwd`` at the end of it.

If you wish to deploy a specific tag to production, do this::

    ansible-playbook -i production site-infrastructure.yml --tags <site-app> --vault-password-file vault.passwd

Fill in the ``--tags <site-app>`` with the tag of the infrastructure that you want to run.  For example, ``--tags site-kafka`` or ``--tags ELK``.  You can also limit by server group by using ``--limit aws`` or ``--limit internap``.
  
Site Applications
-----------------

This section talks about deploying site application software.  This typically includes custom applications that we have developed.  Examples include Cooper, Traptor, Scrapy-Cluster, custom Elastic Search mappings or code.

Typically the **site-infrastructure.yml** top level playbook is run first to provision the software suites needed.  After that is run you can similarly run the **site-applications.yml** playbook by running::

    ansible-playbook -i production site-applications.yml --tags <site-app> --vault-password-file vault.passwd

Fill in the ``--tags <site-app>`` with the tag of the application that you want to run.  For example, ``--tags site-cooper``.

By default this will deploy to the **staging** inventory.  If you want to deploy to production, add a ``-i production`` tag in there.

