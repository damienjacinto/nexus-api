#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nexus_client import NexusClient
from nexus_client.config import Config
from data import DataNexus

def main():
    config = Config()
    data = DataNexus(db_path=config.database_path)
    data.connect()

    with NexusClient(**config.get_client_kwargs()) as client:
        try:
            ## list all repository
            repos = client.repositories.list()
            print(f"Found {len(repos)} repositories")
            for repo in repos:
                print(f" - {repo['name']} ({repo['format']})")
                # save to sqlite base
                repo_id = data.save_repository(repo['name'], repo['format'])
                sys.stdout.write(f"   ✓ Saved to database with ID {repo_id}\n")

                components = client.components.list(repo['name'])
                print(f"   Found {len(components)} components")
                for component in components:
                    print(f"   - Component: {component['name']} (ID: {component['id']})")
                    component_id = data.save_component(component['name'], component.get('format'), component.get('group'), component.get('version'), repo_id)
                    sys.stdout.write(f"     ✓ Saved component to database with ID {component_id}\n")

                # assets = client.assets.list(repo['name'])
                # for asset in assets:
                #     print(f"   - Asset: {asset['name']} (ID: {asset['id']})")
                #     asset_id = data.save_asset(asset['name'], asset['id'], asset.get('fileSize'), asset.get('lastModified'), asset.get('lastDownloaded'), asset.get('uploader'), asset.get('blobCreated'), asset.get('blobStoreName'), asset.get('format'), asset.get('path'), asset.get('downloadUrl'), asset.get('contentType'), repo_id)
                #     sys.stdout.write(f"     ✓ Saved asset to database with ID {asset_id}\n")

        except Exception as e:
            print(f"   ✗ Error: {e}")
            return
        finally:
            data.close()


if __name__ == "__main__":
    main()
