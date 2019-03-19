curl -X POST -H "Content-Type: application/json" \
-H "X-Access-Token: $WUNDERLIST_ACCESS_TOKEN" \
-H "X-Client-ID: $WUNDERLIST_CLIENT_ID" \
a.wunderlist.com/api/v1/webhooks \
-d `cat << EOF
{
  "list_id": 134237755,
  "url": "$WUNDERLIST_WEBHOOK_URL",
  "processor_type": "generic",
  "configuration": ""
}
EOF
`
