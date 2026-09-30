# Python Automation Tools

A collection of small Python utilities for everyday tasks. Most programs use
[Flet](https://flet.dev/) for their graphical interface; `notes.py` is a
command-line tool.

## Requirements

- Python 3.13 or a version compatible with the installed dependencies;
- `pip`;
- Flet 1.0 or newer for the graphical applications;
- FFmpeg is optional for merging video and audio streams in the YouTube
  downloader;
- A RapidAPI key for the jobs search tool.

External dependencies are listed in
[requirements.txt](requirements.txt):

```powershell
pip install -r requirements.txt
```

`threading`, `hashlib`, `configparser`, `os`, `argparse`, and `difflib` are
part of Python's standard library and do not need to be installed with `pip`.

To upgrade already-installed packages to the newest versions allowed by the
requirements, run:

```powershell
python -m pip install --upgrade -r requirements.txt
```

The `>=` constraints intentionally allow newer compatible releases, but
`pip install -r requirements.txt` does not upgrade a package that is already
installed. The command above does. GitHub Dependabot is also configured to
open weekly update pull requests for the dependencies.

## Tools

### `auto_shutdown.py` — shutdown timer

A Flet application that starts a countdown and shuts down the computer when
the countdown ends. Press **Stop Timer** to cancel the countdown and any
scheduled shutdown immediately; no password is required. The program uses
`shutdown_config.ini` to store the default time and shutdown settings.

```powershell
python auto_shutdown.py
```

The interface accepts values between 1 and 120 minutes. The shutdown
operation depends on the operating system and should be used carefully,
because it may interrupt unsaved work.

When the countdown reaches zero, the application asks for confirmation before
starting the system shutdown. If a shutdown has already been scheduled, use
**Stop Timer** to cancel it.

### `youtube_downloader.py` — YouTube downloader

Downloads videos using `pytubefix`. The application attempts to use adaptive
streams up to 1080p and merge them with audio when FFmpeg is available.
Without FFmpeg, it is limited to the available progressive streams.

```powershell
python youtube_downloader.py
```

By default, files are saved to:

```text
C:\Users\<user>\Downloads\Youtube Videos
```

The program allows you to select another directory through the interface.
Use it only for content you are authorized to download and in accordance
with the service's terms of use.

### `image_to_pdf.py` — images to PDF

Converts multiple images into a single PDF. It accepts `JPG`, `JPEG`, `PNG`,
`BMP`, and `GIF`, and allows you to choose the output filename.

```powershell
python image_to_pdf.py
```

The default output directory is:

```text
C:\Users\<user>\Downloads\Image to PDF Files
```

### `photo_compressor.py` — photo compressor

Compresses a single image or all images in a folder. It accepts `JPG`,
`JPEG`, `PNG`, `BMP`, and `GIF`, allows you to choose a quality value between
1% and 100%, and saves the results as JPEG files with the `_compressed`
suffix.

```powershell
python photo_compressor.py
```

The default output directory is:

```text
C:\Users\<user>\Downloads\Compressed Photos
```

### `internet_speed_test.py` — speed test

Measures download, upload, and ping using `speedtest-cli`, and displays the
ISP and selected server.

```powershell
python internet_speed_test.py
```

An Internet connection is required. Results may vary depending on the
selected server and network conditions.

### `linkedin_jobs.py` — jobs search

Queries the JSearch API through RapidAPI and searches for remote and
on-site jobs. The country is determined from the name entered in the
interface.

```powershell
python linkedin_jobs.py
```

A valid RapidAPI key for the JSearch endpoint is required. The key should be
provided through an environment variable or a secure configuration mechanism;
do not publish API keys in source code.

Results are written to `.txt` files in:

```text
C:\Users\<user>\Downloads\LinkedIn Jobs
```

### `rename_random.py` — file renamer

Renames files in a folder with random 8-character alphanumeric names while
preserving their extensions. It can also process subfolders.

```powershell
python rename_random.py
```

By default, the interface starts with the current user's `Pictures` folder,
but another folder can be selected. This operation changes file names and
does not provide an undo function; create a backup before running it.

### `notes.py` — note creator

A command-line tool that creates a folder and a file with the extension
corresponding to the selected type. On Windows, macOS, and Linux, it attempts
to open the file in the system's default editor.

Syntax:

```powershell
python notes.py -e EXTENSION -f FOLDER -n NAME [-t]
```

Options:

- `-e, --extension`: file type;
- `-f, --folder`: folder where the file will be created;
- `-n, --name`: filename without the extension;
- `-t, --no-template`: create an empty file instead of using a template.

Available types:

```text
ruby, php, javascript, typescript, python, java, dart, text,
xml, html, css, json, c, cpp, csharp, sql
```

Examples:

```powershell
python notes.py -e python -f projects -n todo_app
python notes.py -e text -f documents -n notes -t
```

Templates are available for Python, HTML, JavaScript, and Java. Other
formats are created empty when no template is defined.

## Known limitations

- Programs with graphical interfaces use several Windows-specific default
  paths, such as `C:\Users\<user>\Downloads`. Compatibility with macOS and
  Linux is not guaranteed for every tool.
- Output directories are created automatically when needed.
- Graphical interfaces run time-consuming operations in threads to avoid
  blocking the window, but performance depends on the system, network, and
  files being processed.
- The JSearch API and content downloads depend on external services that may
  change or become unavailable.

## Main structure

```text
auto_shutdown.py          Shutdown timer
youtube_downloader.py     YouTube downloader
image_to_pdf.py           Image-to-PDF converter
photo_compressor.py       Image compressor
internet_speed_test.py    Speed test
linkedin_jobs.py          Jobs search
plagiarism_checker.py     Text comparison
rename_random.py          File renamer
notes.py                  CLI note creator
shutdown_config.ini       Shutdown timer configuration
requirements.txt          External dependencies
```

## Development

Python and pytest caches are ignored by
[.gitignore](.gitignore). Run the programs using the same Python environment
where the dependencies were installed.
