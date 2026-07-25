import winreg

def collect():
    """Collects security-relevant registry settings and hardware identifiers."""
    data = {}
    try:
        # UAC Check (EnableLUA)
        try:
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
                val, _ = winreg.QueryValueEx(key, "EnableLUA")
                data["uac_enabled"] = bool(val)
        except OSError:
            data["uac_enabled"] = "Unknown"

        # Hardware Identifiers (Commonly spoofed in hardened VMs)
        hw_path = r"HARDWARE\Description\System"
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, hw_path) as key:
                for val_name in ["SystemBiosVersion", "VideoBiosVersion", "SystemProductName", "Identifier"]:
                    try:
                        val, _ = winreg.QueryValueEx(key, val_name)
                        # SystemBiosVersion is often a list of strings
                        if isinstance(val, list):
                            val = " ".join(val)
                        data[val_name] = val
                    except OSError:
                        data[val_name] = "Not Found"
        except OSError:
            pass

        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
