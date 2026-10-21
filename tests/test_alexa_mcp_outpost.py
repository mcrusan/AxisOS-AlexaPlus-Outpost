# ==============================================================================
# File: tests/test_alexa_mcp_outpost.py
# Project: AxisOS Alexa+ Outpost (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Unit test suite for AxisOS Alexa+ Streamable HTTP MCP Server,
#              Amazon Bedrock AgentCore orchestrator, Fire TV HUD, Ring
#              correlation, and WORM Anti-Data-Loss Vault protection.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Initial creation (7 unit tests).
# ==============================================================================

from axisos_alexa_mcp.bedrock_orchestrator import AlexaPlusBedrockOrchestrator
from axisos_alexa_mcp.mcp_server import AlexaPlusMCPServer
from axisos_alexa_mcp.triad_bridge import SovereignTriadBridge


def test_mcp_initialize_protocol() -> None:
    mcp = AlexaPlusMCPServer(SovereignTriadBridge())
    res = mcp.handle_jsonrpc({"jsonrpc": "2.0", "id": 10, "method": "initialize"})
    assert res["jsonrpc"] == "2.0"
    assert res["id"] == 10
    assert res["result"]["serverInfo"]["vendor"] == "Crusan & Co."


def test_mcp_tools_list_registers_four_sovereign_tools() -> None:
    mcp = AlexaPlusMCPServer(SovereignTriadBridge())
    res = mcp.handle_jsonrpc({"jsonrpc": "2.0", "id": 11, "method": "tools/list"})
    names = [t["name"] for t in res["result"]["tools"]]
    assert "axisos_triad_telemetry" in names
    assert "axisos_ring_perimeter_correlate" in names
    assert "axisos_firetv_hud_dispatch" in names
    assert "axisos_worm_vault_guard" in names


def test_live_kernel_telemetry_ground_truth() -> None:
    bridge = SovereignTriadBridge()
    kt = bridge.read_kernel_telemetry()
    assert kt["source"] == "live_kernel_proc_sys"
    assert kt["mem_total_mb"] > 0
    assert kt["ramgak_bracket"] in ("GREEN_NOMINAL", "AMBER_PRESSURE")
    assert isinstance(kt["active_nics"], list) and len(kt["active_nics"]) >= 1


def test_alexa_ring_perimeter_node001_correlation() -> None:
    orch = AlexaPlusBedrockOrchestrator(AlexaPlusMCPServer(SovereignTriadBridge()))
    res = orch.process_alexa_utterance(
        "Alexa, ask Axis Outpost to check the Ring North Gate perimeter sensor"
    )
    assert res["http_status"] == 200
    assert res["mcp_tool_invoked"] == "axisos_ring_perimeter_correlate"
    assert res["payload"]["node001_mayor"]["heartbeat_signature"] == "[💃🍪🕺]"


def test_alexa_firetv_10foot_hud_dispatch() -> None:
    orch = AlexaPlusBedrockOrchestrator(AlexaPlusMCPServer(SovereignTriadBridge()))
    res = orch.process_alexa_utterance(
        "Alexa, project the Sovereign Triad HUD onto Fire TV"
    )
    assert res["http_status"] == 200
    assert res["mcp_tool_invoked"] == "axisos_firetv_hud_dispatch"
    assert "Fire TV" in res["payload"]["target_runtime"]


def test_worm_vault_blocks_destructive_voice_command() -> None:
    orch = AlexaPlusBedrockOrchestrator(AlexaPlusMCPServer(SovereignTriadBridge()))
    res = orch.process_alexa_utterance(
        "Alexa, DELETE all backups in /mnt/raid/AxisOS_Curated_Vault"
    )
    assert res["http_status"] == 403
    assert res["status"] == "blocked_by_worm"
    assert res["payload"]["allowed"] is False


def test_worm_vault_allows_append_only_checkpoint() -> None:
    bridge = SovereignTriadBridge()
    res = bridge.enforce_worm_vault("APPEND_CHECKPOINT", "/mnt/raid/vault/audit.log")
    assert res["allowed"] is True
    assert res["http_status"] == 200
    assert res["status"] == "committed_to_worm_vault"
