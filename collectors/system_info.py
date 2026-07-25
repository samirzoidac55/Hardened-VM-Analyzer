import platform
import subprocess
import json

def collect():
    """Collects basic and deep system information."""
    try:
        data = {
            "os": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "architecture": platform.machine(),
            "hostname": platform.node(),
        }
        # Attempt deeper info via PowerShell
        try:
            cmd = "powershell -Command \"Get-ComputerInfo | Select-Object -Property OsName, OsVersion, OsBuildNumber | ConvertTo-Json\""
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True, encoding='utf-8', errors='replace')
            if result.returncode == 0:
                ps_info = json.loads(result.stdout)
                data.update(ps_info)
        except Exception:
            # Fallback if PS is restricted
            pass

        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
