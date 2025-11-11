#!/usr/bin/env python3
"""
Script de conveniencia para ejecutar el demo verbose desde la raíz del proyecto
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    """Ejecutar el demo verbose de GoPhish MCP"""
    # Cambiar al directorio de scripts de pruebas
    scripts_dir = Path(__file__).parent / "tests" / "scripts"
    os.chdir(scripts_dir)
    
    print("🎬 Ejecutando demo verbose de GoPhish MCP...")
    print("=" * 50)
    
    # Ejecutar demo_verbose.py
    cmd = [sys.executable, "demo_verbose.py"]
    
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando el demo: {e}")
        return e.returncode
    except KeyboardInterrupt:
        print("\n⚠️  Demo interrumpido por el usuario")
        return 1

if __name__ == "__main__":
    sys.exit(main())