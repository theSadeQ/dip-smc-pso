#!/usr/bin/env python3
"""
Pandas MCP Server for Data Analysis
Provides pandas data manipulation and analysis via MCP protocol
"""

import sys
import json
import pandas as pd
import numpy as np
from pathlib import Path


def handle_load_csv(filepath):
    """Load CSV file and return summary"""
    try:
        df = pd.read_csv(filepath)
        return {
            "success": True,
            "shape": df.shape,
            "columns": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "head": df.head().to_dict(),
            "stats": df.describe().to_dict()
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def handle_analyze(filepath, column=None):
    """Analyze data in CSV file"""
    try:
        df = pd.read_csv(filepath)
        if column and column in df.columns:
            return {
                "success": True,
                "mean": float(df[column].mean()),
                "median": float(df[column].median()),
                "std": float(df[column].std()),
                "min": float(df[column].min()),
                "max": float(df[column].max())
            }
        return {"success": True, "summary": df.describe().to_dict()}
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    """MCP Server main loop"""
    print("[INFO] Pandas MCP Server started on stdio", file=sys.stderr)

    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break

            request = json.loads(line)
            method = request.get("method")
            params = request.get("params", {})

            if method == "load_csv":
                result = handle_load_csv(params.get("filepath"))
            elif method == "analyze":
                result = handle_analyze(
                    params.get("filepath"),
                    params.get("column")
                )
            else:
                result = {"success": False, "error": "Unknown method"}

            response = {
                "id": request.get("id"),
                "result": result
            }
            print(json.dumps(response), flush=True)

        except Exception as e:
            print(f"[ERROR] {str(e)}", file=sys.stderr)
            continue


if __name__ == "__main__":
    main()
