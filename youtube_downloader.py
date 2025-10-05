import os
import re
import threading
import subprocess
import tempfile
import flet as ft
from pytubefix import YouTube

def check_ffmpeg():
    """Check if ffmpeg is installed"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except:
        return False

def is_valid_youtube_url(url):
    """Basic YouTube URL validation"""
    youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?\s]{11})'
    
    return re.match(youtube_regex, url) is not None

def create_default_directory():
    """Create default download directory if it doesn't exist"""
    default_dir = r"C:\Users\jpagu\Downloads\Youtube Videos"
    
    if not os.path.exists(default_dir):
        try:
            os.makedirs(default_dir)
        except Exception as e:
            return os.path.expanduser("~/Downloads")
    
    return default_dir

def main(page: ft.Page):
    page.title = "YouTube Downloader"
    page.window_resizable = False
    page.window.center()
    page.theme_mode = "light"
    page.padding = 30
    page.window.height = 550
    page.window.width = 550
    
    # Create UI elements
    title = ft.Text(
        "YouTube Downloader",
        size=30,
        font_family="Arial",
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.RED_800,
        text_align=ft.TextAlign.CENTER
    )
    
    # FFmpeg status indicator
    ffmpeg_available = check_ffmpeg()
    ffmpeg_status = ft.Text(
        f"{'✓ FFmpeg Available' if ffmpeg_available else '⚠ FFmpeg Not Found'}",
        size=12,
        color=ft.Colors.GREEN_600 if ffmpeg_available else ft.Colors.ORANGE_600,
        text_align=ft.TextAlign.CENTER
    )
    
    # URL input field
    url_field = ft.TextField(
        label="YouTube URL",
        hint_text="e.g., https://www.youtube.com/watch?v=...",
        width=320,
        border_radius=10,
        border_color=ft.Colors.RED_600,
        focused_border_color=ft.Colors.RED_600,
    )
    
    # Download button
    download_button = ft.ElevatedButton(
        text="Download Video",
        width=140,
        height=50,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.RED_600,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        disabled=False
    )
    
    # Change location button
    location_button = ft.ElevatedButton(
        text="Change Location",
        width=140,
        height=50,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.GREY_600,
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )
    
    # Progress ring
    progress_ring = ft.ProgressRing(
        visible=False,
        color=ft.Colors.RED_600,
        width=25,
        height=25
    )
    
    # Status text
    status_text = ft.Text(
        "Ready to download",
        size=14,
        color=ft.Colors.RED_600,
        text_align=ft.TextAlign.CENTER
    )
    
    # Output info
    output_info = ft.Text(
        f"Downloads to: C:\\Users\\jpagu\\Downloads\\Youtube Videos",
        size=12,
        color=ft.Colors.GREY_500,
        text_align=ft.TextAlign.CENTER
    )
    
    # Dialog functions
    def close_dialog(dialog):
        dialog.open = False
        page.update()
    
    def show_success_dialog(message, output_path=""):
        success_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Download Completed!", color=ft.Colors.GREEN_600),
            content=ft.Column([
                ft.Text(message),
                ft.Divider(),
                ft.Text("Video saved to:", weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Text(output_path, size=12),
                    bgcolor=ft.Colors.GREY_100,
                    padding=10,
                    border_radius=5
                )
            ], tight=True),
            actions=[
                ft.TextButton("OK", on_click=lambda e: close_dialog(success_dialog))
            ],
        )
        page.dialog = success_dialog
        success_dialog.open = True
        page.update()
    
    def show_error_dialog(title, message):
        error_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(title, color=ft.Colors.RED_600),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=lambda e: close_dialog(error_dialog))
            ],
        )
        page.dialog = error_dialog
        error_dialog.open = True
        page.update()
    
    # Progress hook for download
    def progress_hook(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        
        def update_progress():
            status_text.value = f"Downloading: {percentage:.1f}%"
            page.update()
        
        page.run_thread(update_progress)
    
    # Change download location function
    def change_download_location(e):
        def folder_picker_result(e: ft.FilePickerResultEvent):
            if e.path:
                global DEFAULT_DOWNLOAD_DIR
                DEFAULT_DOWNLOAD_DIR = e.path
                output_info.value = f"Downloads to: {e.path}"
                page.update()
                show_success_dialog(f"Download directory changed to:\n{e.path}")
        
        folder_picker = ft.FilePicker(on_result=folder_picker_result)
        page.overlay.append(folder_picker)
        page.update()
        folder_picker.get_directory_path(dialog_title="Select Download Directory")
    
    # Download video function
    def download_video(e):
        url = url_field.value.strip()
        
        if not is_valid_youtube_url(url):
            show_error_dialog("Error", "Please enter a valid YouTube URL")
            return
        
        # Update UI for download
        download_button.disabled = True
        progress_ring.visible = True
        status_text.value = "Downloading... Please wait"
        status_text.color = ft.Colors.RED_600
        page.update()
        
        def download_thread():
            try:
                download_dir = create_default_directory()
                
                # Create YouTube object
                yt = YouTube(url, on_progress_callback=progress_hook)
                
                ffmpeg_available = check_ffmpeg()
                
                if ffmpeg_available:
                    # Try to get highest adaptive video stream
                    video_stream = (yt.streams.filter(res="1080p", adaptive=True, file_extension='mp4').first() or
                                   yt.streams.filter(res="720p", adaptive=True, file_extension='mp4').first() or
                                   yt.streams.filter(res="480p", adaptive=True, file_extension='mp4').first())
                    audio_stream = yt.streams.filter(only_audio=True, abr="128kbps").first()
                    
                    if video_stream and audio_stream:
                        def update_status_merge():
                            status_text.value = "Downloading video and audio streams..."
                            page.update()
                        page.run_thread(update_status_merge)
                        
                        with tempfile.TemporaryDirectory() as temp_dir:
                            # Download video and audio to temp
                            video_file = video_stream.download(output_path=temp_dir, filename="video.mp4")
                            audio_file = audio_stream.download(output_path=temp_dir, filename="audio.mp4")
                            
                            # Merge with FFmpeg
                            output_file = os.path.join(download_dir, f"{yt.title}.mp4")
                            
                            def update_status_ffmpeg():
                                status_text.value = "Merging with FFmpeg..."
                                page.update()
                            page.run_thread(update_status_ffmpeg)
                            
                            merge_cmd = ['ffmpeg', '-i', video_file, '-i', audio_file, '-c', 'copy', '-y', output_file]
                            subprocess.run(merge_cmd, check=True, capture_output=True)
                        
                        def update_ui_success():
                            progress_ring.visible = False
                            download_button.disabled = False
                            status_text.value = "Download completed!"
                            status_text.color = ft.Colors.GREEN_600
                            page.update()
                            show_success_dialog("Video Downloaded Successfully!", output_file)
                        
                        page.run_thread(update_ui_success)
                        return
                
                # Fallback to highest progressive stream
                def update_status_progressive():
                    status_text.value = "FFmpeg not available - using progressive stream..."
                    page.update()
                page.run_thread(update_status_progressive)
                
                stream = yt.streams.get_highest_resolution()
                
                if not stream:
                    def update_ui_no_stream():
                        progress_ring.visible = False
                        download_button.disabled = False
                        status_text.value = "Ready to download"
                        status_text.color = ft.Colors.RED_600
                        page.update()
                        show_error_dialog("Error", "No suitable stream found.")
                    page.run_thread(update_ui_no_stream)
                    return
                
                output_file = stream.download(output_path=download_dir)
                
                def update_ui_progressive_success():
                    progress_ring.visible = False
                    download_button.disabled = False
                    status_text.value = "Download completed!"
                    status_text.color = ft.Colors.GREEN_600
                    page.update()
                    show_success_dialog("Video Downloaded Successfully (Progressive - No FFmpeg)!", output_file)
                
                page.run_thread(update_ui_progressive_success)
                
            except Exception as e:
                def update_ui_error():
                    progress_ring.visible = False
                    download_button.disabled = False
                    status_text.value = "Download failed"
                    status_text.color = ft.Colors.RED_600
                    page.update()
                    show_error_dialog("Download Error", f"Download failed:\n\n{str(e)}")
                
                page.run_thread(update_ui_error)
        
        threading.Thread(target=download_thread, daemon=True).start()
    
    # Assign button events
    download_button.on_click = download_video
    location_button.on_click = change_download_location
    
    # Global variable for download directory
    global DEFAULT_DOWNLOAD_DIR
    DEFAULT_DOWNLOAD_DIR = r"C:\Users\jpagu\Downloads\Youtube Videos"
    
    # Layout
    page.add(
        ft.Container(
            content=ft.Container(
                content=ft.Column([
                    # Header
                    ft.Container(
                        content=ft.Column([
                            title,
                            ft.Container(height=5),
                            ffmpeg_status,
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        alignment=ft.alignment.center,
                        margin=ft.margin.only(bottom=25)
                    ),
                    
                    # URL input with info button
                    ft.Container(
                        content=url_field,
                        margin=ft.margin.only(bottom=25)
                    ),
                    
                    # Download and location buttons
                    ft.Container(
                        content=ft.Row([
                            download_button,
                            ft.Container(width=15),
                            location_button,
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        margin=ft.margin.only(bottom=20)
                    ),
                    
                    # Progress ring
                    ft.Container(
                        content=progress_ring,
                        margin=ft.margin.only(bottom=15)
                    ),
                    
                    # Status and info
                    ft.Container(
                        content=ft.Column([
                            status_text,
                            ft.Container(height=5),
                            output_info,
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