import pandas as pd
import os
import sqlite3 as sql
import matplotlib.pyplot as plt

conn = sql.connect("C:/data_analysis/analysis/data.db")

cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS customers")
cursor.execute("DROP TABLE IF EXISTS orders")
cursor.execute("DROP TABLE IF EXISTS order_items")


cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER,
    name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER,
    customer_id INTEGER,
    product TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS order_items (
     amount INTEGER,
     revenue INTEGER,
     order_id INTEGER,
     date TEXT
)
""")

cursor.executemany(
    "INSERT INTO customers VALUES (?, ?)",
    [
        (1, "Ana"),
        (2, "Jack"),
        (3, "Michael")
    ]
)

cursor.executemany(
    "INSERT INTO orders VALUES (?, ?, ?)",
    [
        (1, 1, "Laptop"),
        (2, 2, "TV"),
        (3, 3, "Speakers")
    ]
)

cursor.executemany(
    "INSERT INTO order_items VALUES (?, ?, ?, ?)",
    [
        (1, 300, 1, "2026-01-05"),
        (1, 500, 2, "2026-03-10"),
        (2, 150, 3, "2026-03-11")
    ]
)


conn.commit()

query = """
SELECT
    c.name,
    c.customer_id,
    o.order_id,
    oi.revenue,
    oi.amount,
    o.product,
    oi.date
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
"""

df = pd.read_sql(query, con=conn)

df["total_revenue"] = df["revenue"] * df["amount"]
print(df[["name", "product", "amount", "revenue", "total_revenue"]])
print(df)

df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.strftime("%Y-%m")

monthly = (
    df.groupby("month")["total_revenue"]
    .sum()
    .reset_index()
)
print(monthly)

os.makedirs("C:/data_analysis/analysis/charts", exist_ok=True)

monthly.plot(x="month", y="total_revenue", kind="line")
plt.title("Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.savefig("charts/revenue_chart.png")
plt.show()