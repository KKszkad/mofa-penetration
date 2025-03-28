from mofa.agent_build.base.base_agent import MofaAgent, run_agent

    # outputs:
    # - conclusion
    # inputs:
    #   query: terminal-input/data
    #   plan: make_plan/plan
    #   web_page_content: check_content/web_page_content

def process():
    return '最终的响应'

@run_agent
def run(agent:MofaAgent):
    query = agent.receive_parameter('query')
    plan = agent.receive_parameter('plan')
    web_page_content = agent.receive_parameter('web_page_content')

    # TODO: 在下面添加你的Agent代码,其中agent_inputs是你的Agent的需要输入的参数
    agent_output_name = 'conclusion'
    conclusion = process()
    agent.send_output(agent_output_name=agent_output_name,agent_result=conclusion)
def main():
    agent = MofaAgent(agent_name='conclude_result')
    run(agent=agent)
if __name__ == "__main__":
    main()
