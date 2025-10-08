# Example from: docs\tools\ast_traversal_patterns.md
# Index: 17
# Runnable: False
# Hash: 63612b22

# example-metadata:
# runnable: false

def extract_from_file(file_path: str) -> List[Dict]:
    try:
        source = Path(file_path).read_text(encoding='utf-8')
        tree = ast.parse(source)

        extractor = CodeClaimExtractor()
        extractor.visit(tree)
        return extractor.claims

    except SyntaxError as e:
        logger.warning(f"Syntax error in {file_path}:{e.lineno} - skipping")
        return []

    except UnicodeDecodeError:
        logger.error(f"Encoding issue in {file_path} - skipping")
        return []

    except Exception as e:
        logger.error(f"Unexpected error in {file_path}: {e}")
        return []