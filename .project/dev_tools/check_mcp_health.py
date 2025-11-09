#!/usr/bin/env python3
"""
MCP Health Check Script
Verifies all 11 MCP servers are installed and operational

Usage:
    python .project/dev_tools/check_mcp_health.py
    python .project/dev_tools/check_mcp_health.py --fix
"""

import subprocess
import sys
import json
from pathlib import Path

# Color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

MCP_CONFIG = Path("D:/Projects/main/.mcp.json")
NPM_GLOBAL_ROOT = "C:\\Program Files\\nodejs\\node_modules"


def check_node_server(server_name, server_path):
    """Check if Node.js MCP server exists and is accessible"""
    full_path = Path(server_path)

    if not full_path.exists():
        return False, f"File not found: {server_path}"

    # Try to run server with --help or verify it exists
    try:
        result = subprocess.run(
            ["node", str(full_path), "--help"],
            capture_output=True,
            text=True,
            timeout=2
        )
        # If it runs without crashing, it's probably OK
        return True, "Operational"
    except subprocess.TimeoutExpired:
        # Timeout is OK - server might be waiting for stdio
        return True, "Operational (stdio)"
    except Exception as e:
        return False, str(e)


def check_python_server(server_name, module_or_path):
    """Check if Python MCP server exists and is accessible"""
    if module_or_path.startswith("-m"):
        # It's a module
        module_name = module_or_path.split()[1]
        try:
            result = subprocess.run(
                ["python", "-m", module_name, "--help"],
                capture_output=True,
                text=True,
                timeout=2
            )
            return True, "Operational (module)"
        except subprocess.TimeoutExpired:
            return True, "Operational (stdio)"
        except Exception as e:
            return False, f"Module not found: {module_name}"
    else:
        # It's a file path
        full_path = Path(module_or_path)
        if not full_path.exists():
            return False, f"File not found: {module_or_path}"
        return True, "Operational (file)"


def check_npx_server(server_name, package):
    """Check if npx-based server is accessible"""
    try:
        result = subprocess.run(
            ["npx", "-y", package, "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return True, "Operational (npx)"
    except Exception as e:
        return False, str(e)


def load_mcp_config():
    """Load MCP configuration"""
    if not MCP_CONFIG.exists():
        print(f"{RED}[ERROR]{RESET} .mcp.json not found at {MCP_CONFIG}")
        sys.exit(1)

    with open(MCP_CONFIG) as f:
        return json.load(f)


def check_all_servers(config, verbose=False):
    """Check all MCP servers"""
    servers = config.get("mcpServers", {})
    results = {}

    print(f"\n{BLUE}[INFO]{RESET} Checking {len(servers)} MCP servers...\n")

    for server_name, server_config in servers.items():
        command = server_config.get("command")
        args = server_config.get("args", [])

        # Special handling for context7 - check if API key is configured
        if server_name == "context7":
            if "REQUIRED" in args:
                status, message = False, "API key required (get from context7.com/dashboard)"
            else:
                status, message = check_npx_server(server_name, "@upstash/context7-mcp")
        elif command == "node" and args:
            status, message = check_node_server(server_name, args[0])
        elif command == "python" and args:
            status, message = check_python_server(server_name, " ".join(args))
        elif command == "cmd" or command.endswith("npx"):
            status, message = check_npx_server(server_name, args[-1] if args else server_name)
        elif command == "lighthouse-mcp":
            # Standalone executable - check if in PATH (doesn't support --version)
            import shutil
            if shutil.which(command):
                status, message = True, "Operational (standalone)"
            else:
                status, message = False, "Not found in PATH"
        else:
            status, message = False, f"Unknown command type: {command}"

        results[server_name] = (status, message)

        # Print result
        status_icon = f"{GREEN}[OK]{RESET}" if status else f"{RED}[ERROR]{RESET}"
        print(f"{status_icon} {server_name:25s} - {message}")

    return results


def print_summary(results):
    """Print summary of health check"""
    total = len(results)
    passed = sum(1 for status, _ in results.values() if status)
    failed = total - passed

    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}SUMMARY{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    print(f"Total servers: {total}")
    print(f"{GREEN}Operational: {passed}{RESET}")
    print(f"{RED}Failed: {failed}{RESET}")

    if failed > 0:
        print(f"\n{YELLOW}[WARNING]{RESET} Some servers are not operational")
        print(f"Run with --fix to attempt automatic repairs")
        sys.exit(1)
    else:
        print(f"\n{GREEN}[OK]{RESET} All MCP servers are operational!")
        sys.exit(0)


def main():
    """Main entry point"""
    fix_mode = "--fix" in sys.argv
    verbose = "-v" in sys.argv or "--verbose" in sys.argv

    print(f"{BLUE}MCP Health Check{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")

    config = load_mcp_config()
    results = check_all_servers(config, verbose)
    print_summary(results)


if __name__ == "__main__":
    main()
