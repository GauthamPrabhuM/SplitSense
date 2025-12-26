#!/usr/bin/env python3
"""
Start script for Railway deployment.
Reads PORT from environment variable and starts the server.
"""
import os
import sys
import uvicorn

if __name__ == "__main__":
    try:
        port = int(os.getenv("PORT", "8000"))
        print(f"Starting server on port {port}", file=sys.stderr)
        print(f"PORT environment variable: {os.getenv('PORT', 'not set')}", file=sys.stderr)
        uvicorn.run("main:app", host="0.0.0.0", port=port, workers=1, log_level="info")
    except Exception as e:
        print(f"Error starting server: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

