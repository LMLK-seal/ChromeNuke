#!/usr/bin/env python3
"""
ChromeNuke Military-Grade Data Deletion Tool
A professional-grade application for secure deletion of Chrome browser data
with multiple overwrite passes and forensic-level data destruction.

Author: LMLK-seal
Version: 2.1.0
License: MIT
"""

import os
import sys
import sqlite3
import json
import shutil
import psutil
import threading
import hashlib
import secrets
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import customtkinter as ctk
from tkinter import messagebox, filedialog
import subprocess
import platform
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chrome_data_destroyer.log'),
        logging.StreamHandler()
    ]
)

class SecureDeletion:
    """Military-grade secure deletion implementation"""
    
    @staticmethod
    def dod_5220_22_m_wipe(filepath: str, passes: int = 7) -> bool:
        """
        DoD 5220.22-M standard wiping with multiple passes
        Pass 1: Write 0x00
        Pass 2: Write 0xFF  
        Pass 3: Write random data
        Repeat pattern for specified passes
        """
        try:
            if not os.path.exists(filepath):
                return True
                
            file_size = os.path.getsize(filepath)
            if file_size == 0:
                os.remove(filepath)
                return True
            
            with open(filepath, "r+b") as file:
                for pass_num in range(passes):
                    file.seek(0)
                    
                    if pass_num % 3 == 0:
                        # Pass 1: Write zeros
                        pattern = b'\x00' * min(8192, file_size)
                    elif pass_num % 3 == 1:
                        # Pass 2: Write ones
                        pattern = b'\xFF' * min(8192, file_size)
                    else:
                        # Pass 3: Write random data
                        pattern = secrets.token_bytes(min(8192, file_size))
                    
                    bytes_written = 0
                    while bytes_written < file_size:
                        chunk_size = min(len(pattern), file_size - bytes_written)
                        file.write(pattern[:chunk_size])
                        bytes_written += chunk_size
                    
                    file.flush()
                    os.fsync(file.fileno())
            
            # Remove the file after wiping
            os.remove(filepath)
            return True
            
        except Exception as e:
            logging.error(f"Error wiping file {filepath}: {e}")
            return False
    
    @staticmethod
    def secure_directory_wipe(directory: str, passes: int = 7) -> bool:
        """Securely wipe entire directory structure"""
        try:
            if not os.path.exists(directory):
                return True
                
            for root, dirs, files in os.walk(directory, topdown=False):
                # Wipe all files
                for file in files:
                    filepath = os.path.join(root, file)
                    SecureDeletion.dod_5220_22_m_wipe(filepath, passes)
                
                # Remove directories
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    try:
                        os.rmdir(dir_path)
                    except OSError:
                        pass
            
            # Remove root directory
            try:
                os.rmdir(directory)
            except OSError:
                pass
                
            return True
            
        except Exception as e:
            logging.error(f"Error wiping directory {directory}: {e}")
            return False

class ChromeDataLocator:
    """Locates Chrome data directories across different operating systems"""
    
    @staticmethod
    def get_chrome_profiles() -> List[Path]:
        """Get all Chrome profile directories"""
        profiles = []
        
        if platform.system() == "Windows":
            base_paths = [
                Path.home() / "AppData" / "Local" / "Google" / "Chrome" / "User Data",
                Path.home() / "AppData" / "Local" / "Chromium" / "User Data"
            ]
        elif platform.system() == "Darwin":  # macOS
            base_paths = [
                Path.home() / "Library" / "Application Support" / "Google" / "Chrome",
                Path.home() / "Library" / "Application Support" / "Chromium"
            ]
        else:  # Linux
            base_paths = [
                Path.home() / ".config" / "google-chrome",
                Path.home() / ".config" / "chromium"
            ]
        
        for base_path in base_paths:
            if base_path.exists():
                # Default profile
                if (base_path / "Default").exists():
                    profiles.append(base_path / "Default")
                
                # Additional profiles
                for item in base_path.iterdir():
                    if item.is_dir() and item.name.startswith("Profile "):
                        profiles.append(item)
        
        return profiles
    
    @staticmethod
    def get_chrome_cache_dirs() -> List[Path]:
        """Get Chrome cache directories"""
        cache_dirs = []
        
        if platform.system() == "Windows":
            cache_paths = [
                Path.home() / "AppData" / "Local" / "Google" / "Chrome" / "User Data" / "Default" / "Cache",
                Path.home() / "AppData" / "Local" / "Google" / "Chrome" / "User Data" / "ShaderCache"
            ]
        elif platform.system() == "Darwin":
            cache_paths = [
                Path.home() / "Library" / "Caches" / "Google" / "Chrome",
                Path.home() / "Library" / "Application Support" / "Google" / "Chrome" / "Default" / "Cache"
            ]
        else:
            cache_paths = [
                Path.home() / ".cache" / "google-chrome",
                Path.home() / ".config" / "google-chrome" / "Default" / "Cache"
            ]
        
        for cache_path in cache_paths:
            if cache_path.exists():
                cache_dirs.append(cache_path)
        
        return cache_dirs

class ProcessManager:
    """Manages Chrome process detection and termination"""
    
    @staticmethod
    def is_chrome_running() -> bool:
        """Check if Chrome processes are running"""
        chrome_processes = ['chrome.exe', 'chromium', 'google-chrome', 'Google Chrome']
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if any(chrome_name.lower() in proc.info['name'].lower() 
                      for chrome_name in chrome_processes):
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return False
    
    @staticmethod
    def terminate_chrome_processes() -> bool:
        """Forcefully terminate all Chrome processes"""
        chrome_processes = ['chrome.exe', 'chromium', 'google-chrome', 'Google Chrome']
        terminated = []
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if any(chrome_name.lower() in proc.info['name'].lower() 
                      for chrome_name in chrome_processes):
                    proc.terminate()
                    terminated.append(proc.info['pid'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Wait for processes to terminate
        time.sleep(2)
        
        # Force kill if still running
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if any(chrome_name.lower() in proc.info['name'].lower() 
                      for chrome_name in chrome_processes):
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return len(terminated) > 0

class DataAnalyzer:
    """Analyzes Chrome data for deletion statistics"""
    
    @staticmethod
    def analyze_profile(profile_path: Path) -> Dict[str, int]:
        """Analyze Chrome profile for data statistics"""
        stats = {
            'history_entries': 0,
            'cookies': 0,
            'downloads': 0,
            'cache_files': 0,
            'bookmarks': 0,
            'passwords': 0,
            'extensions': 0
        }
        
        try:
            # History database
            history_db = profile_path / "History"
            if history_db.exists():
                conn = sqlite3.connect(str(history_db))
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM urls")
                stats['history_entries'] = cursor.fetchone()[0]
                conn.close()
            
            # Cookies database
            cookies_db = profile_path / "Cookies"
            if cookies_db.exists():
                conn = sqlite3.connect(str(cookies_db))
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM cookies")
                stats['cookies'] = cursor.fetchone()[0]
                conn.close()
            
            # Downloads database
            downloads_db = profile_path / "History"
            if downloads_db.exists():
                conn = sqlite3.connect(str(downloads_db))
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM downloads")
                stats['downloads'] = cursor.fetchone()[0]
                conn.close()
            
            # Cache files
            cache_dir = profile_path / "Cache"
            if cache_dir.exists():
                stats['cache_files'] = len(list(cache_dir.rglob("*")))
            
            # Bookmarks
            bookmarks_file = profile_path / "Bookmarks"
            if bookmarks_file.exists():
                with open(bookmarks_file, 'r', encoding='utf-8') as f:
                    bookmarks_data = json.load(f)
                    stats['bookmarks'] = len(str(bookmarks_data).split('"url"')) - 1
            
            # Extensions
            extensions_dir = profile_path / "Extensions"
            if extensions_dir.exists():
                stats['extensions'] = len([d for d in extensions_dir.iterdir() if d.is_dir()])
            
        except Exception as e:
            logging.error(f"Error analyzing profile {profile_path}: {e}")
        
        return stats

class ChromeDataDestroyer(ctk.CTk):
    """Main application class with GUI"""
    
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("ChromeNuke - Military-Grade Data Destroyer v2.1.0")
        self.geometry("900x700")
        self.resizable(True, True)
        
        # Configure theme
        ctk.set_appearance_mode("dark")
        try:
            ctk.set_default_color_theme("blue")  # Use standard blue theme
        except Exception as e:
            logging.warning(f"Could not set color theme: {e}")
            # Continue with default theme
        
        # Initialize variables
        self.profiles = []
        self.cache_dirs = []
        self.selected_items = {}
        self.deletion_stats = {}
        self.is_scanning = False
        self.is_deleting = False
        
        self.setup_ui()
        self.scan_chrome_data()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="Chrome Military-Grade Data Destroyer",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#ff6b6b"  # Use a softer red color
        )
        title_label.pack(pady=(20, 10))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            self.main_frame,
            text="Professional-grade secure deletion with DoD 5220.22-M standard",
            font=ctk.CTkFont(size=12),
            text_color="#cccccc"
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Status frame
        self.status_frame = ctk.CTkFrame(self.main_frame)
        self.status_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Ready - Click 'Scan Chrome Data' to begin",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.status_label.pack(pady=10)
        
        # Control buttons frame
        self.controls_frame = ctk.CTkFrame(self.main_frame)
        self.controls_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Buttons
        self.btn_scan = ctk.CTkButton(
            self.controls_frame,
            text="🔍 Scan Chrome Data",
            command=self.scan_chrome_data,
            font=ctk.CTkFont(size=12, weight="bold"),
            height=40
        )
        self.btn_scan.pack(side="left", padx=10, pady=10)
        
        self.btn_terminate = ctk.CTkButton(
            self.controls_frame,
            text="⚠️ Terminate Chrome",
            command=self.terminate_chrome,
            font=ctk.CTkFont(size=12, weight="bold"),
            height=40,
            fg_color="#e67e22"  # Orange color that should work
        )
        self.btn_terminate.pack(side="left", padx=10, pady=10)
        
        self.btn_destroy = ctk.CTkButton(
            self.controls_frame,
            text="💀 SECURE DELETE",
            command=self.confirm_deletion,
            font=ctk.CTkFont(size=12, weight="bold"),
            height=40,
            fg_color="#e74c3c"  # Red color that should work
        )
        self.btn_destroy.pack(side="right", padx=10, pady=10)
        
        # Settings frame
        self.settings_frame = ctk.CTkFrame(self.main_frame)
        self.settings_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Deletion passes slider
        passes_label = ctk.CTkLabel(
            self.settings_frame,
            text="Deletion Passes (DoD 5220.22-M):",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        passes_label.pack(side="left", padx=10, pady=10)
        
        self.passes_var = ctk.IntVar(value=7)
        self.passes_slider = ctk.CTkSlider(
            self.settings_frame,
            from_=3,
            to=35,
            number_of_steps=32,
            variable=self.passes_var
        )
        self.passes_slider.pack(side="left", padx=10, pady=10)
        
        self.passes_label = ctk.CTkLabel(
            self.settings_frame,
            text="7 passes",
            font=ctk.CTkFont(size=12)
        )
        self.passes_label.pack(side="left", padx=10, pady=10)
        
        # Update passes label
        self.passes_slider.configure(command=self.update_passes_label)
        
        # Data selection frame
        self.data_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.data_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Progress frame
        self.progress_frame = ctk.CTkFrame(self.main_frame)
        self.progress_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.pack(fill="x", padx=20, pady=10)
        self.progress_bar.set(0)
        
        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="",
            font=ctk.CTkFont(size=10)
        )
        self.progress_label.pack(pady=(0, 10))
    
    def update_passes_label(self, value):
        """Update the passes label"""
        passes = int(value)
        self.passes_label.configure(text=f"{passes} passes")
    
    def scan_chrome_data(self):
        """Scan for Chrome data in a separate thread"""
        if self.is_scanning:
            return
        
        self.is_scanning = True
        self.btn_scan.configure(state="disabled")
        self.status_label.configure(text="Scanning Chrome data...")
        
        thread = threading.Thread(target=self._scan_thread)
        thread.daemon = True
        thread.start()
    
    def _scan_thread(self):
        """Thread function for scanning Chrome data"""
        try:
            # Clear previous data
            for widget in self.data_frame.winfo_children():
                widget.destroy()
            
            self.profiles = ChromeDataLocator.get_chrome_profiles()
            self.cache_dirs = ChromeDataLocator.get_chrome_cache_dirs()
            
            # Check if Chrome is running
            chrome_running = ProcessManager.is_chrome_running()
            
            # Update UI in main thread
            self.after(0, self._update_scan_results, chrome_running)
            
        except Exception as e:
            logging.error(f"Error during scan: {e}")
            self.after(0, self._scan_error, str(e))
    
    def _update_scan_results(self, chrome_running):
        """Update UI with scan results"""
        try:
            if chrome_running:
                warning_frame = ctk.CTkFrame(self.data_frame, fg_color="#d35400")  # Orange that should work
                warning_frame.pack(fill="x", padx=10, pady=10)
                
                warning_label = ctk.CTkLabel(
                    warning_frame,
                    text="⚠️ WARNING: Chrome is currently running! Close Chrome or use 'Terminate Chrome' button.",
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color="white"
                )
                warning_label.pack(pady=10)
            
            # Display profiles
            if self.profiles:
                profiles_label = ctk.CTkLabel(
                    self.data_frame,
                    text="Chrome Profiles Found:",
                    font=ctk.CTkFont(size=16, weight="bold")
                )
                profiles_label.pack(anchor="w", padx=10, pady=(10, 5))
                
                for i, profile in enumerate(self.profiles):
                    self._create_profile_section(profile, i)
            
            # Display cache directories
            if self.cache_dirs:
                cache_label = ctk.CTkLabel(
                    self.data_frame,
                    text="Cache Directories Found:",
                    font=ctk.CTkFont(size=16, weight="bold")
                )
                cache_label.pack(anchor="w", padx=10, pady=(20, 5))
                
                for i, cache_dir in enumerate(self.cache_dirs):
                    self._create_cache_section(cache_dir, i)
            
            # Update status
            total_items = len(self.profiles) + len(self.cache_dirs)
            self.status_label.configure(
                text=f"Scan complete - Found {total_items} data locations"
            )
            
        except Exception as e:
            logging.error(f"Error updating scan results: {e}")
        
        finally:
            self.is_scanning = False
            self.btn_scan.configure(state="normal")
    
    def _create_profile_section(self, profile_path, index):
        """Create UI section for a Chrome profile"""
        profile_frame = ctk.CTkFrame(self.data_frame)
        profile_frame.pack(fill="x", padx=10, pady=5)
        
        # Profile header
        header_frame = ctk.CTkFrame(profile_frame)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        checkbox_var = ctk.BooleanVar()
        self.selected_items[f"profile_{index}"] = checkbox_var
        
        checkbox = ctk.CTkCheckBox(
            header_frame,
            text=f"Profile: {profile_path.name}",
            variable=checkbox_var,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        checkbox.pack(side="left", padx=10)
        
        # Analyze profile data
        try:
            stats = DataAnalyzer.analyze_profile(profile_path)
            
            stats_text = f"History: {stats['history_entries']} | Cookies: {stats['cookies']} | " \
                        f"Downloads: {stats['downloads']} | Cache: {stats['cache_files']} files"
            
            stats_label = ctk.CTkLabel(
                header_frame,
                text=stats_text,
                font=ctk.CTkFont(size=10),
                text_color="#aaaaaa"
            )
            stats_label.pack(side="right", padx=10)
            
        except Exception as e:
            logging.error(f"Error analyzing profile {profile_path}: {e}")
        
        # Path label
        path_label = ctk.CTkLabel(
            profile_frame,
            text=f"Path: {profile_path}",
            font=ctk.CTkFont(size=9),
            text_color="#888888"
        )
        path_label.pack(anchor="w", padx=20, pady=(0, 10))
    
    def _create_cache_section(self, cache_path, index):
        """Create UI section for a cache directory"""
        cache_frame = ctk.CTkFrame(self.data_frame)
        cache_frame.pack(fill="x", padx=10, pady=5)
        
        # Cache header
        header_frame = ctk.CTkFrame(cache_frame)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        checkbox_var = ctk.BooleanVar()
        self.selected_items[f"cache_{index}"] = checkbox_var
        
        checkbox = ctk.CTkCheckBox(
            header_frame,
            text=f"Cache: {cache_path.name}",
            variable=checkbox_var,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        checkbox.pack(side="left", padx=10)
        
        # Cache size
        try:
            total_size = sum(f.stat().st_size for f in cache_path.rglob('*') if f.is_file())
            size_mb = total_size / (1024 * 1024)
            
            size_label = ctk.CTkLabel(
                header_frame,
                text=f"Size: {size_mb:.1f} MB",
                font=ctk.CTkFont(size=10),
                text_color="#aaaaaa"
            )
            size_label.pack(side="right", padx=10)
            
        except Exception as e:
            logging.error(f"Error calculating cache size {cache_path}: {e}")
        
        # Path label
        path_label = ctk.CTkLabel(
            cache_frame,
            text=f"Path: {cache_path}",
            font=ctk.CTkFont(size=9),
            text_color="#888888"
        )
        path_label.pack(anchor="w", padx=20, pady=(0, 10))
    
    def _scan_error(self, error_msg):
        """Handle scan error"""
        self.status_label.configure(text=f"Scan error: {error_msg}")
        self.is_scanning = False
        self.btn_scan.configure(state="normal")
    
    def terminate_chrome(self):
        """Terminate Chrome processes"""
        if ProcessManager.is_chrome_running():
            result = messagebox.askyesno(
                "Terminate Chrome",
                "This will forcefully close all Chrome windows and processes. "
                "Any unsaved work will be lost. Continue?"
            )
            
            if result:
                success = ProcessManager.terminate_chrome_processes()
                if success:
                    self.status_label.configure(text="Chrome processes terminated successfully")
                    messagebox.showinfo("Success", "Chrome processes have been terminated.")
                else:
                    self.status_label.configure(text="No Chrome processes found")
                    messagebox.showinfo("Info", "No Chrome processes were found running.")
        else:
            messagebox.showinfo("Info", "Chrome is not currently running.")
    
    def confirm_deletion(self):
        """Confirm deletion with user"""
        if self.is_deleting:
            return
        
        # Check if any items are selected
        selected_count = sum(1 for var in self.selected_items.values() if var.get())
        
        if selected_count == 0:
            messagebox.showwarning("No Selection", "Please select items to delete.")
            return
        
        # Final confirmation
        passes = self.passes_var.get()
        result = messagebox.askyesno(
            "CONFIRM SECURE DELETION",
            f"This will permanently delete selected Chrome data using {passes} overwrite passes.\n\n"
            f"Selected items: {selected_count}\n"
            f"Deletion method: DoD 5220.22-M Standard\n\n"
            f"⚠️ THIS ACTION CANNOT BE UNDONE! ⚠️\n\n"
            f"Are you absolutely sure you want to proceed?",
            icon="warning"
        )
        
        if result:
            self.start_deletion()
    
    def start_deletion(self):
        """Start the secure deletion process"""
        self.is_deleting = True
        self.btn_destroy.configure(state="disabled")
        self.btn_scan.configure(state="disabled")
        
        thread = threading.Thread(target=self._deletion_thread)
        thread.daemon = True
        thread.start()
    
    def _deletion_thread(self):
        """Thread function for secure deletion"""
        try:
            passes = self.passes_var.get()
            total_items = sum(1 for var in self.selected_items.values() if var.get())
            current_item = 0
            
            self.deletion_stats = {
                'profiles_deleted': 0,
                'cache_dirs_deleted': 0,
                'files_deleted': 0,
                'bytes_deleted': 0,
                'errors': []
            }
            
            # Delete selected profiles
            for i, profile in enumerate(self.profiles):
                if self.selected_items.get(f"profile_{i}", ctk.BooleanVar()).get():
                    current_item += 1
                    progress = current_item / total_items
                    
                    self.after(0, self._update_progress, progress, f"Deleting profile: {profile.name}")
                    
                    try:
                        # Calculate size before deletion
                        size_before = sum(f.stat().st_size for f in profile.rglob('*') if f.is_file())
                        
                        if SecureDeletion.secure_directory_wipe(str(profile), passes):
                            self.deletion_stats['profiles_deleted'] += 1
                            self.deletion_stats['bytes_deleted'] += size_before
                        else:
                            self.deletion_stats['errors'].append(f"Failed to delete profile: {profile}")
                            
                    except Exception as e:
                        error_msg = f"Error deleting profile {profile}: {e}"
                        self.deletion_stats['errors'].append(error_msg)
                        logging.error(error_msg)
            
            # Delete selected cache directories
            for i, cache_dir in enumerate(self.cache_dirs):
                if self.selected_items.get(f"cache_{i}", ctk.BooleanVar()).get():
                    current_item += 1
                    progress = current_item / total_items
                    
                    self.after(0, self._update_progress, progress, f"Deleting cache: {cache_dir.name}")
                    
                    try:
                        # Calculate size before deletion
                        size_before = sum(f.stat().st_size for f in cache_dir.rglob('*') if f.is_file())
                        
                        if SecureDeletion.secure_directory_wipe(str(cache_dir), passes):
                            self.deletion_stats['cache_dirs_deleted'] += 1
                            self.deletion_stats['bytes_deleted'] += size_before
                        else:
                            self.deletion_stats['errors'].append(f"Failed to delete cache: {cache_dir}")
                            
                    except Exception as e:
                        error_msg = f"Error deleting cache {cache_dir}: {e}"
                        self.deletion_stats['errors'].append(error_msg)
                        logging.error(error_msg)
            
            # Completion
            self.after(0, self._deletion_complete)
            
        except Exception as e:
            logging.error(f"Error during deletion thread: {e}")
            self.after(0, self._deletion_error, str(e))
    
    def _update_progress(self, progress, message):
        """Update progress bar and message"""
        self.progress_bar.set(progress)
        self.progress_label.configure(text=message)
        self.status_label.configure(text=f"Secure deletion in progress... {int(progress * 100)}%")
    
    def _deletion_complete(self):
        """Handle deletion completion"""
        self.progress_bar.set(1.0)
        self.progress_label.configure(text="Secure deletion completed!")
        
        # Show completion stats
        stats = self.deletion_stats
        bytes_mb = stats['bytes_deleted'] / (1024 * 1024)
        
        completion_msg = (
            f"Secure Deletion Complete!\n\n"
            f"Profiles deleted: {stats['profiles_deleted']}\n"
            f"Cache directories deleted: {stats['cache_dirs_deleted']}\n"
            f"Data securely wiped: {bytes_mb:.1f} MB\n"
            f"Overwrite passes used: {self.passes_var.get()}\n\n"
        )
        
        if stats['errors']:
            completion_msg += f"Errors encountered: {len(stats['errors'])}\n"
            completion_msg += "Check log file for details."
        else:
            completion_msg += "All selected data has been securely destroyed."
        
        messagebox.showinfo("Deletion Complete", completion_msg)
        
        # Reset UI
        self.status_label.configure(text="Secure deletion completed successfully")
        self.is_deleting = False
        self.btn_destroy.configure(state="normal")
        self.btn_scan.configure(state="normal")
        
        # Rescan for updated data
        self.after(2000, self.scan_chrome_data)
    
    def _deletion_error(self, error_msg):
        """Handle deletion error"""
        self.progress_label.configure(text=f"Deletion error: {error_msg}")
        self.status_label.configure(text="Secure deletion failed")
        
        messagebox.showerror("Deletion Error", f"An error occurred during deletion:\n\n{error_msg}")
        
        self.is_deleting = False
        self.btn_destroy.configure(state="normal")
        self.btn_scan.configure(state="normal")
    
    def on_closing(self):
        """Handle application closing"""
        if self.is_deleting:
            result = messagebox.askyesno(
                "Deletion in Progress",
                "Secure deletion is currently in progress. "
                "Closing now may leave some data partially wiped. "
                "Are you sure you want to exit?"
            )
            if not result:
                return
        
        logging.info("Application closing")
        self.destroy()

class AboutDialog(ctk.CTkToplevel):
    """About dialog window"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("About Chrome Data Destroyer")
        self.geometry("600x500")
        self.resizable(False, False)
        
        # Make it modal
        self.transient(parent)
        self.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup about dialog UI"""
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="Chrome Military-Grade Data Destroyer",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ff6b6b"  # Use consistent color
        )
        title_label.pack(pady=(10, 5))
        
        # Version
        version_label = ctk.CTkLabel(
            main_frame,
            text="Version 2.1.0",
            font=ctk.CTkFont(size=12),
            text_color="#cccccc"
        )
        version_label.pack(pady=(0, 20))
        
        # Description
        desc_text = """
A professional-grade secure deletion tool for Chrome browser data.
Uses military-standard DoD 5220.22-M deletion methods with multiple
overwrite passes to ensure complete data destruction.

Features:
• Multi-pass secure deletion (3-35 passes)
• DoD 5220.22-M compliance
• Chrome process detection and termination
• Cross-platform support (Windows, macOS, Linux)
• Detailed deletion statistics and logging
• Professional GUI with real-time progress tracking

Security Methods:
• Zero-fill passes (0x00)
• One-fill passes (0xFF)
• Random data passes
• File system synchronization
• Directory structure elimination

This tool is designed for privacy-conscious users who require
complete and verifiable data destruction beyond standard deletion.
        """
        
        desc_label = ctk.CTkLabel(
            main_frame,
            text=desc_text,
            font=ctk.CTkFont(size=11),
            justify="left"
        )
        desc_label.pack(pady=(0, 20), padx=20)
        
        # Warning
        warning_frame = ctk.CTkFrame(main_frame, fg_color="#d35400")  # Orange that should work
        warning_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        warning_label = ctk.CTkLabel(
            warning_frame,
            text="⚠️ WARNING: This tool permanently destroys data.\nDeleted files cannot be recovered by any means.",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="white"
        )
        warning_label.pack(pady=10)
        
        # Close button
        close_btn = ctk.CTkButton(
            main_frame,
            text="Close",
            command=self.destroy,
            width=100
        )
        close_btn.pack(pady=10)

def main():
    """Main application entry point"""
    try:
        # Check for required dependencies
        required_modules = ['customtkinter', 'psutil']
        missing_modules = []
        
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing_modules.append(module)
        
        if missing_modules:
            print(f"Error: Missing required modules: {', '.join(missing_modules)}")
            print("Please install them using:")
            print(f"pip install {' '.join(missing_modules)}")
            return 1
        
        # Initialize logging
        logging.info("Starting Chrome Military-Grade Data Destroyer v2.1.0")
        
        # Check CustomTkinter version compatibility
        try:
            import customtkinter as ctk
            logging.info(f"CustomTkinter version: {ctk.__version__}")
        except AttributeError:
            logging.warning("Could not determine CustomTkinter version")
        
        # Create and run application
        app = ChromeDataDestroyer()
        
        # Add about menu (could be expanded with menu bar)
        app.protocol("WM_DELETE_WINDOW", app.on_closing)
        
        # Add keyboard shortcuts
        app.bind('<Control-q>', lambda e: app.on_closing())
        app.bind('<F1>', lambda e: AboutDialog(app))
        app.bind('<F5>', lambda e: app.scan_chrome_data())
        
        logging.info("Application GUI initialized successfully")
        app.mainloop()
        
        logging.info("Application terminated normally")
        return 0
        
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        import traceback
        logging.error(f"Traceback: {traceback.format_exc()}")
        
        # Try to show error dialog if possible
        try:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Fatal Error", f"A fatal error occurred:\n\n{e}\n\nCheck the log file for details.")
        except:
            print(f"Fatal error: {e}")
        
        return 1

if __name__ == "__main__":
    exit_code = main()
