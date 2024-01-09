from flask import Flask, render_template, request, jsonify
import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import UnstructuredURLLoader
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main_page.html')

@app.route('/main')
def main_page():
    return render_template('botinterface.html')

@app.route('/process_input', methods=['POST'])
def process_input():
    z = request.json.get('user_input', '')
    os.environ["OPENAI_API_KEY"] = "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"
    urls = ["https://coal.nic.in", "https://mines.gov.in"]
    loaders = UnstructuredURLLoader(urls)
    data = loaders.load()
    text_splitter = CharacterTextSplitter(separator='\n', chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(data)
    embeddings = OpenAIEmbeddings()
    corpus = [" ".join(doc) for doc in docs]
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)
    llm = OpenAI(temperature=0, model_name='text-davinci-003')

    def retrieve_answers(question):
        question_vector = vectorizer.transform([question])
        similarities = cosine_similarity(question_vector, X)
        top_doc_index = similarities.argmax()
        top_doc = docs[top_doc_index]
        answer = llm.predict({"question": question, "context": top_doc})['answer']
        return answer

    response = retrieve_answers(z)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
