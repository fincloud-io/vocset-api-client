"""
VOCSET Trade Upload Client

Uploads trade data to the VOCSET API from Excel (.xlsx) or JSON files.
Supports both single-leg trades and multi-leg strategies (spreads, butterflies, etc.).

Usage:
    python uploadTrades.py config.yaml trades.xlsx
    python uploadTrades.py config.yaml trades.json
    python uploadTrades.py -v config.yaml trades.json  # verbose mode
"""
import argparse
import json
import logging

import pandas as pd
import requests
import yaml

# Date columns that need to be formatted as YYYY-MM-DD
DATE_COLUMNS = ['tradeDate', 'maturity', 'clearingDate']


def load_config(config_path):
    """Load YAML configuration file containing API credentials and trade file path."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def get_log_level(config):
    """Get logging level from config, defaulting to INFO if not specified."""
    level = config.get("log_level", "INFO")
    return getattr(logging, level, logging.INFO)


def restructure_multileg_trades(trades):
    """
    Restructure flat trade list into nested multi-leg format.

    Trades with a 'parentTradeId' are grouped as legs under their parent trade.
    Single-leg trades (no parentTradeId) are passed through unchanged.

    Note: parentTradeId is only used for Excel restructuring - it is removed
    from legs before sending to the API, as legs inherit these values from parent.
    """
    parents = {}
    single_legs = []

    # Fields that legs inherit from parent (should not be sent on legs)
    inherited_fields = ['parentTradeId', 'tradeDate', 'client', 'executingBroker',
                        'executingAccount', 'clearingBroker', 'clearingAccount']

    # First pass: identify parent trades and single-leg trades
    for trade in trades:
        parent_id = trade.get('parentTradeId')
        if parent_id:
            # This is a leg trade - will be nested later
            continue
        elif trade.get('strategyName'):
            # This is a parent trade (has strategyName)
            parents[trade['tradeID']] = trade
            trade['legs'] = []
        else:
            # Single-leg trade
            single_legs.append(trade)

    # Second pass: attach legs to their parents, removing inherited fields
    for trade in trades:
        parent_id = trade.get('parentTradeId')
        if parent_id and parent_id in parents:
            # Remove fields that are inherited from parent
            leg = {k: v for k, v in trade.items() if k not in inherited_fields}
            parents[parent_id]['legs'].append(leg)

    # Combine single-leg trades and parent trades (with nested legs)
    return single_legs + list(parents.values())


def read_trades_from_xlsx(file_path):
    """
    Read trades from an Excel file.

    Converts date columns to YYYY-MM-DD format. Supports both single-leg
    and multi-leg trades. Multi-leg trades are identified by:
    - Parent rows: have 'strategyName' field
    - Leg rows: have 'parentTradeId' referencing the parent's tradeID
    """
    try:
        df = pd.read_excel(file_path, dtype=str)
        df = df.dropna(axis=1, how='all')  # Remove empty columns

        # Convert date columns to standard format
        for col in DATE_COLUMNS:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d')

        trades = json.loads(df.to_json(orient="records"))

        # Remove null/NaN values from each trade dict
        trades = [{k: v for k, v in t.items() if v is not None and v != ''} for t in trades]

        # Restructure if there are multi-leg trades
        return restructure_multileg_trades(trades)
    except Exception as e:
        logging.error("Error reading Excel file: %s", e)
        return None


def read_trades_from_json(file_path):
    """
    Read trades from a JSON file.

    Supports both single-leg and multi-leg trades (with nested 'legs' array).
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error("Error reading JSON file: %s", e)
        return None


def read_trades(file_path):
    """
    Read trades from file based on extension.

    Supported formats:
        - .xlsx/.xls: Excel files (single-leg trades)
        - .json: JSON files (single-leg or multi-leg trades)
    """
    if file_path.endswith('.json'):
        return read_trades_from_json(file_path)
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        return read_trades_from_xlsx(file_path)
    else:
        logging.error("Unsupported file format: %s (use .xlsx or .json)", file_path)
        return None


def upload_trades(config, trade_file):
    """
    Upload trades to VOCSET API.

    Args:
        config: Configuration dict with API credentials
        trade_file: Path to trade data file (.xlsx or .json)
    """
    url = config["api"]["url"]

    headers = {
        "X-API-KEY": config["api"]["api_key"],
        "X-API-SECRET": config["api"]["api_secret"],
    }

    trade_data = read_trades(trade_file)
    if trade_data is None:
        logging.error("Failed to read trade file: %s", trade_file)
        return

    logging.info("Uploading %d trade(s) from %s", len(trade_data), trade_file)

    try:
        response = requests.post(url, json=trade_data, headers=headers)
        if response.status_code == 200:
            res = response.json()
            if 'ERROR' in [i['status'] for i in res['result']]:
                logging.error("Response: %s", res['result'])
            else:
                logging.info("Response: %s", response.json())
        else:
            logging.error("Upload failed: %s %s", response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        logging.error("Request failed: %s", e)


def main():
    """Parse arguments and run the trade upload."""
    parser = argparse.ArgumentParser(
        description="Upload trades to VOCSET API",
        epilog="See doc/trade/post.md for trade format documentation"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging")
    parser.add_argument("configfile", help="Path to YAML configuration file (API credentials)")
    parser.add_argument("tradefile", help="Path to trade data file (.xlsx or .json)")
    args = parser.parse_args()

    config = load_config(args.configfile)
    log_level = logging.DEBUG if args.verbose else get_log_level(config)

    logging.basicConfig(
        format="%(asctime)s %(levelname)s - %(message)s",
        level=log_level,
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    upload_trades(config, args.tradefile)


if __name__ == "__main__":
    main()
