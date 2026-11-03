from netops.models import Device, DeviceRole, DeviceStatus, Inventory
import pytest


#devices
r1 = Device(
    hostname="R1",
    mgmt_ip="192.168.1.1",
    vendor="Cisco",
    role=DeviceRole.ROUTER,
    status=DeviceStatus.ONLINE
)

sw1 = Device(
    hostname="SW1",
    mgmt_ip="192.168.1.2",
    vendor="Juniper",
    role=DeviceRole.SWITCH,
    status=DeviceStatus.OFFLINE
)

fw1 = Device(
    hostname="FW1",
    mgmt_ip="192.168.1.3",
    vendor="Fortinet",
    role=DeviceRole.FIREWALL,
    status=DeviceStatus.UNKNOWN
)


r2 = Device(
    hostname="R1",
    mgmt_ip="192.168.1.1",
    vendor="Cisco",
    role=DeviceRole.ROUTER,
    status=DeviceStatus.ONLINE
)


def test_valid_device():
    assert r2.hostname == "R1"
    assert r2.mgmt_ip == "192.168.1.1"
    assert fw1.status == "unknown"
    assert sw1.role == "switch"
    
    with pytest.raises(ValueError):
        Device(
            hostname="",
            mgmt_ip="192.168.1.2",
            vendor="Cisco",
            role=DeviceRole.ROUTER,
            status=DeviceStatus.ONLINE)
        
        
        
        
    
        
    

def test_invalid_ip():
    with pytest.raises(TypeError):
        Device(
            hostname="R3",
            mgmt_ip=123,
            vendor="Cisco",
            role=DeviceRole.ROUTER,
            status=DeviceStatus.ONLINE
        )
           
    with pytest.raises(ValueError):
        Device(
            hostname="R4",
            mgmt_ip="192.468.1.1",
            vendor="Cisco",
            role=DeviceRole.ROUTER,
            status=DeviceStatus.ONLINE
        )
        
    with pytest.raises(ValueError):
        Device(
            hostname="R5",
            mgmt_ip="192.168.1.",
            vendor="Cisco",
            role=DeviceRole.ROUTER,
            status=DeviceStatus.ONLINE
        )
                
        
    

def test_inventory():
    inventory = Inventory()
    inventory.add(r1)
    
    assert inventory.get("r1") is r1
    
    with pytest.raises(ValueError):
        inventory.add(R1)
        
    
    
    