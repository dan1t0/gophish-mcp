#!/usr/bin/env python3
"""
Convenience script to run the verbose demo from the project root
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    """Run the GoPhish MCP verbose demo"""
    # Change to the test scripts directory
    scripts_dir = Path(__file__).parent / "tests" / "scripts"
    os.chdir(scripts_dir)
    
    print("🎬 Running GoPhish MCP verbose demo...")
    print("=" * 50)
    
    # Run demo_verbose.py
    cmd = [sys.executable, "demo_verbose.py"]
    
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running demo: {e}")
        return e.returncode
    except KeyboardInterrupt:
        print("\n⚠️  Demo interrupted by user")
        return 1

if __name__ == "__main__":
    sys.exit(main())