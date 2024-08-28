import asyncio
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ConnectionException
import socket

# Create a global lock
lock = asyncio.Lock()

async def run_modbus_client_coil():
    async with lock:  # Acquire the lock before running this coroutine
        try:
            # Connect to the Modbus TCP server at 192.168.1.9 on port 502
            async with AsyncModbusTcpClient('192.168.1.9', port=502) as client:
                # Example: Reading 20 coils starting from address 1000 (adjust this to your valid range)
                digital_result = await client.read_coils(0, 10)
                if digital_result.isError():
                    print(f"Error reading digital states: {digital_result}")
                else:
                    print(f"Digital States: {digital_result.bits}")
        except ConnectionException:
            print("Machine is not connected (while reading coils).")
        except socket.error as e:
            if e.errno == 1225:  # WinError 1225: The remote computer refused the network connection
                print("Failed to connect: The remote computer refused the network connection.")
            else:
                print(f"Socket error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while reading coils: {e}")

async def run_modbus_client_holding_register():
    async with lock:  # Acquire the lock before running this coroutine
        try:
            # Connect to the Modbus TCP server at 192.168.1.9 on port 502
            async with AsyncModbusTcpClient('192.168.1.9', port=502) as client:
                # Example: Reading 20 holding registers starting from address 40001 (adjust this to your valid range)
                analog_result = await client.read_holding_registers(0, 10)
                if analog_result.isError():
                    print(f"Error reading holding registers: {analog_result}")
                else:
                    print(f"Analog Inputs: {analog_result.registers}")
        except ConnectionException:
            print("Machine is not connected (while reading holding registers).")
        except socket.error as e:
            if e.errno == 1225:  # WinError 1225: The remote computer refused the network connection
                print("Failed to connect: The remote computer refused the network connection.")
            else:
                print(f"Socket error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while reading holding registers: {e}")

async def main():
    while True:
        await run_modbus_client_coil()
        await run_modbus_client_holding_register()
        await asyncio.sleep(1)  # Add a delay between reads to avoid overloading the server

# Run the main loop
asyncio.run(main())
