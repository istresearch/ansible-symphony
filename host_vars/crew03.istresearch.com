---
storm_worker_ports: [6701, 6702, 6703, 6704, 6705, 6706, 6707, 6708, 6709, 6710, 6711, 6712, 6713, 6714, 6715, 6716, 6717, 6718, 6719, 6720, 6721, 6722, 6723, 6724, 6725, 6726, 6727, 6728, 6729, 6730, 6731, 6732, 6733, 6734, 6735, 6736, 6737, 6738, 6739, 6740, 6741, 6742]

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
  ist_zookeeper:
    enabled: true
    is_custom_check: true
    host: localhost
    port: "{{ zookeeper_client_port | default(2181) }}"
