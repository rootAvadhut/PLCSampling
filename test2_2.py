import asyncio
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ConnectionException
import socket

# Create a global lock
lock = asyncio.Lock()

# Variables to store the latest values
coil_states = None
input_registers = None
input_status = None

# Function to read coils
async def run_modbus_client_coil():
    global coil_states
    async with lock:
        try:
            async with AsyncModbusTcpClient('192.168.1.9', port=502) as client:
                digital_result = await client.read_coils(0, 10)
                if not digital_result.isError():
                    coil_states = digital_result.bits
        except ConnectionException:
            coil_states = None  # Set to None if the machine is not connected
        except socket.error as e:
            coil_states = None  # Set to None on socket error
        except Exception as e:
            coil_states = None  # Set to None on any other error

# Function to read input registers
async def run_modbus_client_input_register():
    global input_registers
    async with lock:
        try:
            async with AsyncModbusTcpClient('192.168.1.9', port=502) as client:
                input_register_result = await client.read_input_registers(0, 10)
                if not input_register_result.isError():
                    input_registers = input_register_result.registers
        except ConnectionException:
            input_registers = None  # Set to None if the machine is not connected
        except socket.error as e:
            input_registers = None  # Set to None on socket error
        except Exception as e:
            input_registers = None  # Set to None on any other error

# Function to read input status
async def run_modbus_client_input_status():
    global input_status
    async with lock:
        try:
            async with AsyncModbusTcpClient('192.168.1.9', port=502) as client:
                input_status_result = await client.read_discrete_inputs(0, 10)
                if not input_status_result.isError():
                    input_status = input_status_result.bits
        except ConnectionException:
            input_status = None  # Set to None if the machine is not connected
        except socket.error as e:
            input_status = None  # Set to None on socket error
        except Exception as e:
            input_status = None  # Set to None on any other error

# Getter functions to access the latest values
def get_coil_states():
    return coil_states

def get_input_registers():
    return input_registers

def get_input_status():
    return input_status

async def main():
    while True:
        await run_modbus_client_coil()
        await run_modbus_client_input_register()
        await run_modbus_client_input_status()
        await asyncio.sleep(1)
   

# Run the main loop
asyncio.run(main())

# Example usage of getter functions
coil_states_value = get_coil_states()
input_registers_value = get_input_registers()
input_status_value = get_input_status()

# Now you can use these values in your code as needed
