#!/usr/bin/env python3
"""
Convenience script to run comprehensive tests from the project root
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    """Run comprehensive GoPhish MCP tests"""
    # Change to the comprehensive tests directory
    comprehensive_dir = Path(__file__).parent / "tests" / "comprehensive"
    os.chdir(comprehensive_dir)
    
    print("🔬 Running comprehensive GoPhish MCP tests...")
    print("=" * 50)
    
    # Run test_comprehensive.py
    cmd = [sys.executable, "test_comprehensive.py"] + sys.argv[1:]
    
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running comprehensive tests: {e}")
        return e.returncode
    except KeyboardInterrupt:
        print("\n⚠️  Tests interrupted by user")
        return 1

if __name__ == "__main__":
    sys.exit(main())
