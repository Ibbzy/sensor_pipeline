import uuid
from datetime import datetime, UTC

# Utility function to generate unique filenames
def generate_filename(prefix, extension):
    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]  # Shortened UUID for simplicity
    return f"{prefix}_{timestamp}_{unique_id}.{extension}"