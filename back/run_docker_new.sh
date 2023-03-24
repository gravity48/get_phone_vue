#!/bin/bash
docker run -it -v /home/gravity/Work/PycharmProjects/get_phone_view/logfiles:/home/get_phone_view/logfiles -v /home/gravity/Work/PycharmProjects/:/srv -v /home/gravity/Temp/Files:/mnt -p 8080:8080 get_phone_view:new bash
