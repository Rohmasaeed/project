import streamlit as st
import pandas as pd
import mysql.connector

# Database Connection
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="playgirl123",
    database="OnlineBookstore"
)

# Function to run query
def run_query(query):
    df = pd.read_sql(query, conn)
    return df

st.title("📚 Online Bookstore Analytics Dashboard")

st.write("Data Analysis using SQL + Python + Streamlit")

# -----------------------------------
# Total Revenue
# -----------------------------------

revenue_query = """
SELECT SUM(Total_Amount) as Total_Revenue
FROM Orders
"""

revenue = run_query(revenue_query)

st.subheader("💰 Total Revenue")
st.write(revenue)

# -----------------------------------
# Top Selling Books
# -----------------------------------

top_books_query = """
SELECT b.Title, SUM(o.Quantity) as Total_Sold
FROM Orders o
JOIN Books b
ON o.Book_ID = b.Book_ID
GROUP BY b.Title
ORDER BY Total_Sold DESC
LIMIT 5
"""

top_books = run_query(top_books_query)

st.subheader("📖 Top Selling Books")
st.dataframe(top_books)

st.bar_chart(top_books.set_index("Title"))

# -----------------------------------
# Sales by Genre
# -----------------------------------

genre_query = """
SELECT b.Genre, SUM(o.Quantity) as Books_Sold
FROM Orders o
JOIN Books b
ON o.Book_ID = b.Book_ID
GROUP BY b.Genre
"""

genre_sales = run_query(genre_query)

st.subheader("📊 Sales by Genre")
st.dataframe(genre_sales)

st.bar_chart(genre_sales.set_index("Genre"))

# -----------------------------------
# Top Customers
# -----------------------------------

customer_query = """
SELECT c.Name, SUM(o.Total_Amount) as Total_Spent
FROM Customers c
JOIN Orders o
ON c.Customer_ID = o.Customer_ID
GROUP BY c.Name
ORDER BY Total_Spent DESC
LIMIT 5
"""

top_customers = run_query(customer_query)

st.subheader("👑 Top Customers")
st.dataframe(top_customers)

st.bar_chart(top_customers.set_index("Name"))

