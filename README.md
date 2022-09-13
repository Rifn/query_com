# 通过爬取企查查网站批量获取企业基本信息的桌面小工具

#使用说明
[GitHub源代码地址](https://github.com/Rifn/query_com)

## 1、文件介绍
- **qcc**.py:  用 python 代码写的主程序，将使用代码的爬虫程序转化为可以用鼠标键盘操作的可视化界面，使用 *PyQt* 的窗体、标签、文本框、按钮、资源访问等控件构成；

- **tool.**py:  主程序 *qcc.py* 调用的脚本，封装了 *request* 查询与 *BeautifulSoup* 网页解析，并保存为 *DataFrame* 数据结构的方法； 

- **qcc.**ui:  使用 *PyQt Desinger* 设计的动态 *ui* 文件；

- **setting**.json: 用于实时更新企查查网站登录 ***账号*** 与 ***密码***，以及 ***代理*** 与 ***cookie*** 的 *json* 文件；

- **rifn**.png: 主窗体的图标；

- **rifn2**.ico: 发布桌面程序的图标；

- **demo**.txt: 批量查询模式下，导入企业名称的模板，每行为一个公司名称，末尾空一行；

- **企查查工具更新代理和cookie**.pdf: 更新配置页面的详细操作步骤；

# 2、配置环境

- Python 3.7

- Pandas 1.4.3

- request 2.26.0

- PyQt5 5.15.4

# 3、发布成为桌面程序
### 3.1 安装 pyinstaller
通过以下代码安装：
> pip install pyinstaller

### 3.2 发布程序
然后将在 *qcc.py* 所在的工作目录打开终端（保证所有文件都在该目录下），输入以下代码：
> pyinstaller qcc.py --noconsole --hidden-import PyQt.QtXml --icon="rifn2.ico"
### 3.3 所需文件拖入可执行文件目录
将 *qcc.ui* 、*rifn.png* 、*setting.json* 三个文件拖入 *dist/qcc/* 下即可

# 4、使用步骤
### 4.1 更新配置信息
在程序的配置页面更新配置，具体操作说明见 ***企查查工具更新代理和cookie***.*pdf*，页面如下所示：
![配置页面](https://wx4.sinaimg.cn/mw2000/83129e77gy1h64pbzhhp3j216e0trh2g.jpg)
![配置页面2](https://wx4.sinaimg.cn/mw2000/83129e77gy1h64pc0bsxpj216e0tr19r.jpg)
### 4.2 两种查询模式
- **单个查询**： 直接输入公司名称，然后点击单个查询即可。若查询成功，控制台会更新查询到的信息，然后可转至数据页面导出数据（csv或者xlsx）

- **批量查询**： 点击 **导入查询公司(.txt)** 按钮导入查询公司名称，一个公司名称占一行，末尾空一行，可以直接从 excel 列表复制到记事本生成

### 4.3 导出查询到的数据
将页面切换至 **数据** 页，然后点击导出为 csv 或 xlsx格式



