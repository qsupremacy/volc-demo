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

async def add_memory(m: MemoryClient, user_id: str, messages: list) -> str:
    ret = m.add(messages, user_id=user_id, async_mode=True)
    return "mock memory"


@app.entrypoint
async def run(payload: dict, headers: dict) -> str:
    prompt = payload["prompt"]
    user_id = headers["user_id"]
    session_id = headers["session_id"]

    messages = [
        {"role": "assistant", "content": "你好呀！能先告诉我你叫什么名字吗？"},
        {"role": "user", "content": "我叫李明。今年30岁了。"},
        {"role": "assistant", "content": "很高兴认识你，李明！看您资料是来自北京对吧？为了能更好地为您服务，想了解一下您的饮食偏好，比如您吃辣吗？"},
        {"role": "user", "content": "是休闲旅游。我穿衣嘛，平时基本都穿黑色或灰色的衣服，比较喜欢简约休闲的风格，舒服最重要。"}
    ]


    #response = await runner.run(messages=prompt, user_id=user_id, session_id=session_id)
    
    for i in range(100, 201):
        user_id = f"user-{i}"
        start = asyncio.get_event_loop().time()
        response = await add_memory(m, user_id, messages)
        elapsed = asyncio.get_event_loop().time() - start

        logger.info(f"write memory with prompt: {prompt}, user_id: {user_id}, session_id: {session_id}, elapsed: {elapsed:.3f}s")
        await asyncio.sleep(0.1)
    
    response = "all"    
    logger.info(f"Run response: {response}")
    return response


@app.ping
def ping() -> str:
    return "pong!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
