setlocal
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m streamlit run app.py
endlocal