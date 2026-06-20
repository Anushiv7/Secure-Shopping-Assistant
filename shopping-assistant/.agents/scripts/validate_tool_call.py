import sys
import json

def main():
    try:
        # Read tool call data from stdin
        input_data = sys.stdin.read()
        if not input_data:
            sys.exit(0)

        data = json.loads(input_data)

        # The hook system typically passes the tool call in a format like:
        # {"tool": "run_command", "arguments": {"command": "...", ...}}
        arguments = data.get("arguments", {})
        command = arguments.get("command", "")

        if not command:
            sys.exit(0)

        # List of highly destructive patterns to block
        forbidden_patterns = [
            "rm -rf /",
            "rm -rf C:",
            "mkfs",
            "format ",
            "dd if=",
            "shutdown",
            "poweroff"
        ]

        for pattern in forbidden_patterns:
            if pattern in command:
                print(f"SECURITY BLOCK: Destructive command detected: {pattern}", file=sys.stderr)
                sys.exit(1)

        sys.exit(0)

    except json.JSONDecodeError:
        print("Error: Failed to decode tool call JSON", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error in validation script: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
