# OM1 Emoji Order Assistant — Smart Voice Integration

🎉 **Bug Bounty Submission for OM1 Issue #367**  
Complete voice-activated emoji ordering system with smart assistant integration.

## ✅ Features Implemented

### Core Requirements
- **Voice Command Processing**: Natural language processing for commands like _“order ☕🍕 for John”_  
- **Emoji Processing**: Advanced emoji-to-menu-item conversion  
- **Smart Assistant Integration**: Bridge for Home Assistant with notifications  
- **Order Management**: Full order lifecycle with status tracking  
- **Payment Integration**: Wallet-connected payment flow via MetaMask / browser wallet  
- **REST API**: Built with FastAPI, endpoints for commands, orders & payments  

### Advanced Features
- Multi-language support: Indonesian (“order …”) + English commands  
- AI-powered customer name extraction from voice commands  
- Real-time notifications for new orders via smart assistant  
- Order status progression: Pending → Paid → Preparing → Ready → Completed  
- Comprehensive error handling and input validation  

## 📋 Available Menu

| Emoji | Item             | Price  |
|-------|------------------|--------|
| ☕     | Coffee           | $3.50  |
| ☕☕    | Large Coffee     | $5.00  |
| 🍕     | Pizza            | $12.00 |
| 🥗     | Salad            | $8.00  |
| 🥤     | Smoothie         | $6.00  |
| 🚀     | Express (+$2.00) | Modifier |
| 📍     | Delivery (+$3.00)| Modifier |
| 💪     | Protein Boost (+$2.50) | Modifier |

## 🎤 Voice Commands Examples

#### 🇬🇧 English
order ☕🥐 for Mike
make me ☕☕🍰 please
I want 🍕🥤 delivery

## 🔧 API Endpoints

**Voice Commands**  
`POST /api/voice-command`  
Content-Type: `application/json`
```json
{
  "command": "order ☕🍕 for John",
  "customer_name": "John Doe"
}
```

**Emoji Orders**  
`POST /api/emoji-order`  
Content-Type: `application/json`
```json
{
  "emoji_string": "☕🥗",
  "user_id": "Jane"
}
```

**Payment Processing**  
`POST /api/payment/signed`  
Content-Type: `application/json`
```json
{
  "order_id": "b0521fe8",
  "txHash": "0x1234abcd…"
}
```

**Order Status**  
`GET /api/orders`

---

## 🧪 Quick Start
```bash
git clone https://github.com/Wanbogang/om1-emoji-order-assistant.git
cd om1-emoji-order-assistant
pip install -r requirements.txt
cp .env.example .env   # edit .env with API keys if needed
./demo/e2e_wallet_demo.sh
```

Open your browser at `http://localhost:8080/` (requires MetaMask or browser wallet on testnet/local).  
Connect your wallet → Sign & Send Tx → then check orders:
```bash
curl http://localhost:8080/api/orders
```

---

## 🏁 Claim Bounty — OM1 Issue #367
**Home Assistant used:** Yes — `home_assistant_config.yaml` included  
**Repo:** https://github.com/Wanbogang/om1-emoji-order-assistant  
**PR:** https://github.com/Wanbogang/om1-emoji-order-assistant/pull/2  
**Demo Video:** https://youtu.be/eB4q9EvyHDA  

### Notes:
- Run: `./demo/e2e_wallet_demo.sh`
- Use browser wallet (MetaMask) on testnet/local
- Flow: voice → create order → wallet signature → server records `txHash`

**Artifacts in this PR:**
- `web-client/` — demo wallet UI  
- `server.py` — FastAPI demo + `/api/payment/signed` + `/api/orders`  
- `demo/e2e_wallet_demo.sh`  
- `home_assistant_config.yaml`  
- `README.md` — Claim Bounty section updated

---

## 📝 License
MIT License — free for commercial and non-commercial use.

## 🤝 Contributing
Fork the repository → Create feature branch → Make changes → Test thoroughly → Submit pull request

