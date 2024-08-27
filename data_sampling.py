import time
from datetime import datetime
from file_operations import log_change_to_file

def validate_sampling_time(sampling_entry):
    """Validate and return the sampling time from the input."""
    try:
        sampling_time = float(sampling_entry.get())
        if sampling_time < 0.1 or sampling_time > 60000:
            raise ValueError
        return sampling_time
    except ValueError:
        raise ValueError("Sampling time must be between 0.1 seconds and 1 minute.")

def get_sampled_data():
    """Simulate data sampling. Replace this with real logic."""
    return {"value": 10}  # Placeholder value

def has_significant_change(new_data, change_threshold):
    """Check if there has been a significant change in data."""
    # Simulate checking for changes in data (replace with actual comparison logic)
    return True  # Placeholder, assume change detected

def sample_data(sampling_entry, change_entry, file_entry):
    """Sample data, check for changes, and log them if necessary."""
    try:
        sampling_time = validate_sampling_time(sampling_entry)
    except ValueError as e:
        return
    
    sampled_data = get_sampled_data()

    if has_significant_change(sampled_data, float(change_entry.get())):
        log_change_to_file(sampled_data, file_entry.get())
    
    # Schedule the next sampling event
    time.sleep(sampling_time)
    sample_data(sampling_entry, change_entry, file_entry)
