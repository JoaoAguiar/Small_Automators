import threading
import flet as ft
import speedtest as st

async def main(page: ft.Page):
    page.title = "Internet Speed Test"
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 30
    page.window.height = 600
    page.window.width = 500
    await page.window.center()
    
    # Create UI elements
    title = ft.Text(
        "Internet Speed Test",
        size=30,
        font_family="Arial",
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.PURPLE_800,
        text_align=ft.TextAlign.CENTER
    )
    
    # Test button
    test_button = ft.Button(
        content="Start Speed Test",
        width=150,
        height=50,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.PURPLE_600,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        disabled=False
    )
    
    # Progress ring
    progress_ring = ft.ProgressRing(
        visible=False,
        color=ft.Colors.PURPLE_600,
        width=25,
        height=25
    )
    
    # Status text
    status_text = ft.Text(
        "Ready to test your internet speed",
        size=14,
        color=ft.Colors.PURPLE_600,
        text_align=ft.TextAlign.CENTER
    )
    
    # Results display
    server_info = ft.Text(
        "Server: Not tested",
        size=13,
        color=ft.Colors.GREY_700,
        text_align=ft.TextAlign.CENTER
    )
    
    isp_info = ft.Text(
        "ISP: Not tested",
        size=13,
        color=ft.Colors.GREY_700,
        text_align=ft.TextAlign.CENTER
    )
    
    download_speed = ft.Text(
        "Download: - Mbps",
        size=16,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.PURPLE_600,
        text_align=ft.TextAlign.CENTER
    )
    
    upload_speed = ft.Text(
        "Upload: - Mbps",
        size=16,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.PURPLE_600,
        text_align=ft.TextAlign.CENTER
    )
    
    ping_speed = ft.Text(
        "Ping: - ms",
        size=16,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.PURPLE_600,
        text_align=ft.TextAlign.CENTER
    )
    
    # Dialog functions
    def close_dialog(dialog):
        if dialog.open:
            page.pop_dialog()
    
    def show_results_dialog(server_name, isp_name, down, up, ping):
        results_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Speed Test Results", color=ft.Colors.PURPLE_600),
            content=ft.Column([
                ft.Text(f"🌐 Server: {server_name}", weight=ft.FontWeight.BOLD),
                ft.Text(f"🏢 ISP: {isp_name}"),
                ft.Divider(),
                ft.Text(f"⬇️ Download: {down:.2f} Mbps", color=ft.Colors.GREEN_600, size=16),
                ft.Text(f"⬆️ Upload: {up:.2f} Mbps", color=ft.Colors.BLUE_600, size=16),
                ft.Text(f"📡 Ping: {ping:.2f} ms", color=ft.Colors.ORANGE_600, size=16),
                ft.Divider(),
                ft.Text("Test completed successfully!", color=ft.Colors.GREEN_600, italic=True)
            ], tight=True),
            actions=[
                ft.TextButton(content="OK", on_click=lambda e: close_dialog(results_dialog))
            ],
        )
        page.show_dialog(results_dialog)
    
    def show_error_dialog(title, message):
        error_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(title, color=ft.Colors.RED_600),
            content=ft.Text(message),
            actions=[
                ft.TextButton(content="OK", on_click=lambda e: close_dialog(error_dialog))
            ],
        )
        page.show_dialog(error_dialog)
    
    # Speed test function
    def run_speed_test(e):
        # Update UI for testing
        test_button.disabled = True
        progress_ring.visible = True
        status_text.value = "Initializing speed test..."
        status_text.color = ft.Colors.PURPLE_600
        
        # Reset results
        server_info.value = "Server: Testing..."
        isp_info.value = "ISP: Testing..."
        download_speed.value = "Download: Testing..."
        upload_speed.value = "Upload: Testing..."
        ping_speed.value = "Ping: Testing..."
        
        page.update()
        
        def test_thread():
            try:
                # Initialize speedtest
                def update_status(message):
                    def update_ui():
                        status_text.value = message
                        page.update()
                    page.run_thread(update_ui)
                
                update_status("Finding best server...")
                
                # Set Best Server
                server = st.Speedtest()
                server.get_best_server()
                
                # Get server and ISP info
                location = server.results.server['name']
                isp = server.results.client['isp']
                
                def update_server_info():
                    server_info.value = f"Server: {location}"
                    isp_info.value = f"ISP: {isp}"
                    page.update()
                page.run_thread(update_server_info)
                
                update_status("Testing download speed...")
                
                # Test Download Speed
                down = server.download()
                down = down / 1000000  # Convert to Mbps
                
                def update_download():
                    download_speed.value = f"Download: {down:.2f} Mbps"
                    page.update()
                page.run_thread(update_download)
                
                update_status("Testing upload speed...")
                
                # Test Upload Speed
                up = server.upload()
                up = up / 1000000  # Convert to Mbps
                
                def update_upload():
                    upload_speed.value = f"Upload: {up:.2f} Mbps"
                    page.update()
                page.run_thread(update_upload)
                
                update_status("Getting ping...")
                
                # Test Ping
                ping = server.results.ping
                
                def update_ping():
                    ping_speed.value = f"Ping: {ping:.2f} ms"
                    page.update()
                page.run_thread(update_ping)
                
                # Update UI with success
                def update_ui_success():
                    progress_ring.visible = False
                    test_button.disabled = False
                    status_text.value = "Speed test completed!"
                    status_text.color = ft.Colors.GREEN_600
                    page.update()
                    show_results_dialog(location, isp, down, up, ping)
                
                page.run_thread(update_ui_success)
                
            except Exception as ex:
                error_msg = str(ex)
                def update_ui_error():
                    progress_ring.visible = False
                    test_button.disabled = False
                    status_text.value = "Speed test failed"
                    status_text.color = ft.Colors.RED_600
                    
                    # Reset results
                    server_info.value = "Server: Test failed"
                    isp_info.value = "ISP: Test failed"
                    download_speed.value = "Download: - Mbps"
                    upload_speed.value = "Upload: - Mbps"
                    ping_speed.value = "Ping: - ms"
                    
                    page.update()
                    show_error_dialog("Speed Test Error", f"Test failed:\n\n{error_msg}")
                
                page.run_thread(update_ui_error)
        
        threading.Thread(target=test_thread, daemon=True).start()
    
    # Assign button event
    test_button.on_click = run_speed_test
    
    # Layout
    page.add(
        ft.Container(
            content=ft.Container(
                content=ft.Column([
                    # Header
                    ft.Container(
                        content=title,
                        alignment=ft.Alignment(0, 0),
                        margin=ft.Margin(bottom=30)
                    ),
                    
                    # Test button and progress
                    ft.Container(
                        content=ft.Column([
                            test_button,
                            ft.Container(height=10),
                            progress_ring,
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ),
                    
                    # Status
                    ft.Container(
                        content=status_text,
                        margin=ft.Margin(bottom=20)
                    ),
                    
                    # Results section
                    ft.Container(
                        content=ft.Column([
                            # Server and ISP info
                            ft.Container(
                                content=ft.Column([
                                    server_info,
                                    isp_info,
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                margin=ft.Margin(bottom=10)
                            ),
                            
                            # Speed results
                            ft.Container(
                                content=ft.Column([
                                    download_speed,
                                    ft.Container(height=1),
                                    upload_speed,
                                    ft.Container(height=1),
                                    ping_speed,
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                padding=15,
                                bgcolor=ft.Colors.GREY_50,
                                border_radius=10,
                                border=ft.Border.all(1, ft.Colors.GREY_300)
                            )
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