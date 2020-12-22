import sys
from cx_Freeze import setup, Executable

include = ["autorun.inf", ".env"]
base = None

if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="simpleGame",
    version="0.1",
    description="simple game",
    options={"build_exe": {"include_files": include}},
    executables=[Executable("client.py", base=base)],
)
