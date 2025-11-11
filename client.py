"""
Gophish API Client
"""
import requests
from typing import Dict, List, Optional, Any
import json


class GophishClient:
    def __init__(self, base_url: str, api_key: str, verify_ssl: bool = False):
        """
        Initialize Gophish client
        
        Args:
            base_url: Gophish server URL (e.g., https://localhost:3333)
            api_key: API key for authentication
            verify_ssl: Whether to verify SSL certificates (default: False for local dev)
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
        # SSL verification setting
        self.session.verify = verify_ssl
        
        # Disable SSL warnings if not verifying
        if not verify_ssl:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to Gophish API"""
        url = f"{self.base_url}/api{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json() if response.content else {}
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
    
    # Campaigns
    def get_campaigns(self) -> List[Dict]:
        """Get all campaigns"""
        return self._make_request('GET', '/campaigns/')
    
    def get_campaign(self, campaign_id: int) -> Dict:
        """Get specific campaign"""
        return self._make_request('GET', f'/campaigns/{campaign_id}')
    
    def create_campaign(self, campaign_data: Dict) -> Dict:
        """Create new campaign"""
        return self._make_request('POST', '/campaigns/', campaign_data)
    
    def delete_campaign(self, campaign_id: int) -> Dict:
        """Delete campaign"""
        return self._make_request('DELETE', f'/campaigns/{campaign_id}')
    
    # Groups
    def get_groups(self) -> List[Dict]:
        """Get all groups"""
        return self._make_request('GET', '/groups/')
    
    def get_group(self, group_id: int) -> Dict:
        """Get specific group"""
        return self._make_request('GET', f'/groups/{group_id}')
    
    def create_group(self, group_data: Dict) -> Dict:
        """Create new group"""
        return self._make_request('POST', '/groups/', group_data)
    
    def delete_group(self, group_id: int) -> Dict:
        """Delete group"""
        return self._make_request('DELETE', f'/groups/{group_id}')
    
    # Templates
    def get_templates(self) -> List[Dict]:
        """Get all email templates"""
        return self._make_request('GET', '/templates/')
    
    def get_template(self, template_id: int) -> Dict:
        """Get specific template"""
        return self._make_request('GET', f'/templates/{template_id}')
    
    def create_template(self, template_data: Dict) -> Dict:
        """Create new template"""
        return self._make_request('POST', '/templates/', template_data)
    
    def delete_template(self, template_id: int) -> Dict:
        """Delete template"""
        return self._make_request('DELETE', f'/templates/{template_id}')
    
    # Landing Pages
    def get_pages(self) -> List[Dict]:
        """Get all landing pages"""
        return self._make_request('GET', '/pages/')
    
    def get_page(self, page_id: int) -> Dict:
        """Get specific landing page"""
        return self._make_request('GET', f'/pages/{page_id}')
    
    def create_page(self, page_data: Dict) -> Dict:
        """Create new landing page"""
        return self._make_request('POST', '/pages/', page_data)
    
    def delete_page(self, page_id: int) -> Dict:
        """Delete landing page"""
        return self._make_request('DELETE', f'/pages/{page_id}')
    
    # Sending Profiles
    def get_smtp(self) -> List[Dict]:
        """Get all SMTP profiles"""
        return self._make_request('GET', '/smtp/')
    
    def get_smtp_profile(self, smtp_id: int) -> Dict:
        """Get specific SMTP profile"""
        return self._make_request('GET', f'/smtp/{smtp_id}')
    
    def create_smtp_profile(self, smtp_data: Dict) -> Dict:
        """Create new SMTP profile"""
        return self._make_request('POST', '/smtp/', smtp_data)
    
    def delete_smtp_profile(self, smtp_id: int) -> Dict:
        """Delete SMTP profile"""
        return self._make_request('DELETE', f'/smtp/{smtp_id}')
    
    # Update operations (PUT)
    def update_campaign(self, campaign_id: int, campaign_data: Dict) -> Dict:
        """Update existing campaign"""
        return self._make_request('PUT', f'/campaigns/{campaign_id}', campaign_data)
    
    def update_group(self, group_id: int, group_data: Dict) -> Dict:
        """Update existing group"""
        return self._make_request('PUT', f'/groups/{group_id}', group_data)
    
    def update_template(self, template_id: int, template_data: Dict) -> Dict:
        """Update existing template"""
        return self._make_request('PUT', f'/templates/{template_id}', template_data)
    
    def update_page(self, page_id: int, page_data: Dict) -> Dict:
        """Update existing landing page"""
        return self._make_request('PUT', f'/pages/{page_id}', page_data)
    
    def update_smtp_profile(self, smtp_id: int, smtp_data: Dict) -> Dict:
        """Update existing SMTP profile"""
        return self._make_request('PUT', f'/smtp/{smtp_id}', smtp_data)
    
    # User/Admin management
    def get_users(self) -> List[Dict]:
        """Get all users/admins"""
        return self._make_request('GET', '/users/')
    
    def get_user(self, user_id: int) -> Dict:
        """Get specific user"""
        return self._make_request('GET', f'/users/{user_id}')
    
    def create_user(self, user_data: Dict) -> Dict:
        """Create new user"""
        return self._make_request('POST', '/users/', user_data)
    
    def update_user(self, user_id: int, user_data: Dict) -> Dict:
        """Update existing user"""
        return self._make_request('PUT', f'/users/{user_id}', user_data)
    
    def delete_user(self, user_id: int) -> Dict:
        """Delete user"""
        return self._make_request('DELETE', f'/users/{user_id}')
    
    # Campaign results and statistics
    def get_campaign_results(self, campaign_id: int) -> Dict:
        """Get detailed results for a campaign"""
        return self._make_request('GET', f'/campaigns/{campaign_id}/results')
    
    def get_campaign_summary(self, campaign_id: int) -> Dict:
        """Get campaign summary with statistics"""
        campaign = self.get_campaign(campaign_id)
        results = campaign.get('results', [])
        
        # Calculate statistics
        total_targets = len(results)
        status_counts = {}
        for result in results:
            status = result.get('status', 'Unknown')
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Calculate percentages
        status_percentages = {}
        for status, count in status_counts.items():
            status_percentages[status] = round((count / total_targets) * 100, 2) if total_targets > 0 else 0
        
        return {
            'campaign_id': campaign_id,
            'campaign_name': campaign.get('name'),
            'status': campaign.get('status'),
            'total_targets': total_targets,
            'status_breakdown': status_counts,
            'status_percentages': status_percentages,
            'launch_date': campaign.get('launch_date'),
            'created_date': campaign.get('created_date'),
            'completed_date': campaign.get('completed_date')
        }
    
    def get_campaign_events(self, campaign_id: int) -> List[Dict]:
        """Get events for a specific campaign"""
        campaign = self.get_campaign(campaign_id)
        return campaign.get('results', [])
    
    def get_campaign_by_status(self, status: str) -> List[Dict]:
        """Get campaigns filtered by status"""
        campaigns = self.get_campaigns()
        return [c for c in campaigns if c.get('status') == status]
    
    def get_active_campaigns(self) -> List[Dict]:
        """Get all active campaigns"""
        return self.get_campaign_by_status('In Progress')
    
    def get_completed_campaigns(self) -> List[Dict]:
        """Get all completed campaigns"""
        return self.get_campaign_by_status('Completed')
    
    def get_queued_campaigns(self) -> List[Dict]:
        """Get all queued campaigns"""
        return self.get_campaign_by_status('Queued')
    
    # System information
    def get_system_status(self) -> Dict:
        """Get system status and information"""
        try:
            # Try to get basic info by making a simple request
            campaigns = self.get_campaigns()
            groups = self.get_groups()
            templates = self.get_templates()
            pages = self.get_pages()
            smtp_profiles = self.get_smtp()
            users = self.get_users()
            
            return {
                'status': 'online',
                'campaigns_count': len(campaigns),
                'groups_count': len(groups),
                'templates_count': len(templates),
                'pages_count': len(pages),
                'smtp_profiles_count': len(smtp_profiles),
                'users_count': len(users),
                'active_campaigns': len(self.get_active_campaigns()),
                'completed_campaigns': len(self.get_completed_campaigns())
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    # Utility methods
    def search_campaigns(self, query: str) -> List[Dict]:
        """Search campaigns by name"""
        campaigns = self.get_campaigns()
        query_lower = query.lower()
        return [c for c in campaigns if query_lower in c.get('name', '').lower()]
    
    def search_groups(self, query: str) -> List[Dict]:
        """Search groups by name"""
        groups = self.get_groups()
        query_lower = query.lower()
        return [g for g in groups if query_lower in g.get('name', '').lower()]
    
    def search_templates(self, query: str) -> List[Dict]:
        """Search templates by name or subject"""
        templates = self.get_templates()
        query_lower = query.lower()
        return [t for t in templates if 
                query_lower in t.get('name', '').lower() or 
                query_lower in t.get('subject', '').lower()]
    
    def get_campaign_targets(self, campaign_id: int) -> List[Dict]:
        """Get all targets for a specific campaign"""
        campaign = self.get_campaign(campaign_id)
        targets = []
        for group in campaign.get('groups', []):
            targets.extend(group.get('targets', []))
        return targets
    
    def get_campaign_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """Get campaigns within a date range"""
        campaigns = self.get_campaigns()
        filtered = []
        for campaign in campaigns:
            created_date = campaign.get('created_date', '')
            if start_date <= created_date <= end_date:
                filtered.append(campaign)
        return filtered
    
    def get_recent_campaigns(self, days: int = 7) -> List[Dict]:
        """Get campaigns created in the last N days"""
        from datetime import datetime, timedelta
        end_date = datetime.now().isoformat()
        start_date = (datetime.now() - timedelta(days=days)).isoformat()
        return self.get_campaign_by_date_range(start_date, end_date)
    
    # Advanced analytics
    def get_campaign_analytics(self, campaign_id: int) -> Dict:
        """Get comprehensive analytics for a campaign"""
        campaign = self.get_campaign(campaign_id)
        results = campaign.get('results', [])
        
        if not results:
            return {
                'campaign_id': campaign_id,
                'campaign_name': campaign.get('name'),
                'status': campaign.get('status'),
                'message': 'No results available'
            }
        
        # Detailed analysis
        total_targets = len(results)
        status_breakdown = {}
        email_events = {}
        ip_addresses = set()
        user_agents = set()
        
        for result in results:
            status = result.get('status', 'Unknown')
            status_breakdown[status] = status_breakdown.get(status, 0) + 1
            
            # Track email events
            for event in result.get('events', []):
                event_type = event.get('message', 'Unknown')
                email_events[event_type] = email_events.get(event_type, 0) + 1
                
                # Collect IP addresses and user agents
                if 'ip' in event:
                    ip_addresses.add(event['ip'])
                if 'user_agent' in event:
                    user_agents.add(event['user_agent'])
        
        # Calculate metrics
        click_rate = (status_breakdown.get('Clicked Link', 0) / total_targets * 100) if total_targets > 0 else 0
        submit_rate = (status_breakdown.get('Submitted Data', 0) / total_targets * 100) if total_targets > 0 else 0
        email_open_rate = (status_breakdown.get('Email Opened', 0) / total_targets * 100) if total_targets > 0 else 0
        
        return {
            'campaign_id': campaign_id,
            'campaign_name': campaign.get('name'),
            'status': campaign.get('status'),
            'total_targets': total_targets,
            'status_breakdown': status_breakdown,
            'click_rate': round(click_rate, 2),
            'submit_rate': round(submit_rate, 2),
            'email_open_rate': round(email_open_rate, 2),
            'email_events': email_events,
            'unique_ips': len(ip_addresses),
            'unique_user_agents': len(user_agents),
            'launch_date': campaign.get('launch_date'),
            'created_date': campaign.get('created_date'),
            'completed_date': campaign.get('completed_date')
        }
    
    def get_global_analytics(self) -> Dict:
        """Get global analytics across all campaigns"""
        campaigns = self.get_campaigns()
        total_campaigns = len(campaigns)
        total_targets = 0
        total_clicks = 0
        total_submissions = 0
        total_emails_opened = 0
        
        status_distribution = {}
        campaign_types = {}
        
        for campaign in campaigns:
            results = campaign.get('results', [])
            total_targets += len(results)
            
            # Count events across all campaigns
            for result in results:
                status = result.get('status', 'Unknown')
                status_distribution[status] = status_distribution.get(status, 0) + 1
                
                if status == 'Clicked Link':
                    total_clicks += 1
                elif status == 'Submitted Data':
                    total_submissions += 1
                elif status == 'Email Opened':
                    total_emails_opened += 1
            
            # Track campaign types by template
            template_name = campaign.get('template', {}).get('name', 'Unknown')
            campaign_types[template_name] = campaign_types.get(template_name, 0) + 1
        
        return {
            'total_campaigns': total_campaigns,
            'total_targets': total_targets,
            'total_clicks': total_clicks,
            'total_submissions': total_submissions,
            'total_emails_opened': total_emails_opened,
            'overall_click_rate': round((total_clicks / total_targets * 100), 2) if total_targets > 0 else 0,
            'overall_submit_rate': round((total_submissions / total_targets * 100), 2) if total_targets > 0 else 0,
            'overall_email_open_rate': round((total_emails_opened / total_targets * 100), 2) if total_targets > 0 else 0,
            'status_distribution': status_distribution,
            'campaign_types': campaign_types
        }