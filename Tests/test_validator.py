import sys
import os
import subprocess

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestCase:
    def __init__(self, name, cache_size, assoc, block_size, policy, num_blocks, input_file, expected):
        self.name = name
        self.command = f"python {os.path.join(os.path.dirname(os.path.dirname(__file__)), 'main.py')} {cache_size} {assoc} {block_size} {policy} {num_blocks} {input_file}"
        self.additional_command = f"python {os.path.join(os.path.dirname(os.path.dirname(__file__)), 'main.py')} {cache_size} {assoc} {block_size} {policy} 0 {input_file}"
        self.expected = expected

def compare_outputs(expected, actual, tolerance=0.01):
    if len(expected) != len(actual):
        return False
    return all(abs(a - b) <= tolerance for a, b in zip(expected, actual))

def run_test(test_case):
    try:
        result = subprocess.run(test_case.command.split(), 
                              capture_output=True, 
                              text=True)
        
        if result.stderr:
            return False, f"Error: {result.stderr}"

        actual_values = [float(x.strip()) for x in result.stdout.strip().split(',')]
        
        if compare_outputs(test_case.expected, actual_values):
            return True, None
        else:
            return False, f"Expected: {test_case.expected}\nGot: {actual_values}"
            
    except Exception as e:
        return False, f"Test execution error: {str(e)}"

def main():
    test_cases = [
        TestCase(
            name="Example 1 - Small cache with bin_100",
            cache_size=256,
            assoc=4,
            block_size=1,
            policy="R",
            num_blocks=1,
            input_file="../Enderecos/bin_100.bin",
            expected=[100, 0.92, 0.08, 1.00, 0.00, 0.00]
        ),
        TestCase(
            name="Example 2 - Medium cache with bin_1000",
            cache_size=128,
            assoc=2,
            block_size=4,
            policy="R",
            num_blocks=1,
            input_file="../Enderecos/bin_1000.bin",
            expected=[1000, 0.86, 0.14, 1.00, 0.00, 0.00]
        ),
        TestCase(
            name="Example 3 - Small cache with bin_10000",
            cache_size=16,
            assoc=2,
            block_size=8,
            policy="R",
            num_blocks=1,
            input_file="../Enderecos/bin_10000.bin",
            expected=[10000, 0.93, 0.07, 0.19, 0.81, 0.00]
        ),
        TestCase(
            name="Example 4 - Large cache with vortex",
            cache_size=512,
            assoc=8,
            block_size=2,
            policy="R",
            num_blocks=1,
            input_file="../Enderecos/vortex.in.sem.persons.bin",
            expected=[186676, 0.88, 0.12, 0.05, 0.95, 0.00]
        ),
        TestCase(
            name="Example 5 - Minimal cache with vortex",
            cache_size=1,
            assoc=4,
            block_size=32,
            policy="R",
            num_blocks=1,
            input_file="../Enderecos/vortex.in.sem.persons.bin",
            expected=[186676, 0.54, 0.46, 0.00, 1.00, 0.00]
        ),
        TestCase(
            name="Example 6 - Cache with bin_100",
            cache_size=2,
            assoc=1,
            block_size=8,
            policy="R",
            num_blocks=1,
            input_file="../Enderecos/bin_100.bin",
            expected=[100, 0.43, 0.57, 0.28, 0.68, 0.04]
        ),
        TestCase(
            name="Example 7 - Cache with bin_100",
            cache_size=2,
            assoc=1,
            block_size=8,
            policy="L",
            num_blocks=1,
            input_file="../Enderecos/bin_100.bin",
            expected=[100, 0.46, 0.54, 0.30, 0.67, 0.04]
        ),
        TestCase(
            name="Example 8 - Cache with bin_100",
            cache_size=2,
            assoc=1,
            block_size=8,
            policy="F",
            num_blocks=1,
            input_file="../Enderecos/bin_100.bin",
            expected=[100, 0.43, 0.57, 0.28, 0.68, 0.04]
        ),
        TestCase(
            name="Example 9 - Cache with vortex",
            cache_size=1,
            assoc=4,
            block_size=32,
            policy="R",
            num_blocks=1,
            input_file="../Enderecos/vortex.in.sem.persons.bin",
            expected=[186676, 0.5440, 0.4560, 0.00, 1.00, 0.00]
        ),
        TestCase(
            name="Example 10 - Cache with vortex",
            cache_size=1,
            assoc=4,
            block_size=32,
            policy="L",
            num_blocks=1,
            input_file="../Enderecos/vortex.in.sem.persons.bin",
            expected=[186676, 0.5756, 0.4244, 0.00, 1.00, 0.00]
        ),
        TestCase(
            name="Example 11 - Cache with vortex",
            cache_size=1,
            assoc=4,
            block_size=32,
            policy="F",
            num_blocks=1,
            input_file="../Enderecos/vortex.in.sem.persons.bin",
            expected=[186676, 0.5530, 0.4470, 0.00, 1.00, 0.00]
        )
    ]

    if len(sys.argv) > 1:
        test_number = int(sys.argv[1])
        if 1 <= test_number <= len(test_cases):
            test = test_cases[test_number - 1]
            print(f"\nRunning Test {test_number}: {test.name}")
            print(f"Command: {test.command}")
            
            success, error = run_test(test)
            
            if success:
                print("Status: ✅ PASSED")
            else:
                print("Status: ❌ FAILED")
                print(error)
            
            print(f"\nExecuting additional command: {test.additional_command}")
            subprocess.run(test.additional_command.split())
        else:
            print(f"Invalid test number. Please provide a number between 1 and {len(test_cases)}.")
    else:
        print("Cache Simulator Test Suite")
        print("=" * 50)

        passed = 0
        total = len(test_cases)

        for i, test in enumerate(test_cases, 1):
            print(f"\nTest {i}: {test.name}")
            print(f"Command: {test.command}")
            
            success, error = run_test(test)
            
            if success:
                print("Status: ✅ PASSED")
                passed += 1
            else:
                print("Status: ❌ FAILED")
                print(error)

        print("\n" + "=" * 50)
        print(f"Summary: {passed}/{total} tests passed")

if __name__ == "__main__":
    main()