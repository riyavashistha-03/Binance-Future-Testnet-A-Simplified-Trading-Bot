import argparse
from bot.client import get_binance_client
from bot.orders import place_order
from bot.validators import validate_order_inputs
from bot.logging_config import logger

def main():
    parser = argparse.ArgumentParser(description="Simplified Binance Futures Trading Bot")
    
    parser.add_argument('--symbol', type=str, required=True, help="Trading pair symbol (e.g., BTCUSDT)")
    parser.add_argument('--side', type=str, required=True, choices=['BUY', 'SELL'], help="Order side (BUY or SELL)")
    parser.add_argument('--type', type=str, required=True, choices=['MARKET', 'LIMIT'], help="Order type (MARKET or LIMIT)")
    parser.add_argument('--quantity', type=float, required=True, help="Quantity to trade")
    parser.add_argument('--price', type=float, required=False, help="Price (Required for LIMIT orders)")

    args = parser.parse_args()

    try:
        # 1. Validate inputs
        validate_order_inputs(args.symbol, args.side, args.type, args.quantity, args.price)
        
        # 2. Get Client
        client = get_binance_client()
        
        # 3. Place Order
        place_order(
            client=client,
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price
        )

    except ValueError as ve:
        logger.error(f"Validation Error: {ve}")
    except Exception as e:
        logger.error(f"Application Error: {e}")

if __name__ == "__main__":
    main()