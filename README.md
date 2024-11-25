# solagos

python3 -m venv solagos
source solagos/bin/activate
pip freeze > requirements.txt
deactivate

pip install streamlit
pip install pandas