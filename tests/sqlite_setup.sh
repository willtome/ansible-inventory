#!/bin/bash
rm hosts.db
sqlite3 hosts.db <<EOF
CREATE TABLE hosts(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,  name TEXT NOT NULL, ip TEXT NOT NULL, groups TEXT NOT NULL);
INSERT INTO hosts(name, ip, groups) VALUES ('web1', '192.168.1.21','web,primary');
INSERT INTO hosts(name, ip, groups) VALUES ('web2', '192.168.1.22','web,secondary');
INSERT INTO hosts(name, ip, groups) VALUES ('nxos101', '192.168.1.23','network,cisco');
INSERT INTO hosts(name, ip, groups) VALUES ('nxos102', '192.168.1.24','network,cisco');
INSERT INTO hosts(name, ip, groups) VALUES ('nxos103', '192.168.1.25','network,cisco');
EOF
