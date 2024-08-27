import tkinter as tk
from tkinter import filedialog, messagebox
import time
import pandas as pd
from datetime import datetime

# Function to handle file browsing
def browse_file():
    file_path = filedialog.askopenfilename()
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

# Function to validate and adjust sampling time
def validate_sampling_time():
    try:
        sampling_time = float(sampling_entry.get())
        if sampling_time < 0.1 or sampling_time > 60000:
            raise ValueError
        return sampling_time
    except ValueError:
        messagebox.showerror("Invalid Input", "Sampling time must be between 0.1 seconds and 1 minute.")
        return None

# Function to sample data and check for changes
def sample_data():
    sampling_time = validate_sampling_time()
    if sampling_time is None:
        return
    
    # Simulate data sampling here, replace this with actual data sampling logic
    sampled_data = get_sampled_data()

    # Check for percentage change
    if has_significant_change(sampled_data):
        log_change_to_file(sampled_data)
    
    # Schedule the next sampling event
    root.after(int(sampling_time * 1000), sample_data)

# Function to simulate data sampling (replace with real logic)
def get_sampled_data():
    # Simulate sampling of digital or analog data
    return {"value": 10}  # Placeholder value

# Function to check for significant changes in data
def has_significant_change(new_data):
    change_threshold = float(change_entry.get())
    # Simulate checking for changes in data (replace with actual comparison logic)
    return True  # Placeholder, assume change detected

# Function to log changes to the Excel file
def log_change_to_file(data):
    file_path = file_entry.get()
    if not file_path:
        messagebox.showerror("Error", "Please select a file to log data.")
        return
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data['timestamp'] = timestamp
    
    # Append data to the Excel file
    try:
        df = pd.DataFrame([data])
        with pd.ExcelWriter(file_path, mode='a', if_sheet_exists='overlay', engine='openpyxl') as writer:
            df.to_excel(writer, index=False, header=writer.sheets['Sheet1'].max_row == 1)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to log data to file: {e}")

# Create the main window
root = tk.Tk()
root.title("PLC Interface")

# Create and place labels and entry fields
tk.Label(root, text="IP Address:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
ip_entry = tk.Entry(root, width=30)
ip_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Port No.:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
port_entry = tk.Entry(root, width=10)  # Adjusted width for 6-digit input
port_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

tk.Label(root, text="Sampling Frequency (ms):").grid(row=2, column=0, padx=10, pady=5, sticky='e')
sampling_entry = tk.Entry(root, width=10)  # Adjusted width for 6-digit input
sampling_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')

# Adding the label "(100 ms to 1 min) (input in milli sec)" next to Sampling Frequency
tk.Label(root, text="(100 ms to 1 min) (input in milli sec)").grid(row=2, column=2, padx=5, pady=5, sticky='w')

tk.Label(root, text="Change in Data (%):").grid(row=3, column=0, padx=10, pady=5, sticky='e')
change_entry = tk.Entry(root, width=10)  # Adjusted width for 6-digit input
change_entry.grid(row=3, column=1, padx=10, pady=5, sticky='w')

# Adding the label "(change in %)" next to Change in Data
tk.Label(root, text="(change in %)").grid(row=3, column=2, padx=5, pady=5, sticky='w')

# File Address Section
tk.Label(root, text="File Address:").grid(row=4, column=0, padx=10, pady=10, sticky='e')
file_entry = tk.Entry(root, width=30)
file_entry.grid(row=4, column=1, padx=10, pady=10, sticky='w')
file_button = tk.Button(root, text="Browse", command=browse_file)
file_button.grid(row=4, column=2, padx=10, pady=10)

# Start sampling process
tk.Button(root, text="Start Sampling", command=sample_data).grid(row=5, column=1, padx=10, pady=20)

# Run the application
root.mainloop()
