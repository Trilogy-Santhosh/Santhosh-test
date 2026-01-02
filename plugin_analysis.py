#!/usr/bin/env python3
"""
Plugin Analysis Report for lansweeper.stage
Analyzes plugin loading patterns over the past 24 hours
"""

import json
from datetime import datetime
from collections import Counter, defaultdict

# Raw data from Sumo Logic search
raw_data = """
2025-12-11 08:13:43,451 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/themes/25.11-release/res/feature/theme-marketing
2025-12-11 08:13:43,451 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/themes/25.11-release/res/feature/theme-support
2025-12-11 08:13:43,450 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/themes/25.11-release/res/feature/theme-hermes
2025-12-11 08:13:43,450 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/themes/25.11-release/res/feature/theme-base
2025-12-11 08:13:43,448 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/angular-li/25.11-release/res/feature/memberships
2025-12-11 08:13:43,447 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/angular-li/25.11-release/res/feature/grouphubs
2025-12-11 08:13:43,447 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/angular-li/25.11-release/res/feature/editors
2025-12-11 08:13:43,447 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/angular-li/25.11-release/res/feature/occasions
2025-12-11 08:13:43,446 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/angular-li/25.11-release/res/feature/responsivepeak
2025-12-11 08:13:43,445 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/angular-li/25.11-release/res/feature/responsivebase
2025-12-11 08:13:43,444 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/angular-li/25.11-release/res/feature/user
2025-12-11 08:13:43,444 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/angular-li/25.11-release/res/feature/tkb
2025-12-11 08:13:43,443 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/angular-li/25.11-release/res/feature/support
2025-12-11 08:13:43,443 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/angular-li/25.11-release/res/feature/search
2025-12-11 08:13:43,442 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/angular-li/25.11-release/res/feature/qanda
2025-12-11 08:13:43,442 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/angular-li/25.11-release/res/feature/nodes
2025-12-11 08:13:43,441 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/angular-li/25.11-release/res/feature/notes
2025-12-11 08:13:43,441 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/angular-li/25.11-release/res/feature/notificationfeed
2025-12-11 08:13:43,441 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/angular-li/25.11-release/res/feature/messages
2025-12-11 08:13:43,440 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/angular-li/25.11-release/res/feature/media
2025-12-11 08:13:43,440 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/angular-li/25.11-release/res/feature/kudos
2025-12-11 08:13:43,439 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/angular-li/25.11-release/res/feature/ideas
2025-12-11 08:13:43,439 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/angular-li/25.11-release/res/feature/forums
2025-12-11 08:13:43,438 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/angular-li/25.11-release/res/feature/contests
2025-12-11 08:13:43,437 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/angular-li/25.11-release/res/feature/communities
2025-12-11 08:13:43,437 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/angular-li/25.11-release/res/feature/codebook
2025-12-11 08:13:43,436 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/angular-li/25.11-release/res/feature/categories
2025-12-11 08:13:43,436 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/angular-li/25.11-release/res/feature/blogs
2025-12-11 08:13:43,435 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/angular-li/25.11-release/res/feature/avatars
2025-12-11 08:13:43,435 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/angular-li/25.11-release/res/feature/authentication
2025-12-11 08:13:43,434 +0100 [3-thread-1] INFO   [cid=, tx=, rh=, userId=-1] lithium.util.plugin.Plugin         - loading plugin: /home/lithium/customer/lansweeper.stage/plugins/core/lithium/angular-li/25.11-release/res/feature/attachments
2025-12-11 08:13:34,602 +0100 [7-thread-1] INFO   [cid=, tx=, rh=, userId=] ium.plugins.PluginLifecycleManager - Found no custom components for plugin custom.lansweeper.lansweeper.stage while scanning from root package
"""

def extract_plugins(log_data):
    """Extract plugin paths from log data"""
    plugins = []
    for line in log_data.strip().split('\n'):
        if 'loading plugin:' in line:
            plugin_path = line.split('loading plugin: ')[-1].strip()
            timestamp_str = line.split(' [')[0].strip()
            try:
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f %z')
            except:
                timestamp = None
            plugins.append({
                'path': plugin_path,
                'timestamp': timestamp,
                'name': plugin_path.split('/')[-1] if '/' in plugin_path else plugin_path,
                'category': categorize_plugin(plugin_path)
            })
    return plugins

def categorize_plugin(plugin_path):
    """Categorize plugin by type"""
    if '/themes/' in plugin_path:
        return 'Theme'
    elif '/angular-li/' in plugin_path:
        return 'Angular Feature'
    elif '/custom/' in plugin_path or 'custom.' in plugin_path:
        return 'Custom'
    else:
        return 'Core'

def analyze_plugins(plugins):
    """Analyze plugin data and generate statistics"""
    
    # Count by category
    category_counts = Counter([p['category'] for p in plugins])
    
    # Count by feature name
    feature_counts = Counter([p['name'] for p in plugins])
    
    # Group by version
    versions = defaultdict(list)
    for p in plugins:
        if '25.11-release' in p['path']:
            versions['25.11-release'].append(p['name'])
        else:
            versions['other'].append(p['name'])
    
    return {
        'total_plugins': len(plugins),
        'unique_plugins': len(set(p['path'] for p in plugins)),
        'category_counts': dict(category_counts),
        'feature_counts': dict(feature_counts),
        'versions': dict(versions)
    }

def generate_report(plugins, stats):
    """Generate comprehensive analysis report"""
    
    report = []
    report.append("=" * 80)
    report.append("PLUGIN ANALYSIS REPORT - lansweeper.stage")
    report.append(f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Time Range: Past 24 hours")
    report.append("=" * 80)
    report.append("")
    
    report.append("SUMMARY")
    report.append("-" * 80)
    report.append(f"Total Plugin Load Events: {stats['total_plugins']}")
    report.append(f"Unique Plugins: {stats['unique_plugins']}")
    report.append("")
    
    report.append("PLUGINS BY CATEGORY")
    report.append("-" * 80)
    for category, count in sorted(stats['category_counts'].items(), key=lambda x: -x[1]):
        report.append(f"  {category:<20} {count:>3} plugins")
    report.append("")
    
    report.append("VERSION INFORMATION")
    report.append("-" * 80)
    report.append(f"  Version 25.11-release: {len(stats['versions'].get('25.11-release', []))} plugins")
    report.append("")
    
    report.append("THEME PLUGINS")
    report.append("-" * 80)
    theme_plugins = [p for p in plugins if p['category'] == 'Theme']
    for plugin in sorted(set(p['name'] for p in theme_plugins)):
        report.append(f"  ✓ {plugin}")
    report.append("")
    
    report.append("ANGULAR FEATURE PLUGINS")
    report.append("-" * 80)
    angular_plugins = [p for p in plugins if p['category'] == 'Angular Feature']
    for plugin in sorted(set(p['name'] for p in angular_plugins)):
        report.append(f"  ✓ {plugin}")
    report.append("")
    
    report.append("ISSUES & WARNINGS")
    report.append("-" * 80)
    custom_plugins = [p for p in plugins if p['category'] == 'Custom']
    if custom_plugins:
        report.append(f"  ⚠ Found reference to custom plugin without components:")
        for cp in set(p['path'] for p in custom_plugins):
            report.append(f"    - {cp}")
    else:
        report.append("  ✓ No issues detected")
    report.append("")
    
    report.append("KEY FINDINGS")
    report.append("-" * 80)
    report.append(f"  • Instance is running version 25.11-release")
    report.append(f"  • {len([p for p in plugins if 'theme' in p['name'].lower()])} theme plugins loaded")
    report.append(f"  • {len([p for p in plugins if p['category'] == 'Angular Feature'])} Angular features enabled")
    report.append(f"  • Custom plugin 'custom.lansweeper.lansweeper.stage' has no components")
    report.append("")
    
    report.append("=" * 80)
    
    return '\n'.join(report)

def main():
    # Extract plugins from logs
    plugins = extract_plugins(raw_data)
    
    # Analyze
    stats = analyze_plugins(plugins)
    
    # Generate report
    report = generate_report(plugins, stats)
    
    # Print report
    print(report)
    
    # Save to file
    with open('plugin_analysis_report.txt', 'w') as f:
        f.write(report)
    print("\n✓ Report saved to: plugin_analysis_report.txt")
    
    # Also save raw data as JSON
    with open('plugin_data.json', 'w') as f:
        json.dump({
            'plugins': [{'path': p['path'], 'name': p['name'], 'category': p['category']} 
                       for p in plugins],
            'statistics': stats
        }, f, indent=2)
    print("✓ Raw data saved to: plugin_data.json")

if __name__ == '__main__':
    main()




