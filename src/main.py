import streamlit as st

from services import ExecutionsService
from utils import dataframes, download_link, relative_time, render_badge

if "executions" not in st.session_state:
    st.session_state.executions = []


@st.fragment
def executions_section():
    st.session_state.executions = ExecutionsService().list_executions()

    if not st.session_state.executions:
        st.info("Nenhuma execução encontrada")
        return

    for execution in st.session_state.executions:
        with st.container(key=execution.uuid):
            with st.expander(f"{execution.uuid}", expanded=False):
                first_column, second_column = st.columns(2)
                with first_column:
                    st.markdown(
                        **relative_time("Inicializada", execution.started_at)  # type: ignore
                    )
                    st.badge(**render_badge(execution))  # type: ignore
                with second_column:
                    st.markdown(
                        **relative_time("Concluída", execution.completed_at)  # type: ignore
                    )

                input_tab, output_tab = st.tabs(["Entrada", "Saída"])
                with input_tab:
                    st.markdown(
                        f"**Download:** {download_link(execution.input_file)}",
                        unsafe_allow_html=True,
                    )
                    dfs = dataframes(execution.input_file)
                    tabs = st.tabs(list(dfs.keys()))  # type: ignore
                    for tab, (_, df) in zip(tabs, dfs.items()):  # type: ignore
                        with tab:
                            st.dataframe(df)
                with output_tab:
                    st.markdown(
                        f"**Download:** {download_link(execution.output_file)}",
                        unsafe_allow_html=True,
                    )
                    dfs = dataframes(execution.output_file)
                    tabs = st.tabs(list(dfs.keys()))  # type: ignore
                    for tab, (_, df) in zip(tabs, dfs.items()):  # type: ignore
                        with tab:
                            st.dataframe(df)


st.html("""
<style>
    .footer-center {
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        color: rgb(100, 102, 106);
        font-size: 0.9rem;
    }

    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
    }

    /* Target all Streamlit buttons */
    .stButton > button {
        background-color: rgb(0, 161, 252) !important;
        border-color: rgb(0, 161, 252) !important;
        color: white !important;
    }

    /* Hover state */
    .stButton > button:hover {
        background-color: rgb(0, 141, 232) !important;
        border-color: rgb(0, 141, 232) !important;
        color: white !important;
    }

    /* Focus state */
    .stButton > button:focus {
        background-color: rgb(0, 161, 252) !important;
        border-color: rgb(0, 161, 252) !important;
        color: white !important;
    }

    /* Target form submit buttons specifically */
    .stFormSubmitButton > button {
        background-color: rgb(0, 161, 252) !important;
        border-color: rgb(0, 161, 252) !important;
        color: white !important;
    }

    /* Form submit button hover state */
    .stFormSubmitButton > button:hover {
        background-color: rgb(0, 141, 232) !important;
        border-color: rgb(0, 141, 232) !important;
        color: white !important;
    }

    /* Form submit button focus state */
    .stFormSubmitButton > button:focus {
        background-color: rgb(0, 161, 252) !important;
        border-color: rgb(0, 161, 252) !important;
        color: white !important;
    }

    /* Target secondary buttons */
    .stFileUploader button {
        border-color: rgb(0, 161, 252) !important;
    }

    /* Secondary button hover state */
    .stFileUploader button:hover {
        background-color: #f8f8f8 !important;
        border-color: rgb(0, 161, 252) !important;
        color: #333 !important;
    }

    /* Secondary button focus state */
    .stFileUploader button:focus {
        background-color: rgb(0, 161, 252) !important;
        border-color: rgb(0, 161, 252) !important;
        color: white !important;
    }
</style>
""")

with st.sidebar:
    st.logo("src/public/crewai.svg", size="large")
    st.divider()
    st.text(
        """
        Esta aplicação demonstra como projetar interfaces visuais eficazes que se integram perfeitamente com automações da CrewAI — suportando tanto processos baseados em Crews quanto processos baseados em Flows.

        Explore exemplos interativos que destacam as melhores práticas para criar experiências de usuário intuitivas e produtivas, com base nas capacidades de automação da CrewAI.
        """
    )
    st.markdown(
        "[**Avalie gratuitamente**](https://app.crewai.com/)",
    )
    st.divider()
    with st.form("upload_form", clear_on_submit=True, border=False):
        st.file_uploader(
            "Aparelhos",
            key="file_uploader",
            type="xlsx",
            help="Carregue um arquivo XLSX com todas os aparelhos que deseja pesquisar",
        )
        st.form_submit_button(
            "Upload",
            type="primary",
        )

with st.container():
    st.subheader("Análise Mercadológica de Aparelhos Celulares")
    executions_section()

with st._bottom:
    st.html(
        """
        <p class="footer-center">
            CrewAI © Copyright 2025, All Rights Reserved by CrewAI™, Inc.
        </p>
        """
    )

if st.session_state.file_uploader is not None:
    celphones_spreadsheet = st.session_state.file_uploader.getvalue()
    ExecutionsService().start_execution(celphones_spreadsheet)
    st.toast(
        "Execução iniciada! Recarregue a página para ver os resultados.",
        icon=":material/refresh:",
    )
