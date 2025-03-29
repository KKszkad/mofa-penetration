from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
import json

def process(plan_str):
    
    #！ 此处使用searXNG元搜索引擎
    searxng_url = 'http://127.0.0.1:4567'
    plan_obj = json.loads(plan_str)
    # 拼接大模型帮助生成的搜索词，保证全面,采用or来连接。
    query = ' or '.join(plan_obj['search_words'])
    params = {
        'q': query,
        'format': 'json',
        'language': 'zh',
        'pageno': 1,
        'time_range': 'day',
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    try:
        response = requests.get(searxng_url, params=params, headers=headers)
        response.raise_for_status()
        all_data = response.json()
        
        results = []
        for data in all_data.get('results', []):
            item = {
                'title': data.get('title'),
                'url': data.get('url'),
                'content': data.get('content')
            }
            results.append(item)


        # for result in results.get('results', []):
        #     print(f"标题: {result.get('title')}")
        #     print(f"链接: {result.get('url')}")
        #     print(f"内容: {result.get('content')}")
        #     print('---')
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP错误发生: {http_err}')
    except Exception as err:
        print(f'其他错误发生: {err}')
    return results

@run_agent
def run(agent:MofaAgent):
    plan = agent.receive_parameter('plan')
    # TODO: 在下面添加你的Agent代码,其中agent_inputs是你的Agent的需要输入的参数
    agent_output_name = 'web_page_outline'
    search_outline = process(plan)
    agent.send_output(agent_output_name=agent_output_name,agent_result=search_outline)
def main():
    agent = MofaAgent(agent_name='search_outline')
    run(agent=agent)
if __name__ == "__main__":
    main()
