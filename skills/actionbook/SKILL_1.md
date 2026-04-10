---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 3046022100c751f8ccdcbf787c3752334f7dc8297f96377c79404ff657d18d4d62dda671440221009670fa904bfb4e5ad7c60242576e55e4acbd8eadb6cefb53d5d2f91a00688c25
    ReservedCode2: 3045022060f30d42c1177ef01480ad60d0a5a85df91ba009587bf9c401160dd353d9548a022100edd39db92a047af49683dbf09e619fe0a6de046364f0de7348d0f48929c1c6b7
description: 'Browser automation and web scraping with anti-detection stealth mode. Use when you need to: (1) Scrape Twitter/X content without login, (2) Extract data from websites with anti-bot protection, (3) Automate browser interactions (clicking, typing, screenshots), (4) Bypass JavaScript-rendered content that web_fetch cannot handle, (5) Access pages requiring cookies or sessions. Built on Chrome DevTools Protocol with fingerprint spoofing.'
name: actionbook
---

# Actionbook - Stealth Browser Automation

High-performance browser automation using your existing Chrome/Brave/Edge browser via Chrome DevTools Protocol (CDP). Zero downloads, anti-detection built-in.

## Core Capabilities

### 1. Twitter/X Scraping (No Login Required)

Extract tweets, profiles, and timelines using stealth mode:

```bash
# Open Twitter with anti-detection
actionbook --stealth browser open "https://x.com/username/status/123456789"

# Extract tweet text
actionbook browser eval 'document.body.innerText'

# Screenshot the tweet
actionbook browser screenshot tweet.png
```

### 2. JavaScript-Heavy Websites

Handle SPAs and dynamic content that web_fetch cannot parse:

```bash
# Navigate and wait for content
actionbook browser goto "https://example.com/dashboard"
actionbook browser wait '[data-loaded="true"]'

# Extract after JS execution
actionbook browser eval 'JSON.stringify(window.appState)'
```

### 3. Interactive Automation

Automate form filling, clicking, and multi-step workflows:

```bash
# Fill a search form
actionbook browser type 'input[name="q"]' "OpenClaw"
actionbook browser click 'button[type="submit"]'
actionbook browser wait '.results'

# Extract results
actionbook browser eval 'document.querySelector(".results").innerText'
```

### 4. Session & Cookie Management

Maintain login state using profiles:

```bash
# Create a dedicated profile
actionbook profile create twitter-session

# Use it (manual login once, cookies persist)
actionbook --profile twitter-session browser open "https://x.com"

# Reuse in future sessions
actionbook --profile twitter-session browser goto "https://x.com/home"
```

## Quick Reference

### Essential Commands

```bash
# Browser control
actionbook browser open <URL>        # Open URL in new browser
actionbook browser goto <URL>        # Navigate current page
actionbook browser close             # Close browser

# Content extraction
actionbook browser eval <JS>         # Execute JavaScript
actionbook browser snapshot          # Get accessibility tree
actionbook browser screenshot [PATH] # Take screenshot

# Interaction
actionbook browser click <SELECTOR>          # Click element
actionbook browser type <SELECTOR> <TEXT>   # Type into input
actionbook browser wait <SELECTOR>           # Wait for element

# Cookies & state
actionbook browser cookies list              # List all cookies
actionbook browser cookies get <NAME>        # Get specific cookie
actionbook browser cookies set <NAME> <VAL>  # Set cookie
```

### Global Flags

```bash
--stealth     # Enable anti-detection (recommended for Twitter/X)
--profile     # Use saved profile with cookies
```

## Installation

```bash
# macOS / Linux
curl -fsSL https://actionbook.dev/install.sh | bash

# or via npm
npm install -g @actionbookdev/cli

# then run setup
actionbook setup
```

## Triggers

- "Extract data from [URL]"
- "Scrape Twitter content"
- "Take screenshot of [URL]"
- "Open page and click [element]"
- "Fill form on [URL]"
- "Bypass anti-bot protection"
