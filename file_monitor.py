# file_monitor.py
import time
import sys
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

PATH_TO_WATCH = "/media/pi/89F6-78B8"

class MyEventHandler(FileSystemEventHandler):
    """Logs all file system events."""
    def on_moved(self, event):
        print(f"Moved: {event.src_path} to {event.dest_path}")

    def on_created(self, event):
        print(f"Created: {event.src_path}")

    def on_deleted(self, event):
        print(f"Deleted: {event.src_path}")

    def on_modified(self, event):
        # Ignore directory modifications which often happen automatically
        if not event.is_directory:
            print(f"Modified: {event.src_path}")

if __name__ == "__main__":
    print("--- File Monitor Script ---")

    # Check if the path exists and is a directory
    if not os.path.isdir(PATH_TO_WATCH):
        print(f"Error: Path '{PATH_TO_WATCH}' does not exist or is not a directory.")
        print("Please plug in your USB drive and update the PATH_TO_WATCH variable in the script.")
        sys.exit(1) # Exit the script

    print(f"Starting to monitor directory: {PATH_TO_WATCH}")
    event_handler = MyEventHandler()
    observer = Observer()
    observer.schedule(event_handler, PATH_TO_WATCH, recursive=True)
    observer.start()
    print("Monitoring active. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping observer...")
        observer.stop()
        print("Observer stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")
        observer.stop()

    observer.join()
    print("Script finished.")
