#!/usr/bin/env python3
"""
Script principal para ejecutar todas las pruebas de GoPhish MCP
"""
import os
import sys
import subprocess
from pathlib import Path

def show_help():
    """Mostrar ayuda del script"""
    print("🧪 GoPhish MCP - Script de Pruebas")
    print("=" * 40)
    print("Uso: python test.py [comando] [opciones]")
    print()
    print("Comandos disponibles:")
    print("  readonly     - Ejecutar pruebas de solo lectura")
    print("  demo         - Ejecutar demo verbose")
    print("  comprehensive - Ejecutar pruebas comprehensivas")
    print("  all          - Ejecutar todas las pruebas")
    print()
    print("Opciones:")
    print("  --verbose, -v - Salida detallada con colores")
    print("  --help, -h    - Mostrar esta ayuda")
    print()
    print("Ejemplos:")
    print("  python test.py readonly")
    print("  python test.py demo")
    print("  python test.py readonly --verbose")
    print("  python test.py all")

def main():
    """Función principal"""
    if len(sys.argv) < 2 or sys.argv[1] in ['--help', '-h']:
        show_help()
        return 0
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    # Cambiar al directorio de tests
    tests_dir = Path(__file__).parent / "tests"
    os.chdir(tests_dir)
    
    try:
        if command == "readonly":
            print("🧪 Ejecutando pruebas de solo lectura...")
            cmd = [sys.executable, "run_tests.py"] + args
        elif command == "demo":
            print("🎬 Ejecutando demo verbose...")
            cmd = [sys.executable, "demo_verbose.py"] + args
        elif command == "comprehensive":
            print("🔬 Ejecutando pruebas comprehensivas...")
            cmd = [sys.executable, "run_comprehensive_tests.py"] + args
        elif command == "all":
            print("🚀 Ejecutando todas las pruebas...")
            print("=" * 50)
            
            # Ejecutar pruebas de solo lectura
            print("\n1️⃣ Pruebas de solo lectura:")
            result1 = subprocess.run([sys.executable, "run_tests.py"] + args)
            
            # Ejecutar demo verbose
            print("\n2️⃣ Demo verbose:")
            result2 = subprocess.run([sys.executable, "demo_verbose.py"])
            
            # Ejecutar pruebas comprehensivas
            print("\n3️⃣ Pruebas comprehensivas:")
            result3 = subprocess.run([sys.executable, "run_comprehensive_tests.py"] + args)
            
            # Resumen final
            print("\n" + "=" * 50)
            print("📊 RESUMEN FINAL:")
            print(f"  Pruebas de solo lectura: {'✅' if result1.returncode == 0 else '❌'}")
            print(f"  Demo verbose: {'✅' if result2.returncode == 0 else '❌'}")
            print(f"  Pruebas comprehensivas: {'✅' if result3.returncode == 0 else '❌'}")
            
            return max(result1.returncode, result2.returncode, result3.returncode)
        else:
            print(f"❌ Comando desconocido: {command}")
            show_help()
            return 1
        
        if command != "all":
            result = subprocess.run(cmd, check=True)
            return result.returncode
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando {command}: {e}")
        return e.returncode
    except KeyboardInterrupt:
        print(f"\n⚠️  {command} interrumpido por el usuario")
        return 1

if __name__ == "__main__":
    sys.exit(main())
