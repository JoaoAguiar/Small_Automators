import os
import threading
import flet as ft

try:
    from PIL import Image
except ImportError:
    print("PIL (Pillow) is not installed. Please install it with: pip install Pillow")
    exit()

def create_default_directory():
    """Create default output directory if it doesn't exist"""
    default_dir = r"C:\Users\jpagu\Downloads\Compressed Photos"

    if not os.path.exists(default_dir):
        try:
            os.makedirs(default_dir)
        except Exception as e:
            return None
    
    return default_dir

def main(page: ft.Page):
    page.title = "Photo Compressor"
    page.window_resizable = False
    page.window.center()
    page.theme_mode = "light"
    page.padding = 30
    page.window.height = 700
    page.window.width = 550
    
    # Create UI elements
    title = ft.Text(
        "Photo Compressor",
        size=30,
        font_family="Arial",
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_900,
        text_align=ft.TextAlign.CENTER
    )
    
    # File picker field
    file_field = ft.TextField(
        label="Select Image File",
        hint_text="Click browse to select an image",
        width=250,
        border_radius=10,
        border_color=ft.Colors.BLUE_600,
        focused_border_color=ft.Colors.BLUE_600,
        read_only=True
    )
    
    # Folder picker field
    folder_field = ft.TextField(
        label="Or Select Folder",
        hint_text="Click browse to select a folder",
        width=250,
        border_radius=10,
        border_color=ft.Colors.BLUE_600,
        focused_border_color=ft.Colors.BLUE_600,
        read_only=True
    )
    
    # Quality slider
    quality_slider = ft.Slider(
        min=1,
        max=100,
        value=85,
        divisions=99,
        label="{value}%",
        width=400,
        active_color=ft.Colors.BLUE_600,
        inactive_color=ft.Colors.GREY_300
    )
    
    # Quality label
    quality_label = ft.Text(
        "Quality: 85%",
        size=14,
        color=ft.Colors.BLUE_600,
        text_align=ft.TextAlign.CENTER
    )
    
    # Browse buttons
    file_browse_button = ft.ElevatedButton(
        text="Browse File",
        width=120,
        height=40,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.GREY_600,
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )
    
    folder_browse_button = ft.ElevatedButton(
        text="Browse Folder",
        width=120,
        height=40,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.GREY_600,
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )
    
    # Compress button
    compress_button = ft.ElevatedButton(
        text="Compress",
        width=100,
        height=50,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.GREEN_600,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        disabled=False
    )
    
    # Progress ring
    progress_ring = ft.ProgressRing(
        visible=False,
        color=ft.Colors.GREEN_600,
        width=25,
        height=25
    )
    
    # Status text
    status_text = ft.Text(
        "Ready to compress",
        size=14,
        color=ft.Colors.GREEN_600,
        text_align=ft.TextAlign.CENTER
    )
    
    # Output info
    output_info = ft.Text(
        f"Output: C:\\Users\\jpagu\\Downloads\\Compressed Photos",
        size=12,
        color=ft.Colors.GREY_500,
        text_align=ft.TextAlign.CENTER
    )
    
    # Update quality label when slider changes
    def update_quality_label(e):
        quality_label.value = f"Quality: {int(quality_slider.value)}%"
        page.update()
    
    quality_slider.on_change = update_quality_label
    
    # File picker functions
    def pick_file(e):
        def file_picker_result(e: ft.FilePickerResultEvent):
            if e.files:
                file_field.value = e.files[0].path
                folder_field.value = ""  # Clear folder field
                page.update()
        
        file_picker = ft.FilePicker(on_result=file_picker_result)
        page.overlay.append(file_picker)
        page.update()
        
        file_picker.pick_files(
            dialog_title="Select an image file",
            allowed_extensions=["jpg", "jpeg", "png", "bmp", "gif"]
        )
    
    def pick_folder(e):
        def folder_picker_result(e: ft.FilePickerResultEvent):
            if e.path:
                folder_field.value = e.path
                file_field.value = ""  # Clear file field
                page.update()
        
        folder_picker = ft.FilePicker(on_result=folder_picker_result)
        page.overlay.append(folder_picker)
        page.update()
        
        folder_picker.get_directory_path(dialog_title="Select a folder")
    
    # Dialog functions
    def close_dialog(dialog):
        dialog.open = False
        page.update()
    
    def show_success_dialog(message, output_path=""):
        success_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Compression Completed!", color=ft.Colors.GREEN_600),
            content=ft.Column([
                ft.Text(message),
                ft.Divider(),
                ft.Text("Files saved to:", weight=ft.FontWeight.BOLD),
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
    
    # Compression function
    def compress_images(e):
        quality = int(quality_slider.value)
        
        file_path = file_field.value.strip()
        folder_path = folder_field.value.strip()
        
        if not file_path and not folder_path:
            show_error_dialog("Error", "Please select a file or folder")
            return
        
        # Validate paths
        if file_path and not os.path.isfile(file_path):
            show_error_dialog("Error", "Selected file does not exist")
            return
        if folder_path and not os.path.isdir(folder_path):
            show_error_dialog("Error", "Selected folder does not exist")
            return
        
        # Use default directory
        output_dir = create_default_directory()
        if not output_dir:
            show_error_dialog("Error", "Could not create output directory")
            return
        
        # Update UI for compression
        compress_button.disabled = True
        progress_ring.visible = True
        status_text.value = "Compressing... Please wait"
        status_text.color = ft.Colors.GREEN_600
        page.update()
        
        def compress_thread():
            try:
                if file_path:
                    # Compress single file
                    try:
                        img = Image.open(file_path)
                        if img.mode != 'RGB':
                            img = img.convert('RGB')
                        
                        base_name = os.path.splitext(os.path.basename(file_path))[0]
                        output_path = os.path.join(output_dir, f"{base_name}_compressed.jpg")
                        img.save(output_path, "JPEG", optimize=True, quality=quality)
                        img.close()
                        
                        def update_ui_success():
                            progress_ring.visible = False
                            compress_button.disabled = False
                            status_text.value = "Compression completed!"
                            status_text.color = ft.Colors.GREEN_600
                            page.update()
                            show_success_dialog("Image compressed successfully!", output_path)
                        
                        page.run_thread(update_ui_success)
                        
                    except Exception as img_error:
                        error_msg = f"Error processing image: {str(img_error)}"
                        def update_ui_error():
                            progress_ring.visible = False
                            compress_button.disabled = False
                            status_text.value = "Compression failed"
                            status_text.color = ft.Colors.RED_600
                            page.update()
                            show_error_dialog("Error", error_msg)
                        page.run_thread(update_ui_error)
                        return
                
                else:
                    # Compress all images in folder
                    try:
                        image_files = []
                        for f in os.listdir(folder_path):
                            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
                                image_files.append(f)
                        
                        if not image_files:
                            def update_ui_no_files():
                                progress_ring.visible = False
                                compress_button.disabled = False
                                status_text.value = "No images found"
                                status_text.color = ft.Colors.ORANGE_600
                                page.update()
                                show_error_dialog("Warning", "No image files found in the selected folder")
                            page.run_thread(update_ui_no_files)
                            return
                        
                        successful_compressions = 0
                        
                        for i, filename in enumerate(image_files):
                            img_path = os.path.join(folder_path, filename)
                            try:
                                img = Image.open(img_path)
                                if img.mode != 'RGB':
                                    img = img.convert('RGB')
                                
                                base_name = os.path.splitext(filename)[0]
                                output_path = os.path.join(output_dir, f"{base_name}_compressed.jpg")
                                img.save(output_path, "JPEG", optimize=True, quality=quality)
                                img.close()
                                successful_compressions += 1
                                
                            except Exception as img_error:
                                print(f"Error processing {filename}: {img_error}")
                                continue
                        
                            # Update progress
                            progress = int((i + 1) / len(image_files) * 100)
                            def update_progress_ui():
                                status_text.value = f"Compressing: {progress}%"
                                page.update()
                            page.run_thread(update_progress_ui)
                        
                        def update_ui_folder_success():
                            progress_ring.visible = False
                            compress_button.disabled = False
                            status_text.value = "Compression completed!"
                            status_text.color = ft.Colors.GREEN_600
                            page.update()
                            show_success_dialog(f"{successful_compressions} of {len(image_files)} images compressed successfully!", output_dir)
                        
                        page.run_thread(update_ui_folder_success)
                        
                    except Exception as folder_error:
                        error_msg = f"Error processing folder: {str(folder_error)}"
                        def update_ui_folder_error():
                            progress_ring.visible = False
                            compress_button.disabled = False
                            status_text.value = "Compression failed"
                            status_text.color = ft.Colors.RED_600
                            page.update()
                            show_error_dialog("Error", error_msg)
                        page.run_thread(update_ui_folder_error)
                
            except Exception as e:
                error_msg = f"Unexpected error: {str(e)}"
                def update_ui_general_error():
                    progress_ring.visible = False
                    compress_button.disabled = False
                    status_text.value = "Compression failed"
                    status_text.color = ft.Colors.RED_600
                    page.update()
                    show_error_dialog("Error", error_msg)
                page.run_thread(update_ui_general_error)
        
        threading.Thread(target=compress_thread, daemon=True).start()
    
    # Assign button events
    file_browse_button.on_click = pick_file
    folder_browse_button.on_click = pick_folder
    compress_button.on_click = compress_images
    
    # Layout
    page.add(
        ft.Container(
            content=ft.Container(
                content=ft.Column([
                    # Header
                    ft.Container(
                        content=title,
                        alignment=ft.alignment.center,
                        margin=ft.margin.only(bottom=30)
                    ),
                    
                    # File selection - CAMPO E BOTÃO LADO A LADO
                    ft.Container(
                        content=ft.Row([
                            file_field,
                            ft.Container(width=10),  # Espaçamento entre campo e botão
                            file_browse_button,
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        margin=ft.margin.only(bottom=20)
                    ),
                    
                    # Folder selection - CAMPO E BOTÃO LADO A LADO
                    ft.Container(
                        content=ft.Row([
                            folder_field,
                            ft.Container(width=10),  # Espaçamento entre campo e botão
                            folder_browse_button,
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        margin=ft.margin.only(bottom=20)
                    ),
                    
                    # Quality setting with slider
                    ft.Container(
                        content=ft.Column([
                            quality_label,
                            ft.Container(height=5),
                            quality_slider,
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        margin=ft.margin.only(bottom=25)
                    ),
                    
                    # Compress button and progress
                    ft.Container(
                        content=ft.Column([
                            compress_button,
                            ft.Container(height=10),
                            progress_ring,
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        margin=ft.margin.only(bottom=25)
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