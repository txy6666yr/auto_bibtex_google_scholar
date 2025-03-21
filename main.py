from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import pandas as pd

# 随机 User-Agent 列表
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0",
]

# 随机选择一个 User-Agent
user_agent = random.choice(user_agents)

# 配置 WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_argument(f"user-agent={user_agent}")
# 无头模式
# chrome_options.add_argument("--headless")

# 添加代理 IP，这里只是示例，需要替换为真实可用的代理
proxy = "http://127.0.0.1:7890"
chrome_options.add_argument(f"--proxy-server={proxy}")

service = Service(
    "C:/Users/txy/.wdm/drivers/chromedriver/win64/114.0.5735.90/chromedriver.exe"
)
driver = webdriver.Chrome(service=service, options=chrome_options)


def get_bibtex(paper_title):
    max_retries = 3
    retries = 0
    while retries < max_retries:
        try:
            driver.get("https://scholar.google.com/")
            # 随机延迟
            time.sleep(random.uniform(2, 5))

            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            print("正在搜索：", paper_title)
            search_box.send_keys(paper_title + Keys.RETURN)

            # 随机延迟
            time.sleep(random.uniform(2, 5))

            # 等待结果加载
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.gs_ri"))
            )

            # 点击第一个搜索结果的引用按钮
            print("正在点击引用按钮：", paper_title)
            cite_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "(//div[contains(@class,'gs_fl')]//a[.//span[text()='引用']])[1]",
                    )
                )
            )
            driver.execute_script("arguments[0].click();", cite_button)

            # 随机延迟
            time.sleep(random.uniform(2, 5))

            # 方案一：使用文本精准匹配
            print("正在点击Bibtex按钮...")
            bibtex_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@id='gs_citi']/a[text()='BibTeX']")
                )
            )
            # 直接导航到BibTeX页面
            print("正在进入bibtex页面...")
            bibtex_url = bibtex_link.get_attribute("href")
            driver.get(bibtex_url)

            # 随机延迟
            time.sleep(random.uniform(2, 5))

            # 获取内容
            bibtex_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "pre"))
            )
            print("获取bibtex内容成功...")
            return bibtex_element.text

        except Exception as e:
            print(f"尝试第 {retries + 1} 次失败，错误信息: {e}")
            retries += 1
            if retries < max_retries:
                print("刷新页面并重新尝试...")
                driver.refresh()
                time.sleep(random.uniform(2, 5))
            else:
                print("达到最大重试次数，无法获取 BibTeX。")
                return ""


def save_bibtex_from_json(paper_df:pd.DataFrame, bib_file_path):
    try:
        with open(bib_file_path, "w", encoding="utf-8") as bib_file:
            for _, row in paper_df.iterrows():
                bibtex = row.get("bibtex")
                if bibtex:
                    bib_file.write(bibtex + "\n\n")
        print(f"BibTeX 内容已成功保存到 {bib_file_path}")
    except Exception as e:
        print(f"发生未知错误: {e}")


def test():
    # 运行测试
    paper_title = "GPT-4 Technical Report"
    bibtex_result = get_bibtex(paper_title)
    print("获取到的 BibTeX：\n", bibtex_result if bibtex_result else "未找到")

if __name__ == "__main__":

    paper_df = pd.read_json("references.json")
    paper_dict = paper_df.to_dict(orient="records")
    # 修改原dict存入bibtex信息
    results = []
    for paper in paper_dict:
        print(f'正在获取第{paper["id"]}篇论文的BibTeX信息')
        paper["bibtex"] = get_bibtex(paper["title"])
        results.append(paper)
    print("获取BibTeX信息完成")
    paper_df_new = pd.DataFrame(results)
    # 保存为json
    paper_df_new.to_json("references_with_bibtex.json", orient="records", force_ascii=False)
    print("保存为json完成")
    # 保存为bib
    save_bibtex_from_json(paper_df_new, "references.bib")
    print("保存为bib完成")
    driver.quit()
