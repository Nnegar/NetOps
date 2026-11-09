from enum import Enum
from dataclasses import dataclass
from ipaddress import ip_address


class DeviceStatus(str,Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    UNKNOWN = "unknown"
    
    
class DeviceRole(str, Enum):
    ROUTER = "router"
    SWITCH = "switch"
    FIREWALL = "firewall"
    

@dataclass(frozen=True)
class Device:
    hostname: str
    mgmt_ip: str
    vendor: str
    role: DeviceRole
    status: DeviceStatus
    
    
    def __post_init__(self):
        if not isinstance(self.hostname, str):
            raise TypeError("Hostname should be a string.")
        
        if not self.hostname.strip():
            raise ValueError("Hostname should not be empty.")
        
        if not isinstance(self.mgmt_ip, str):
            raise TypeError("IP address must be a string.")
        ip_address(self.mgmt_ip)
        
        if not isinstance(self.vendor, str):
            raise TypeError("Vendor should be a string.")
        
        
        if not isinstance(self.role, DeviceRole):
            raise TypeError("Device role is not correct.")
        if not isinstance(self.status, DeviceStatus):
            raise TypeError("Device status is not correct.")
    
    

class Inventory:
    def __init__(self):
        self.devices = {}
        
        
    def add(self, device):
        if not isinstance(device, Device):
            raise TypeError("object is not of type Device.")
        
        key = device.hostname.lower().strip()
        if key in self.devices:
            raise ValueError("Device already exists in the inventory.")
        self.devices[key]=device
        
        
    def get(self, hostname):
        if not isinstance(hostname, str):
            raise TypeError("Hostname should be a string.")
        hostname = hostname.lower().strip()
        if hostname in self.devices:
            return self.devices[hostname]
        return None
    
    
    def remove(self, hostname):
        if not isinstance(hostname,str):
            raise TypeError("Hostname should be a string")
        
        hostname = hostname.lower().strip()
        return self.devices.pop(hostname, None)
    
    def list(self):
        return(list(self.devices.values()))
    
    