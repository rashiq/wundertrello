ps aux | grep wundertrello |  grep -v grep | awk '{print }' | xargs kill -9
