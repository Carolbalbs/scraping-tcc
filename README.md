# Visualizador de Artigos PubMed (TCC)

Esta é uma interface Streamlit para visualizar os resultados do scraping de artigos do PubMed salvos em formato JSON.

## Como executar localmente

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Execute o Streamlit:
   ```bash
   streamlit run app.py
   ```

## Requisitos para Publicação no Streamlit Cloud

Para publicar no [Streamlit Cloud](https://streamlit.io/cloud), siga estes requisitos:

1. **Repositório Git:** O código deve estar em um repositório público (ou privado com permissão) no GitHub.
2. **Arquivo `requirements.txt`:** Deve conter `streamlit` e `pandas`. Já está incluído na raiz.
3. **Arquivo de Dados:** O arquivo `pubmed_articles.json` deve estar presente no repositório para que a nuvem consiga lê-lo.
4. **Estrutura:** O arquivo principal deve ser o `app.py`.

### Passos para Deploy:
1. Faça o push do seu código para o GitHub.
2. Acesse [share.streamlit.io](https://share.streamlit.io).
3. Conecte seu repositório.
4. Selecione o arquivo `app.py` como "Main file path".
5. Clique em "Deploy".

## Funcionalidades
- Resumo estatístico (Total de artigos, Data da busca).
- Listagem de palavras-chave utilizadas.
- Filtro por busca textual (Título, Autor, Periódico).
- Filtros laterais por Ano e Periódico.
- Visualização detalhada de abstracts com expanders.
- Download dos dados filtrados em formato CSV.
