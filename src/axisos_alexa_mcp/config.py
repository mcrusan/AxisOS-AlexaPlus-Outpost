# ==============================================================================
# File: src/axisos_alexa_mcp/config.py
# Project: AxisOS Alexa+ Outpost (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Runtime configuration for AxisOS Alexa+ Streamable HTTP MCP
#              Server, AWS Bedrock AgentCore, and Sovereign Triad endpoints.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Initial creation.
# ==============================================================================

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class OutpostConfig:
    """Immutable configuration for AxisOS Alexa+ Outpost."""

    mcp_host: str = os.getenv("ALEXA_MCP_HOST", "0.0.0.0")
    mcp_port: int = int(os.getenv("ALEXA_MCP_PORT", "8092"))
    alexa_skill_id: str = os.getenv(
        "ALEXA_SKILL_ID", "amzn1.ask.skill.axisos-sovereign-outpost"
    )
    aws_region: str = os.getenv("AWS_REGION", "us-west-2")
    bedrock_model_id: str = os.getenv(
        "BEDROCK_MODEL_ID", "us.amazon.nova-pro-v1:0"
    )
    bedrock_agent_id: str = os.getenv(
        "BEDROCK_AGENT_ID", "AXISOS-OUTPOST-AGENT"
    )
    zero_core_url: str = os.getenv("AXISOS_ZERO_CORE_URL", "http://127.0.0.1:8081")
    agent_lite_url: str = os.getenv("AXISOS_AGENT_LITE_URL", "http://127.0.0.1:8080")
    axis_agent_url: str = os.getenv("AXISOS_AXIS_AGENT_URL", "http://127.0.0.1:8082")
    zero_comms_url: str = os.getenv("AXISOS_ZERO_COMMS_URL", "http://127.0.0.1:8085")
    cloud_outpost_url: str = os.getenv(
        "AXISOS_CLOUD_OUTPOST_URL",
        "https://axisos-sovereign-triad-4zye7tn3qq-uw.a.run.app",
    )
    node001_mesh_ip: str = os.getenv("NODE001_MESH_IP", "10.10.0.35")
    node001_lan_ip: str = os.getenv("NODE001_LAN_IP", "192.168.1.35")
    node001_udp_port: int = int(os.getenv("NODE001_UDP_PORT", "50000"))


CONFIG = OutpostConfig()
