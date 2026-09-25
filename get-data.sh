#!/bin/sh

if test -z $SOLAIRE_TOKEN
then
  echo 'you forgot about the $SOLAIRE_TOKEN bro'
  exit 1
fi

curl -H "Authorization: Bearer $SOLAIRE_TOKEN" "https://api.le-systeme-solaire.net/rest/bodies/" -o bodies.json
