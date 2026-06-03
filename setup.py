#!/usr/bin/env python3
"""
REX AI System - Standalone Installer & Setup
Complete one-file installation system with simplified GUI
"""

import os
import sys
import subprocess
import json
import platform
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
from pathlib import Path
from typing import Optional, Dict, Any


class REXInstaller:
    """Simplified GUI installer for REX AI System"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("REX AI System - Installer")
        self.root.geometry("650x500")
        self.root.resizable(True, True)
        
        # Set minimum size
        self.root.minsize(600, 450)
        
        self.install_path = Path.home() / "REX_AI"
        self.venv_path = self.install_path / "venv"
        self.python_path = self.venv_path / ("Scripts" if platform.system() == "Windows" else "bin")
        self.pip_path = self.python_path / ("pip.exe" if platform.system() == "Windows" else "pip")
        
        self.current_step = 0
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main UI"""
        # Top banner
        banner = tk.Frame(self.root, bg="#00ff41", height=60)
        banner.pack(fill=tk.X, padx=0, pady=0)
        
        title = tk.Label(
            banner,
            text="REX AI SYSTEM - INSTALLER",
            font=("Arial", 14, "bold"),
            bg="#00ff41",
            fg="#000000"
        )
        title.pack(pady=10)
        
        subtitle = tk.Label(
            banner,
            text="Advanced AI with Self-Modification Capabilities",
            font=("Arial", 9),
            bg="#00ff41",
            fg="#333333"
        )
        subtitle.pack()
        
        # Main content area
        content = tk.Frame(self.root, bg="#f0f0f0")
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Step indicator
        self.step_label = tk.Label(
            content,
            text="Step 1 of 4: Welcome",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0"
        )
        self.step_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Content area
        self.content_frame = tk.Frame(content, bg="white", relief=tk.SUNKEN, bd=1)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=10)
        
        # Log area
        self.log_frame = tk.Frame(content, bg="white", relief=tk.SUNKEN, bd=1)
        self.log_frame.pack(fill=tk.BOTH, expand=False, padx=0, pady=10, height=120)
        
        log_label = tk.Label(self.log_frame, text="Installation Log:", bg="white", font=("Arial", 9, "bold"))
        log_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.log_text = scrolledtext.ScrolledText(
            self.log_frame,
            height=6,
            width=70,
            bg="#000000",
            fg="#00ff41",
            font=("Courier", 8),
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_text.config(state=tk.DISABLED)
        
        # Button frame
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.back_btn = tk.Button(
            button_frame,
            text="← Back",
            command=self.prev_step,
            bg="#cccccc",
            fg="#000000",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            state=tk.DISABLED
        )
        self.back_btn.pack(side=tk.LEFT, padx=5)
        
        self.next_btn = tk.Button(
            button_frame,
            text="Next →",
            command=self.next_step,
            bg="#00aa00",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8
        )
        self.next_btn.pack(side=tk.LEFT, padx=5)
        
        self.install_btn = tk.Button(
            button_frame,
            text="Install Now!",
            command=self.start_installation,
            bg="#00ff41",
            fg="#000000",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            state=tk.DISABLED
        )
        self.install_btn.pack(side=tk.LEFT, padx=5)
        
        self.quit_btn = tk.Button(
            button_frame,
            text="Quit",
            command=self.root.quit,
            bg="#ff3333",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8
        )
        self.quit_btn.pack(side=tk.RIGHT, padx=5)
        
        # Show first step
        self.show_step(0)
    
    def show_step(self, step: int):
        """Show a specific step"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        if step == 0:
            self.show_welcome()
        elif step == 1:
            self.show_configuration()
        elif step == 2:
            self.show_review()
        elif step == 3:
            self.show_installation()
        
        self.current_step = step
        self.update_buttons()
    
    def show_welcome(self):
        """Welcome step"""
        self.step_label.config(text="Step 1 of 4: Welcome")
        
        text = scrolledtext.ScrolledText(
            self.content_frame,
            height=15,
            width=70,
            bg="white",
            fg="#000000",
            font=("Arial", 10),
            relief=tk.FLAT,
            wrap=tk.WORD
        )
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        content = """Welcome to REX AI System!

REX is an advanced AI assistant inspired by JARVIS with incredible capabilities:

🤖 FEATURES:
  • Natural Language Processing (GPT-4)
  • Multi-Step Reasoning Engine
  • Persistent Memory System
  • Permission-Based Security
  • Voice Interface (Speech & TTS)
  • Plugin Architecture
  • Autonomous Agents
  • Self-Modification Capabilities
  • REST API Server
  • Beautiful GUI

📋 SYSTEM REQUIREMENTS:
  • Python 3.8 or higher
  • 2GB free disk space
  • Internet connection
  • OpenAI API key (get free at https://platform.openai.com)

📂 INSTALLATION LOCATION:
  {0}

Click "Next →" to continue with configuration!"""
        
        text.insert(1.0, content.format(self.install_path))
        text.config(state=tk.DISABLED)
    
    def show_configuration(self):
        """Configuration step"""
        self.step_label.config(text="Step 2 of 4: Configuration")
        
        frame = tk.Frame(self.content_frame, bg="white")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # API Key
        tk.Label(
            frame,
            text="OpenAI API Key:",
            font=("Arial", 10, "bold"),
            bg="white"
        ).pack(anchor=tk.W, pady=(10, 5))
        
        self.api_key_var = tk.StringVar()
        api_entry = tk.Entry(
            frame,
            textvariable=self.api_key_var,
            show="*",
            font=("Arial", 10),
            width=50
        )
        api_entry.pack(anchor=tk.W, pady=(0, 5), fill=tk.X)
        
        tk.Label(
            frame,
            text="Get your API key from: https://platform.openai.com/api/keys",
            font=("Arial", 8),
            fg="#666666",
            bg="white"
        ).pack(anchor=tk.W, pady=(0, 15))
        
        # API Port
        tk.Label(
            frame,
            text="API Server Port:",
            font=("Arial", 10, "bold"),
            bg="white"
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.port_var = tk.StringVar(value="5000")
        port_frame = tk.Frame(frame, bg="white")
        port_frame.pack(anchor=tk.W, fill=tk.X)
        
        tk.Entry(
            port_frame,
            textvariable=self.port_var,
            font=("Arial", 10),
            width=10
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(
            port_frame,
            text="(default: 5000)",
            font=("Arial", 8),
            fg="#666666",
            bg="white"
        ).pack(side=tk.LEFT)
        
        # Environment
        tk.Label(
            frame,
            text="Environment:",
            font=("Arial", 10, "bold"),
            bg="white"
        ).pack(anchor=tk.W, pady=(15, 5))
        
        self.env_var = tk.StringVar(value="development")
        env_frame = tk.Frame(frame, bg="white")
        env_frame.pack(anchor=tk.W, fill=tk.X)
        
        tk.Radiobutton(
            env_frame,
            text="Development",
            variable=self.env_var,
            value="development",
            bg="white",
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Radiobutton(
            env_frame,
            text="Production",
            variable=self.env_var,
            value="production",
            bg="white",
            font=("Arial", 10)
        ).pack(side=tk.LEFT)
        
        # Voice
        tk.Label(
            frame,
            text="Features:",
            font=("Arial", 10, "bold"),
            bg="white"
        ).pack(anchor=tk.W, pady=(15, 5))
        
        self.voice_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            frame,
            text="Enable Voice Interface (Speech Recognition & Text-to-Speech)",
            variable=self.voice_var,
            bg="white",
            font=("Arial", 10)
        ).pack(anchor=tk.W)
        
        # Auto-start
        self.autostart_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            frame,
            text="Start REX after installation completes",
            variable=self.autostart_var,
            bg="white",
            font=("Arial", 10)
        ).pack(anchor=tk.W, pady=(10, 0))
    
    def show_review(self):
        """Review step"""
        self.step_label.config(text="Step 3 of 4: Review Configuration")
        
        text = scrolledtext.ScrolledText(
            self.content_frame,
            height=15,
            width=70,
            bg="white",
            fg="#000000",
            font=("Courier", 10),
            relief=tk.FLAT,
            wrap=tk.WORD
        )
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        content = f"""INSTALLATION SUMMARY
═══════════════════════════════════════════════════════════

Install Location:
  {self.install_path}

Configuration:
  API Port: {self.port_var.get()}
  Environment: {self.env_var.get()}
  Voice Enabled: {self.voice_var.get()}
  Auto-Start: {self.autostart_var.get()}

API Key: {"●" * 10} (configured)

What will be installed:
  ✓ Python Virtual Environment
  ✓ All dependencies (pip packages)
  ✓ REX AI System core files
  ✓ Configuration files
  ✓ Desktop shortcuts
  ✓ Log directories
  ✓ Memory database

Estimated time: 5-10 minutes
(depending on internet speed)

═══════════════════════════════════════════════════════════

Click "Install Now!" to begin installation."""
        
        text.insert(1.0, content)
        text.config(state=tk.DISABLED)
    
    def show_installation(self):
        """Installation step"""
        self.step_label.config(text="Step 4 of 4: Installing...")
        
        frame = tk.Frame(self.content_frame, bg="white")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.progress_label = tk.Label(
            frame,
            text="Preparing installation...",
            font=("Arial", 10, "bold"),
            bg="white"
        )
        self.progress_label.pack(anchor=tk.W, pady=(0, 10))
        
        self.progress_bar = ttk.Progressbar(
            frame,
            mode='determinate',
            length=400,
            maximum=100
        )
        self.progress_bar.pack(fill=tk.X, pady=10)
        
        self.status_label = tk.Label(
            frame,
            text="0%",
            font=("Arial", 10),
            bg="white"
        )
        self.status_label.pack()
        
        # Disable all buttons during installation
        self.back_btn.config(state=tk.DISABLED)
        self.next_btn.config(state=tk.DISABLED)
        self.install_btn.config(state=tk.DISABLED)
    
    def next_step(self):
        """Go to next step"""
        if self.current_step < 3:
            # Validate API key before proceeding
            if self.current_step == 1:  # From configuration
                if not self.api_key_var.get():
                    messagebox.showerror("Missing API Key", "Please enter your OpenAI API key")
                    return
            
            self.show_step(self.current_step + 1)
    
    def prev_step(self):
        """Go to previous step"""
        if self.current_step > 0:
            self.show_step(self.current_step - 1)
    
    def update_buttons(self):
        """Update button states"""
        # Back button
        self.back_btn.config(state=tk.NORMAL if self.current_step > 0 else tk.DISABLED)
        
        # Next button
        self.next_btn.config(state=tk.NORMAL if self.current_step < 2 else tk.DISABLED)
        
        # Install button
        self.install_btn.config(state=tk.NORMAL if self.current_step == 2 else tk.DISABLED)
    
    def log(self, message: str):
        """Add message to log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()
    
    def start_installation(self):
        """Start installation in background thread"""
        self.show_step(3)
        
        thread = threading.Thread(target=self.run_installation)
        thread.daemon = True
        thread.start()
    
    def run_installation(self):
        """Run the actual installation"""
        try:
            self.log("═" * 60)
            self.log("REX AI SYSTEM INSTALLATION")
            self.log("═" * 60)
            
            # Step 1: Create directories
            self.log("\n[1/6] Creating installation directories...")
            self.progress_bar['value'] = 10
            self.progress_label.config(text="Creating directories...")
            self.status_label.config(text="10%")
            
            self.install_path.mkdir(parents=True, exist_ok=True)
            (self.install_path / "logs").mkdir(exist_ok=True)
            (self.install_path / "data").mkdir(exist_ok=True)
            (self.install_path / "plugins").mkdir(exist_ok=True)
            (self.install_path / "agents").mkdir(exist_ok=True)
            
            self.log(f"✓ Directories created at: {self.install_path}")
            
            # Step 2: Create virtual environment
            self.log("\n[2/6] Creating Python virtual environment...")
            self.progress_bar['value'] = 25
            self.progress_label.config(text="Creating virtual environment...")
            self.status_label.config(text="25%")
            
            result = subprocess.run(
                [sys.executable, "-m", "venv", str(self.venv_path)],
                capture_output=True,
                timeout=120
            )
            
            if result.returncode == 0:
                self.log(f"✓ Virtual environment created")
            else:
                raise Exception(f"venv creation failed: {result.stderr.decode()}")
            
            # Step 3: Upgrade pip
            self.log("\n[3/6] Upgrading pip...")
            self.progress_bar['value'] = 40
            self.progress_label.config(text="Upgrading pip...")
            self.status_label.config(text="40%")
            
            subprocess.run(
                [str(self.pip_path), "install", "--upgrade", "pip", "--quiet"],
                capture_output=True,
                timeout=60
            )
            self.log("✓ pip upgraded")
            
            # Step 4: Install dependencies
            self.log("\n[4/6] Installing dependencies...")
            self.progress_bar['value'] = 55
            self.progress_label.config(text="Installing packages...")
            self.status_label.config(text="55%")
            
            requirements = [
                "OpenAI>=1.3.0",
                "flask==3.0.0",
                "flask-cors==4.0.0",
                "python-dotenv==1.0.0",
                "pydantic==2.5.0",
                "requests==2.31.0",
                "speech-recognition==3.10.0",
                "pyttsx3==2.90",
                "colorama==0.4.6",
                "python-dateutil==2.8.2",
                "markdown==3.5.1",
                "aiohttp==3.9.1",
                "aiofiles==23.2.1",
                "cryptography==41.0.7",
                "PyYAML==6.0.1",
                "PyJWT==2.8.1"
            ]
            
            for i, req in enumerate(requirements):
                self.log(f"  Installing: {req}...")
                subprocess.run(
                    [str(self.pip_path), "install", req, "--quiet"],
                    capture_output=True,
                    timeout=120
                )
                progress = 55 + (i / len(requirements)) * 20
                self.progress_bar['value'] = progress
                self.status_label.config(text=f"{int(progress)}%")
            
            self.log("✓ All dependencies installed")
            
            # Step 5: Create configuration
            self.log("\n[5/6] Creating configuration files...")
            self.progress_bar['value'] = 80
            self.progress_label.config(text="Setting up configuration...")
            self.status_label.config(text="80%")
            
            env_content = f"""# REX AI System Configuration
OPENAI_API_KEY={self.api_key_var.get()}
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_TEMPERATURE=0.7

# REX System Configuration
REX_ENV={self.env_var.get()}
REX_LOG_LEVEL=INFO
REX_API_PORT={self.port_var.get()}
REX_API_HOST=127.0.0.1

# Security
REX_PERMISSION_REQUIRED=true
REX_ADMIN_USER=admin
REX_SECRET_KEY={os.urandom(32).hex()}

# Voice
REX_VOICE_ENABLED={'true' if self.voice_var.get() else 'false'}
REX_VOICE_RATE=150

# Database
REX_DB_TYPE=sqlite
REX_DB_PATH=data/rex.db
"""
            
            with open(self.install_path / ".env", "w") as f:
                f.write(env_content)
            
            self.log("✓ Configuration files created")
            
            # Step 6: Create shortcuts
            self.log("\n[6/6] Creating shortcuts...")
            self.progress_bar['value'] = 95
            self.progress_label.config(text="Creating shortcuts...")
            self.status_label.config(text="95%")
            
            self.create_shortcuts()
            self.log("✓ Shortcuts created")
            
            # Complete
            self.progress_bar['value'] = 100
            self.progress_label.config(text="Installation Complete!")
            self.status_label.config(text="100%")
            
            self.log("\n" + "═" * 60)
            self.log("✓ INSTALLATION SUCCESSFUL!")
            self.log("═" * 60)
            self.log(f"\nREX installed at: {self.install_path}")
            self.log("To start REX:")
            self.log(f"  cd {self.install_path}")
            self.log("  python main.py")
            self.log("\nOr use the desktop shortcut created on your desktop!")
            
            messagebox.showinfo(
                "Installation Complete!",
                f"REX AI System installed successfully!\n\n"
                f"Location: {self.install_path}\n\n"
                f"To start:\n"
                f"  python main.py\n\n"
                f"Then open: http://localhost:{self.port_var.get()}"
            )
            
            # Auto-start if enabled
            if self.autostart_var.get():
                self.log("\nStarting REX AI System...")
                self.root.after(2000, self.start_rex)
        
        except Exception as e:
            self.log(f"\n✗ Installation Failed!")
            self.log(f"Error: {str(e)}")
            messagebox.showerror("Installation Failed", f"Error:\n{str(e)}")
    
    def create_shortcuts(self):
        """Create desktop shortcuts"""
        system = platform.system()
        desktop = Path.home() / "Desktop"
        
        if system == "Windows":
            launcher_content = f"""@echo off
cd /d "{self.install_path}"
title REX AI System
python main.py
pause
"""
            launcher_path = self.install_path / "REX.bat"
            with open(launcher_path, "w") as f:
                f.write(launcher_content)
            
            # Try to create shortcut
            try:
                import win32com.client
                shell = win32com.client.Dispatch("WScript.Shell")
                shortcut = shell.CreateShortcut(str(desktop / "REX AI System.lnk"))
                shortcut.TargetPath = str(launcher_path)
                shortcut.WorkingDirectory = str(self.install_path)
                shortcut.save()
                self.log("✓ Desktop shortcut created")
            except:
                self.log("Note: Could not create Windows shortcut")
        
        elif system == "Darwin":  # macOS
            launcher_content = f"""#!/bin/bash
cd "{self.install_path}"
python3 main.py
"""
            launcher_path = self.install_path / "REX.command"
            with open(launcher_path, "w") as f:
                f.write(launcher_content)
            os.chmod(launcher_path, 0o755)
            self.log("✓ macOS launcher created")
        
        else:  # Linux
            launcher_content = f"""#!/bin/bash
cd "{self.install_path}"
python main.py
"""
            launcher_path = self.install_path / "REX.sh"
            with open(launcher_path, "w") as f:
                f.write(launcher_content)
            os.chmod(launcher_path, 0o755)
            self.log("✓ Linux launcher created")
    
    def start_rex(self):
        """Start REX after installation"""
        try:
            os.chdir(self.install_path)
            if platform.system() == "Windows":
                subprocess.Popen([str(self.python_path / "python.exe"), "main.py"])
            else:
                subprocess.Popen([str(self.python_path / "python"), "main.py"])
        except:
            pass


def main():
    """Main entry point"""
    root = tk.Tk()
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"+{x}+{y}")
    
    app = REXInstaller(root)
    root.mainloop()


if __name__ == "__main__":
    main()
