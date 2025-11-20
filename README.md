本项目仅供参考学习，用于：
- 主动从网易云后端fetch到个人歌单的必要信息以供本地掌控。
- 针对性获取其它网站的业务所能提供的某类内容（如评论/图片）

### 配置方式

确保本地有uv的环境并保证项目有可用的网络环境。为创建虚拟环境供程序正常执行，到当前项目所在文件夹中执行下列三条命令。

```shell
$ uv venv # 创建虚拟环境
$ source .venv/bin/activate # 激活，windows上直接用 .venv/Scripts/activate
$ uv sync # 同步依赖
```

然后到 `configs` 下按照 `exmaple.json` 创建自己的 `config.json`，并视需求修改 `configs/args_loader.py` 中的配置内容。
如果没有安装过 `npm`，需要下并将 `node_modules` 的位置记录到 config.json 内。
  - 不想拿浏览器看自己的id和歌单的id，可以到APP里找到想要的歌单，然后点分享，再点复制链接，就可以得到url中作为get请求参数的`id=<歌单id>&userid=<你的id>`。
  - 如果没有用 `npm` 安装过 _crypto-js_ 这个库，需要 `sudo npm install -g crypto-js`。

在使用uv的情况下，如要对歌单详情做备份，可直接通过以下命令运行爬取程序。

```shell
(proj) $ uv run fetch_songslist_info.py
```
- 
- 若运行于命令行，则提供 `--user=` 参数以获取必要的信息或者直接按格式，否则使用默认的 `user1` 并执行以下命令；

```shell
# 不太推荐，容易错
(proj)  $ python3 -m fetch_songslist_info --songslist-author=user1
# 或者在配好配置的前提下
(proj)  $ uv run fetch_songslist_info.py
```
- 若运行于 pycharm，视需求而调整 `misc_utils/args_loader.py` 里头 `--songslist-author, --login-dummy` 中的 default 域。然后执行/调试。
    - 或阅读 [官方文档](https://docs.python.org/3/library/argparse.html#parents) 等在线文档并上手修改和实验。

项目内有文件会修改配置。除非读者能保证不会有并发写入的风险，最好不要临时修改`config.json`的内容。

### 可能会遇到/出现的问题

- 如果想尽可能完整地备份但是歌单内的单曲数量超过上千，`fetch_songslist_info.py` 会运行超过10分钟。
  - 如果中途出错的，最好立即**手动**销毁终端并删除`assets/dyn/somg.db.journal`。
  - 如果进度条不动的，最好马上cat日志看看发生什么情况。
- 其它网站的内容获取逻辑在设计上是**有错才输出**。
- 如果发现报错/异常退出但是命令行没输出，到 `assets/stat/logs/` 下检查当天运行后生成的所有日志记录。
- 每次commit会调整函数名/数据库内列名，并分离耦合程度高的逻辑，所以并不能保证做到前后向兼容。
- 不排除过一段时间后因网站混淆前端暴露出的后端接口大改而导致本项目失效。~~即使能抽时间出来重新逆但人的精力总是有限且总容易被一些乱七八糟的事所半途中断~~。
- 如果想直接运行某个程序而报模块找不到的错，比如要运行 `multtp/songslist_hit_bot.py`，但出现

```shell
(proj)  $ python3 songslist_hit_bot.py
Traceback (most recent call last):
line ... in <module>
    from misc_utils.opts.json.conf_reader import PRIVATE_CONFIG
ModuleNotFoundError: No module named 'misc_utils'
```
**在工程目录下**（即fetch_songslist_info.py所在的目录下）开命令行，按下述命令将 `songslist_hit_bot` 加载成模块后传参就能执行。其它同理不再赘述。
```shell
(proj)  $ python3 -m multtp.songslist_hit_bot --author=user1 --dummy=user1

## 或者在linux环境下用bot_hits.sh配置为crontab定时任务
(proj)  $ ./bot_man.sh -f boot -s user1 -d user1
```

如果做完这些还有错误，优先考虑是否能通过错误信息补充依赖而消除。

实在没有办法解决的，就过来提 issue(s) 和 pr 让大家看看。

### 致谢
排名不区分前后，且部分致谢保留于特定实现内此处为偷懒而不再列出。

- [AST 还原 JavaScript 混淆代码](https://www.52pojie.cn/thread-1744206-1-1.html)
- [crypto-js](https://github.com/crypto-js/crypto-js)
- [python](https://www.python.org/)
