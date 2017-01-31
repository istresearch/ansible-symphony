---
# See TEC-1114
datadog_monitors:
  ist_supervisord:
    enabled: true
    is_custom_check: true
    server_name: '{{ inventory_hostname }}'
  disk:
    enabled: true
    is_custom_check: false
    use_mount: no
  network:
    enabled: false
    is_custom_check: false
    collect_connection_state: yes

