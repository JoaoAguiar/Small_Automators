import yt_dlp
from tkinter import *
from tkinter import messagebox, filedialog
import re
import os

def is_valid_youtube_url(url):
    # Basic YouTube URL validation
    youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?\s]{11})'
    return re.match(youtube_regex, url) is not None

def download_video(url):
    if not is_valid_youtube_url(url):
        messagebox.showerror("Error", "Please enter a valid YouTube URL")
        return
        
    try:
        # Ask user to select download directory
        download_dir = filedialog.askdirectory(title="Select Download Directory")
        if not download_dir:
            return  # User canceled directory selection
            
        # Update status
        status_label.config(text="Downloading... Please wait")
        root.update()
        
        # Set options for yt-dlp
        ydl_opts = {
            'format': 'best',  # Download the best quality
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
        }

        # Initialize yt-dlp object with options
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        status_label.config(text="")
        messagebox.showinfo("Success", "Video Downloaded Successfully!")

    except Exception as e:
        status_label.config(text="")
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def progress_hook(d):
    if d['status'] == 'downloading':
        status_label.config(text=f"Downloading: {d.get('_percent_str', '0%')}")
        root.update()

def Widgets_GUI():
    # URL entry
    Label(root, text="YouTube URL:", font="Arial 10").place(relx=0.5, rely=0.2, anchor=CENTER)
    root.linkText = Entry(root, width=40, textvariable=link, font="Arial 12")
    root.linkText.place(relx=0.5, rely=0.3, anchor=CENTER)

    # Download button
    downloader_button = Button(root, text="Download", 
                              command=lambda: download_video(link.get()), 
                              width=10, height=1, relief=GROOVE, 
                              font="Arial 13", bg="white", fg="black")
    downloader_button.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Status label
    global status_label
    status_label = Label(root, text="", font="Arial 10")
    status_label.place(relx=0.5, rely=0.7, anchor=CENTER)

# Set up the main window
root = Tk()
root.geometry("500x200")  # Larger window size
root.resizable(False, False)
root.title("YouTube Downloader")

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the position to center the window
position_top = int(screen_height / 2 - 200 / 2)  # 200 is the window height
position_left = int(screen_width / 2 - 500 / 2)  # 500 is the window width

# Set the window geometry (width x height + X + Y)
root.geometry(f"500x200+{position_left}+{position_top}")

link = StringVar()
status_label = None  # Will be initialized in Widgets_GUI

Widgets_GUI()

root.mainloop()