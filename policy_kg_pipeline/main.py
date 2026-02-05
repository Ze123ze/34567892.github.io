from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from .pipeline import MultiAgentKGPipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="DeepSea policy KG extractor")
    parser.add_argument("--doc-id", required=True)
    parser.add_argument("--title", default=None)
    parser.add_argument("--input", required=True, help="政策文本文件路径")
    parser.add_argument("--output", default="output.json")
    return parser.parse_args()


async def _run(args: argparse.Namespace) -> None:
    text = Path(args.input).read_text(encoding="utf-8")
    pipeline = MultiAgentKGPipeline()
    result = await pipeline.run(args.doc_id, args.title, text)
    Path(args.output).write_text(
        json.dumps(result.model_dump(), ensure_ascii=False, indent=2), encoding="utf-8"
    )


def main() -> None:
    args = parse_args()
    asyncio.run(_run(args))


if __name__ == "__main__":
    main()
