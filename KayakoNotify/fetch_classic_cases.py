#!/usr/bin/env python3
"""
Simple script to fetch Kayako cases and display them with all available fields.
This will help us see what fields we CAN filter on.
"""

import requests
import json
import os
from typing import Dict, List

# Kayako credentials (from environment or hardcode for testing)
KAYAKO_USER = os.getenv('KAYAKO_USER', 'your_email@example.com')
KAYAKO_PASSWORD = os.getenv('KAYAKO_PASSWORD', 'your_password')
KAYAKO_API = 'https://central-supportdesk.kayako.com/api/v1'

def fetch_open_cases(limit=100) -> List[Dict]:
    """Fetch all open cases from Kayako."""
    url = f"{KAYAKO_API}/cases.json"
    params = {
        'status': 'open',
        'limit': limit
    }
    
    response = requests.get(
        url,
        auth=(KAYAKO_USER, KAYAKO_PASSWORD),
        params=params,
        timeout=30
    )
    response.raise_for_status()
    
    data = response.json()
    return data.get('data', [])

def display_case_info(case: Dict, index: int):
    """Display all available fields for a case."""
    print(f"\n{'='*80}")
    print(f"CASE #{index + 1}: {case.get('id')}")
    print(f"{'='*80}")
    
    # Basic info
    print(f"Subject: {case.get('subject', 'N/A')}")
    print(f"Created: {case.get('created_at', 'N/A')}")
    print(f"Updated: {case.get('updated_at', 'N/A')}")
    
    # Status
    status = case.get('status', {})
    if isinstance(status, dict):
        print(f"Status Type: {status.get('type', 'N/A')}")
        print(f"Status Label: {status.get('label', 'N/A')}")
    else:
        print(f"Status: {status}")
    
    # Priority
    priority = case.get('priority', {})
    if isinstance(priority, dict):
        print(f"Priority: {priority.get('label', 'N/A')}")
    
    # Brand
    brand = case.get('brand', {})
    if isinstance(brand, dict):
        print(f"Brand ID: {brand.get('id', 'N/A')}")
        print(f"Brand Name: {brand.get('name', 'N/A')}")
    
    # Organization
    org = case.get('organization', {})
    if isinstance(org, dict):
        print(f"Organization: {org.get('name', 'N/A')}")
    
    # Form
    form = case.get('form', {})
    if isinstance(form, dict):
        print(f"Form ID: {form.get('id', 'N/A')}")
        print(f"Form Name: {form.get('name', 'N/A')}")
    
    # Custom Fields
    custom_fields = case.get('custom_fields', [])
    if custom_fields:
        print(f"\nCustom Fields ({len(custom_fields)}):")
        if isinstance(custom_fields, list):
            for field in custom_fields:
                if isinstance(field, dict):
                    name = field.get('name', 'NO_NAME')
                    value = field.get('value', 'NO_VALUE')
                    print(f"  - {name}: {value}")
        elif isinstance(custom_fields, dict):
            for key, value in custom_fields.items():
                print(f"  - {key}: {value}")
    else:
        print("Custom Fields: None")
    
    # Assignee
    assignee = case.get('assigned_agent', {})
    if isinstance(assignee, dict):
        print(f"Assigned to: {assignee.get('full_name', 'Unassigned')}")
    
    # Requester
    requester = case.get('requester', {})
    if isinstance(requester, dict):
        print(f"Requester: {requester.get('full_name', 'N/A')}")

def find_classic_cases(cases: List[Dict]) -> List[Dict]:
    """Try to find cases related to Khoros Community Classic."""
    classic_cases = []
    
    for case in cases:
        # Check multiple fields for "classic" or "khoros" keywords
        searchable_text = []
        
        # Subject
        subject = case.get('subject', '')
        searchable_text.append(subject.lower())
        
        # Organization
        org = case.get('organization', {})
        if isinstance(org, dict):
            searchable_text.append(org.get('name', '').lower())
        
        # Brand
        brand = case.get('brand', {})
        if isinstance(brand, dict):
            searchable_text.append(brand.get('name', '').lower())
        
        # Form
        form = case.get('form', {})
        if isinstance(form, dict):
            searchable_text.append(form.get('name', '').lower())
        
        combined = ' '.join(searchable_text)
        
        # Look for Classic-related keywords
        if 'classic' in combined or ('khoros' in combined and 'aurora' not in combined):
            classic_cases.append(case)
    
    return classic_cases

def main():
    print("="*80)
    print("KAYAKO CASE FETCHER - Khoros Community Classic (Open Status)")
    print("="*80)
    
    print("\nFetching open cases from Kayako API...")
    
    try:
        all_cases = fetch_open_cases(limit=100)
        print(f"✓ Fetched {len(all_cases)} total open cases")
        
        print("\nFiltering for 'Khoros Community Classic' cases...")
        classic_cases = find_classic_cases(all_cases)
        print(f"✓ Found {len(classic_cases)} potential Classic cases")
        
        if classic_cases:
            print(f"\n{'='*80}")
            print(f"DISPLAYING {len(classic_cases)} KHOROS COMMUNITY CLASSIC CASES:")
            print(f"{'='*80}")
            
            for idx, case in enumerate(classic_cases):
                display_case_info(case, idx)
        else:
            print("\n⚠️  No Khoros Community Classic cases found!")
            print("\nShowing first 3 cases to see what fields are available:")
            for idx in range(min(3, len(all_cases))):
                display_case_info(all_cases[idx], idx)
        
        # Summary
        print(f"\n{'='*80}")
        print("SUMMARY")
        print(f"{'='*80}")
        print(f"Total open cases: {len(all_cases)}")
        print(f"Khoros Classic cases: {len(classic_cases)}")
        
        if classic_cases:
            print("\nCase IDs for hardcoding:")
            case_ids = [case.get('id') for case in classic_cases]
            print(f"  {case_ids}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you set KAYAKO_USER and KAYAKO_PASSWORD environment variables!")
        print("Or edit the script to hardcode your credentials.")

if __name__ == '__main__':
    main()





