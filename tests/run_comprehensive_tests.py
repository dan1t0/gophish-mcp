#!/usr/bin/env python3
"""
Script de conveniencia para ejecutar las pruebas comprehensivas desde la raíz del proyecto
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    """Ejecutar las pruebas comprehensivas de GoPhish MCP"""
    # Cambiar al directorio de pruebas comprehensivas
    comprehensive_dir = Path(__file__).parent / "tests" / "comprehensive"
    os.chdir(comprehensive_dir)
    
    print("🔬 Ejecutando pruebas comprehensivas de GoPhish MCP...")
    print("=" * 50)
    
    # Ejecutar test_comprehensive.py
    cmd = [sys.executable, "test_comprehensive.py"] + sys.argv[1:]
    
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando las pruebas comprehensivas: {e}")
        return e.returncode
    except KeyboardInterrupt:
        print("\n⚠️  Pruebas interrumpidas por el usuario")
        return 1

if __name__ == "__main__":
    sys.exit(main())
