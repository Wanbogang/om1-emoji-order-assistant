from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging
import os
from datetime import datetime

from src.emoji_bot import EmojiBot
from src.order_manager import OrderStatus


# Pydantic models for API requests/responses
class OrderRequest(BaseModel):
    emoji_string: str
    customer_name: Optional[str] = None


class OrderResponse(BaseModel):
    success: bool
    order_id: Optional[str] = None
    message: str
    payment_url: Optional[str] = None
    total_amount: Optional[float] = None
    items: Optional[List[Dict[str, Any]]] = None


# Initialize FastAPI app
app = FastAPI(
    title="Emoji Order Assistant API",
    description="API for processing emoji-based food orders with payment integration",
    version="1.0.0"
)

# Initialize the bot
bot = EmojiBot(demo_mode=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with basic HTML interface."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Emoji Order Assistant</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .emoji-input { font-size: 24px; padding: 10px; width: 300px; }
            .btn { background-color: #4CAF50; color: white; padding: 10px 20px; border: none; cursor: pointer; }
            .menu { background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0; }
            .result { background-color: #e8f5e8; padding: 15px; border-radius: 5px; margin: 10px 0; }
            .error { background-color: #ffe8e8; padding: 15px; border-radius: 5px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <h1>🤖 Emoji Order Assistant</h1>
        <p>Order food by sending emojis! 🍕☕🥐</p>
        
        <div class="menu">
            <h3>Available Items:</h3>
            <p>☕ Coffee ($3.50) | 🥐 Croissant ($2.50) | 🥪 Sandwich ($8.00) | 🍕 Pizza ($5.50)</p>
            <p>🍔 Burger ($7.50) | 🥗 Salad ($6.00) | 🍰 Cake ($4.50) | 🍪 Cookie ($2.00)</p>
            <p>🧋 Bubble Tea ($6.50) | 🥤 Soda ($2.50) | 🍣 Sushi ($8.50) | 🍜 Ramen ($9.00)</p>
        </div>
        
        <div>
            <input type="text" id="emojiInput" class="emoji-input" placeholder="Enter emojis..." />
            <input type="text" id="nameInput" placeholder="Your name (optional)" />
            <button class="btn" onclick="placeOrder()">Place Order</button>
        </div>
        
        <div id="result"></div>
        
        <script>
            async function placeOrder() {
                const emojiString = document.getElementById('emojiInput').value;
                const customerName = document.getElementById('nameInput').value;
                const resultDiv = document.getElementById('result');
                
                if (!emojiString) {
                    resultDiv.innerHTML = '<div class="error">Please enter emojis for your order!</div>';
                    return;
                }
                
                try {
                    const response = await fetch('/api/order', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            emoji_string: emojiString,
                            customer_name: customerName || null
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        resultDiv.innerHTML = `
                            <div class="result">
                                <h3>✅ Order Created!</h3>
                                <p><strong>Order ID:</strong> ${data.order_id}</p>
                                <p><strong>Total:</strong> $${data.total_amount.toFixed(2)}</p>
                                <p><strong>Items:</strong> ${data.items.map(item => item.emoji + ' ' + item.name).join(', ')}</p>
                                ${data.payment_url ? `<p><a href="${data.payment_url}" target="_blank">💳 Complete Payment</a></p>` : ''}
                            </div>
                        `;
                    } else {
                        resultDiv.innerHTML = `<div class="error">❌ Error: ${data.message}</div>`;
                    }
                } catch (error) {
                    resultDiv.innerHTML = `<div class="error">❌ Network error: ${error.message}</div>`;
                }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/api/menu")
async def get_menu():
    """Get available menu items."""
    menu_items = []
    for emoji, item in bot.emoji_processor.emoji_to_item.items():
        menu_items.append({
            "emoji": emoji,
            "name": item.name,
            "price": item.price
        })
    
    return {"menu_items": menu_items}


@app.post("/api/order", response_model=OrderResponse)
async def create_order(request: OrderRequest):
    """Create a new order from emoji string."""
    try:
        result = bot.process_emoji_order(request.emoji_string, request.customer_name)
        
        if result["success"]:
            order = result["order"]
            
            # Format items for response
            items_data = []
            item_counts = {}
            for item in order.items:
                if item.emoji in item_counts:
                    item_counts[item.emoji] = (item_counts[item.emoji][0] + 1, item)
                else:
                    item_counts[item.emoji] = (1, item)
            
            for emoji, (count, item) in item_counts.items():
                items_data.append({
                    "emoji": emoji,
                    "name": item.name,
                    "quantity": count,
                    "unit_price": item.price,
                    "total_price": item.price * count
                })
            
            return OrderResponse(
                success=True,
                order_id=order.id,
                message=result.get("message", "Order created successfully"),
                payment_url=result.get("payment_url"),
                total_amount=order.total_amount,
                items=items_data
            )
        else:
            return OrderResponse(
                success=False,
                message=result.get("error", "Failed to create order")
            )
            
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/order/{order_id}")
async def get_order(order_id: str):
    """Get order details by ID."""
    try:
        order = bot.get_order_by_id(order_id)
        
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        # Format items for response
        items_data = []
        item_counts = {}
        for item in order.items:
            if item.emoji in item_counts:
                item_counts[item.emoji] = (item_counts[item.emoji][0] + 1, item)
            else:
                item_counts[item.emoji] = (1, item)
        
        for emoji, (count, item) in item_counts.items():
            items_data.append({
                "emoji": emoji,
                "name": item.name,
                "quantity": count,
                "unit_price": item.price,
                "total_price": item.price * count
            })
        
        return {
            "order_id": order.id,
            "customer_name": order.customer_name,
            "status": order.status.value,
            "total_amount": order.total_amount,
            "items": items_data,
            "created_at": order.created_at.isoformat(),
            "updated_at": order.updated_at.isoformat(),
            "payment_url": order.payment_url
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting order: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/orders")
async def list_orders(status: Optional[str] = None, limit: int = 20):
    """List orders with optional status filter."""
    try:
        # Parse status if provided
        status_filter = None
        if status:
            try:
                status_filter = OrderStatus(status.lower())
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
        
        orders = bot.order_manager.list_orders(status_filter)
        orders = orders[:limit]  # Apply limit
        
        orders_data = []
        for order in orders:
            # Count items
            item_counts = {}
            for item in order.items:
                if item.emoji in item_counts:
                    item_counts[item.emoji] = (item_counts[item.emoji][0] + 1, item)
                else:
                    item_counts[item.emoji] = (1, item)
            
            items_summary = ", ".join([f"{emoji}x{count}" for emoji, (count, _) in item_counts.items()])
            
            orders_data.append({
                "order_id": order.id,
                "customer_name": order.customer_name,
                "status": order.status.value,
                "total_amount": order.total_amount,
                "items_summary": items_summary,
                "item_count": len(order.items),
                "created_at": order.created_at.isoformat(),
                "updated_at": order.updated_at.isoformat()
            })
        
        return {"orders": orders_data, "total": len(orders_data)}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing orders: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_statistics():
    """Get order statistics."""
    try:
        stats = bot.order_manager.get_statistics()
        return stats
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    
    # Run the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
