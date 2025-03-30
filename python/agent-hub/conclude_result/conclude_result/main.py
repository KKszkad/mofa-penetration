from mofa.agent_build.base.base_agent import MofaAgent, run_agent
from openai import OpenAI
import json
    # outputs:
    # - conclusion
    # inputs:
    #   query: terminal-input/data
    #   plan: make_plan/plan
    #   web_page_content: check_content/web_page_content

def process(query, plan_str, web_page_content_str):
    web_page_content_json = json.loads(web_page_content_str)    
    plan_json = json.loads(plan_str)

    system_prompt = f"""
    用户正在搜索结果，我们对用户的思路进行了分析({plan_json['schedule']})，
    并增加了搜索词：{plan_json['search_words']}。
    请结合上述目标和主题，以及下述的网页信息。给予用户回答。
    {web_page_content_json}
    """
    client = OpenAI(api_key="sk-7a27f1c4d52c46409ddcc83418d59f0a", base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
            "role": "system", "content":  system_prompt},
            {"role": "user", "content": query},
        ],
        stream=False
    )
    return response.choices[0].message.content

@run_agent
def run(agent:MofaAgent):
    query = agent.receive_parameter('query')
    plan = agent.receive_parameter('plan')
    web_page_content = agent.receive_parameter('web_page_content')

    # TODO: 在下面添加你的Agent代码,其中agent_inputs是你的Agent的需要输入的参数
    agent_output_name = 'conclusion'
    conclusion = process(query, plan, web_page_content)
    agent.send_output(agent_output_name=agent_output_name,agent_result=conclusion)
def main():
    agent = MofaAgent(agent_name='conclude_result')
    run(agent=agent)
if __name__ == "__main__":
    main()
