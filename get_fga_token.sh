#!/bin/bash
source .env

# Step 01. Get the Bearer Token
curl -X POST \
    https://fga.us.auth0.com/oauth/token \
    -H 'content-type: application/json' \
    -d '{"client_id":"'$CLIENT_ID'","client_secret":"'$CLIENT_SECRET'","audience":"https://api.us1.fga.dev/","grant_type":"client_credentials"}'

# The response will be returned in the form
# {
#  "access_token": "eyJ...Ggg",
#  "expires_in": 86400,
#  "scope": "read:tuples write:tuples check:tuples ... write:authorization-models",
#  "token_type": "Bearer"
# }
# Store the `access_token` value in environment variable `AUTH0_FGA_BEARER_TOKEN`

# Step 02. Use it to authenticate your API calls
#curl -X POST https://api.us1.fga.dev/stores/01GZE886BK7NC959XNE0DJ7PZE/check \
#    -H "Authorization: Bearer $AUTH0_FGA_BEARER_TOKEN" \
#    -H 'content-type: application/json' \
#    -d '{"tuple_key":{"user":"bob","relation":"view","object":"doc:roadmap"}}'