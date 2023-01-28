import requests

banned_words = ["spread", "copy and", "/groups/", "/games/", "/catalog/", "/game-pass/", "copy/", "paste", "have robux", "give robux", "give me robux", "robux please", "robux pls", "pls robux", "pls code", "code pls", "give code", "robux plz", "plz robux", "plz give", "pls give", "please give", "join my group", "go to my", "click my", "click on my", "/e free", "/e robux", "shut the hell", "shut up", "/vip"]

class wall:
    def __init__(self, group_id, cookie):
        session = requests.Session()
        self.group_id = group_id
        self.cookie = cookie
        self.session = session
        self.session.cookies.update({
            ".ROBLOSECURITY": self.cookie
        })

    def fetch_csrf(self):
        url = "https://auth.roblox.com/v2/logout"
        response = self.session.post(url)
        return response.headers["x-csrf-token"]

    def get_posts(self, *, sort_order="Desc", limit=10):
        url = f"https://groups.roblox.com/v2/groups/{self.group_id}/wall/posts"
        response = self.session.get(url, params={
            "sortOrder": sort_order,
            "limit": limit
        })

        response = response.json()["data"]

        return [wall_post(post["poster"]["user"]["username"], post["body"], post["poster"]["role"]["rank"], post["id"], self.group_id, self.cookie) for post in response]

class wall_post(wall):
    def __init__(self, author, body, rank, post_id, group_id, cookie):
        self.author = author
        self.body = body
        self.rank = rank
        self.post_id = post_id
        super().__init__(group_id, cookie)

    def __repr__(self):
        return f"{self.author} (Rank: {self.rank}) - \"{self.body}\""

    def scan(self):
        for word in banned_words:
            if word in self.body.lower():
                print(f"Bad word found in post: {self.body}")
                self.delete()

    def delete(self):
        url = f"https://groups.roblox.com/v1/groups/{self.group_id}/wall/posts/{self.post_id}"
        response = self.session.delete(url, headers={"x-csrf-token": self.fetch_csrf()})
        
        if response.status_code == 200:
            print(f"Post {self} deleted")