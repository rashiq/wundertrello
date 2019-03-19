# wundertrello
A simple app does a two way sync between my wunderlist inbox to and my trello board. 
It does this by registering a webhook for wunderlist and trello.

It automatically applys due dates and sorts items into the right trello board.
My trello setup might not work for you, so I'd advise you to change it to your liking by configuring the logic in the `app.py` file.

**This merely exists because I didn't want to pay for a premium account of IFTTT.**


# Getting started

Create a `.env` file with following variables:

``` sh
# I have a reverse proxy running that serves this through `https://todo.rashiq.me`.
APP_URL="172.18.0.1:4323"

# Wunderlist access token & client id. You have to register a wunderlist app to get those.
WUNDERLIST_ACCESS_TOKEN="xyz"
WUNDERLIST_CLIENT_ID="xyz"
# The list id of the wunderlist list you want to sync/register the webhook for.
WUNDERLIST_LIST_ID="1234"
# The webhook url you want to receive your wunderlist payload to.
WUNDERLIST_WEBHOOK_URL="https://todo.rashiq.me/wunderlist"

# Trello access token & client id. You have to register a trello app to get those.
TRELLO_ACCESS_TOKEN="xyz"
TRELLO_CLIENT_ID="xyz"
# The board id of the trello board you want to sync/register the webhook for.
TRELLO_BOARD_ID="1234"
# The webhook url you want to receive your trello payload to.
TRELLO_WEBHOOK_URL="https://todo.rashiq.me/trello"
```

Run `source .env`

# Registering your webhooks

Run `./init_wunderlist_hook.sh` and `./init_trello_hook.sh`

You can unregister the webhooks by running `./delete_wl_hooks.sh` and `./trello_trello_hooks.sh`

# Run the app

I don't run the app with docker, but if you want to, it should be very easy to containerize it. 
For now just create a `virtualenv`, install all dependencies in `requirements.txt` and run `./start.sh`.

Stop it with `./stop.sh`.
