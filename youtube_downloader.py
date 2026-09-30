import os
import re
import subprocess
import tempfile
import threading

import flet as ft
from pytubefix import YouTube


def check_ffmpeg():
    """Check if ffmpeg is installed"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def sanitize_filename(filename):
    """Remove characters that are invalid in Windows filenames."""
    sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", filename).strip()
    return sanitized.rstrip(". ") or "youtube_video"

def is_valid_youtube_url(url):
    """Basic YouTube URL validation"""
    youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?\s]{11})'

    return re.fullmatch(youtube_regex, url) is not None

def create_default_directory():
    """Create default download directory if it doesn't exist"""
    default_dir = os.path.join(os.path.expanduser("~"), "Downloads", "Youtube Videos")

    if not os.path.exists(default_dir):
        try:
            os.makedirs(default_dir)
        except OSError:
            return os.path.expanduser("~/Downloads")

    return default_dir

async def main(page: ft.Page):
    page.title = "YouTube Downloader"
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 30
    page.window.height = 550
    page.window.width = 550
    await page.window.center()

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
    download_button = ft.Button(
        content="Download Video",
        width=140,
        height=50,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.RED_600,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        disabled=False,
    )

    # Change location button
    location_button = ft.Button(
        content="Change Location",
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
        f"Downloads to: {create_default_directory()}",
        size=12,
        color=ft.Colors.GREY_500,
        text_align=ft.TextAlign.CENTER
    )

    # FilePicker is a page-level service in Flet 1.x. Creating it during page
    # initialization registers it with the client before any button is clicked.
    async def change_download_location(e):
        nonlocal download_dir

        selected_path = await folder_picker.get_directory_path(
            dialog_title="Select Download Directory",
            initial_directory=download_dir,
        )
        if selected_path:
            download_dir = selected_path
            output_info.value = f"Downloads to: {selected_path}"
            page.update()
            show_success_dialog(f"Download directory changed to:\n{selected_path}")

    folder_picker = ft.FilePicker()

    # Dialog functions
    def close_dialog(dialog):
        if dialog.open:
            page.pop_dialog()

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
                ft.TextButton(content="OK", on_click=lambda e: close_dialog(success_dialog))
            ],
        )
        page.show_dialog(success_dialog)

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

    # Progress hook for download
    def progress_hook(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100

        def update_progress():
            status_text.value = f"Downloading: {percentage:.1f}%"
            page.update()

        page.run_thread(update_progress)

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
                output_dir = download_dir or create_default_directory()

                # Create YouTube object
                yt = YouTube(url, on_progress_callback=progress_hook)

                ffmpeg_available = check_ffmpeg()

                if ffmpeg_available:
                    # Select the highest available MP4 video and audio streams.
                    video_streams = yt.streams.filter(
                        only_video=True,
                        adaptive=True,
                        file_extension="mp4",
                    )
                    video_stream = video_streams.order_by("resolution").desc().first()
                    audio_streams = yt.streams.filter(
                        only_audio=True,
                        file_extension="mp4",
                    )
                    audio_stream = audio_streams.order_by("abr").desc().first()

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
                            output_file = os.path.join(
                                output_dir,
                                f"{sanitize_filename(yt.title)}.mp4",
                            )

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

                stream = (
                    yt.streams.filter(
                        progressive=True,
                        file_extension="mp4",
                    )
                    .order_by("resolution")
                    .desc()
                    .first()
                )

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

                output_file = stream.download(output_path=output_dir)
                if output_file is None:
                    raise RuntimeError("The download did not produce an output file.")

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

    download_dir = create_default_directory()

    # Layout
    page.add(
        ft.Container(
            content=ft.Container(
                content=ft.Column(
                    [
                        # Header
                        ft.Container(
                            content=ft.Column(
                                [
                                    title,
                                    ft.Container(height=5),
                                    ffmpeg_status,
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            alignment=ft.Alignment(0, 0),
                            margin=ft.Margin(bottom=25),
                        ),
                        # URL input with info button
                        ft.Container(content=url_field, margin=ft.Margin(bottom=25)),
                        # Download and location buttons
                        ft.Container(
                            content=ft.Row(
                                [
                                    download_button,
                                    ft.Container(width=15),
                                    location_button,
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            margin=ft.Margin(bottom=20),
                        ),
                        # Progress ring
                        ft.Container(
                            content=progress_ring, margin=ft.Margin(bottom=15)
                        ),
                        # Status and info
                        ft.Container(
                            content=ft.Column(
                                [
                                    status_text,
                                    ft.Container(height=5),
                                    output_info,
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            )
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=30,
                bgcolor=ft.Colors.WHITE,
                border_radius=15,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.Colors.with_opacity(0.3, ft.Colors.GREY_400),
                    offset=ft.Offset(0, 0),
                ),
            ),
            alignment=ft.Alignment(0, 0),
            expand=True,
        )
    )


if __name__ == "__main__":
    ft.run(main)
