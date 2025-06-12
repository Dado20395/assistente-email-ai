# Importiamo le librerie necessarie
import streamlit as st
import google.generativeai as genai
import os

# --- CONFIGURAZIONE PAGINA ---
# MODIFICA 1: Titolo della pagina e icona personalizzati
st.set_page_config(page_title="DI - Assistente Email", page_icon="📧") 

# --- CONFIGURAZIONE API ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") 
genai.configure(api_key=GOOGLE_API_KEY)
# Torniamo al modello Flash per evitare problemi di quota durante gli esperimenti
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# --- LOGICA DEI TEMPLATE (per la modalità dettagliata) ---
templates = {
    "Nessuno": {"tono": "Formale", "obiettivo": "", "punti_chiave": [""]},
    "Follow-up Riunione": {"tono": "Professionale", "obiettivo": "Riassumere i punti discussi e definire i prossimi passi.", "punti_chiave": ["Ringraziamenti per la partecipazione", "Breve riepilogo delle decisioni chiave prese", "Elenco delle azioni assegnate", "Proposta per la data della prossima riunione."]},
    "Richiesta Informazioni": {"tono": "Formale", "obiettivo": "Ottenere informazioni specifiche su un determinato argomento.", "punti_chiave": ["Breve introduzione del contesto", "Domanda specifica", "Richiesta di eventuale documentazione", "Indicazione della scadenza per la risposta."]},
}

def applica_template():
    template_scelto = st.session_state.template_selezionato
    template_valori = templates.get(template_scelto, templates["Nessuno"])
    st.session_state.tono_selezionato = template_valori["tono"]
    st.session_state.obiettivo = template_valori["obiettivo"]
    st.session_state.punti_chiave = list(template_valori["punti_chiave"])

# --- INIZIALIZZAZIONE DELLO STATO DI SESSIONE ---
if 'punti_chiave' not in st.session_state: st.session_state.punti_chiave = [""] 
default_valori = {"destinatario": "", "tono_selezionato": "Formale", "tono_personalizzato": "", "obiettivo": "", "lunghezza": "Media (2 paragrafi)", "lingua": "Italiano", "mio_nome": "", "mio_ruolo": "", "template_selezionato": "Nessuno", "ultima_email": "", "creativita": 0.7}
for key, value in default_valori.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- INTERFACCIA UTENTE (SEMPRE VISIBILE) ---
# MODIFICA 2: Titolo principale dell'app
st.title("DI - Il Tuo Assistente Email")

# --- DEFINIZIONE DELLE SCHEDE (TABS) ---
tab1, tab2 = st.tabs(["Modalità Rapida (Conversazionale)", "Modalità Dettagliata"])

# --- CONTENUTO DELLA SCHEDA 1: MODALITÀ RAPIDA ---
with tab1:
    st.header("Descrivi l'email che ti serve")
    st.write("Scrivi la tua richiesta in linguaggio naturale. L'AI capirà il contesto e genererà l'email per te.")
    st.text_area("La tua richiesta:", key="richiesta_rapida", height=150, placeholder="Es: Scrivi un'email formale al prof. Rossi per chiedere quando posso riavere il mio CV che ho consegnato l'11 giugno. Firmati come Davide Izzo, AI Specialist.")
    if st.button("Genera da Richiesta Rapida", type="primary"):
        if not st.session_state.richiesta_rapida:
            st.warning("Per favore, inserisci una richiesta.")
        else:
            with st.spinner("L'AI sta interpretando la tua richiesta e scrivendo l'email..."):
                conversational_prompt = f"""
                Agisci come un assistente personale ultra-efficiente. Il tuo compito è interpretare la richiesta dell'utente scritta in linguaggio naturale e generare un'email professionale e completa.
                RICHIESTA DELL'UTENTE:
                "{st.session_state.richiesta_rapida}"
                Tuo compito:
                1. Analizza la richiesta per identificare il destinatario, il tono implicito (se non specificato, usa un tono professionale), i punti chiave, l'obiettivo e chi è il mittente.
                2. Scrivi un'email completa in italiano (o nella lingua richiesta, se specificata) che soddisfi la richiesta dell'utente.
                3. Includi un oggetto (Subject:) appropriato.
                4. Genera solo ed esclusivamente il testo dell'email. Non aggiungere commenti o la tua analisi.
                EMAIL GENERATA:
                """
                try:
                    generation_config = {"temperature": 0.6}
                    response = model.generate_content(conversational_prompt, generation_config=generation_config)
                    st.session_state.ultima_email = response.text
                except Exception as e:
                    st.error(f"Si è verificato un errore: {e}")

# --- CONTENUTO DELLA SCHEDA 2: MODALITÀ DETTAGLIATA ---
with tab2:
    st.write("Usa le opzioni nella barra laterale per un controllo granulare su ogni aspetto dell'email.")
    with st.sidebar:
        st.title("⚙️ Controlli Dettagliati")
        st.selectbox("Usa un Modello (opzionale):", options=list(templates.keys()), key='template_selezionato', on_change=applica_template)
        st.markdown("---")
        st.header("Destinatario e Tono")
        st.text_input("A chi è indirizzata l'email?", key='destinatario')
        tono_opzioni = ["Formale", "Professionale", "Amichevole", "Informale", "Persuasivo", "Risolutivo", "Altro (specifica sotto)..."]
        st.selectbox("Tono dell'email:", tono_opzioni, key='tono_selezionato')
        if st.session_state.tono_selezionato == "Altro (specifica sotto)...":
            st.text_input("Specifica il tono personalizzato:", key="tono_personalizzato")
        st.header("Contenuto e Obiettivo")
        st.markdown("**Punti Chiave da Includere:**")
        for i in range(len(st.session_state.punti_chiave)):
            col1, col2 = st.columns([4, 1])
            st.session_state.punti_chiave[i] = col1.text_input(f"Punto #{i+1}", value=st.session_state.punti_chiave[i], label_visibility="collapsed")
            if i > 0 and col2.button("X", key=f"rimuovi_{i}"):
                st.session_state.punti_chiave.pop(i); st.rerun()
        if st.button("+ Aggiungi Punto"):
            st.session_state.punti_chiave.append(""); st.rerun()
        st.text_input("Qual è l'obiettivo finale dell'email?", key='obiettivo')
        st.header("Stile e Formato")
        st.slider("Livello di Creatività (Temperatura):", 0.0, 1.0, key="creativita", step=0.1)
        st.select_slider("Lunghezza desiderata:", ["Breve (2-3 frasi)", "Media (2 paragrafi)", "Dettagliata (3+ paragrafi)"], key='lunghezza')
        st.selectbox("Lingua dell'email:", ["Italiano", "Inglese (British)", "Inglese (American)", "Francese", "Spagnolo", "Tedesco"], key='lingua')
        st.header("La Tua Firma")
        st.text_input("Il tuo nome (per la firma):", key='mio_nome')
        st.text_input("Tua qualifica/ruolo (opzionale):", key='mio_ruolo')
    if st.button("Genera da Opzioni Dettagliate"):
        punti_validi = [punto for punto in st.session_state.punti_chiave if punto.strip()]
        if not st.session_state.destinatario or not punti_validi:
            st.warning("Per favore, compila 'Destinatario' e almeno un 'Punto chiave'.")
        else:
            with st.spinner("Il motore AI sta componendo la tua email..."):
                tono_da_usare = st.session_state.tono_personalizzato if st.session_state.tono_selezionato == "Altro (specifica sotto)..." else st.session_state.tono_selezionato
                punti_formattati = "\n- ".join(punti_validi)
                prompt = f"Agisci come un assistente di comunicazione esperto. Il tuo compito è scrivere una bozza di email impeccabile basata sulle seguenti specifiche:\n**Lingua di scrittura:** {st.session_state.lingua}, **Destinatario:** {st.session_state.destinatario}, **Tono da adottare:** {tono_da_usare}, **Lunghezza desiderata:** {st.session_state.lunghezza},\n**Punti chiave da comunicare:**\n- {punti_formattati},\n**Obiettivo principale dell'email:** {st.session_state.obiettivo},\n**Informazioni sul mittente per la firma:** Nome: {st.session_state.mio_nome}, Ruolo: {st.session_state.mio_ruolo if st.session_state.mio_ruolo else 'Non specificato'}\nPer favore, sii creativo e varia lo stile di scrittura per non sembrare un robot. Genera solo ed esclusivamente il testo dell'email, includendo un oggetto (Subject:) appropriato."
                generation_config = {"temperature": st.session_state.creativita}
                try:
                    response = model.generate_content(prompt, generation_config=generation_config)
                    st.session_state.ultima_email = response.text
                except Exception as e:
                    st.error(f"Si è verificato un errore: {e}")

# --- SEZIONE DI VISUALIZZAZIONE E PERFEZIONAMENTO (COMUNE A ENTRAMBE LE MODALITÀ) ---
if st.session_state.ultima_email:
    st.markdown("---")
    st.subheader("✉️ Bozza Corrente:")
    st.text_area("Ecco la bozza (puoi copiarla da qui):", st.session_state.ultima_email, height=300)
    st.subheader("Perfeziona il risultato:")
    col1, col2, col3 = st.columns(3)
    if col1.button("Rendila più Concisa"):
         with st.spinner("..."):
            refinement_prompt = f"Prendi la seguente email e riscrivila in modo più breve e conciso...\n\n---\n\n{st.session_state.ultima_email}"
            new_response = model.generate_content(refinement_prompt)
            st.session_state.ultima_email = new_response.text
            st.rerun()
    if col2.button("Usa un Tono più Formale"):
         with st.spinner("..."):
            refinement_prompt = f"Prendi la seguente email e riscrivila usando un linguaggio più formale...\n\n---\n\n{st.session_state.ultima_email}"
            new_response = model.generate_content(refinement_prompt)
            st.session_state.ultima_email = new_response.text
            st.rerun()
    if col3.button("Sii più Amichevole"):
         with st.spinner("..."):
            refinement_prompt = f"Prendi la seguente email e riscrivila usando un linguaggio più amichevole...\n\n---\n\n{st.session_state.ultima_email}"
            new_response = model.generate_content(refinement_prompt)
            st.session_state.ultima_email = new_response.text
            st.rerun()