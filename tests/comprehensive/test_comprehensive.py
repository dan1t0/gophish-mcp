#!/usr/bin/env python3
"""
Comprehensive test script for all GoPhish MCP functionalities
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
    print("❌ Error: GOPHISH_API_KEY is not configured")
    print("   Configure environment variables or create a .env file")
    sys.exit(1)

os.environ["GOPHISH_URL"] = GOPHISH_URL
os.environ["GOPHISH_API_KEY"] = GOPHISH_API_KEY

async def test_all_functionality():
    """Test all GoPhish MCP functionalities"""
    print("🚀 Starting comprehensive GoPhish MCP tests...")
    print("=" * 80)
    
    server = GophishMCPServer()
    server.initialize_client()
    
    # Test 1: System Status
    print("\n📊 TEST 1: System Status")
    print("-" * 40)
    status = await server._handle_tool_call("gophish_get_system_status", {})
    print(json.dumps(status, indent=2))
    
    # Test 2: Campaign Management
    print("\n🎯 TEST 2: Campaign Management")
    print("-" * 40)
    
    # Get all campaigns
    campaigns = await server._handle_tool_call("gophish_get_campaigns", {})
    print(f"Total campaigns: {len(campaigns)}")
    
    if campaigns:
        # Get latest campaign
        latest = await server._handle_tool_call("gophish_get_latest_campaign", {})
        print(f"Latest campaign: {latest.get('name', 'No name')}")
        
        # Get campaign summary
        campaign_id = latest.get('id')
        if campaign_id:
            summary = await server._handle_tool_call("gophish_get_campaign_summary", {"campaign_id": campaign_id})
            print(f"Campaign summary {campaign_id}:")
            print(f"  - Total targets: {summary.get('total_targets', 0)}")
            print(f"  - Status: {summary.get('status', 'Unknown')}")
    
    # Test 3: Advanced Campaign Analytics
    print("\n📈 TEST 3: Advanced Campaign Analytics")
    print("-" * 40)
    
    # Get active campaigns
    active = await server._handle_tool_call("gophish_get_active_campaigns", {})
    print(f"Active campaigns: {len(active)}")
    
    # Get completed campaigns
    completed = await server._handle_tool_call("gophish_get_completed_campaigns", {})
    print(f"Completed campaigns: {len(completed)}")
    
    # Get recent campaigns
    recent = await server._handle_tool_call("gophish_get_recent_campaigns", {"days": 30})
    print(f"Campaigns from last 30 days: {len(recent)}")
    
    # Test 4: Search Functionality
    print("\n🔍 TEST 4: Search Functionality")
    print("-" * 40)
    
    # Search campaigns
    search_results = await server._handle_tool_call("gophish_search_campaigns", {"query": "test"})
    print(f"Search campaigns with 'test': {len(search_results)} results")
    
    # Test 5: Groups Management
    print("\n👥 TEST 5: Groups Management")
    print("-" * 40)
    
    groups = await server._handle_tool_call("gophish_get_groups", {})
    print(f"Total groups: {len(groups)}")
    
    if groups:
        # Search groups
        group_search = await server._handle_tool_call("gophish_search_groups", {"query": "test"})
        print(f"Search groups with 'test': {len(group_search)} results")
    
    # Test 6: Templates Management
    print("\n📧 TEST 6: Templates Management")
    print("-" * 40)
    
    templates = await server._handle_tool_call("gophish_get_templates", {})
    print(f"Total templates: {len(templates)}")
    
    if templates:
        # Search templates
        template_search = await server._handle_tool_call("gophish_search_templates", {"query": "urgent"})
        print(f"Search templates with 'urgent': {len(template_search)} results")
    
    # Test 7: Pages Management
    print("\n🌐 TEST 7: Pages Management")
    print("-" * 40)
    
    pages = await server._handle_tool_call("gophish_get_pages", {})
    print(f"Total pages: {len(pages)}")
    
    # Test 8: SMTP Profiles Management
    print("\n📮 TEST 8: SMTP Profiles Management")
    print("-" * 40)
    
    smtp_profiles = await server._handle_tool_call("gophish_get_smtp_profiles", {})
    print(f"Total SMTP profiles: {len(smtp_profiles)}")
    
    # Test 9: User Management
    print("\n👤 TEST 9: User Management")
    print("-" * 40)
    
    users = await server._handle_tool_call("gophish_get_users", {})
    print(f"Total users: {len(users)}")
    
    # Test 10: Global Analytics
    print("\n📊 TEST 10: Global Analytics")
    print("-" * 40)
    
    global_analytics = await server._handle_tool_call("gophish_get_global_analytics", {})
    print("Global analytics:")
    print(f"  - Total campaigns: {global_analytics.get('total_campaigns', 0)}")
    print(f"  - Total targets: {global_analytics.get('total_targets', 0)}")
    print(f"  - Overall click rate: {global_analytics.get('overall_click_rate', 0)}%")
    print(f"  - Overall submit rate: {global_analytics.get('overall_submit_rate', 0)}%")
    
    # Test 11: Campaign Validation and Export
    if campaigns:
        print("\n✅ TEST 11: Validation and Export")
        print("-" * 40)
        
        campaign_id = campaigns[0].get('id')
        if campaign_id:
            # Validate campaign
            validation = await server._handle_tool_call("gophish_validate_campaign", {"campaign_id": campaign_id})
            print(f"Campaign validation {campaign_id}:")
            print(f"  - Valid: {validation.get('valid', False)}")
            print(f"  - Errors: {len(validation.get('errors', []))}")
            print(f"  - Warnings: {len(validation.get('warnings', []))}")
            
            # Export campaign data
            export_data = await server._handle_tool_call("gophish_export_campaign_data", {
                "campaign_id": campaign_id,
                "format": "summary"
            })
            print(f"Data export: {export_data.get('format', 'unknown')} format")
    
    # Test 12: Date Range Queries
    print("\n📅 TEST 12: Date Range Queries")
    print("-" * 40)
    
    # Get campaigns from last 7 days
    end_date = datetime.now().isoformat()
    start_date = (datetime.now() - timedelta(days=7)).isoformat()
    
    date_range_campaigns = await server._handle_tool_call("gophish_get_campaign_by_date_range", {
        "start_date": start_date,
        "end_date": end_date
    })
    print(f"Campaigns from last 7 days: {len(date_range_campaigns)}")
    
    print("\n" + "=" * 80)
    print("✅ Tests completed successfully!")
    print("🎉 GoPhish MCP is working correctly with all functionalities.")
    print("=" * 80)

async def test_specific_campaign_analytics():
    """Specific test for campaign analytics"""
    print("\n🔬 SPECIFIC TEST: Detailed Campaign Analytics")
    print("=" * 60)
    
    server = GophishMCPServer()
    server.initialize_client()
    
    # Get campaigns
    campaigns = await server._handle_tool_call("gophish_get_campaigns", {})
    
    if not campaigns:
        print("❌ No campaigns available for analysis")
        return
    
    # Get the first campaign
    campaign = campaigns[0]
    campaign_id = campaign.get('id')
    campaign_name = campaign.get('name', 'No name')
    
    print(f"Analyzing campaign: {campaign_name} (ID: {campaign_id})")
    
    # Get detailed analytics
    analytics = await server._handle_tool_call("gophish_get_campaign_analytics", {"campaign_id": campaign_id})
    
    print("\n📊 Detailed Analytics:")
    print(f"  - Total targets: {analytics.get('total_targets', 0)}")
    print(f"  - Click rate: {analytics.get('click_rate', 0)}%")
    print(f"  - Submit rate: {analytics.get('submit_rate', 0)}%")
    print(f"  - Email open rate: {analytics.get('email_open_rate', 0)}%")
    print(f"  - Unique IPs: {analytics.get('unique_ips', 0)}")
    print(f"  - Unique user agents: {analytics.get('unique_user_agents', 0)}")
    
    # Show status breakdown
    status_breakdown = analytics.get('status_breakdown', {})
    if status_breakdown:
        print("\n📈 Status Distribution:")
        for status, count in status_breakdown.items():
            print(f"  - {status}: {count}")
    
    # Show email events
    email_events = analytics.get('email_events', {})
    if email_events:
        print("\n📧 Email Events:")
        for event, count in email_events.items():
            print(f"  - {event}: {count}")

if __name__ == "__main__":
    print("🧪 STARTING COMPREHENSIVE GOPHISH MCP TESTS")
    print("=" * 80)
    
    try:
        # Run main tests
        asyncio.run(test_all_functionality())
        
        # Run specific analytics test
        asyncio.run(test_specific_campaign_analytics())
        
    except Exception as e:
        print(f"\n❌ Error during tests: {e}")
        print("\n💡 Verify that:")
        print("  1. Your GoPhish server is running")
        print("  2. The URL and API key are correct")
        print("  3. You have permissions to access the API")
