import requests
import json

class RotaAPI:
    def __init__(self, email: str):
        self.email = email
        self.base_url = "https://rota.praetorian.com/rota/service/play.php"
        res = requests.get(f"{self.base_url}?request=new&email={email}")
        self.cookies = res.cookies

    def place(self, x):
        response = requests.get(f"{self.base_url}?request=place&location={x}", cookies=self.cookies)
        return parse_json_response(response)

    def move(self, x, y):
        response = requests.get(f"{self.base_url}?request=move&from={x}&to={y}", cookies=self.cookies)
        return parse_json_response(response)

    def status(self):
        response = requests.get(f"{self.base_url}?request=status", cookies=self.cookies)
        return parse_json_response(response)

    def reset(self):
        res = requests.get(f"{self.base_url}?request=new&email={self.email}")
        self.cookies = res.cookies
        return parse_json_response(res)


def parse_json_response(response: requests.Response):
    # Try JSON first, else fall back to naked board string if present
    try:
        return response.json()
    except Exception:
        text = response.text.strip()
        if len(text) == 9 and set(text) <= set("-pc"):
            return {"board": text}
        return {"status_code": response.status_code, "text": response.text}
