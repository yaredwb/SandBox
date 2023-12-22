from llama_index import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("C:\\Users\\yaredbe\\Documents\\Literature").load_data()
index = VectorStoreIndex(documents)
