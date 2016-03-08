MySQL
========

Deploys `MySQL <http://www.mysql.com>`_

Ansible Keys
------------

* **[mysql-node]** - The machine to deploy MySQL to.

UI Ports
--------

None

Verify Your Installation
------------------------

MySQL is installed under Supervisord. You can confirm MySQL is installed and running via the following command:

#. SSH onto the MySQL machine.

#. Run the following command from anywhere

::

    $ sudo supervisorctl
    mysql          RUNNING   pid 12345, uptime 0:01:00

