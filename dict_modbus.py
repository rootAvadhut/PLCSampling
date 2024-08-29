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
                # Example: Reading 10 coils starting from address 0 (adjust this to your valid range)
                digital_result = await client.read_coils(0, 10)
                if digital_result.isError():
                    if digital_result.exception_code == 1:
                        print("Illegal function. The function code received in the query is not recognized.")
                    elif digital_result.exception_code == 2:
                        pass  # Modify this block to handle specific errors as needed
                    else:
                        print(f"Error reading digital states: {digital_result}")
                else:
                    coil_dict = {f"{address + 1:05}": state for address, state in enumerate(digital_result.bits, start=0)}
                    print(f"Coil States: {coil_dict}")
                    return coil_dict
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
                # Example: Reading 10 holding registers starting from address 0 (adjust this to your valid range)
                analog_result = await client.read_holding_registers(0, 10)
                if analog_result.isError():
                    if analog_result.exception_code == 1:
                        print("Illegal function. The function code received in the query is not recognized.")
                    elif analog_result.exception_code == 2:
                        pass  # Modify this block to handle specific errors as needed
                    else:
                        print(f"Error reading holding registers: {analog_result}")
                else:
                    register_dict = {f"{address + 40001}": value for address, value in enumerate(analog_result.registers, start=0)}
                    print(f"Holding Register Values: {register_dict}")
                    return register_dict
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
        coil_states = await run_modbus_client_coil()
        holding_register_values = await run_modbus_client_holding_register()
        await asyncio.sleep(1)  # Add a delay between reads to avoid overloading the server

# Run the main loop
asyncio.run(main())

#output:
# Holding Register Values: {'40001': 0, '40002': 0, '40003': 0, '40004': 0, '40005': 0, '40006': 0, '40007': 0, '40008': 0, '40009': 0, '40010': 0}
# Coil States: {'00001': False, '00002': False, '00003': False, '00004': False, '00005': False, '00006': False, '00007': False, '00008': False, '00009': False, '00010': False, '00011': False, '00012': False, '00013': False, '00014': False, '00015': False, '00016': False}