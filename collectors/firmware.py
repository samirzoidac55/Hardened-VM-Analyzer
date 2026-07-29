import ctypes
from ctypes import wintypes
import struct

# Constants
ACPI_SIGNATURE = struct.unpack('<I', b'ACPI')[0]
RSMB_SIGNATURE = struct.unpack('<I', b'RSMB')[0]

def get_firmware_table(provider_signature, table_id=0):
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    
    # First call to get required buffer size
    size = kernel32.GetSystemFirmwareTable(provider_signature, table_id, None, 0)
    if size == 0:
        return None
        
    buffer = ctypes.create_string_buffer(size)
    result = kernel32.GetSystemFirmwareTable(provider_signature, table_id, buffer, size)
    
    if result == 0:
        return None
        
    return buffer.raw

def collect():
    """Collects low-level firmware table data."""
    data = {
        "acpi_raw": None,
        "smbios_raw": None
    }
    
    try:
        # Get raw ACPI table
        acpi = get_firmware_table(ACPI_SIGNATURE)
        if acpi:
            data["acpi_raw"] = acpi.hex()[:100]  # Store hex snippet to keep data size manageable
            
        # Get raw SMBIOS table
        smbios = get_firmware_table(RSMB_SIGNATURE)
        if smbios:
            data["smbios_raw"] = smbios.hex()[:100]
            
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
