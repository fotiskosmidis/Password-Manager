import os
import ctypes
from pathlib import Path

# Set the app database path to ~/.local/share/yourapp/ in linux
appName = "PasswordManager"
data_root = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share"))

# Create app directory (creates parents if needed)
app_dir = data_root / appName
app_dir.mkdir(parents=True, exist_ok=True)

# Create DBfiles directory inside app folder
db_dir = app_dir / "DBfiles"
db_dir.mkdir(exist_ok=True)