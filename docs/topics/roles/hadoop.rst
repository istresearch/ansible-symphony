Hadoop
======

Deploys `HDFS <http://hadoop.apache.org>`_

Ansible Keys
------------

* **[hadoop-namenode-node]** - The machine to deploy Namenode to.


* **[hadoop-secondary-namenode-node]** - The machines to deploy Secondary Namenode to.

* **[hadoop-datanode-nodes]** - - The machines to deploy Datanodes to.

UI Ports
--------

* **<namenode>:50070** - Main HDFS UI

* **<namenode>:19888** - Job History UI

* **<namenode>:8088** - HDFS Node UI

* **<secodary_namenode>:50090** - Secondary Namenode UI

Verify Your Installation
------------------------

Besides hitting all of the various UI pages, you can run an example Map Reduce Job by doing the following

#. SSH onto the namenode machine

#. Change user to ``hadoop``

#. Run the following command from the installation directory ``/opt/hadoop/default``

::

    # substitute <version> for the current HDFS version installed
    $ bin/hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-<version>.jar pi 10 1000
    ...
    Job Finished in 22.502 seconds
    Estimated value of Pi is 3.14080000000000000000
