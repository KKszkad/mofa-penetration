from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
import json

def process(plan):
    
    #！ 此处使用本地部署的searXNG元搜索引擎
    searxng_url = 'http://127.0.0.1:4567'
    plan_json = json.loads(plan)
    # 拼接大模型帮助生成的搜索词，保证全面,采用or来连接。
    query = ' or '.join(plan_json['search_words'])
    params = {
        'q': query,
        'format': 'json',
        'language': 'zh',
        'pageno': 1
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    try:
        response = requests.get(searxng_url, params=params, headers=headers)
        response.raise_for_status()
        all_data = response.json()
        
        #提取搜索引擎响应中的有用的信息
        outlines = []
        for data in all_data.get('results', []):
            item = {
                'title': data.get('title'),
                'url': data.get('url'),
                'content': data.get('content')
            }
            outlines.append(item)

        #为了格式规范，将数据封装到json中。    
        outlines_json = {
            'outlines': outlines
        }
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP错误发生: {http_err}')
    except Exception as err:
        print(f'其他错误发生: {err}')
    return outlines_json

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
