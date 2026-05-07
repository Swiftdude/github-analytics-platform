from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict

from dotenv import load_dotenv

from github_analytics_platform.main import run_analysis


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze a GitHub repository for health and maintainability.")
    parser.add_argument("--owner", help="GitHub repository owner or organization name.")
    parser.add_argument("--repo", help="GitHub repository name.")
    parser.add_argument(
        "--format",
        choices=["pretty", "json"],
        default="pretty",
        help="Output format.",
    )
    return parser.parse_args()


def main() -> None:
    load_dotenv()
    args = parse_args()
    token = os.getenv("GITHUB_TOKEN")
    result = run_analysis(owner=args.owner, repo=args.repo, token=token)

    if args.format == "json":
        print(json.dumps(asdict(result), default=str, indent=2))
        return

    print(f"Repository: {result.repository}")
    print("Predictions:")
    for key, value in result.predictions.items():
        print(f"  - {key}: {value}")

    print("Metrics:")
    for key, value in result.metrics.items():
        print(f"  - {key}: {value}")

    print("Recommendations:")
    for item in result.recommendations:
        print(f"  - {item}")


if __name__ == "__main__":
    main()
