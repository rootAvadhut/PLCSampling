import tkinter as tk
from file_operations import browse_file
from data_sampling import sample_data

def run_application():
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
    file_button = tk.Button(root, text="Browse", command=lambda: browse_file(file_entry))
    file_button.grid(row=4, column=2, padx=10, pady=10)

    # Start sampling process
    tk.Button(root, text="Start Sampling", command=lambda: sample_data(sampling_entry, change_entry, file_entry)).grid(row=5, column=1, padx=10, pady=20)

    # Run the application
    root.mainloop()
