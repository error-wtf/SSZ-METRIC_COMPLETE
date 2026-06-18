"""
Pytest configuration - NO FAKER ALLOWED.
This file runs before any tests and ensures faker is never loaded.
"""
import sys

# Block faker from being imported ever
class FakerBlocker:
    """Blocks faker imports to prevent reputation damage."""
    def find_module(self, fullname, path=None):
        if 'faker' in fullname.lower():
            raise ImportError(f"FAKER IS FORBIDDEN: {fullname} - "
                            "This project uses ONLY calculated physical values, "
                            "never fake/generated data!")
        return None

# Install the blocker
sys.meta_path.insert(0, FakerBlocker())

# Also remove faker from pytest plugins if it was loaded
if 'faker' in sys.modules:
    del sys.modules['faker']
if 'Faker' in sys.modules:
    del sys.modules['Faker']

print("[OK] Anti-Faker blocker installed - faker is FORBIDDEN in this project")
