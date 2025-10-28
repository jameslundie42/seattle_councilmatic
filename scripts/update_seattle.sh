#!/bin/bash
set -e  # Exit on error

echo "================================"
echo "Seattle Councilmatic Update"
echo "================================"

echo ""
echo "1. Running Pupa scrapers..."
pupa update seattle "$@"

echo ""
echo "2. Syncing to Councilmatic models..."
python manage.py sync_councilmatic

echo ""
echo "3. Rebuilding search index..."
python manage.py update_index

echo ""
echo "================================"
echo "✓ Update complete!"
echo "================================"