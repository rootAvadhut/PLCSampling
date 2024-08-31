import tkinter as tk
import tkinter.font as tkFont
import modbus
import threading

def run_application():
    # Create the UI for user input
    root = tk.Tk()
    root.title("PLC Interface")

    root.geometry("500x250+300+200")

    custom_font = tkFont.Font(family="Helvetica", size=10)

    # Create and place labels and entry fields
    tk.Label(root, text="IP Address:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
    ip_entry = tk.Entry(root, width=30)
    ip_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')
    ip_entry.insert(0, "192.168.1.9")  # Default value

    tk.Label(root, text="Port No.:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
    port_entry = tk.Entry(root, width=10)  # Adjusted width for 6-digit input
    port_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')
    port_entry.insert(0, "502")  # Default value

    tk.Label(root, text="Sampling Frequency (ms):").grid(row=2, column=0, padx=10, pady=5, sticky='e')
    sampling_entry = tk.Entry(root, width=10)  # Adjusted width for 6-digit input
    sampling_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')
    sampling_entry.insert(0, "1000")  # Default value (1 second)

    # Adding the label "(100 ms to 1 min) (input in milli sec)" next to Sampling Frequency
    tk.Label(root, text="(100 ms to 1 min) (input in milli sec)").grid(row=2, column=2, padx=5, pady=5, sticky='w')

    tk.Label(root, text="Change in Data (%):").grid(row=3, column=0, padx=10, pady=5, sticky='e')
    change_entry = tk.Entry(root, width=10)  # Adjusted width for 6-digit input
    change_entry.grid(row=3, column=1, padx=10, pady=5, sticky='w')

    # Adding the label "(change in %)" next to Change in Data
    tk.Label(root, text="(change in %)").grid(row=3, column=2, padx=5, pady=5, sticky='w')

    # Function to start the Modbus client using the user-provided inputs
    def start_modbus_client():
        ip_address = ip_entry.get()
        port_number = int(port_entry.get())
        sampling_frequency = float(sampling_entry.get()) / 1000  # Convert ms to seconds 

        # Start the Modbus client in a separate thread
        threading.Thread(target=modbus.run_client, args=(ip_address, port_number, sampling_frequency), daemon=True).start()

    # Add a button to start the Modbus client
    start_button = tk.Button(root, text="Start", command=start_modbus_client)
    start_button.grid(row=4, column=1, padx=10, pady=10, sticky='w')

    # Run the UI
    root.mainloop()

# You can call run_application() from main.py to start the UI
