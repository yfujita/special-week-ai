
import requests


def get(url: str) -> requests.Response:
    headers = {'User-Agent': 'Special Week Crawler'}
    return requests.get(url, headers=headers)

