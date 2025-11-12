#!/usr/bin/env python3
"""
Test suite for GoPhish MCP read-only tools
"""
import argparse
import asyncio
import json
import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import GophishMCPServer

# Load environment variables
load_dotenv()

# ANSI color codes for beautiful output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Emojis for different data types
class Emojis:
    CAMPAIGN = "🎯"
    GROUP = "👥"
    TEMPLATE = "📧"
    PAGE = "🌐"
    SMTP = "📤"
    USER = "👤"
    EVENT = "📅"
    METRIC = "📊"
    STATUS = "🟢"
    ERROR = "❌"
    SUCCESS = "✅"
    INFO = "ℹ️"
    WARNING = "⚠️"
    JSON = "📄"
    ARRAY = "📋"
    OBJECT = "📦"

class GoPhishMCPTester:
    def __init__(self, verbose=False):
        self.server = GophishMCPServer()
        self.test_results = []
        self.passed_tests = 0
        self.failed_tests = 0
        self.verbose = verbose
        
    def initialize_client(self):
        """Initialize GoPhish client"""
        try:
            self.server.initialize_client()
            print(f"{Colors.OKGREEN}✅ GoPhish client initialized successfully{Colors.ENDC}")
            return True
        except Exception as e:
            print(f"{Colors.FAIL}❌ Error initializing client: {e}{Colors.ENDC}")
            return False
    
    def get_emoji_for_data(self, data, tool_name=""):
        """Get appropriate emoji for data type"""
        if isinstance(data, list):
            if len(data) > 0:
                first_item = data[0]
                if isinstance(first_item, dict):
                    if 'name' in first_item and 'template' in first_item:
                        return Emojis.CAMPAIGN
                    elif 'name' in first_item and 'targets' in first_item:
                        return Emojis.GROUP
                    elif 'name' in first_item and 'subject' in first_item:
                        return Emojis.TEMPLATE
                    elif 'name' in first_item and 'html' in first_item:
                        return Emojis.PAGE
                    elif 'name' in first_item and 'host' in first_item:
                        return Emojis.SMTP
                    elif 'username' in first_item:
                        return Emojis.USER
                    elif 'email' in first_item:
                        return Emojis.EVENT
                    elif 'timestamp' in first_item:
                        return Emojis.EVENT
            return Emojis.ARRAY
        elif isinstance(data, dict):
            if 'campaigns' in data or 'campaign' in tool_name.lower():
                return Emojis.CAMPAIGN
            elif 'groups' in data or 'group' in tool_name.lower():
                return Emojis.GROUP
            elif 'templates' in data or 'template' in tool_name.lower():
                return Emojis.TEMPLATE
            elif 'pages' in data or 'page' in tool_name.lower():
                return Emojis.PAGE
            elif 'smtp' in data or 'smtp' in tool_name.lower():
                return Emojis.SMTP
            elif 'users' in data or 'user' in tool_name.lower():
                return Emojis.USER
            elif 'events' in data or 'event' in tool_name.lower():
                return Emojis.EVENT
            elif 'analytics' in data or 'status' in data or 'summary' in data:
                return Emojis.METRIC
            return Emojis.OBJECT
        return Emojis.JSON
    
    def format_json_output(self, data, tool_name=""):
        """Format JSON output with colors and emojis"""
        if not self.verbose:
            return ""
        
        emoji = self.get_emoji_for_data(data, tool_name)
        
        # Pretty print JSON with colors
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        
        # Add colors to different parts
        lines = json_str.split('\n')
        colored_lines = []
        
        for line in lines:
            if line.strip().startswith('"'):
                # Key-value pairs
                if ':' in line:
                    key, value = line.split(':', 1)
                    colored_line = f"{Colors.OKCYAN}{key}{Colors.ENDC}:{Colors.OKGREEN}{value}{Colors.ENDC}"
                else:
                    colored_line = f"{Colors.OKCYAN}{line}{Colors.ENDC}"
            elif line.strip().startswith('[') or line.strip().startswith('{'):
                colored_line = f"{Colors.BOLD}{line}{Colors.ENDC}"
            elif line.strip().startswith(']') or line.strip().startswith('}'):
                colored_line = f"{Colors.BOLD}{line}{Colors.ENDC}"
            else:
                colored_line = line
            
            colored_lines.append(colored_line)
        
        formatted_json = '\n'.join(colored_lines)
        
        return f"\n{Colors.HEADER}{emoji} {Colors.BOLD}JSON Response:{Colors.ENDC}\n{Colors.OKBLUE}{'─' * 60}{Colors.ENDC}\n{formatted_json}\n{Colors.OKBLUE}{'─' * 60}{Colors.ENDC}"
    
    async def test_tool(self, tool_name, arguments=None, description=""):
        """Test a single tool"""
        print(f"\n{Colors.OKBLUE}🧪 Testing: {Colors.BOLD}{tool_name}{Colors.ENDC}")
        if description:
            print(f"   {Colors.OKCYAN}Description: {description}{Colors.ENDC}")
        
        try:
            # Get the tool handler
            tool_handler = None
            for tool in self.server.tools:
                if tool.name == tool_name:
                    tool_handler = tool
                    break
            
            if not tool_handler:
                print(f"{Colors.FAIL}❌ Tool {tool_name} not found{Colors.ENDC}")
                self.failed_tests += 1
                return False
            
            # Call the tool
            result = await self.server._handle_tool_call(tool_name, arguments or {})
            
            if result and len(result) > 0:
                response_text = result[0].text
                
                # Check if it's an error
                if response_text.startswith("Error:"):
                    print(f"{Colors.FAIL}❌ Error in {tool_name}: {response_text}{Colors.ENDC}")
                    self.failed_tests += 1
                    return False
                
                # Try to parse JSON to validate structure
                try:
                    data = json.loads(response_text)
                    data_count = len(data) if isinstance(data, (list, dict)) else 'data'
                    print(f"{Colors.OKGREEN}✅ {tool_name} - Valid response (JSON with {data_count}){Colors.ENDC}")
                    
                    # Add verbose JSON output if enabled
                    if self.verbose:
                        json_output = self.format_json_output(data, tool_name)
                        print(json_output)
                    
                    self.passed_tests += 1
                    return True
                except json.JSONDecodeError:
                    print(f"{Colors.OKGREEN}✅ {tool_name} - Valid response (text){Colors.ENDC}")
                    
                    # Add verbose text output if enabled
                    if self.verbose:
                        print(f"\n{Colors.HEADER}📄 {Colors.BOLD}Text Response:{Colors.ENDC}\n{Colors.OKBLUE}{'─' * 60}{Colors.ENDC}\n{Colors.OKGREEN}{response_text}{Colors.ENDC}\n{Colors.OKBLUE}{'─' * 60}{Colors.ENDC}")
                    
                    self.passed_tests += 1
                    return True
            else:
                print(f"{Colors.FAIL}❌ {tool_name} - No response{Colors.ENDC}")
                self.failed_tests += 1
                return False
                
        except Exception as e:
            print(f"{Colors.FAIL}❌ Error in {tool_name}: {str(e)}{Colors.ENDC}")
            self.failed_tests += 1
            return False
    
    async def run_all_readonly_tests(self):
        """Run all readonly tool tests"""
        print(f"{Colors.HEADER}🚀 STARTING TEST SUITE - READ-ONLY TOOLS{Colors.ENDC}")
        print(f"{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
        
        if not self.initialize_client():
            print(f"{Colors.FAIL}❌ Cannot continue without GoPhish client{Colors.ENDC}")
            return
        
        # 🎯 CAMPAIGN MANAGEMENT (Read-only)
        print(f"\n{Colors.OKBLUE}📋 CAMPAIGN MANAGEMENT TESTS{Colors.ENDC}")
        print(f"{Colors.OKBLUE}{'-' * 50}{Colors.ENDC}")
        
        await self.test_tool("gophish_get_campaigns", 
                           description="Get all campaigns")
        
        await self.test_tool("gophish_get_active_campaigns", 
                           description="Get active campaigns")
        
        await self.test_tool("gophish_get_completed_campaigns", 
                           description="Get completed campaigns")
        
        await self.test_tool("gophish_get_recent_campaigns", 
                           arguments={"days": 30},
                           description="Get recent campaigns (30 days)")
        
        await self.test_tool("gophish_get_latest_campaign", 
                           description="Get most recent campaign")
        
        await self.test_tool("gophish_get_campaigns_summary", 
                           arguments={"limit": 5},
                           description="Get campaign summary (5)")
        
        # 📊 ANALYTICS AND REPORTING (Read-only)
        print(f"\n{Colors.OKBLUE}📊 ANALYTICS AND REPORTING TESTS{Colors.ENDC}")
        print(f"{Colors.OKBLUE}{'-' * 50}{Colors.ENDC}")
        
        await self.test_tool("gophish_get_system_status", 
                           description="Get system status")
        
        await self.test_tool("gophish_get_global_analytics", 
                           description="Get global analytics")
        
        # 🔍 INTELLIGENT SEARCH (Read-only)
        print(f"\n{Colors.OKBLUE}🔍 INTELLIGENT SEARCH TESTS{Colors.ENDC}")
        print(f"{Colors.OKBLUE}{'-' * 50}{Colors.ENDC}")
        
        await self.test_tool("gophish_search_campaigns", 
                           arguments={"query": "test"},
                           description="Search campaigns containing 'test'")
        
        await self.test_tool("gophish_search_groups", 
                           arguments={"query": "test"},
                           description="Search groups containing 'test'")
        
        await self.test_tool("gophish_search_templates", 
                           arguments={"query": "test"},
                           description="Search templates containing 'test'")
        
        # 🛠️ RESOURCE MANAGEMENT (Read-only)
        print(f"\n{Colors.OKBLUE}🛠️ RESOURCE MANAGEMENT TESTS{Colors.ENDC}")
        print(f"{Colors.OKBLUE}{'-' * 50}{Colors.ENDC}")
        
        await self.test_tool("gophish_get_groups", 
                           description="Get all groups")
        
        await self.test_tool("gophish_get_templates", 
                           description="Get all templates")
        
        await self.test_tool("gophish_get_pages", 
                           description="Get all pages")
        
        await self.test_tool("gophish_get_smtp_profiles", 
                           description="Get SMTP profiles")
        
        # 👤 USER MANAGEMENT (Read-only)
        print(f"\n{Colors.OKBLUE}👤 USER MANAGEMENT TESTS{Colors.ENDC}")
        print(f"{Colors.OKBLUE}{'-' * 50}{Colors.ENDC}")
        
        await self.test_tool("gophish_get_users", 
                           description="Get all users")
        
        # 🔍 ADVANCED FILTERS (Read-only)
        print(f"\n{Colors.OKBLUE}🔍 ADVANCED FILTER TESTS{Colors.ENDC}")
        print(f"{Colors.OKBLUE}{'-' * 50}{Colors.ENDC}")
        
        await self.test_tool("gophish_get_campaign_by_status", 
                           arguments={"status": "In Progress"},
                           description="Filter campaigns by 'In Progress' status")
        
        await self.test_tool("gophish_get_campaign_by_status", 
                           arguments={"status": "Completed"},
                           description="Filter campaigns by 'Completed' status")
        
        # Test date range (last 30 days)
        end_date = datetime.now().isoformat()
        start_date = (datetime.now() - timedelta(days=30)).isoformat()
        
        await self.test_tool("gophish_get_campaign_by_date_range", 
                           arguments={"start_date": start_date, "end_date": end_date},
                           description="Filter campaigns by date range (last 30 days)")
        
        # 📈 TESTS WITH SPECIFIC CAMPAIGNS (if available)
        print(f"\n{Colors.OKBLUE}📈 SPECIFIC CAMPAIGN TESTS{Colors.ENDC}")
        print(f"{Colors.OKBLUE}{'-' * 50}{Colors.ENDC}")
        
        # First, get campaigns to test with specific IDs
        campaigns_result = await self.server._handle_tool_call("gophish_get_campaigns", {})
        if campaigns_result and len(campaigns_result) > 0:
            try:
                campaigns_data = json.loads(campaigns_result[0].text)
                if isinstance(campaigns_data, list) and len(campaigns_data) > 0:
                    campaign_id = campaigns_data[0].get('id')
                    if campaign_id:
                        await self.test_tool("gophish_get_campaign", 
                                           arguments={"campaign_id": campaign_id},
                                           description=f"Get specific campaign (ID: {campaign_id})")
                        
                        await self.test_tool("gophish_get_campaign_results", 
                                           arguments={"campaign_id": campaign_id},
                                           description=f"Get campaign results (ID: {campaign_id})")
                        
                        await self.test_tool("gophish_get_campaign_summary", 
                                           arguments={"campaign_id": campaign_id},
                                           description=f"Get campaign summary (ID: {campaign_id})")
                        
                        await self.test_tool("gophish_get_campaign_analytics", 
                                           arguments={"campaign_id": campaign_id},
                                           description=f"Get campaign analytics (ID: {campaign_id})")
                        
                        await self.test_tool("gophish_get_campaign_targets", 
                                           arguments={"campaign_id": campaign_id},
                                           description=f"Get campaign targets (ID: {campaign_id})")
                        
                        await self.test_tool("gophish_get_campaign_events", 
                                           arguments={"campaign_id": campaign_id},
                                           description=f"Get campaign events (ID: {campaign_id})")
                    else:
                        print("⚠️  No valid campaign ID found")
                else:
                    print("⚠️  No campaigns available for specific tests")
            except Exception as e:
                print(f"⚠️  Error processing campaigns: {e}")
        else:
            print("⚠️  Unable to retrieve campaigns for specific tests")
        
        # 📊 FINAL SUMMARY
        print(f"\n{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
        print(f"{Colors.HEADER}📊 TEST SUMMARY{Colors.ENDC}")
        print(f"{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
        
        total_tests = self.passed_tests + self.failed_tests
        success_rate = (self.passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"{Colors.OKGREEN}✅ Successful tests: {self.passed_tests}{Colors.ENDC}")
        print(f"{Colors.FAIL}❌ Failed tests: {self.failed_tests}{Colors.ENDC}")
        print(f"{Colors.OKBLUE}📊 Total tests: {total_tests}{Colors.ENDC}")
        print(f"{Colors.OKCYAN}🎯 Success rate: {success_rate:.1f}%{Colors.ENDC}")
        
        if success_rate >= 90:
            print(f"{Colors.OKGREEN}🎉 EXCELLENT! The GoPhish agent is working perfectly{Colors.ENDC}")
        elif success_rate >= 70:
            print(f"{Colors.OKGREEN}✅ GOOD! The GoPhish agent is working well{Colors.ENDC}")
        elif success_rate >= 50:
            print(f"{Colors.WARNING}⚠️  FAIR! Some tools need attention{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}❌ ISSUE! The GoPhish agent needs review{Colors.ENDC}")
        
        print(f"{Colors.BOLD}{'=' * 80}{Colors.ENDC}")

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Test suite for GoPhish MCP read-only tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage examples:
  python test_readonly_tools.py                    # Run basic tests
  python test_readonly_tools.py --verbose          # Run with detailed output
  python test_readonly_tools.py -v                 # Short form for verbose
        """
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed output with formatted JSON and colors'
    )
    
    return parser.parse_args()

async def main():
    """Main test function"""
    args = parse_arguments()
    
    print(f"{Colors.HEADER}🧪 GoPhish MCP Tester{Colors.ENDC}")
    print(f"{Colors.OKBLUE}Mode: {'Verbose' if args.verbose else 'Basic'}{Colors.ENDC}")
    print()
    
    tester = GoPhishMCPTester(verbose=args.verbose)
    await tester.run_all_readonly_tests()

if __name__ == "__main__":
    asyncio.run(main())
