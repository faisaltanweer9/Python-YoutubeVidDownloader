import os
import sys
import subprocess
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

def update_yt_dlp():
    """Updates yt-dlp to the latest version."""
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'yt-dlp'], check=True)
        print("✅ yt-dlp updated successfully.")
    except Exception as e:
        print(f"⚠️ Failed to update yt-dlp: {e}")

def get_download_folder():
    """Gets the download folder path from the user."""
    folder = input("Enter the folder path for downloads (default: current directory): ").strip()
    return folder if folder else os.getcwd()

def get_video_link():
    """Gets the YouTube link from the user."""
    return input("Enter YouTube Video/Playlist Link: ").strip()

def choose_quality():
    """Lets the user select the video quality."""
    print("\nSelect Video Quality:")
    print("1. Best Quality (default)")
    print("2. 720p (HD)")
    print("3. 480p (SD)")
    print("4. 144p (Lowest quality)")
    print("5. MP3 (Audio only)")
    choice = input("Enter your choice (1/2/3/4/5): ").strip()

    quality_map = {
        '1': 'bestvideo+bestaudio/best',
        '2': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        '3': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
        '4': 'bestvideo[height<=144]+bestaudio/best[height<=144]',
        '5': 'bestaudio/best'
    }
    return quality_map.get(choice, 'bestvideo+bestaudio/best')

def choose_range():
    """Lets the user decide if they want full playlist or specific videos."""
    choice = input("\nDo you want to download the full playlist? (y/n): ").strip().lower()
    if choice == 'n':
        print("👉 Enter video numbers or ranges (e.g., '1-3' or '2,4,6').")
        return input("Enter range: ").strip()
    return None

def download_video(url, output_path, format_option, playlist_range=None):
    """Downloads the video(s) using yt-dlp with the specified options."""

    # If playlist detected, include numbering in filename
    if playlist_range:
        out_template = os.path.join(output_path, '%(playlist_index)s - %(title)s.%(ext)s')
    else:
        out_template = os.path.join(output_path, '%(title)s.%(ext)s')

    ydl_opts = {
        'format': format_option,
        'outtmpl': out_template,
        'merge_output_format': 'mp4',
        'progress_hooks': [download_progress],
        'cookiefile': 'cookies.txt',
    }

    if playlist_range:
        ydl_opts['playlist_items'] = playlist_range

    print(f"\nStarting download for: {url}")
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("\n✅ Download completed successfully.")
    except DownloadError as e:
        error_msg = f"❌ Error downloading with yt-dlp: {e}"
        print(error_msg)
        with open("error_log.txt", "a", encoding="utf-8") as log:
            log.write(f"{error_msg}\n")
        print("⚠️ Error details saved in error_log.txt.")

def download_progress(d):
    """A hook to display download progress."""
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '').strip()
        speed = d.get('_speed_str', '').strip()
        eta = d.get('_eta_str', '').strip()
        print(f"\rDownloading: {percent} | Speed: {speed} | ETA: {eta}", end="")
    elif d['status'] == 'finished':
        print(f"\n✔️ Download finished: {d['filename']}")

def main():
    """Main function to run the downloader."""
    update_yt_dlp()
    output_path = get_download_folder()
    url = get_video_link()
    format_option = choose_quality()

    # Detect playlist via "list=" parameter in URL
    playlist_range = None
    if "list=" in url.lower():
        playlist_range = choose_range()

    download_video(url, output_path, format_option, playlist_range)

if __name__ == '__main__':
    main()
