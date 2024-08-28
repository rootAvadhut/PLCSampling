import asyncio
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ConnectionException

async def run_modbus_client():
    try:
        async with AsyncModbusTcpClient('192.168.1.9', port=502) as client:
            # result = await client.read_holding_registers(0, 10)
            result = await client.read_coils(0, 10)
            if result.isError():
                print(f"Error reading registers: {result}")
            else:
                print(f"Registers: {result.bits}")
                print(f"Registers: {result.registers}")
    except ConnectionException as e:
        print(f"Failed to connect: {e}")

asyncio.run(run_modbus_client())

