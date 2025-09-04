import os
import sys

# 测试导入路径
ROOT = os.path.dirname(os.path.dirname(__file__))
PLUGIN_DIR = os.path.join(ROOT, 'backend', 'plugins', 'pm_agent')
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
if PLUGIN_DIR not in sys.path:
    sys.path.insert(0, PLUGIN_DIR)

# 禁用代理，确保本地请求直连
for key in [
    'HTTP_PROXY', 'HTTPS_PROXY', 'FTP_PROXY',
    'http_proxy', 'https_proxy', 'ftp_proxy'
]:
    os.environ.pop(key, None)

os.environ['NO_PROXY'] = 'localhost,127.0.0.1,0.0.0.0'
