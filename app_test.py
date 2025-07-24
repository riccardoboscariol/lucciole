import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

# SETUP Google Sheet
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("lucciole_risposte").sheet1

# Funzione per scala inversa
def reverse(score):
    return 6 - score  # 1 diventa 5, 2 diventa 4, ecc.

st.title("🧠 Test Interpersonal Reactivity Index (IRI)")
st.markdown("Compila tutte le 28 domande. I tuoi dati saranno trasformati in un'opera visiva generativa.")

# DOMANDE per scala
questions = {
    "Perspective Taking": {
        "Cerco di guardare le cose dal punto di vista dei miei amici quando siamo in disaccordo.": False,
        "A volte ho difficoltà a vedere le cose dal punto di vista di qualcun altro.": True,
        "Cerco di pensare agli altri in situazioni simili a quella che stanno vivendo.": False,
        "Spesso riesco ad anticipare come una persona si sentirà rispetto a una situazione.": False,
        "Ho difficoltà a vedere le cose da una prospettiva diversa dalla mia.": True,
        "Sono molto bravo/a a vedere le cose dalla prospettiva di un’altra persona.": False,
        "Prima di criticare qualcuno, cerco di immaginare come mi sentirei al suo posto.": False
    },
    "Fantasy": {
        "Riesco facilmente a mettermi nei panni dei personaggi nei romanzi o nei film.": False,
        "Spesso mi sento come se stessi vivendo direttamente le esperienze dei personaggi dei libri.": False,
        "Quando guardo un film o leggo, dimentico me stesso/a e mi identifico completamente con il personaggio.": False,
        "Mi immagino facilmente come sarebbe essere nei panni di un eroe o un’eroina.": False,
        "Non riesco a entrare nella storia quando leggo narrativa o guardo film.": True,
        "Mi capita di provare emozioni forti per i personaggi immaginari.": False,
        "Mi sento coinvolto/a nei destini dei personaggi quando guardo film o leggo romanzi.": False
    },
    "Empathic Concern": {
        "Spesso provo tenerezza e compassione per le persone meno fortunate di me.": False,
        "A volte non mi sento particolarmente toccato/a quando vedo persone che hanno bisogno di aiuto.": True,
        "Mi capita di preoccuparmi per persone che sembrano avere problemi.": False,
        "Mi sento coinvolto/a quando vedo qualcuno essere trattato ingiustamente.": False,
        "Riesco a sentire grande compassione per chi soffre.": False,
        "Mi irrita quando qualcuno si comporta in modo debole e bisognoso.": True,
        "Provo affetto e cura per persone che hanno bisogno di supporto.": False
    },
    "Personal Distress": {
        "A volte mi sento sopraffatto/a quando vedo qualcuno soffrire.": False,
        "Reagisco con disagio quando vedo qualcuno in difficoltà.": False,
        "Mi sento a disagio in situazioni in cui gli altri hanno problemi emotivi.": False,
        "Quando vedo qualcuno che ha bisogno urgente di aiuto, mi sento sconvolto/a.": False,
        "Cerco di evitare di entrare in contatto con persone che sono molto angosciate.": True,
        "Mi sento agitato/a quando vedo qualcuno essere maltrattato.": False,
        "Quando vedo qualcuno ferito, mi sento nervoso/a e scosso/a.": False
    }
}

# Risposte utente
user_responses = []
scores = {"Perspective Taking": 0, "Fantasy": 0, "Empathic Concern": 0, "Personal Distress": 0}

st.write("---")
st.subheader("📋 Rispondi da 1 (Per niente d'accordo) a 5 (Molto d'accordo)")

for category, items in questions.items():
    st.markdown(f"### {category}")
    for question, is_reversed in items.items():
        val = st.slider(question, 1, 5, 3, key=question)
        adjusted = reverse(val) if is_reversed else val
        scores[category] += adjusted
        user_responses.append(val)

# MEDIA su 7 item per categoria
final_scores = {k: round(v / 7, 2) for k, v in scores.items()}

# Invio
if st.button("📨 Invia le tue risposte"):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([
        now,
        *user_responses,
        final_scores["Perspective Taking"],
        final_scores["Fantasy"],
        final_scores["Empathic Concern"],
        final_scores["Personal Distress"]
    ])
    st.success("Risposte inviate! Grazie 🌱 La tua forma si sta generando...")

