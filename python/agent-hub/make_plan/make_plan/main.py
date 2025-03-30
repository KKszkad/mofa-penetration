from mofa.agent_build.base.base_agent import MofaAgent, run_agent
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
def process(query):

    # load_dotenv('.env.secret')

    # client = OpenAI(
    #     api_key=os.getenv('[API-KEY]'),
    #     base_url=os.getenv('[API-URL]')
    # )
    client = OpenAI(
        api_key ='sk-7a27f1c4d52c46409ddcc83418d59f0a',
        base_url = 'https://api.deepseek.com'
    )

    system_prompt = """
    用户向搜索引擎输入了搜索词，请分析用户的搜索意图，此部分为schedule，并给出三条拓展、优化过后的搜索词，可以使用搜索引擎的特殊语法，此部分为search_words。
    输出请严格按照给定格式。

    输入示例：
    如何变强

    输出示例：
    {
    "schedule": "用户可能正在寻找提升自身能力、技能或身体素质的方法，可能涉及个人成长、健身、学习技巧等方面。",
    "search_words": [
        "如何快速提升个人能力",
        "健身增肌训练计划",
        "高效学习方法与技巧"
    ]
    }

    """
    # model=os.getenv('[LLM-MODEL]'),
    response = client.chat.completions.create(
        model='deepseek-chat',
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ],
        stream=False
    )
    return response.choices[0].message.content





@run_agent
def run(agent:MofaAgent):
    query = agent.receive_parameter('query')
    
    # TODO: 在下面添加你的Agent代码,其中agent_inputs是你的Agent的需要输入的参数
    agent_output_name = 'plan'
    plan = process(query)

    agent.send_output(agent_output_name=agent_output_name,agent_result=plan)
def main():
    agent = MofaAgent(agent_name='make_plan')
    run(agent=agent)
if __name__ == "__main__":
    main()
