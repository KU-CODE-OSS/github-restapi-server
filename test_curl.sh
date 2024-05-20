#!/bin/bash

url='http://127.0.0.1:1234/api/user?github_id=123'
header='accept: */*'

for i in {1..5000}
do
  response=$(curl -s -o /dev/null -w "%{http_code}" -X 'GET' "$url" -H "$header")
  echo "Attempt $i: Response Code $response"
done

