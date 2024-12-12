#!/bin/bash
exec uwsgi --http-socket :8080 --module myproject.wsgi:application --master --processes 4 --threads 2
