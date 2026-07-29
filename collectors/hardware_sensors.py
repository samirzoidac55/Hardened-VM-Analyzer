import subprocess
import json

def collect():
    """Queries hardware sensor data via WMI/CIM."""
    sensors = {
        "thermal_zones": [],
        "fan_data": []
    }
    
    try:
        # Check thermal zones
        cmd_thermal = "powershell -Command \"Get-CimInstance -Namespace root/wmi -ClassName MSAcpi_ThermalZoneTemperature | Select-Object -Property CurrentTemperature | ConvertTo-Json\""
        result_thermal = subprocess.run(cmd_thermal, capture_output=True, text=True, shell=True, encoding='utf-8', errors='replace')
        if result_thermal.returncode == 0 and result_thermal.stdout.strip():
            sensors["thermal_zones"] = json.loads(result_thermal.stdout)
            
        # Check fans (if applicable)
        cmd_fans = "powershell -Command \"Get-CimInstance -ClassName Win32_Fan | Select-Object -Property Name, Status | ConvertTo-Json\""
        result_fans = subprocess.run(cmd_fans, capture_output=True, text=True, shell=True, encoding='utf-8', errors='replace')
        if result_fans.returncode == 0 and result_fans.stdout.strip():
            sensors["fan_data"] = json.loads(result_fans.stdout)
            
        return {"status": "success", "data": sensors}
    except Exception as e:
        return {"status": "error", "message": str(e)}
