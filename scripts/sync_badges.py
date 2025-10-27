#!/usr/bin/env python3
import json
import os
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def load_google_sheet():
    """Load data from Google Sheets."""
    creds_json = os.environ.get('GOOGLE_CREDENTIALS')
    sheet_id = os.environ.get('SHEET_ID')
    
    if not creds_json or not sheet_id:
        raise ValueError("Missing GOOGLE_CREDENTIALS or SHEET_ID environment variables")
    
    # Parse credentials
    creds_dict = json.loads(creds_json)
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    
    # Open the sheet
    sheet = client.open_by_key(sheet_id).sheet1
    return sheet.get_all_records()

def process_badges(records):
    """Process badge records and generate user leaderboard."""
    user_badges = {}
    
    for record in records:
        full_name = record.get('Full name', '').strip()
        discord = record.get('Discord username', '').strip()
        badge = record.get('Badge name', '').strip()
        timestamp = record.get('Timestamp', '')
        
        if not full_name or not badge:
            continue
        
        if full_name not in user_badges:
            user_badges[full_name] = {
                'full_name': full_name,
                'discord': discord,
                'badges': []
            }
        
        user_badges[full_name]['badges'].append({
            'name': badge,
            'timestamp': timestamp
        })
    
    # Calculate badge counts and sort
    leaderboard = []
    for user_data in user_badges.values():
        badge_count = len(user_data['badges'])
        leaderboard.append({
            'full_name': user_data['full_name'],
            'discord': user_data['discord'],
            'badge_count': badge_count,
            'badges': user_data['badges']
        })
    
    # Sort by badge count (descending), then by name (ascending)
    leaderboard.sort(key=lambda x: (-x['badge_count'], x['full_name'].lower()))
    
    # Assign ranks (same rank for ties)
    current_rank = 1
    for i, user in enumerate(leaderboard):
        if i > 0 and user['badge_count'] < leaderboard[i-1]['badge_count']:
            current_rank = i + 1
        user['rank'] = current_rank
    
    return leaderboard

def generate_html(leaderboard):
    """Generate the HTML leaderboard page."""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Badge Leaderboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 2rem;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 3rem 2rem;
            text-align: center;
        }
        
        .header h1 {
            font-size: 3rem;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .leaderboard {
            padding: 2rem;
        }
        
        .leaderboard-entry {
            display: flex;
            align-items: center;
            padding: 1.5rem;
            margin-bottom: 1rem;
            background: #f8f9fa;
            border-radius: 12px;
            transition: transform 0.2s, box-shadow 0.2s;
            border-left: 4px solid #667eea;
        }
        
        .leaderboard-entry:hover {
            transform: translateX(5px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .rank {
            font-size: 2rem;
            font-weight: bold;
            color: #667eea;
            min-width: 60px;
            text-align: center;
        }
        
        .rank-1 { color: #FFD700; }
        .rank-2 { color: #C0C0C0; }
        .rank-3 { color: #CD7F32; }
        
        .user-info {
            flex: 1;
            margin-left: 1.5rem;
        }
        
        .user-name {
            font-size: 1.4rem;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 0.25rem;
        }
        
        .discord-name {
            font-size: 0.9rem;
            color: #7289da;
            margin-bottom: 0.5rem;
        }
        
        .badge-count {
            font-size: 1.1rem;
            color: #555;
            font-weight: 500;
        }
        
        .badges {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-left: 2rem;
        }
        
        .badge {
            width: 48px;
            height: 48px;
            transition: transform 0.2s;
        }
        
        .badge:hover {
            transform: scale(1.2);
        }
        
        .last-updated {
            text-align: center;
            padding: 2rem;
            color: #666;
            font-size: 0.9rem;
        }
        
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }
            
            .leaderboard-entry {
                flex-direction: column;
                align-items: flex-start;
            }
            
            .badges {
                margin-left: 0;
                margin-top: 1rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏆 Badge Leaderboard</h1>
            <p>Top contributors and their achievements</p>
        </div>
        
        <div class="leaderboard">
"""
    
    for entry in leaderboard:
        rank_class = ''
        if entry['rank'] == 1:
            rank_class = 'rank-1'
        elif entry['rank'] == 2:
            rank_class = 'rank-2'
        elif entry['rank'] == 3:
            rank_class = 'rank-3'
        
        badges_html = ''
        for badge in entry['badges']:
            badge_filename = badge['name'].lower().replace(' ', '_') + '.svg'
            badges_html += f'            <img src="./badges/{badge_filename}" alt="{badge["name"]}" class="badge" title="{badge["name"]}">\n'
        
        discord_display = f'<div class="discord-name">@{entry["discord"]}</div>' if entry['discord'] else ''
        
        html += f"""            <div class="leaderboard-entry">
                <div class="rank {rank_class}">#{entry['rank']}</div>
                <div class="user-info">
                    <div class="user-name">{entry['full_name']}</div>
                    {discord_display}
                    <div class="badge-count">{entry['badge_count']} badge{'s' if entry['badge_count'] != 1 else ''}</div>
                </div>
                <div class="badges">
{badges_html}                </div>
            </div>
"""
    
    html += f"""        </div>
        
        <div class="last-updated">
            Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
        </div>
    </div>
</body>
</html>"""
    
    return html

def main():
    """Main execution function."""
    print("Loading data from Google Sheets...")
    records = load_google_sheet()
    print(f"Loaded {len(records)} records")
    
    print("Processing badges...")
    leaderboard = process_badges(records)
    print(f"Generated leaderboard with {len(leaderboard)} users")
    
    # Save JSON data
    os.makedirs('data', exist_ok=True)
    with open('data/badges.json', 'w') as f:
        json.dump(leaderboard, f, indent=2)
    print("Saved badges data to data/badges.json")
    
    # Generate and save HTML
    html_content = generate_html(leaderboard)
    os.makedirs('docs', exist_ok=True)
    with open('docs/index.html', 'w') as f:
        f.write(html_content)
    print("Generated leaderboard at docs/index.html")
    
    print("Sync complete!")

if __name__ == '__main__':
    main()