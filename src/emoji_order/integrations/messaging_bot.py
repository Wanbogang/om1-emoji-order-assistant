import asyncio
from typing import Dict
from rich.console import Console
from ..core.order_manager import OrderManager
from ..core.payment_handler import PaymentHandler

console = Console()

class EmojiBot:
    def __init__(self):
        self.order_manager = OrderManager()
        self.payment_handler = PaymentHandler()
    
    def process_message(self, message: str, user_id: str) -> Dict:
        """Process incoming emoji message"""
        try:
            # Create order from emoji
            order = self.order_manager.create_order(message, user_id)
            
            if 'error' in order:
                return {
                    'response': f"❌ {order['error']}. Try: ☕ 🍕 🥗 🥤",
                    'success': False
                }
            
            # Create payment
            payment = self.payment_handler.create_payment_charge(order)
            
            if not payment['success']:
                return {
                    'response': f"❌ Payment error: {payment['error']}",
                    'success': False
                }
            
            # Format response
            items_str = " + ".join(order['items'])
            if order['modifiers']:
                items_str += f" ({', '.join(order['modifiers']})"
            
            response = f"""☕ Order Received! 🎉

📦 Items: {items_str}
💰 Total: ${order['total_price']:.2f}
🔗 Pay: {payment['hosted_url']}
🆔 Order: {order['order_id']}

✅ Click the link to pay with crypto!
"""
            
            return {
                'response': response,
                'success': True,
                'order_id': order['order_id'],
                'payment_url': payment['hosted_url']
            }
            
        except Exception as e:
            return {
                'response': f"❌ System error: {str(e)}",
                'success': False
            }
    
    def check_order_status(self, order_id: str) -> str:
        """Check order status"""
        order = self.order_manager.get_order(order_id)
        if not order:
            return "❌ Order not found"
        
        status_emoji = {
            'pending_payment': '⏳',
            'paid': '💳',
            'preparing': '👨‍🍳',
            'ready': '✅',
            'completed': '🎉',
            'cancelled': '❌'
        }
        
        emoji = status_emoji.get(order['status'], '❓')
        return f"{emoji} Order {order_id}: {order['status'].replace('_', ' ').title()}"

# Mock bot instance
bot = EmojiBot()
