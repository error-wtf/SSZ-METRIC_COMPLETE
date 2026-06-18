"""Add print statements to all test functions for verbose output."""
import ast
import re
from pathlib import Path

def add_print_to_test_file(filepath):
    """Add print statements to all test functions in a file."""
    content = filepath.read_text(encoding='utf-8')
    
    # Find all test function definitions
    test_funcs = re.findall(r'(def test_\w+\([^)]*\):\s*\n\s*"""[^"]*""")', content)
    
    for func_match in test_funcs:
        # Check if already has print
        func_start = content.find(func_match)
        func_end = content.find('\ndef ', func_start + len(func_match))
        if func_end == -1:
            func_end = len(content)
        func_body = content[func_start:func_end]
        
        if 'print(' not in func_body:
            # Add print statement after docstring
            docstring_end = func_match.find('"""') + 3
            after_docstring = func_match[docstring_end:]
            
            # Extract test name for print
            test_name = re.search(r'def (test_\w+)', func_match).group(1)
            
            # Create new function with print
            indent = "    "
            new_func = (func_match[:docstring_end] + 
                       f'\n{indent}print("  Running: {test_name}")' +
                       after_docstring)
            
            content = content.replace(func_match, new_func)
    
    filepath.write_text(content, encoding='utf-8')
    print(f"Updated: {filepath}")

# Update all test files
test_dir = Path("e:/clone/SSZ-METRIC_COMPLETE/tests")
for test_file in test_dir.glob("test_*.py"):
    add_print_to_test_file(test_file)

print("\n[OK] All test files updated with print statements!")
