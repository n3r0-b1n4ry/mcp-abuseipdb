#!/usr/bin/env python3

import asyncio
from modules import AbuseIPDBServer

async def main():
    """Main entry point"""
    server = AbuseIPDBServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main()) 