import streamlit as st
import pandas as pd
import mysql.connector

# ==============================
# DATABASE CONNECTION
# ==============================
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="playgirl123",
    database="OnlineBookstore"
)

# ==============================
# RUN QUERY FUNCTION
# ==============================
def run_query(query):
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    data = cursor.fetchall()
    return pd.DataFrame(data, columns=columns)

# ==============================
# STREAMLIT UI
# ==============================
st.set_page_config(page_title="Online Bookstore Dashboard", layout="wide")

st.title("📚 Online Bookstore Analytics Dashboard")
st.write("SQL + Python + Streamlit Project")

# ==============================
# TOTAL REVENUE
# ==============================
revenue_query = """
SELECT SUM(Total_Amount) AS Total_Revenue
FROM Orders
"""

revenue = run_query(revenue_query)

st.subheader("💰 Total Revenue")

if not revenue.empty:
    st.metric("Revenue", revenue.iloc[0, 0])
else:
    st.warning("No revenue data found")

# ==============================
# TOP SELLING BOOKS
# ==============================
top_books_query = """
SELECT b.Title, SUM(o.Quantity) AS Total_Sold
FROM Orders o
JOIN Books b ON o.Book_ID = b.Book_ID
GROUP BY b.Title
ORDER BY Total_Sold DESC
LIMIT 5
"""

top_books = run_query(top_books_query)

st.subheader("📖 Top Selling Books")
st.dataframe(top_books)

if not top_books.empty:
    st.bar_chart(top_books.set_index("Title"))

# ==============================
# SALES BY GENRE
# ==============================
genre_query = """
SELECT b.Genre, SUM(o.Quantity) AS Books_Sold
FROM Orders o
JOIN Books b ON o.Book_ID = b.Book_ID
GROUP BY b.Genre
"""

genre_sales = run_query(genre_query)

st.subheader("📊 Sales by Genre")
st.dataframe(genre_sales)

if not genre_sales.empty:
    st.bar_chart(genre_sales.set_index("Genre"))

# ==============================
# TOP CUSTOMERS
# ==============================
customer_query = """
SELECT c.Name, SUM(o.Total_Amount) AS Total_Spent
FROM Customers c
JOIN Orders o ON c.Customer_ID = o.Customer_ID
GROUP BY c.Name
ORDER BY Total_Spent DESC
LIMIT 5
"""

top_customers = run_query(customer_query)

st.subheader("👑 Top Customers")
st.dataframe(top_customers)

if not top_customers.empty:
    st.bar_chart(top_customers.set_index("Name"))
