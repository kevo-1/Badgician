# Badge Management System 🏆

An automated badge awarding and leaderboard system that syncs with Google Sheets and displays achievements on a beautiful static website.

## 🌟 Features

- **Automated Sync**: Daily synchronization with Google Sheets at midnight UTC
- **Dynamic Leaderboard**: Real-time ranking based on badge counts
- **Beautiful UI**: Modern, responsive leaderboard interface
- **GitHub Pages**: Static website deployment
- **Fair Ranking**: Tied users share the same rank, sorted lexicographically

## 📋 Available Badges

Below are all the badges that can be awarded to users:

---

## 🚀 Setup Instructions

### Prerequisites

- GitHub account with a repository
- Google account with access to Google Sheets
- Google Cloud Project with Sheets API enabled

### Step 1: Google Sheets Setup

1. Create a Google Sheet with the following columns:
   - **Full name**: The user's full name
   - **Discord username**: Their Discord handle (optional)
   - **Timestamp**: When the badge was awarded
   - **Badge name**: Name of the badge (must match SVG filename without extension)

2. Example format:
   ```
   Full name         | Discord username | Timestamp           | Badge name
   John Doe          | johndoe#1234    | 2025-10-27 10:30:00 | Contributor
   Jane Smith        | janesmith#5678  | 2025-10-27 11:00:00 | Innovator
   ```

### Step 2: Google Cloud Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the **Google Sheets API**
4. Create a service account:
   - Go to "IAM & Admin" → "Service Accounts"
   - Click "Create Service Account"
   - Give it a name and create
   - Click on the service account → "Keys" → "Add Key" → "Create new key" → "JSON"
   - Download the JSON key file

5. Share your Google Sheet with the service account email (found in the JSON file under `client_email`)

### Step 3: GitHub Repository Setup

1. Create the following directory structure:
   ```
   your-repo/
   ├── .github/
   │   └── workflows/
   │       └── sync-badges.yml
   ├── scripts/
   │   └── sync_badges.py
   ├── data/
   │   └── badges.json (will be auto-generated)
   ├── docs/
   │   └── index.html (will be auto-generated)
   |   └──badges/
   │      ├── contributor.svg
   │      ├── rising_star.svg
   │      ├── innovator.svg
   │      └── ... (add your badge SVGs here)
   └── README.md
   ```

2. Add your badge SVG files to the `badges/` folder
   - Name them using lowercase with underscores (e.g., `bug_hunter.svg`)

### Step 4: GitHub Secrets

1. Go to your repository → Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `GOOGLE_CREDENTIALS`: Paste the entire contents of your JSON key file
   - `SHEET_ID`: Your Google Sheet ID (found in the URL: `https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit`)

### Step 5: Enable GitHub Pages

1. Go to Settings → Pages
2. Source: Deploy from a branch
3. Branch: `gh-pages` (will be created automatically by the workflow)
4. Click Save

### Step 6: Initial Run

1. Go to Actions tab in your repository
2. Select "Sync Badges from Google Sheets"
3. Click "Run workflow" → "Run workflow"
4. Wait for the workflow to complete

Your leaderboard will be available at: `https://yourusername.github.io/your-repo-name/`

## 📊 How It Works

1. **Daily Sync**: GitHub Actions runs the Python script at midnight UTC
2. **Data Fetch**: Script pulls data from Google Sheets using the service account
3. **Processing**: Aggregates badges per user, calculates ranks
4. **Generation**: Creates a beautiful HTML leaderboard with badge icons
5. **Deployment**: Commits changes and deploys to GitHub Pages

## 🎨 Customization

### Adding New Badges

1. Create an SVG file for the badge
2. Add it to the `badges/` folder
3. Update the README.md with badge description
4. Add badge name to Google Sheets when awarding

### Styling the Leaderboard

Edit the CSS in `scripts/sync_badges.py` within the `generate_html()` function to customize colors, fonts, and layout.

### Changing Sync Schedule

Modify the cron expression in `.github/workflows/sync-badges.yml`:
```yaml
schedule:
  - cron: '0 0 * * *'  # Midnight UTC daily
```

[Cron expression helper](https://crontab.guru/)

## 🔧 Manual Trigger

You can manually trigger the sync workflow:
1. Go to Actions tab
2. Select "Sync Badges from Google Sheets"
3. Click "Run workflow"

## 📝 License

MIT License - feel free to use and modify for your needs.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

Made with ❤️ for recognizing awesome contributors!
