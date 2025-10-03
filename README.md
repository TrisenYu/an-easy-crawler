本项目仅供参考学习，用于主动从网易云后端fetch到个人歌单的必要信息以供本地掌控。

### 配置方式

确保本地有uv以及网络环境可用。到当前项目所在文件夹中执行下列三条命令。

```shell
$ uv venv # 创建虚拟环境
$ source .venv/bin/activate
$ uv sync # 同步依赖
```

然后到 `configs` 下按照 `exmaple.json` 创建自己的 `config.json`，并视需求修改 `misc_utils/args_loader.py` 中的配置内容。
如果没有安装过 `npm`，需要下并将 `node_modules` 的位置记录到 config.json 内。
  - 如果没有用 `npm` 安装过 _crypto-js_ 这个库，需要 `sudo npm install -g crypto-js`。

在使用uv的情况下，直接通过以下命令运行爬取程序。

```shell
(proj) $ uv run fetch_songslist_info.py
```

- 若运行于命令行，则提供 `--user=` 参数以获取必要的信息或者直接按格式，否则使用默认的 `user1` 并执行以下命令；

```shell
(proj)  $ python3 -m fetch_songslist_info --songslist-author=user1
# 或者在配好配置的前提下
(proj)  $ uv run fetch_songslist_info.py
```
- 若运行于 pycharm，视需求而调整 `misc_utils/args_loader.py` 里头 `--songslist-author, --login-dummy` 中的 default 域。然后执行/调试。
    - 或阅读 [官方文档](https://docs.python.org/3/library/argparse.html#parents) 等在线文档并上手修改和实验。

项目内某些程序在执行时会读写 `config.json`。最好不要临时修改其中的内容，除非读者能保证不会有并发写入的风险。

### 可能会出现的问题

- 如果发现报错但是没输出，请到 `assets/stat/logs/` 下检查当天运行后生成的日志记录。
- 每次commit会调整函数的名称以及逻辑，不保证前后向兼容。
- 不排除过一段时间后因前后端大改导致本项目失效。~~这可以抽时间出来重新逆~~，还是看以后如何吧（沉思）。
- 如果想直接运行某个程序而报模块找不到的错，比如要运行 `multifn/songslist_hit_bot.py`，但出现

```shell
(proj)  $ python3 songslist_hit_bot.py
Traceback (most recent call last):
line 35, in <module>
    from misc_utils.opts.json.conf_reader import PRIVATE_CONFIG
ModuleNotFoundError: No module named 'misc_utils'
```
**在工程目录下**（即fetch_songslist_info.py所在的目录下）开命令行，按下述命令将 `songslist_hit_bot` 加载成模块后传参就能执行。其它同理不再赘述。
```shell
(proj)  $ python3 -m multifn.songslist_hit_bot --author=user1 --dummy=user1

## 或者在linux环境下用bot_hits.sh配置为crontab定时任务
(proj)  $ ./bot_hits.sh -f boot -s user1 -d user1
```

如果做完这些还有错误，优先考虑是否能通过错误信息补充依赖而消除。

实在没有办法解决的，就过来提 issue(s) 和 pr 让大家看看。

### TODO

看时间、心情和兴趣做其它方向的逆向工程。如手机上能看某首歌的红心数量，但web端和桌面应用是看不见的。

### 致谢
排名不区分前后。

- [AST 还原 JavaScript 混淆代码](https://www.52pojie.cn/thread-1744206-1-1.html)
- [crypto-js](https://github.com/crypto-js/crypto-js)
- [python](https://www.python.org/)
