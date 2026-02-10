#!/usr/bin/env python3
"""
Fetch details for Kayako case 60281650
"""

import requests
import json
import os
from datetime import datetime

# Kayako credentials
KAYAKO_USER = os.getenv('KAYAKO_USER')
KAYAKO_PASSWORD = os.getenv('KAYAKO_PASSWORD')
KAYAKO_API = 'https://central-supportdesk.kayako.com/api/v1'

# Validate required environment variables
if not KAYAKO_USER or not KAYAKO_PASSWORD:
    print("Error: KAYAKO_USER and KAYAKO_PASSWORD environment variables must be set")
    print("\nPlease set them with:")
    print("  export KAYAKO_USER='your.email@example.com'")
    print("  export KAYAKO_PASSWORD='your_password'")
    exit(1)
def fetch_case_details(case_id):
    """Fetch detailed information for a specific case."""
    url = f"{KAYAKO_API}/cases/{case_id}.json"
    
    try:
        response = requests.get(
            url,
            auth=(KAYAKO_USER, KAYAKO_PASSWORD),
            timeout=30
        )
        response.raise_for_status()
        
        data = response.json()
        return data.get('data')
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"❌ Case {case_id} not found")
        else:
            print(f"❌ HTTP Error: {e}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def display_case_details(case):
    """Display comprehensive case information."""
    if not case:
        return
    
    print("\n" + "="*80)
    print(f"KAYAKO CASE DETAILS - #{case.get('id')}")
    print("="*80)
    
    # Basic Information
    print("\n📋 BASIC INFORMATION")
    print("-" * 80)
    print(f"Case ID:       {case.get('id')}")
    print(f"Subject:       {case.get('subject', 'N/A')}")
    print(f"Created At:    {case.get('created_at', 'N/A')}")
    print(f"Updated At:    {case.get('updated_at', 'N/A')}")
    print(f"Last Replied:  {case.get('last_replied_at', 'N/A')}")
    
    # Status Information
    print("\n📊 STATUS & PRIORITY")
    print("-" * 80)
    status = case.get('status', {})
    if isinstance(status, dict):
        print(f"Status Type:   {status.get('type', 'N/A')}")
        print(f"Status Label:  {status.get('label', 'N/A')}")
    else:
        print(f"Status:        {status}")
    
    priority = case.get('priority', {})
    if isinstance(priority, dict):
        print(f"Priority:      {priority.get('label', 'N/A')} (Level {priority.get('level', 'N/A')})")
    
    # People
    print("\n👥 PEOPLE")
    print("-" * 80)
    requester = case.get('requester', {})
    if isinstance(requester, dict):
        print(f"Requester:     {requester.get('full_name', 'N/A')}")
        print(f"  Email:       {requester.get('email', 'N/A')}")
        print(f"  ID:          {requester.get('id', 'N/A')}")
    
    assignee = case.get('assigned_agent', {})
    if isinstance(assignee, dict):
        print(f"Assigned To:   {assignee.get('full_name', 'Unassigned')}")
        print(f"  Email:       {assignee.get('email', 'N/A')}")
    else:
        print(f"Assigned To:   Unassigned")
    
    assigned_team = case.get('assigned_team', {})
    if isinstance(assigned_team, dict):
        print(f"Assigned Team: {assigned_team.get('title', 'N/A')}")
    
    # Organization & Brand
    print("\n🏢 ORGANIZATION & BRAND")
    print("-" * 80)
    org = case.get('organization', {})
    if isinstance(org, dict):
        print(f"Organization:  {org.get('name', 'N/A')}")
        print(f"  ID:          {org.get('id', 'N/A')}")
    else:
        print(f"Organization:  None")
    
    brand = case.get('brand', {})
    if isinstance(brand, dict):
        print(f"Brand:         {brand.get('name', 'N/A')}")
        print(f"  ID:          {brand.get('id', 'N/A')}")
    
    # Form & Type
    print("\n📝 FORM & TYPE")
    print("-" * 80)
    form = case.get('form', {})
    if isinstance(form, dict):
        print(f"Form:          {form.get('name', 'N/A')}")
        print(f"  ID:          {form.get('id', 'N/A')}")
    
    case_type = case.get('type', {})
    if isinstance(case_type, dict):
        print(f"Type:          {case_type.get('label', 'N/A')}")
    
    # Custom Fields
    custom_fields = case.get('custom_fields', [])
    if custom_fields:
        print("\n🔧 CUSTOM FIELDS")
        print("-" * 80)
        if isinstance(custom_fields, list):
            for field in custom_fields:
                if isinstance(field, dict):
                    name = field.get('name', 'NO_NAME')
                    value = field.get('value', 'NO_VALUE')
                    field_type = field.get('type', 'unknown')
                    
                    # Format the value based on type
                    if field_type == 'DATE' and value:
                        try:
                            # Try to format date if it's a timestamp
                            if isinstance(value, (int, float)):
                                value = datetime.fromtimestamp(value).strftime('%Y-%m-%d')
                        except:
                            pass
                    
                    print(f"{name:30} {value}")
        elif isinstance(custom_fields, dict):
            for key, value in custom_fields.items():
                print(f"{key:30} {value}")
    
    # Tags
    tags = case.get('tags', [])
    if tags:
        print("\n🏷️  TAGS")
        print("-" * 80)
        if isinstance(tags, list):
            print(", ".join([tag.get('name', tag) if isinstance(tag, dict) else str(tag) for tag in tags]))
        else:
            print(tags)
    
    # Statistics
    print("\n📈 STATISTICS")
    print("-" * 80)
    print(f"Total Posts:   {case.get('posts_count', 0)}")
    print(f"Views:         {case.get('views_count', 0)}")
    print(f"Followers:     {case.get('followers_count', 0)}")
    
    # URLs
    print("\n🔗 LINKS")
    print("-" * 80)
    print(f"Case URL:      https://central-supportdesk.kayako.com/agent/conversations/view/{case.get('id')}")
    
    # Resource URLs (if available)
    resource_url = case.get('resource_url')
    if resource_url:
        print(f"Resource URL:  {resource_url}")
    
    print("\n" + "="*80)

def fetch_case_posts(case_id):
    """Fetch all posts/messages in the case."""
    url = f"{KAYAKO_API}/cases/{case_id}/posts.json"
    
    try:
        response = requests.get(
            url,
            auth=(KAYAKO_USER, KAYAKO_PASSWORD),
            params={'limit': 100},
            timeout=30
        )
        response.raise_for_status()
        
        data = response.json()
        return data.get('data', [])
        
    except Exception as e:
        print(f"⚠️  Could not fetch posts: {e}")
        return []

def display_case_posts(posts):
    """Display case posts/conversation."""
    if not posts:
        return
    
    print("\n" + "="*80)
    print(f"CONVERSATION ({len(posts)} posts)")
    print("="*80)
    
    for idx, post in enumerate(posts, 1):
        creator = post.get('creator', {})
        creator_name = creator.get('full_name', 'Unknown') if isinstance(creator, dict) else 'Unknown'
        creator_type = creator.get('type', 'unknown') if isinstance(creator, dict) else 'unknown'
        
        # Icon based on creator type
        icon = "👤" if creator_type == "user" else "🎧"
        
        print(f"\n{icon} Post #{idx} - {creator_name} ({creator_type})")
        print(f"   Created: {post.get('created_at', 'N/A')}")
        
        # Content preview (first 500 chars)
        content_text = post.get('content_text', '')
        if content_text:
            preview = content_text[:500]
            if len(content_text) > 500:
                preview += "..."
            print(f"\n{preview}")
        
        # Attachments
        attachments = post.get('attachments', [])
        if attachments:
            print(f"\n   📎 Attachments: {len(attachments)}")
            for att in attachments:
                if isinstance(att, dict):
                    print(f"      - {att.get('name', 'Unknown')} ({att.get('size', 0)} bytes)")
        
        print("-" * 80)

def main():
    case_id = "60281650"
    
    print("\n" + "="*80)
    print(f"FETCHING KAYAKO CASE #{case_id}")
    print("="*80)
    print(f"\nAPI Endpoint: {KAYAKO_API}")
    print(f"User: {KAYAKO_USER}")
    
    # Fetch case details
    print(f"\n⏳ Fetching case details...")
    case = fetch_case_details(case_id)
    
    if case:
        print("✅ Case details retrieved successfully!")
        display_case_details(case)
        
        # Fetch posts
        print(f"\n⏳ Fetching case conversation...")
        posts = fetch_case_posts(case_id)
        
        if posts:
            print(f"✅ Retrieved {len(posts)} post(s)")
            display_case_posts(posts)
        
        # Save to JSON file for reference
        output_file = f"case_{case_id}_details.json"
        try:
            with open(output_file, 'w') as f:
                json.dump({
                    'case': case,
                    'posts': posts
                }, f, indent=2)
            print(f"\n💾 Full details saved to: {output_file}")
        except Exception as e:
            print(f"\n⚠️  Could not save to file: {e}")
            
    else:
        print("\n❌ Failed to retrieve case details")
        print("\nTroubleshooting:")
        print("1. Make sure KAYAKO_USER and KAYAKO_PASSWORD environment variables are set")
        print("2. Verify you have access to case 60281650")
        print("3. Check your network connection")
        print("\nYou can set credentials with:")
        print("   export KAYAKO_USER='your.email@example.com'")
        print("   export KAYAKO_PASSWORD='your_password'")

if __name__ == '__main__':
    main()

