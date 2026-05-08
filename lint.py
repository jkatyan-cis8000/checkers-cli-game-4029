#!/usr/bin/env python3
"""
Lint.py: Enforces layered architecture and code quality rules.

Rules:
1. Every file under src/ belongs in exactly one layer directory.
2. Imports may only target layers in the file's own "may import from" set.
3. No file exceeds 300 lines.
4. Tests live under tests/ (not under src/) and are not lint-checked here.
"""

import ast
import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Layer definitions and allowed imports per layer
LAYERS = {
    'types': {'types'},
    'config': {'types', 'config'},
    'repo': {'types', 'config', 'repo'},
    'providers': {'types', 'config', 'utils', 'providers'},
    'service': {'types', 'config', 'repo', 'providers', 'service'},
    'utils': {'utils'},
    'runtime': {'types', 'config', 'repo', 'service', 'providers', 'runtime'},
    'ui': {'types', 'config', 'service', 'runtime', 'providers', 'ui'},
}

# Allowed layer directories
ALLOWED_LAYERS = set(LAYERS.keys())
SRC_DIR = Path('/workspace/checkers-cli-game-4029/src')
MAX_LINES = 300


def get_layer_for_file(filepath: Path) -> str | None:
    """Determine which layer a file belongs to based on its directory."""
    try:
        rel_path = filepath.relative_to(SRC_DIR)
        parts = rel_path.parts
        if parts and parts[0] in ALLOWED_LAYERS:
            return parts[0]
    except ValueError:
        pass
    return None


def get_imported_modules(node: ast.AST) -> List[str]:
    """Extract module names from import statements."""
    modules = []
    if isinstance(node, ast.Import):
        for alias in node.names:
            modules.append(alias.name.split('.')[0])
    elif isinstance(node, ast.ImportFrom):
        if node.module:
            modules.append(node.module.split('.')[0])
    return modules


def get_allowed_imports(layer: str) -> Set[str]:
    """Get set of allowed import module names for a layer."""
    allowed = LAYERS[layer]
    # Map layer names to actual module names used in imports
    layer_to_module = {
        'types': 'types',
        'config': 'config',
        'repo': 'repo',
        'providers': 'providers',
        'service': 'service',
        'utils': 'utils',
        'runtime': 'runtime',
        'ui': 'ui',
    }
    return {layer_to_module[l] for l in allowed if l in layer_to_module}


def check_file(filepath: Path) -> List[str]:
    """Check a single file for linting violations."""
    violations = []
    
    # Rule 1: File must be in a valid layer directory
    layer = get_layer_for_file(filepath)
    if layer is None:
        violations.append(f"{filepath}: File is not in a valid layer directory under src/")
        return violations
    
    # Check line count (Rule 3)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) > MAX_LINES:
                violations.append(f"{filepath}:{len(lines)}: File exceeds {MAX_LINES} lines ({len(lines)} lines)")
    except Exception as e:
        violations.append(f"{filepath}: Error reading file: {e}")
        return violations
    
    # Check imports (Rule 2)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        tree = ast.parse(source, filename=str(filepath))
        
        allowed_modules = get_allowed_imports(layer)
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                imported = get_imported_modules(node)
                for module in imported:
                    # Check if it's an internal import (starts with 'src.')
                    # or a direct layer import
                    if module in {'src', layer} or module in ALLOWED_LAYERS:
                        # This is an internal import - validate against layer rules
                        if module not in allowed_modules:
                            violations.append(
                                f"{filepath}: Invalid import '{module}'. "
                                f"Layer '{layer}' may only import from: {', '.join(sorted(allowed_modules))}"
                            )
    except SyntaxError as e:
        violations.append(f"{filepath}:{e.lineno or 0}: Syntax error: {e.msg}")
    
    return violations


def find_all_py_files(directory: Path) -> List[Path]:
    """Find all Python files in directory, excluding __pycache__ and .git."""
    py_files = []
    for root, dirs, files in os.walk(directory):
        # Skip pycache and git directories
        dirs[:] = [d for d in dirs if d not in {'__pycache__', '.git', '.state'}]
        for file in files:
            if file.endswith('.py'):
                py_files.append(Path(root) / file)
    return sorted(py_files)


def main() -> int:
    """Run linting and return exit code."""
    all_violations = []
    
    # Check all Python files under src/
    if SRC_DIR.exists():
        py_files = find_all_py_files(SRC_DIR)
        for filepath in py_files:
            violations = check_file(filepath)
            all_violations.extend(violations)
    
    # Report results
    if all_violations:
        print("Linting failed with the following violations:\n")
        for v in all_violations:
            print(f"  {v}")
        print(f"\n{len(all_violations)} violation(s) found.")
        return 1
    else:
        print("Linting passed. No violations found.")
        return 0


if __name__ == '__main__':
    sys.exit(main())
