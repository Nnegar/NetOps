from netops.models import Device, DeviceRole, DeviceStatus, Inventory
import pytest
from dataclasses import asdict, FrozenInstanceError
import re




@pytest.fixture
def router():
    return Device(
            hostname="R1",
            mgmt_ip="192.168.1.1",
            vendor="Cisco",
            role=DeviceRole.ROUTER,
            status=DeviceStatus.ONLINE
        )
    
@pytest.fixture
def switch():
       return Device(
            hostname="S1",
            mgmt_ip="192.168.1.2",
            vendor="Nokia",
            role=DeviceRole.SWITCH,
            status=DeviceStatus.OFFLINE
        ) 

@pytest.fixture
def inventory():
    return Inventory()


def test_router_creation(router):
    assert router.hostname == "R1"
    assert router.mgmt_ip == "192.168.1.1"
    assert router.role == DeviceRole.ROUTER
        
        
def test_inventory_starts_empty(inventory):
    assert inventory.list() == []
    
   
@pytest.mark.parametrize("field, invalid_value, expected_error", [
   ("hostname", "", ValueError),
   ("hostname", None, TypeError),
   ("mgmt_ip", "999.1.1.1", ValueError),
   ("mgmt_ip", 123, TypeError),
   ("role", "router", TypeError),
   ("status", "online", TypeError),
   ("vendor", 564,TypeError )
])
def test_invalid_device_inputs(router, field, invalid_value, expected_error):
    data = asdict(router)
    data[field] = invalid_value
    
    with pytest.raises(expected_error):
        Device(**data)
    
    
    
@pytest.mark.parametrize("field, invalid_value, expected_error, message",[
    ("role", "switch", TypeError, "Device role is not correct."),
    ("hostname", 123,  TypeError, "Hostname should be a string.")
])
def test_error_messages(router, field, invalid_value, expected_error, message):
    data = asdict(router)
    data[field] = invalid_value
    
    with pytest.raises(expected_error, match=f"^{re.escape(message)}$"):
        Device(**data)
    
    
def test_hostname_change_after_add(router, inventory):
    inventory.add(router)
    with pytest.raises(FrozenInstanceError):
        router.hostname = "R2"
        
        
        
def test_inventory_add(router, switch, inventory):
    inventory.add(router)
    assert len(inventory.list()) == 1
    
    inventory.add(switch)
    assert len(inventory.list()) == 2
    
    with pytest.raises(ValueError, match ="Device already exists in the inventory."):
        inventory.add(router)
    
    not_device = asdict(switch)    
    with pytest.raises(TypeError, match="object is not of type Device"):
        inventory.add(not_device)
        
        
def test_inventory_get(router,inventory):
    assert inventory.list() == []
    
    inventory.add(router)
    assert inventory.get("R1") is router
    assert inventory.get("r1") is router
    assert inventory.get("S1") is None
    
    with pytest.raises(TypeError, match="Hostname should be a string."):
        inventory.get(1)
        
        
def test_inventory_remove(router,switch,inventory):
    inventory.add(router)
    inventory.add(switch)
    assert inventory.remove("R1") is router
    assert inventory.remove("s1") is switch
    assert inventory.list() == []
    assert inventory.remove("R1") is None
    with pytest.raises(TypeError, match="Hostname should be a string"):
        inventory.remove(1)
        
        
def test_inventory_hostname_withspace(inventory):
    router_with_space = Device(
            hostname=" R1 ",
            mgmt_ip="192.168.1.1",
            vendor="Cisco",
            role=DeviceRole.ROUTER,
            status=DeviceStatus.ONLINE    
    )
    
    inventory.add(router_with_space)
    assert inventory.get(" R1 ") is router_with_space
    assert inventory.get("R1") is router_with_space