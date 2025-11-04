# generate_ratings.py
import csv, random, time, os
random.seed(42)

os.makedirs("data", exist_ok=True)

num_users = 80
num_movies = 100
rows = []
for user in range(1, num_users + 1):
    rated = random.sample(range(1, num_movies + 1), random.randint(15, 40))
    for mid in rated:
        rating = random.choice([1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0])
        timestamp = int(time.time()) - random.randint(0, 10_000_000)
        rows.append([user, mid, rating, timestamp])

with open("data/ratings.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["userId","movieId","rating","timestamp"])
    writer.writerows(rows)

print(f"Wrote {len(rows)} ratings to data/ratings.csv")
