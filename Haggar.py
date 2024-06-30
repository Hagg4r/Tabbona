import subprocess
import sys
import pkg_resources
from subprocess import CalledProcessError

def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except CalledProcessError:
        print(f"Failed to install {package}")

def check_and_install_python_packages():
    required_packages = ['ping3']
    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    for package in required_packages:
        if package not in installed_packages:
            print(f"Installing Python package: {package}")
            install_package(package)

def check_command(command):
    try:
        subprocess.run([command, '--version'], capture_output=True, text=True, check=True)
    except CalledProcessError:
        return False
    return True

def install_system_package(package_name, install_command):
    if not check_command(package_name):
        print(f"{package_name} not found. Installing...")
        try:
            subprocess.check_call(install_command, shell=True)
        except CalledProcessError:
            print(f"Failed to install {package_name}. Please install it manually.")

def check_and_install_system_packages():
    system_packages = {
        'nikto': 'sudo apt-get install -y nikto',
        'sqlmap': 'sudo apt-get install -y sqlmap',
        'uniscan': 'sudo apt-get install -y uniscan',
        'nmap': 'sudo apt-get install -y nmap'
    }
    for package, install_cmd in system_packages.items():
        install_system_package(package, install_cmd)

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

def scan_target(target):
    print(f"Scanning target: {target}")
    
    # Run nikto scan
    print("Running nikto scan...")
    nikto_result = run_command(["nikto", "-h", target])
    print(nikto_result)
    
    # Run sqlmap scan
    print("Running sqlmap scan...")
    sqlmap_result = run_command(["sqlmap", "-u", target, "--batch"])
    print(sqlmap_result)
    
    # Run uniscan scan
    print("Running uniscan scan...")
    uniscan_result = run_command(["uniscan", "-u", target, "-qweds"])
    print(uniscan_result)
    
    # Run nmap scan
    print("Running nmap scan...")
    nmap_result = run_command(["nmap", "-sV", "-O", target])
    print(nmap_result)
    
    # Run ping3
    print("Running ping3...")
    ping_result = run_command(["ping3", target])
    print(ping_result)

if __name__ == "__main__":
    check_and_install_python_packages()
    check_and_install_system_packages()
    
    if len(sys.argv) != 2:
        print("Usage: python script.py <target>")
        sys.exit(1)
    
    target = sys.argv[1]
    scan_target(target)
