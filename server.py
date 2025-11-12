#!/usr/bin/env python3
"""
GoPhish MCP server
"""
import asyncio
import json
import os
import sys
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import ServerCapabilities
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
)

# Add the current directory to the Python path
sys.path.insert(0, '.')

from client import GophishClient


class GophishMCPServer:
    def __init__(self):
        self.server = Server("gophish-mcp-server")
        self.client: Optional[GophishClient] = None
        self._setup_handlers()
    
    def _setup_handlers(self):
        # Define tools - PHASE 1: High Priority
        self.tools = [
            # 🎯 CAMPAIGN MANAGEMENT (Core)
            Tool(
                name="gophish_get_campaigns",
                description="Get all phishing campaigns from GoPhish",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            Tool(
                name="gophish_get_campaign",
                description="Get specific campaign by ID with full details",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "campaign_id": {
                            "type": "integer",
                            "description": "Campaign ID to retrieve"
                        }
                    },
                    "required": ["campaign_id"]
                }
            ),
            Tool(
                name="gophish_create_campaign",
                description="Create a new phishing campaign",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Campaign name"
                        },
                        "template_id": {
                            "type": "integer",
                            "description": "Email template ID"
                        },
                        "page_id": {
                            "type": "integer",
                            "description": "Landing page ID"
                        },
                        "smtp_id": {
                            "type": "integer",
                            "description": "SMTP profile ID"
                        },
                        "groups": {
                            "type": "array",
                            "description": "Array of group IDs to target",
                            "items": {"type": "integer"}
                        },
                        "launch_date": {
                            "type": "string",
                            "description": "Launch date (ISO format)"
                        }
                    },
                    "required": ["name", "template_id", "page_id", "smtp_id", "groups"]
                }
            ),
            Tool(
                name="gophish_update_campaign",
                description="Update existing campaign",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "campaign_id": {
                            "type": "integer",
                            "description": "Campaign ID to update"
                        },
                        "campaign_data": {
                            "type": "object",
                            "description": "Updated campaign data"
                        }
                    },
                    "required": ["campaign_id", "campaign_data"]
                }
            ),
            Tool(
                name="gophish_delete_campaign",
                description="Delete campaign by ID",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "campaign_id": {
                            "type": "integer",
                            "description": "Campaign ID to delete"
                        }
                    },
                    "required": ["campaign_id"]
                }
            ),
            Tool(
                name="gophish_get_active_campaigns",
                description="Get all active (in progress) campaigns",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            Tool(
                name="gophish_get_completed_campaigns",
                description="Get all completed campaigns",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            Tool(
                name="gophish_get_recent_campaigns",
                description="Get campaigns created in the last N days",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "days": {
                            "type": "integer",
                            "description": "Number of days to look back (default: 7)",
                            "default": 7
                        }
                    },
                    "required": []
                }
            ),
            
            # 📊 ANALYTICS AND REPORTING (Core)
            Tool(
                name="gophish_get_campaign_results",
                description="Get detailed results for a specific campaign",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "campaign_id": {
                            "type": "integer",
                            "description": "Campaign ID to get results for"
                        }
                    },
                    "required": ["campaign_id"]
                }
            ),
            Tool(
                name="gophish_get_campaign_summary",
                description="Get campaign summary with statistics",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "campaign_id": {
                            "type": "integer",
                            "description": "Campaign ID to get summary for"
                        }
                    },
                    "required": ["campaign_id"]
                }
            ),
            Tool(
                name="gophish_get_campaign_analytics",
                description="Get comprehensive analytics for a campaign",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "campaign_id": {
                            "type": "integer",
                            "description": "Campaign ID to analyze"
                        }
                    },
                    "required": ["campaign_id"]
                }
            ),
            Tool(
                name="gophish_get_global_analytics",
                description="Get global analytics across all campaigns",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            Tool(
                name="gophish_get_system_status",
                description="Get system status and general statistics",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            
            # 🔍 INTELLIGENT SEARCH (Core)
            Tool(
                name="gophish_search_campaigns",
                description="Search campaigns by name",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query for campaign names"
                        }
                    },
                    "required": ["query"]
                }
            ),
            Tool(
                name="gophish_search_groups",
                description="Search groups by name",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query for group names"
                        }
                    },
                    "required": ["query"]
                }
            ),
            Tool(
                name="gophish_search_templates",
                description="Search templates by name or subject",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query for template names or subjects"
                        }
                    },
                    "required": ["query"]
                }
            ),
            
            # 🛠️ RESOURCE MANAGEMENT (Phase 2)
            Tool(
                name="gophish_get_groups",
                description="Get all groups from GoPhish",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            Tool(
                name="gophish_create_group",
                description="Create a new group",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Group name"
                        },
                        "targets": {
                            "type": "array",
                            "description": "Array of target email addresses",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "email": {"type": "string"},
                                    "first_name": {"type": "string"},
                                    "last_name": {"type": "string"},
                                    "position": {"type": "string"}
                                },
                                "required": ["email"]
                            }
                        }
                    },
                    "required": ["name", "targets"]
                }
            ),
            Tool(
                name="gophish_get_templates",
                description="Get all email templates from GoPhish",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            Tool(
                name="gophish_create_template",
                description="Create a new email template",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Template name"
                        },
                        "subject": {
                            "type": "string",
                            "description": "Email subject"
                        },
                        "html": {
                            "type": "string",
                            "description": "HTML content of the email"
                        },
                        "text": {
                            "type": "string",
                            "description": "Text content of the email"
                        }
                    },
                    "required": ["name", "subject", "html"]
                }
            ),
            Tool(
                name="gophish_get_pages",
                description="Get all landing pages from GoPhish",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            Tool(
                name="gophish_create_page",
                description="Create a new landing page",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Page name"
                        },
                        "html": {
                            "type": "string",
                            "description": "HTML content of the page"
                        },
                        "capture_credentials": {
                            "type": "boolean",
                            "description": "Whether to capture credentials",
                            "default": True
                        },
                        "capture_passwords": {
                            "type": "boolean",
                            "description": "Whether to capture passwords",
                            "default": True
                        }
                    },
                    "required": ["name", "html"]
                }
            ),
            Tool(
                name="gophish_get_smtp_profiles",
                description="Get all SMTP profiles from GoPhish",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            Tool(
                name="gophish_create_smtp_profile",
                description="Create a new SMTP profile",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "SMTP profile name"
                        },
                        "from_address": {
                            "type": "string",
                            "description": "From email address"
                        },
                        "host": {
                            "type": "string",
                            "description": "SMTP server host"
                        },
                        "port": {
                            "type": "integer",
                            "description": "SMTP server port"
                        },
                        "username": {
                            "type": "string",
                            "description": "SMTP username"
                        },
                        "password": {
                            "type": "string",
                            "description": "SMTP password"
                        }
                    },
                    "required": ["name", "from_address", "host", "port", "username", "password"]
                }
            ),
            
            # 🔍 ADVANCED FILTERS (Phase 2)
            Tool(
                name="gophish_get_campaign_by_status",
                description="Get campaigns filtered by status",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "description": "Campaign status to filter by (e.g., 'In Progress', 'Completed', 'Queued')"
                        }
                    },
                    "required": ["status"]
                }
            ),
            Tool(
                name="gophish_get_campaign_by_date_range",
                description="Get campaigns within a date range",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "start_date": {
                            "type": "string",
                            "description": "Start date (ISO format)"
                        },
                        "end_date": {
                            "type": "string",
                            "description": "End date (ISO format)"
                        }
                    },
                    "required": ["start_date", "end_date"]
                }
            ),
            Tool(
                name="gophish_get_campaign_targets",
                description="Get all targets for a specific campaign",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "campaign_id": {
                            "type": "integer",
                            "description": "Campaign ID to get targets for"
                        }
                    },
                    "required": ["campaign_id"]
                }
            ),
            Tool(
                name="gophish_get_campaign_events",
                description="Get events for a specific campaign",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "campaign_id": {
                            "type": "integer",
                            "description": "Campaign ID to get events for"
                        }
                    },
                    "required": ["campaign_id"]
                }
            ),
            
            # 👤 USER MANAGEMENT (Phase 3)
            Tool(
                name="gophish_get_users",
                description="Get all users from GoPhish",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            Tool(
                name="gophish_create_user",
                description="Create a new user",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "username": {
                            "type": "string",
                            "description": "Username for the new user"
                        },
                        "password": {
                            "type": "string",
                            "description": "Password for the new user"
                        },
                        "role": {
                            "type": "string",
                            "description": "User role (admin, user)",
                            "default": "user"
                        }
                    },
                    "required": ["username", "password"]
                }
            ),
            Tool(
                name="gophish_update_user",
                description="Update existing user",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "integer",
                            "description": "User ID to update"
                        },
                        "user_data": {
                            "type": "object",
                            "description": "Updated user data"
                        }
                    },
                    "required": ["user_id", "user_data"]
                }
            ),
            
            # 🔄 UPDATE OPERATIONS (Phase 3)
            Tool(
                name="gophish_update_group",
                description="Update existing group",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "group_id": {
                            "type": "integer",
                            "description": "Group ID to update"
                        },
                        "group_data": {
                            "type": "object",
                            "description": "Updated group data"
                        }
                    },
                    "required": ["group_id", "group_data"]
                }
            ),
            Tool(
                name="gophish_update_template",
                description="Update existing template",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "template_id": {
                            "type": "integer",
                            "description": "Template ID to update"
                        },
                        "template_data": {
                            "type": "object",
                            "description": "Updated template data"
                        }
                    },
                    "required": ["template_id", "template_data"]
                }
            ),
            Tool(
                name="gophish_update_page",
                description="Update existing page",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "page_id": {
                            "type": "integer",
                            "description": "Page ID to update"
                        },
                        "page_data": {
                            "type": "object",
                            "description": "Updated page data"
                        }
                    },
                    "required": ["page_id", "page_data"]
                }
            ),
            Tool(
                name="gophish_update_smtp_profile",
                description="Update existing SMTP profile",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "smtp_id": {
                            "type": "integer",
                            "description": "SMTP profile ID to update"
                        },
                        "smtp_data": {
                            "type": "object",
                            "description": "Updated SMTP profile data"
                        }
                    },
                    "required": ["smtp_id", "smtp_data"]
                }
            ),
            
            # 🗑️ DELETE OPERATIONS (Phase 3)
            Tool(
                name="gophish_delete_group",
                description="Delete group by ID",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "group_id": {
                            "type": "integer",
                            "description": "Group ID to delete"
                        }
                    },
                    "required": ["group_id"]
                }
            ),
            Tool(
                name="gophish_delete_template",
                description="Delete template by ID",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "template_id": {
                            "type": "integer",
                            "description": "Template ID to delete"
                        }
                    },
                    "required": ["template_id"]
                }
            ),
            Tool(
                name="gophish_delete_page",
                description="Delete page by ID",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "page_id": {
                            "type": "integer",
                            "description": "Page ID to delete"
                        }
                    },
                    "required": ["page_id"]
                }
            ),
            Tool(
                name="gophish_delete_smtp_profile",
                description="Delete SMTP profile by ID",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "smtp_id": {
                            "type": "integer",
                            "description": "SMTP profile ID to delete"
                        }
                    },
                    "required": ["smtp_id"]
                }
            ),
            
            # 🔄 EXISTING TOOLS (backward compatibility)
            Tool(
                name="gophish_get_latest_campaign",
                description="Get the most recent campaign with full details",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            Tool(
                name="gophish_get_campaigns_summary",
                description="Get a summary of recent campaigns",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "description": "Number of campaigns to return (default: 10)",
                            "default": 10
                        }
                    },
                    "required": []
                }
            )
        ]
        
        # Register list_tools handler
        @self.server.list_tools()
        async def handle_list_tools():
            return self.tools
        
        # Register call_tool handler  
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict | None) -> list[TextContent]:
            if not self.client:
                return [TextContent(
                    type="text",
                    text="Error: GoPhish client not initialized"
                )]
            
            try:
                # 🎯 CAMPAIGN MANAGEMENT
                if name == "gophish_get_campaigns":
                    campaigns = self.client.get_campaigns()
                    return [TextContent(
                        type="text",
                        text=json.dumps(campaigns, indent=2)
                    )]
                elif name == "gophish_get_campaign":
                    campaign_id = (arguments or {}).get("campaign_id")
                    if not campaign_id:
                        return [TextContent(
                            type="text",
                            text="Error: campaign_id is required"
                        )]
                    campaign = self.client.get_campaign(campaign_id)
                    return [TextContent(
                        type="text",
                        text=json.dumps(campaign, indent=2)
                    )]
                elif name == "gophish_create_campaign":
                    campaign_data = {
                        "name": (arguments or {}).get("name"),
                        "template": {"id": (arguments or {}).get("template_id")},
                        "page": {"id": (arguments or {}).get("page_id")},
                        "smtp": {"id": (arguments or {}).get("smtp_id")},
                        "groups": [{"id": gid} for gid in (arguments or {}).get("groups", [])],
                        "launch_date": (arguments or {}).get("launch_date")
                    }
                    result = self.client.create_campaign(campaign_data)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]
                elif name == "gophish_update_campaign":
                    campaign_id = (arguments or {}).get("campaign_id")
                    campaign_data = (arguments or {}).get("campaign_data")
                    if not campaign_id or not campaign_data:
                        return [TextContent(
                            type="text",
                            text="Error: campaign_id and campaign_data are required"
                        )]
                    result = self.client.update_campaign(campaign_id, campaign_data)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]
                elif name == "gophish_delete_campaign":
                    campaign_id = (arguments or {}).get("campaign_id")
                    if not campaign_id:
                        return [TextContent(
                            type="text",
                            text="Error: campaign_id is required"
                        )]
                    result = self.client.delete_campaign(campaign_id)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]
                elif name == "gophish_get_active_campaigns":
                    campaigns = self.client.get_active_campaigns()
                    return [TextContent(
                        type="text",
                        text=json.dumps(campaigns, indent=2)
                    )]
                elif name == "gophish_get_completed_campaigns":
                    campaigns = self.client.get_completed_campaigns()
                    return [TextContent(
                        type="text",
                        text=json.dumps(campaigns, indent=2)
                    )]
                elif name == "gophish_get_recent_campaigns":
                    days = (arguments or {}).get("days", 7)
                    campaigns = self.client.get_recent_campaigns(days)
                    return [TextContent(
                        type="text",
                        text=json.dumps(campaigns, indent=2)
                    )]
                
                # 📊 ANALYTICS AND REPORTING
                elif name == "gophish_get_campaign_results":
                    campaign_id = (arguments or {}).get("campaign_id")
                    if not campaign_id:
                        return [TextContent(
                            type="text",
                            text="Error: campaign_id is required"
                        )]
                    results = self.client.get_campaign_results(campaign_id)
                    return [TextContent(
                        type="text",
                        text=json.dumps(results, indent=2)
                    )]
                elif name == "gophish_get_campaign_summary":
                    campaign_id = (arguments or {}).get("campaign_id")
                    if not campaign_id:
                        return [TextContent(
                            type="text",
                            text="Error: campaign_id is required"
                        )]
                    summary = self.client.get_campaign_summary(campaign_id)
                    return [TextContent(
                        type="text",
                        text=json.dumps(summary, indent=2)
                    )]
                elif name == "gophish_get_campaign_analytics":
                    campaign_id = (arguments or {}).get("campaign_id")
                    if not campaign_id:
                        return [TextContent(
                            type="text",
                            text="Error: campaign_id is required"
                        )]
                    analytics = self.client.get_campaign_analytics(campaign_id)
                    return [TextContent(
                        type="text",
                        text=json.dumps(analytics, indent=2)
                    )]
                elif name == "gophish_get_global_analytics":
                    analytics = self.client.get_global_analytics()
                    return [TextContent(
                        type="text",
                        text=json.dumps(analytics, indent=2)
                    )]
                elif name == "gophish_get_system_status":
                    status = self.client.get_system_status()
                    return [TextContent(
                        type="text",
                        text=json.dumps(status, indent=2)
                    )]
                
                # 🔍 INTELLIGENT SEARCH
                elif name == "gophish_search_campaigns":
                    query = (arguments or {}).get("query")
                    if not query:
                        return [TextContent(
                            type="text",
                            text="Error: query is required"
                        )]
                    results = self.client.search_campaigns(query)
                    return [TextContent(
                        type="text",
                        text=json.dumps(results, indent=2)
                    )]
                elif name == "gophish_search_groups":
                    query = (arguments or {}).get("query")
                    if not query:
                        return [TextContent(
                            type="text",
                            text="Error: query is required"
                        )]
                    results = self.client.search_groups(query)
                    return [TextContent(
                        type="text",
                        text=json.dumps(results, indent=2)
                    )]
                elif name == "gophish_search_templates":
                    query = (arguments or {}).get("query")
                    if not query:
                        return [TextContent(
                            type="text",
                            text="Error: query is required"
                        )]
                    results = self.client.search_templates(query)
                    return [TextContent(
                        type="text",
                        text=json.dumps(results, indent=2)
                    )]
                
                # 🛠️ RESOURCE MANAGEMENT (Phase 2)
                elif name == "gophish_get_groups":
                    groups = self.client.get_groups()
                    return [TextContent(
                        type="text",
                        text=json.dumps(groups, indent=2)
                    )]
                elif name == "gophish_create_group":
                    group_data = {
                        "name": (arguments or {}).get("name"),
                        "targets": (arguments or {}).get("targets", [])
                    }
                    if not group_data["name"] or not group_data["targets"]:
                        return [TextContent(
                            type="text",
                            text="Error: name and targets are required"
                        )]
                    result = self.client.create_group(group_data)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]
                elif name == "gophish_get_templates":
                    templates = self.client.get_templates()
                    return [TextContent(
                        type="text",
                        text=json.dumps(templates, indent=2)
                    )]
                elif name == "gophish_create_template":
                    template_data = {
                        "name": (arguments or {}).get("name"),
                        "subject": (arguments or {}).get("subject"),
                        "html": (arguments or {}).get("html"),
                        "text": (arguments or {}).get("text", "")
                    }
                    if not template_data["name"] or not template_data["subject"] or not template_data["html"]:
                        return [TextContent(
                            type="text",
                            text="Error: name, subject, and html are required"
                        )]
                    result = self.client.create_template(template_data)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]
                elif name == "gophish_get_pages":
                    pages = self.client.get_pages()
                    return [TextContent(
                        type="text",
                        text=json.dumps(pages, indent=2)
                    )]
                elif name == "gophish_create_page":
                    page_data = {
                        "name": (arguments or {}).get("name"),
                        "html": (arguments or {}).get("html"),
                        "capture_credentials": (arguments or {}).get("capture_credentials", True),
                        "capture_passwords": (arguments or {}).get("capture_passwords", True)
                    }
                    if not page_data["name"] or not page_data["html"]:
                        return [TextContent(
                            type="text",
                            text="Error: name and html are required"
                        )]
                    result = self.client.create_page(page_data)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]
                elif name == "gophish_get_smtp_profiles":
                    smtp_profiles = self.client.get_smtp()
                    return [TextContent(
                        type="text",
                        text=json.dumps(smtp_profiles, indent=2)
                    )]
                elif name == "gophish_create_smtp_profile":
                    smtp_data = {
                        "name": (arguments or {}).get("name"),
                        "from_address": (arguments or {}).get("from_address"),
                        "host": (arguments or {}).get("host"),
                        "port": (arguments or {}).get("port"),
                        "username": (arguments or {}).get("username"),
                        "password": (arguments or {}).get("password")
                    }
                    required_fields = ["name", "from_address", "host", "port", "username", "password"]
                    missing_fields = [field for field in required_fields if not smtp_data[field]]
                    if missing_fields:
                        return [TextContent(
                            type="text",
                            text=f"Error: Missing required fields: {', '.join(missing_fields)}"
                        )]
                    result = self.client.create_smtp_profile(smtp_data)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]
                
                # 🔍 ADVANCED FILTERS (Phase 2)
                elif name == "gophish_get_campaign_by_status":
                    status = (arguments or {}).get("status")
                    if not status:
                        return [TextContent(
                            type="text",
                            text="Error: status is required"
                        )]
                    campaigns = self.client.get_campaign_by_status(status)
                    return [TextContent(
                        type="text",
                        text=json.dumps(campaigns, indent=2)
                    )]
                elif name == "gophish_get_campaign_by_date_range":
                    start_date = (arguments or {}).get("start_date")
                    end_date = (arguments or {}).get("end_date")
                    if not start_date or not end_date:
                        return [TextContent(
                            type="text",
                            text="Error: start_date and end_date are required"
                        )]
                    campaigns = self.client.get_campaign_by_date_range(start_date, end_date)
                    return [TextContent(
                        type="text",
                        text=json.dumps(campaigns, indent=2)
                    )]
                elif name == "gophish_get_campaign_targets":
                    campaign_id = (arguments or {}).get("campaign_id")
                    if not campaign_id:
                        return [TextContent(
                            type="text",
                            text="Error: campaign_id is required"
                        )]
                    targets = self.client.get_campaign_targets(campaign_id)
                    return [TextContent(
                        type="text",
                        text=json.dumps(targets, indent=2)
                    )]
                elif name == "gophish_get_campaign_events":
                    campaign_id = (arguments or {}).get("campaign_id")
                    if not campaign_id:
                        return [TextContent(
                            type="text",
                            text="Error: campaign_id is required"
                        )]
                    events = self.client.get_campaign_events(campaign_id)
                    return [TextContent(
                        type="text",
                        text=json.dumps(events, indent=2)
                    )]
                
                # 👤 USER MANAGEMENT (Phase 3)
                elif name == "gophish_get_users":
                    users = self.client.get_users()
                    return [TextContent(
                        type="text",
                        text=json.dumps(users, indent=2)
                    )]
                elif name == "gophish_create_user":
                    user_data = {
                        "username": (arguments or {}).get("username"),
                        "password": (arguments or {}).get("password"),
                        "role": (arguments or {}).get("role", "user")
                    }
                    if not user_data["username"] or not user_data["password"]:
                        return [TextContent(
                            type="text",
                            text="Error: username and password are required"
                        )]
                    result = self.client.create_user(user_data)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]
                elif name == "gophish_update_user":
                    user_id = (arguments or {}).get("user_id")
                    user_data = (arguments or {}).get("user_data")
                    if not user_id or not user_data:
                        return [TextContent(
                            type="text",
                            text="Error: user_id and user_data are required"
                        )]
                    result = self.client.update_user(user_id, user_data)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]
                
                # 🔄 UPDATE OPERATIONS (Phase 3)
                elif name == "gophish_update_group":
                    group_id = (arguments or {}).get("group_id")
                    group_data = (arguments or {}).get("group_data")
                    if not group_id or not group_data:
                        return [TextContent(
                            type="text",
                            text="Error: group_id and group_data are required"
                        )]
                    result = self.client.update_group(group_id, group_data)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]
                elif name == "gophish_update_template":
                    template_id = (arguments or {}).get("template_id")
                    template_data = (arguments or {}).get("template_data")
                    if not template_id or not template_data:
                        return [TextContent(
                            type="text",
                            text="Error: template_id and template_data are required"
                        )]
                    result = self.client.update_template(template_id, template_data)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]
                elif name == "gophish_update_page":
                    page_id = (arguments or {}).get("page_id")
                    page_data = (arguments or {}).get("page_data")
                    if not page_id or not page_data:
                        return [TextContent(
                            type="text",
                            text="Error: page_id and page_data are required"
                        )]
                    result = self.client.update_page(page_id, page_data)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]
                elif name == "gophish_update_smtp_profile":
                    smtp_id = (arguments or {}).get("smtp_id")
                    smtp_data = (arguments or {}).get("smtp_data")
                    if not smtp_id or not smtp_data:
                        return [TextContent(
                            type="text",
                            text="Error: smtp_id and smtp_data are required"
                        )]
                    result = self.client.update_smtp_profile(smtp_id, smtp_data)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]
                
                # 🗑️ DELETE OPERATIONS (Phase 3)
                elif name == "gophish_delete_group":
                    group_id = (arguments or {}).get("group_id")
                    if not group_id:
                        return [TextContent(
                            type="text",
                            text="Error: group_id is required"
                        )]
                    result = self.client.delete_group(group_id)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]
                elif name == "gophish_delete_template":
                    template_id = (arguments or {}).get("template_id")
                    if not template_id:
                        return [TextContent(
                            type="text",
                            text="Error: template_id is required"
                        )]
                    result = self.client.delete_template(template_id)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]
                elif name == "gophish_delete_page":
                    page_id = (arguments or {}).get("page_id")
                    if not page_id:
                        return [TextContent(
                            type="text",
                            text="Error: page_id is required"
                        )]
                    result = self.client.delete_page(page_id)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]
                elif name == "gophish_delete_smtp_profile":
                    smtp_id = (arguments or {}).get("smtp_id")
                    if not smtp_id:
                        return [TextContent(
                            type="text",
                            text="Error: smtp_id is required"
                        )]
                    result = self.client.delete_smtp_profile(smtp_id)
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]
                
                # 🔄 EXISTING TOOLS (compatibility)
                elif name == "gophish_get_latest_campaign":
                    campaigns = self.client.get_campaigns()
                    if not campaigns:
                        return [TextContent(
                            type="text",
                            text="No campaigns found"
                        )]
                    latest = max(campaigns, key=lambda x: x.get('id', 0))
                    return [TextContent(
                        type="text",
                        text=json.dumps(latest, indent=2)
                    )]
                elif name == "gophish_get_campaigns_summary":
                    limit = (arguments or {}).get("limit", 10)
                    campaigns = self.client.get_campaigns()
                    summary = campaigns[:limit]
                    return [TextContent(
                        type="text",
                        text=json.dumps(summary, indent=2)
                    )]
                else:
                    return [TextContent(
                        type="text",
                        text=f"Unknown tool: {name}"
                    )]
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )]
    
    def initialize_client(self):
        """Initialize GoPhish client with environment variables"""
        base_url = os.getenv("GOPHISH_URL")
        api_key = os.getenv("GOPHISH_API_KEY")
        
        if not base_url or not api_key:
            raise ValueError("GOPHISH_URL and GOPHISH_API_KEY environment variables must be set")
        
        self.client = GophishClient(base_url, api_key)
    
    async def _handle_tool_call(self, name: str, arguments: dict | None) -> list[TextContent]:
        """Handle tool call for testing purposes"""
        if not self.client:
            return [TextContent(
                type="text",
                text="Error: GoPhish client not initialized"
            )]
        
        try:
            # 🎯 CAMPAIGN MANAGEMENT
            if name == "gophish_get_campaigns":
                campaigns = self.client.get_campaigns()
                return [TextContent(
                    type="text",
                    text=json.dumps(campaigns, indent=2)
                )]
            elif name == "gophish_get_campaign":
                campaign_id = (arguments or {}).get("campaign_id")
                if not campaign_id:
                    return [TextContent(
                        type="text",
                        text="Error: campaign_id is required"
                    )]
                campaign = self.client.get_campaign(campaign_id)
                return [TextContent(
                    type="text",
                    text=json.dumps(campaign, indent=2)
                )]
            elif name == "gophish_get_active_campaigns":
                campaigns = self.client.get_active_campaigns()
                return [TextContent(
                    type="text",
                    text=json.dumps(campaigns, indent=2)
                )]
            elif name == "gophish_get_completed_campaigns":
                campaigns = self.client.get_completed_campaigns()
                return [TextContent(
                    type="text",
                    text=json.dumps(campaigns, indent=2)
                )]
            elif name == "gophish_get_recent_campaigns":
                days = (arguments or {}).get("days", 7)
                campaigns = self.client.get_recent_campaigns(days)
                return [TextContent(
                    type="text",
                    text=json.dumps(campaigns, indent=2)
                )]
            elif name == "gophish_get_latest_campaign":
                campaigns = self.client.get_campaigns()
                if not campaigns:
                    return [TextContent(
                        type="text",
                        text="No campaigns found"
                    )]
                latest = max(campaigns, key=lambda x: x.get('id', 0))
                return [TextContent(
                    type="text",
                    text=json.dumps(latest, indent=2)
                )]
            elif name == "gophish_get_campaigns_summary":
                limit = (arguments or {}).get("limit", 10)
                campaigns = self.client.get_campaigns()
                summary = campaigns[:limit]
                return [TextContent(
                    type="text",
                    text=json.dumps(summary, indent=2)
                )]
            
            # 📊 ANALYTICS AND REPORTING
            elif name == "gophish_get_campaign_results":
                campaign_id = (arguments or {}).get("campaign_id")
                if not campaign_id:
                    return [TextContent(
                        type="text",
                        text="Error: campaign_id is required"
                    )]
                results = self.client.get_campaign_results(campaign_id)
                return [TextContent(
                    type="text",
                    text=json.dumps(results, indent=2)
                )]
            elif name == "gophish_get_campaign_summary":
                campaign_id = (arguments or {}).get("campaign_id")
                if not campaign_id:
                    return [TextContent(
                        type="text",
                        text="Error: campaign_id is required"
                    )]
                summary = self.client.get_campaign_summary(campaign_id)
                return [TextContent(
                    type="text",
                    text=json.dumps(summary, indent=2)
                )]
            elif name == "gophish_get_campaign_analytics":
                campaign_id = (arguments or {}).get("campaign_id")
                if not campaign_id:
                    return [TextContent(
                        type="text",
                        text="Error: campaign_id is required"
                    )]
                analytics = self.client.get_campaign_analytics(campaign_id)
                return [TextContent(
                    type="text",
                    text=json.dumps(analytics, indent=2)
                )]
            elif name == "gophish_get_global_analytics":
                analytics = self.client.get_global_analytics()
                return [TextContent(
                    type="text",
                    text=json.dumps(analytics, indent=2)
                )]
            elif name == "gophish_get_system_status":
                status = self.client.get_system_status()
                return [TextContent(
                    type="text",
                    text=json.dumps(status, indent=2)
                )]
            
            # 🔍 INTELLIGENT SEARCH
            elif name == "gophish_search_campaigns":
                query = (arguments or {}).get("query")
                if not query:
                    return [TextContent(
                        type="text",
                        text="Error: query is required"
                    )]
                results = self.client.search_campaigns(query)
                return [TextContent(
                    type="text",
                    text=json.dumps(results, indent=2)
                )]
            elif name == "gophish_search_groups":
                query = (arguments or {}).get("query")
                if not query:
                    return [TextContent(
                        type="text",
                        text="Error: query is required"
                    )]
                results = self.client.search_groups(query)
                return [TextContent(
                    type="text",
                    text=json.dumps(results, indent=2)
                )]
            elif name == "gophish_search_templates":
                query = (arguments or {}).get("query")
                if not query:
                    return [TextContent(
                        type="text",
                        text="Error: query is required"
                    )]
                results = self.client.search_templates(query)
                return [TextContent(
                    type="text",
                    text=json.dumps(results, indent=2)
                )]
            
            # 🛠️ RESOURCE MANAGEMENT
            elif name == "gophish_get_groups":
                groups = self.client.get_groups()
                return [TextContent(
                    type="text",
                    text=json.dumps(groups, indent=2)
                )]
            elif name == "gophish_get_templates":
                templates = self.client.get_templates()
                return [TextContent(
                    type="text",
                    text=json.dumps(templates, indent=2)
                )]
            elif name == "gophish_get_pages":
                pages = self.client.get_pages()
                return [TextContent(
                    type="text",
                    text=json.dumps(pages, indent=2)
                )]
            elif name == "gophish_get_smtp_profiles":
                smtp_profiles = self.client.get_smtp()
                return [TextContent(
                    type="text",
                    text=json.dumps(smtp_profiles, indent=2)
                )]
            
            # 👤 USER MANAGEMENT
            elif name == "gophish_get_users":
                users = self.client.get_users()
                return [TextContent(
                    type="text",
                    text=json.dumps(users, indent=2)
                )]
            
            # 🔍 ADVANCED FILTERS
            elif name == "gophish_get_campaign_by_status":
                status = (arguments or {}).get("status")
                if not status:
                    return [TextContent(
                        type="text",
                        text="Error: status is required"
                    )]
                campaigns = self.client.get_campaign_by_status(status)
                return [TextContent(
                    type="text",
                    text=json.dumps(campaigns, indent=2)
                )]
            elif name == "gophish_get_campaign_by_date_range":
                start_date = (arguments or {}).get("start_date")
                end_date = (arguments or {}).get("end_date")
                if not start_date or not end_date:
                    return [TextContent(
                        type="text",
                        text="Error: start_date and end_date are required"
                    )]
                campaigns = self.client.get_campaign_by_date_range(start_date, end_date)
                return [TextContent(
                    type="text",
                    text=json.dumps(campaigns, indent=2)
                )]
            elif name == "gophish_get_campaign_targets":
                campaign_id = (arguments or {}).get("campaign_id")
                if not campaign_id:
                    return [TextContent(
                        type="text",
                        text="Error: campaign_id is required"
                    )]
                targets = self.client.get_campaign_targets(campaign_id)
                return [TextContent(
                    type="text",
                    text=json.dumps(targets, indent=2)
                )]
            elif name == "gophish_get_campaign_events":
                campaign_id = (arguments or {}).get("campaign_id")
                if not campaign_id:
                    return [TextContent(
                        type="text",
                        text="Error: campaign_id is required"
                    )]
                events = self.client.get_campaign_events(campaign_id)
                return [TextContent(
                    type="text",
                    text=json.dumps(events, indent=2)
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"Unknown tool: {name}"
                )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error: {str(e)}"
            )]


async def main():
    """Main entry point"""
    # Load environment variables from .env file
    load_dotenv()
    
    server_instance = GophishMCPServer()
    
    # Initialize client
    try:
        server_instance.initialize_client()
    except ValueError as e:
        print(f"Warning: {e}")
    
    # Run server
    async with stdio_server() as (read_stream, write_stream):
        await server_instance.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="gophish-mcp-server",
                server_version="0.1.0",
                capabilities=ServerCapabilities(tools={"listChanged": False})
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
