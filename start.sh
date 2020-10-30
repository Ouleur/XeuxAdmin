#!/bin/bash
app="one4driver"
docker build -t ${app} .
docker run -d -p 56700:80 --name=${app} -v $PWD:/app ${app}
