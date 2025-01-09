# solagos

python3 -m venv solagos
source solagos/bin/activate
pip freeze > requirements.txt

pip install -r requirements.txt
deactivate

pip install streamlit
pip install pandas

streamlit run app.py