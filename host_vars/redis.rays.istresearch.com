---
datadog_monitors:
  disk:
    enabled: true
    is_custom_check: false
    use_mount: no
  network:
    enabled: true
    is_custom_check: false
    collect_connection_state: yes
  ntp:
    enabled: true
    is_custom_check: false
    offset_threshold: 60
  redisdb:
    enabled: true
    is_custom_check: false
    host: localhost
    port: 6379
