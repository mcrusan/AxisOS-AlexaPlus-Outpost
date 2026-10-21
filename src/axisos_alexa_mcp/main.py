# ==============================================================================
# File: src/axisos_alexa_mcp/main.py
# Project: AxisOS Alexa+ Outpost (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: FastAPI server exposing the Streamable HTTP MCP endpoint (/mcp),
#              Alexa+ Voice Simulator (/alexa/simulate), Ring Perimeter Webhook
#              (/ring/webhook), and Fire TV 10-Foot Fleet Deck HUD (/firetv/hud).
# Changelog:
#   - 2026-10-20 (MFC/AGY): Initial creation for Amazon Developer Hackathon.
# ==============================================================================

from typing import Any, Dict
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from .bedrock_orchestrator import ORCHESTRATOR
from .mcp_server import MCP_SERVER
from .triad_bridge import BRIDGE

app = FastAPI(
    title="AxisOS Alexa+ Sovereign Outpost (Streamable HTTP MCP + Fire TV HUD)",
    version="1.0.0",
    description="Crusan & Co. — AxisOS Sovereign Triad MCP Bridge for Alexa+, Fire TV, Ring, and AWS Bedrock AgentCore.",
)


class AlexaUtteranceRequest(BaseModel):
    utterance: str
    session_id: str = "alexa-plus-session-001"


class RingWebhookRequest(BaseModel):
    zone: str = "Shop North Gate"
    event_type: str = "motion_detected"
    confidence: float = 0.98


@app.get("/health")
def health_check() -> Dict[str, Any]:
    """Returns live kernel and Sovereign Triad health."""
    return {
        "status": "healthy",
        "service": "axisos-alexaplus-sovereign-outpost",
        "vendor": "Crusan & Co.",
        "pillars": ["HONEST", "AUDITABLE", "OWNED"],
        "telemetry": BRIDGE.read_kernel_telemetry(),
    }


@app.post("/mcp")
def mcp_streamable_http(request_body: Dict[str, Any]) -> JSONResponse:
    """Open Model Context Protocol (MCP) Streamable HTTP JSON-RPC 2.0 endpoint."""
    response = MCP_SERVER.handle_jsonrpc(request_body)
    return JSONResponse(content=response)


@app.post("/alexa/simulate")
def simulate_alexa_plus(req: AlexaUtteranceRequest) -> JSONResponse:
    """Simulates an Alexa+ voice utterance routed via Amazon Bedrock AgentCore to MCP."""
    result = ORCHESTRATOR.process_alexa_utterance(
        utterance=req.utterance, session_id=req.session_id
    )
    return JSONResponse(status_code=result["http_status"], content=result)


@app.post("/ring/webhook")
def ring_perimeter_webhook(req: RingWebhookRequest) -> Dict[str, Any]:
    """Ingests a Ring camera/doorbell event and correlates it with Node 001 RP2350 mesh."""
    return BRIDGE.correlate_ring_with_node001(
        zone=req.zone, event_type=req.event_type, confidence=req.confidence
    )


@app.get("/firetv/hud", response_class=HTMLResponse)
def firetv_10foot_hud() -> str:
    """Renders the 1920x1080 10-foot Fire TV / Vega OS Sovereign Fleet Deck HUD."""
    kt = BRIDGE.read_kernel_telemetry()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>AxisOS Fleet Deck — Fire TV 10-Foot Sovereign HUD</title>
  <style>
    body {{ background:#070b14; color:#e2e8f0; font-family:monospace; margin:0; padding:32px; }}
    .header {{ border-bottom:2px solid #10b981; padding-bottom:16px; margin-bottom:24px; }}
    .grid {{ display:grid; grid-template-columns:repeat(3, 1fr); gap:20px; }}
    .card {{ background:#0f172a; border:1px solid #1e293b; border-radius:8px; padding:20px; }}
    .badge {{ color:#10b981; font-weight:bold; }}
  </style>
</head>
<body>
  <div class="header">
    <h1>CRUSAN &amp; CO. — AXISOS FLEET DECK (FIRE TV / VEGA OS 10-FOOT HUD)</h1>
    <p>Alexa+ Streamable HTTP MCP Linked • AWS Bedrock AgentCore • Node 001 [💃🍪🕺]</p>
  </div>
  <div class="grid">
    <div class="card">
      <h2>Sovereign Triad Reflex</h2>
      <p>Zero-Core (:8081) • Agent-Lite (:8080) • Axis-Agent (:8082)</p>
      <p class="badge">Latency: {kt['reflex_latency_us']} µs (RAMDisk C99)</p>
    </div>
    <div class="card">
      <h2>RAMGAK Memory &amp; Thermal</h2>
      <p>Bracket: <span class="badge">{kt['ramgak_bracket']}</span> ({kt['mem_used_pct']}% used)</p>
      <p>SoC Thermal: {kt['thermal_c']} °C | NICs: {', '.join(kt['active_nics'])}</p>
    </div>
    <div class="card">
      <h2>Ring Perimeter &amp; Node 001</h2>
      <p>RP2350 Pico 2 W: 10.10.0.35 / 192.168.1.35 [💃🍪🕺]</p>
      <p>WORM Ledger Entries: {len(BRIDGE.worm_ledger)} (Protected)</p>
    </div>
  </div>
</body>
</html>"""
