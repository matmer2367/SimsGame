import yaml

def load(path: str):
    with open(path, "r") as f:
        return yaml.safe_load(f)