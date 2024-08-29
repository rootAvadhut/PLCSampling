import asyncio
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ConnectionException
import socket

# Create a global lock
lock = asyncio.Lock()

# Function to read coils
async def run_modbus_client_coil(ip_address, port_number):
    async with lock:
        try:
            async with AsyncModbusTcpClient(ip_address, port=port_number) as client:
                digital_result = await client.read_coils(0, 10)
                if digital_result.isError():
                    if digital_result.exception_code == 1:
                        print("Illegal function. The function code received in the query is not recognized.")
                    elif digital_result.exception_code == 2:
                        pass  # coils are being read
                    else:
                        print(f"Error reading coils: {digital_result}")
                else:
                    print(f"Coil States: {digital_result.bits}")
        except ConnectionException:
            print("Machine is not connected (while reading coils).")
        except socket.error as e:
            if e.errno == 1225:
                print("Failed to connect: The remote computer refused the network connection.")
            else:
                print(f"Socket error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while reading coils: {e}")

# Function to read input registers
async def run_modbus_client_input_register(ip_address, port_number):
    async with lock:
        try:
            async with AsyncModbusTcpClient(ip_address, port=port_number) as client:
                input_register_result = await client.read_input_registers(0, 10)
                if input_register_result.isError():
                    if input_register_result.exception_code == 1:
                        print("Illegal function. The function code received in the query is not recognized.")
                    elif input_register_result.exception_code == 2:
                        pass  # input registers are being read
                    else:
                        print(f"Error reading input registers: {input_register_result}")
                else:
                    print(f"Input Registers: {input_register_result.registers}")
        except ConnectionException:
            print("Machine is not connected (while reading input registers).")
        except socket.error as e:
            if e.errno == 1225:
                print("Failed to connect: The remote computer refused the network connection.")
            else:
                print(f"Socket error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while reading input registers: {e}")

# Function to read input status
async def run_modbus_client_input_status(ip_address, port_number):
    async with lock:
        try:
            async with AsyncModbusTcpClient(ip_address, port=port_number) as client:
                input_status_result = await client.read_discrete_inputs(0, 10)
                if input_status_result.isError():
                    if input_status_result.exception_code == 1:
                        print("Illegal function. The function code received in the query is not recognized.")
                    elif input_status_result.exception_code == 2:
                        pass  # input status is being read
                    else:
                        print(f"Error reading input status: {input_status_result}")
                else:
                    print(f"Input Status: {input_status_result.bits}")
        except ConnectionException:
            print("Machine is not connected (while reading input status).")
        except socket.error as e:
            if e.errno == 1225:
                print("Failed to connect: The remote computer refused the network connection.")
            else:
                print(f"Socket error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while reading input status: {e}")

# Main function to start the Modbus client
async def main(ip_address, port_number, sampling_frequency):
    while True:
        await run_modbus_client_coil(ip_address, port_number)
        await run_modbus_client_input_register(ip_address, port_number)
        await run_modbus_client_input_status(ip_address, port_number)
        await asyncio.sleep(sampling_frequency)  # Use the user-defined or default sampling frequency

# Function to run the Modbus client
def run_client(ip_address, port_number, sampling_frequency):
    asyncio.run(main(ip_address, port_number, sampling_frequency))
