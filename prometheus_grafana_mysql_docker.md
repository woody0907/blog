##Use docker to run prometheus and grafana to monit mysql and node

###Environment

__Grafana__:http://47.93.190.72:16003/
or in 47.93.26.124 docker (I have pulled the grafana image,but not run it)

 Mysql:47.93.26.124
 Prometheus:47.93.26.124
```
    docker run -it -d --name prometheus -p 9090:9090 -v /opt/docker/prometheus:/etc/prometheus prom/prometheus -config.file=/etc/prometheus/prometheus.yml

```
__prometheus.yml__
```
global:
  scrape_interval:     60s
  evaluation_interval: 60s

scrape_configs:
  - job_name: prometheus
    static_configs:
      - targets: ['localhost:9090']
        labels:
          instance: prometheus

  - job_name: linux
    static_configs:
      - targets: ['47.93.26.124:9100']
        labels:
          instance: db1

  - job_name: mysql
    static_configs:
      - targets: ['47.93.26.124:9104']
        labels:
          instance: db1
```

__node_exporter:__
```
docker run -d -p 9100:9100 --name node-exporter -v "/proc:/host/proc" -v "/sys:/host/sys" -v "/:/rootfs" --net="host" prom/node-exporter -collector.procfs /host/proc -collector.sysfs /host/sys -collector.filesystem.ignored-mount-points "^/(sys|proc|dev|host|etc)($|/)"

```

__mysql_exporter:__
```
docker run -d -p 9104:9104 -e DATA_SOURCE_NAME="mysql_monitor:mysql_monitor@(localhost:3306)/" prom/mysqld-exporter
```