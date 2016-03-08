MySQL ES Connector
==================

Installs the software and scripts required to run the MySQL ES Connector in the Pulse platform. Configures a cron job to run the default ES index.

Ansible Keys
------------

* **[pulse-mysql-es-host]** - The machine to install the MySQL ES Connector on.

UI Ports
--------

None

Verify Your Installation
------------------------

Verify the cron job for the default MySQL ES index has been created via the following command: 

::

    $ sudo crontab -l
    */1 * * * * sudo /opt/miniconda/bin/python2.7 /opt/mysql_es_pulse/mysql_es_pulse.py 
    --dbhost=localhost --dbuser=pulse --db=pulse --pw=12Z0GQ03Eta4 --interval=5 
    --es=vagrant-ist-01:9200 --index=pulse-1 --build=incremental 
    --mapping=/opt/mysql_es_pulse/pulse_mapping_dynamic.json --logfile=/var/log/mysql_es_pulse/pulse.log 
    --db_prefix=pulse

Verify the cron job for the default MySQL ES index has run successfully via the following command:

::

    $ sudo vim /var/log/mysql_es_pulse/pulse.log
    2016-03-07 14:43:11.258011       no db query results for question_responses
    2016-03-07 14:43:11.261572       no db query results for outgoing
    2016-03-07 14:43:11.266470       no db query results for deploy
    2016-03-07 14:44:01.454351       no db query results for question_responses
    2016-03-07 14:44:01.457125       no db query results for outgoing
    2016-03-07 14:44:01.460255       no db query results for deploy
    2016-03-07 14:45:01.623841       no db query results for question_responses
    2016-03-07 14:45:01.626900       no db query results for outgoing
    2016-03-07 14:45:01.630024       no db query results for deploy
    .
    .
    .
