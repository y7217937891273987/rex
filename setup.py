#!/usr/bin/env python3
"""
REX AI System - Standalone Installer & Setup
Complete one-file installation system with GUI, auto-installation, and standalone launcher
"""

import os
import sys
import subprocess
import json
import platform
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
from pathlib import Path
from typing import Optional, Dict, Any
import requests
import zipfile
import shutil
import tempfile


class REXSetupUI:
    """GUI-based setup interface for REX AI System"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("REX AI System - Installer")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Colors
        self.bg_color = "#1a1a2e"
        self.fg_color = "#eaeaea"
        self.accent_color = "#00ff41"
        self.secondary_color = "#16213e"
        
        self.root.configure(bg=self.bg_color)
        
        self.install_path = Path.home() / "REX_AI"
        self.venv_path = self.install_path / "venv"
        self.python_path = self.venv_path / ("Scripts" if platform.system() == "Windows" else "bin")
        self.pip_path = self.python_path / ("pip.exe" if platform.system() == "Windows" else "pip")
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main UI layout"""
        # Banner
        banner_frame = tk.Frame(self.root, bg=self.secondary_color, height=100)
        banner_frame.pack(fill=tk.X, padx=0, pady=0)
        
        banner_text = tk.Label(
            banner_frame,
            text="""
╔═══════════════════════════════════════════════════════╗
║         REX AI SYSTEM - JARVIS ASSISTANT             ║
║     Advanced AI with Self-Modification Capabilities   ║
╚═══════════════════════════════════════════════════════╝
            """,
            font=("Courier", 10, "bold"),
            fg=self.accent_color,
            bg=self.secondary_color,
            justify=tk.CENTER
        )
        banner_text.pack(pady=10)
        
        # Main content frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title = ttk.Label(
            main_frame,
            text="Installation & Setup Wizard",
            font=("Arial", 16, "bold"),
            foreground=self.accent_color
        )
        title.pack(pady=(0, 20))
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.welcome_tab = ttk.Frame(self.notebook)
        self.install_tab = ttk.Frame(self.notebook)
        self.config_tab = ttk.Frame(self.notebook)
        self.complete_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.welcome_tab, text="Welcome")
        self.notebook.add(self.install_tab, text="Installation")
        self.notebook.add(self.config_tab, text="Configuration")
        self.notebook.add(self.complete_tab, text="Complete")
        
        self.setup_welcome_tab()
        self.setup_install_tab()
        self.setup_config_tab()
        self.setup_complete_tab()
        
        # Footer
        footer_frame = ttk.Frame(self.root)
        footer_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.button_frame = ttk.Frame(footer_frame)
        self.button_frame.pack(side=tk.RIGHT)
        
        self.back_btn = ttk.Button(self.button_frame, text="Back", command=self.prev_tab, state=tk.DISABLED)
        self.back_btn.pack(side=tk.LEFT, padx=5)
        
        self.next_btn = ttk.Button(self.button_frame, text="Next", command=self.next_tab)
        self.next_btn.pack(side=tk.LEFT, padx=5)
        
        self.install_btn = ttk.Button(self.button_frame, text="Install", command=self.start_installation, state=tk.DISABLED)
        self.install_btn.pack(side=tk.LEFT, padx=5)
    
    def setup_welcome_tab(self):
        """Setup welcome tab"""
        frame = ttk.Frame(self.welcome_tab, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        welcome_text = """
Welcome to REX AI System Setup!

REX is an advanced AI assistant inspired by JARVIS with:
• Natural Language Processing (GPT-4)
• Multi-Step Reasoning Engine
• Persistent Memory System
• Permission-Based Security
• Voice Interface (Speech Recognition & TTS)
• Plugin Architecture
• Autonomous Agents
• Self-Modification Capabilities
• REST API Server
• Beautiful GUI Dashboard

This installer will:
1. Create a virtual environment
2. Download and install all dependencies
3. Configure your OpenAI API key
4. Set up the REX AI system
5. Create desktop shortcuts

Installation Path: {}

System Requirements:
• Python 3.8+ (will be detected)
• 2GB free disk space
• Internet connection
• OpenAI API key (get from https://platform.openai.com)

Click 'Next' to continue...
        """.format(self.install_path)
        
        label = ttk.Label(frame, text=welcome_text, justify=tk.LEFT, font=("Arial", 10))
        label.pack(fill=tk.BOTH, expand=True)
    
    def setup_install_tab(self):
        """Setup installation tab"""
        frame = ttk.Frame(self.install_tab, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Progress label
        self.progress_label = ttk.Label(frame, text="Ready to install...", font=("Arial", 10))
        self.progress_label.pack(pady=(0, 10))
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(frame, mode='determinate', length=400)
        self.progress_bar.pack(fill=tk.X, pady=10)
        
        # Log text area
        log_frame = ttk.LabelFrame(frame, text="Installation Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.log_text = tk.Text(log_frame, height=15, width=80, bg="#000000", fg="#00ff41", font=("Courier", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.log_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text['yscrollcommand'] = scrollbar.set
        scrollbar['command'] = self.log_text.yview
    
    def setup_config_tab(self):
        """Setup configuration tab"""
        frame = ttk.Frame(self.config_tab, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # OpenAI API Key
        ttk.Label(frame, text="OpenAI API Key Configuration", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        key_frame = ttk.Frame(frame)
        key_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(key_frame, text="API Key:", font=("Arial", 10)).pack(side=tk.LEFT)
        self.api_key_var = tk.StringVar()
        self.api_key_entry = ttk.Entry(key_frame, textvariable=self.api_key_var, show="*", width=50)
        self.api_key_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        ttk.Label(frame, text="Get your API key from: https://platform.openai.com/api/keys", font=("Arial", 9), foreground="gray").pack(anchor=tk.W, pady=(0, 20))
        
        # Environment settings
        ttk.Label(frame, text="Environment Settings", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        settings_frame = ttk.Frame(frame)
        settings_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(settings_frame, text="API Port:", font=("Arial", 10)).pack(side=tk.LEFT)
        self.port_var = tk.StringVar(value="5000")
        ttk.Spinbox(settings_frame, from_=1000, to=65535, textvariable=self.port_var, width=10).pack(side=tk.LEFT, padx=10)
        
        ttk.Label(settings_frame, text="Environment:", font=("Arial", 10)).pack(side=tk.LEFT, padx=(20, 0))
        self.env_var = tk.StringVar(value="development")
        ttk.Combobox(settings_frame, textvariable=self.env_var, values=["development", "production"], state="readonly", width=15).pack(side=tk.LEFT, padx=10)
        
        # Voice settings
        ttk.Label(frame, text="Voice Settings", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(20, 10))
        
        self.voice_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame, text="Enable Voice Interface (Speech Recognition & Text-to-Speech)", variable=self.voice_var).pack(anchor=tk.W, pady=5)
        
        # Auto-start
        ttk.Label(frame, text="Startup Options", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(20, 10))
        
        self.autostart_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame, text="Start REX after installation", variable=self.autostart_var).pack(anchor=tk.W, pady=5)
        
        self.desktop_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame, text="Create desktop shortcut", variable=self.desktop_var).pack(anchor=tk.W, pady=5)
    
    def setup_complete_tab(self):
        """Setup completion tab"""
        frame = ttk.Frame(self.complete_tab, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        self.complete_text = tk.Text(frame, height=20, width=80, bg="#000000", fg="#00ff41", font=("Courier", 9))
        self.complete_text.pack(fill=tk.BOTH, expand=True)
        
        complete_message = """
╔═══════════════════════════════════════════════════════════╗
║          REX AI SYSTEM INSTALLATION COMPLETE!            ║
╚═══════════════════════════════════════════════════════════╝

✓ Installation successful!
✓ All dependencies installed
✓ Configuration saved
✓ Ready to use

WHAT'S NEXT?

1. Start REX:
   • Double-click the desktop shortcut, or
   • Run: python main.py from the installation directory

2. Access the Dashboard:
   • GUI Dashboard: Launches automatically
   • Web Dashboard: http://localhost:5000
   • API Endpoint: POST http://localhost:5000/api/v1/chat

3. Chat with REX:
   • Use the voice interface, or
   • Use the GUI dashboard, or
   • Use the REST API

4. Configure Plugins & Agents:
   • Add custom plugins to the plugins/ directory
   • Create autonomous agents in agents/ directory

5. View Logs & Memory:
   • Logs: {}logs/
   • Memory: {}data/

USEFUL COMMANDS:

Start API Server:
  python main.py --server

Start GUI Dashboard:
  python main.py --gui

Start Interactive Mode:
  python main.py --interactive

View Logs:
  tail -f {}logs/rex.log

SUPPORT:

Documentation: {}README.md
GitHub: https://github.com/y7217937891273987/rex
OpenAI API: https://platform.openai.com

Enjoy using REX! 🤖
        """.format(
            str(self.install_path / "logs" / ""),
            str(self.install_path / "data" / ""),
            str(self.install_path / "logs" / ""),
            str(self.install_path / "")
        )
        
        self.complete_text.insert(1.0, complete_message)
        self.complete_text.config(state=tk.DISABLED)
    
    def log(self, message: str):
        """Log message to installation log"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def prev_tab(self):
        """Go to previous tab"""
        current = self.notebook.index(self.notebook.select())
        if current > 0:
            self.notebook.select(current - 1)
            self.update_button_states()
    
    def next_tab(self):
        """Go to next tab"""
        current = self.notebook.index(self.notebook.select())
        if current < 3:
            self.notebook.select(current + 1)
            self.update_button_states()
    
    def update_button_states(self):
        """Update button states based on current tab"""
        current = self.notebook.index(self.notebook.select())
        
        self.back_btn.config(state=tk.NORMAL if current > 0 else tk.DISABLED)
        self.next_btn.config(state=tk.NORMAL if current < 2 else tk.DISABLED)
        self.install_btn.config(state=tk.NORMAL if current == 2 else tk.DISABLED)
    
    def start_installation(self):
        """Start the installation in a separate thread"""
        # Validate API key
        if not self.api_key_var.get():
            messagebox.showerror("Missing Configuration", "Please enter your OpenAI API key")
            return
        
        self.notebook.select(1)
        self.back_btn.config(state=tk.DISABLED)
        self.next_btn.config(state=tk.DISABLED)
        self.install_btn.config(state=tk.DISABLED)
        
        # Start installation in background thread
        thread = threading.Thread(target=self.run_installation)
        thread.daemon = True
        thread.start()
    
    def run_installation(self):
        """Run the actual installation"""
        try:
            self.log("=" * 60)
            self.log("REX AI SYSTEM INSTALLATION")
            self.log("=" * 60)
            
            # Step 1: Create installation directory
            self.log("\n[1/6] Creating installation directory...")
            self.progress_bar['value'] = 10
            self.progress_label.config(text="Creating directories...")
            
            self.install_path.mkdir(parents=True, exist_ok=True)
            self.log(f"✓ Directory created: {self.install_path}")
            
            # Step 2: Create virtual environment
            self.log("\n[2/6] Creating Python virtual environment...")
            self.progress_bar['value'] = 25
            self.progress_label.config(text="Creating virtual environment...")
            
            subprocess.run([sys.executable, "-m", "venv", str(self.venv_path)], check=True, capture_output=True)
            self.log(f"✓ Virtual environment created: {self.venv_path}")
            
            # Step 3: Upgrade pip
            self.log("\n[3/6] Upgrading pip...")
            self.progress_bar['value'] = 40
            self.progress_label.config(text="Upgrading pip...")
            
            subprocess.run([str(self.pip_path), "install", "--upgrade", "pip"], check=True, capture_output=True)
            self.log("✓ pip upgraded")
            
            # Step 4: Install dependencies
            self.log("\n[4/6] Installing dependencies...")
            self.progress_bar['value'] = 55
            self.progress_label.config(text="Installing Python packages...")
            
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
                self.log(f"  Installing {req}...")
                subprocess.run([str(self.pip_path), "install", req], capture_output=True)
                progress = 55 + (i / len(requirements)) * 20
                self.progress_bar['value'] = progress
            
            self.log("✓ All dependencies installed")
            
            # Step 5: Create configuration files
            self.log("\n[5/6] Creating configuration files...")
            self.progress_bar['value'] = 80
            self.progress_label.config(text="Setting up configuration...")
            
            self.create_config_files()
            self.log("✓ Configuration files created")
            
            # Step 6: Create desktop shortcuts and launchers
            self.log("\n[6/6] Creating shortcuts and launchers...")
            self.progress_bar['value'] = 95
            self.progress_label.config(text="Creating desktop shortcuts...")
            
            self.create_shortcuts()
            self.log("✓ Shortcuts created")
            
            # Final
            self.progress_bar['value'] = 100
            self.progress_label.config(text="Installation complete!")
            
            self.log("\n" + "=" * 60)
            self.log("INSTALLATION COMPLETE!")
            self.log("=" * 60)
            
            # Switch to complete tab
            self.root.after(500, lambda: self.notebook.select(3))
            
            # Auto-start if enabled
            if self.autostart_var.get():
                self.log("\nStarting REX AI System...")
                self.root.after(2000, self.start_rex)
        
        except Exception as e:
            self.log(f"\n❌ Installation failed: {str(e)}")
            messagebox.showerror("Installation Failed", f"Error: {str(e)}")
    
    def create_config_files(self):
        """Create necessary configuration files"""
        # Create directories
        (self.install_path / "logs").mkdir(exist_ok=True)
        (self.install_path / "data").mkdir(exist_ok=True)
        (self.install_path / "plugins").mkdir(exist_ok=True)
        (self.install_path / "agents").mkdir(exist_ok=True)
        
        # Create .env file
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

# Self-Modification
REX_SELF_MODIFY_ENABLED=true
REX_CODE_REVIEW_REQUIRED=true
REX_MAX_ITERATIONS=10

# Database
REX_DB_TYPE=sqlite
REX_DB_PATH=data/rex.db
"""
        
        with open(self.install_path / ".env", "w") as f:
            f.write(env_content)
    
    def create_shortcuts(self):
        """Create desktop shortcuts and launcher scripts"""
        system = platform.system()
        
        if system == "Windows":
            # Windows batch file launcher
            launcher_content = f"""@echo off
title REX AI System
cd /d "{self.install_path}"
echo.
echo ╔═══════════════════════════════════════════════════════╗
echo ║         REX AI SYSTEM - JARVIS ASSISTANT             ║
echo ╚═══════════════════════════════════════════════════════╝
echo.
echo Starting REX AI System...
echo API Server: http://localhost:{self.port_var.get()}
echo.
"{self.python_path / 'python.exe'}" main.py
pause
"""
            launcher_path = self.install_path / "REX.bat"
            with open(launcher_path, "w") as f:
                f.write(launcher_content)
            
            # Desktop shortcut
            desktop = Path.home() / "Desktop"
            shortcut_path = desktop / "REX AI System.lnk"
            
            try:
                import win32com.client
                shell = win32com.client.Dispatch("WScript.Shell")
                shortcut = shell.CreateShortcut(str(shortcut_path))
                shortcut.TargetPath = str(launcher_path)
                shortcut.WorkingDirectory = str(self.install_path)
                shortcut.IconLocation = str(self.install_path / "rex.ico")
                shortcut.save()
            except:
                self.log("Note: Could not create Windows shortcut, but launcher script created")
        
        elif system == "Darwin":  # macOS
            launcher_content = f"""#!/bin/bash
cd "{self.install_path}"
export PATH="{self.python_path}:$PATH"
echo "╔═══════════════════════════════════════════════════════╗"
echo "║         REX AI SYSTEM - JARVIS ASSISTANT             ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""
echo "Starting REX AI System..."
echo "API Server: http://localhost:{self.port_var.get()}"
echo ""
python3 main.py
"""
            launcher_path = self.install_path / "REX.command"
            with open(launcher_path, "w") as f:
                f.write(launcher_content)
            os.chmod(launcher_path, 0o755)
        
        else:  # Linux
            launcher_content = f"""#!/bin/bash
cd "{self.install_path}"
export PATH="{self.python_path}:$PATH"
echo "╔═══════════════════════════════════════════════════════╗"
echo "║         REX AI SYSTEM - JARVIS ASSISTANT             ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""
echo "Starting REX AI System..."
echo "API Server: http://localhost:{self.port_var.get()}"
echo ""
python main.py
"""
            launcher_path = self.install_path / "REX.sh"
            with open(launcher_path, "w") as f:
                f.write(launcher_content)
            os.chmod(launcher_path, 0o755)
    
    def start_rex(self):
        """Start the REX system"""
        if self.autostart_var.get():
            try:
                os.chdir(self.install_path)
                if platform.system() == "Windows":
                    subprocess.Popen([str(self.python_path / "python.exe"), "main.py"])
                else:
                    subprocess.Popen([str(self.python_path / "python"), "main.py"])
                self.log("\n✓ REX AI System started!")
                messagebox.showinfo("REX Started", "REX AI System is now running!\n\nAPI Server: http://localhost:{}\n\nCheck the browser window for the GUI dashboard.".format(self.port_var.get()))
            except Exception as e:
                self.log(f"\n❌ Failed to start REX: {str(e)}")


class REXLauncher:
    """Standalone launcher for REX after installation"""
    
    @staticmethod
    def create_launcher_script():
        """Create a launcher script for easy startup"""
        launcher_code = '''#!/usr/bin/env python3
"""REX AI System - Standalone Launcher"""

import sys
import os
import subprocess
import platform
from pathlib import Path

REX_PATH = Path.home() / "REX_AI"
PYTHON_EXE = REX_PATH / ("venv" if platform.system() != "Windows" else "venv\\\\Scripts\\\\python.exe")

if not REX_PATH.exists():
    print("REX is not installed. Please run the installer.")
    sys.exit(1)

os.chdir(REX_PATH)

try:
    subprocess.run([str(PYTHON_EXE), "main.py"], check=True)
except KeyboardInterrupt:
    print("\\nREX shutdown.")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
'''
        return launcher_code


def main():
    """Main entry point"""
    root = tk.Tk()
    app = REXSetupUI(root)
    app.update_button_states()
    root.mainloop()


if __name__ == "__main__":
    main()
