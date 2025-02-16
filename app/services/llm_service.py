from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.schema import HumanMessage, SystemMessage
from typing import Dict

class LLMService:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.7)
        self.summary_parser = JsonOutputParser()

    async def generate_summary(self, document: str) -> str:
        summary_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="You are a helpful assistant that summarizes documents."),
            HumanMessage(content="""
                Summarize the following document in less than 140 words. 
                Return the result in JSON format with a single key 'summary'.
                Document: {document}
            """)
        ])
        
        chain = summary_prompt | self.llm | self.summary_parser
        result = await chain.ainvoke({"document": document})
        return result['summary']

    async def generate_recommendation_reason(
        self,
        query_doc: str,
        retrieved_doc: str
    ) -> str:
        recommend_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="You are a helpful assistant that explains document similarities."),
            HumanMessage(content="""
                Explain why these two documents are related and why someone interested in the first document
                might be interested in the second document. Keep it concise and specific.
                
                Document 1: {query_doc}
                Document 2: {retrieved_doc}
            """)
        ])
        
        chain = recommend_prompt | self.llm
        result = await chain.ainvoke({
            "query_doc": query_doc,
            "retrieved_doc": retrieved_doc
        })
        return result 