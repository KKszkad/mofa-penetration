from mofa.agent_build.base.base_agent import MofaAgent, run_agent
from openai import OpenAI
import json, configparser
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
    config = configparser.ConfigParser()
    config.read('settings.ini')
    llm_base_url = config.get('llm-api', 'base-url')
    llm_api_key = config.get('llm-api', 'api-key')
    llm_model = config.get('llm-api', 'model')

    client = OpenAI(api_key=llm_api_key, base_url=llm_base_url)
    response = client.chat.completions.create(
        model=llm_model,
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
