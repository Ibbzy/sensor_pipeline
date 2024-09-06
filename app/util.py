import uuid
from datetime import datetime, timezone


# Utility function to generate unique filenames
def generate_filename(sensor_type: str, extension: str) -> str:
    """Generate a unique filename based on the sensor type, timestamp, and UUID."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]  # Shortened UUID for simplicity
    return f"{sensor_type}_{timestamp}_{unique_id}.{extension}"


def get_partitioned_path(sensor_type: str, filename: str) -> str:
    """Generate a partitioned path based on current date and sensor type."""
    now = datetime.now(timezone.utc)
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    return f"{sensor_type}/{year}/{month}/{day}/{filename}"
