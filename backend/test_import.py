import sys
from pathlib import Path

# Add the src and app directories to the Python path
current_dir = Path('.').resolve()
src_path = current_dir / 'src'
app_path = src_path / 'app'

print(f"Current directory: {current_dir}")
print(f"Src path: {src_path}")
print(f"App path: {app_path}")

# Add paths to Python path
sys.path.insert(0, str(app_path))
sys.path.insert(0, str(src_path))

print("Python path updated. Trying to import app.main...")
try:
    from app.main import app
    print("Import OK")
except ImportError as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()