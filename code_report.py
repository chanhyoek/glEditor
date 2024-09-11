import subprocess
import locale

def run_command(command):
    """Execute a shell command and return its output."""
    # 시스템의 기본 인코딩 가져오기
    encoding = locale.getpreferredencoding()

    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode(encoding)
    except subprocess.CalledProcessError as e:
        print(f"Error executing {command}: {e.stderr.decode(encoding)}")
        return ""

def run_prospector(target):
    """Run Prospector to analyze the code quality."""
    print("Running Prospector...")
    return run_command(f"prospector {target} --output-format text")

def autopep8_fix(target):
    """Automatically format code to follow PEP8 using Autopep8."""
    print("Running autopep8 to fix style issues...")
    return run_command(f"autopep8 --in-place --aggressive --aggressive {target}")

def pylint_analysis(target):
    """Run Pylint analysis to find code issues."""
    print("Running Pylint...")
    return run_command(f"pylint {target}")

def rope_refactor(target):
    """Perform code refactoring using Rope."""
    print("Rope does not have a simple command-line interface and is usually used within an editor.")
    pass

def main():
    # Define target directory or file for analysis
    target = 'C:/Users/cpark136/Desktop/TAXDA/TDAProject/glEditor/' # Replace with your project directory

    # Run Prospector analysis
    prospector_report = run_prospector(target)
    
    # Save the Prospector report to a file
    with open('prospector_report.txt', 'w') as report_file:
        report_file.write(prospector_report)
    print("Prospector analysis report saved to 'prospector_report.txt'.")

    # Automatically fix code style issues with Autopep8
    autopep8_fix(target)
    print("Code style issues fixed using Autopep8.")

    # Run Pylint after Autopep8 fixes
    pylint_report = pylint_analysis(target)
    
    # Save the Pylint report to a file
    with open('pylint_report.txt', 'w') as report_file:
        report_file.write(pylint_report)
    print("Pylint analysis report saved to 'pylint_report.txt'.")

    # Additional refactoring using Rope (if needed)
    rope_refactor(target)
    print("Code refactoring completed (if any).")

if __name__ == "__main__":
    main()
