#!/bin/sh
set -eu

image="pwnsandbox"
container="pwnsandbox"

docker build -t "$image" .
docker rm -f "$container" >/dev/null 2>&1 || true
docker run -d \
  --name "$container" \
  --restart always \
  --privileged \
  --pids-limit 100 \
  --memory 128m \
  --cpus 1.0 \
  -p 127.0.0.1:10058:10058 \
  "$image"

printf 'running: nc 127.0.0.1 10058\n'
