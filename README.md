# AKJ 
This project is created with FastAPI

Supervisor Conf

location: `/etc/supervisor/conf.d/gunicorn.conf`

```
[inet_http_server]
port=127.0.0.1:9001
[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface
[supervisorctl]
serverurl=http://127.0.0.1:9001
[supervisord]
[program:gunicorn]
environment = PYTHONUNBUFFERED=1
user=ubuntu
directory=/var/www/html/python/akj/backenend/fastapi/fastapi_akj/app
command=/var/www/html/python/akj/backenend/fastapi/fastapi_akj/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
autostart=true
autorestart=true
stderr_logfile=/var/log/gunicorn/gunicorn.err.log
stdout_logfile=/var/log/gunicorn/gunicorn.out.log
```

refresh/reload supervisor after changes in code as supervisor creates caches
```
sudo supervisorctl reread && sudo supervisorctl update

``` 

