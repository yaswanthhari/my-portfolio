import time
import shutil
import yaml
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from logger_config import setup_logger

class FileOrganizerHandler(FileSystemEventHandler):
    """Handles file events and organizes them automatically"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.watch_dir = Path(config['watch_directory']).expanduser()
        self.rules = config['organize_by']
        self.ignore = config['ignore_files']
        
    def on_created(self, event):
        """Triggered when a new file is created"""
        if event.is_directory:
            return
            
        file_path = Path(event.src_path)
        self.organize_file(file_path)
    
    def on_modified(self, event):
        """Triggered when file is modified"""
        if not event.is_directory:
            file_path = Path(event.src_path)
            self.logger.info(f"File modified: {file_path.name}")
            # Optional: re-organize if needed
            # self.organize_file(file_path)
    
    def get_destination_folder(self, file_extension: str) -> str:
        """Determine which folder the file belongs to"""
        for folder, extensions in self.rules.items():
            if file_extension.lower() in extensions:
                return folder
        return "Others"
    
    def organize_file(self, file_path: Path):
        """Move file to appropriate folder"""
        try:
            # Skip if file should be ignored
            if file_path.name in self.ignore:
                self.logger.debug(f"Ignored file: {file_path.name}")
                return
            
            # Skip if file is being written (wait for complete)
            time.sleep(0.5)
            if not file_path.exists():
                return
            
            # Determine destination
            ext = file_path.suffix
            dest_folder = self.get_destination_folder(ext)
            dest_path = self.watch_dir / dest_folder
            
            # Create destination folder if needed
            dest_path.mkdir(exist_ok=True)
            
            # Handle duplicate filenames
            dest_file = dest_path / file_path.name
            counter = 1
            while dest_file.exists():
                dest_file = dest_path / f"{file_path.stem}_{counter}{file_path.suffix}"
                counter += 1
            
            # Move file
            shutil.move(str(file_path), str(dest_file))
            self.logger.info(f"Organized: {file_path.name} -> {dest_folder}/{dest_file.name}")
            
        except Exception as e:
            self.logger.error(f"Failed to organize {file_path.name}: {str(e)}")

def start_monitoring():
    """Start the real-time file monitoring system"""
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Setup logger
    logger = setup_logger('FileOrganizer', 'logs/organizer.log')
    logger.info("Starting File Organizer")
    
    # Setup watchdog
    watch_path = Path(config['watch_directory']).expanduser()
    
    # Ensure watch directory exists
    watch_path.mkdir(parents=True, exist_ok=True)
    
    event_handler = FileOrganizerHandler(config, logger)
    observer = Observer()
    observer.schedule(event_handler, str(watch_path), recursive=False)
    
    logger.info(f"Monitoring: {watch_path}")
    logger.info("Press Ctrl+C to stop")
    
    try:
        observer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        observer.stop()
    
    observer.join()
    logger.info("File Organizer stopped")

if __name__ == "__main__":
    start_monitoring()
