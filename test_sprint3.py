"""Test suite for Sprint 3: Basic CLI.

Tests all CLI commands and functionality.
"""

import subprocess
import sys


def run_command(cmd: list) -> tuple:
    """Run a command and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    return result.returncode, result.stdout, result.stderr


def test_cli_help():
    """Test CLI help command."""
    print("Test 1: CLI Help...")
    code, out, err = run_command(["py", "-m", "xojodoc.cli", "--help"])
    
    assert code == 0, f"Help command failed with code {code}"
    assert "XojoDoc" in out, "Help should contain 'XojoDoc'"
    assert "search" in out, "Help should list 'search' command"
    assert "cls" in out or "class" in out, "Help should list class command"
    assert "method" in out, "Help should list 'method' command"
    
    print("  ✓ PASSED\n")


def test_search_command():
    """Test search command."""
    print("Test 2: Search Command...")
    code, out, err = run_command(["py", "-m", "xojodoc.cli", "search", "Graphics"])
    
    assert code == 0, f"Search failed with code {code}"
    assert "Graphics" in out, "Search should find Graphics class"
    assert "graphics.Graphics" in out, "Should show module.class format"
    
    print("  ✓ PASSED\n")


def test_class_command():
    """Test class command."""
    print("Test 3: Class Command...")
    code, out, err = run_command(["py", "-m", "xojodoc.cli", "cls", "Graphics"])
    
    assert code == 0, f"Class command failed with code {code}"
    assert "Graphics" in out, "Should display Graphics class"
    assert "Properties" in out, "Should show properties section"
    assert "Methods" in out, "Should show methods section"
    
    print("  ✓ PASSED\n")


def test_method_command():
    """Test method command."""
    print("Test 4: Method Command...")
    code, out, err = run_command(["py", "-m", "xojodoc.cli", "method", "Graphics", "DrawText"])
    
    assert code == 0, f"Method command failed with code {code}"
    assert "DrawText" in out, "Should display DrawText method"
    assert "Signature" in out or "Parameters" in out, "Should show signature/parameters"
    
    print("  ✓ PASSED\n")


def test_class_not_found():
    """Test class not found error."""
    print("Test 5: Class Not Found...")
    code, out, err = run_command(["py", "-m", "xojodoc.cli", "cls", "NonExistentClass"])
    
    assert code != 0, "Should return error code for non-existent class"
    assert "not found" in out.lower() or "not found" in err.lower(), "Should show 'not found' message"
    
    print("  ✓ PASSED\n")


def test_method_not_found():
    """Test method not found error."""
    print("Test 6: Method Not Found...")
    code, out, err = run_command(["py", "-m", "xojodoc.cli", "method", "Graphics", "NonExistentMethod"])
    
    assert code != 0, "Should return error code for non-existent method"
    assert "not found" in out.lower() or "not found" in err.lower(), "Should show 'not found' message"
    
    print("  ✓ PASSED\n")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Sprint 3: Basic CLI Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        test_cli_help,
        test_search_command,
        test_class_command,
        test_method_command,
        test_class_not_found,
        test_method_not_found,
    ]
    
    failed = []
    
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"  ✗ FAILED: {e}\n")
            failed.append((test.__name__, str(e)))
        except Exception as e:
            print(f"  ✗ ERROR: {e}\n")
            failed.append((test.__name__, str(e)))
    
    print("=" * 60)
    print("Test Results")
    print("=" * 60)
    print(f"Total tests: {len(tests)}")
    print(f"Passed: {len(tests) - len(failed)}")
    print(f"Failed: {len(failed)}")
    
    if failed:
        print("\nFailed tests:")
        for name, error in failed:
            print(f"  - {name}: {error}")
        sys.exit(1)
    else:
        print("\n✓ All tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
