#!/bin/bash
docker-compose -f /opt/compose/traptor-geo-compose.prod.yml -p traptor "$@"
