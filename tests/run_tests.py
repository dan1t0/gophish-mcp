#!/usr/bin/env python3
"""
Script de conveniencia para ejecutar las pruebas desde la raíz del proyecto
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    """Ejecutar las pruebas de GoPhish MCP"""
    # Cambiar al directorio de scripts de pruebas
    scripts_dir = Path(__file__).parent / "tests" / "scripts"
    os.chdir(scripts_dir)
    
    print("🧪 Ejecutando pruebas de GoPhish MCP...")
    print("=" * 50)
    
    # Ejecutar test_readonly_tools.py con los argumentos pasados
    cmd = [sys.executable, "test_readonly_tools.py"] + sys.argv[1:]
    
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando las pruebas: {e}")
        return e.returncode
    except KeyboardInterrupt:
        print("\n⚠️  Pruebas interrumpidas por el usuario")
        return 1

if __name__ == "__main__":
    sys.exit(main())
