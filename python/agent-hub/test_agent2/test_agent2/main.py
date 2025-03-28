from mofa.agent_build.base.base_agent import MofaAgent, run_agent

@run_agent
def run(agent:MofaAgent):
    task = agent.receive_parameter('query')
    tag1 = agent.receive_parameter('tag1')
    # TODO: 在下面添加你的Agent代码,其中agent_inputs是你的Agent的需要输入的参数
    agent_output_name = 'tag2'
    agent.send_output(agent_output_name=agent_output_name,agent_result=task + 'tag2')
def main():
    agent = MofaAgent(agent_name='test_agent2')
    run(agent=agent)
if __name__ == "__main__":
    main()
