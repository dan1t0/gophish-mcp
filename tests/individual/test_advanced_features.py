#!/usr/bin/env python3
"""
Test de funcionalidades avanzadas del MCP de GoPhish
"""
import os
import sys
import pytest
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from server import GophishMCPServer


class TestAdvancedFeatures:
    """Test de funcionalidades avanzadas"""
    
    def setup_method(self):
        """Setup para cada test"""
        self.api_key = os.getenv("GOPHISH_API_KEY")
        
        if not self.api_key:
            pytest.skip("GOPHISH_API_KEY not configured")
        
        self.server = GophishMCPServer()
        self.server.initialize_client()
    
    @pytest.mark.asyncio
    async def test_system_status(self):
        """Test del estado del sistema"""
        status = await self.server._handle_tool_call("gophish_get_system_status", {})
        assert "status" in status
        print(f"✅ Estado del sistema: {status.get('status')}")
    
    @pytest.mark.asyncio
    async def test_campaign_analytics(self):
        """Test de análisis de campañas"""
        campaigns = await self.server._handle_tool_call("gophish_get_campaigns", {})
        
        if campaigns:
            campaign_id = campaigns[0].get('id')
            analytics = await self.server._handle_tool_call("gophish_get_campaign_analytics", {
                "campaign_id": campaign_id
            })
            assert "total_targets" in analytics
            print(f"✅ Análisis de campaña {campaign_id}: {analytics.get('total_targets', 0)} objetivos")
    
    @pytest.mark.asyncio
    async def test_search_functionality(self):
        """Test de funcionalidad de búsqueda"""
        # Search campaigns
        search_results = await self.server._handle_tool_call("gophish_search_campaigns", {"query": "test"})
        assert isinstance(search_results, list)
        print(f"✅ Búsqueda de campañas: {len(search_results)} resultados")
        
        # Search groups
        group_search = await self.server._handle_tool_call("gophish_search_groups", {"query": "test"})
        assert isinstance(group_search, list)
        print(f"✅ Búsqueda de grupos: {len(group_search)} resultados")
        
        # Search templates
        template_search = await self.server._handle_tool_call("gophish_search_templates", {"query": "test"})
        assert isinstance(template_search, list)
        print(f"✅ Búsqueda de plantillas: {len(template_search)} resultados")
    
    @pytest.mark.asyncio
    async def test_campaign_filters(self):
        """Test de filtros de campañas"""
        # Get active campaigns
        active = await self.server._handle_tool_call("gophish_get_active_campaigns", {})
        assert isinstance(active, list)
        print(f"✅ Campañas activas: {len(active)}")
        
        # Get completed campaigns
        completed = await self.server._handle_tool_call("gophish_get_completed_campaigns", {})
        assert isinstance(completed, list)
        print(f"✅ Campañas completadas: {len(completed)}")
        
        # Get recent campaigns
        recent = await self.server._handle_tool_call("gophish_get_recent_campaigns", {"days": 30})
        assert isinstance(recent, list)
        print(f"✅ Campañas recientes (30 días): {len(recent)}")
    
    @pytest.mark.asyncio
    async def test_global_analytics(self):
        """Test de análisis global"""
        analytics = await self.server._handle_tool_call("gophish_get_global_analytics", {})
        assert "total_campaigns" in analytics
        print(f"✅ Análisis global: {analytics.get('total_campaigns', 0)} campañas totales")
    
    @pytest.mark.asyncio
    async def test_campaign_validation(self):
        """Test de validación de campañas"""
        campaigns = await self.server._handle_tool_call("gophish_get_campaigns", {})
        
        if campaigns:
            campaign_id = campaigns[0].get('id')
            validation = await self.server._handle_tool_call("gophish_validate_campaign", {
                "campaign_id": campaign_id
            })
            assert "valid" in validation
            print(f"✅ Validación de campaña {campaign_id}: {'Válida' if validation.get('valid') else 'Inválida'}")
    
    @pytest.mark.asyncio
    async def test_export_functionality(self):
        """Test de funcionalidad de exportación"""
        campaigns = await self.server._handle_tool_call("gophish_get_campaigns", {})
        
        if campaigns:
            campaign_id = campaigns[0].get('id')
            
            # Test JSON export
            json_export = await self.server._handle_tool_call("gophish_export_campaign_data", {
                "campaign_id": campaign_id,
                "format": "json"
            })
            assert "format" in json_export
            print(f"✅ Exportación JSON: {json_export.get('format')}")
            
            # Test summary export
            summary_export = await self.server._handle_tool_call("gophish_export_campaign_data", {
                "campaign_id": campaign_id,
                "format": "summary"
            })
            assert "format" in summary_export
            print(f"✅ Exportación resumen: {summary_export.get('format')}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
