import random

import matplotlib.pyplot as plt
import numpy as np

# Generate random data for each month
data_per_month = [random.randrange(30) for month in range(12)]

# Create a bar chart
fig, ax = plt.subplots()

# Plot bars for each month
for i, month_data in enumerate(data_per_month):
    bar = ax.bar(i, month_data, color='skyblue')

    # Add count value on top of the bar
    for rect in bar:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, str(height), ha='center', va='bottom')

# Set y-axis range
ax.set_ylim(0, max(data_per_month) + 5)

# Add labels and title
ax.set_xlabel('Month')
ax.set_ylabel('Number of Validations')
ax.set_title('Histogram Example by Month')

# Customize x-axis labels to show months of the year
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
ax.set_xticks(np.arange(0, 12))
ax.set_xticklabels(months)

# Display the bar chart
plt.show()
