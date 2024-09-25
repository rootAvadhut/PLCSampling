import os
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import re

class SettingUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Create and grid the dropdown label with better alignment
        self.dropdown_label = tk.Label(self, text="Select PLC")
        self.dropdown_label.grid(row=0, column=0, padx=(20, 5), pady=(10, 0), sticky="w")

        self.plc_options = [f"PLC{i}" for i in range(1, 21)]
        self.plc_dropdown = ttk.Combobox(self, values=self.plc_options, width=15, state="readonly")
        self.plc_dropdown.set("Select PLC")
        self.plc_dropdown.grid(row=0, column=1, padx=(5, 0), pady=(10, 0), sticky="w")
        self.plc_dropdown.bind("<<ComboboxSelected>>", self.validate_entries)  # Bind dropdown validation

        # Create placeholders for IP Address, Port, and Save button
        self.ip_label = tk.Label(self, text="IP Address")
        self.ip_entry = tk.Entry(self)
        self.ip_entry.bind("<KeyRelease>", self.validate_entries)  # Bind entry validation

        self.port_label = tk.Label(self, text="Port")
        self.port_entry = tk.Entry(self, width=8)
        self.port_entry.bind("<KeyRelease>", self.validate_entries)  # Bind entry validation

        self.save_button = tk.Button(self, text="Save", command=self.save_data, state="disabled")

        # Show additional fields (IP, Port, Save button)
        self.show_additional_fields()

        # Create the table (Treeview) for displaying data from the Excel file
        self.create_table()

    def show_additional_fields(self):
        # Show IP, Port fields and Save button with reduced gaps
        self.ip_label.grid(row=1, column=0, padx=(20, 5), pady=(5, 0), sticky="w")
        self.ip_entry.grid(row=1, column=1, padx=(5, 0), pady=(5, 0), sticky="w")

        self.port_label.grid(row=2, column=0, padx=(20, 5), pady=(5, 0), sticky="w")
        self.port_entry.grid(row=2, column=1, padx=(5, 0), pady=(5, 0), sticky="w")

        self.save_button.grid(row=3, column=0, columnspan=2, pady=(5, 0))

    def create_table(self):
        # Create Treeview widget to display PLC, IP Address, and Port Number
        # Set height to 20 to display all PLCs without scrolling
        self.tree = ttk.Treeview(self, columns=("PLC", "IP Address", "Port"), show="headings", height=20)

        # Define columns
        self.tree.heading("PLC", text="PLC")
        self.tree.heading("IP Address", text="IP Address")
        self.tree.heading("Port", text="Port")

        # Set column widths (increase these to make the table wider)
        self.tree.column("PLC", width=120, anchor="center")
        self.tree.column("IP Address", width=200, anchor="center")
        self.tree.column("Port", width=100, anchor="center")

        # Since there are 20 PLCs, disable the vertical scrollbar
        self.tree.grid(row=0, column=2, rowspan=5, padx=(20, 0), pady=(10, 0), sticky="nsew")
        # Removed scrollbar since we want all rows to fit

        # Load the data from the Excel file and populate the table
        self.load_table_data()

    def load_table_data(self):
        # Path to the Excel file
        file_path = os.path.join("temp", "plc_data.xlsx")

        # Check if the Excel file exists
        if not os.path.exists(file_path):
            # If file doesn't exist, create a new one with default data
            df = pd.DataFrame({
                'PLC': [f"PLC{i}" for i in range(1, 21)],
                'IP Address': [''] * 20,  # Initialize as empty string
                'Port': [0] * 20  # Initialize as integer
            })
            df.to_excel(file_path, index=False)
        else:
            # Load the data from the existing Excel file
            df = pd.read_excel(file_path)

        # Clear the table before populating it
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert data from the dataframe into the Treeview
        for _, row in df.iterrows():
            self.tree.insert("", "end", values=(row['PLC'], row['IP Address'], row['Port']))

    def validate_entries(self, event=None):
        # Enable Save button if both IP and Port fields are valid and a PLC is selected
        ip = self.ip_entry.get()
        port = self.port_entry.get()
        selected_plc = self.plc_dropdown.get()

        if self.validate_ip(ip) and self.validate_port(port) and selected_plc != "Select PLC":
            self.save_button.config(state="normal")
        else:
            self.save_button.config(state="disabled")

    def validate_ip(self, ip):
        # Validate the IP address using a regex pattern
        ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        if re.match(ip_pattern, ip):
            # Ensure each octet is between 0 and 255
            return all(0 <= int(num) <= 255 for num in ip.split('.'))
        return False

    def validate_port(self, port):
        # Validate that the port is an integer and within the range 1-65535
        if port.isdigit():
            port_number = int(port)
            return 1 <= port_number <= 65535
        return False

    def save_data(self):
        ip_address = self.ip_entry.get()
        port = self.port_entry.get()
        selected_plc = self.plc_dropdown.get()

        if selected_plc == "Select PLC":
            messagebox.showerror("Error", "Please select a PLC before saving.")
            return

        if not self.validate_ip(ip_address):
            messagebox.showerror("Error", "Please enter a valid IP Address (e.g., 192.168.1.1).")
            return

        if not self.validate_port(port):
            messagebox.showerror("Error", "Please enter a valid Port number (1-65535).")
            return

        # Prepare the data to update
        port = int(port)  # Convert port to integer

        data_to_update = {
            'PLC': selected_plc,
            'IP Address': ip_address,
            'Port': port
        }

        # Create the 'temp' folder if it doesn't exist
        temp_folder = "temp"
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)

        # Path for the Excel file
        file_path = os.path.join(temp_folder, "plc_data.xlsx")

        # If file doesn't exist, create a new one with PLC1 to PLC20
        if not os.path.exists(file_path):
            # Create the initial dataframe with PLC1 to PLC20
            df = pd.DataFrame({
                'PLC': [f"PLC{i}" for i in range(1, 21)],
                'IP Address': [''] * 20,  # Initialize as string
                'Port': [0] * 20  # Initialize as integer
            })
            df.to_excel(file_path, index=False)

        # Load the existing Excel file
        df = pd.read_excel(file_path)

        # Ensure correct data types: string for 'IP Address' and integer for 'Port'
        df['IP Address'] = df['IP Address'].astype(str)
        df['Port'] = pd.to_numeric(df['Port'], errors='coerce').fillna(0).astype(int)

        # Update the row corresponding to the selected PLC
        df.loc[df['PLC'] == selected_plc, ['IP Address', 'Port']] = [ip_address, port]

        # Save the updated DataFrame back to the Excel file
        df.to_excel(file_path, index=False)

        # Reload the table to reflect the new data
        self.load_table_data()

        messagebox.showinfo("Success", f"Data saved for {selected_plc} to {file_path}")

# # Example of how to integrate this into a Tkinter app
# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("PLC Configuration")
#     SettingUI(root).pack(padx=20, pady=20)
#     root.mainloop()

