本项目仅供参考学习。用于主动获取网易云歌单的必要信息。

### 配置方式

到 `utils/` 下按照 `exmaple.json` 创建自己的 `config.json`。然后运行 `songs_list_info.py`。

### 可能会出现的问题

- 如果没有安装过 `npm`，需要下。
- 如果没有用 `npm` 安装过 _crypto-js_ 这个库，需要 `npm install -g crypto-js`。
- 可能随时间更新，本项目会失效。不过这可以抽时间出来重新逆。
- 如果报了找不到 `Crypto` 的错，则 `/path/to/venv/pip install pycryptodome`。

### TODO

- 解析命令行参数从而完成一次配置。