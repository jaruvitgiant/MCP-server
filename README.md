# MCP Project Setup Guide

## Table of Contents
- [1. Node.js & NVM Installation](#nodejs--nvm-installation)
- [2. Gemini Client Setup](#gemini-client-setup)
- [3. MCP Server Setup](#mcp-server-setup)
- [4. SQLite Reference](#sqlite-reference)
- [5. Blender Reference](#blender-reference)
- [6. YouTube Tutorial](#youtube-tutorial)

---

## 1. Node.js & NVM Installation

**Install NVM:**
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
```

**(Optional) Reload NVM without restarting shell:**
```bash
. "$HOME/.nvm/nvm.sh"
```

**Install Node.js:**
```bash
nvm install 22
```

**Verify Node.js version:**
```bash
node -v   # Should print "v22.20.0"
```

**Verify npm version:**
```bash
npm -v    # Should print "10.9.3"
```

---

## 2. Gemini Client Setup

**Install Gemini CLI:**
```bash
npm install -g @google/gemini-cli@latest
```

**Test Gemini:**
```bash
gemini
```

**Add MCP server to Gemini:**
```bash
gemini mcp add --transport http note <ngrok url>/mcp
```

---

## 3. MCP Server Setup

**Start ngrok:**
```bash
ngrok http 8000
```

**Run the server:**
```bash
uv run .\server.py
```

---

## 4. SQLite Reference

- [Quickstart Guide (claudemcp.com)](https://www.claudemcp.com/docs/quickstart)

---

## 5. Blender Reference

- [Blender MCP GitHub](https://github.com/ahujasid/blender-mcp)

---

## 6. YouTube Tutorial

- [📺 Click here to watch the setup tutorial on YouTube](https://your-youtube-link-here)

---

> _Feel free to update the YouTube link above with your actual tutorial video._
