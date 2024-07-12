import streamlit as st
from streamlit_option_menu import option_menu


class MultiApp:
    def __init__(self, user=None):
        self.user = user
        self.apps = dict()
        if 'current_page' not in st.session_state:
            st.session_state.current_page = None

    def add_app(self, title, func):
        self.apps[title] = func

    def change_page(self, new_page):
        st.session_state.current_page = new_page
        st.rerun()

    async def run(self):
        st.set_page_config(layout='wide')

        with st.sidebar:
            selected = option_menu("Main Menu" if not self.user else self.user['name'],
                                   list(self.apps.keys()),
                                   icons=[],
                                   menu_icon='house',
                                   default_index=0)

        # Si la página seleccionada es diferente a la página actual, cambia la página
        if selected != st.session_state.current_page:
            self.change_page(selected)

        # Limpia el contenido anterior
        main_container = st.empty()

        # Renderiza la página seleccionada
        with main_container.container():
            await self.apps[selected]()
