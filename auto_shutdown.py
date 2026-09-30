import os
import time
import threading
import configparser
import flet as ft

# Configuration file for settings
CONFIG_FILE = "shutdown_config.ini"

async def main(page: ft.Page):
    page.title = "Auto Shutdown Timer"
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 30
    page.window.height = 650
    page.window.width = 500
    await page.window.center()
    
    # Global variables
    remaining_time = 0
    timer_running = False
    timer_thread = None
    
    def get_default_time():
        """Get default countdown time from config"""
        config = configparser.ConfigParser()
        if os.path.exists(CONFIG_FILE):
            config.read(CONFIG_FILE)
            if 'Settings' in config and 'DefaultTime' in config['Settings']:
                return int(config['Settings']['DefaultTime'])
        return 90  # Default fallback
    
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

    def get_selected_minutes() -> int:
        value = time_slider.value
        return int(value) if value is not None else 1
    
    # Slider value display
    slider_value_text = ft.Text(
        f"{get_selected_minutes()} minutes",
        size=14,
        color=ft.Colors.GREY_600,
        text_align=ft.TextAlign.CENTER
    )

    def update_slider_display(e):
        slider_value_text.value = f"{get_selected_minutes()} minutes"
        page.update()
    
    # Start button
    start_button = ft.Button(
        content="Start Timer",
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
    stop_button = ft.Button(
        content="Stop Timer",
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
        "âš ï¸ System will shutdown when timer reaches 00:00",
        size=12,
        color=ft.Colors.ORANGE_600,
        text_align=ft.TextAlign.CENTER,
        visible=False
    )
    
    # Dialog functions
    
    def show_shutdown_confirmation(callback):
        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirm Shutdown", color=ft.Colors.RED_600),
            content=ft.Column([
                ft.Text("âš ï¸ The system will shut down now!", size=16, weight=ft.FontWeight.BOLD),
                ft.Text("This action cannot be undone."),
                ft.Text("Do you want to continue?")
            ], tight=True),
            actions=[
                ft.TextButton(content="Cancel", on_click=lambda e: [page.pop_dialog(), callback(False)]),
                ft.TextButton(content="Shutdown Now", on_click=lambda e: [page.pop_dialog(), callback(True)])
            ],
        )
        page.show_dialog(confirm_dialog)
    
    def show_error_dialog(title, message):
        error_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(title, color=ft.Colors.RED_600),
            content=ft.Text(message),
            actions=[
                ft.TextButton(content="OK", on_click=lambda e: [page.pop_dialog()])
            ],
        )
        page.show_dialog(error_dialog)
    
    def show_success_dialog(message):
        success_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Timer Stopped", color=ft.Colors.GREEN_600),
            content=ft.Text(message),
            actions=[
                ft.TextButton(content="OK", on_click=lambda e: [page.pop_dialog()])
            ],
        )
        page.show_dialog(success_dialog)
    
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
        minutes = get_selected_minutes()
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
        nonlocal timer_running
        timer_running = False

        # Cancel any scheduled shutdown.
        try:
            os.system("shutdown /a")
        except OSError as ex:
            print(f"Error cancelling shutdown: {ex}")

        time_display.value = "Timer stopped"
        time_display.color = ft.Colors.BLUE_600
        status_text.value = "Timer stopped by user"
        status_text.color = ft.Colors.BLUE_600
        warning_text.visible = False
        start_button.disabled = False
        stop_button.disabled = True
        page.update()

        show_success_dialog("Timer has been stopped and shutdown cancelled.")
    
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
                        alignment=ft.Alignment(0, 0),
                        margin=ft.Margin(bottom=25)
                    ),
                    
                    # Time display
                    ft.Container(
                        content=time_display,
                        alignment=ft.Alignment(0, 0),
                        padding=10,
                        bgcolor=ft.Colors.GREY_50,
                        border_radius=15,
                        border=ft.Border.all(2, ft.Colors.GREY_300),
                        margin=ft.Margin(bottom=20)
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
                        margin=ft.Margin(bottom=25)
                    ),
                    
                    # Buttons
                    ft.Container(
                        content=ft.Row([
                            start_button,
                            ft.Container(width=20),
                            stop_button,
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        margin=ft.Margin(bottom=20)
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
            alignment=ft.Alignment(0, 0),
            expand=True,
        )
    )

if __name__ == "__main__":
    ft.run(main)
