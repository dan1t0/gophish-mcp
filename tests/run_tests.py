#!/usr/bin/env python3
"""
Convenience script to run tests from the project root
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    """Run GoPhish MCP tests"""
    # Change to the test scripts directory
    scripts_dir = Path(__file__).parent / "tests" / "scripts"
    os.chdir(scripts_dir)
    
    print("🧪 Running GoPhish MCP tests...")
    print("=" * 50)
    
    # Run test_readonly_tools.py with any provided arguments
    cmd = [sys.executable, "test_readonly_tools.py"] + sys.argv[1:]
    
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running tests: {e}")
        return e.returncode
    except KeyboardInterrupt:
        print("\n⚠️  Tests interrupted by user")
        return 1

if __name__ == "__main__":
    sys.exit(main())
