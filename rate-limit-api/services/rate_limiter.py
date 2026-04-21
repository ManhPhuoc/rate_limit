from config_store import get_config
from strategies.sliding_window import sliding_window_allow
from strategies.token_bucket import token_bucket_allow

def check_rate_limit(api_key):
    config = get_config(api_key)

    strategy = config["strategy"]

    if strategy == "sliding_window":
        return sliding_window_allow(
            api_key,
            config["limit"],
            config["window"]
        )

    elif strategy == "token_bucket":
        return token_bucket_allow(
            api_key,
            capacity=config["limit"],
            refill_rate=config["limit"] / config["window"]
        )

    else:
        return False, 0