#!/bin/bash

gunicorn --certfile=/etc/letsencrypt/live/licensure.tech/fullchain.pem \
         --keyfile=/etc/letsencrypt/live/licensure.tech/privkey.pem \
         --bind 0.0.0.0:8082 \
         --workers 3 \
         app
