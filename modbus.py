import asyncio
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ConnectionException
import socket

# Global flag to track the connection status
connected = False

async def check_connection(client):
    global connected
    try:
        result = await client.read_coils(0, 1)
        if result.isError():
            connected = False
            return False
        connected = True
        return True
    except (ConnectionException, socket.error):
        connected = False
        return False
    except Exception as e:
        print(f"An unexpected error occurred during the connection check: {e}")
        connected = False
        return False

async def run_modbus_client_coil(client):
    try:
        digital_result = await client.read_coils(0, 15)
        if digital_result.isError():
            return None
        else:
            return digital_result.bits
    except Exception as e:
        return None

async def run_modbus_client_input_register(client):
    try:
        input_register_result = await client.read_input_registers(0, 7)
        if input_register_result.isError():
            return None
        else:
            return input_register_result.registers
    except Exception as e:
        return None

async def run_modbus_client_input_status(client):
    try:
        input_status_result = await client.read_discrete_inputs(0, 15)
        if input_status_result.isError():
            return None
        else:
            return input_status_result.bits
    except Exception as e:
        return None

async def modbus_client_loop(ip_address, port, sampling_frequency, update_ui_callback):
    global connected
    async with AsyncModbusTcpClient(ip_address, port=port) as client:
        while True:
            if not connected:
                if await check_connection(client):
                    print("Machine connected. Starting data retrieval...")
                else:
                    await asyncio.sleep(sampling_frequency)
                    continue

            # Get the data
            coil_states = await run_modbus_client_coil(client)
            input_registers = await run_modbus_client_input_register(client)
            input_statuses = await run_modbus_client_input_status(client)

            # Update the UI
            update_ui_callback(coil_states, input_registers, input_statuses)

            await asyncio.sleep(sampling_frequency)

def run_client(ip_address, port, sampling_frequency, update_ui_callback):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(modbus_client_loop(ip_address, port, sampling_frequency, update_ui_callback))
    loop.close()



# import asyncio
# from pymodbus.client import AsyncModbusTcpClient
# from pymodbus.exceptions import ConnectionException
# import socket

# # Global flag to track the connection status
# connected = False

# # Function to attempt connection to the PLC
# async def check_connection(client):
#     global connected
#     try:
#         # Attempt to read a small range of coils to check the connection
#         result = await client.read_coils(0, 1)
#         if result.isError():
#             connected = False
#             return False
#         connected = True
#         return True
#     except (ConnectionException, socket.error):
#         connected = False
#         return False
#     except Exception as e:
#         print(f"An unexpected error occurred during the connection check: {e}")
#         connected = False
#         return False

# # Function to read coils
# async def run_modbus_client_coil(client):
#     try:
#         digital_result = await client.read_coils(0, 15)
#         if digital_result.isError():
#             if digital_result.exception_code == 1:  # Handle Illegal Address
#                 return  # Suppress IllegalAddress error
#             return  # Suppress other errors silently
#         else:
#             print(f"Coil States: {digital_result.bits}")
#     except Exception as e:
#         return  # Suppress any unexpected errors while reading coils

# # Function to read input registers
# async def run_modbus_client_input_register(client):
#     try:
#         input_register_result = await client.read_input_registers(0, 7)
#         if input_register_result.isError():
#             return  # Suppress errors silently
#         else:
#             print(f"Input Registers: {input_register_result.registers}")
#     except Exception as e:
#         return  # Suppress any unexpected errors while reading input registers

# # Function to read input status
# async def run_modbus_client_input_status(client):
#     try:
#         input_status_result = await client.read_discrete_inputs(0, 15)
#         if input_status_result.isError():
#             return  # Suppress errors silently
#         else:
#             print(f"Input Status: {input_status_result.bits}")
#     except Exception as e:
#         return  # Suppress any unexpected errors while reading input status

# async def modbus_client_loop(ip_address, port, sampling_frequency):
#     global connected
#     async with AsyncModbusTcpClient(ip_address, port=port) as client:
#         while True:
#             # Check if the PLC is connected
#             if not connected:
#                 print("Checking connection to PLC...")
#                 if await check_connection(client):
#                     print("Machine connected. Starting data retrieval...")
#                 else:
#                     print("Machine is not connected. Retrying in a moment...")
#                     await asyncio.sleep(sampling_frequency)
#                     continue

#             # If connected, read the data
#             await run_modbus_client_coil(client)
#             await run_modbus_client_input_register(client)
#             await run_modbus_client_input_status(client)
#             await asyncio.sleep(sampling_frequency)

# def run_client(ip_address, port, sampling_frequency):
#     loop = asyncio.new_event_loop()  # Create a new event loop
#     asyncio.set_event_loop(loop)  # Set the event loop for this thread
#     loop.run_until_complete(modbus_client_loop(ip_address, port, sampling_frequency))
#     loop.close()  # Close the loop when done

