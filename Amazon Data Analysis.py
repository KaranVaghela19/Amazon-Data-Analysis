#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


# In[3]:


data = pd.read_csv("Amazon Sale Report.csv")


# In[4]:


data


# In[5]:


missing_values = data.isnull().sum()
data_types = data.dtypes
print(missing_values)
print(data_types )


# # Basic Statistical Summary

# In[6]:


stat_summary = data.describe(include='all')
print(stat_summary)


# # Sales Summary

# In[7]:


data['Date']=pd.to_datetime(data['Date'],format='%m-%d-%y',errors='coerce')
sales_over_time = data.groupby(data['Date'].dt.to_period('M')).sum()['Amount']
sales_over_time.plot(kind='line')


# # Product Analysis

# In[8]:


product_analysis = data.groupby(['Category', 'Size']).agg({'Qty': 'sum', 'Amount': 'sum'}).reset_index()
plt.figure(figsize=(14, 8))
product_pivot = product_analysis.pivot(index='Category', columns='Size', values='Qty')
product_pivot.plot(kind='bar', stacked=True, figsize=(14, 8), colormap='viridis')
plt.title('Quantity Sold by Category and Size')
plt.xlabel('Category')
plt.ylabel('Quantity Sold')
plt.legend(title='Size')
plt.show()


# # Fulfillment Analysis

# In[9]:


fulfillment_analysis = data.groupby('Fulfilment').agg({'Order ID': 'count', 'Amount': 'sum','Status':'count'}).reset_index()
plt.figure(figsize=(10, 6))
plt.pie(fulfillment_analysis['Order ID'], labels=fulfillment_analysis['Fulfilment'], autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Orders by Fulfilment Method')
plt.axis('equal')  
plt.show()


# # Customer Segmentation

# In[10]:



customer_data = data.groupby('index').agg({
    'Order ID': 'nunique',   
    'Amount': 'sum',        
    'Qty': 'sum',            
    'ship-state': 'first'        
}).reset_index()


customer_data['Avg_Order_Value'] = customer_data['Amount'] / customer_data['Order ID']
customer_data['Order_Frequency'] = customer_data['Order ID'] / ((data['Date'].max() - data['Date'].min()).days)
print(customer_data)


# # Geographical Analysis

# In[11]:


geo_analysis = data.groupby(['ship-state']).agg({'Amount': 'sum'}).reset_index()
plt.figure(figsize=(10, 6))
plt.bar(geo_analysis['ship-state'], geo_analysis['Amount'], color='skyblue')
plt.xlabel('ship-state')
plt.ylabel('Amount')
plt.title('Total Amount by State')
plt.xticks(rotation=90)  # Rotate state names for better readability
plt.show()

