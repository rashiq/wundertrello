curl -X POST -H "Content-Type: application/json" \
https://api.trello.com/1/tokens/$TRELLO_CLIENT_ID/webhooks/ \
-d `cat << EOF
{
  "key": "$TRELLO_ACCESS_TOKEN",
  "callbackURL": "$TRELLO_WEBHOOK_URL",
  "idModel":"59e51180274d83e7ca907a34",
  "description": "Wunderlist + Trello Sync"
}
EOF
`
