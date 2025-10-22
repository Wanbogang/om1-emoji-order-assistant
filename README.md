# Emoji Order Assistant

A revolutionary food ordering system that allows customers to place orders using emojis! 🍕☕🥐

## Features

- 🎯 **Emoji-based Ordering**: Simply send emojis to order food
- 💳 **Payment Integration**: Coinbase Commerce integration for crypto payments
- 📊 **Order Management**: Complete order lifecycle tracking
- 🤖 **Interactive Demo**: Rich terminal interface for testing
- 🌐 **REST API**: Full API for integration with other systems
- 📱 **Web Interface**: Simple HTML interface for web users

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt

### 2. Run the Interactive Demo

python quick_demo.py
This will start an interactive terminal session where you can:

Type emojis to place orders (e.g., ☕🥐 for coffee and croissant)
View the menu with menu
See statistics with stats
Get help with help

### 3. Start the API Server

python main.py
The API will be available at http://localhost:8000

Web Interface: http://localhost:8000
API Documentation: http://localhost:8000/docs
Available Menu Items
| Emoji | Item | Price |
|-------|------|-------|
| ☕ | Coffee | $3.50 |
| 🥐 | Croissant | $2.50 |
| 🥪 | Sandwich | $8.00 |
| 🍕 | Pizza Slice | $5.50 |
| 🍔 | Burger | $7.50 |
| 🥗 | Salad | $6.00 |
| 🍰 | Cake | $4.50 |
| 🍪 | Cookie | $2.00 |
| 🧋 | Bubble Tea | $6.50 |
| 🥤 | Soda | $2.50 |
| 🍣 | Sushi Roll | $8.50 |
| 🍜 | Ramen | $9.00 |


## API Usage Examples
Create an Order
curl -X POST "http://localhost:8000/api/order" \
     -H "Content-Type: application/json" \
     -d '{
       "emoji_string": "☕🥐🍕",
       "customer_name": "John Doe"
     }'
Get Order Details
curl "http://localhost:8000/api/order/{order_id}"
List All Orders
curl "http://localhost:8000/api/orders"
Get Menu
curl "http://localhost:8000/api/menu"
Get Statistics
curl "http://localhost:8000/api/stats"

## Configuration
Create a .env file for production use:
COINBASE_COMMERCE_API_KEY=your_api_key_here
COINBASE_COMMERCE_WEBHOOK_SECRET=your_webhook_secret_here

## Architecture
The system consists of several key components:

EmojiProcessor: Parses emoji strings and converts them to menu items
OrderManager: Manages order lifecycle and storage
PaymentHandler: Handles payment processing with Coinbase Commerce
EmojiBot: Main integration class that coordinates all components
FastAPI Server: REST API for web integration
Demo Mode
The system runs in demo mode by default, which means:

No actual payments are processed
Mock payment URLs are generated
All functionality works for testing purposes
To enable real payments, set up Coinbase Commerce API keys in your environment.

Contributing
Fork the repository
Create a feature branch
Make your changes
Add tests if applicable
Submit a pull request
License
This project is open source and available under the MIT License.

## Wallet-connected vs Payment-Processor flows

This project supports two payment approaches:
- **Payment-processor (Coinbase Commerce)** — users pay via third-party gateway; server receives webhook confirmation.
- **Wallet-connected (WalletConnect / injected wallet)** — users *connect* and *sign* on-chain transactions; server receives `tx_hash` and monitors receipt via RPC (ETH_RPC).

Important Environment Variables:
- `ETH_RPC` — RPC endpoint (e.g., Ganache `http://127.0.0.1:8545`, Infura/Alchemy).
- `COINBASE_WEBHOOK_SECRET` — HMAC secret for Coinbase Commerce webhook verification (if used).

📞 Contact: @Wanbogang for support and customization

## 🏁 Claim bounty — OM1 Issue #367 (submission checklist)

**Home Assistant used:** Yes — `home_assistant_config.yaml` included.

**Post Link:** https://x.com/berkah_nikki/status/1980786927914873005

**Demo Video:** https://youtu.be/eB4q9EvyHDA

**Notes / How to reproduce (quick):**
1. Copy `.env.example` → `.env` and set keys (if needed).
2. Start demo server:
   ```bash
   ./demo/e2e_wallet_demo.sh
Open browser: http://localhost:8080/ (MetaMask required; use testnet/local chain).

Connect wallet → Sign & Send Tx → server will record order_id → verify:
curl http://localhost:8080/api/orders
Artifacts included in this PR:

web-client/ — simple wallet demo (connect & sign tx).

server.py — FastAPI demo + /api/payment/signed and /api/orders.

demo/e2e_wallet_demo.sh — start script + instructions.

home_assistant_config.yaml — example HA automation.

README.md — this checklist & reproduction steps.
