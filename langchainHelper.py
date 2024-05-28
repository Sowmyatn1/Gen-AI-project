from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import chroma
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.vectorstores import Chroma
from langchain.prompts import FewShotPromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.prompts.prompt import PromptTemplate
import os
from Fewshots import few_shots


from dotenv import load_dotenv
load_dotenv()


def get_few_shot_db_chain():
    # create llm object
    llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=os.environ["api_key"], temperature=0.1)

    #create DB object
    db_user="root"
    db_password="1234"
    db_host="localhost"
    db_name="atliq_tshirts"
    db=SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",sample_rows_in_table_info=3)
    #print(db.table_info)

    # create embeddings
    # create a embedding for the Q and A , embedding is a sequence of numbers represents word as a number
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    # convert all the strings in few_shot array to a single line string
    to_vectorize = [" ".join(examples.values()) for examples in few_shots]
    #print(to_vectorize)

    # save the above embedding into a vector database

    vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=few_shots)

    # Similarity matching for the embeddings we saved in the vectordatabase.ex: find in the vector
    # database similar looking queries

    example_selector = SemanticSimilarityExampleSelector(
        vectorstore=vectorstore,
        k=2,
    )

    example_selector.select_examples({"Question": "How many Adidas T shirts I have left in my store?"})

    # create a custom propmt to say instructions like use only column relevent to my table
    print(_mysql_prompt)

    # create a prompt template

    example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult", "Answer", ],
        template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
    )

    # create relation ship between llm and vector database ask llm to refer to vector db when a question is asked

    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=_mysql_prompt,
        suffix=PROMPT_SUFFIX,
        input_variables=["input", "table_info", "top_k"],
    )

    new_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, prompt=few_shot_prompt)

    return new_chain


if __name__=="__main__":
    chain=get_few_shot_db_chain()
    print(chain.run("How many totoal tshirts are left in totoal stocks?"))




