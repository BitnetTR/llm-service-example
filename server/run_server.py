import os
import subprocess
import sys

from dotenv import load_dotenv

load_dotenv()

PORT = os.getenv("SERVER_PORT", "8001")
HOST = os.getenv("SERVER_HOST", "0.0.0.0")


def main():
    print(f"Starting LLM API server on {HOST}:{PORT}")

    command = [
        sys.executable,
        "-m",
        "uvicorn",
        "server:app",
        "--host",
        HOST,
        "--port",
        PORT,
    ]

    subprocess.run(command)


if __name__ == "__main__":
    main()