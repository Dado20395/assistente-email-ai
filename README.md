# 🤖 Assistente Email Esperto v2.0

Un'applicazione web avanzata costruita con Streamlit e l'API di Google Gemini per generare, perfezionare e personalizzare email complesse in modo rapido e intuitivo. Questo progetto dimostra l'integrazione di un'AI in un'interfaccia utente reattiva, con memoria di sessione e capacità conversazionali.

## 📸 Screenshot



## 🚀 Funzionalità Principali

- **Doppia Modalità di Input:**
    - **Conversazionale:** L'utente descrive l'email richiesta in linguaggio naturale.
    - **Dettagliata:** Un'interfaccia con controlli granulari per ogni aspetto dell'email (tono, lunghezza, lingua, firma).
- **Template Pre-impostati:** Modelli per le email più comuni (es. Follow-up, sollecito) che pre-compilano l'interfaccia per velocizzare il lavoro.
- **Perfezionamento Iterativo:** Pulsanti interattivi per modificare la bozza generata, chiedendo all'AI di renderla più concisa, più formale o più amichevole.
- **Memoria di Sessione:** L'app ricorda le impostazioni dell'utente durante la sessione di lavoro grazie all'uso di `st.session_state`.

## 🛠️ Tecnologie Utilizzate

- **Linguaggio:** Python
- **Framework Web:** Streamlit
- **Modello AI:** Google Gemini (API)
- **Librerie Principali:** `google-generativeai`, `streamlit`

## ⚙️ Come Avviare il Progetto

1.  Clonare il repository: `git clone https://github.com/Dado20395/assistente-email-ai`
2.  Navigare nella cartella del progetto.
3.  Installare le dipendenze: `pip install streamlit google-generativeai`
4.  Impostare la variabile d'ambiente `GOOGLE_API_KEY` con la propria chiave API di Google.
5.  Lanciare l'app: `streamlit run Progetto.py`
