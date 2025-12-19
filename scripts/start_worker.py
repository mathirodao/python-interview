#!/usr/bin/env python3
"""Script to start the RQ worker."""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.worker import start_worker

if __name__ == "__main__":
    print("Starting RQ worker...")
    print("Press Ctrl+C to stop")
    start_worker()
