#!/usr/bin/env python3
"""
Demo del modo verbose del tester de GoPhish MCP
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_readonly_tools import GoPhishMCPTester

async def demo_verbose():
    """Demo con solo algunas herramientas para mostrar el formato verbose"""
    print("🎬 DEMO DEL MODO VERBOSE - GoPhish MCP Tester")
    print("=" * 60)
    
    tester = GoPhishMCPTester(verbose=True)
    
    if not tester.initialize_client():
        print("❌ No se puede continuar sin cliente GoPhish")
        return
    
    # Demo con solo 3 herramientas representativas
    print("\n🎯 DEMO: 3 herramientas con salida verbose")
    print("-" * 40)
    
    # 1. Obtener campañas (muchos datos)
    await tester.test_tool("gophish_get_campaigns", 
                          description="Obtener todas las campañas (demo verbose)")
    
    # 2. Estado del sistema (datos estructurados)
    await tester.test_tool("gophish_get_system_status", 
                          description="Obtener estado del sistema (demo verbose)")
    
    # 3. Una campaña específica (datos detallados)
    campaigns_result = await tester.server._handle_tool_call("gophish_get_campaigns", {})
    if campaigns_result and len(campaigns_result) > 0:
        import json
        campaigns_data = json.loads(campaigns_result[0].text)
        if isinstance(campaigns_data, list) and len(campaigns_data) > 0:
            campaign_id = campaigns_data[0].get('id')
            if campaign_id:
                await tester.test_tool("gophish_get_campaign", 
                                      arguments={"campaign_id": campaign_id},
                                      description=f"Campaña específica ID {campaign_id} (demo verbose)")
    
    print(f"\n{chr(10).join(['=' * 60, '🎉 DEMO COMPLETADO', '=' * 60])}")

if __name__ == "__main__":
    asyncio.run(demo_verbose())
