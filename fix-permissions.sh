#!/bin/bash
# Fix permissions for Podman rootless mode
# This script sets the correct ownership for the downloads folder

set -e

echo "Fixing permissions for Podman rootless mode..."

# Create downloads directory if it doesn't exist
mkdir -p downloads

# Set correct ownership using podman unshare
# This maps UID 1000 in the container namespace to the correct UID on the host
podman unshare chown 1000:1000 downloads
podman unshare chmod 755 downloads

echo "✓ Permissions fixed successfully!"
echo "The downloads folder is now owned by UID 100999 on the host,"
echo "which maps to UID 1000 (appuser) in the container."
echo ""
echo "You can now start the container with: podman compose up -d"
