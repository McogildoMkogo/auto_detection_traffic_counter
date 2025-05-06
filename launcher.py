import os
import subprocess
import sys

def main():
    # Get the directory where the executable is located
    if getattr(sys, 'frozen', False):
        # If running as a bundled executable
        app_dir = os.path.dirname(sys.executable)
    else:
        # If running as a script
        app_dir = os.path.dirname(os.path.abspath(__file__))

    # Change to the app directory
    os.chdir(app_dir)

    # Determine the path to streamlit.exe
    if getattr(sys, 'frozen', False):
        # If running as a bundled executable, use the bundled streamlit
        streamlit_path = os.path.join(app_dir, "streamlit.exe")
    else:
        # If running as a script, use the system streamlit
        streamlit_path = "streamlit"

    # Run Streamlit
    subprocess.run([streamlit_path, "run", "app.py", "--server.address", "0.0.0.0"])

if __name__ == "__main__":
    main() 