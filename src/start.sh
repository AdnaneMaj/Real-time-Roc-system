#!/bin/bash

#insert data inside the mongodb
python src/data/static/insert_data.py

# Run app.py in the foreground
streamlit run src/dashboard/app.py --server.port=8501 --server.address=0.0.0.0