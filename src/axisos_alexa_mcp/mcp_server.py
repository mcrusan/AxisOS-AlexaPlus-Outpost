# ==============================================================================
# File: src/axisos_alexa_mcp/mcp_server.py
# Project: AxisOS Alexa+ Outpost (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Self-hosted Streamable HTTP Model Context Protocol (MCP) Server
#              (JSON-RPC 2.0) for the Amazon Alexa+ Track.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Initial creation implementing open MCP specification.
# ==============================================================================

import json
from typing import Any, Dict, List

from .triad_bridge import BRIDGE, SovereignTriadBridge


class AlexaPlusMCPServer:
    """Implements the Open Model Context Protocol (MCP) over Streamable HTTP."""

    PROTOCOL_VERSION = "2025-03-26"

    def __init__(self, bridge: SovereignTriadBridge = BRIDGE) -> None:
        self.bridge = bridge

    def list_tools(self) -> List[Dict[str, Any]]:
        """Returns the 5 Sovereign Triad + Ring + Fire TV MCP tools for Alexa+."""
        return [
            {
                "name": "axisos_triad_telemetry",
                "description": (
                    "Read live /proc and /sys kernel telemetry, RAMGAK DDR4 memory "
                    "brackets, and Sovereign Triad (:8081, :8080, :8082) health."
                ),
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "include_daemons": {"type": "boolean", "default": True}
                    },
                },
            },
            {
                "name": "axisos_ring_perimeter_correlate",
                "description": (
                    "Correlate a Ring camera/doorbell motion event with Node 001 "
                    "(RP2350 Pico 2 W) dual-homed mesh telemetry ([💃🍪🕺])."
                ),
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "zone": {"type": "string"},
                        "event_type": {"type": "string"},
                        "confidence": {"type": "number", "default": 0.97},
                    },
                    "required": ["zone", "event_type"],
                },
            },
            {
                "name": "axisos_firetv_hud_dispatch",
                "description": (
                    "Push a 10-foot multimodal telemetry & perimeter card to the "
                    "Fire TV / Vega OS Fleet Deck HUD."
                ),
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "subtitle": {"type": "string"},
                        "priority": {"type": "string", "default": "HIGH"},
                    },
                    "required": ["title", "subtitle"],
                },
            },
            {
                "name": "axisos_worm_vault_guard",
                "description": (
                    "Commit an append-only audit checkpoint or enforce WORM "
                    "Anti-Data-Loss Vault protection against destructive operations."
                ),
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "operation": {"type": "string"},
                        "target_resource": {"type": "string"},
                    },
                    "required": ["operation", "target_resource"],
                },
            },
        ]

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Executes an MCP tool call and formats the standard MCP content response."""
        if name == "axisos_triad_telemetry":
            kernel = self.bridge.read_kernel_telemetry()
            daemons = (
                self.bridge.probe_triad_daemons()
                if arguments.get("include_daemons", True)
                else {}
            )
            payload = {"kernel_telemetry": kernel, "triad_daemons": daemons}
            return {
                "isError": False,
                "content": [{"type": "text", "text": json.dumps(payload)}],
                "structuredContent": payload,
            }

        if name == "axisos_ring_perimeter_correlate":
            res = self.bridge.correlate_ring_with_node001(
                zone=str(arguments.get("zone", "Shop North Gate")),
                event_type=str(arguments.get("event_type", "motion_detected")),
                confidence=float(arguments.get("confidence", 0.97)),
            )
            return {
                "isError": False,
                "content": [{"type": "text", "text": json.dumps(res)}],
                "structuredContent": res,
            }

        if name == "axisos_firetv_hud_dispatch":
            res = self.bridge.dispatch_firetv_hud_card(
                title=str(arguments.get("title", "AxisOS Sovereign Fleet Deck")),
                subtitle=str(arguments.get("subtitle", "Triad Nominal")),
                priority=str(arguments.get("priority", "HIGH")),
            )
            return {
                "isError": False,
                "content": [{"type": "text", "text": json.dumps(res)}],
                "structuredContent": res,
            }

        if name == "axisos_worm_vault_guard":
            res = self.bridge.enforce_worm_vault(
                operation=str(arguments.get("operation", "APPEND_CHECKPOINT")),
                target_resource=str(arguments.get("target_resource", "/mnt/raid/vault")),
            )
            return {
                "isError": not res["allowed"],
                "content": [{"type": "text", "text": json.dumps(res)}],
                "structuredContent": res,
            }

        return {
            "isError": True,
            "content": [{"type": "text", "text": f"Unknown MCP tool: {name}"}],
        }

    def handle_jsonrpc(self, request_body: Dict[str, Any]) -> Dict[str, Any]:
        """Handles a JSON-RPC 2.0 Streamable HTTP MCP request."""
        rpc_id = request_body.get("id", 1)
        method = request_body.get("method", "")
        params = request_body.get("params") or {}

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "protocolVersion": self.PROTOCOL_VERSION,
                    "capabilities": {
                        "tools": {"listChanged": False},
                        "resources": {"subscribe": False, "listChanged": False},
                        "prompts": {"listChanged": False},
                    },
                    "serverInfo": {
                        "name": "axisos-alexaplus-sovereign-outpost",
                        "version": "1.0.0",
                        "vendor": "Crusan & Co.",
                    },
                },
            }

        if method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {"tools": self.list_tools()},
            }

        if method == "tools/call":
            tool_name = params.get("name", "")
            tool_args = params.get("arguments") or {}
            result = self.call_tool(tool_name, tool_args)
            return {"jsonrpc": "2.0", "id": rpc_id, "result": result}

        if method == "resources/list":
            return {
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "resources": [
                        {
                            "uri": "axisos://triad/telemetry",
                            "name": "AxisOS Sovereign Triad Live Kernel Telemetry",
                            "mimeType": "application/json",
                        },
                        {
                            "uri": "axisos://node001/mesh",
                            "name": "Node 001 (RP2350 Pico 2 W) Mesh Heartbeat",
                            "mimeType": "application/json",
                        },
                    ]
                },
            }

        return {
            "jsonrpc": "2.0",
            "id": rpc_id,
            "error": {"code": -32601, "message": f"Method not found: {method}"},
        }


MCP_SERVER = AlexaPlusMCPServer()
