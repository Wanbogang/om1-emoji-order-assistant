from dataclasses import dataclass
from typing import Dict, List, Optional
import re


@dataclass
class MenuItem:
    """Represents a menu item with emoji, name, and price."""
    emoji: str
    name: str
    price: float


class EmojiProcessor:
    """Processes emoji strings and converts them to menu items."""
    
    def __init__(self):
        # Menu configuration - emoji to item mapping
        self.menu_items: Dict[str, MenuItem] = {
            "☕": MenuItem("☕", "Coffee", 3.50),
            "🥐": MenuItem("🥐", "Croissant", 2.50),
            "🥪": MenuItem("🥪", "Sandwich", 8.00),
            "🍕": MenuItem("🍕", "Pizza Slice", 5.50),
            "🍔": MenuItem("🍔", "Burger", 7.50),
            "🥗": MenuItem("🥗", "Salad", 6.00),
            "🍰": MenuItem("🍰", "Cake", 4.50),
            "🍪": MenuItem("🍪", "Cookie", 2.00),
            "🧋": MenuItem("🧋", "Bubble Tea", 6.50),
            "🥤": MenuItem("🥤", "Soda", 2.50),
            "🍣": MenuItem("🍣", "Sushi Roll", 8.50),
            "🍜": MenuItem("🍜", "Ramen", 9.00),
        }
        
        # Reverse mapping for easy lookup
        self.emoji_to_item = {item.emoji: item for item in self.menu_items.values()}
    
    def extract_emojis(self, text: str) -> List[str]:
        """Extract all emojis from the input text."""
        # Simple approach: iterate through known emoji menu items
        found_emojis = []
        for emoji in self.emoji_to_item.keys():
            if emoji in text:
                found_emojis.append(emoji)
        return found_emojis
    
    def process_order(self, emoji_string: str) -> List[MenuItem]:
        """
        Process an emoji string and return a list of menu items.
        
        Args:
            emoji_string: String containing emojis for the order
            
        Returns:
            List of MenuItem objects representing the order
        """
        emojis = self.extract_emojis(emoji_string)
        order_items = []
        
        for emoji in emojis:
            if emoji in self.emoji_to_item:
                order_items.append(self.emoji_to_item[emoji])
        
        return order_items
    
    def calculate_total(self, items: List[MenuItem]) -> float:
        """Calculate the total price for a list of items."""
        return sum(item.price for item in items)
    
    def get_menu_summary(self) -> str:
        """Return a formatted summary of available menu items."""
        lines = ["📋 Available Menu Items:"]
        for emoji, item in self.emoji_to_item.items():
            lines.append(f"  {emoji} {item.name} - ${item.price:.2f}")
        return "\n".join(lines)
    
    def validate_order(self, emoji_string: str) -> tuple[bool, str]:
        """
        Validate if the emoji string contains valid menu items.
        
        Returns:
            Tuple of (is_valid, message)
        """
        emojis = self.extract_emojis(emoji_string)
        
        if not emojis:
            return False, "No emojis found in the input. Please include emojis for your order."
        
        valid_items = []
        invalid_emojis = []
        
        for emoji in emojis:
            if emoji in self.emoji_to_item:
                valid_items.append(self.emoji_to_item[emoji])
            else:
                invalid_emojis.append(emoji)
        
        if not valid_items:
            return False, f"No valid menu items found. Invalid emojis: {' '.join(invalid_emojis)}"
        
        if invalid_emojis:
            return (True, 
                   f"Order processed with some invalid emojis ignored: {' '.join(invalid_emojis)}")
        
        return True, "Order is valid!"
