# GoPhish MCP Architecture

## 🏗️ Correct Configuration Flow

### ❌ **Incorrect Configuration (Redundant)**

```
MCP Client (Claude/Cursor) 
    ↓ (env variables)
MCP Server 
    ↓ (env variables)
GoPhish API
```

**Problem**: Credentials duplicated in two places.

### ✅ **Correct Configuration (Current)**

```
MCP Client (Claude/Cursor) 
    ↓ (command only)
MCP Server 
    ↓ (.env file)
GoPhish API
```

**Advantage**: Credentials only in one place.

## 📁 **Where Credentials Go**

### 1. **MCP Server** (`.env`)

```bash
# Only here, in the server
GOPHISH_URL=https://your-server:3333
GOPHISH_API_KEY=your-real-api-key
```

### 2. **MCP Client** (JSON configuration)
```json
{
  "mcpServers": {
    "gophish": {
      "command": "python",
      "args": ["/absolute/path/to/server.py"],
      "cwd": "/path/to/server",
      "disabled": false
    }
  }
}
```

**No credentials** - Only tells how to execute the server.

## 🔄 **Execution Flow**

1. **MCP Client** reads its JSON configuration
2. **MCP Client** executes the server command
3. **MCP Server** reads its `.env` file
4. **MCP Server** connects to GoPhish with credentials
5. **MCP Client** communicates with server via MCP protocol

## 🎯 **Advantages of this Architecture**

### Security

- ✅ Credentials only in the server
- ✅ Not exposed in client configuration files
- ✅ Easy credential rotation

### Maintainability

- ✅ Single source of truth for credentials
- ✅ Client configuration independent of server
- ✅ Easy deployment in different environments

### Flexibility

- ✅ Same server can be used by multiple clients
- ✅ Different environments (dev/prod) with different `.env`
- ✅ Client doesn't need to know credentials

## 📋 **Step-by-Step Configuration**

### 1. Configure Server

```bash
# In the server directory
cp env.example .env
# Edit .env with real credentials
```

### 2. Configure Client

```json
{
  "mcpServers": {
    "gophish": {
      "command": "python",
      "args": ["/absolute/path/to/server.py"],
      "cwd": "/absolute/path/to/server"
    }
  }
}
```

### 3. Test Connection

```bash
# From the server directory
python server.py
```

## 🔧 **Troubleshooting**

### Error: "GOPHISH_URL and GOPHISH_API_KEY environment variables must be set"

- **Cause**: No `.env` file exists or is empty
- **Solution**: Create `.env` with credentials

### Error: "No such file or directory"

- **Cause**: `cwd` in JSON points to incorrect path
- **Solution**: Use correct absolute path

### Error: "Module not found"

- **Cause**: Server not installed or incorrect Python path
- **Solution**: `pip install -e .` in server directory

## 📚 **Summary**

- **Credentials**: Only in server's `.env`
- **Client**: Only execution configuration
- **Communication**: Via MCP protocol
- **Security**: Credentials isolated in server