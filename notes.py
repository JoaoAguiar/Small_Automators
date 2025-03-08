import os
import sys
import argparse
import subprocess
import platform

class NoteAutomator:
    # Define file extensions for different programming languages
    EXTENSIONS = {
        "ruby": ".rb", "php": ".php", "javascript": ".js", "typescript": ".ts",
        "python": ".py", "java": ".java", "dart": ".dart", "text": ".txt", 
        "xml": ".xml", "html": ".html", "css": ".css", "json": ".json",
        "c": ".c", "cpp": ".cpp", "csharp": ".cs", "sql": ".sql"
    }
    
    # Basic templates for different file types
    TEMPLATES = {
        ".py": "#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n\n\ndef main():\n    pass\n\n\nif __name__ == \"__main__\":\n    main()\n",
        ".html": "<!DOCTYPE html>\n<html>\n<head>\n    <title>Title</title>\n    <meta charset=\"utf-8\">\n</head>\n<body>\n\n</body>\n</html>\n",
        ".js": "// JavaScript Document\n\n(function() {\n    'use strict';\n    \n    // Your code here\n    \n})();\n",
        ".java": "public class ClassName {\n    public static void main(String[] args) {\n        // Your code here\n    }\n}\n"
    }

    def __init__(self):
        self.extension = ".txt"
        self.folder_name = "general_folder"
        self.file_name = "general_note"
        self.path = os.getcwd()
        self.use_template = True

    def parse_args(self):
        """Parse command line arguments using argparse"""
        parser = argparse.ArgumentParser(description="Create and open note files with specific extensions")
        parser.add_argument("-e", "--extension", required=True, 
                           help="File extension/language (python, javascript, text, etc.)")
        parser.add_argument("-f", "--folder", required=True, 
                           help="Folder name to store the note")
        parser.add_argument("-n", "--name", required=True, 
                           help="Note file name (without extension)")
        parser.add_argument("-t", "--no-template", action="store_true",
                           help="Don't use language template (create empty file)")
        
        args = parser.parse_args()
        
        # Handle extension
        ext_value = args.extension.lower()
        if ext_value in self.EXTENSIONS:
            self.extension = self.EXTENSIONS[ext_value]
        else:
            print(f"Error: Invalid extension '{ext_value}'")
            print(f"Valid extensions are: {', '.join(sorted(self.EXTENSIONS.keys()))}")
            sys.exit(1)
        
        # Handle folder and filename
        self.folder_name = args.folder
        self.file_name = args.name
        self.use_template = not args.no_template
        
        return True

    def open_file_with_default_editor(self, filepath):
        """Open a file with the default editor based on OS"""
        try:
            if platform.system() == 'Windows':
                os.startfile(filepath)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', filepath])
            else:  # Linux and other Unix-like
                subprocess.run(['xdg-open', filepath])
        except Exception as e:
            print(f"Error opening file: {e}")
            print(f"File created at: {filepath}")

    def create_note_file(self):
        """Create the note file inside the specified folder."""
        full_filename = self.file_name + self.extension
        
        # Check if folder exists, if not, create it
        folder_path = os.path.join(self.path, self.folder_name)
        if not os.path.isdir(folder_path):
            try:
                os.mkdir(folder_path)
                print(f"Created folder: {folder_path}")
            except Exception as e:
                print(f"Error creating folder: {e}")
                return False

        # Create the full file path
        file_path = os.path.join(folder_path, full_filename)
        
        # Check if file already exists
        if os.path.exists(file_path):
            overwrite = input(f"File '{full_filename}' already exists. Overwrite? (y/n): ")
            if overwrite.lower() != 'y':
                print("Operation cancelled.")
                return False
        
        # Create the file with template content if available
        try:
            with open(file_path, "w") as f:
                if self.use_template and self.extension in self.TEMPLATES:
                    f.write(self.TEMPLATES[self.extension])
                    print(f"Created file with template: {file_path}")
                else:
                    print(f"Created empty file: {file_path}")
            
            # Open the created file with default editor
            self.open_file_with_default_editor(file_path)
            return True
            
        except Exception as e:
            print(f"Error creating file: {e}")
            return False


def main():
    # Initialize the note automator
    notes = NoteAutomator()
    
    try:
        # Parse arguments using argparse
        if len(sys.argv) > 1:
            notes.parse_args()
            notes.create_note_file()
        else:
            # If no arguments provided, show help
            print("Error: Missing arguments.")
            print("Usage: python notes.py -e <extension> -f <folder> -n <filename>")
            print("Example: python notes.py -e python -f my_notes -n todo_list")
            sys.exit(1)
            
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
