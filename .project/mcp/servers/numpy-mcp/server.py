#!/usr/bin/env python3
"""
NumPy MCP Server for Numerical Computations
Provides numerical analysis and linear algebra via MCP protocol
"""

import sys
import json
import numpy as np


def handle_matrix_op(operation, matrix_a, matrix_b=None):
    """Handle matrix operations"""
    try:
        a = np.array(matrix_a)

        if operation == "eigenvalues":
            eigenvalues = np.linalg.eigvals(a)
            return {
                "success": True,
                "eigenvalues": eigenvalues.tolist()
            }
        elif operation == "inverse":
            inv = np.linalg.inv(a)
            return {
                "success": True,
                "result": inv.tolist()
            }
        elif operation == "multiply" and matrix_b:
            b = np.array(matrix_b)
            result = np.matmul(a, b)
            return {
                "success": True,
                "result": result.tolist()
            }
        else:
            return {"success": False, "error": "Invalid operation"}

    except Exception as e:
        return {"success": False, "error": str(e)}


def handle_stats(data):
    """Calculate statistics"""
    try:
        arr = np.array(data)
        return {
            "success": True,
            "mean": float(np.mean(arr)),
            "median": float(np.median(arr)),
            "std": float(np.std(arr)),
            "var": float(np.var(arr)),
            "min": float(np.min(arr)),
            "max": float(np.max(arr))
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    """MCP Server main loop"""
    print("[INFO] NumPy MCP Server started on stdio", file=sys.stderr)

    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break

            request = json.loads(line)
            method = request.get("method")
            params = request.get("params", {})

            if method == "matrix_op":
                result = handle_matrix_op(
                    params.get("operation"),
                    params.get("matrix_a"),
                    params.get("matrix_b")
                )
            elif method == "stats":
                result = handle_stats(params.get("data"))
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
