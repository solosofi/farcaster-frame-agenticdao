#!/usr/bin/env python3
"""Farcaster Frame action handler - processes tx actions and unlocks."""
import json
import os
import urllib.request

PORT = int(os.environ.get("PORT", 8080))
WALLET = "0x2d44fc27a616606b42448309F4d8e3F423d93267"

def handle_frame_action(payload: dict) -> dict:
    """Process Farcaster frame button action."""
    action = payload.get("action", "")
    if action == "tx":
        return {
            "type": "transaction",
            "chain": "eip155:8453",  # Base mainnet
            "to": WALLET,
            "value": "10000000000000000",  # 0.01 ETH in wei
            "status": "ready",
        }
    return {"type": "postback", "message": "Unknown action"}
