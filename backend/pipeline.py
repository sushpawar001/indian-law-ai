from langchain_community.document_loaders import PyPDFLoader
from db.db import vector_store
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.csv_loader import CSVLoader
import pandas as pd
from langchain_community.document_loaders import DataFrameLoader

def constitution_processor():
    file_path = "../docs/constitution_of_india.pdf"
    loader = PyPDFLoader(file_path)

    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,  # chunk size
        chunk_overlap=200,  # chunk overlap
        add_start_index=True,  
    )

    all_splits = text_splitter.split_documents(docs)

    print(f"Split document into {len(all_splits)} sub-documents.")

    vector_store.add_documents(documents=all_splits)

    print("Stored data into vector db")


def laws_parquet_processor():
    files_path = "../docs/central-00000-of-00001.parquet"
    col_name = "Markdown"

    df = pd.read_parquet(files_path)


    missing_count = df[col_name].isna().sum()
    print(f"Warning: Found {missing_count} rows missing {col_name} text. Dropping them.")
    clean_df = df.dropna(subset=[col_name])

    loader = DataFrameLoader(clean_df, page_content_column=col_name)
    docs = loader.load()


    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,  # chunk size
        chunk_overlap=200,  # chunk overlap
        add_start_index=True,
    )

    all_splits = text_splitter.split_documents(docs)

    print(f"Split document into {len(all_splits)} sub-documents.")

    vector_store.add_documents(documents=all_splits)

    print("Stored Laws data into vector db")

if __name__ == "__main__":
    # constitution_processor()
    laws_parquet_processor()