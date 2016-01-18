#Storm
Installs [Apache Storm](http://storm.incubator.apache.org/)

##Requirements
By default neither nimbus nor supervisors will be enabled, set one or both of these variables to enable.
- storm_nimbus_enabled: true
- storm_supervisor_enabled: true

The UI is installed on the same box as nimbus. Typically there is a single nimbus server and multiple supervisors.

The variable are required for proper setup
- nimbus_host
- zookeeper_hosts - comma separated list of hosts, any specified port is ignored 2181 is used.

##License
Apache

##Author Information
Tim Kuhlman

Monasca Team email monasca@lists.launchpad.net
