import os
import threading
import flet as ft
from difflib import SequenceMatcher

def main(page: ft.Page):
    page.title = "Plagiarism Checker"
    page.window_resizable = False
    page.window.center()
    page.theme_mode = "light"
    page.padding = 30
    page.window.height = 665
    page.window.width = 550
    
    # Global variables for selected files
    file1_path = ""
    file2_path = ""
    
    # Create UI elements
    title = ft.Text(
        "Plagiarism Checker",
        size=30,
        font_family="Arial",
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.INDIGO_800,
        text_align=ft.TextAlign.CENTER
    )
    
    # File 1 selection
    file1_field = ft.TextField(
        label="First File",
        hint_text="Click browse to select first file",
        width=280,
        border_radius=10,
        border_color=ft.Colors.INDIGO_600,
        focused_border_color=ft.Colors.INDIGO_600,
        read_only=True
    )
    
    browse1_button = ft.ElevatedButton(
        text="Browse",
        width=100,
        height=40,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_600,
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )
    
    # File 2 selection
    file2_field = ft.TextField(
        label="Second File",
        hint_text="Click browse to select second file",
        width=280,
        border_radius=10,
        border_color=ft.Colors.INDIGO_600,
        focused_border_color=ft.Colors.INDIGO_600,
        read_only=True
    )
    
    browse2_button = ft.ElevatedButton(
        text="Browse",
        width=100,
        height=40,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_600,
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )
    
    # Check plagiarism button
    check_button = ft.ElevatedButton(
        text="Check Plagiarism",
        width=150,
        height=50,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.INDIGO_600,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        disabled=True  # Disabled until both files are selected
    )
    
    # Clear selection button
    clear_button = ft.ElevatedButton(
        text="Clear Files",
        width=100,
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
        color=ft.Colors.INDIGO_600,
        width=25,
        height=25
    )
    
    # Status text
    status_text = ft.Text(
        "Select two files to compare",
        size=14,
        color=ft.Colors.INDIGO_600,
        text_align=ft.TextAlign.CENTER
    )
    
    # Result display
    result_text = ft.Text(
        "Similarity: Not calculated",
        size=18,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.GREY_600,
        text_align=ft.TextAlign.CENTER
    )
    
    # File info
    file_info = ft.Text(
        "No files selected",
        size=12,
        color=ft.Colors.GREY_500,
        text_align=ft.TextAlign.CENTER
    )
    
    # Dialog functions
    def close_dialog(dialog):
        dialog.open = False
        page.update()
    
    def show_results_dialog(similarity, file1_name, file2_name, file1_size, file2_size):
        # Determine similarity level and color
        if similarity >= 80:
            similarity_level = "Very High"
            color = ft.Colors.RED_600
        elif similarity >= 60:
            similarity_level = "High"
            color = ft.Colors.ORANGE_600
        elif similarity >= 40:
            similarity_level = "Medium"
            color = ft.Colors.YELLOW_800
        elif similarity >= 20:
            similarity_level = "Low"
            color = ft.Colors.BLUE_600
        else:
            similarity_level = "Very Low"
            color = ft.Colors.GREEN_600
        
        results_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Plagiarism Check Results", color=ft.Colors.INDIGO_600),
            content=ft.Column([
                ft.Text(f"📄 File 1: {file1_name}", weight=ft.FontWeight.BOLD),
                ft.Text(f"📄 File 2: {file2_name}", weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text(f"📊 Similarity: {similarity:.2f}%", size=18, color=color, weight=ft.FontWeight.BOLD),
                ft.Text(f"📈 Level: {similarity_level}", size=14, color=color),
                ft.Divider(),
                ft.Text(f"📏 File 1 size: {file1_size} characters"),
                ft.Text(f"📏 File 2 size: {file2_size} characters"),
                ft.Divider(),
                ft.Text("Analysis complete!", color=ft.Colors.GREEN_600, italic=True)
            ], tight=True),
            actions=[
                ft.TextButton("OK", on_click=lambda e: close_dialog(results_dialog))
            ],
        )
        page.dialog = results_dialog
        results_dialog.open = True
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
    
    # Update UI state function
    def update_ui_state():
        nonlocal file1_path, file2_path
        
        # Update file fields
        file1_field.value = os.path.basename(file1_path) if file1_path else ""
        file2_field.value = os.path.basename(file2_path) if file2_path else ""
        
        # Update file info
        if file1_path and file2_path:
            file_info.value = f"Ready to compare: {os.path.basename(file1_path)} vs {os.path.basename(file2_path)}"
            file_info.color = ft.Colors.GREEN_600
            check_button.disabled = False
            clear_button.disabled = False
            status_text.value = "Files selected - ready to check"
        elif file1_path or file2_path:
            selected = os.path.basename(file1_path) if file1_path else os.path.basename(file2_path)
            file_info.value = f"Selected: {selected} (need one more file)"
            file_info.color = ft.Colors.ORANGE_600
            check_button.disabled = True
            clear_button.disabled = False
            status_text.value = "Select second file to continue"
        else:
            file_info.value = "No files selected"
            file_info.color = ft.Colors.GREY_500
            check_button.disabled = True
            clear_button.disabled = True
            status_text.value = "Select two files to compare"
        
        page.update()
    
    # File selection functions
    def select_file1(e):
        def file_picker_result(e: ft.FilePickerResultEvent):
            nonlocal file1_path
            if e.files:
                file1_path = e.files[0].path
                update_ui_state()
        
        file_picker = ft.FilePicker(on_result=file_picker_result)
        page.overlay.append(file_picker)
        page.update()
        
        file_picker.pick_files(
            dialog_title="Select the first file",
            allowed_extensions=["txt", "doc", "docx", "py", "js", "html", "css", "md"]
        )
    
    def select_file2(e):
        def file_picker_result(e: ft.FilePickerResultEvent):
            nonlocal file2_path
            if e.files:
                file2_path = e.files[0].path
                update_ui_state()
        
        file_picker = ft.FilePicker(on_result=file_picker_result)
        page.overlay.append(file_picker)
        page.update()
        
        file_picker.pick_files(
            dialog_title="Select the second file",
            allowed_extensions=["txt", "doc", "docx", "py", "js", "html", "css", "md"]
        )
    
    # Clear files function
    def clear_files(e):
        nonlocal file1_path, file2_path
        file1_path = ""
        file2_path = ""
        result_text.value = "Similarity: Not calculated"
        result_text.color = ft.Colors.GREY_600
        update_ui_state()
    
    # Plagiarism check function
    def plagiarism_checker(f1, f2):
        """Check similarity between two files"""
        try:
            with open(f1, 'r', encoding='utf-8', errors="ignore") as file1:
                f1_data = file1.read()
            
            with open(f2, 'r', encoding='utf-8', errors="ignore") as file2:
                f2_data = file2.read()
            
            # Calculate similarity
            similarity = SequenceMatcher(None, f1_data, f2_data).ratio() * 100
            
            return similarity, len(f1_data), len(f2_data)
        
        except Exception as e:
            raise Exception(f"Error reading files: {str(e)}")
    
    # Check plagiarism function
    def check_plagiarism(e):
        if not file1_path or not file2_path:
            show_error_dialog("Error", "Please select both files first")
            return
        
        # Update UI for checking
        check_button.disabled = True
        progress_ring.visible = True
        status_text.value = "Analyzing files... Please wait"
        status_text.color = ft.Colors.INDIGO_600
        page.update()
        
        def check_thread():
            try:
                # Perform plagiarism check
                similarity, file1_size, file2_size = plagiarism_checker(file1_path, file2_path)
                
                # Determine result color based on similarity
                if similarity >= 80:
                    color = ft.Colors.RED_600
                elif similarity >= 60:
                    color = ft.Colors.ORANGE_600
                elif similarity >= 40:
                    color = ft.Colors.YELLOW_800
                elif similarity >= 20:
                    color = ft.Colors.BLUE_600
                else:
                    color = ft.Colors.GREEN_600
                
                def update_ui_success():
                    progress_ring.visible = False
                    check_button.disabled = False
                    status_text.value = "Analysis completed!"
                    status_text.color = ft.Colors.GREEN_600
                    result_text.value = f"Similarity: {similarity:.2f}%"
                    result_text.color = color
                    page.update()
                    
                    # Show detailed results
                    show_results_dialog(
                        similarity, 
                        os.path.basename(file1_path), 
                        os.path.basename(file2_path),
                        file1_size,
                        file2_size
                    )
                
                page.run_thread(update_ui_success)
                
            except Exception as ex:
                error_msg = str(ex)
                def update_ui_error():
                    progress_ring.visible = False
                    check_button.disabled = False
                    status_text.value = "Analysis failed"
                    status_text.color = ft.Colors.RED_600
                    result_text.value = "Similarity: Error"
                    result_text.color = ft.Colors.RED_600
                    page.update()
                    show_error_dialog("Analysis Error", f"Failed to analyze files:\n\n{error_msg}")
                
                page.run_thread(update_ui_error)
        
        threading.Thread(target=check_thread, daemon=True).start()
    
    # Assign button events
    browse1_button.on_click = select_file1
    browse2_button.on_click = select_file2
    check_button.on_click = check_plagiarism
    clear_button.on_click = clear_files
    
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
                    
                    # File 1 selection
                    ft.Container(
                        content=ft.Row([
                            file1_field,
                            ft.Container(width=10),
                            browse1_button,
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        margin=ft.margin.only(bottom=15)
                    ),
                    
                    # File 2 selection
                    ft.Container(
                        content=ft.Row([
                            file2_field,
                            ft.Container(width=10),
                            browse2_button,
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        margin=ft.margin.only(bottom=20)
                    ),
                    
                    # File info
                    ft.Container(
                        content=file_info,
                        margin=ft.margin.only(bottom=25)
                    ),
                    
                    # Check and clear buttons
                    ft.Container(
                        content=ft.Row([
                            check_button,
                            ft.Container(width=15),
                            clear_button,
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        margin=ft.margin.only(bottom=15)
                    ),
                    
                    # Progress ring
                    ft.Container(
                        content=progress_ring,
                        margin=ft.margin.only(bottom=20)
                    ),
                    
                    # Result display
                    ft.Container(
                        content=ft.Column([
                            result_text,
                            ft.Container(height=10),
                            status_text,
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=15,
                        bgcolor=ft.Colors.GREY_50,
                        border_radius=10,
                        border=ft.border.all(1, ft.Colors.GREY_300)
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