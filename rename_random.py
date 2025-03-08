import os
import random
import string
import sys
import argparse

def generate_random_name(length=8):
    """Generates a random name based on the specified length"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def rename_files_in_directory(target_folder, name_length=8, recursive=False, confirm=True):
    """Renames all files in the target folder with random names"""
    if not os.path.exists(target_folder):
        print(f"Error: The folder '{target_folder}' does not exist.")
        return 0, 0
    
    # Count files before asking for confirmation
    file_count = sum(1 for _ in get_files_to_rename(target_folder, recursive))
    
    if confirm and file_count > 0:
        user_input = input(f"This will rename {file_count} file(s) in '{target_folder}'. Continue? (y/n): ")
        if user_input.lower() != 'y':
            print("Operation cancelled.")
            return 0, 0
    
    renamed_files = 0
    errors = 0
    
    for full_path, file_name in get_files_to_rename(target_folder, recursive):
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
            print(f"File '{file_name}' renamed to '{new_name}'.")
        except PermissionError:
            print(f"Permission denied to rename the file '{file_name}'.")
            errors += 1
        except Exception as e:
            print(f"Error renaming the file '{file_name}': {e}")
            errors += 1
    
    return renamed_files, errors

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

def main():
    parser = argparse.ArgumentParser(description="Rename files with random alphanumeric names.")
    parser.add_argument("folders", nargs="*", help="Folders containing files to rename")
    parser.add_argument("-l", "--length", type=int, default=8, help="Length of random names (default: 8)")
    parser.add_argument("-r", "--recursive", action="store_true", help="Process subdirectories recursively")
    parser.add_argument("-y", "--yes", action="store_true", help="Skip confirmation prompt")
    
    args = parser.parse_args()
    
    # If no folders provided, ask for input
    folders = args.folders
    if not folders:
        folder_input = input("Enter folder paths separated by commas: ")
        folders = [folder.strip() for folder in folder_input.split(",")]
    
    total_renamed = 0
    total_errors = 0
    
    for target_folder in folders:
        renamed, errors = rename_files_in_directory(
            target_folder, 
            name_length=args.length,
            recursive=args.recursive,
            confirm=not args.yes
        )
        total_renamed += renamed
        total_errors += errors
        
        if renamed == 0 and errors == 0:
            print(f"No files found to rename in '{target_folder}'.")
    
    print(f"\nSummary: {total_renamed} file(s) renamed successfully, {total_errors} error(s) encountered.")

if __name__ == "__main__":
    main()
