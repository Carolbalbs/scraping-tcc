import streamlit as st
import json
import pandas as pd
import os
from datetime import datetime

# Page configuration for Streamlit Cloud
st.set_page_config(
    page_title="Visualizador de Artigos TCC",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better aesthetics
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stCard {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .article-title {
        color: #1e88e5;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .badge {
        background-color: #e3f2fd;
        color: #1976d2;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        margin-right: 5px;
    }
    </style>
""", unsafe_allow_html=True)

def load_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo JSON: {e}")
        return None

def main():
    st.title("📚 Dashboard de Artigos TCC")
    st.markdown("Visualize de forma amigável os resultados do seu scraping de diversas plataformas.")

    # Sidebar: File Selection
    st.sidebar.header("📁 Seleção de Dados")
    json_files = [f for f in os.listdir('.') if f.endswith('.json')]
    
    if not json_files:
        st.error("Nenhum arquivo JSON encontrado no diretório.")
        return

    selected_file = st.sidebar.selectbox(
        "Escolha o arquivo de dados:",
        json_files,
        index=json_files.index("pubmed_articles.json") if "pubmed_articles.json" in json_files else 0
    )

    # Load data
    data = load_data(selected_file)

    if not data:
        st.warning("Nenhum dado encontrado no arquivo JSON.")
        return

    # Sidebar: Summary and Filters
    st.sidebar.header("🔍 Filtros e Resumo")
    
    # Summary stats
    gen_at = data.get("generated_at", "N/A")
    try:
        dt_obj = datetime.fromisoformat(gen_at)
        formatted_date = dt_obj.strftime("%d/%m/%Y %H:%M:%S")
    except:
        formatted_date = gen_at

    st.sidebar.info(f"📅 **Data da busca:**\n{formatted_date}")
    st.sidebar.metric("Total de Artigos", data.get("total", 0))

    # Keywords display
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔑 Palavras-chave")
    for kw in data.get("keywords", []):
        st.sidebar.markdown(f"- {kw}")

    # Main area
    articles = data.get("articles", [])
    if not articles:
        st.info("Nenhum artigo encontrado.")
        return

    df = pd.DataFrame(articles)
    
    # Ensure necessary columns exist in the DataFrame to avoid errors
    for col in ['title', 'authors', 'journal', 'year', 'pmid', 'abstract', 'url', 'doi']:
        if col not in df.columns:
            df[col] = "N/A"

    # Search and Filter logic
    search_query = st.text_input("Filtrar por título, autor ou periódico:", "")
    
    filtered_df = df.copy()
    if search_query:
        mask = (
            df['title'].astype(str).str.contains(search_query, case=False, na=False) |
            df['authors'].astype(str).str.contains(search_query, case=False, na=False) |
            df['journal'].astype(str).str.contains(search_query, case=False, na=False)
        )
        filtered_df = df[mask]

    # Filters by Year and Journal in Sidebar
    years = sorted(df['year'].astype(str).unique(), reverse=True)
    selected_year = st.sidebar.multiselect("Filtrar por Ano:", years, default=years)
    
    journals = sorted(df['journal'].astype(str).unique())
    selected_journals = st.sidebar.multiselect("Filtrar por Periódico:", journals, default=journals)

    filtered_df = filtered_df[
        (filtered_df['year'].astype(str).isin(selected_year)) &
        (filtered_df['journal'].astype(str).isin(selected_journals))
    ]

    st.write(f"Exibindo **{len(filtered_df)}** de **{len(df)}** artigos.")

    # Displaying Articles
    for _, row in filtered_df.iterrows():
        with st.container():
            st.markdown(f"### {row['title']}")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            col1.markdown(f"🗓️ **Ano:** {row['year']}")
            col2.markdown(f"📖 **Journal:** {row['journal']}")
            
            pmid_val = row.get('pmid', 'N/A')
            col3.markdown(f"🆔 **ID/PMID:** {pmid_val}")

            with st.expander("Ver Resumo e Detalhes"):
                st.markdown("**Autores:**")
                st.write(row.get('authors', 'Não informado'))
                st.markdown("**Abstract:**")
                st.write(row.get('abstract', 'Resumo não disponível'))
                
                doi = row.get('doi')
                if doi and doi != "N/A":
                    st.markdown(f"🔗 **DOI:** [{doi}](https://doi.org/{doi})")
                
                url = row.get('url', '#')
                st.markdown(f"🌐 [Acessar Artigo]({url})")
            
            st.markdown("---")

    # Download Button
    st.sidebar.markdown("---")
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="📥 Baixar Filtros como CSV",
        data=csv,
        file_name='artigos_filtrados.csv',
        mime='text/csv',
    )

if __name__ == "__main__":
    main()
