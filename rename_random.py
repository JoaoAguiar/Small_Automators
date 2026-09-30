import os
import random
import string
import threading
import flet as ft

def generate_random_name(length=8):
    """Generates a random name based on the specified length"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def get_files_to_rename(target_folder, recursive):
    """Generator that yields files to be renamed"""
    if recursive:
        for root, _, files in os.walk(target_folder):
            for file_name in files:
                yield os.path.join(root, file_name), file_name
    else:
        for file_name in os.listdir(target_folder):
            full_path = os.path.join(target_folder, file_name)
            if os.path.isfile(full_path):
                yield full_path, file_name

async def main(page: ft.Page):
    page.title = "Random File Renamer"
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 30
    page.window.height = 435
    page.window.width = 550
    await page.window.center()
    folder_picker = ft.FilePicker()
    
    # Global variable for selected folder
    selected_folder = r"C:\Users\jpagu\Pictures"
    
    # Create UI elements
    title = ft.Text(
        "Random File Renamer",
        size=30,
        font_family="Arial",
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.TEAL_800,
        text_align=ft.TextAlign.CENTER
    )
    
    # Folder selection
    folder_field = ft.TextField(
        label="Select Folder",
        hint_text="Click browse to select a folder",
        width=250,
        border_radius=10,
        border_color=ft.Colors.TEAL_600,
        focused_border_color=ft.Colors.TEAL_600,
        read_only=True
    )
    
    browse_button = ft.Button(
        content="Browse",
        width=100,
        height=40,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_600,
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )
    

    
    # Recursive checkbox
    recursive_checkbox = ft.Checkbox(
        label="Include subfolders (recursive)",
        value=False,
        fill_color=ft.Colors.TEAL_600
    )
    
    # Rename button
    rename_button = ft.Button(
        content="Rename Files",
        width=140,
        height=50,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.TEAL_600,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        disabled=True  # Disabled until folder is selected
    )
    
    # File count info
    file_count_text = ft.Text(
        "No folder selected",
        size=12,
        color=ft.Colors.GREY_500,
        text_align=ft.TextAlign.CENTER
    )
    
    # Dialog functions
    def close_dialog(dialog):
        if dialog.open:
            page.pop_dialog()
    
    def show_success_dialog(renamed_count, error_count, folder_path):
        success_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Rename Operation Completed!", color=ft.Colors.GREEN_600),
            content=ft.Column([
                ft.Text(f"📁 Folder: {os.path.basename(folder_path)}"),
                ft.Divider(),
                ft.Text(f"✅ Files renamed: {renamed_count}", color=ft.Colors.GREEN_600),
                ft.Text(f"❌ Errors: {error_count}", color=ft.Colors.RED_600 if error_count > 0 else ft.Colors.GREY_500),
                ft.Divider(),
                ft.Text("Operation completed!", color=ft.Colors.GREEN_600, italic=True)
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
    
    # Update UI state
    def update_ui_state():
        nonlocal selected_folder
        
        if selected_folder:
            folder_field.value = os.path.basename(selected_folder)
            
            # Count files
            try:
                name_length = 8
                recursive = recursive_checkbox.value
                
                files_list = list(get_files_to_rename(selected_folder, recursive))
                file_count = len(files_list)
                
                if file_count > 0:
                    file_count_text.value = f"{file_count} file(s) found"
                    file_count_text.color = ft.Colors.GREEN_600
                    rename_button.disabled = False
                else:
                    file_count_text.value = "No files found in selected folder"
                    file_count_text.color = ft.Colors.ORANGE_600
                    rename_button.disabled = True
                                
            except Exception as e:
                file_count_text.value = f"Error accessing folder: {str(e)}"
                file_count_text.color = ft.Colors.RED_600
                rename_button.disabled = True
        else:
            folder_field.value = ""
            file_count_text.value = "No folder selected"
            file_count_text.color = ft.Colors.GREY_500
            rename_button.disabled = True
        
        page.update()
    
    # Folder selection function
    async def select_folder(e):
        nonlocal selected_folder

        selected_path = await folder_picker.get_directory_path(
            dialog_title="Select folder to rename files",
            initial_directory=selected_folder,
        )
        if selected_path:
            selected_folder = selected_path
            update_ui_state()
    
    # Rename files function
    def rename_files(e):
        if not selected_folder:
            show_error_dialog("Error", "Please select a folder first")
            return
        
        name_length = 8
        
        recursive = recursive_checkbox.value
        
        try:
            files_list = list(get_files_to_rename(selected_folder, recursive))
            
            if not files_list:
                show_error_dialog("No Files", "No files found in the selected folder")
                return
            
            # Directly call perform_rename instead of showing confirmation dialog
            perform_rename()
            
        except Exception as ex:
            show_error_dialog("Error", f"Error accessing folder:\n\n{str(ex)}")
    
    # Perform rename function
    def perform_rename():
        # Update UI for renaming
        rename_button.disabled = True
        page.update()
        
        def rename_thread():
            try:
                name_length = 8
                recursive = recursive_checkbox.value
                
                renamed_files = 0
                errors = 0
                
                files_list = list(get_files_to_rename(selected_folder, recursive))
                total_files = len(files_list)
                
                for i, (full_path, file_name) in enumerate(files_list):
                    # Update progress
                    progress = int((i + 1) / total_files * 100)
                    def update_progress():
                        page.update()
                    page.run_thread(update_progress)
                    
                    name, extension = os.path.splitext(file_name)
                    new_name = generate_random_name(name_length) + extension
                    new_full_path = os.path.join(os.path.dirname(full_path), new_name)

                    # Prevent potential name collisions
                    while os.path.exists(new_full_path):
                        new_name = generate_random_name(name_length) + extension
                        new_full_path = os.path.join(os.path.dirname(full_path), new_name)

                    try:
                        os.rename(full_path, new_full_path)
                        renamed_files += 1
                    except PermissionError:
                        errors += 1
                    except Exception as e:
                        errors += 1
                
                def update_ui_success():
                    rename_button.disabled = False
                    page.update()
                    show_success_dialog(renamed_files, errors, selected_folder)
                    update_ui_state()  # Refresh file count
                
                page.run_thread(update_ui_success)
                
            except Exception as ex:
                error_msg = str(ex)
                def update_ui_error():
                    rename_button.disabled = False
                    page.update()
                    show_error_dialog("Rename Error", f"Failed to rename files:\n\n{error_msg}")
                
                page.run_thread(update_ui_error)
        
        threading.Thread(target=rename_thread, daemon=True).start()
    
    # Event handlers
    browse_button.on_click = select_folder
    rename_button.on_click = rename_files
    recursive_checkbox.on_change = lambda e: update_ui_state()
    
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
                    
                    # Folder selection
                    ft.Container(
                        content=ft.Row([
                            folder_field,
                            ft.Container(width=10),
                            browse_button,
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        margin=ft.Margin(bottom=15)
                    ),
                    
                    # File count with recursive checkbox
                    ft.Container(
                        content=ft.Row([
                            recursive_checkbox,
                            ft.Container(width=20),
                            file_count_text,
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        margin=ft.Margin(bottom=30)
                    ),
                    
                    # Action button
                    ft.Container(
                        content=rename_button,
                        margin=ft.Margin(bottom=20)
                    ),                   
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