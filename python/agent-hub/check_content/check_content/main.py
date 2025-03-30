from mofa.agent_build.base.base_agent import MofaAgent, run_agent
from openai import OpenAI
import json, configparser
import asyncio, re
from crawl4ai import *

# 清除markdown格式的不必要字符和网页的链接以获取较为纯净的数据
def clean_md_text(md_text):
    # 去除 Markdown 链接
    md_text = re.sub(r'\[.*?\]\(.*?\)', '', md_text)
    # 去除标题符号
    md_text = re.sub(r'^#+\s', '', md_text, flags=re.MULTILINE)
    # 去除列表符号
    md_text = re.sub(r'^([-*]|\d+\.)\s', '', md_text, flags=re.MULTILINE)
    # 去除强调符号
    md_text = re.sub(r'(\*\*|__|_|\*)', '', md_text)
    # 去除多余的换行符和空格
    md_text = re.sub(r'\s+', ' ', md_text).strip()
    return md_text

#Crawl4AI抓取网页数据
async def get_pure_page_content(url_str):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url_str,
        )
        pure_content = clean_md_text(result.markdown)
        return pure_content


    # outputs:
    # # - web_page_content
    # - deduction
    # inputs:
    #   query: terminal-input/data
    #   plan: make_plan/plan
    #   web_page_outline: search_outline/web_page_outline

def process(query, plan_str, web_page_outline_str):
    web_page_outline_json = json.loads(web_page_outline_str)
    web_page_outline = web_page_outline_json['outlines']
    plan_json = json.loads(plan_str)
    num_reference = 4

    system_prompt = f"""
    现在用户向搜索引擎输入了[{query}]，我们对用户的思路进行了分析({plan_json['schedule']})，
    并增加了搜索词：{plan_json['search_words']}。
    请结合上述目标和主题，以及下述的网页概览信息，选择最贴合主题的{num_reference}个网页,避免广告。
    ——————
    {web_page_outline}
    ——————
    分析完成后，你应当只输出符合条件的网页在网页概览信息中的位次，使用空格分开。
    ——————
    （假设第1，3，5，7，12个概览为最优选择）
    示例输出：
    1 3 5 7 12
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
            {"role": "user", "content": "帮助用户选择最相关的网页"},
        ],
        stream=False
    )

    content = response.choices[0].message.content
    #TODO 下一步：确定好传输回来的数据
    num_str_list = content.split()
    indexes = [int(num) for num in num_str_list]    #得到目标outline的索引

    #TODO 后续用 目前回传的deduction和web_page_content都是 选定的网页概览信息
    # 获取确定的结果url
    # urls = []
    # for index in indexes:
    #     urls.append(web_page_outline[index - 1]['url'])
    
    # web_page_content = []
    # for url in urls:
    #     web_page_content.append(get_pure_page_content(url))
    result = []
    for index in indexes:
        result.append(web_page_outline[index-1])

    # return web_page_content
    return result

@run_agent
def run(agent:MofaAgent):
    query = agent.receive_parameter('query')
    plan = agent.receive_parameter('plan')
    web_page_outline = agent.receive_parameter('web_page_outline')
    # TODO: 在下面添加你的Agent代码,其中agent_inputs是你的Agent的需要输入的参数
    agent_output_name = ['deduction','web_page_content']

    #TODO 后续爬虫完成后区分两者
    result = process(query, plan, web_page_outline)
    deduction = result
    web_page_content = result

    agent.send_output(agent_output_name=agent_output_name[0],agent_result=deduction)
    agent.send_output(agent_output_name=agent_output_name[1],agent_result=web_page_content)

def main():
    agent = MofaAgent(agent_name='check-content')
    run(agent=agent)
if __name__ == "__main__":
    main()
