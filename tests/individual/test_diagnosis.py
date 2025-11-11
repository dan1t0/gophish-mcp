#!/usr/bin/env python3
"""
Test de diagnóstico para verificar la conexión con Gophish
"""
import os
import sys
import socket
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class TestDiagnosis:
    """Test de diagnóstico de conexión"""
    
    def setup_method(self):
        """Setup para cada test"""
        self.url = os.getenv("GOPHISH_URL", "https://localhost:3333")
        self.api_key = os.getenv("GOPHISH_API_KEY")
        
        if not self.api_key:
            pytest.skip("GOPHISH_API_KEY not configured")
    
    def test_host_reachable(self):
        """Test de conectividad del host"""
        parsed = urlparse(self.url)
        host = parsed.hostname
        port = parsed.port or (443 if parsed.scheme == 'https' else 80)
        
        print(f"\n🔍 Verificando conectividad a {host}:{port}...")
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                print(f"✅ Puerto {port} está abierto en {host}")
                assert True
            else:
                print(f"❌ No se puede conectar al puerto {port} en {host}")
                print(f"   Error code: {result}")
                assert False, f"Cannot connect to {host}:{port}"
                
        except socket.gaierror:
            print(f"❌ No se puede resolver el hostname: {host}")
            assert False, f"Cannot resolve hostname: {host}"
        except Exception as e:
            print(f"❌ Error al verificar conectividad: {e}")
            assert False, f"Connection error: {e}"
    
    def test_api_endpoint(self):
        """Test del endpoint de la API"""
        print(f"\n🔍 Verificando endpoint de API...")
        
        try:
            # Disable SSL warnings
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            
            response = requests.get(
                f"{self.url}/api/campaigns/",
                headers={'Authorization': f'Bearer {self.api_key}'},
                verify=False,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✅ API respondió correctamente (200 OK)")
                campaigns = response.json()
                print(f"   Campañas encontradas: {len(campaigns)}")
                assert True
            elif response.status_code == 401:
                print(f"❌ Error de autenticación (401)")
                print(f"   Verifica que tu API key sea correcta")
                assert False, "Authentication failed - check API key"
            else:
                print(f"⚠️  API respondió con código: {response.status_code}")
                print(f"   Respuesta: {response.text[:200]}")
                assert False, f"API returned status {response.status_code}"
                
        except requests.exceptions.SSLError as e:
            print(f"❌ Error SSL: {e}")
            print(f"   Intenta con verify_ssl=False")
            assert False, f"SSL error: {e}"
        except requests.exceptions.ConnectionError as e:
            print(f"❌ Error de conexión: {e}")
            assert False, f"Connection error: {e}"
        except requests.exceptions.Timeout:
            print(f"❌ Timeout al conectar con la API")
            assert False, "API timeout"
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            assert False, f"Unexpected error: {e}"
    
    def test_full_diagnosis(self):
        """Test completo de diagnóstico"""
        print("=" * 60)
        print("🔧 DIAGNÓSTICO DE CONEXIÓN GOPHISH")
        print("=" * 60)
        
        print(f"\nConfiguración:")
        print(f"  URL: {self.url}")
        print(f"  API Key: {'*' * 20}{self.api_key[-4:] if len(self.api_key) > 4 else '****'}")
        
        # Test host connectivity
        self.test_host_reachable()
        
        # Test API endpoint
        self.test_api_endpoint()
        
        print("\n" + "=" * 60)
        print("✅ DIAGNÓSTICO EXITOSO")
        print("=" * 60)
        print("\n🎉 Tu servidor MCP de Gophish debería funcionar correctamente!")


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "-s"])
