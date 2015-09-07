```
docker run -t \
-v /home/core/share/codes/src/github.com/CuriosityChina/curio-nsq-admin:/python/CuriosityChina/curio-nsq-admin:rw \
--name curio-nsq -i \
-p 80:8888 \
--link task-mongodb:mongo-rs \
--link nsqd:nsq \
-d python-task-admin /bin/bash

```