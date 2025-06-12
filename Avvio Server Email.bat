@echo off
TITLE DI

echo Avvio del server per l'Assistente Email AI in corso...
echo.
echo QUESTA FINESTRA DEVE RIMANERE APERTA (puoi ridurla a icona).
echo Chiudila solo quando hai finito di usare l'app.
echo.

cd C:\Users\david\OneDrive\Desktop\Progetto_API

rem 
"C:\Users\david\AppData\Local\Programs\Python\Python313\Scripts\streamlit.exe" run Progetto.py --server.headless=true
pause