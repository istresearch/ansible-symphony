Pulse UI
========

Installs required infrastructure applications for the Pulse UI platform.

Ansible Keys
------------

* **[pulse-ui-node]** - The machine to deploy the Pulse infrastructure to.

UI Ports
--------

None

Verify Your Installation
------------------------

Verify Apache service is installed and running via the following command:

::

    For Debian & Ubuntu:
    $ sudo service apache2 status
    * apache2 is running

    For CentOS & RedHat
    $ sudo service httpd status
    httpd (pid 1234) is running...

Verify Supervisord, Elasticsearch, Kibana, and MySQL are installed and running via the following command:

::

    $ sudo supervisorctl
    elasticsearch-master_data          RUNNING   pid 11111, uptime 0:01:00
    kibana4                            RUNNING   pid 22222, uptime 0:01:30
    mysql                              RUNNING   pid 33333, uptime 0:02:00

