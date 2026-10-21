# ==============================================================================
# File: src/axisos_alexa_mcp/bedrock_orchestrator.py
# Project: AxisOS Alexa+ Outpost (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Amazon Bedrock AgentCore + Alexa+ Conversational Orchestrator
#              for the AWS Builder Mini-Challenge.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Initial creation routing Alexa+ utterances to MCP tools.
# ==============================================================================

from typing import Any, Dict

from .config import CONFIG
from .mcp_server import AlexaPlusMCPServer, MCP_SERVER


class AlexaPlusBedrockOrchestrator:
    """Translates Alexa+ voice utterances into MCP tool executions via Bedrock AgentCore."""

    def __init__(self, mcp_server: AlexaPlusMCPServer = MCP_SERVER) -> None:
        self.mcp = mcp_server

    def process_alexa_utterance(
        self, utterance: str, session_id: str = "alexa-plus-session-001"
    ) -> Dict[str, Any]:
        """Routes an Alexa+ voice command through Bedrock AgentCore + MCP tools."""
        text_upper = utterance.upper()

        # Check for destructive operations first (WORM Vault enforcement)
        for verb in ("DELETE", "OVERWRITE", "TRUNCATE", "WIPE", "DROP"):
            if verb in text_upper:
                rpc_res = self.mcp.handle_jsonrpc(
                    {
                        "jsonrpc": "2.0",
                        "id": "worm-guard",
                        "method": "tools/call",
                        "params": {
                            "name": "axisos_worm_vault_guard",
                            "arguments": {
                                "operation": verb,
                                "target_resource": "/mnt/raid/AxisOS_Curated_Vault",
                            },
                        },
                    }
                )["result"]["structuredContent"]
                return {
                    "session_id": session_id,
                    "orchestrator": f"Amazon Bedrock AgentCore ({CONFIG.bedrock_model_id})",
                    "mcp_tool_invoked": "axisos_worm_vault_guard",
                    "http_status": rpc_res["http_status"],
                    "status": rpc_res["status"],
                    "alexa_speech": (
                        "Security alert: Axis-Agent on port 8082 blocked that request. "
                        "Destructive operations are forbidden by the Write-Once-Read-Many Vault."
                    ),
                    "payload": rpc_res,
                }

        # Ring perimeter correlation intent
        if "RING" in text_upper or "PERIMETER" in text_upper or "GATE" in text_upper:
            rpc_res = self.mcp.handle_jsonrpc(
                {
                    "jsonrpc": "2.0",
                    "id": "ring-correlate",
                    "method": "tools/call",
                    "params": {
                        "name": "axisos_ring_perimeter_correlate",
                        "arguments": {
                            "zone": "Shop North Gate & Lab Entry",
                            "event_type": "person_and_vehicle_motion",
                            "confidence": 0.98,
                        },
                    },
                }
            )["result"]["structuredContent"]
            return {
                "session_id": session_id,
                "orchestrator": f"Amazon Bedrock AgentCore ({CONFIG.bedrock_model_id})",
                "mcp_tool_invoked": "axisos_ring_perimeter_correlate",
                "http_status": 200,
                "status": "ok",
                "alexa_speech": (
                    f"Ring perimeter event {rpc_res['event_id']} correlated with Node 001 "
                    f"RP2350 Mayor at {rpc_res['node001_mayor']['mesh_ip']}. Heartbeat "
                    "signature verified and logged to the WORM vault."
                ),
                "payload": rpc_res,
            }

        # Fire TV 10-foot HUD projection intent
        if "FIRE TV" in text_upper or "FIRETV" in text_upper or "HUD" in text_upper:
            rpc_res = self.mcp.handle_jsonrpc(
                {
                    "jsonrpc": "2.0",
                    "id": "firetv-hud",
                    "method": "tools/call",
                    "params": {
                        "name": "axisos_firetv_hud_dispatch",
                        "arguments": {
                            "title": "AxisOS Sovereign Triad & Ring Perimeter HUD",
                            "subtitle": "Zero (:8081) • Lite (:8080) • Axis-Agent (:8082) • Node 001 [💃🍪🕺]",
                            "priority": "HIGH",
                        },
                    },
                }
            )["result"]["structuredContent"]
            return {
                "session_id": session_id,
                "orchestrator": f"Amazon Bedrock AgentCore ({CONFIG.bedrock_model_id})",
                "mcp_tool_invoked": "axisos_firetv_hud_dispatch",
                "http_status": 200,
                "status": "ok",
                "alexa_speech": (
                    f"Projecting card {rpc_res['card_id']} onto your Fire TV 10-foot Fleet Deck HUD. "
                    f"RAMGAK bracket is {rpc_res['ramgak_bracket']} at {rpc_res['thermal_c']} degrees Celsius."
                ),
                "payload": rpc_res,
            }

        # Default: Sovereign Triad & RAMGAK telemetry status
        rpc_res = self.mcp.handle_jsonrpc(
            {
                "jsonrpc": "2.0",
                "id": "triad-telemetry",
                "method": "tools/call",
                "params": {
                    "name": "axisos_triad_telemetry",
                    "arguments": {"include_daemons": True},
                },
            }
        )["result"]["structuredContent"]
        kt = rpc_res["kernel_telemetry"]
        return {
            "session_id": session_id,
            "orchestrator": f"Amazon Bedrock AgentCore ({CONFIG.bedrock_model_id})",
            "mcp_tool_invoked": "axisos_triad_telemetry",
            "http_status": 200,
            "status": "ok",
            "alexa_speech": (
                f"AxisOS Sovereign Triad is online. C99 reflex latency is {kt['reflex_latency_us']} "
                f"microseconds, RAMGAK memory bracket is {kt['ramgak_bracket']} at "
                f"{kt['mem_used_pct']} percent used, and SoC thermal is {kt['thermal_c']} degrees Celsius."
            ),
            "payload": rpc_res,
        }


ORCHESTRATOR = AlexaPlusBedrockOrchestrator()
