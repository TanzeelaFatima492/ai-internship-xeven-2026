import json
import os

CONFIG_FILE = "config.json"

default_config = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "mydb"
    },
    "api": {
        "key": "default_key",
        "timeout": 30
    }
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
    else:
        config = default_config

    return config


def validate_config(config):
    required_keys = ["database", "api"]

    for key in required_keys:
        if key not in config:
            print(f"Missing key: {key}, using default")
            config[key] = default_config[key]

    return config

# Save config
def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)


# Update config programmatically
def update_config(config, section, key, value):
    if section not in config:
        config[section] = {}

    config[section][key] = value
    save_config(config)
    print("Config updated!")

config = load_config()
config = validate_config(config)

print("\nCurrent Config:")
print(config)

# Example usage with .get() (safe access)
db_host = config.get("database", {}).get("host", "localhost")
api_key = config.get("api", {}).get("key", "NO_KEY")

print("\nDatabase Host:", db_host)
print("API Key:", api_key)

# Example update
update_config(config, "features", "dark_mode", True)