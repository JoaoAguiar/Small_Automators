# Python Automation Tools

This repository contains a collection of Python automation tools with **modern Flet-based GUIs** designed to simplify everyday tasks. Each tool features a beautiful, responsive interface built with Google's Material Design principles through the Flet framework.

## Installation

To install all required dependencies, run:

```bash
pip install -r requirements.txt
```

**Main Requirements:**
- Python 3.8+
- Flet 0.21.0+ (Modern GUI framework)
- Additional libraries as specified in requirements.txt

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

A modern countdown timer application with Material Design interface that automatically initiates system shutdown when the timer reaches zero. Features password-based security and real-time countdown display.

### Key Features

- **Modern Flet GUI** with Material Design elements
- Configurable countdown timer with slider (1-120 minutes)
- **Real-time countdown display** with color-coded progress
- Password protection with secure SHA-256 hashing
- **Automatic shutdown confirmation** dialog
- Threaded countdown to prevent UI freezing
- Settings stored in `shutdown_config.ini`
- **Responsive design** with centered layout and shadows

### Requirements

- Python 3.8+
- Flet framework
- Built-in modules: `os`, `time`, `threading`, `hashlib`, `configparser`

### Usage

1. Run the script:
   ```bash
   python auto_shutdown.py
   ```
2. Set desired time using the intuitive slider interface
3. Click "Start Timer" to begin countdown with visual feedback
4. To stop: click "Stop Timer" and enter password (default: "pass")
5. **New**: Visual countdown with color transitions (green → orange → red)

### Configuration

- Password and default timer settings stored in `shutdown_config.ini`
- Default password: "pass" (can be modified in config file)
- Customizable default countdown time

## YouTube Downloader

A modern GUI application for downloading YouTube videos with adaptive quality selection and FFmpeg integration. Built with Flet for a responsive, Material Design interface.

### Key Features

- **Modern Flet interface** with Material Design elements
- Downloads videos in maximum available quality (up to 1080p with FFmpeg)
- **FFmpeg detection and integration** for adaptive stream merging
- **Progress tracking** with real-time download status
- Custom download directory selection
- **Threaded downloads** to prevent UI freezing
- URL validation and video info display
- **Responsive design** with clean, centered layout

### Requirements

- Python 3.8+
- Flet framework
- `pytubefix` library
- FFmpeg (optional, for maximum quality up to 1080p)

### Usage

1. Run the script:
   ```bash
   python youtube_downloader.py
   ```
2. Paste a valid YouTube video URL
3. Click "Info" to view video details and available streams
4. Click "Download Video" and monitor progress
5. Videos saved to Downloads/Youtube Videos (or custom location)

### Notes

- FFmpeg status indicator shows availability (green checkmark)
- With FFmpeg: Downloads up to 1080p using adaptive streams
- Without FFmpeg: Limited to progressive streams (typically 720p)

## Image to PDF Converter

A streamlined tool for converting multiple image files into a single PDF document with an intuitive Flet-based interface.

### Key Features

- **Modern Flet GUI** with drag-and-drop feel
- **Multiple image selection** at once
- Supports JPG, JPEG, and PNG formats
- **Automatic page sizing** and positioning
- Real-time conversion feedback
- **Material Design** file selection dialogs

### Requirements

- Python 3.8+
- Flet framework
- fpdf2 library

### Usage

1. Run the script:
   ```bash
   python image_to_pdf.py
   ```
2. Click "Browse Files" to select multiple images
3. Click "Convert to PDF" to process
4. PDF saved as "image_to_pdf_result.pdf"

## Photo Compressor

A powerful image compression tool with quality controls and batch processing capabilities, featuring a modern Flet interface.

### Key Features

- **Modern Flet GUI** with intuitive controls
- **Quality slider** for precise compression control (1-100%)
- **File and folder selection** options
- **Batch processing** with progress tracking
- **Multiple format support** (JPG, JPEG, PNG, BMP, GIF)
- **Threaded compression** for responsive UI
- **Automatic RGB conversion** for optimal output
- **Real-time progress updates** and statistics

### Requirements

- Python 3.8+
- Flet framework
- Pillow (PIL) library

### Usage

1. Run the script:
   ```bash
   python photo_compressor.py
   ```
2. Select single image or entire folder
3. Adjust quality using the slider
4. Click "Compress" and monitor progress
5. Compressed images saved to dedicated output folder

### Output

- Default location: `C:\Users\jpagu\Downloads\Compressed Photos`
- Files saved with "_compressed" suffix
- All images converted to JPEG format

## Internet Speed Test

A clean, modern internet speed testing tool with real-time results display built using Flet's responsive interface.

### Key Features

- **Modern Flet interface** with live results
- **Real-time speed measurement** display
- Download, upload, and ping testing
- **Automatic server selection** for optimal testing
- **ISP and server information** display
- **Responsive design** with progress indicators

### Requirements

- Python 3.8+
- Flet framework
- speedtest-cli library

### Usage

1. Run the script:
   ```bash
   python internet_speed_test.py
   ```
2. Click "Start Test" to begin speed measurement
3. View real-time results for download/upload speeds
4. Results include ping, ISP info, and server location

## LinkedIn Jobs Scraper

An automated job search tool with modern interface for finding remote and on-site positions using the JSearch API.

### Key Features

- **Modern Flet GUI** with search controls
- **Multi-country job search** with auto-detection
- **Remote and on-site position filtering**
- **Multiple employment types** (full-time, part-time, internships)
- **Duplicate removal** and result organization
- **Real-time search progress** and status updates
- **Export functionality** to text files

### Requirements

- Python 3.8+
- Flet framework
- requests library
- Valid RapidAPI key for JSearch API

### Usage

1. Update API key in script
2. Run the script:
   ```bash
   python linkedin_jobs.py
   ```
3. Enter job title and select country
4. Click "Search Jobs" and monitor progress
5. Results saved to "linkedin_jobs_result.txt"

### Configuration

- Requires RapidAPI key for JSearch API
- Supports multiple countries with automatic code detection
- Configurable search parameters and filters

## Plagiarism Checker

A text similarity analyzer with modern interface for comparing documents and detecting potential plagiarism.

### Key Features

- **Modern Flet interface** for file selection
- **Dual file comparison** with similarity percentage
- **SequenceMatcher algorithm** for accurate analysis
- **Encoding error handling** for various text formats
- **Real-time analysis** with progress feedback
- **Clear results display** with percentage breakdown

### Requirements

- Python 3.8+
- Flet framework
- Built-in difflib module

### Usage

1. Run the script:
   ```bash
   python plagiarism_checker.py
   ```
2. Select first file using "Browse" button
3. Select second file for comparison
4. Click "Check Similarity" to analyze
5. View similarity percentage and analysis

## File Renaming Tool

A utility for bulk file renaming with random alphanumeric names, featuring a clean Flet interface with safety features.

### Key Features

- **Modern Flet GUI** with intuitive controls
- **Random name generation** (fixed 8-character length)
- **Extension preservation** for all file types
- **Recursive folder processing** option
- **Collision prevention** with duplicate checking
- **Real-time file counting** and preview
- **Threaded operations** for responsive UI
- **Default folder setup** (C:\Users\jpagu\Pictures)

### Requirements

- Python 3.8+
- Flet framework
- Built-in modules: `os`, `random`, `string`, `threading`

### Usage

1. Run the script:
   ```bash
   python rename_random.py
   ```
2. Select target folder (defaults to Pictures)
3. Enable recursive processing if needed
4. Click "Rename Files" to process
5. All files renamed with 8-character random names

### Safety Features

- **File count preview** before operation
- **Extension preservation** to maintain file types
- **Collision detection** to prevent overwrites
- **Progress feedback** during batch operations

## Notes Automator

A productivity tool for creating organized note files with language-specific templates and automatic folder organization.

### Core Features

- **File template system** for 16+ programming languages
- **Automatic folder organization** and creation
- **Cross-platform editor integration** (Windows, macOS, Linux)
- **Command-line interface** with flexible options
- **Language-specific extensions** and templates

### Supported Languages

| Language/Type | Extension | Command |
|---------------|-----------|---------|
| Ruby          | `.rb`     | `ruby`  |
| PHP           | `.php`    | `php`   |
| JavaScript    | `.js`     | `javascript` |
| TypeScript    | `.ts`     | `typescript` |
| Python        | `.py`     | `python` |
| Java          | `.java`   | `java`  |
| Dart          | `.dart`   | `dart`  |
| Plain Text    | `.txt`    | `text`  |
| XML           | `.xml`    | `xml`   |
| HTML          | `.html`   | `html`  |
| CSS           | `.css`    | `css`   |
| JSON          | `.json`   | `json`  |
| C             | `.c`      | `c`     |
| C++           | `.cpp`    | `cpp`   |
| C#            | `.cs`     | `csharp` |
| SQL           | `.sql`    | `sql`   |

### Requirements

- Python 3.8+
- No external dependencies required

### Usage

```bash
python notes.py -e EXTENSION -f FOLDER -n FILENAME [-t]
```

Options:
- `-e, --extension`: Language/file type from supported list
- `-f, --folder`: Organization folder name
- `-n, --name`: Note filename (without extension)
- `-t, --no-template`: Create empty file (skip template)

### Examples

```bash
# Create Python note with template
python notes.py -e python -f projects -n todo_app

# Create empty text file
python notes.py -e text -f documents -n notes -t
```

---

## Technology Stack

All applications in this repository utilize:

- **Frontend**: Flet (Python) with Material Design
- **Architecture**: Threaded operations for responsive UI
- **File Operations**: Built-in Python libraries
- **Configuration**: INI files and local storage
- **Cross-Platform**: Windows, macOS, Linux support