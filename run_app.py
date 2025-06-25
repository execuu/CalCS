import os
import subprocess
import webbrowser

app_path = os.path.join(os.path.dirname(__file__), '/home/execu/Programming/CalCS/jb/main.py')

subprocess.Popen(f"streamlit run \"{app_path}\"", shell=True)
webbrowser.open("http://localhost:8501")
