
########################################################################################################################

import json
import os

from fastapi import FastAPI, HTTPException, Path, Body, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from agent_getter import get_chain

router = APIRouter()

from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(
    model_name="gpt-4o",
    temperature=0,
    streaming=True,
    api_key=openai_api_key
)


class ExecuteChainRequest(BaseModel):
    chain_id: str = Field(..., example="example_chain", title="Chain ID", description="The unique ID of the chain to execute.")
    query: Dict[str, Any] = Field(..., example={"input": "What is my name?", "chat_history": [["user", "hello, my name is mario!"], ["assistant", "hello, how are you mario?"]]}, title="Query", description="The input query for the chain.")
    inference_kwargs: Dict[str, Any] = Field(..., example={}, description="")



@router.post("/stream_events_chain")
async def stream_events_chain(request: ExecuteChainRequest):

    async def generate_response(chain: Any, query: Dict[str, Any], inference_kwargs: Dict[str, Any], stream_only_content: bool = False):

        async for event in chain.astream_events(
            query,
            version="v1",
            **inference_kwargs,
    ):
            kind = event["event"]
            if kind == "on_chain_start":
                if (
                        event["name"] == "Agent"
                ):  # Was assigned when creating the agent with `.with_config({"run_name": "Agent"})`
                    print(
                        f"Starting agent: {event['name']} with input: {event['data'].get('input')}"
                    )
            elif kind == "on_chain_end":
                if (
                        event["name"] == "Agent"
                ):  # Was assigned when creating the agent with `.with_config({"run_name": "Agent"})`
                    print()
                    print("--")
                    print(
                        f"Done agent: {event['name']} with output: {event['data'].get('output')['output']}"
                    )
            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    # Empty content in the context of OpenAI means
                    # that the model is asking for a tool to be invoked.
                    # So we only print non-empty content
                    print(content, end="|")
                    yield content
            elif kind == "on_tool_start":
                print("--")
                print(
                    f"Starting tool: {event['name']} with inputs: {event['data'].get('input')}"
                )
            elif kind == "on_tool_end":
                print(f"Done tool: {event['name']}")
                print(f"Tool output was: {event['data'].get('output')}")
                print("--")

    try:
        body = request

        chain = get_chain(
            llm=llm,
            connection_string="mongodb://localhost:27017",
            default_database="item_classification_db_3",
            default_collection=None
        )

        query = body.query
        inference_kwargs = body.inference_kwargs
        return StreamingResponse(generate_response(chain, query, inference_kwargs), media_type="application/json")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permetti tutte le origini
    allow_credentials=True,
    allow_methods=["*"],  # Permetti tutti i metodi (GET, POST, OPTIONS, ecc.)
    allow_headers=["*"],  # Permetti tutti gli headers
)

app.include_router(router, prefix="/agent", tags=["agent"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8100)

