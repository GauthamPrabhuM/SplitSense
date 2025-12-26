#!/usr/bin/env python3
"""
Start script for Railway deployment.
Reads PORT from environment variable and starts the server.
"""
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, workers=2)

