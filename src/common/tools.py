
import logging
import os
from pathlib import Path
import time

import yaml

# create module logger
logger = logging.getLogger(__name__)

def get_project_root():
    """Returns project root folder.
    .../alphatrader/
    """
    return Path(__file__).parent.parent.parent


if __name__ == "__main__":
    print(get_project_root())