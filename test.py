#!/usr/bin/env python3
"""
Main script to run all GoPhish MCP tests
"""
import os
import sys
import subprocess
from pathlib import Path

def show_help():
    """Show script help"""
    print("🧪 GoPhish MCP - Test Script")
    print("=" * 40)
    print("Usage: python test.py [command] [options]")
    print()
    print("Available commands:")
    print("  readonly     - Run read-only tests")
    print("  demo         - Run verbose demo")
    print("  comprehensive - Run comprehensive tests")
    print("  all          - Run every test suite")
    print()
    print("Options:")
    print("  --verbose, -v - Detailed output with colors")
    print("  --help, -h    - Show this help message")
    print()
    print("Examples:")
    print("  python test.py readonly")
    print("  python test.py demo")
    print("  python test.py readonly --verbose")
    print("  python test.py all")

def main():
    """Main entry point"""
    if len(sys.argv) < 2 or sys.argv[1] in ['--help', '-h']:
        show_help()
        return 0
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    # Change to the tests directory
    tests_dir = Path(__file__).parent / "tests"
    os.chdir(tests_dir)
    
    try:
        if command == "readonly":
            print("🧪 Running read-only tests...")
            cmd = [sys.executable, "run_tests.py"] + args
        elif command == "demo":
            print("🎬 Running verbose demo...")
            cmd = [sys.executable, "demo_verbose.py"] + args
        elif command == "comprehensive":
            print("🔬 Running comprehensive tests...")
            cmd = [sys.executable, "run_comprehensive_tests.py"] + args
        elif command == "all":
            print("🚀 Running all tests...")
            print("=" * 50)
            
            # Run read-only tests
            print("\n1️⃣ Read-only tests:")
            result1 = subprocess.run([sys.executable, "run_tests.py"] + args)
            
            # Run verbose demo
            print("\n2️⃣ Verbose demo:")
            result2 = subprocess.run([sys.executable, "demo_verbose.py"])
            
            # Run comprehensive tests
            print("\n3️⃣ Comprehensive tests:")
            result3 = subprocess.run([sys.executable, "run_comprehensive_tests.py"] + args)
            
            # Final summary
            print("\n" + "=" * 50)
            print("📊 FINAL SUMMARY:")
            print(f"  Read-only tests: {'✅' if result1.returncode == 0 else '❌'}")
            print(f"  Verbose demo: {'✅' if result2.returncode == 0 else '❌'}")
            print(f"  Comprehensive tests: {'✅' if result3.returncode == 0 else '❌'}")
            
            return max(result1.returncode, result2.returncode, result3.returncode)
        else:
            print(f"❌ Unknown command: {command}")
            show_help()
            return 1
        
        if command != "all":
            result = subprocess.run(cmd, check=True)
            return result.returncode
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {command}: {e}")
        return e.returncode
    except KeyboardInterrupt:
        print(f"\n⚠️  {command} interrupted by user")
        return 1

if __name__ == "__main__":
    sys.exit(main())
