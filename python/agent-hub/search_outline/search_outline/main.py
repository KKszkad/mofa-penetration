from mofa.agent_build.base.base_agent import MofaAgent, run_agent

def process():
    return "获取网页概览信息"

@run_agent
def run(agent:MofaAgent):
    plan = agent.receive_parameter('plan')
    # TODO: 在下面添加你的Agent代码,其中agent_inputs是你的Agent的需要输入的参数
    agent_output_name = 'web_page_outline'
    search_outline = process()
    agent.send_output(agent_output_name=agent_output_name,agent_result=search_outline)
def main():
    agent = MofaAgent(agent_name='search_outline')
    run(agent=agent)
if __name__ == "__main__":
    main()
