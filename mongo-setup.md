# Create an ubuntu 18.04 server/vm

### Bootstrap with the following

```bash
#!/bin/bash

sudo apt-get update
wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -

echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list
sudo apt-get update

sudo apt-get install -y mongodb-org=4.2.18 mongodb-org-server=4.2.18 mongodb-org-shell=4.2.18 mongodb-org-mongos=4.2.18 mongodb-org-tools=4.2.18

sudo systemctl daemon-reload
sudo systemctl start mongod
sudo systemctl enable mongod


echo -e "# mongod.conf\n\n# for documentation of all options, see:\n#   http://docs.mongodb.org/manual/reference/configuration-options/\n\n# Where and how to store data.\nstorage:\n  dbPath: /var/lib/mongodb\n  journal:\n    enabled: true\n#  engine:\n#  mmapv1:\n#  wiredTiger:\n\n# where to write logging data.\nsystemLog:\n  destination: file\n  logAppend: true\n  path: /var/log/mongodb/mongod.log\n\n# network interfaces\nnet:\n  port: 27017\n  bindIp: 0.0.0.0\n\n\n# how the process runs\nprocessManagement:\n  timeZoneInfo: /usr/share/zoneinfo\n\n#security:\n\n#operationProfiling:\n\n#replication:\n\n#sharding:\n\n## Enterprise-Only Options:\n\n#auditLog:\n\n#snmp:" | sudo tee /etc/mongod.conf

sudo systemctl restart mongod
```

### Now run the following commands

- `mongo` this should put you into the mongo shell
- `use my_db` creates a database and switches to it
- `db.createCollection('Sample')` this creates a sample collection (this is so there is something inside the database and allows it to save)
