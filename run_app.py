import os
import subprocess
import webbrowser

# Get full path to main.py
app_path = os.path.join(os.path.dirname(__file__), '/home/execu/Programming/CalCS/jb/main.py')

# Launch Streamlit with the full path
subprocess.Popen(f"streamlit run \"{app_path}\"", shell=True)
webbrowser.open("http://localhost:8501")
