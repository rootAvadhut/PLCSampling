
import tkinter as tk
import tkinter.font as tkFont
import modbus
import threading

def create_plc_output_table(root):
    # Digital Inputs for Coils table
    title_label = tk.Label(root, text="Digital Inputs for Coils", font=('Helvetica', 12, 'bold'))
    title_label.grid(row=5, column=0, columnspan=3, pady=10, sticky='we')

    headers = ["PLC OUTPUT NO", "MODBUS ADDRESS", "States"]
    for col, header in enumerate(headers):
        label = tk.Label(root, text=header, font=('Helvetica', 10, 'bold'))
        label.grid(row=6, column=col, padx=5, pady=5, sticky='w')

    state_labels = []
    for i in range(16):
        output_label = tk.Label(root, text=f"OUT PUT {i}")
        output_label.grid(row=7+i, column=0, padx=10, pady=5, sticky='w')

        address_label = tk.Label(root, text=f"1000{i+1:02}")
        address_label.grid(row=7+i, column=1, padx=10, pady=5, sticky='w')

        state_label = tk.Label(root, text="FALSE")
        state_label.grid(row=7+i, column=2, padx=10, pady=5, sticky='w')
        state_labels.append(state_label)

    # Digital Inputs for Input Bit table
    title_label_2 = tk.Label(root, text="Digital Inputs for Input Bit", font=('Helvetica', 12, 'bold'))
    title_label_2.grid(row=5, column=4, columnspan=3, pady=10, sticky='we')

    headers_2 = ["Input Bit NO", "MODBUS ADDRESS", "States"]
    for col, header in enumerate(headers_2):
        label = tk.Label(root, text=header, font=('Helvetica', 10, 'bold'))
        label.grid(row=6, column=4+col, padx=5, pady=5, sticky='w')

    input_bit_labels = []
    for i in range(16):
        input_label = tk.Label(root, text=f"INPUT BIT {i}")
        input_label.grid(row=7+i, column=4, padx=10, pady=5, sticky='w')

        address_label = tk.Label(root, text=f"0000{i+1:02}")
        address_label.grid(row=7+i, column=5, padx=10, pady=5, sticky='w')

        state_label = tk.Label(root, text="FALSE")
        state_label.grid(row=7+i, column=6, padx=10, pady=5, sticky='w')
        input_bit_labels.append(state_label)

    # Add an empty column for spacing
    root.grid_columnconfigure(7, minsize=50)  # Adjust the minsize to increase/decrease the space

    # Analog Inputs for Input Register table
    title_label_3 = tk.Label(root, text="Analog Inputs for Input Register", font=('Helvetica', 12, 'bold'))
    title_label_3.grid(row=5, column=8, columnspan=3, pady=10, sticky='we')

    headers_3 = ["PLC ANALOG INPUT SLOT", "MODBUS ADDRESS", "Values"]
    for col, header in enumerate(headers_3):
        label = tk.Label(root, text=header, font=('Helvetica', 10, 'bold'))
        label.grid(row=6, column=8+col, padx=5, pady=5, sticky='w')

    analog_input_labels = []
    for i in range(8):
        analog_label = tk.Label(root, text=f"ANALOG INPUT {i}")
        analog_label.grid(row=7+i, column=8, padx=10, pady=5, sticky='w')

        address_label = tk.Label(root, text=f"3000{i+2:02}")
        address_label.grid(row=7+i, column=9, padx=10, pady=5, sticky='w')

        value_label = tk.Label(root, text="0")
        value_label.grid(row=7+i, column=10, padx=10, pady=5, sticky='w')
        analog_input_labels.append(value_label)

    return state_labels, input_bit_labels, analog_input_labels

def update_ui(coil_states, input_registers, input_statuses):
    for i, state in enumerate(coil_states or []):
        state_labels[i].config(text="TRUE" if state else "FALSE")
    
    for i, value in enumerate(input_registers or []):
        analog_input_labels[i].config(text=str(value))
    
    for i, status in enumerate(input_statuses or []):
        input_bit_labels[i].config(text="TRUE" if status else "FALSE")

def run_application():
    global state_labels, input_bit_labels, analog_input_labels
    root = tk.Tk()
    root.title("PLC Interface")

    root.geometry("1500x550+300+200")

    state_labels, input_bit_labels, analog_input_labels = create_plc_output_table(root)

    tk.Label(root, text="IP Address:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
    ip_entry = tk.Entry(root, width=30)
    ip_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')
    ip_entry.insert(0, "192.168.1.9")  # Default value

    tk.Label(root, text="Port No.:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
    port_entry = tk.Entry(root, width=10)
    port_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')
    port_entry.insert(0, "502")  # Default value

    tk.Label(root, text="Sampling Frequency (ms):").grid(row=2, column=0, padx=10, pady=5, sticky='e')
    sampling_entry = tk.Entry(root, width=10)
    sampling_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')
    sampling_entry.insert(0, "1000")  # Default value

    tk.Label(root, text="(100 ms to 1 min) (input in milli sec)").grid(row=2, column=2, padx=5, pady=5, sticky='w')

    tk.Label(root, text="Change in Data (%):").grid(row=3, column=0, padx=10, pady=5, sticky='e')
    change_entry = tk.Entry(root, width=10)
    change_entry.grid(row=3, column=1, padx=10, pady=5, sticky='w')

    tk.Label(root, text="(change in %)").grid(row=3, column=2, padx=5, pady=5, sticky='w')

    def start_modbus_client():
        ip_address = ip_entry.get()
        port_number = int(port_entry.get())
        sampling_frequency = float(sampling_entry.get()) / 1000  # Convert ms to seconds
        threading.Thread(
            target=modbus.run_client,
            args=(ip_address, port_number, sampling_frequency, update_ui),
            daemon=True
        ).start()

    start_button = tk.Button(root, text="Start", command=start_modbus_client)
    start_button.grid(row=4, column=1, padx=10, pady=10, sticky='w')

    root.mainloop()

# You can call run_application() from main.py to start the UI


