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
    enabled: true
    is_custom_check: false
    collect_connection_state: yes
  docker_daemon:
    enabled: true
    is_custom_check: false
    socket_path: "unix://var/run/docker.sock"
    labels_as_tags: ["com.docker.compose.service", "com.docker.compose.project"]
