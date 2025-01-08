import argparse
import json
import logging

import pandas as pd
import requests
import yaml


def load_config(configfile):
    with open(configfile, 'r') as config_file:
        return yaml.safe_load(config_file)


def get_log_level(config):
    level = config.get("log_level")
    return getattr(logging, level, logging.INFO)


def read_trades_from_xlsx(file_path):
    try:
        df = pd.read_excel(file_path, dtype=str)
        df = df.dropna(axis=1, how='any')
        date_columns = ['tradeDate', 'maturity', 'clearingDate']

        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d')

        convert_trade_file = df.to_json(orient="records")
        trades = json.loads(convert_trade_file)
        return trades
    except Exception as e:
        logging.error("Error reading file: %s", e)
        return None


def upload_trades(config):
    upload_url = config["api"]["url"]
    api_key = config["api"]["api_key"]
    api_secret = config["api"]["api_secret"]
    trade_file = config["api"]["trade_file_path"]

    headers = {
        "X-API-KEY": api_key,
        "X-API-SECRET": api_secret,
    }

    trade_data = read_trades_from_xlsx(trade_file)
    if trade_data is None:
        logging.error("No file found.")
        return

    try:
        response = requests.post(upload_url, json=trade_data, headers=headers)
        if response.status_code == 200:
            logging.info("Trades Uploaded")
            logging.debug("Trade data: %s", response.json())
        else:
            logging.error("Error: %s %s ", response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        logging.error("Error: %s", e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload VOCSET Trades")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("configfile", help="configuration file")
    args = parser.parse_args()

    # Load configuration
    config = load_config(args.configfile)
    log_level = logging.DEBUG if args.verbose else get_log_level(config)
    logging.basicConfig(
        format="%(asctime)-15s %(levelname)s - %(message)s",
        level=log_level,
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    upload_trades(config)
