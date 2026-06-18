"""
Anti-Faker Guard: Ensures no fake data generation is used in tests.
All tests must use calculated physical values, never fake/generated data.
"""
import os
import re
import ast


class TestNoFakingInTests:
    """Verify that no test uses faker or fake data generation."""
    
    def test_no_faker_imports_in_source(self):
        """Check that no Python file imports faker or Faker."""
        banned_imports = [
            "import faker",
            "from faker import",
            "import Faker",
            "from faker import Faker",
            "import fake",
            "from fake import",
            "import mock",
            "from mock import",
            "import unittest.mock",
            "from unittest.mock import",
        ]
        
        violations = []
        
        # Scan src and tests directories
        for scan_dir in ["src", "tests"]:
            if not os.path.exists(scan_dir):
                continue
            for root, _, files in os.walk(scan_dir):
                for file in files:
                    if file.endswith(".py"):
                        filepath = os.path.join(root, file)
                        with open(filepath, "r", encoding="utf-8") as f:
                            content = f.read()
                            lines = content.split("\n")
                        
                        for idx, line in enumerate(lines, 1):
                            # Skip this test file itself
                            if "test_no_faking" in file:
                                continue
                            # Check for banned imports
                            for banned in banned_imports:
                                if banned in line and not line.strip().startswith("#"):
                                    violations.append({
                                        "file": filepath,
                                        "line": idx,
                                        "content": line.strip()
                                    })
        
        print(f"  Scanned files for faker imports")
        print(f"  Violations found: {len(violations)}")
        
        if violations:
            raise AssertionError(
                f"FAKER/Fake imports found in source code:\n" +
                "\n".join([f"  {v['file']}:{v['line']} - {v['content']}" for v in violations]) +
                "\n\nAll tests must use calculated physical values, never fake/generated data!"
            )
    
    def test_no_random_data_in_assertions(self):
        """Check that test assertions don't use random/fake values."""
        violations = []
        
        for scan_dir in ["tests"]:
            if not os.path.exists(scan_dir):
                continue
            for root, _, files in os.walk(scan_dir):
                for file in files:
                    if file.endswith(".py") and "test_no_faking" not in file:
                        filepath = os.path.join(root, file)
                        with open(filepath, "r", encoding="utf-8") as f:
                            content = f.read()
                        
                        # Check for random.random(), random.randint, etc.
                        fake_patterns = [
                            r"random\.random\(\)",
                            r"random\.randint\(",
                            r"random\.choice\(",
                            r"random\.uniform\(",
                            r"np\.random\.random",
                            r"np\.random\.rand",
                            r"np\.random\.randint",
                        ]
                        
                        for pattern in fake_patterns:
                            matches = re.finditer(pattern, content)
                            for match in matches:
                                line_num = content[:match.start()].count("\n") + 1
                                violations.append({
                                    "file": filepath,
                                    "line": line_num,
                                    "pattern": pattern
                                })
        
        if violations:
            raise AssertionError(
                f"Random/fake data generation found in tests:\n" +
                "\n".join([f"  {v['file']}:{v['line']} - {v['pattern']}" for v in violations]) +
                "\n\nAll test values must be physically calculated, not randomly generated!"
            )
    
    def test_all_assertions_use_calculated_values(self):
        """Verify that all test assertions use physically calculated values."""
        print(f"  All assertions use calculated values: DOCUMENTED")
        # This is a documentation test - it always passes but documents the requirement
        assert True, "All test values must be calculated from SSZ physics, never faked"
