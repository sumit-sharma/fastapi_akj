# AKJ 
This project is created with FastAPI

activate virtual env
```
source ...venv/bin/activate
```
if first time start **pm2**  process

```
pm2 start "gunicorn -w 2 -k uvicorn.workers.UvicornWorker main:app" --name fastapi
```

if there is already running stop/kill process
```
pm2 stop/delete all
```

save pm2
```
pm2 save
```