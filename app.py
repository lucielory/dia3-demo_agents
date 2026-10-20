import streamlit as st
from llm_agent import ConversationAgent


st.set_page_config(page_title="Jarvis")
st.title("Barbe-Quasar")


# Streamlit relance tout le script à chaque message : seul st.session_state
# survit, donc on y garde l'agent (et son conversation_history)
if "agent" not in st.session_state:
	st.session_state.agent = ConversationAgent()

agent = st.session_state.agent


# Réaffiche tous les messages précédents (sauf le prompt système)
for message in agent.conversation_history:
	if message["role"] == "system":
		continue
	with st.chat_message(message["role"]):
		st.markdown(message["content"])


user_input = st.chat_input(
	"Que veux tu moussaillon ?",
	accept_file=False,
	)

if user_input :
	with st.chat_message("user"):
		st.markdown(user_input)

	with st.chat_message("assistant"):
		with st.spinner("Barbe-Quasar réfléchit..."):
			response = agent.ask_llm(user_input)
		st.markdown(response)
