import pandas as pd
from tkinter import filedialog, messagebox
from datetime import datetime

def browse_file(file_entry):
    """Handle file browsing and insert the selected path into the entry."""
    file_path = filedialog.askopenfilename()
    file_entry.delete(0, "end")
    file_entry.insert(0, file_path)

def log_change_to_file(data, file_path):
    """Log the sampled data to the Excel file with a timestamp."""
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
