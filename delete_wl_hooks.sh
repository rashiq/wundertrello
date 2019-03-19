#!/bin/bash

delete_hook() {
  http DELETE a.wunderlist.com/api/v1/webhooks/$1 X-Access-Token:$WUNDERLIST_ACCESS_TOKEN X-Client-ID:$WUNDERLIST_CLIENT_ID --verbose
}

export -f delete_hook
http "a.wunderlist.com/api/v1/webhooks?list_id=$WUNDERLIST_LIST_ID" X-Access-Token:$WUNDERLIST_ACCESS_TOKEN X-Client-ID:$WUNDERLIST_CLIENT_ID | jq '.[].id' | xargs -n 1 bash -c 'delete_hook "$@"' _
