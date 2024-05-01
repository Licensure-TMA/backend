#!/bin/bash

# Запускает socat на порту 8888, обрабатывая каждое новое подключение с помощью request_handler.sh
socat TCP-LISTEN:8890,reuseaddr,fork EXEC:./request_handler.sh