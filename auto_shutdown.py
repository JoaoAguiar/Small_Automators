import tkinter as tk
import time
import threading
import os
import sys
from tkinter import simpledialog, messagebox, Scale
import winsound  # Import the winsound module for sound on Windows
import configparser
import hashlib

# Configuration file for settings
CONFIG_FILE = "shutdown_config.ini"

class ShutdownTimer:
    def __init__(self, root):
        self.root = root
        self.remaining_time = 0
        self.timer_running = False
        self.password_hash = self.get_password_hash()
        
        # Set up the UI
        self.setup_ui()
    
    def get_password_hash(self):
        """Get password hash from config or create new config with default"""
        config = configparser.ConfigParser()
        
        if os.path.exists(CONFIG_FILE):
            config.read(CONFIG_FILE)
            if 'Security' in config and 'PasswordHash' in config['Security']:
                return config['Security']['PasswordHash']
        
        # Create default config if no file exists
        config['Security'] = {'PasswordHash': hashlib.sha256("pass".encode()).hexdigest()}
        config['Settings'] = {'DefaultTime': '90'}
        
        with open(CONFIG_FILE, 'w') as f:
            config.write(f)
        
        return config['Security']['PasswordHash']
    
    def get_default_time(self):
        """Get default countdown time from config"""
        config = configparser.ConfigParser()
        if os.path.exists(CONFIG_FILE):
            config.read(CONFIG_FILE)
            if 'Settings' in config and 'DefaultTime' in config['Settings']:
                return int(config['Settings']['DefaultTime'])
        return 90  # Default fallback
    
    def setup_ui(self):
        """Set up the user interface"""
        # Set the window title
        self.root.title("Shutdown Timer")
        
        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Set the window size
        window_width = 400
        window_height = 350
        
        # Calculate the position of the window
        position_top = int(screen_height / 2 - window_height / 2)
        position_left = int(screen_width / 2 - window_width / 2)
        
        # Set the geometry of the window
        self.root.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")
        
        # Create a label for the timer slider
        tk.Label(self.root, text="Set Shutdown Timer (minutes):", font=("Arial", 12)).pack(pady=(20, 5))
        
        # Create time selector slider
        self.time_slider = Scale(self.root, from_=1, to=120, orient=tk.HORIZONTAL, length=300)
        self.time_slider.set(self.get_default_time() // 60)  # Set default in minutes
        self.time_slider.pack(pady=10)
        
        # Create a label to display the time
        self.time_label = tk.Label(self.root, font=("Arial", 20), padx=20, pady=20)
        self.time_label.pack(pady=10)
        
        # Create a frame to hold the buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        # Create buttons
        self.start_button = tk.Button(button_frame, text="Start Timer", command=self.start_timer, 
                                      font=("Arial", 14))
        self.start_button.grid(row=0, column=0, padx=10)
        
        self.stop_button = tk.Button(button_frame, text="Stop Timer", command=self.stop_timer, 
                                    font=("Arial", 14), state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=10)
        
        # Set the initial time display
        self.time_label.config(text="Timer not started")
    
    def update_time(self):
        """Update the countdown timer"""
        if self.timer_running and self.remaining_time > 0:
            # Decrease the remaining time by 1 second
            self.remaining_time -= 1
            
            # Format the time as minutes:seconds
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            self.time_label.config(text=f"{minutes:02d}:{seconds:02d}")
            
            # Play a sound every second
            winsound.Beep(1000, 100)  # Beep with 1000 Hz for 100 ms
            
            # After 1 second, call the update_time function again
            self.root.after(1000, self.update_time)
        elif self.timer_running and self.remaining_time <= 0:
            # Ask for confirmation before shutdown
            if messagebox.askyesno("Confirm Shutdown", "The system will shut down now. Continue?"):
                self.time_label.config(text="Shutting down...")
                os.system("shutdown /s /t 10")  # 10 second delay
            else:
                self.time_label.config(text="Shutdown cancelled")
                self.timer_running = False
                self.start_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.DISABLED)
    
    def verify_password(self, input_password):
        """Verify the password against stored hash"""
        input_hash = hashlib.sha256(input_password.encode()).hexdigest()
        return input_hash == self.password_hash
    
    def start_timer(self):
        """Start countdown timer"""
        # Get minutes from the slider and convert to seconds
        minutes = self.time_slider.get()
        self.remaining_time = minutes * 60
        
        # Format the time as minutes:seconds
        min_display = self.remaining_time // 60
        sec_display = self.remaining_time % 60
        self.time_label.config(text=f"{min_display:02d}:{sec_display:02d}")
        
        # Update button states
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # Set timer running flag and start countdown
        self.timer_running = True
        self.update_time()
    
    def stop_timer(self):
        """Stop countdown and cancel shutdown"""
        password = simpledialog.askstring("Password", "Enter the password:", show='*')
        if password and self.verify_password(password):
            self.timer_running = False
            self.time_label.config(text="Timer stopped")
            
            # Cancel any scheduled shutdown
            os.system("shutdown /a")
            
            # Reset button states
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
        else:
            messagebox.showerror("Incorrect Password", "The password is incorrect.")

# Create the main window
root = tk.Tk()

# Initialize the shutdown timer
shutdown_app = ShutdownTimer(root)

# Start the GUI application
root.mainloop()