ps aux | grep wundertrello |  grep -v grep | awk '{print $2}' | xargs kill -9
