import tkinter as tk
from setting_ui import SettingUI
from home_ui import HomeUI  # Import HomeUI


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Tab Navigation")
        
        # Set window size
        self.geometry("800x600")

        # Default colors
        self.default_bg = "lightgray"
        self.active_bg = "lightblue"

        # Track the current tab
        self.current_tab = None

        # Create the main frame
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Create the left side button frame
        self.button_frame = tk.Frame(self.main_frame, width=150)
        self.button_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Create the content frame
        self.content_frame = tk.Frame(self.main_frame)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Add buttons to the button frame with reduced size and spacing
        self.home_button = tk.Button(self.button_frame, text="Home", command=self.show_home_tab, width=12, height=1)
        self.home_button.pack(fill="x", pady=5)

        self.setting_button = tk.Button(self.button_frame, text="Setting", command=self.show_setting_tab, width=12, height=1)
        self.setting_button.pack(fill="x", pady=5)

        # Initialize with the home tab selected
        self.show_home_tab()

    def show_home_tab(self):
        self.current_tab = "Home"  # Track the current tab
        self.clear_content_frame()

        # Update button colors
        self.update_button_colors(self.home_button)

        # Load the HomeUI into the content frame
        home_ui = HomeUI(self.content_frame)
        home_ui.pack(fill="both", expand=True)

    def show_setting_tab(self):
        self.current_tab = "Setting"  # Track the current tab
        self.clear_content_frame()

        # Update button colors
        self.update_button_colors(self.setting_button)

        # Load the SettingUI into the content frame
        setting_ui = SettingUI(self.content_frame)
        setting_ui.pack(fill="both", expand=True)



    def clear_content_frame(self):
        # Clear the content frame before showing a new tab
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def update_button_colors(self, active_button):
        # Reset all button colors to default
        self.home_button.config(bg=self.default_bg)
        self.setting_button.config(bg=self.default_bg)
      
        
        # Set the active button color
        active_button.config(bg=self.active_bg)

if __name__ == "__main__":
    app = App()
    app.mainloop()
