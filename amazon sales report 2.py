import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
df=pd.read_excel("C:/Users/Lenovo/Downloads/Amazon Sale Report.xlsx")
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
print(df.info())
print(df.isnull().sum())
#data cleaning
df = df.drop(columns=['New'])
df = df.drop(columns=['PendingS'])
print(df)
percent=df.isnull().sum()/df.shape[0]*100
print(percent)
drop_columns = percent[percent >60].index
print("\nColumns to be dropped:")
print(drop_columns)
df.drop(columns=drop_columns, inplace=True)
print(df.info())
plt.figure(figsize=(25,25))
sns.heatmap(df.isnull())
print(plt.show())
# Group by 'Category' and sum 'Amount'
df_grouped = df.groupby('Category').agg(total_amount=('Amount', 'sum')).reset_index()

# Display the grouped data
print(df_grouped)
df['Date'] = pd.to_datetime(df['Date'])

# Handle missing values in 'Amount' column if necessary
df = df.dropna(subset=['Amount'])

# Aggregate sales data by month
sales_over_time = df.resample('M', on='Date').agg({'Amount': 'sum', 'Order ID': 'count'}).reset_index()
sales_over_time.columns = ['Month', 'Total Sales', 'Total Orders']

# Plot sales trends over time
plt.figure(figsize=(14, 7))
sns.lineplot(data=sales_over_time, x='Month', y='Total Sales', marker='o')
plt.title('Total Sales Over Time')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.grid(True)
plt.show()
# Analyze distribution by Category
category_distribution = df.groupby('Category').agg(total_quantity_sold=('Qty', 'sum')).reset_index()
category_distribution = category_distribution.sort_values(by='total_quantity_sold', ascending=False)

plt.figure(figsize=(14, 7))
sns.barplot(data=category_distribution, x='total_quantity_sold', y='Category', palette='viridis')
plt.title('Distribution of Quantities Sold by Product Category')
plt.xlabel('Total Quantity Sold')
plt.ylabel('Product Category')
plt.show()
# Analyze distribution by Size
size_distribution = df.groupby('Size').agg(total_quantity_sold=('Qty', 'sum')).reset_index()
size_distribution = size_distribution.sort_values(by='total_quantity_sold', ascending=False)

plt.figure(figsize=(14, 7))
sns.barplot(data=size_distribution, x='Size', y='total_quantity_sold', palette='coolwarm')
plt.title('Distribution of Quantities Sold by Product Size')
plt.xlabel('Product Size')
plt.ylabel('Total Quantity Sold')
plt.show()

# Identify the most popular products
most_popular_category = category_distribution.iloc[0]
print(f"Most Popular Category: {most_popular_category['Category']} with {most_popular_category['total_quantity_sold']} units sold")
most_popular_size = size_distribution.iloc[0]
print(f"Most Popular Size: {most_popular_size['Size']} with {most_popular_size['total_quantity_sold']} units sold")

# Identify the most popular products
most_popular_category = category_distribution.iloc[0]
print(f"Most Popular Category: {most_popular_category['Category']} with {most_popular_category['total_quantity_sold']} units sold")
most_popular_size = size_distribution.iloc[0]
print(f"Most Popular Size: {most_popular_size['Size']} with {most_popular_size['total_quantity_sold']} units sold")

# Check the unique fulfillment methods
print(df['Fulfilment'].unique())
# Analyze the effectiveness of fulfillment methods by order status
fulfillment_analysis = df.groupby(['Fulfilment', 'Status']).agg(order_count=('Order ID', 'count')).reset_index()
# Calculate the percentage of each status within each fulfillment method
fulfillment_analysis['percentage'] = fulfillment_analysis.groupby('Fulfilment')['order_count'].apply(lambda x: 100 * x / x.sum())
# Plot the effectiveness of fulfillment methods
plt.figure(figsize=(14, 7))
sns.barplot(data=fulfillment_analysis, x='Fulfilment', y='percentage', hue='Status', palette='Set2')
plt.title('Effectiveness of Fulfillment Methods by Order Status')
plt.xlabel('Fulfillment Method')
plt.ylabel('Percentage of Orders')
plt.legend(title='Order Status', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# Aggregate features for each customer
customer_data = df.groupby('Order ID').agg({
    'Qty': 'sum',
    'Amount': 'sum',
    'ship-city': 'first',
    'ship-state': 'first'
}).reset_index()
# Define segmentation criteria
def segment_customer(row):
    if row['Amount'] > 1000 and row['Qty'] > 10:
        return 'High Value, High Quantity'
    elif row['Amount'] > 1000:
        return 'High Value'
    elif row['Qty'] > 10:
        return 'High Quantity'
    else:
        return 'Regular'
# Apply the segmentation
customer_data['Segment'] = customer_data.apply(segment_customer, axis=1)
# Analyze each segment
segment_summary = customer_data.groupby('Segment').agg({
    'Qty': 'mean',
    'Amount': 'mean',
    'ship-city': lambda x: x.mode()[0],
    'ship-state': lambda x: x.mode()[0]
}).reset_index()
print("Segment Summary:")
print(segment_summary)
# Visualize the segments
import seaborn as sns
import matplotlib.pyplot as plt
plt.figure(figsize=(12, 8))
sns.scatterplot(data=customer_data, x='Qty', y='Amount', hue='Segment', palette='Set2', marker='o')
plt.title('Customer Segmentation')
plt.xlabel('Total Quantity Purchased')
plt.ylabel('Total Amount Spent')
plt.legend(title='Segment')
plt.show()

df = df.dropna(subset=['ship-city', 'ship-state', 'Amount'])
# Aggregate sales by state
sales_by_state = df.groupby('ship-state').agg({
    'Amount': 'sum',
    'Qty': 'sum'
}).reset_index()
# Aggregate sales by city
sales_by_city = df.groupby('ship-city').agg({
    'Amount': 'sum',
    'Qty': 'sum'
}).reset_index()
# Plot total sales by state
plt.figure(figsize=(12, 6))
sns.barplot(data=sales_by_state, x='ship-state', y='Amount', palette='viridis')
plt.title('Total Sales Amount by State')
plt.xlabel('State')
plt.ylabel('Total Sales Amount')
plt.xticks(rotation=90)
plt.show()
# Plot total sales by city
plt.figure(figsize=(12, 6))
top_cities = sales_by_city.nlargest(10, 'Amount')  # Show top 10 cities
sns.barplot(data=top_cities, x='ship-city', y='Amount', palette='viridis')
plt.title('Top 10 Cities by Total Sales Amount')
plt.xlabel('City')
plt.ylabel('Total Sales Amount')
plt.xticks(rotation=90)
plt.show()



