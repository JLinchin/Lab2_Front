import streamlit as st
import requests

api_url = "https://supreme-succotash-7v9gw6p7x79whrrvp-8000.app.github.dev/predict"

st.set_page_config(page_title="Prédiction Prix Immobilier", page_icon="🏠", layout="centered")

st.title("🏠 Prédiction du prix d'un logement")
st.write("Renseignez les champs ci-dessous puis envoyez la requête à l'API.")

st.subheader("Caractéristiques du logement")

col1, col2 = st.columns(2)

with col1:
    med_inc = st.number_input("Salaire médian", value=8.3, step=0.1, format="%.2f")
    house_age = st.number_input("Age moyen des maisons", value=41.0, step=1.0, format="%.0f")
    ave_rooms = st.number_input("Nombre moyen de pièces", value=6.9, step=0.1, format="%.2f")
    ave_bedrms = st.number_input("Nombre moyen de chambres", value=1.0, step=0.1, format="%.2f")

with col2:
    population = st.number_input("Population", value=322.0, step=1.0, format="%.0f")
    ave_occup = st.number_input("Nombre moyen d'occupants par maison", value=2.5, step=0.1, format="%.2f")
    latitude = st.number_input("Latitude", value=37.88, step=0.01, format="%.2f")
    longitude = st.number_input("Longitude", value=-122.23, step=0.01, format="%.2f")

# Construction de la requête JSON
requete = {
    "MedInc": med_inc,
    "HouseAge": house_age,
    "AveRooms": ave_rooms,
    "AveBedrms": ave_bedrms,
    "Population": population,
    "AveOccup": ave_occup,
    "Latitude": latitude,
    "Longitude": longitude,
}

if st.button("🚀 Envoyer la requête", type="primary", use_container_width=True):
    if not api_url:
        st.error("Veuillez renseigner l'URL de l'API.")
    else:
        try:
            with st.spinner("Envoi de la requête en cours..."):
                response = requests.post(api_url, json=requete, timeout=15)

            if response.status_code == 200:
                st.success("Requête envoyée avec succès !")
                try:
                    result = response.json()
                    st.subheader("Réponse de l'API")
                    st.json(result)
                except ValueError:
                    st.subheader("Réponse de l'API (texte brut)")
                    st.text(response.text)
            else:
                st.error(f"Erreur : l'API a répondu avec le code {response.status_code}")
                st.text(response.text)

        except requests.exceptions.ConnectionError:
            st.error("Impossible de se connecter à l'API. Vérifiez l'URL et que le serveur est bien lancé.")
        except requests.exceptions.Timeout:
            st.error("La requête a expiré (timeout).")
        except requests.exceptions.RequestException as e:
            st.error(f"Une erreur est survenue lors de la requête : {e}")