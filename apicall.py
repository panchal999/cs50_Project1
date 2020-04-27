import requests

res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "9GUF2T1jJgHkJKcFYsnkg", "isbns": "9781632168146"})

print(res.json())
