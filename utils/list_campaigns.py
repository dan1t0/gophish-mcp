#!/usr/bin/env python3
"""
Script to list GoPhish campaigns
"""
import os
import json
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from client import GophishClient

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Get configuration from environment variables
GOPHISH_URL = os.getenv("GOPHISH_URL", "https://localhost:3333")
GOPHISH_API_KEY = os.getenv("GOPHISH_API_KEY")

if not GOPHISH_API_KEY:
    print("❌ Error: GOPHISH_API_KEY is not configured")
    print("   Set the environment variables or create a .env file")
    exit(1)

def main():
    print("Connecting to GoPhish...")
    client = GophishClient(GOPHISH_URL, GOPHISH_API_KEY)
    
    print("Fetching campaigns...\n")
    campaigns = client.get_campaigns()
    
    print(f"Total campaigns: {len(campaigns)}\n")
    
    # Sort by ID (the most recent usually has the highest ID)
    campaigns_sorted = sorted(campaigns, key=lambda x: x.get('id', 0), reverse=True)
    
    print("=" * 80)
    print("MOST RECENT CAMPAIGN")
    print("=" * 80)
    
    if campaigns_sorted:
        latest = campaigns_sorted[0]
        print(f"\nID: {latest.get('id')}")
        print(f"Name: {latest.get('name')}")
        print(f"Status: {latest.get('status')}")
        print(f"Created at: {latest.get('created_date')}")
        print(f"Launched at: {latest.get('launch_date')}")
        
        if latest.get('template'):
            print(f"Template: {latest['template'].get('name', 'N/A')}")
        
        if latest.get('page'):
            print(f"Landing page: {latest['page'].get('name', 'N/A')}")
        
        if latest.get('smtp'):
            print(f"SMTP: {latest['smtp'].get('name', 'N/A')}")
        
        if latest.get('results'):
            print(f"\nResults:")
            print(f"  Total targets: {len(latest['results'])}")
            
            # Count statuses
            statuses = {}
            for result in latest['results']:
                status = result.get('status', 'Unknown')
                statuses[status] = statuses.get(status, 0) + 1
            
            for status, count in statuses.items():
                print(f"  - {status}: {count}")
        
        print("\n" + "=" * 80)
        print("\nLATEST 10 CAMPAIGNS:")
        print("=" * 80)
        
        for i, campaign in enumerate(campaigns_sorted[:10], 1):
            print(f"\n{i}. ID: {campaign.get('id')} - {campaign.get('name')}")
            print(f"   Status: {campaign.get('status')} | Created: {campaign.get('created_date')}")
    else:
        print("No campaigns found")

if __name__ == "__main__":
    main()
