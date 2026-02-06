#!/usr/bin/env python3

import sys
import os
from xmlrpc import client

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nexus_client import NexusClient
from nexus_client.config import Config


def main():
    config = Config()
    with NexusClient(**config.get_client_kwargs()) as client:
      try:
          status = client.get_status()
          print(f"   ✓ Server is online")
          print(f"   Version: {status.get('Server', 'unknown')}")
      except Exception as e:
          print(f"   ✗ Error: {e}")
          return


if __name__ == "__main__":
    main()
