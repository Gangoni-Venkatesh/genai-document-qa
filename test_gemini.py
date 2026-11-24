from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv(override=True)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.3
)

try:
    response = llm.invoke(
        "Explain Retrieval-Augmented Generation in two simple sentences."
    )

    print("\nGEMINI API CONNECTION SUCCESSFUL!")
    print("--------------------------------")
    print(response.content)

except Exception as e:
    print("\nGEMINI API CONNECTION FAILED!")
    print("--------------------------------")
    print(type(e).__name__)
    print(str(e)[:1000])