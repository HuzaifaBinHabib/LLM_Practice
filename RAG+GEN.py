from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from phi.utils.pprint import pprint_run_response
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="getenv.env")
# Groq API Key and Agent Initialization
api_key = os.getenv("API_KEY")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=api_key,
    temperature=0.1
)

# Database connection details
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

# Create the SQLDatabase connection
db = SQLDatabase.from_uri(
    f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",
    sample_rows_in_table_info=8000
)
data =db.table_info
# print(data)

few_short='''Answer in just 2 or 3 lines (Do not show strictly Vector Database Results):
Retrieve and present information according to the SQL URI data in a well-structured and concise format.
Do not show SQL query results directly. Instead, provide concise answers and include relevant product details (such as size if applicable).
If no products exist in the database, respond only with: "I don't know, sorry."
'''


# Query the chain
user_input = "burberry jeckets how i buyee it"+data+few_short
response = llm.invoke(user_input)

# Extract the result from the response and ensure it is saved correctly

# Check if sql_result contains the expected data
if response:
    print("SQL Result:", response.content)
    # Print the result in markdown format
    # pprint_run_response(response.content, markdown=True)
else:
    print("No result found in the response.")
