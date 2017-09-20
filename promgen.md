##Install Promgen
__Config__
```
vim CELERY_BROKER_URL
    redis://xxxx:16379/0
vim DATABASE_URL
    mysql://mysql_monitor:xxx@xxx/promgen
vim SECRET_KEY
    xxxx
```
__Init__
```
docker run --rm --network host -v /etc/promgen:/etc/promgen/ kfdm/promgen:latest bootstrap

```
__Update Database__
```
docker run --rm --network host -v /etc/promgen:/etc/promgen/ kfdm/promgen:latest migrate
```

__Start__
```
docker run -d --network host -p 8000:8000 -v /etc/promgen:/etc/promgen/ kfdm/promgen:latest
```