25 5    * * *   pentaho    bash -c 'source /deploy/zuora_producer/current/bin/activ
ate && /deploy/zuora_producer/current/bin/python -u /deploy/zuora_producer/curre
nt/lib/python2.7/site-packages/producers/producer/manager.py -d 5 && deactivate' > /v
ar/log/zuora_producer/producer.log 2>&1
#Run @ 5:25am every day, python -u (no stdout buffer) manager.py (defaults = all/5 days abck) log to producer.log

25 5    * * *   pentaho    bash -c 'source /deploy/zuora_producer/current/bin/activ
ate && /deploy/zuora_producer/current/bin/python -u /deploy/zuora_producer/curre
nt/lib/python2.7/site-packages/producers/producer/manager.py -d 0 -i && deactivate' > /v
ar/log/zuora_producer/producer.log 2>&1
#Run @ 5:25am every day, python -u (no stdout buffer) manager.py (defaults = all/5 days abck) log to producer.log