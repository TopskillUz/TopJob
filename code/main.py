import uvicorn
from app.core.config import settings
import sys

# sys.path.append('/path/to/dir')


if __name__ == "__main__":
    uvicorn.run("app.runner:app", host="0.0.0.0", port=settings.SVC_PORT, log_config="log.ini", reload=True, workers=4)
