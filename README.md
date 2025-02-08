本项目以供参考学习，用于主动从网易云后端fetch到歌单的必要信息。

### 配置方式

到 `utils/` 下按照 `exmaple.json` 创建自己的 `config.json`。创建完成并配好环境后，如果：

- 若运行于命令行，则提供 `--user=` 参数以获取必要的信息或者直接按格式，使用默认的 `user1` 而执行以下命令；

```shell
$ python3 song_list_info.py --user=user1
```

- 若运行于 pycharm，视需求而调整 `utils/args_loader.py` 里头 `--songlist-author, --login-dummy` 中的 default 域。然后执行/调试。
    - 或阅读 [官方文档](https://docs.python.org/3/library/argparse.html#parents) 等在线文档并上手实验。

项目内某些程序运行时会读写 `config.json`。除非读者知道自己在做什么，最好不要临时修改其中的内容。

### 可能会出现的问题

- 如果没有安装过 `npm`，需要下并配置好 `config.json`。
- 如果没有用 `npm` 安装过 _crypto-js_ 这个库，需要 `npm install -g crypto-js`。
- 可能随时间更新，本项目会失效。不过这可以抽时间出来重新逆。
- 如果运行时报了缺少包，如找不到 `Crypto` 的错，则 `/path/to/venv/pip install pycryptodome` 逐个下载。不过还是建议直接建一个虚拟环境或者用 pycharm，能省很多事。
- 如果想直接运行某个程序而报模块 `utils` 找不到的错，比如要运行 `multifn/update_song_list_cnt.py`，但

```shell
$ python update_song_list_cnt.py
Traceback (most recent call last):
line 35, in <module>
    from utils.json_paser import PRIVATE_CONFIG
ModuleNotFoundError: No module named 'utils'
```
  - **在工程目录下**（即songs_list_info.py所在的目录下）开命令行，按下述命令将 `update_song_list_cnt` 加载成模块后传参就能执行。其它同理不再赘述。
```shell
$ python -m multifn.update_song_list_cnt --author=user2 --dummy=user2
```

如果做完这些还有错误，Unix类系统考虑更新。

实在没有办法解决的，就过来提 issues 和 pr 让大家看看。

### TODO

看时间、心情和兴趣做其它方向的逆。比如手机上能看某首歌的红心数量，但web端和桌面应用看不见。
