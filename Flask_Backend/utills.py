import re
import os


def uploadTrainingFilesUtil(files, loadDataPath, weatherDataPath, holidaysDataPath):
    for file in files:
        safe_filename = re.sub(r'[\\/:"*?<>|]+', '_', file.filename)

        if 'Load' in safe_filename:
            file.save(os.path.join(loadDataPath, safe_filename))
        elif 'Weather' in safe_filename:
            file.save(os.path.join(weatherDataPath, safe_filename))
        elif 'Holidays' in safe_filename:
            file.save(os.path.join(holidaysDataPath, safe_filename))

    return {"num_received_files": len(files)}