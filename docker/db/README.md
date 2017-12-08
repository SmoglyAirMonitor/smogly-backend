## To manually monitor conatiner state use below command
`docker inspect --format='{{json .State.Health}}' smoglybackend_web_db_1`

I.e. message below:
```json
{"Status":"healthy","FailingStreak":0,"Log":[{"Start":"2017-02-02T18:50:42.83427782+01:00","End":"2017-02-02T18:50:42.869961142+01:00","ExitCode":0,"Output":""},{"Start":"2017-02-02T18:51:12.870148749+01:00","End":"2017-02-02T18:51:12.911524939+01:00","ExitCode":0,"Output":""}]}
```

With `docker ps` your container status should be healthy 

    CONTAINER ID        IMAGE                   COMMAND                  CREATED              STATUS                         PORTS               NAMES
    5f3cf5212031        smoglybackend_web_test   "py.test -s --cov=."     About a minute ago   Restarting (0) 4 seconds ago                       smoglybackend_web_test_1
    7765dc8099d9        smoglybackend_web_db     "/docker-entrypoint.s"   2 minutes ago        Up 2 minutes (healthy)         5432/tcp            smoglybackend_web_db_1
