# 🎣 GoPhish MCP Server

<div align="center">

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![MCP](https://img.shields.io/badge/MCP-Protocol-green.svg)
![GoPhish](https://img.shields.io/badge/GoPhish-0.11.0-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**A complete MCP (Model Context Protocol) server for interacting with all GoPhish API functionalities.**

[Features](#-key-features) • [Installation](#-installation) • [Configuration](#-configuration) • [Usage](#-usage-with-claude-cursor-vscode-kiro) • [Tools](#-available-tools)

</div>

---

> **📝 Note:** This MCP has been tested and works with GoPhish version **0.11.0**. If I receive enough love 😊, I might update it with new capabilities!

---

## ✨ Key Features

- 🎯 **Complete Campaign Management**: Full CRUD + advanced analysis and statistics
- 👥 **Group Management**: Manage target user groups with search capabilities
- 📧 **Email Templates**: Create, edit and manage email templates
- 🌐 **Landing Pages**: Manage landing pages for campaigns
- 📮 **SMTP Profiles**: Configure email sending profiles
- 👤 **User Management**: Manage system users and administrators
- 📊 **Analysis and Reports**: Detailed statistics, data export and global analysis
- 🔍 **Utility Tools**: Search, validation, duplication and diagnostics

## 🚀 Quick Start

### Installation

1. Clone this repository

```bash
git clone <repository-url>
cd gophish-mcp
```

2. Install dependencies:

```bash
pip install -e .
```

### Configuration

#### Option 1: .env file (Recommended)

1. Copy the example file:

```bash
cp env.example .env
```

2. Edit `.env` with your credentials:

```bash
GOPHISH_URL=https://your-gophish-server:3333
GOPHISH_API_KEY=your-api-key-here
```

#### Option 2: Environment variables

```bash
export GOPHISH_URL="https://your-gophish-server:3333"
export GOPHISH_API_KEY="your-api-key"
```

## 💻 Usage with Claude, Cursor, VSCode, Kiro

### Step 1: Configure Credentials (One time only)

Create a `.env` file in the project directory:

```bash
cp env.example .env
# Edit .env with your real credentials
```

### Step 2: Configure MCP Client

Add the server to your MCP configuration (without credentials):

```json
{
  "mcpServers": {
    "gophish": {
      "command": "python",
      "args": ["/path/to/your/gophish-mcp/server.py"],
      "cwd": "/path/to/your/gophish-mcp",
      "disabled": false,
      "autoApprove": [
        "gophish_get_campaigns",
        "gophish_get_campaign",
        "gophish_get_active_campaigns",
        "gophish_get_completed_campaigns",
        "gophish_get_recent_campaigns",
        "gophish_get_latest_campaign",
        "gophish_get_campaigns_summary",
        "gophish_get_campaign_results",
        "gophish_get_campaign_summary",
        "gophish_get_campaign_analytics",
        "gophish_get_global_analytics",
        "gophish_get_system_status",
        "gophish_search_campaigns",
        "gophish_search_groups",
        "gophish_search_templates",
        "gophish_get_groups",
        "gophish_get_templates",
        "gophish_get_pages",
        "gophish_get_smtp_profiles",
        "gophish_get_users",
        "gophish_get_campaign_by_status",
        "gophish_get_campaign_by_date_range",
        "gophish_get_campaign_targets",
        "gophish_get_campaign_events"
      ]
    }
  }
}
```

### Step 3: Restart MCP Client

Restart your MCP client (Claude, Cursor, etc.)

> **🔒 Security Note:** Credentials are only configured in the server's `.env` file, not in the client JSON.
>
> All tools listed in `autoApprove` are read-only according to the API implementation in `server.py`. Any create, update or delete operation (`gophish_create_*`, `gophish_update_*`, `gophish_delete_*`) will always require manual approval.

## 🛠️ Tool Categories

| Category | Description |
|----------|-------------|
| **📖 READ-ONLY** | These tools only read data and are automatically approved by the MCP client |
| **✏️ WRITE** | These tools modify data and require manual approval for security |

## 📋 Available Tools

### 🎯 Campaigns (Complete Management)

#### Basic Operations

| Tool | Description | Type |
|------|-------------|------|
| `gophish_get_campaigns` | Get all campaigns | 📖 READ-ONLY |
| `gophish_get_campaign` | Get details of a specific campaign | 📖 READ-ONLY |
| `gophish_create_campaign` | Create new campaign | ✏️ WRITE |
| `gophish_update_campaign` | Update existing campaign | ✏️ WRITE |
| `gophish_delete_campaign` | Delete campaign | ✏️ WRITE |

#### Analysis and Statistics

| Tool | Description | Type |
|------|-------------|------|
| `gophish_get_latest_campaign` | Get latest campaign with complete statistics | 📖 READ-ONLY |
| `gophish_get_campaigns_summary` | Get summary of last N campaigns | 📖 READ-ONLY |
| `gophish_get_campaign_results` | Get detailed results of a campaign | 📖 READ-ONLY |
| `gophish_get_campaign_summary` | Get summary with statistics of a campaign | 📖 READ-ONLY |
| `gophish_get_campaign_analytics` | Get complete analysis of a campaign | 📖 READ-ONLY |

#### Filters and Search

| Tool | Description | Type |
|------|-------------|------|
| `gophish_get_active_campaigns` | Get active campaigns | 📖 READ-ONLY |
| `gophish_get_completed_campaigns` | Get completed campaigns | 📖 READ-ONLY |
| `gophish_get_campaign_by_status` | Filter campaigns by status | 📖 READ-ONLY |
| `gophish_get_recent_campaigns` | Get campaigns from last N days | 📖 READ-ONLY |
| `gophish_get_campaign_by_date_range` | Get campaigns in date range | 📖 READ-ONLY |
| `gophish_search_campaigns` | Search campaigns by name | 📖 READ-ONLY |

#### Utilities

| Tool | Description | Type |
|------|-------------|------|
| `gophish_get_campaign_targets` | Get all targets of a campaign | 📖 READ-ONLY |
| `gophish_get_campaign_events` | Get events of a campaign | 📖 READ-ONLY |

### 👥 Groups (Complete Management)

| Tool | Description | Type |
|------|-------------|------|
| `gophish_get_groups` | Get all groups | 📖 READ-ONLY |
| `gophish_create_group` | Create new group | ✏️ WRITE |
| `gophish_update_group` | Update existing group | ✏️ WRITE |
| `gophish_delete_group` | Delete group | ✏️ WRITE |
| `gophish_search_groups` | Search groups by name | 📖 READ-ONLY |

### 📧 Email Templates (Complete Management)

| Tool | Description | Type |
|------|-------------|------|
| `gophish_get_templates` | Get all templates | 📖 READ-ONLY |
| `gophish_create_template` | Create new template | ✏️ WRITE |
| `gophish_update_template` | Update existing template | ✏️ WRITE |
| `gophish_delete_template` | Delete template | ✏️ WRITE |
| `gophish_search_templates` | Search templates by name or subject | 📖 READ-ONLY |

### 🌐 Landing Pages (Complete Management)

| Tool | Description | Type |
|------|-------------|------|
| `gophish_get_pages` | Get all pages | 📖 READ-ONLY |
| `gophish_create_page` | Create new page | ✏️ WRITE |
| `gophish_update_page` | Update existing page | ✏️ WRITE |
| `gophish_delete_page` | Delete page | ✏️ WRITE |

### 📮 SMTP Profiles (Complete Management)

| Tool | Description | Type |
|------|-------------|------|
| `gophish_get_smtp_profiles` | Get all SMTP profiles | 📖 READ-ONLY |
| `gophish_create_smtp_profile` | Create new SMTP profile | ✏️ WRITE |
| `gophish_update_smtp_profile` | Update existing SMTP profile | ✏️ WRITE |
| `gophish_delete_smtp_profile` | Delete SMTP profile | ✏️ WRITE |

### 👤 User Management

| Tool | Description | Type |
|------|-------------|------|
| `gophish_get_users` | Get all users/administrators | 📖 READ-ONLY |
| `gophish_create_user` | Create new user | ✏️ WRITE |
| `gophish_update_user` | Update existing user | ✏️ WRITE |

### 📊 Global Analysis and Reports

| Tool | Description | Type |
|------|-------------|------|
| `gophish_get_system_status` | Get system status and general statistics | 📖 READ-ONLY |
| `gophish_get_global_analytics` | Get global analysis of all campaigns | 📖 READ-ONLY |

## 💡 Usage Examples

Once configured, you can use commands like:

### Basic Management

```
Show me all GoPhish campaigns
```

```
Create a new campaign called "Test Campaign" using template with ID 1
```

```
Update campaign with ID 5 to change its name to "Updated Campaign"
```

### Analysis and Reports

```
Show me the complete analysis of campaign with ID 3
```

```
Get global statistics of all campaigns
```

```
Show me events from campaign 2
```

### Search and Filters

```
Search campaigns containing "phishing" in the name
```

```
Show me all active campaigns
```

```
Get campaigns created in the last 7 days
```

### User Management

```
List all system users
```

```
Create a new administrator user
```

### Advanced Search

```
Search templates containing "urgent" in the subject
```

```
Find groups containing "marketing" in the name
```

## 🔒 Security

- ⚠️ Server disables SSL verification by default for local development
- ✅ Make sure to use HTTPS in production
- 🔑 Keep your API key secure and don't share it
- 🛡️ All write operations require valid authentication

## 🧪 Testing

### Run Tests

```bash
# Run all tests
python test.py all

# Run read-only tests
python test.py readonly

# Run verbose demo
python test.py demo

# Run comprehensive tests
python test.py comprehensive
```

### Testing Requirements

- ✅ GoPhish server running
- ✅ Valid credentials in `.env`
- ✅ Dependencies installed: `pip install -e .`

See `tests/README.md` for more details about testing.

## 🛠️ Utilities

### Utility Scripts

```bash
# List campaigns
python utils/list_campaigns.py
```

## 🏗️ Development

For local development:

```bash
# Install in development mode
pip install -e .

# Run server directly
python server.py

# Run tests
python test.py all
```

## 📚 Additional Resources

- [Architecture Documentation](ARCHITECTURE.md) - Learn about the server architecture
- [Test Results](TEST_RESULTS.md) - View comprehensive test results

---

<div align="center">

**Made with ❤️ for the [GoPhish](https://github.com/gophish/gophish) community**

⭐ Star this repo if you find it useful!

</div>
