Pulse Docker
============

Installs Docker Engine, along with Elasticsearch and Kibana containers needed for the Pulse platform.

Ansible Keys
------------

* **[docker-engine]** - The machine to deploy the Docker Engine and required containers to.

UI Ports
--------
* **<docker-engine>:9200** - Elasticsearch network http port.
* **<docker-engine>:9300** - Elasticsearch network tcp port.
* **<docker-engine>:5601** - Kibana port.

.. note:: All ports are configureable in the plays. The above ports are the defaults.

Verify Your Installation
------------------------

Verify the two Docker containers, **elasticsearch** and **kibana**, are running via the following command:

::

    $ sudo docker ps
    CONTAINER ID        IMAGE                 COMMAND                  CREATED
       STATUS              PORTS                                            NAMES
    40b510cabac3        kibana:4.4            "/docker-entrypoint.s"   31 minutes ago
       Up 31 minutes       0.0.0.0:5601->5601/tcp                           KIBANA_pulse
    ccec3cf86660        elasticsearch:2.2.0   "/docker-entrypoint.s"   32 minutes ago
       Up 32 minutes       0.0.0.0:9200->9200/tcp, 0.0.0.0:9300->9300/tcp   ES_pulse

Verify the **elasticsearch** container is configured correctly via the following command:

::

    $ curl <docker-engine>:9200
    {
      "name" : "Gomi",
      "cluster_name" : "pulse_es_cluster",
      "version" : {
        "number" : "2.2.0",
        "build_hash" : "8ff36d139e16f8720f2947ef62c8167a888992fe",
        "build_timestamp" : "2016-01-27T13:32:39Z",
        "build_snapshot" : false,
        "lucene_version" : "5.4.1"
      },
      "tagline" : "You Know, for Search"
    }

Verify the **kibana** container is configured correctly via teh following command:

::

    $ curl <docker-engine>:5601
    <script>var hashRoute = '/app/kibana';
    var defaultRoute = '/app/kibana';

    var hash = window.location.hash;
    if (hash.length) {
      window.location = hashRoute + hash;
    } else {
      window.location = defaultRoute;
    }</script>

