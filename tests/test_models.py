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