#!/bin/bash

gunicorn --bind 0.0.0.0:8082 \
         --workers 3 \
         app
