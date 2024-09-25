import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk, messagebox
import pandas as pd
import threading
import modbus

# Path to the Excel file
excel_file_path = r"E:\project 4\24-09-2024\temp\plc_data.xlsx"

def readExcel(file_path):
    """Function to read the Excel file and return the data as a DataFrame."""
    try:
        data = pd.read_excel(file_path)
        return data
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

def get_plc_details(plc_data, selected_plc):
    """Function to fetch the details (IP Address, Port) for the selected PLC."""
    plc_row = plc_data[plc_data['PLC'] == selected_plc]
    if not plc_row.empty:
        ip_address = plc_row['IP Address'].values[0]
        port = plc_row['Port'].values[0]
        return ip_address, port
    else:
        return None, None

class HomeUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.plc_data = readExcel(excel_file_path)  # Call readExcel function to get the data
        self.create_widgets()

    def create_widgets(self):
        # Create label for the dropdown
        self.plc_label = tk.Label(self, text="Select PLC:")
        self.plc_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Create a dropdown menu (Combobox)
        self.plc_var = tk.StringVar()  # Variable to hold the selected PLC
        self.plc_combobox = ttk.Combobox(self, textvariable=self.plc_var, state="readonly")
        self.plc_combobox['values'] = [f'PLC{i}' for i in range(1, 21)]  # PLC1 to PLC20
        self.plc_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Sampling Frequency label and entry
        self.sampling_freq_label = tk.Label(self, text="Sampling Frequency (ms):")
        self.sampling_freq_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.sampling_freq_entry = tk.Entry(self)
        self.sampling_freq_entry.insert(0, "1000")  # Default value
        self.sampling_freq_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Change in Data (%) label and entry
        self.change_data_label = tk.Label(self, text="Change in Data (%):")
        self.change_data_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.change_data_entry = tk.Entry(self)
        self.change_data_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Start button
        self.start_button = tk.Button(self, text="Start", command=self.start_process)
        self.start_button.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Create the table layout for PLC Output and Input data
        self.create_plc_output_table()

    def start_process(self):
        selected_plc = self.plc_var.get()  # Get the selected PLC
        sampling_freq = self.sampling_freq_entry.get()  # Get sampling frequency
        change_in_data = self.change_data_entry.get()  # Get change in data

        # Fetch the IP and Port for the selected PLC
        ip_address, port = get_plc_details(self.plc_data, selected_plc)

        if ip_address and port:
            print(f"Selected PLC: {selected_plc}, IP Address: {ip_address}, Port: {port}")
            # Start the Modbus client in a new thread
            threading.Thread(
                target=modbus.run_client,
                args=(ip_address, int(port), int(sampling_freq), self.update_ui),
                daemon=True
            ).start()
        else:
            # Show a popup message if no data is found
            messagebox.showerror("Data Error", f"No data found for: {selected_plc}")

    def create_plc_output_table(self):
        """Function to create PLC Output, Input Bit, and Analog Input tables."""
        # Digital Inputs for Coils table
        title_label = tk.Label(self, text="Digital Inputs for Coils", font=('Helvetica', 12, 'bold'))
        title_label.grid(row=5, column=0, columnspan=3, pady=10, sticky='we')

        headers = ["PLC OUTPUT NO", "MODBUS ADDRESS", "States"]
        for col, header in enumerate(headers):
            label = tk.Label(self, text=header, font=('Helvetica', 10, 'bold'))
            label.grid(row=6, column=col, padx=5, pady=5, sticky='w')

        self.state_labels = []
        for i in range(16):
            output_label = tk.Label(self, text=f"OUT PUT {i}")
            output_label.grid(row=7+i, column=0, padx=10, pady=5, sticky='w')

            address_label = tk.Label(self, text=f"1000{i+1:02}")
            address_label.grid(row=7+i, column=1, padx=10, pady=5, sticky='w')

            state_label = tk.Label(self, text="FALSE")
            state_label.grid(row=7+i, column=2, padx=10, pady=5, sticky='w')
            self.state_labels.append(state_label)

        # Digital Inputs for Input Bit table
        title_label_2 = tk.Label(self, text="Digital Inputs for Input Bit", font=('Helvetica', 12, 'bold'))
        title_label_2.grid(row=5, column=4, columnspan=3, pady=10, sticky='we')

        headers_2 = ["Input Bit NO", "MODBUS ADDRESS", "States"]
        for col, header in enumerate(headers_2):
            label = tk.Label(self, text=header, font=('Helvetica', 10, 'bold'))
            label.grid(row=6, column=4+col, padx=5, pady=5, sticky='w')

        self.input_bit_labels = []
        for i in range(16):
            input_label = tk.Label(self, text=f"INPUT BIT {i}")
            input_label.grid(row=7+i, column=4, padx=10, pady=5, sticky='w')

            address_label = tk.Label(self, text=f"0000{i+1:02}")
            address_label.grid(row=7+i, column=5, padx=10, pady=5, sticky='w')

            state_label = tk.Label(self, text="FALSE")
            state_label.grid(row=7+i, column=6, padx=10, pady=5, sticky='w')
            self.input_bit_labels.append(state_label)

        # Analog Inputs for Input Register table
        title_label_3 = tk.Label(self, text="Analog Inputs for Input Register", font=('Helvetica', 12, 'bold'))
        title_label_3.grid(row=5, column=8, columnspan=3, pady=10, sticky='we')

        headers_3 = ["PLC ANALOG INPUT SLOT", "MODBUS ADDRESS", "Values"]
        for col, header in enumerate(headers_3):
            label = tk.Label(self, text=header, font=('Helvetica', 10, 'bold'))
            label.grid(row=6, column=8+col, padx=5, pady=5, sticky='w')

        self.analog_input_labels = []
        for i in range(8):
            analog_label = tk.Label(self, text=f"ANALOG INPUT {i}")
            analog_label.grid(row=7+i, column=8, padx=10, pady=5, sticky='w')

            address_label = tk.Label(self, text=f"3000{i+2:02}")
            address_label.grid(row=7+i, column=9, padx=10, pady=5, sticky='w')

            value_label = tk.Label(self, text="0")
            value_label.grid(row=7+i, column=10, padx=10, pady=5, sticky='w')
            self.analog_input_labels.append(value_label)

    def update_ui(self, coil_states, input_registers, input_statuses):
        """Function to update the UI with the latest Modbus data."""
        for i, state in enumerate(coil_states or []):
            self.state_labels[i].config(text="TRUE" if state else "FALSE")

        for i, value in enumerate(input_registers or []):
            self.analog_input_labels[i].config(text=str(value))

        for i, status in enumerate(input_statuses or []):
            self.input_bit_labels[i].config(text="TRUE" if status else "FALSE")

if __name__ == "__main__":
    root = tk.Tk()
    home_ui = HomeUI(root)
    home_ui.pack(padx=20, pady=20)
    root.mainloop()



#working code ......
# import tkinter as tk
# from tkinter import ttk
# import pandas as pd
# from tkinter import messagebox  # Import for popup message

# # Path to the Excel file
# excel_file_path = r"E:\project 4\24-09-2024\temp\plc_data.xlsx"

# def readExcel(file_path):
#     """Function to read the Excel file and return the data as a DataFrame."""
#     try:
#         data = pd.read_excel(file_path)
#         return data
#     except Exception as e:
#         print(f"Error reading Excel file: {e}")
#         return None

# def get_plc_details(plc_data, selected_plc):
#     """Function to fetch the details (IP Address, Port) for the selected PLC."""
#     plc_row = plc_data[plc_data['PLC'] == selected_plc]
#     if not plc_row.empty:
#         ip_address = plc_row['IP Address'].values[0]
#         port = plc_row['Port'].values[0]
#         return ip_address, port
#     else:
#         return None, None

# class HomeUI(tk.Frame):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.plc_data = readExcel(excel_file_path)  # Call readExcel function to get the data
#         self.create_widgets()

#     def create_widgets(self):
#         # Create label for the dropdown
#         self.plc_label = tk.Label(self, text="Select PLC:")
#         self.plc_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

#         # Create a dropdown menu (Combobox)
#         self.plc_var = tk.StringVar()  # Variable to hold the selected PLC
#         self.plc_combobox = ttk.Combobox(self, textvariable=self.plc_var, state="readonly")
#         self.plc_combobox['values'] = [f'PLC{i}' for i in range(1, 21)]  # PLC1 to PLC20
#         self.plc_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="w")

#         # Sampling Frequency label and entry
#         self.sampling_freq_label = tk.Label(self, text="Sampling Frequency (ms):")
#         self.sampling_freq_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

#         self.sampling_freq_entry = tk.Entry(self)
#         self.sampling_freq_entry.insert(0, "1000")  # Default value
#         self.sampling_freq_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

#         # Change in Data (%) label and entry
#         self.change_data_label = tk.Label(self, text="Change in Data (%):")
#         self.change_data_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

#         self.change_data_entry = tk.Entry(self)
#         self.change_data_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

#         # Start button
#         self.start_button = tk.Button(self, text="Start", command=self.start_process)
#         self.start_button.grid(row=3, column=1, padx=10, pady=10, sticky="w")

#     def start_process(self):
#         selected_plc = self.plc_var.get()  # Get the selected PLC
#         sampling_freq = self.sampling_freq_entry.get()  # Get sampling frequency
#         change_in_data = self.change_data_entry.get()  # Get change in data

#         # Fetch the IP and Port for the selected PLC
#         ip_address, port = get_plc_details(self.plc_data, selected_plc)

#         if ip_address and port:
#             print(f"Selected PLC: {selected_plc}, IP Address: {ip_address}, Port: {port}")
#         else:
#             # Show a popup message if no data is found
#             messagebox.showerror("Data Error", f"No data found for: {selected_plc}")
        
#         # Add your logic to handle the start process here
#         print(f"Sampling Frequency: {sampling_freq}, Change in Data: {change_in_data}")

# # if __name__ == "__main__":
# #     root = tk.Tk()
# #     home_ui = HomeUI(root)
# #     home_ui.pack(padx=20, pady=20)
# #     root.mainloop()
