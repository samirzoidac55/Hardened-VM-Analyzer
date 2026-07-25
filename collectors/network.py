import subprocess
import json

def collect():
    """Collects network interface information including MAC addresses."""
    try:
        cmd = "powershell -Command \"Get-NetAdapter | Select-Object -Property Name, InterfaceDescription, MacAddress, Status | ConvertTo-Json\""
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True, encoding='utf-8', errors='replace')
        if result.returncode == 0:
            adapters = json.loads(result.stdout)
            # Ensure output is a list even if only one adapter is found
            if isinstance(adapters, dict):
                adapters = [adapters]
            return {"status": "success", "data": {"adapters": adapters}}
        return {"status": "error", "message": "Failed to collect network adapters"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
