# Docker Commands

1. Start up datatbase

```docker start mysql```

2. Docker Compose

```docker-compose up```

If something already running

```docker-compose rm and then docker-compose up```


3. To access shell of docker compose container

```docker exec -it [name of container] bash```

To find name of container, check output of ```docker-compose up``` or use ```docker ps -a```
