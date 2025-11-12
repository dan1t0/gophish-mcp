#!/usr/bin/env python3
"""
Demo of verbose mode for GoPhish MCP tester
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_readonly_tools import GoPhishMCPTester

async def demo_verbose():
    """Demo with only a few tools to show verbose format"""
    print("🎬 VERBOSE MODE DEMO - GoPhish MCP Tester")
    print("=" * 60)
    
    tester = GoPhishMCPTester(verbose=True)
    
    if not tester.initialize_client():
        print("❌ Cannot continue without GoPhish client")
        return
    
    # Demo with only 3 representative tools
    print("\n🎯 DEMO: 3 tools with verbose output")
    print("-" * 40)
    
    # 1. Get campaigns (lots of data)
    await tester.test_tool("gophish_get_campaigns", 
                          description="Get all campaigns (verbose demo)")
    
    # 2. System status (structured data)
    await tester.test_tool("gophish_get_system_status", 
                          description="Get system status (verbose demo)")
    
    # 3. A specific campaign (detailed data)
    campaigns_result = await tester.server._handle_tool_call("gophish_get_campaigns", {})
    if campaigns_result and len(campaigns_result) > 0:
        import json
        campaigns_data = json.loads(campaigns_result[0].text)
        if isinstance(campaigns_data, list) and len(campaigns_data) > 0:
            campaign_id = campaigns_data[0].get('id')
            if campaign_id:
                await tester.test_tool("gophish_get_campaign", 
                                      arguments={"campaign_id": campaign_id},
                                      description=f"Specific campaign ID {campaign_id} (verbose demo)")
    
    print(f"\n{chr(10).join(['=' * 60, '🎉 DEMO COMPLETED', '=' * 60])}")

if __name__ == "__main__":
    asyncio.run(demo_verbose())
