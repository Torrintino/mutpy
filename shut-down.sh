echo "Shutting down container & cleaning up: "
docker rm -f mutpy_dev
screen -X -S loggingSession quit
screen -wipe
