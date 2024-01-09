import os
from langchain.vectorstores.faiss import FAISS
from langchain.docstore.in_memory import InMemoryDocstore
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings


# Environment settings
os.environ["OPENAI_API_KEY"] = "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"

# Define URLs you want to fetch documents from
urls = ["https://coal.nic.in", "https://mines.gov.in"]
loaders = UnstructuredURLLoader(urls)
data = loaders.load()

# We split the loaded documents on line breaks('\\n') and make sure that each
# chunk has a maximum of 1000 characters.
text_splitter = CharacterTextSplitter(separator='\n', chunk_size=1000, chunk_overlap=200)
docs = text_splitter.split_documents(data)

# From the OpenAI embeddings, we generate embeddings for our documents
embeddings = OpenAIEmbeddings()
doc_embeddings = []
for doc in docs:
  embedded_doc = embeddings.embed_query(doc["content"])
  doc_embeddings.append((doc["content"], embedded_doc))

# Initialize document store and store embeddings and text in it
docstore = InMemoryDocstore()
ids = docstore.add({str(i): {"content": doc} for i, doc in enumerate(docs)})

# Initialize the FAISS vector store and add the document vectors to it
vectorstore = FAISS.from_embeddings(doc_embeddings, OpenAIEmbeddings(), ids=ids)

# Ask the question to the language model
question = "what is mining"

# Get the embeddings for the question
question_embedding = embeddings.embed_query(question)

# Find the most similar document to the question
most_similar_document = vectorstore.similarity_search_by_vector(question_embedding, k=1)[0]

# Get the answer for the question using the most similar document
answer = most_similar_document.page_content

# The response statement would be "answer".
print(answer)