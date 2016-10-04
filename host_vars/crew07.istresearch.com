---
# file: host_vars/crew07.istresearch.com

storm_worker_ports: [6701, 6702, 6703, 6704, 6705, 6706, 6707, 6708, 6709, 6710, 6711, 6712, 6713, 6714, 6715, 6716, 6717, 6718, 6719, 6720, 6721, 6722, 6723, 6724, 6725]
datadog_monitors:
  supervisord:
    enabled: true
    is_custom_check: false
    server_name: '{{ inventory_hostname }}'
  disk:
    enabled: true
    is_custom_check: false
    use_mount: no
  network:
    enabled: true
    is_custom_check: false
    collect_connection_state: yes
  kafka:
    enabled: true
    is_custom_check: false
    host: localhost
    jmx_port: 9999
