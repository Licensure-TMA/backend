#!/bin/bash

echo -e "HTTP/1.1 200 OK\r"
echo -e "Content-Type: text/plain\r"
echo -e "Connection: close\r"
echo -e "\r"
echo -e "Received request"

bash /home/defendershow/backend/deploy/webhook.sh