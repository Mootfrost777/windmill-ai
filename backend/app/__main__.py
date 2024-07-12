import uvicorn

from app.config import config
from app import app, log_config

if __name__ == '__main__':
    uvicorn.run(app, host=config.host, port=config.port, log_config=log_config)
