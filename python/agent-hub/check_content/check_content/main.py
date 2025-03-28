from mofa.agent_build.base.base_agent import MofaAgent, run_agent

    # outputs:
    # # - web_page_content
    # - deduction
    # inputs:
    #   query: terminal-input/data
    #   plan: make_plan/plan
    #   web_page_outline: search_outline/web_page_outline

def process():
    return ['推断信息','网页内容']

@run_agent
def run(agent:MofaAgent):
    query = agent.receive_parameter('query')
    plan = agent.receive_parameter('plan')
    web_page_outline = agent.receive_parameter('web_page_outline')
    # TODO: 在下面添加你的Agent代码,其中agent_inputs是你的Agent的需要输入的参数
    agent_output_name = ['deduction','web_page_content']
    deduction = process()[0]
    web_page_content = process()[1]
    agent.send_output(agent_output_name=agent_output_name[0],agent_result=deduction)
    agent.send_output(agent_output_name=agent_output_name[1],agent_result=web_page_content)
    web_page_content
    agent.send_output()
def main():
    agent = MofaAgent(agent_name='check-content')
    run(agent=agent)
if __name__ == "__main__":
    main()
