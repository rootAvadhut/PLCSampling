import asyncio
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ConnectionException

async def run_modbus_client():
    try:
        # Connect to the Modbus TCP server at 192.168.1.110 on port 502
        async with AsyncModbusTcpClient('192.168.1.9', port=502) as client:
            # Reading 20 coils starting from address 0001
            digital_result = await client.read_coils(0, 20)
            if digital_result.isError():
                print(f"Error reading digital states: {digital_result}")
            else:
                print(f"Digital States: {digital_result.bits}")

            # Reading 20 holding registers starting from address 40001 (address 0 in the code)
            analog_result = await client.read_holding_registers(0, 20)
            if analog_result.isError():
                print(f"Error reading analog inputs: {analog_result}")
            else:
                print(f"Analog Inputs: {analog_result.registers}")

    except ConnectionException as e:
        print(f"Failed to connect: {e}")

asyncio.run(run_modbus_client())

