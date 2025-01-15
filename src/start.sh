#!/bin/bash
# Run fetch_data.py in the background
python src/api/fetch_data.py &

# Run app.py in the foreground
python src/dashboard/app.py