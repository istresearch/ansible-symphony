#!/bin/bash
docker-compose -f /opt/compose/traptor-follow-compose.prod.yml -p traptor "$@"
