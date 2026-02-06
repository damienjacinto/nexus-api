# Nexus Repository Manager Python Client

A comprehensive Python client library for interacting with Sonatype Nexus Repository Manager REST API (v3.68.1+).

## Features

- 🔐 **Authentication** - Username/password authentication support
- 📦 **Repository Management** - Create, update, delete, and list repositories
- 🔍 **Search** - Search for components and assets with various filters
- 📤 **Upload/Download** - Upload and download components and assets
- 👥 **Security Management** - Manage users, roles, and privileges
- 🗄️ **Blob Stores** - Manage blob store configurations
- ⚙️ **Tasks** - View and manage scheduled tasks
- 🔄 **Multiple Formats** - Support for Maven, NPM, Docker, Raw, and more

## Installation

### Using pip (from source)

```bash
cd nexus-python-app
pip install -e .
```

### Using requirements.txt

```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Configure Your Environment

Copy the example environment file and update with your Nexus server details:

```bash
cp .env.example .env
```

Edit `.env`:
```env
NEXUS_URL=https://nexus.example.com
NEXUS_USERNAME=admin
NEXUS_PASSWORD=your-password
NEXUS_VERIFY_SSL=true
NEXUS_TIMEOUT=30
```

### 2. Basic Usage

```python
from nexus_client import NexusClient
from nexus_client.config import Config

# Load config from .env file
config = Config()

# Create client
with NexusClient(**config.get_client_kwargs()) as client:
    # Get server status
    status = client.get_status()
    print(f"Nexus version: {status['version']}")

    # List repositories
    repos = client.repositories.list()
    for repo in repos:
        print(f"{repo['name']} - {repo['format']}")
```

Or create client directly:

```python
from nexus_client import NexusClient

client = NexusClient(
    base_url="https://nexus.example.com",
    username="admin",
    password="admin123"
)

# Your code here...
client.close()
```

## Usage Examples

### Repository Management

```python
# List all repositories
repos = client.repositories.list()

# Get specific repository
repo = client.repositories.get("maven-releases")

# Create a Maven hosted repository
client.repositories.create_maven_hosted(
    name="my-maven-repo",
    blob_store="default",
    version_policy="RELEASE"
)

# Create an NPM hosted repository
client.repositories.create_npm_hosted(
    name="my-npm-repo",
    blob_store="default"
)

# Create a Docker hosted repository
client.repositories.create_docker_hosted(
    name="my-docker-repo",
    http_port=8082
)

# Delete a repository
client.repositories.delete("my-maven-repo")
```

### Component Search

```python
# Search all components in a repository
result = client.search.search(repository="maven-releases")

# Search by component name
result = client.search.search(
    name="junit",
    format="maven2"
)

# Search by group and artifact
result = client.search.search(
    group="org.springframework",
    name="spring-core",
    version="5.3.0"
)

# Search assets by checksum
result = client.search.search_assets(
    sha1="abc123...",
    repository="maven-releases"
)

# Pagination
continuation_token = None
while True:
    result = client.search.search(
        repository="maven-releases",
        continuation_token=continuation_token
    )

    for component in result['items']:
        print(component['name'])

    continuation_token = result.get('continuationToken')
    if not continuation_token:
        break
```

### Upload Components

```python
# Upload Maven component
client.components.upload_maven(
    repository="maven-releases",
    group_id="com.example",
    artifact_id="my-app",
    version="1.0.0",
    file_path="/path/to/my-app-1.0.0.jar",
    packaging="jar"
)

# Upload NPM package
client.components.upload_npm(
    repository="npm-hosted",
    package_path="/path/to/package-1.0.0.tgz"
)

# Upload raw file
client.components.upload_raw(
    repository="raw-hosted",
    directory="files/documents",
    filename="readme.txt",
    file_path="/path/to/readme.txt"
)
```

### Component and Asset Management

```python
# List components
result = client.components.list(repository="maven-releases")
for component in result['items']:
    print(f"{component['name']} - {component['version']}")

# Get component details
component = client.components.get(component_id="abc123...")

# Delete component
client.components.delete(component_id="abc123...")

# List assets
result = client.assets.list(repository="maven-releases")

# Get asset details
asset = client.assets.get(asset_id="xyz789...")

# Download asset
client.assets.download(
    asset_id="xyz789...",
    output_path="/path/to/save/file.jar"
)

# Delete asset
client.assets.delete(asset_id="xyz789...")
```

### User Management

```python
# List users
users = client.security.list_users()

# Create user
user = client.security.create_user(
    user_id="john.doe",
    first_name="John",
    last_name="Doe",
    email="john.doe@example.com",
    password="SecurePassword123!",
    roles=["nx-developer"],
    status="active"
)

# Update user
client.security.update_user(
    user_id="john.doe",
    first_name="John",
    last_name="Doe",
    email="john.doe@example.com",
    roles=["nx-developer", "nx-admin"]
)

# Change password
client.security.change_password(
    user_id="john.doe",
    new_password="NewPassword456!"
)

# Delete user
client.security.delete_user("john.doe")
```

### Role Management

```python
# List roles
roles = client.security.list_roles()

# Get role details
role = client.security.get_role("nx-admin")

# Create role
role = client.security.create_role(
    role_id="custom-developer",
    name="Custom Developer",
    description="Developer with custom privileges",
    privileges=["nx-repository-view-*-*-browse"],
    roles=[]
)

# Update role
client.security.update_role(
    role_id="custom-developer",
    name="Custom Developer",
    description="Updated description",
    privileges=["nx-repository-view-*-*-browse", "nx-repository-view-*-*-read"]
)

# Delete role
client.security.delete_role("custom-developer")
```

### Task Management

```python
# List all tasks
tasks = client.tasks.list()

# Get task details
task = client.tasks.get(task_id="abc123...")

# Run task immediately
client.tasks.run(task_id="abc123...")

# Stop running task
client.tasks.stop(task_id="abc123...")
```

### Blob Store Management

```python
# List blob stores
blob_stores = client.blob_stores.list()

# Get blob store configuration
config = client.blob_stores.get_file_blob_store("default")

# Create file blob store
client.blob_stores.create_file_blob_store(
    name="my-blob-store",
    path="/data/blobs/my-blob-store",
    soft_quota_type="spaceRemainingQuota",
    soft_quota_limit=10000  # MB
)

# Update blob store
client.blob_stores.update_file_blob_store(
    name="my-blob-store",
    soft_quota_limit=20000
)

# Get quota status
status = client.blob_stores.get_quota_status("my-blob-store")

# Delete blob store
client.blob_stores.delete("my-blob-store")
```

## Running Examples

The `examples/` directory contains several ready-to-run scripts:

```bash
# Basic usage - view server info, repos, users, etc.
python examples/basic_usage.py

# Search for components
python examples/search_components.py

# Manage repositories
python examples/manage_repositories.py

# Upload components
python examples/upload_components.py

# Manage users and roles
python examples/manage_users_roles.py
```

## API Reference

### NexusClient

Main client class for interacting with Nexus.

#### Constructor Parameters

- `base_url` (str): Base URL of Nexus server (e.g., "https://nexus.example.com")
- `username` (str, optional): Username for authentication
- `password` (str, optional): Password for authentication
- `verify_ssl` (bool, default=True): Verify SSL certificates
- `timeout` (int, default=30): Request timeout in seconds

#### Modules

- `client.repositories`: Repository management API
- `client.components`: Component management API
- `client.assets`: Asset management API
- `client.search`: Search API
- `client.security`: User, role, and privilege management
- `client.tasks`: Task management API
- `client.blob_stores`: Blob store management API

## Error Handling

The library provides custom exceptions for better error handling:

```python
from nexus_client.exceptions import (
    NexusException,
    NexusAuthenticationError,
    NexusNotFoundError,
    NexusForbiddenError,
    NexusBadRequestError
)

try:
    repo = client.repositories.get("non-existent")
except NexusNotFoundError as e:
    print(f"Repository not found: {e}")
except NexusForbiddenError as e:
    print(f"Access forbidden: {e}")
except NexusAuthenticationError as e:
    print(f"Authentication failed: {e}")
except NexusException as e:
    print(f"Error: {e}")
```

## Development

### Project Structure

```
nexus-python-app/
├── nexus_client/           # Main package
│   ├── __init__.py
│   ├── client.py          # Main client class
│   ├── config.py          # Configuration management
│   ├── exceptions.py      # Custom exceptions
│   ├── repositories.py    # Repository API
│   ├── components.py      # Component API
│   ├── assets.py          # Asset API
│   ├── search.py          # Search API
│   ├── security.py        # Security API
│   ├── tasks.py           # Task API
│   └── blob_stores.py     # Blob store API
├── examples/              # Example scripts
│   ├── basic_usage.py
│   ├── search_components.py
│   ├── manage_repositories.py
│   ├── upload_components.py
│   └── manage_users_roles.py
├── .env.example           # Example environment file
├── .gitignore
├── requirements.txt       # Dependencies
├── pyproject.toml        # Package configuration
└── README.md
```

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests (when available)
pytest

# Run with coverage
pytest --cov=nexus_client
```

## Requirements

- Python 3.8+
- requests >= 2.31.0
- python-dotenv >= 1.0.0

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues related to:
- This client library: Open an issue on GitHub
- Nexus Repository Manager: Visit [Sonatype Support](https://help.sonatype.com/)

## Resources

- [Nexus Repository Manager Documentation](https://help.sonatype.com/repomanager3)
- [Nexus REST API Documentation](https://help.sonatype.com/repomanager3/integrations/rest-and-integration-api)
- [Sonatype Community](https://community.sonatype.com/)
