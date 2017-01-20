---

elasticsearch_heap_size: 31g

data_volume:
  - /dev/xvdb

elasticsearch_is_master: "false"
elasticsearch_is_data: "true"
elasticsearch_data_dir:
  - /data/elasticsearch
