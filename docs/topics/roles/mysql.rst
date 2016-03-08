MySQL
=====

Deploys `MySQL <http://www.mysql.com>`_

Ansible Keys
------------

* **[mysql-node]** - The machine to deploy MySQL to.

Ports
-----

* **<mysql-node>:3306** - The main port to access MySQL

Verify Your Installation
------------------------

MySQL is installed under Supervisord. You can confirm MySQL is installed and running via the following command:

1. SSH onto the MySQL machine.

2. Log into MySQL (Password stored in the defaults.yml file)

::

    $ mysql -u root -p

3. Execute a command to show the databases within MySQL

::

    mysql> show databases;
    +--------------------+
    | Database           |
    +--------------------+
    | information_schema |
    | mysql              |
    | performance_schema |
    +--------------------+
    3 rows in set (0.00 sec)
