# Itv-chat.ru

### Install on server:
```
docker build -t twaddle-chat .
docker run --name redishost -d avezhenya/redis
docker run --name chat -p 8889:8889 --link redishost:redishost -d twaddle-chat
```

If you want automatic deploy you may use _docker-compose_ and _makefile_.