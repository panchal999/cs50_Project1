import requests

res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "9GUF2T1jJgHkJKcFYsnkg", "isbns": "0380795272"})

print(res.json())
data=res.json()

print(data['books'][0]['average_rating'])
print(data['books'][0]['work_ratings_count'])

