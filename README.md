# Python Automation Tools

This repository contains a collection of Python automation tools designed to simplify everyday tasks. Each tool is designed to be easy to use and requires minimal setup.

## Table of Contents

- [Shutdown Timer](#shutdown-timer)
- [YouTube Downloader](#youtube-downloader)
- [File Renaming Tool](#file-renaming-tool)
- [Notes Automator](#notes-automator)

## Shutdown Timer

A countdown timer application that automatically initiates system shutdown when the timer reaches zero. It uses a password-based security mechanism to prevent unauthorized timer cancellation.

### Features

- Configurable countdown timer with slider (1-120 minutes)
- Password protection with secure hashing for stopping the countdown
- Sound alerts during countdown
- Confirmation dialog before shutdown
- Automatic system shutdown when timer expires
- GUI built with Tkinter
- Settings stored in configuration file

### Requirements

- Python 3.x
- Tkinter (for GUI)
  ```bash
  pip install tk
  ```
- `winsound` module (included in Windows installations)

### Usage

1. Run the script:
   ```bash
   python auto_shutdown.py
   ```
2. Set desired time using the slider
3. Click "Start Timer" to begin countdown
4. To stop the timer, click the "Stop Timer" button and enter the correct password when prompted

## YouTube Downloader

A simple GUI application for downloading YouTube videos in the highest available resolution. This tool uses the `yt-dlp` library for efficient video downloads.

### Features

- Download videos in the best available quality
- Custom download directory selection
- Progress indicator during download
- URL validation to ensure valid YouTube links
- Simple and clean graphical user interface
- Centered window placement on the screen
- Success/error notification messages

### Requirements

- Python 3.x
- `yt-dlp` library
  ```bash
  pip install yt-dlp
  ```
- Tkinter (usually included with Python)

### Usage

1. Run the script:
   ```bash
   python youtube_downloader.py
   ```
2. Paste a valid YouTube video URL in the input field
3. Click the "Download" button
4. Select a destination folder when prompted
5. Monitor the download progress
6. Wait for the success message or check for error notifications

## File Renaming Tool

A utility script that renames all files in specified directories with random alphanumeric names while preserving file extensions. It handles name conflicts and provides detailed feedback.

### Features

- Renames files with randomly generated alphanumeric names
- Preserves original file extensions
- Configurable random name length
- Optional recursive mode to process subdirectories
- User confirmation before batch operations
- Prevents name conflicts by checking existing names
- Works with multiple directories simultaneously
- Provides detailed feedback and summary statistics

### Requirements

- Python 3.x
- No external libraries required (uses standard libraries only)

### Usage

```bash
python rename_random.py [folders...] [-l LENGTH] [-r] [-y]
```

Options:
- `folders`: Space-separated list of directories to process
- `-l, --length`: Length of generated random names (default: 8)
- `-r, --recursive`: Process subdirectories recursively
- `-y, --yes`: Skip confirmation prompts

If no folder paths are provided, the script will prompt for target folders.

### Example

```bash
# Basic usage
python rename_random.py "C:\Users\YourUsername\Documents"

# With options
python rename_random.py "C:\Users\YourUsername\Documents" -l 12 -r -y
```

## Notes Automator

A productivity tool that streamlines the creation of note files with specific extensions in organized folders. It's particularly useful for programmers who work with multiple languages.

### Features

- Creates notes with appropriate file extensions for different programming languages
- Automatically organizes files into specified folders
- File templates for common programming languages
- Opens the created note file in the default system editor
- Cross-platform support (Windows, macOS, Linux)
- Supports 16+ file types including programming languages and text formats

### Supported File Extensions

| Language/Type | Extension | Command Argument |
|---------------|-----------|-----------------|
| Ruby          | `.rb`     | `ruby`          |
| PHP           | `.php`    | `php`           |
| JavaScript    | `.js`     | `javascript`    |
| TypeScript    | `.ts`     | `typescript`    |
| Python        | `.py`     | `python`        |
| Java          | `.java`   | `java`          |
| Dart          | `.dart`   | `dart`          |
| Plain Text    | `.txt`    | `text`          |
| XML           | `.xml`    | `xml`           |
| HTML          | `.html`   | `html`          |
| CSS           | `.css`    | `css`           |
| JSON          | `.json`   | `json`          |
| C             | `.c`      | `c`             |
| C++           | `.cpp`    | `cpp`           |
| C#            | `.cs`     | `csharp`        |
| SQL           | `.sql`    | `sql`           |

### Requirements

- Python 3.x
- No external libraries required

### Usage

```bash
python notes.py -e EXTENSION -f FOLDER -n FILENAME [-t]
```

Where:
- `-e, --extension`: File extension/language (use language name from the table)
- `-f, --folder`: Folder name to store the note
- `-n, --name`: Name of the note file (without extension)
- `-t, --no-template`: Don't use language template (create empty file)

### Examples

```bash
# Create a Python note with template
python notes.py -e python -f my_notes -n todo_list

# Create a text note (empty file)
python notes.py -e text -f documents -n shopping_list -t
```

## License

This project is open source and available under the [MIT License](LICENSE).