from curl_cffi import requests
try:
	resp = requests.get('music.163.com')
except Exception as e:
	print(e)
	exit(0)

# TODO: 内嵌 js？这怎么搞？
print(resp.text)