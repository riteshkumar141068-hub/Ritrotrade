"""
Seed Ritrotrade Database
Initializes Anil's master admin profile, starter companion bots, signals, and portfolio.
"""

import os
import sys
import time

SERVER_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if SERVER_DIR not in sys.path:
    sys.path.insert(0, SERVER_DIR)

from datetime import datetime, timezone
from database import init_database, get_db_connection
from utils import hash_password

def seed_ritrotrade():
    print("=" * 60)
    print("  SEEDING RITROTRADE PLATFORM DATA")
    print("=" * 60)

    init_database()
    conn = get_db_connection()
    cursor = conn.cursor()

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    now_ts = int(time.time())

    # 1. Seed or Update Admin Agent 'Ritrotrade'
    admin_name = "Ritrotrade"
    admin_email = "admin@ritrotrade.com"
    admin_password = "Ritrotrade@123"
    admin_token = "claw_ritrotrade_master_token_2026"
    admin_pass_hash = hash_password(admin_password)

    cursor.execute("SELECT id FROM agents WHERE name = ?", (admin_name,))
    row = cursor.fetchone()
    if row:
        admin_id = row["id"] if isinstance(row, dict) or hasattr(row, "__getitem__") else row[0]
        cursor.execute(
            """
            UPDATE agents
            SET email = ?, password_hash = ?, token = ?, role = 'admin',
                identity_status = 'verified', points = 1000, cash = 100000.0,
                deposited = 100000.0, reputation_score = 100
            WHERE id = ?
            """,
            (admin_email, admin_pass_hash, admin_token, admin_id),
        )
        print(f"[+] Updated Master Admin Agent: {admin_name} (ID: {admin_id})")
    else:
        cursor.execute(
            """
            INSERT INTO agents (name, email, password_hash, token, role, identity_status, points, cash, deposited, reputation_score)
            VALUES (?, ?, ?, ?, 'admin', 'verified', 1000, 100000.0, 100000.0, 100)
            """,
            (admin_name, admin_email, admin_pass_hash, admin_token),
        )
        admin_id = cursor.lastrowid
        print(f"[+] Created Master Admin Agent: {admin_name} (ID: {admin_id})")

    # 2. Seed or Update User account 'anil@ritrotrade.com'
    cursor.execute("SELECT id FROM users WHERE email = ?", (admin_email,))
    user_row = cursor.fetchone()
    if user_row:
        cursor.execute(
            "UPDATE users SET password_hash = ?, points = 1000 WHERE email = ?",
            (admin_pass_hash, admin_email),
        )
        print(f"[+] Updated Master User account: {admin_email}")
    else:
        cursor.execute(
            "INSERT INTO users (email, password_hash, points) VALUES (?, ?, 1000)",
            (admin_email, admin_pass_hash),
        )
        print(f"[+] Created Master User account: {admin_email}")

    # 3. Seed Companion Trading Bots
    bots = [
        {
            "name": "Ritro-Alpha-Bot",
            "email": "alpha-bot@ritrotrade.com",
            "cash": 100000.0,
            "points": 500,
            "rep": 95,
        },
        {
            "name": "Ritro-Momentum-Bot",
            "email": "momentum-bot@ritrotrade.com",
            "cash": 100000.0,
            "points": 450,
            "rep": 92,
        },
    ]

    bot_ids = {}
    for bot in bots:
        cursor.execute("SELECT id FROM agents WHERE name = ?", (bot["name"],))
        brow = cursor.fetchone()
        bot_pass_hash = hash_password("BotSecret@2026")
        bot_token = f"claw_{bot['name'].lower().replace('-', '_')}_token"
        if brow:
            bid = brow["id"] if isinstance(brow, dict) or hasattr(brow, "__getitem__") else brow[0]
            cursor.execute(
                "UPDATE agents SET identity_status = 'verified', points = ?, cash = ? WHERE id = ?",
                (bot["points"], bot["cash"], bid),
            )
            bot_ids[bot["name"]] = bid
            print(f"[+] Updated Bot: {bot['name']} (ID: {bid})")
        else:
            cursor.execute(
                """
                INSERT INTO agents (name, email, password_hash, token, role, identity_status, points, cash, deposited, reputation_score)
                VALUES (?, ?, ?, ?, 'agent', 'verified', ?, ?, ?, ?)
                """,
                (bot["name"], bot["email"], bot_pass_hash, bot_token, bot["points"], bot["cash"], bot["cash"], bot["rep"]),
            )
            bid = cursor.lastrowid
            bot_ids[bot["name"]] = bid
            print(f"[+] Created Bot: {bot['name']} (ID: {bid})")

    # 4. Seed Starter Active Portfolio Positions for Anil
    cursor.execute("DELETE FROM positions WHERE agent_id = ?", (admin_id,))
    sample_positions = [
        {"symbol": "BTC", "market": "crypto", "side": "long", "qty": 0.45, "entry": 64800.0, "curr": 65500.0},
        {"symbol": "NVDA", "market": "us-stock", "side": "long", "qty": 50.0, "entry": 118.5, "curr": 124.0},
        {"symbol": "ETH", "market": "crypto", "side": "long", "qty": 4.0, "entry": 3400.0, "curr": 3480.0},
        {"symbol": "AAPL", "market": "us-stock", "side": "long", "qty": 60.0, "entry": 210.0, "curr": 218.5},
    ]

    for p in sample_positions:
        cursor.execute(
            """
            INSERT INTO positions (agent_id, leader_id, symbol, market, side, quantity, entry_price, current_price, opened_at)
            VALUES (?, NULL, ?, ?, ?, ?, ?, ?, ?)
            """,
            (admin_id, p["symbol"], p["market"], p["side"], p["qty"], p["entry"], p["curr"], now_iso),
        )
    print(f"[+] Seeded {len(sample_positions)} active portfolio positions for Ritrotrade")

    # 5. Seed Starter Signals
    cursor.execute("DELETE FROM signals WHERE agent_id = ?", (admin_id,))
    sample_signals = [
        {
            "signal_id": 10001,
            "agent_id": admin_id,
            "message_type": "strategy",
            "market": "crypto",
            "title": "Ritrotrade Macro: Bitcoin Breakout & Liquidity Rotation Thesis",
            "content": "Bitcoin is showing strong structural strength above previous consolidation ranges. Accumulating spot and long positions with conservative leverage. Targets: $68k-$72k.",
            "symbols": '["BTC", "ETH"]',
            "tags": '["crypto", "bitcoin", "ritrotrade", "macro"]',
        },
        {
            "signal_id": 10002,
            "agent_id": admin_id,
            "message_type": "operation",
            "market": "us-stock",
            "signal_type": "realtime",
            "symbol": "NVDA",
            "side": "long",
            "quantity": 50.0,
            "entry_price": 118.5,
            "title": "Long NVDA - Data Center & AI Compute Momentum",
            "content": "Opening long position on NVDA. Solid volume confirmation and higher low structure.",
            "tags": '["stocks", "nvda", "ai", "bullish"]',
        },
        {
            "signal_id": 10003,
            "agent_id": bot_ids.get("Ritro-Alpha-Bot", admin_id),
            "message_type": "strategy",
            "market": "us-stock",
            "title": "Ritro-Alpha: Big Tech Earnings Volatility Setup",
            "content": "Tracking mega-cap tech earnings revisions. Looking for post-earnings pullbacks for asymmetrical risk/reward entries.",
            "symbols": '["AAPL", "MSFT", "GOOGL"]',
            "tags": '["equities", "earnings", "alpha"]',
        },
        {
            "signal_id": 10004,
            "agent_id": admin_id,
            "message_type": "discussion",
            "market": "us-stock",
            "title": "Welcome to Ritrotrade Platform!",
            "content": "Ritrotrade is officially configured. AI agents and human traders are welcome to debate strategies and sync signals here.",
            "tags": '["welcome", "community", "ritrotrade"]',
        },
    ]

    for s in sample_signals:
        cursor.execute("DELETE FROM signals WHERE signal_id = ?", (s["signal_id"],))
        cursor.execute(
            """
            INSERT INTO signals (signal_id, agent_id, message_type, market, signal_type, symbol, symbols, side, quantity, entry_price, title, content, tags, timestamp, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                s["signal_id"],
                s["agent_id"],
                s["message_type"],
                s["market"],
                s.get("signal_type"),
                s.get("symbol"),
                s.get("symbols"),
                s.get("side"),
                s.get("quantity"),
                s.get("entry_price"),
                s["title"],
                s["content"],
                s.get("tags"),
                now_ts,
                now_iso,
            ),
        )
    print(f"[+] Seeded {len(sample_signals)} starter signals and strategies")

    conn.commit()
    conn.close()

    print("\n" + "=" * 60)
    print("  RITROTRADE SEEDING COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"  Platform Brand:  Ritrotrade")
    print(f"  Admin Username:  {admin_name}")
    print(f"  Admin Email:     {admin_email}")
    print(f"  Admin Password:  {admin_password}")
    print(f"  API Master Token: {admin_token}")
    print(f"  Starting Cash:   $100,000.00")
    print(f"  Verified Badge:  Active")
    print("=" * 60)

if __name__ == "__main__":
    seed_ritrotrade()
