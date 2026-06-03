#!/usr/bin/env python3
"""
REX AI System - Visual Studio Code Integration Guide & Launcher
Complete setup guide for running REX directly in VS Code with integrated terminal
"""

import os
import sys
import json
import platform
import subprocess
from pathlib import Path


class VSCodeSetup:
    """Helper class for VS Code integration"""
    
    @staticmethod
    def create_vscode_config():
        """Create VS Code configuration files for REX"""
        
        vscode_config = {
            ".vscode/settings.json": {
                "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
                "python.linting.enabled": True,
                "python.linting.pylintEnabled": True,
                "python.formatting.provider": "black",
                "[python]": {
                    "editor.defaultFormatter": "ms-python.python",
                    "editor.formatOnSave": True,
                    "editor.rulers": [100]
                },
                "editor.fontSize": 12,
                "editor.fontFamily": "Fira Code, Courier New",
                "editor.wordWrap": "on",
                "files.exclude": {
                    "**/__pycache__": True,
                    "**/*.pyc": True,
                    "**/venv": False
                }
            },
            
            ".vscode/launch.json": {
                "version": "0.2.0",
                "configurations": [
                    {
                        "name": "REX - API Server",
                        "type": "python",
                        "request": "launch",
                        "program": "${workspaceFolder}/main.py",
                        "console": "integratedTerminal",
                        "justMyCode": True,
                        "env": {
                            "PYTHONUNBUFFERED": "1"
                        },
                        "args": ["--server"]
                    },
                    {
                        "name": "REX - Interactive Mode",
                        "type": "python",
                        "request": "launch",
                        "program": "${workspaceFolder}/main.py",
                        "console": "integratedTerminal",
                        "justMyCode": True,
                        "env": {
                            "PYTHONUNBUFFERED": "1"
                        },
                        "args": ["--interactive"]
                    },
                    {
                        "name": "REX - Voice Mode",
                        "type": "python",
                        "request": "launch",
                        "program": "${workspaceFolder}/main.py",
                        "console": "integratedTerminal",
                        "justMyCode": True,
                        "env": {
                            "PYTHONUNBUFFERED": "1"
                        },
                        "args": ["--voice"]
                    },
                    {
                        "name": "Python: Current File",
                        "type": "python",
                        "request": "launch",
                        "program": "${file}",
                        "console": "integratedTerminal",
                        "justMyCode": True
                    }
                ]
            },
            
            ".vscode/tasks.json": {
                "version": "2.0.0",
                "tasks": [
                    {
                        "label": "REX: Install Dependencies",
                        "type": "shell",
                        "command": "${command:python.interpreterPath}",
                        "args": ["-m", "pip", "install", "-r", "requirements.txt"],
                        "problemMatcher": [],
                        "group": {
                            "kind": "build",
                            "isDefault": True
                        }
                    },
                    {
                        "label": "REX: Start API Server",
                        "type": "shell",
                        "command": "${command:python.interpreterPath}",
                        "args": ["main.py", "--server"],
                        "isBackground": True,
                        "problemMatcher": {
                            "pattern": {
                                "regexp": "^.*$",
                                "file": 1,
                                "location": 2,
                                "message": 3
                            },
                            "background": {
                                "activeOnStart": True,
                                "beginsPattern": "^.*Starting.*",
                                "endsPattern": "^.*Running on.*"
                            }
                        },
                        "group": "test"
                    },
                    {
                        "label": "REX: Start Interactive",
                        "type": "shell",
                        "command": "${command:python.interpreterPath}",
                        "args": ["main.py", "--interactive"],
                        "group": "test"
                    },
                    {
                        "label": "REX: Run Tests",
                        "type": "shell",
                        "command": "${command:python.interpreterPath}",
                        "args": ["-m", "pytest", "-v"],
                        "group": "test"
                    },
                    {
                        "label": "REX: Format Code",
                        "type": "shell",
                        "command": "${command:python.interpreterPath}",
                        "args": ["-m", "black", "."],
                        "group": "test"
                    }
                ]
            },
            
            ".vscode/extensions.json": {
                "recommendations": [
                    "ms-python.python",
                    "ms-python.vscode-pylance",
                    "ms-python.debugpy",
                    "ms-python.black-formatter",
                    "ms-python.flake8",
                    "charliermarsh.ruff",
                    "ms-vscode.makefile-tools",
                    "github.copilot",
                    "ms-vscode-remote.remote-containers"
                ]
            }
        }
        
        return vscode_config


def print_setup_guide():
    """Print comprehensive setup guide for VS Code"""
    
    guide = """
╔════════════════════════════════════════════════════════════════════╗
║       REX AI SYSTEM - VISUAL STUDIO CODE SETUP GUIDE              ║
║              Complete Instructions for VS Code Integration         ║
╚════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════
STEP 1: DOWNLOAD & SETUP
═══════════════════════════════════════════════════════════════════════

1.1 Clone or Download the REX Repository:
    • Open VS Code
    • Press Ctrl+` (backtick) to open terminal
    • Run:
      git clone https://github.com/y7217937891273987/rex.git
      cd rex
    
    OR just download setup.py and run:
      python setup.py

1.2 Run the Installer:
    • Open Terminal in VS Code (Ctrl+`)
    • Run: python setup.py
    • Follow the GUI wizard
    • Installation creates everything automatically

═══════════════════════════════════════════════════════════════════════
STEP 2: OPEN REX IN VS CODE
═══════════════════════════════════════════════════════════════════════

2.1 Open the REX folder:
    • File → Open Folder (or Ctrl+K Ctrl+O)
    • Navigate to ~/REX_AI or your installation folder
    • Click "Select Folder"

2.2 Install Recommended Extensions:
    • VS Code will show "Extension Recommendations" popup
    • Click "Install All" or install individually:
      - Python (ms-python.python)
      - Pylance (ms-python.vscode-pylance)
      - Black Formatter (ms-python.black-formatter)
      - GitHub Copilot (github.copilot) - Optional

═══════════════════════════════════════════════════════════════════════
STEP 3: CONFIGURE PYTHON INTERPRETER
═══════════════════════════════════════════════════════════════════════

3.1 Select Virtual Environment:
    • Press Ctrl+Shift+P to open Command Palette
    • Type: "Python: Select Interpreter"
    • Choose the one with "./venv/bin/python" path
    
3.2 Or Manually:
    • Click Python version in bottom-right corner
    • Select "./venv/bin/python" or "./venv/Scripts/python.exe" (Windows)

═══════════════════════════════════════════════════════════════════════
STEP 4: QUICK START - RUN REX IN VS CODE
═══════════════════════════════════════════════════════════════════════

METHOD 1: Using Run Configuration (Easiest)
    • Press Ctrl+Shift+D (Debug view)
    • At the top, select run configuration from dropdown:
      - "REX - API Server" (web interface)
      - "REX - Interactive Mode" (chat in terminal)
      - "REX - Voice Mode" (voice control)
    • Click Green Play button (or F5)
    • REX starts in integrated terminal!

METHOD 2: Using Terminal
    • Press Ctrl+` to open VS Code terminal
    • Run one of:
      
      # Start API Server (web interface)
      python main.py
      
      # Start Interactive Chat
      python main.py --interactive
      
      # Start Voice Mode
      python main.py --voice

METHOD 3: Using Tasks
    • Press Ctrl+Shift+B or go to Terminal → Run Task
    • Select:
      - "REX: Start API Server"
      - "REX: Start Interactive"
    • Task runs in background

═══════════════════════════════════════════════════════════════════════
STEP 5: FIRST RUN - CONFIGURE .ENV FILE
═══════════════════════════════════════════════════════════════════════

5.1 The .env file was created during setup with your API key

5.2 To verify/edit configuration:
    • Open .env file in VS Code
    • Should contain:
      OPENAI_API_KEY=your_key_here
      REX_API_PORT=5000
      REX_ENV=development
      REX_VOICE_ENABLED=true/false
      etc.
    
5.3 If you need to change API key:
    • Edit .env file directly
    • Save (Ctrl+S)
    • Restart REX

═══════════════════════════════════════════════════════════════════════
STEP 6: RUNNING & TESTING
═══════════════════════════════════════════════════════════════════════

OPTION A: WEB INTERFACE (Recommended for first time)
    1. In VS Code terminal, run:
       python main.py
    
    2. You'll see:
       ╔══════════════════════��═══════════╗
       ║    Starting API server on        ║
       ║    http://localhost:5000         ║
       ╚══════════════════════════════════╝
    
    3. Open browser and go to: http://localhost:5000
    
    4. You'll see:
       - Dashboard with chat interface
       - Memory/stats display
       - Plugin management
       - Agent status

OPTION B: INTERACTIVE CHAT (Terminal)
    1. In VS Code terminal, run:
       python main.py --interactive
    
    2. Type messages directly in terminal:
       You: Hello REX
       REX: Hello! I'm REX, your AI assistant...
    
    3. Type 'exit' to quit

OPTION C: VOICE MODE (Interactive + Voice)
    1. Make sure microphone is connected
    2. Run:
       python main.py --voice
    
    3. Speak to REX:
       REX: "I'm listening..."
       [Speak now]
       REX: "You said: [what you said]"

═══════════════════════════════════════════════════════════════════════
STEP 7: DEBUGGING IN VS CODE
═══════════════════════════════════════════════════════════════════════

7.1 Set Breakpoints:
    • Click left margin in code to add red dot
    • Run with F5 (Debug mode)
    • Code stops at breakpoint
    • Use Debug Console to inspect variables

7.2 View Variables:
    • When stopped at breakpoint:
      - Left panel shows "Variables"
      - Hover over variable name to see value
      - Debug Console (Ctrl+Shift+Y) to evaluate expressions

7.3 Step Through Code:
    • F10 = Step over
    • F11 = Step into
    • Shift+F11 = Step out
    • F5 = Continue

═══════════════════════════════════════════════════════════════════════
STEP 8: COMMON OPERATIONS IN VS CODE
═══════════════════════════════════════════════════════════════════════

INSTALL NEW PACKAGE:
    • Terminal → New Terminal (Ctrl+`)
    • Run: pip install package_name
    • It installs in virtual environment automatically

VIEW LOGS:
    • Open: logs/rex.log
    • Right-click → "Open to the Side" for split view
    • Logs update in real-time

CREATE NEW PLUGIN:
    • Right-click plugins/ folder → New File
    • Name: my_plugin.py
    • Copy template from plugins/base.py
    • Edit and save
    • REX loads it automatically

VIEW MEMORY DATA:
    • Data stored in data/rex.db (SQLite)
    • Install SQLite extension: alexcvzz.vscode-sqlite
    • Click data/rex.db to browse tables

═══════════════════════════════════════════════════════════════════════
STEP 9: USEFUL VS CODE SHORTCUTS
═══════════════════════════════════════════════════════════════════════

Ctrl+`             = Open/Close Terminal
Ctrl+Shift+D       = Debug view
Ctrl+Shift+P       = Command Palette
Ctrl+/             = Toggle comment
F5                 = Start debugging
F10                = Step over
F11                = Step into
Ctrl+F             = Find in file
Ctrl+H             = Find and replace
Ctrl+K Ctrl+F      = Format document
Alt+Up/Down        = Move line up/down
Ctrl+D             = Select next occurrence

═══════════════════════════════════════════════════════════════════════
STEP 10: TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════════

PROBLEM: "Python not found"
SOLUTION:
    1. Press Ctrl+Shift+P
    2. Type "Python: Select Interpreter"
    3. Choose ./venv/bin/python (or ./venv/Scripts/python.exe on Windows)
    4. Restart VS Code

PROBLEM: "ModuleNotFoundError: No module named 'openai'"
SOLUTION:
    1. In Terminal: pip install -r requirements.txt
    2. Or: pip install openai

PROBLEM: "Port 5000 already in use"
SOLUTION:
    1. Edit .env file
    2. Change: REX_API_PORT=5000 → REX_API_PORT=5001
    3. Save and restart

PROBLEM: "API key error"
SOLUTION:
    1. Edit .env file
    2. Verify OPENAI_API_KEY=sk-... (starts with sk-)
    3. Make sure it's valid from https://platform.openai.com/api/keys

PROBLEM: "Terminal not working"
SOLUTION:
    1. Press Ctrl+` to toggle terminal
    2. If still not working: Terminal → New Terminal
    3. Verify Python path: which python (Mac/Linux) or where python (Windows)

═══════════════════════════════════════════════════════════════════════
STEP 11: NEXT STEPS
═══════════════════════════════════════════════════════════════════════

✓ Chat with REX using the interface
✓ Create custom plugins in plugins/ folder
✓ Create autonomous agents in agents/ folder
✓ Modify settings in config/settings.py
✓ Add new features using code generation
✓ Train REX with feedback for improvements

═══════════════════════════════════════════════════════════════════════
STEP 12: ADVANCED - CREATE CUSTOM RUN CONFIGURATION
═══════════════════════════════════════════════════════════════════════

To add your own run configuration:
    1. Click Debug icon (Ctrl+Shift+D)
    2. Click "create a launch.json file"
    3. Select "Python"
    4. Add configuration:

{
    "name": "My Custom Mode",
    "type": "python",
    "request": "launch",
    "program": "${workspaceFolder}/main.py",
    "console": "integratedTerminal",
    "args": ["--custom-arg"],
    "env": {
        "PYTHONUNBUFFERED": "1",
        "REX_ENV": "development"
    }
}

═══════════════════════════════════════════════════════════════════════
COMPLETE VS CODE WORKFLOW
═══════════════════════════════════════════════════════════════════════

1. Clone repo / Run setup
2. Open folder in VS Code
3. Select Python interpreter
4. Terminal: pip install -r requirements.txt (if needed)
5. Press F5 or Ctrl+Shift+D → Select run config → Play button
6. REX starts in integrated terminal
7. Open http://localhost:5000 in browser
8. Chat with REX!
9. Edit code in VS Code
10. Create plugins/agents
11. REX loads changes automatically

═══════════════════════════════════════════════════════════════════════
THAT'S IT! 🎉
═══════════════════════════════════════════════════════════════════════

You're now running REX in Visual Studio Code!

For help:
    • Terminal: python main.py --help
    • Docs: README.md
    • Issues: GitHub Issues
    • API Docs: http://localhost:5000/docs (when running)

Happy coding with REX! 🤖✨
"""
    
    return guide


def create_vscode_config_files(install_path: Path):
    """Create VS Code configuration files in the repo"""
    
    vscode_dir = install_path / ".vscode"
    vscode_dir.mkdir(exist_ok=True)
    
    setup = VSCodeSetup()
    config = setup.create_vscode_config()
    
    for file_name, file_content in config.items():
        file_path = install_path / file_name
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w') as f:
            json.dump(file_content, f, indent=4)
        
        print(f"Created: {file_path}")


def main():
    """Main entry point"""
    
    print(print_setup_guide())
    
    print("\n" + "="*70)
    print("Creating VS Code configuration files...")
    print("="*70 + "\n")
    
    install_path = Path.cwd()
    create_vscode_config_files(install_path)
    
    print("\n✓ VS Code configuration files created!")
    print("✓ You can now run REX in VS Code!")
    print("\nNext steps:")
    print("  1. Open this folder in VS Code")
    print("  2. Select Python interpreter (Ctrl+Shift+P → Python: Select Interpreter)")
    print("  3. Press F5 or Ctrl+Shift+D to open Debug view")
    print("  4. Click the Play button to run REX")
    print("\nFor detailed instructions, see the guide above!")


if __name__ == "__main__":
    main()
