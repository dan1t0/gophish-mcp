# Utility Scripts

This directory contains utility scripts for GoPhish MCP Server.

## Scripts

### `list_campaigns.py`

Lists campaigns from GoPhish with detailed information.

**Usage:**

```bash
python utils/list_campaigns.py
```

**Requirements:**

- Configure `.env` file with your GoPhish credentials
- Or set environment variables `GOPHISH_URL` and `GOPHISH_API_KEY`

**Features:**

- Shows latest campaign details
- Lists last 10 campaigns
- Displays campaign statistics
- Shows results breakdown by status

## Configuration

Make sure to configure your GoPhish credentials in `.env`:

```bash
GOPHISH_URL=https://your-gophish-server:3333
GOPHISH_API_KEY=your-api-key-here
```
