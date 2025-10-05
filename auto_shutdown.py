import os
import time
import threading
import hashlib
import configparser
import flet as ft

# Configuration file for settings
CONFIG_FILE = "shutdown_config.ini"

def main(page: ft.Page):
    page.title = "Auto Shutdown Timer"
    page.window_resizable = False
    page.window.center()
    page.theme_mode = "light"
    page.padding = 30
    page.window.height = 650
    page.window.width = 500
    
    # Global variables
    remaining_time = 0
    timer_running = False
    timer_thread = None
    
    def get_password_hash():
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
    
    def get_default_time():
        """Get default countdown time from config"""
        config = configparser.ConfigParser()
        if os.path.exists(CONFIG_FILE):
            config.read(CONFIG_FILE)
            if 'Settings' in config and 'DefaultTime' in config['Settings']:
                return int(config['Settings']['DefaultTime'])
        return 90  # Default fallback
    
    password_hash = get_password_hash()
    
    # Create UI elements
    title = ft.Text(
        "Auto Shutdown Timer",
        size=30,
        font_family="Arial",
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.RED_800,
        text_align=ft.TextAlign.CENTER
    )
    
    # Time display
    time_display = ft.Text(
        "Timer not started",
        size=32,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.RED_600,
        text_align=ft.TextAlign.CENTER
    )
    
    # Time slider
    time_slider_label = ft.Text(
        "Set Shutdown Timer (minutes):",
        size=16,
        color=ft.Colors.GREY_700,
        text_align=ft.TextAlign.CENTER
    )
    
    time_slider = ft.Slider(
        min=1,
        max=120,
        value=get_default_time() // 60,
        divisions=119,
        label="{value} min",
        width=350,
        active_color=ft.Colors.RED_600,
        inactive_color=ft.Colors.GREY_300
    )
    
    # Slider value display
    slider_value_text = ft.Text(
        f"{int(time_slider.value)} minutes",
        size=14,
        color=ft.Colors.GREY_600,
        text_align=ft.TextAlign.CENTER
    )
    
    # Start button
    start_button = ft.ElevatedButton(
        text="Start Timer",
        width=120,
        height=50,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.GREEN_600,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        disabled=False
    )
    
    # Stop button
    stop_button = ft.ElevatedButton(
        text="Stop Timer",
        width=120,
        height=50,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.RED_600,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        disabled=True
    )
    
    # Status text
    status_text = ft.Text(
        "Set timer and click Start to begin countdown",
        size=14,
        color=ft.Colors.GREY_600,
        text_align=ft.TextAlign.CENTER
    )
    
    # Warning text
    warning_text = ft.Text(
        "⚠️ System will shutdown when timer reaches 00:00",
        size=12,
        color=ft.Colors.ORANGE_600,
        text_align=ft.TextAlign.CENTER,
        visible=False
    )
    
    # Password info
    password_info = ft.Text(
        "Default password: 'pass' (stored in shutdown_config.ini)",
        size=10,
        color=ft.Colors.GREY_500,
        text_align=ft.TextAlign.CENTER
    )
    
    # Dialog functions
    
    def show_password_dialog(title_text, callback):
        print(f"Creating password dialog: {title_text}")  # Debug
        
        password_field = ft.TextField(
            label="Password",
            password=True,
            can_reveal_password=True,
            width=250,
            autofocus=True,
            on_submit=lambda e: on_submit()  # Allow Enter key
        )
        
        def on_submit():
            password = password_field.value
            print(f"Password submitted: {password}")  # Debug
            dialog.open = False
            page.update()
            callback(password)
        
        def on_cancel():
            print("Password dialog cancelled")  # Debug
            dialog.open = False
            page.update()
            callback(None)
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(title_text, color=ft.Colors.BLUE_600, size=18),
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Enter password to stop the timer:", size=14),
                    ft.Container(height=10),
                    password_field,
                    ft.Container(height=5),
                    ft.Text("Default password: 'pass'", size=12, color=ft.Colors.GREY_600)
                ], tight=True),
                width=300,
                height=120
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: on_cancel()),
                ft.TextButton("OK", on_click=lambda e: on_submit())
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        try:
            # Use page.overlay instead of page.dialog
            page.overlay.clear()  # Clear any existing overlays
            page.overlay.append(dialog)
            dialog.open = True
            page.update()
            print("Password dialog created and should be visible")  # Debug
            
        except Exception as ex:
            print(f"Error showing dialog: {ex}")  # Debug
    
    def show_shutdown_confirmation(callback):
        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirm Shutdown", color=ft.Colors.RED_600),
            content=ft.Column([
                ft.Text("⚠️ The system will shut down now!", size=16, weight=ft.FontWeight.BOLD),
                ft.Text("This action cannot be undone."),
                ft.Text("Do you want to continue?")
            ], tight=True),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: [setattr(confirm_dialog, 'open', False), page.update(), callback(False)]),
                ft.TextButton("Shutdown Now", on_click=lambda e: [setattr(confirm_dialog, 'open', False), page.update(), callback(True)])
            ],
        )
        page.overlay.append(confirm_dialog)
        confirm_dialog.open = True
        page.update()
    
    def show_error_dialog(title, message):
        error_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(title, color=ft.Colors.RED_600),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=lambda e: [setattr(error_dialog, 'open', False), page.update()])
            ],
        )
        page.overlay.append(error_dialog)
        error_dialog.open = True
        page.update()
    
    def show_success_dialog(message):
        success_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Timer Stopped", color=ft.Colors.GREEN_600),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=lambda e: [setattr(success_dialog, 'open', False), page.update()])
            ],
        )
        page.overlay.append(success_dialog)
        success_dialog.open = True
        page.update()
    
    def verify_password(input_password):
        """Verify the password against stored hash"""
        if not input_password:
            return False
        input_hash = hashlib.sha256(input_password.encode()).hexdigest()
        return input_hash == password_hash
    
    def update_slider_display(e):
        slider_value_text.value = f"{int(time_slider.value)} minutes"
        page.update()
    
    def update_time_display():
        """Update the countdown timer display"""
        nonlocal remaining_time, timer_running
        
        while timer_running and remaining_time > 0:
            # Format the time as minutes:seconds
            minutes = remaining_time // 60
            seconds = remaining_time % 60
            
            def update_ui():
                time_display.value = f"{minutes:02d}:{seconds:02d}"
                
                # Update color based on remaining time
                if remaining_time <= 30:
                    time_display.color = ft.Colors.RED_600
                elif remaining_time <= 60:
                    time_display.color = ft.Colors.ORANGE_600
                else:
                    time_display.color = ft.Colors.GREEN_600
                
                page.update()
            
            page.run_thread(update_ui)
            
            # Decrease time and wait
            remaining_time -= 1
            time.sleep(1)
            
        if timer_running and remaining_time <= 0:
            # Time's up - ask for shutdown confirmation
            def on_shutdown_confirm(confirm):
                nonlocal timer_running
                if confirm:
                    def update_ui_shutdown():
                        time_display.value = "Shutting down..."
                        time_display.color = ft.Colors.RED_800
                        status_text.value = "System shutdown initiated..."
                        page.update()
                    page.run_thread(update_ui_shutdown)
                    
                    # Execute shutdown command
                    try:
                        os.system("shutdown /s /t 60")  # 60 second delay
                    except Exception as e:
                        def show_error():
                            show_error_dialog("Shutdown Error", f"Failed to initiate shutdown:\n{str(e)}")
                        page.run_thread(show_error)
                else:
                    timer_running = False
                    def update_ui_cancel():
                        time_display.value = "Shutdown cancelled"
                        time_display.color = ft.Colors.BLUE_600
                        status_text.value = "Shutdown was cancelled by user"
                        warning_text.visible = False
                        start_button.disabled = False
                        stop_button.disabled = True
                        page.update()
                    page.run_thread(update_ui_cancel)
            
            def show_confirm():
                show_shutdown_confirmation(on_shutdown_confirm)
            page.run_thread(show_confirm)
    
    def start_timer(e):
        print("Start timer button clicked!")  # Debug
        nonlocal remaining_time, timer_running, timer_thread
        
        # Get minutes from slider and convert to seconds
        minutes = int(time_slider.value)
        remaining_time = minutes * 60
        
        # Update UI
        start_button.disabled = True
        stop_button.disabled = False
        warning_text.visible = True
        status_text.value = f"Timer started for {minutes} minute(s)"
        status_text.color = ft.Colors.GREEN_600
        
        # Format initial display
        min_display = remaining_time // 60
        sec_display = remaining_time % 60
        time_display.value = f"{min_display:02d}:{sec_display:02d}"
        time_display.color = ft.Colors.GREEN_600
        
        page.update()
        
        # Start timer
        timer_running = True
        timer_thread = threading.Thread(target=update_time_display, daemon=True)
        timer_thread.start()
        print(f"Timer thread started for {minutes} minutes")  # Debug
    
    def stop_timer(e):
        print("Stop timer button clicked!")  # Debug
        print("Calling show_password_dialog...")  # Debug
        
        def on_password_entered(password):
            print(f"Password callback called with: {password}")  # Debug
            nonlocal timer_running
            
            if password and verify_password(password):
                print("Password verified, stopping timer")  # Debug
                timer_running = False
                
                # Cancel any scheduled shutdown
                try:
                    os.system("shutdown /a")
                    print("Shutdown cancelled")  # Debug
                except Exception as ex:
                    print(f"Error cancelling shutdown: {ex}")  # Debug
                
                # Update UI
                time_display.value = "Timer stopped"
                time_display.color = ft.Colors.BLUE_600
                status_text.value = "Timer stopped by user"
                status_text.color = ft.Colors.BLUE_600
                warning_text.visible = False
                start_button.disabled = False
                stop_button.disabled = True
                page.update()
                
                show_success_dialog("Timer has been stopped and shutdown cancelled.")
                
            elif password is not None:  # Password was entered but incorrect
                print("Incorrect password entered")  # Debug
                show_error_dialog("Incorrect Password", "The password is incorrect.")
            else:
                print("No password entered (cancelled)")  # Debug
        
        # Always show dialog regardless of timer state for testing
        print("About to call show_password_dialog...")  # Debug
        show_password_dialog("Stop Timer", on_password_entered)
    
    # Assign events - ensure they are properly connected
    time_slider.on_change = update_slider_display
    start_button.on_click = start_timer
    stop_button.on_click = stop_timer
    
    # Initialize the display
    update_slider_display(None)  # Update slider display initially
    
    # Layout
    page.add(
        ft.Container(
            content=ft.Container(
                content=ft.Column([
                    # Header
                    ft.Container(
                        content=title,
                        alignment=ft.alignment.center,
                        margin=ft.margin.only(bottom=25)
                    ),
                    
                    # Time display
                    ft.Container(
                        content=time_display,
                        alignment=ft.alignment.center,
                        padding=10,
                        bgcolor=ft.Colors.GREY_50,
                        border_radius=15,
                        border=ft.border.all(2, ft.Colors.GREY_300),
                        margin=ft.margin.only(bottom=20)
                    ),
                    
                    # Time slider section
                    ft.Container(
                        content=ft.Column([
                            time_slider_label,
                            ft.Container(height=1),
                            time_slider,
                            ft.Container(height=1),
                            slider_value_text,
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        margin=ft.margin.only(bottom=25)
                    ),
                    
                    # Buttons
                    ft.Container(
                        content=ft.Row([
                            start_button,
                            ft.Container(width=20),
                            stop_button,
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        margin=ft.margin.only(bottom=20)
                    ),
                    
                    # Warning
                    ft.Container(
                        content=warning_text
                    ),
                    
                    # Status and info
                    ft.Container(
                        content=ft.Column([
                            status_text,
                            ft.Container(height=1),
                            password_info,
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    )
                    
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=30,
                bgcolor=ft.Colors.WHITE,
                border_radius=15,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.Colors.with_opacity(0.3, ft.Colors.GREY_400),
                    offset=ft.Offset(0, 0),
                )
            ),
            alignment=ft.alignment.center,
            expand=True,
        )
    )

if __name__ == "__main__":
    ft.app(main)