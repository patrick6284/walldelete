import wallbot
import json

cookie = ""
group_ids = []

with open("./wallbot_json/data.json") as f:
    data = json.load(f)
    cookie = data["cookie"]
    group_ids = data["group_ids"]

for group_id in group_ids:
    group_wall = wallbot.wall(group_id, cookie)
    posts = group_wall.get_posts()
    
    for post in posts:
        post.scan()