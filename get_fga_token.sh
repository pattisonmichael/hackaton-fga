AUTH0_FGA_CLIENT_ID=0FStczHzsIMNEWcpTNd59vZfdy1Py9wk
AUTH0_FGA_CLIENT_SECRET="R1QGcNkdXs-FQjE-W5EYQhlkeU8MRM6VL9sRmbS7aWVBe8ulnL8x-9yf8YY5aUSr"
AUTH0_FGA_BEARER_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ino4TzF1WEpUMkZ5UHRqZ3RmZDZoMiJ9.eyJodHRwczovL2ZnYS5kZXYvY2xhaW1zL3N0b3JlX3RpZXIiOiJmcmVlIiwiaHR0cHM6Ly9mZ2EuZGV2L2NsYWltcy9jdXN0b21lcl9pZCI6IjAxR1pFODg1N1JSMFpSN0U2REJIUlFBOUVNIiwiaHR0cHM6Ly9mZ2EuZGV2L2NsYWltcy9zdG9yZV9pZCI6IjAxR1pFODg2Qks3TkM5NTlYTkUwREo3UFpFIiwiaXNzIjoiaHR0cHM6Ly9mZ2EudXMuYXV0aDAuY29tLyIsInN1YiI6IjBGU3Rjekh6c0lNTkVXY3BUTmQ1OXZaZmR5MVB5OXdrQGNsaWVudHMiLCJhdWQiOiJodHRwczovL2FwaS51czEuZmdhLmRldi8iLCJpYXQiOjE2ODMwOTU1MTgsImV4cCI6MTY4MzE4MTkxOCwiYXpwIjoiMEZTdGN6SHpzSU1ORVdjcFROZDU5dlpmZHkxUHk5d2siLCJzY29wZSI6InJlYWQ6dHVwbGVzIHdyaXRlOnR1cGxlcyBjaGVjazp0dXBsZXMgZXhwYW5kOnR1cGxlcyByZWFkOmF1dGhvcml6YXRpb25fbW9kZWxzIHdyaXRlOmF1dGhvcml6YXRpb25fbW9kZWxzIHJlYWQ6YXNzZXJ0aW9ucyB3cml0ZTphc3NlcnRpb25zIHJlYWQ6Y2hhbmdlcyBsaXN0Om9iamVjdHMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMifQ.G2O8Drp6YD2VEOtHTQlHncFzGVs5F_HUBxzlvjRKYijjEgiZN2r7zXzUmMAej716afr-I3PL2A9yFBMivjXSkzmzeDalFEbJWre3LFsH7Pr1Cx1GtqPfwyGrRyoy12A0nC_xU6KpVwVVMv5SRzd8fxouekxtjfCM0iBZH3nlvjxBJzugwTIOIeNj0XV3a8yVb2yr0acJgyb_0t--g27X1FlnkvM26FN7qJ01Wj9Co-10B6-N0LKJ9VbMLcVeMjOvatYVR0oE3PrMCndCDzK8QGd5fiCbgA5ckIdLmwogUj-4hfUE70UIyBMvYxW3vXarr7dcuZqt6Tb93ua0F3orsQ"
# Step 01. Get the Bearer Token
#curl -X POST \
#    https://fga.us.auth0.com/oauth/token \
#    -H 'content-type: application/json' \
#    -d '{"client_id":"'$AUTH0_FGA_CLIENT_ID'","client_secret":"'$AUTH0_FGA_CLIENT_SECRET'","audience":"https://api.us1.fga.dev/","grant_type":"client_credentials"}'

# The response will be returned in the form
# {
#  "access_token": "eyJ...Ggg",
#  "expires_in": 86400,
#  "scope": "read:tuples write:tuples check:tuples ... write:authorization-models",
#  "token_type": "Bearer"
# }
# Store the `access_token` value in environment variable `AUTH0_FGA_BEARER_TOKEN`

# Step 02. Use it to authenticate your API calls
curl -X POST https://api.us1.fga.dev/stores/01GZE886BK7NC959XNE0DJ7PZE/check \
    -H "Authorization: Bearer $AUTH0_FGA_BEARER_TOKEN" \
    -H 'content-type: application/json' \
    -d '{"tuple_key":{"user":"bob","relation":"view","object":"doc:roadmap"}}'