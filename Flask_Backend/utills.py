import re
import os


def upload_training_files_util(files, load_data_path, weather_data_path, holidays_data_path):
    for file in files:
        safe_filename = re.sub(r'[\\/:"*?<>|]+', '_', file.filename)

        if 'Load' in safe_filename:
            file.save(os.path.join(load_data_path, safe_filename))
        elif 'Weather' in safe_filename:
            file.save(os.path.join(weather_data_path, safe_filename))
        elif 'Holidays' in safe_filename:
            file.save(os.path.join(holidays_data_path, safe_filename))

    return {"num_received_files": len(files)}