import sys
import os
from streamlit.web import cli as stcli


def main():
    # Ensure we run from the project root where src is located
    # Adjust sys.argv to emulate 'streamlit run src/streamlit_app.py'
    file_path = os.path.join(os.path.dirname(__file__), "streamlit_app.py")
    sys.argv = ["streamlit", "run", file_path]
    sys.exit(stcli.main())
