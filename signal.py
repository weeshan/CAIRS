import asyncio
from bleak import BleakScanner

TARGET_COMPANY_ID = 0xFFFF
TARGET_DATA = b'\x01\x02\x03\x04'   # from your screenshot

async def main():
    print("Scanning...")
    devices = await BleakScanner.discover(timeout=10.0, return_adv=True)

    found = False

    for device, adv in devices.values():
        mdata = adv.manufacturer_data or {}

        if TARGET_COMPANY_ID in mdata:
            if mdata[TARGET_COMPANY_ID] == TARGET_DATA:
                print("\n🎯 Found WEESH!!")
                print("--------------------------")
                print(f"Address: {device.address}")
                print(f"Name: {device.name}")
                print(f"RSSI: {adv.rssi}")
                print(f"Manufacturer data: {mdata}")
                found = True

    if not found:
        print("\n❌ Weesh not found. Try:")
        print(" - Keep phone screen ON")
        print(" - Keep nRF Connect open")
        print(" - Increase timeout to 15 seconds")

asyncio.run(main())
