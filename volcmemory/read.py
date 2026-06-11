# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd. and/or its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import logging
import json
import os

from veadk import Agent, Runner
from agentkit.apps import AgentkitSimpleApp
from veadk.prompts.agent_default_prompt import DEFAULT_DESCRIPTION, DEFAULT_INSTRUCTION
from mem0 import MemoryClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


app = AgentkitSimpleApp()

agent_name = "Agent"
description = DEFAULT_DESCRIPTION 
system_prompt = DEFAULT_INSTRUCTION 


tools = []

# from veadk.tools.builtin_tools.web_search import web_search
# tools.append(web_search)


agent = Agent(
    name=agent_name,
    description=description,
    instruction=system_prompt,
    tools=tools,
)
runner = Runner(agent=agent)
api_key=os.environ.get("VOLCENGINE_MEMROY_KEY")
host="https://mem0-cnlfjzigaku8gczkzo.mem0.volces.com:8000"
m = MemoryClient(host=host,api_key=api_key)

@app.entrypoint
async def run(payload: dict, headers: dict) -> str:
    prompt = payload["prompt"]
    user_id = headers["user_id"]
    session_id = headers["session_id"]
    query = "我的名字是啥?"
    #response = await runner.run(messages=prompt, user_id=user_id, session_id=session_id)
    
    for i in range(100, 201):
        user_id = f"user-{i}"
        start = asyncio.get_event_loop().time()
        
        relevant_memories = m.search(query=query, user_id=user_id)
        elapsed = asyncio.get_event_loop().time() - start

        logger.info(f"search memory: user_id: {user_id}, session_id: {session_id}, memories_count: {len(relevant_memories)}, elapsed: {elapsed:.3f}s")
        await asyncio.sleep(0.1)
    
    response = "all"    
    logger.info(f"Run response: {response}")
    return response


@app.ping
def ping() -> str:
    return "pong!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
