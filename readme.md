# 自动获取谷歌学术Bibtex引用

需要安装chrome 和 chromedriver

然后Python模拟点击搜索框，输入关键词，点击搜索，点击引用，点击Bibtex，获取Bibtex引用，保存到本地。

windows环境适用

## chrome 浏览器114版下载安装(默认路径)
> https://dl.google.com/release2/chrome/ackrdjaxyfituopzhu56unhz6weq_114.0.5735.91/114.0.5735.91_chrome_installer.exe

## chromedriver下载

直接在本仓库中下载chromedriver.exe即可。

## 安装依赖
> pip install selenium   
pip install drivers

## 准备论文标题文件
创建一个文件夹，并放入论文标题文件，文件名格式为：references.json。

json文件格式：
```json
[
    {
        "id": 1,
        "title": "GPT-4 Technical Report"
    },
    {
        "id": 2,
        "title": "Palm 2 technical report"
    }
]
```

直接丢给GPT所有的参考文献，让它生成所有参考文献的这个json格式就行

## 运行代码

代码中将默认的chromedriver.exe路径改为本地下载的chromedriver.exe路径。

其中`chrome_options.add_argument ("--headless")`表示不显示浏览器窗口，注释掉后，将显示浏览器窗口。

设置代理，让浏览器访问谷歌学术：`proxy = "http://127.0.0.1:7890"` 

安装需要的包后，运行代码即可。

`python main.py`

## 可能的问题

谷歌学术会弹出验证码，验证是否人类。反爬机制没辙，不要修改time.sleep()时间。时间短了，会被封ip。

出来验证码后，手动点几次就好了，判断为人类了就好了。
