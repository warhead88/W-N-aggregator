#!/bin/sh
# Run migrations
alembic upgrade head
# Start bot
exec "$@"
