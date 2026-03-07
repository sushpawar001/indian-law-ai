from db.db import vector_store

# vector_store.
query = "What Union territories specified?"
results = vector_store.similarity_search(query, k=1)
print(results)
query = "The Madras Rent and Revenue Sales Act, 1839"
results = vector_store.similarity_search(query, k=1)
print(results)
query = "THE POLICE, AGRA ACT, 1854"
results = vector_store.similarity_search(query, k=1)
print(results)
