<!--
==============================================================================
File: docs/FRICTION_LOG.md
Project: AxisOS Alexa+ Outpost (Crusan & Co.)
Author: Marc F. Crusan / Crusan & Co. w/ AGY
Date: 2026-10-21
Description: Developer Friction Log for Build, Ship, Shape: Amazon Developer
             Hackathon (Alexa+ Streamable HTTP MCP, Fire TV, Ring & Bedrock).
Changelog:
  - 2026-10-21 (MFC/AGY): Created structured Friction Log for judging bonus.
==============================================================================
-->

# AxisOS Alexa+ Sovereign Outpost — Developer Friction Log
**Project:** AxisOS Alexa+ Sovereign Outpost (`Crusan & Co.`)  
**Tracks:** Alexa+ (Primary), Fire TV, Ring, AWS Builder Mini Challenge, Open Source Mini Challenge  
**Architect:** Marc F. Crusan (w/ AGY)  

---

## Friction Item 1: Testing Self-Hosted Streamable HTTP MCP Servers Without Public Alexa+ Console Inspector
- **Specific Task Attempted:** Validating our self-hosted Streamable HTTP Model Context Protocol (`2025-03-26`, JSON-RPC 2.0) server (`POST /mcp`) against Alexa+ voice utterance payloads while Alexa+ preview developer tools are restricted to select partners.
- **Steps Taken:**
  1. Implemented standard MCP JSON-RPC 2.0 methods (`initialize`, `tools/list`, `tools/call`, `resources/list`) in `src/axisos_alexa_mcp/mcp_server.py`.
  2. Looked for an official standalone Alexa+ MCP protocol test harness to simulate voice-to-MCP tool invocation payloads.
- **Expected vs. Actual Result:**
  - *Expected:* A public CLI or web-based Alexa+ MCP handshake validator that sends canonical Alexa+ session metadata alongside MCP `tools/call` requests.
  - *Actual:* Because Alexa+ preview console access is currently gated, developers must construct their own utterance-to-MCP simulator harness.
- **Severity Rating:** **Medium** (Important for developer velocity, though not a blocker).
- **Workaround Used:** We built a deterministic Alexa+ & Amazon Bedrock AgentCore utterance orchestrator (`POST /alexa/simulate` in `src/axisos_alexa_mcp/bedrock_orchestrator.py`) and a 4-stage automated verification script (`scripts/run_alexa_outpost_demo.py`) plus 7 `pytest` unit tests to validate every JSON-RPC 2.0 MCP method end-to-end.
- **Actionable Suggestion:** Publish an open-source `@amazon/alexa-mcp-inspector` CLI package (or web playground) that sends canonical Alexa+ Streamable HTTP MCP handshakes, tests `tools/list` schema compliance, and measures tool round-trip latency.

---

## Friction Item 2: Cross-Device Local LAN Discovery Between Alexa+ MCP, Ring Webhooks, and Fire TV 10-Foot Web HUD
- **Specific Task Attempted:** Pushing real-time 10-foot visual telemetry cards (`FIRETV-HUD-1`) to a Fire TV / Vega OS web runtime (`GET /firetv/hud`) immediately when an Alexa+ MCP tool (`axisos_firetv_hud_dispatch` or `axisos_ring_perimeter_correlate`) executes on the local shop LAN.
- **Steps Taken:**
  1. Configured our MCP tool `axisos_firetv_hud_dispatch` to generate 10-foot `1920x1080` telemetry cards containing live `/proc` and `/sys` kernel metrics and `Node 001` (RP2350 Pico 2 W) mesh correlation state.
  2. Evaluated how a local Fire TV device discovers a self-hosted MCP server on the same subnet (`192.168.1.0/24`) without cloud round-trips.
- **Expected vs. Actual Result:**
  - *Expected:* Native mDNS / ZeroConf discovery between Echo devices, Ring local event relays, and Fire TV / Vega OS web apps on the same LAN.
  - *Actual:* Requires manual endpoint configuration (`ALEXA_MCP_HOST` / `ALEXA_MCP_PORT`) or routing through a public HTTPS endpoint.
- **Severity Rating:** **Low / Nice-to-Have**.
- **Workaround Used:** Exposed both local loopback/LAN endpoints (`:8092/firetv/hud` and `:8092/mcp`) and our live HTTPS Cloud Run Sovereign Triad gateway (`https://axisos-sovereign-triad-4zye7tn3qq-uw.a.run.app`).
- **Actionable Suggestion:** Add native `_alexa-mcp._tcp.local` mDNS service discovery to Echo and Fire TV / Vega OS runtimes so local Streamable HTTP MCP servers are discovered automatically on hybrid/edge networks.
