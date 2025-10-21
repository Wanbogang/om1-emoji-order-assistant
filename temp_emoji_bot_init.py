    def __init__(self, demo_mode=True, ha_url=None, ha_token=None):
        self.demo_mode = demo_mode
        self.processor = EmojiProcessor()
        self.order_manager = OrderManager()
        self.payment_handler = PaymentHandler(demo_mode=demo_mode)
        
        # Smart Assistant integration
        self.smart_assistant = SmartAssistantBridge(ha_url, ha_token)
        self.voice_processor = VoiceCommandProcessor()
        
        # Send notification when bot starts
        self.smart_assistant.send_notification(
            "OM1 Bot Started", 
            "Emoji Order Assistant is ready to receive orders!"
        )
