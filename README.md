# Python Automation Tools

This repository contains a collection of Python automation tools designed to simplify everyday tasks. Each tool is designed to be easy to use and requires minimal setup.

## Installation

To install all required dependencies, run:

```bash
pip install -r requirements.txt
```

## Table of Contents

- [Installation](#installation)
- [Shutdown Timer](#shutdown-timer)
- [YouTube Downloader](#youtube-downloader)
- [Image to PDF Converter](#image-to-pdf-converter)
- [Photo Compressor](#photo-compressor)
- [Internet Speed Test](#internet-speed-test)
- [LinkedIn Jobs Scraper](#linkedin-jobs-scraper)
- [Plagiarism Checker](#plagiarism-checker)
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

## Image to PDF Converter

A simple tool that converts multiple image files (JPG, JPEG, PNG) into a single PDF document. The tool provides a file dialog to select multiple images at once.

### Features

- Supports JPG, JPEG, and PNG image formats
- Combines multiple images into a single PDF
- Interactive file selection dialog
- Automatic page creation for each image
- Configurable image positioning and sizing

### Requirements

- Python 3.x
- fpdf2 library

### Usage

1. Run the script:
   ```bash
   python image_to_pdf.py
   ```
2. Select the images you want to convert using the file dialog
3. The PDF will be created as "image_to_pdf_result.pdf" in the same directory

## Photo Compressor

A basic image compression tool that reduces the file size of images by adjusting the quality settings. This is useful for reducing storage space or preparing images for web use.

### Features

- Compresses images to reduce file size
- Adjustable quality settings
- Supports various image formats
- Interactive file selection
- Optimized JPEG output

### Requirements

- Python 3.x
- Pillow (PIL) library

### Usage

1. Run the script:
   ```bash
   python photo_compressor.py
   ```
2. Select an image file using the file dialog
3. The compressed image will be saved as "photo_compressor_result.jpg"

## Internet Speed Test

A command-line tool that measures your internet connection speed, including download speed, upload speed, and ping. It automatically selects the best server for testing.

### Features

- Measures download and upload speeds
- Tests ping latency
- Automatically selects optimal test server
- Displays ISP information
- Shows server location

### Requirements

- Python 3.x
- speedtest-cli library

### Usage

```bash
python internet_speed_test.py
```

The tool will automatically run the speed test and display the results.

## LinkedIn Jobs Scraper

A job search automation tool that searches for job postings using the JSearch API. It can search for both remote and on-site positions across multiple countries.

### Features

- Searches for jobs by title and country
- Supports multiple countries with automatic country code detection
- Finds both remote and on-site positions
- Filters for full-time, part-time, and internship positions
- Saves results to a text file
- Removes duplicate job postings

### Requirements

- Python 3.x
- requests library
- Valid RapidAPI key for JSearch API

### Usage

1. Update the API key in the script with your RapidAPI key
2. Run the script:
   ```bash
   python linkedin_jobs.py
   ```
3. Enter the job title and country when prompted
4. Results will be saved to "linkedin_jobs_result.txt"

## Plagiarism Checker

A text similarity analyzer that compares two text files and calculates their similarity percentage. This tool is useful for detecting potential plagiarism or duplicate content.

### Features

- Compares two text files for similarity
- Calculates similarity percentage
- Interactive file selection
- Handles text encoding errors gracefully
- Uses SequenceMatcher for accurate comparison

### Requirements

- Python 3.x
- No external libraries required (uses difflib from standard library)

### Usage

1. Run the script:
   ```bash
   python plagiarism_checker.py
   ```
2. Select the first file using the file dialog
3. Select the second file using the file dialog
4. The similarity percentage will be displayed

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