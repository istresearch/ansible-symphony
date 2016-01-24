Hbase
======

Deploys `Hbase <http://hbase.apache.org>`_

.. warning:: This role requires that both :doc:`zookeeper` and :doc:`hadoop` are properly configured and deployed.

Ansible Keys
------------

* **[hbase-master-node]** - The machine to deploy the master node to.

* **[hbase-regionserver-nodes]** - The machines to deploy Regionserver nodes to.

UI Ports
--------

* **<master>:60010** - Main Hbase UI

* **<regionserver>:60030** - The regionserver UI

Verify Your Installation
------------------------

Besides hitting all of the various UI pages, you can create a simple Hbase table via the following commands:

#. SSH onto the master machine

#. Change user to ``hbase``

#. Run the following command from the installation directory ``/opt/hbase/default``

::

    $ ./bin/hbase shell
    ...
    > t1 = create 'test', 'f1'
    0 row(s) in 1.5800 seconds
    => Hbase::Table - test

    > t1.put 'myrow', 'f1', 'my data'
    0 row(s) in 0.1260 seconds

    > t1.scan
    ROW                        COLUMN+CELL
     myrow                     column=f1:, timestamp=1453308934472, value=my data
    1 row(s) in 0.0260 seconds
