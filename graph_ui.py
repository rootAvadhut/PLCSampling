import tkinter as tk

class GraphUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="You are in the Graph tab welcome", font=("Helvetica", 20))
        label.pack(pady=50)
# the excel file contain Date	Time	IP Address	Port Number	Register 300002	Register 300003	Register 300004	Register 300005	Register 300006	Register 300007	Register 300008	Register 300009
# i want that program will read Date and time and Register 300002 values
# Date and Time plot on x axis and use excel file to get Date and time
# for y axis read register 30002 column for values get that values and plot the values and the range of values should be 0-10 on y axis