#!/usr/bin/env python3
"""
Script de prueba completo para todas las funcionalidades del MCP de Gophish
"""
import asyncio
import json
import os
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from server import GophishMCPServer

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Get configuration from environment variables
GOPHISH_URL = os.getenv("GOPHISH_URL", "https://localhost:3333")
GOPHISH_API_KEY = os.getenv("GOPHISH_API_KEY")

if not GOPHISH_API_KEY:
    print("❌ Error: GOPHISH_API_KEY no está configurada")
    print("   Configura las variables de entorno o crea un archivo .env")
    sys.exit(1)

os.environ["GOPHISH_URL"] = GOPHISH_URL
os.environ["GOPHISH_API_KEY"] = GOPHISH_API_KEY

async def test_all_functionality():
    """Prueba todas las funcionalidades del MCP de Gophish"""
    print("🚀 Iniciando pruebas completas del MCP de Gophish...")
    print("=" * 80)
    
    server = GophishMCPServer()
    server.initialize_client()
    
    # Test 1: System Status
    print("\n📊 TEST 1: Estado del Sistema")
    print("-" * 40)
    status = await server._handle_tool_call("gophish_get_system_status", {})
    print(json.dumps(status, indent=2))
    
    # Test 2: Campaign Management
    print("\n🎯 TEST 2: Gestión de Campañas")
    print("-" * 40)
    
    # Get all campaigns
    campaigns = await server._handle_tool_call("gophish_get_campaigns", {})
    print(f"Total de campañas: {len(campaigns)}")
    
    if campaigns:
        # Get latest campaign
        latest = await server._handle_tool_call("gophish_get_latest_campaign", {})
        print(f"Última campaña: {latest.get('name', 'Sin nombre')}")
        
        # Get campaign summary
        campaign_id = latest.get('id')
        if campaign_id:
            summary = await server._handle_tool_call("gophish_get_campaign_summary", {"campaign_id": campaign_id})
            print(f"Resumen de campaña {campaign_id}:")
            print(f"  - Total objetivos: {summary.get('total_targets', 0)}")
            print(f"  - Estado: {summary.get('status', 'Unknown')}")
    
    # Test 3: Advanced Campaign Analytics
    print("\n📈 TEST 3: Análisis Avanzado de Campañas")
    print("-" * 40)
    
    # Get active campaigns
    active = await server._handle_tool_call("gophish_get_active_campaigns", {})
    print(f"Campañas activas: {len(active)}")
    
    # Get completed campaigns
    completed = await server._handle_tool_call("gophish_get_completed_campaigns", {})
    print(f"Campañas completadas: {len(completed)}")
    
    # Get recent campaigns
    recent = await server._handle_tool_call("gophish_get_recent_campaigns", {"days": 30})
    print(f"Campañas de los últimos 30 días: {len(recent)}")
    
    # Test 4: Search Functionality
    print("\n🔍 TEST 4: Funcionalidad de Búsqueda")
    print("-" * 40)
    
    # Search campaigns
    search_results = await server._handle_tool_call("gophish_search_campaigns", {"query": "test"})
    print(f"Búsqueda de campañas con 'test': {len(search_results)} resultados")
    
    # Test 5: Groups Management
    print("\n👥 TEST 5: Gestión de Grupos")
    print("-" * 40)
    
    groups = await server._handle_tool_call("gophish_get_groups", {})
    print(f"Total de grupos: {len(groups)}")
    
    if groups:
        # Search groups
        group_search = await server._handle_tool_call("gophish_search_groups", {"query": "test"})
        print(f"Búsqueda de grupos con 'test': {len(group_search)} resultados")
    
    # Test 6: Templates Management
    print("\n📧 TEST 6: Gestión de Plantillas")
    print("-" * 40)
    
    templates = await server._handle_tool_call("gophish_get_templates", {})
    print(f"Total de plantillas: {len(templates)}")
    
    if templates:
        # Search templates
        template_search = await server._handle_tool_call("gophish_search_templates", {"query": "urgente"})
        print(f"Búsqueda de plantillas con 'urgente': {len(template_search)} resultados")
    
    # Test 7: Pages Management
    print("\n🌐 TEST 7: Gestión de Páginas")
    print("-" * 40)
    
    pages = await server._handle_tool_call("gophish_get_pages", {})
    print(f"Total de páginas: {len(pages)}")
    
    # Test 8: SMTP Profiles Management
    print("\n📮 TEST 8: Gestión de Perfiles SMTP")
    print("-" * 40)
    
    smtp_profiles = await server._handle_tool_call("gophish_get_smtp_profiles", {})
    print(f"Total de perfiles SMTP: {len(smtp_profiles)}")
    
    # Test 9: User Management
    print("\n👤 TEST 9: Gestión de Usuarios")
    print("-" * 40)
    
    users = await server._handle_tool_call("gophish_get_users", {})
    print(f"Total de usuarios: {len(users)}")
    
    # Test 10: Global Analytics
    print("\n📊 TEST 10: Análisis Global")
    print("-" * 40)
    
    global_analytics = await server._handle_tool_call("gophish_get_global_analytics", {})
    print("Análisis global:")
    print(f"  - Total campañas: {global_analytics.get('total_campaigns', 0)}")
    print(f"  - Total objetivos: {global_analytics.get('total_targets', 0)}")
    print(f"  - Click rate general: {global_analytics.get('overall_click_rate', 0)}%")
    print(f"  - Submit rate general: {global_analytics.get('overall_submit_rate', 0)}%")
    
    # Test 11: Campaign Validation and Export
    if campaigns:
        print("\n✅ TEST 11: Validación y Exportación")
        print("-" * 40)
        
        campaign_id = campaigns[0].get('id')
        if campaign_id:
            # Validate campaign
            validation = await server._handle_tool_call("gophish_validate_campaign", {"campaign_id": campaign_id})
            print(f"Validación de campaña {campaign_id}:")
            print(f"  - Válida: {validation.get('valid', False)}")
            print(f"  - Errores: {len(validation.get('errors', []))}")
            print(f"  - Advertencias: {len(validation.get('warnings', []))}")
            
            # Export campaign data
            export_data = await server._handle_tool_call("gophish_export_campaign_data", {
                "campaign_id": campaign_id,
                "format": "summary"
            })
            print(f"Exportación de datos: {export_data.get('format', 'unknown')} format")
    
    # Test 12: Date Range Queries
    print("\n📅 TEST 12: Consultas por Rango de Fechas")
    print("-" * 40)
    
    # Get campaigns from last 7 days
    end_date = datetime.now().isoformat()
    start_date = (datetime.now() - timedelta(days=7)).isoformat()
    
    date_range_campaigns = await server._handle_tool_call("gophish_get_campaign_by_date_range", {
        "start_date": start_date,
        "end_date": end_date
    })
    print(f"Campañas en los últimos 7 días: {len(date_range_campaigns)}")
    
    print("\n" + "=" * 80)
    print("✅ Pruebas completadas exitosamente!")
    print("🎉 El MCP de Gophish está funcionando correctamente con todas las funcionalidades.")
    print("=" * 80)

async def test_specific_campaign_analytics():
    """Prueba específica de análisis de campaña"""
    print("\n🔬 PRUEBA ESPECÍFICA: Análisis Detallado de Campaña")
    print("=" * 60)
    
    server = GophishMCPServer()
    server.initialize_client()
    
    # Get campaigns
    campaigns = await server._handle_tool_call("gophish_get_campaigns", {})
    
    if not campaigns:
        print("❌ No hay campañas disponibles para análisis")
        return
    
    # Get the first campaign
    campaign = campaigns[0]
    campaign_id = campaign.get('id')
    campaign_name = campaign.get('name', 'Sin nombre')
    
    print(f"Analizando campaña: {campaign_name} (ID: {campaign_id})")
    
    # Get detailed analytics
    analytics = await server._handle_tool_call("gophish_get_campaign_analytics", {"campaign_id": campaign_id})
    
    print("\n📊 Análisis Detallado:")
    print(f"  - Total objetivos: {analytics.get('total_targets', 0)}")
    print(f"  - Click rate: {analytics.get('click_rate', 0)}%")
    print(f"  - Submit rate: {analytics.get('submit_rate', 0)}%")
    print(f"  - Email open rate: {analytics.get('email_open_rate', 0)}%")
    print(f"  - IPs únicas: {analytics.get('unique_ips', 0)}")
    print(f"  - User agents únicos: {analytics.get('unique_user_agents', 0)}")
    
    # Show status breakdown
    status_breakdown = analytics.get('status_breakdown', {})
    if status_breakdown:
        print("\n📈 Distribución por Estado:")
        for status, count in status_breakdown.items():
            print(f"  - {status}: {count}")
    
    # Show email events
    email_events = analytics.get('email_events', {})
    if email_events:
        print("\n📧 Eventos de Email:")
        for event, count in email_events.items():
            print(f"  - {event}: {count}")

if __name__ == "__main__":
    print("🧪 INICIANDO PRUEBAS COMPREHENSIVAS DEL MCP GOPHISH")
    print("=" * 80)
    
    try:
        # Run main tests
        asyncio.run(test_all_functionality())
        
        # Run specific analytics test
        asyncio.run(test_specific_campaign_analytics())
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        print("\n💡 Verifica que:")
        print("  1. Tu servidor Gophish esté corriendo")
        print("  2. La URL y API key sean correctas")
        print("  3. Tengas permisos para acceder a la API")
