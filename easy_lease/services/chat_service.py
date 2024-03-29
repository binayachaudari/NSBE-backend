import pickle
import cohere
import os
import hnswlib
import json
import uuid
from dotenv import load_dotenv
from typing import List, Dict
from unstructured.partition.html import partition_html
from unstructured.chunking.title import chunk_by_title

# Load environment variables from .env file
load_dotenv()
# Now you can access the environment variables using os.environ
API_KEY = os.environ.get('COHERE_API_KEY')

co = cohere.Client(API_KEY)

class Documents:
    def __init__(self, sources: List[Dict[str, str]]):
        self.sources = sources
        self.docs = []
        self.docs_embs = []
        self.retrieve_top_k = 10
        self.rerank_top_k = 5
        # # Enable load and embed methods to write to a pickel file
        # self.load()
        # self.embed()
        self.index()

    def load(self) -> None:
        """
        Loads the documents from the sources and chunks the HTML content.
        """
        print("Loading documents...")

        for source in self.sources:
            elements = partition_html(url=source["url"])
            chunks = chunk_by_title(elements)
            for chunk in chunks:
                self.docs.append(
                    {
                        "title": source["title"],
                        "text": str(chunk),
                        "url": source["url"],
                    }
                )

    def embed(self) -> None:
            """
            Embeds the documents using the Cohere API.
            """
            print("Embedding documents...")

            batch_size = 90
            self.docs_len = len(self.docs)

            for i in range(0, self.docs_len, batch_size):
                batch = self.docs[i : min(i + batch_size, self.docs_len)]
                texts = [item["text"] for item in batch]
                docs_embs_batch = co.embed(
                      texts=texts,
                          model="embed-english-v3.0",
                          input_type="search_document"
          ).embeddings

            self.docs_embs.extend(docs_embs_batch)

            with open("docs_embs.pkl", "wb") as f:
                pickle.dump({
                    'docs': self.docs,
                    'embeds': self.docs_embs,
                    'count': self.docs_len
                }, f)
            

    def index(self) -> None:
            """
            Indexes the documents for efficient retrieval.
            """
            print("Indexing documents...")

            with open('docs_embs.pkl', 'rb') as f:
                loaded_model = pickle.load(f)
                self.docs_embs = loaded_model['embeds']
                self.docs_len = loaded_model['count']
                self.docs = loaded_model['docs']

            self.index = hnswlib.Index(space="ip", dim=1024)
            self.index.init_index(max_elements=self.docs_len, ef_construction=512, M=64)
            self.index.add_items(self.docs_embs, list(range(len(self.docs_embs))))

            print(f"Indexing complete with {self.index.get_current_count()} documents.")


    def retrieve(self, query: str) -> List[Dict[str, str]]:
          """
          Retrieves documents based on the given query.

          Parameters:
          query (str): The query to retrieve documents for.

          Returns:
          List[Dict[str, str]]: A list of dictionaries representing the retrieved  documents, with 'title', 'snippet', and 'url' keys.
          """
          docs_retrieved = []
          query_emb = co.embed(
                      texts=[query],
                      model="embed-english-v3.0",
                      input_type="search_query"
                      ).embeddings

          doc_ids = self.index.knn_query(query_emb, k=self.retrieve_top_k)[0][0]

          docs_to_rerank = []
          for doc_id in doc_ids:
              docs_to_rerank.append(self.docs[doc_id]["text"])

          rerank_results = co.rerank(
              query=query,
              documents=docs_to_rerank,
              top_n=self.rerank_top_k,
              model="rerank-english-v2.0",
          )

          doc_ids_reranked = []
          for result in rerank_results:
              doc_ids_reranked.append(doc_ids[result.index])

          for doc_id in doc_ids_reranked:
              docs_retrieved.append(
                  {
                      "title": self.docs[doc_id]["title"],
                      "text": self.docs[doc_id]["text"],
                      "url": self.docs[doc_id]["url"],
                  }
              )

          return docs_retrieved

class Chatbot:
    def __init__(self, docs: Documents):
        self.docs = docs
        self.conversation_id = str(uuid.uuid4())

    def retrieve_docs(self, response) -> List[Dict[str, str]]:
        """
        Retrieves documents based on the search queries in the response.

        Parameters:
        response: The response object containing search queries.

        Returns:
        List[Dict[str, str]]: A list of dictionaries representing the retrieved documents.

        """
        # Get the query(s)
        queries = []
        for search_query in response.search_queries:
            queries.append(search_query["text"])

        # Retrieve documents for each query
        retrieved_docs = []
        for query in queries:
            retrieved_docs.extend(self.docs.retrieve(query))

        return retrieved_docs

    def generate_response(self, message: str):
      # Generate search queries (if any)
      response = co.chat(message=message, search_queries_only=True)

      # If there are search queries, retrieve documents and respond
      if response.search_queries:
          print("Retrieving information...")

          documents = self.retrieve_docs(response)

          response = co.chat(
              message=message,
              documents=documents,
              conversation_id=self.conversation_id,
              stream=False,
              preamble_override="Generate informative responses to questions about housing and renting in Toronto, Canada. Your responses should be concise, accurate, and provide relevant information to the user"
          )
          # for event in response:
          #     yield event
          # yield response

          return response

      # If there is no search query, directly respond
      else:
          response = co.chat(
              message=message,
              conversation_id=self.conversation_id,
              stream=False,
              preamble_override="Generate informative responses to questions about housing and renting in Toronto, Canada. Your responses should be concise, accurate, and provide relevant information to the user"
          )
          # for event in response:
          #     yield event
          return response

class App:
    def __init__(self, chatbot: Chatbot):
        """
        Initializes an instance of the App class.

        Parameters:
        chatbot (Chatbot): An instance of the Chatbot class.

        """
        self.chatbot = chatbot

    def run(self, message):
      """
      Runs the chatbot application.
      """
      # Get the chatbot response
      response = self.chatbot.generate_response(message)

      # Print the chatbot response
      citations_flag = False
      return response

      # for event in response:
      #     stream_type = type(event).__name__

      #     # Text
      #     if stream_type == "StreamTextGeneration":
      #         return event.text
