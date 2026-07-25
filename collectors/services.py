import subprocess
import json

def collect():
    """Collects service names, statuses, and start types using PowerShell."""
    try:
        cmd = "powershell -Command \"Get-Service | Select-Object -Property Name, DisplayName, Status, StartType | ConvertTo-Json\""
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True, encoding='utf-8', errors='replace')
        if result.returncode == 0:
            services = json.loads(result.stdout)
            return {"status": "success", "data": {"services": services}}
        return {"status": "error", "message": "Failed to collect services"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
