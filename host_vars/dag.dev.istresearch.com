---

elasticsearch_heap_size: 4g

data_volume:
  - /dev/xvdb

elasticsearch_data_dir:
  - /data/elasticsearch
