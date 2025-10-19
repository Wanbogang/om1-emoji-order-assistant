from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class EmojiOrder:
    emoji: str
    item: str
    price: float
    category: str
    modifiers: list = None

class EmojiProcessor:
    def __init__(self):
        self.emoji_mappings = {
            # Basic items
            '☕': EmojiOrder('☕', 'Coffee', 3.50, 'beverage'),
            '☕☕': EmojiOrder('☕☕', 'Large Coffee', 5.00, 'beverage'),
            '🍕': EmojiOrder('🍕', 'Pizza', 12.00, 'food'),
            '🥗': EmojiOrder('🥗', 'Salad', 8.00, 'food'),
            '🥤': EmojiOrder('🥤', 'Smoothie', 6.00, 'beverage'),
            
            # Modifiers
            '🚀': EmojiOrder('🚀', 'Express', 2.00, 'modifier'),
            '📍': EmojiOrder('📍', 'Delivery', 3.00, 'modifier'),
            '💪': EmojiOrder('💪', 'Protein Boost', 2.50, 'modifier'),
            
            # Actions
            '✅': EmojiOrder('✅', 'Confirm', 0.00, 'action'),
            '❌': EmojiOrder('❌', 'Cancel', 0.00, 'action'),
        }
    
    def process_emoji_string(self, emoji_string: str) -> Dict:
        """Process emoji string and return order details"""
        if not emoji_string:
            return {'error': 'No emoji provided'}
        
        # Parse emoji combinations
        emojis = list(emoji_string.strip())
        total_price = 0.0
        items = []
        modifiers = []
        
        for emoji in emojis:
            if emoji in self.emoji_mappings:
                order = self.emoji_mappings[emoji]
                if order.category == 'modifier':
                    modifiers.append(order.item)
                    total_price += order.price
                elif order.category == 'action':
                    continue  # Handle separately
                else:
                    items.append(order.item)
                    total_price += order.price
            else:
                return {'error': f'Unknown emoji: {emoji}'}
        
        return {
            'items': items,
            'modifiers': modifiers,
            'total_price': total_price,
            'emoji_string': emoji_string
        }
