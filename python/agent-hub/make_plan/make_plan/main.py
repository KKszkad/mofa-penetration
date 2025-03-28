from mofa.agent_build.base.base_agent import MofaAgent, run_agent

def process():
    return "预处理用户输入，并制定搜索计划。"

@run_agent
def run(agent:MofaAgent):
    task = agent.receive_parameter('query')
    
    # TODO: 在下面添加你的Agent代码,其中agent_inputs是你的Agent的需要输入的参数
    agent_output_name = 'plan'
    plan = process()

    agent.send_output(agent_output_name=agent_output_name,agent_result=plan)
def main():
    agent = MofaAgent(agent_name='make_plan')
    run(agent=agent)
if __name__ == "__main__":
    main()
