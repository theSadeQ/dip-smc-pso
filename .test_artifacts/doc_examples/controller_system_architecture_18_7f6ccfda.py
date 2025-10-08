# Example from: docs\architecture\controller_system_architecture.md
# Index: 18
# Runnable: False
# Hash: 7f6ccfda

class SecurityManager:
    """Security management for production deployment."""

    @staticmethod
    def validate_configuration_integrity(config_path: str) -> bool:
        """Validate configuration file integrity."""

        # Check file permissions
        file_stat = os.stat(config_path)
        if file_stat.st_mode & 0o077:  # Check for world/group writable
            raise SecurityError("Configuration file has insecure permissions")

        # Validate configuration content
        with open(config_path, 'r') as f:
            config_content = f.read()

        # Check for suspicious content
        suspicious_patterns = [
            r'import\s+os',
            r'exec\s*\(',
            r'eval\s*\(',
            r'__import__',
            r'subprocess'
        ]

        for pattern in suspicious_patterns:
            if re.search(pattern, config_content):
                raise SecurityError(f"Suspicious pattern found in config: {pattern}")

        return True

    @staticmethod
    def sanitize_user_input(user_input: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize user input to prevent injection attacks."""

        sanitized = {}

        for key, value in user_input.items():
            # Validate key names
            if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', key):
                raise SecurityError(f"Invalid parameter name: {key}")

            # Sanitize values based on type
            if isinstance(value, str):
                # Remove potentially dangerous characters
                sanitized_value = re.sub(r'[<>\"\'&]', '', value)
                sanitized[key] = sanitized_value
            elif isinstance(value, (int, float)):
                # Validate numeric ranges
                if abs(value) > 1e6:  # Reasonable upper bound
                    raise SecurityError(f"Numeric value out of range: {value}")
                sanitized[key] = value
            else:
                sanitized[key] = value

        return sanitized