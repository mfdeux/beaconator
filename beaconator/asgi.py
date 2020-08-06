from .backend.server import create_server
from .config import load_config

config = load_config(None)
app = create_server(config=config)
