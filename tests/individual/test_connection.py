#!/usr/bin/env python3
"""
Test básico de conexión con GoPhish
"""
import os
import sys
import pytest
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from client import GophishClient


class TestConnection:
    """Test de conexión básica con GoPhish"""
    
    def setup_method(self):
        """Setup para cada test"""
        self.base_url = os.getenv("GOPHISH_URL", "https://localhost:3333")
        self.api_key = os.getenv("GOPHISH_API_KEY")
        
        if not self.api_key:
            pytest.skip("GOPHISH_API_KEY not configured")
        
        self.client = GophishClient(self.base_url, self.api_key)
    
    def test_connection(self):
        """Test de conexión básica"""
        campaigns = self.client.get_campaigns()
        assert isinstance(campaigns, list)
        print(f"✅ Conexión exitosa - {len(campaigns)} campañas encontradas")
    
    def test_get_groups(self):
        """Test de obtención de grupos"""
        groups = self.client.get_groups()
        assert isinstance(groups, list)
        print(f"✅ Grupos obtenidos - {len(groups)} grupos encontrados")
    
    def test_get_templates(self):
        """Test de obtención de plantillas"""
        templates = self.client.get_templates()
        assert isinstance(templates, list)
        print(f"✅ Plantillas obtenidas - {len(templates)} plantillas encontradas")
    
    def test_get_pages(self):
        """Test de obtención de páginas"""
        pages = self.client.get_pages()
        assert isinstance(pages, list)
        print(f"✅ Páginas obtenidas - {len(pages)} páginas encontradas")
    
    def test_get_smtp_profiles(self):
        """Test de obtención de perfiles SMTP"""
        smtp_profiles = self.client.get_smtp()
        assert isinstance(smtp_profiles, list)
        print(f"✅ Perfiles SMTP obtenidos - {len(smtp_profiles)} perfiles encontrados")
    
    def test_get_users(self):
        """Test de obtención de usuarios"""
        users = self.client.get_users()
        assert isinstance(users, list)
        print(f"✅ Usuarios obtenidos - {len(users)} usuarios encontrados")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
