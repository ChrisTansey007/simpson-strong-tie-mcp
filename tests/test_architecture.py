import ast
import pathlib


def test_domain_has_no_framework_dependencies():
    domain_path = pathlib.Path(__file__).parent.parent / "packages" / "domain" / "simpson_domain"
    py_files = list(domain_path.glob("*.py"))

    prohibited = ["fastapi", "mcp", "sqlalchemy", "react", "httpx", "uvicorn"]

    for file in py_files:
        tree = ast.parse(file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    for p in prohibited:
                        assert not alias.name.startswith(p), (
                            f"Prohibited import {alias.name} in {file}"
                        )
            elif isinstance(node, ast.ImportFrom) and node.module:
                for p in prohibited:
                    assert not node.module.startswith(p), (
                        f"Prohibited import {node.module} in {file}"
                    )
