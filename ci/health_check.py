"""Poll a local or containerized /healthz endpoint until it returns HTTP 200."""
import sys
import time
import urllib.error
import urllib.request

def main():
    url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:5099/healthz"
    deadline = time.monotonic() + 30
    last_error = "no response"
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                if response.status == 200:
                    print(f"Health check passed: {url}")
                    return 0
                last_error = f"HTTP {response.status}"
        except (OSError, urllib.error.URLError) as error:
            last_error = str(error)
        time.sleep(1)
    print(f"Health check failed for {url}: {last_error}", file=sys.stderr)
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
