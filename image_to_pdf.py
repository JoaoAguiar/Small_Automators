import os
import threading
import flet as ft
from fpdf import FPDF

def create_default_directory():
    """Create default output directory if it doesn't exist"""
    default_dir = r"C:\Users\jpagu\Downloads\Image to PDF Files"
    if not os.path.exists(default_dir):
        try:
            os.makedirs(default_dir)
        except Exception as e:
            return os.path.expanduser("~/Downloads")
    return default_dir

async def main(page: ft.Page):
    page.title = "Image to PDF Converter"
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 30
    page.window.height = 650
    page.window.width = 520
    await page.window.center()
    file_picker = ft.FilePicker()

    # Set custom icon
    icon_path = os.path.join(os.path.dirname(__file__), "youtube_icon.png")
    if os.path.exists(icon_path):
        page.window.icon = icon_path
    
    # Global variable for selected images
    selected_images: list[str] = []
    
    # Create UI elements
    title = ft.Text(
        "Image to PDF Converter",
        size=30,
        font_family="Arial",
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.DEEP_ORANGE_800,
        text_align=ft.TextAlign.CENTER
    )
    
    # Selected files display
    files_text = ft.Text(
        "No images selected",
        size=12,
        color=ft.Colors.GREY_600,
        text_align=ft.TextAlign.CENTER
    )
    
    # Select images button
    select_button = ft.Button(
        content="Select Images",
        width=140,
        height=45,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_600,
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )
    
    # PDF filename field
    filename_field = ft.TextField(
        label="PDF Filename (without .pdf)",
        hint_text="e.g., my_document",
        value="image_to_pdf_result",
        width=300,
        border_radius=10,
        border_color=ft.Colors.DEEP_ORANGE_600,
        focused_border_color=ft.Colors.DEEP_ORANGE_600,
    )
    
    # Convert button
    convert_button = ft.Button(
        content="Convert to PDF",
        width=140,
        height=50,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.DEEP_ORANGE_600,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        disabled=True  # Disabled until images are selected
    )
    
    # Clear selection button
    clear_button = ft.Button(
        content="Clear Selection",
        width=120,
        height=40,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.GREY_600,
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
        disabled=True
    )
    
    # Progress ring
    progress_ring = ft.ProgressRing(
        visible=False,
        color=ft.Colors.DEEP_ORANGE_600,
        width=25,
        height=25
    )
    
    # Status text
    status_text = ft.Text(
        "Ready to convert images to PDF",
        size=14,
        color=ft.Colors.DEEP_ORANGE_600,
        text_align=ft.TextAlign.CENTER
    )
    
    # Output info
    output_info = ft.Text(
        f"PDFs saved to: C:\\Users\\jpagu\\Downloads\\Image to PDF Files",
        size=12,
        color=ft.Colors.GREY_500,
        text_align=ft.TextAlign.CENTER
    )
    
    # Dialog functions
    def close_dialog(dialog):
        if dialog.open:
            page.pop_dialog()
    
    def show_success_dialog(message, output_path=""):
        success_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("PDF Created Successfully!", color=ft.Colors.GREEN_600),
            content=ft.Column([
                ft.Text(message),
                ft.Divider(),
                ft.Text("PDF saved to:", weight=ft.FontWeight.BOLD),
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
    
    def show_images_dialog():
        if not selected_images:
            return
            
        # Create list of image names
        image_list = ft.Column([
            ft.Text(f"{i+1}. {os.path.basename(img)}", size=12)
            for i, img in enumerate(selected_images[:15])  # Show first 15
        ])
        
        if len(selected_images) > 15:
            image_list.controls.append(
                ft.Text(f"... and {len(selected_images) - 15} more images", 
                       size=12, italic=True, color=ft.Colors.GREY_600)
            )
        
        images_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Selected Images ({len(selected_images)})", color=ft.Colors.BLUE_600),
            content=ft.Container(
                content=image_list,
                height=300,
                width=400
            ),
            actions=[
                ft.TextButton(content="OK", on_click=lambda e: close_dialog(images_dialog))
            ],
        )
        page.show_dialog(images_dialog)
    
    # File selection function
    async def select_images(e):
        def file_picker_result(e: ft.FilePickerResultEvent):
            nonlocal selected_images
            
            if e.files:
                selected_images = []
                for selected_file in e.files:
                    if selected_file.path:
                        selected_images.append(selected_file.path)
                
                # Update UI
                files_text.value = f"{len(selected_images)} image(s) selected"
                files_text.color = ft.Colors.GREEN_600
                convert_button.disabled = False
                clear_button.disabled = False
                
                page.update()
        
        file_picker.on_result = file_picker_result
        await file_picker.pick_files(
            dialog_title="Select images to convert to PDF",
            allowed_extensions=["jpg", "jpeg", "png", "bmp", "gif"],
            allow_multiple=True
        )
    
    # Clear selection function
    def clear_selection(e):
        nonlocal selected_images
        selected_images = []
        
        # Update UI
        files_text.value = "No images selected"
        files_text.color = ft.Colors.GREY_600
        convert_button.disabled = True
        clear_button.disabled = True
        
        page.update()
    
    # Convert to PDF function
    def convert_to_pdf(e):
        if not selected_images:
            show_error_dialog("Error", "Please select images first")
            return
        
        filename = filename_field.value.strip()
        if not filename:
            show_error_dialog("Error", "Please enter a filename")
            return
        
        # Ensure filename doesn't end with .pdf (we'll add it)
        if filename.lower().endswith('.pdf'):
            filename = filename[:-4]
        
        # Update UI for conversion
        convert_button.disabled = True
        progress_ring.visible = True
        status_text.value = "Creating PDF... Please wait"
        status_text.color = ft.Colors.DEEP_ORANGE_600
        page.update()
        
        def convert_thread():
            try:
                output_dir = create_default_directory()
                output_file = os.path.join(output_dir, f"{filename}.pdf")
                
                # Create PDF
                pdf = FPDF()
                
                total_images = len(selected_images)
                
                for i, image_path in enumerate(selected_images):
                    try:
                        # Update progress
                        progress = int((i + 1) / total_images * 100)
                        def update_progress():
                            status_text.value = f"Processing image {i+1}/{total_images} ({progress}%)"
                            page.update()
                        page.run_thread(update_progress)
                        
                        # Add page and image
                        pdf.add_page()
                        
                        # Try to fit image to page while maintaining aspect ratio
                        try:
                            pdf.image(image_path, x=0, y=0, w=210)  # A4 width ≈ 210mm
                        except Exception as img_error:
                            print(f"Error adding image {image_path}: {img_error}")
                            continue
                        
                    except Exception as e:
                        print(f"Error processing image {image_path}: {e}")
                        continue
                
                # Save PDF
                def update_saving():
                    status_text.value = "Saving PDF..."
                    page.update()
                page.run_thread(update_saving)
                
                pdf.output(output_file)
                
                def update_ui_success():
                    progress_ring.visible = False
                    convert_button.disabled = False
                    status_text.value = "PDF created successfully!"
                    status_text.color = ft.Colors.GREEN_600
                    page.update()
                    show_success_dialog(f"PDF created with {len(selected_images)} images!", output_file)
                
                page.run_thread(update_ui_success)
                
            except Exception as ex:
                error_msg = str(ex)
                def update_ui_error():
                    progress_ring.visible = False
                    convert_button.disabled = False
                    status_text.value = "PDF creation failed"
                    status_text.color = ft.Colors.RED_600
                    page.update()
                    show_error_dialog("Conversion Error", f"Failed to create PDF:\n\n{error_msg}")
                
                page.run_thread(update_ui_error)
        
        threading.Thread(target=convert_thread, daemon=True).start()
    
    # Assign button events
    select_button.on_click = select_images
    clear_button.on_click = clear_selection
    convert_button.on_click = convert_to_pdf

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
                    
                    # Image selection
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Container(
                                    content=files_text,
                                    on_click=lambda e: show_images_dialog(),
                                    bgcolor=ft.Colors.GREY_50,
                                    padding=10,
                                    border_radius=8,
                                    border=ft.Border.all(1, ft.Colors.GREY_300),
                                    width=200
                                ),
                                ft.Container(width=10),
                                select_button,
                            ], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Container(height=8),
                            clear_button,
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        margin=ft.Margin(bottom=25)
                    ),
                    
                    # Filename input
                    ft.Container(
                        content=filename_field,
                        margin=ft.Margin(bottom=25)
                    ),
                    
                    # Convert button and progress
                    ft.Container(
                        content=ft.Column([
                            convert_button,
                            ft.Container(height=10),
                            progress_ring,
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        margin=ft.Margin(bottom=25)
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
            alignment=ft.Alignment(0, 0),
            expand=True,
        )
    )

if __name__ == "__main__":
    ft.run(main)