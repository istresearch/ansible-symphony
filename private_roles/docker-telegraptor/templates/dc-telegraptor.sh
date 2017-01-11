#!/bin/bash
docker-compose -f /opt/compose/telegraptor-compose.prod.yaml -p telegraptor "$@"