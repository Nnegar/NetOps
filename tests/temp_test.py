from netops.models import Device, DeviceRole, DeviceStatus, Inventory

r1 = Device(
    hostname="R1",
    mgmt_ip="192.168.1.1",
    vendor="Cisco",
    role=DeviceRole.ROUTER,
    status=DeviceStatus.ONLINE
)


inventory = Inventory()
inventory.add(r1)
print(inventory.get("r2"))  # Cisco Router
