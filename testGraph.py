import pandas as pd
import matplotlib.pyplot as plt

# File path (using raw string to avoid escape sequence issues)
file_path = r"E:\project 4\24-09-2024\temp\analog_register_data.xlsx"

# Load the Excel file
df = pd.read_excel(file_path)

# Combine 'Date' and 'Time' columns to form the x-axis labels as strings
df['DateTime'] = df['Date'].astype(str) + ' ' + df['Time'].astype(str)

# Extract the x and y values for the plot
x_values = df['DateTime']
y_values = df['Register 300002']

# Plot the values, including repetitions
plt.figure(figsize=(10, 6))
plt.plot(x_values, y_values, marker='o', linestyle='-', color='b')

# Set y-axis range from 0 to 10
plt.ylim(0, 10)

# Adding labels and title
plt.xlabel('Date and Time')
plt.ylabel('Register 300002 Values')
plt.title('Register 300002 Values Over Time')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Show grid
plt.grid(True)

# Display the plot
plt.tight_layout()
plt.show()
