#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from pyhive import hive

hive_conn = hive.Connection(host="hive-server", port=10000)
hive_cursor = hive_conn.cursor()


# In[ ]:


import matplotlib.pyplot as plt
import numpy as np

hive_cursor.execute('SELECT COUNT(productid), productcategory FROM ProductSale GROUP BY productcategory')
products = hive_cursor.fetchall()

countItems = []
countItems.extend(product[0] for product in products)

categories = []
categories.extend(product[1] for product in products)
y_pos = np.arange(len(categories))

plt.figure(figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
plt.bar(y_pos, countItems, align='center', alpha=0.5)
plt.xticks(y_pos, categories)
plt.ylabel('Sales Item')
plt.title('Product Categories Sales Report')

plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




