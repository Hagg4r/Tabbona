import subprocess
import sys

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
    if len(sys.argv) != 2:
        print("Usage: python script.py <target>")
        sys.exit(1)
    
    target = sys.argv[1]
    scan_target(target)
