#!/bin/bash

delete_hook() {
  http DELETE https://api.trello.com/1/tokens/$TRELLO_CLIENT_ID/webhooks/$1 key==$TRELLO_ACCESS_TOKEN token==$TRELLO_CLIENT_ID --verbose
}

export -f delete_hook
http https://api.trello.com/1/tokens/$TRELLO_CLIENT_ID/webhooks key==$TRELLO_ACCESS_TOKEN token==$$TRELLO_CLIENT_ID  | jq '.[].id' | xargs -n 1 bash -c 'delete_hook "$@"' _