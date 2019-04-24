#!/usr/bin/env python3

from flask import Flask, render_template, send_file
from jinja2 import FileSystemLoader, Environment, select_autoescape
import importlib
import sys
import hashlib
import os
import argparse
from urllib import parse
import netifaces

file_info_list= []
file_info_dict = {}

try:
    config = importlib.import_module('config')
    template_dir = config.TEMPLATE_DIR
except ModuleNotFoundError:
    template_dir='templates'
loader = FileSystemLoader([template_dir])

app = Flask(__name__)
app.jinja_loader = loader

def init():
    file_list:str = sys.stdin.read().strip()
    file_list:[str] = file_list.split('\n')
    for file_name in file_list:
        key = hashlib.md5(file_name.encode('utf-8')).hexdigest()
        file_info_dict.setdefault(key, file_name)
        file_info_list.append({
            'key': key,
            'file_name': file_name
        })

def get_host_ips()-> [] :
    ips = []
    for iface in netifaces.interfaces():
        adder_info = netifaces.ifaddresses(iface).get(netifaces.AF_INET)
        if adder_info:
            ips.append(adder_info[0]['addr'])
    return ips

def show_addr_msg(ips, port):
    print('请访问以下地址')
    for ip in ips:
        print('http://{}:{}'.format(ip, port))

@app.route('/')
def index():
    return render_template('index.html', file_info_list = file_info_list)

@app.route('/<file_hash>')
def get_file(file_hash):
    file_path= file_info_dict.get(file_hash)
    if not file_path:
        return 'file not found', 404
    abs_dir = os.path.abspath(os.path.curdir)
    abs_file_path = os.path.join(abs_dir, file_path)
    print('access path: {}'.format(abs_file_path))
    if not os.path.isfile(abs_file_path):
        return 'file not found', 404
    file_name = os.path.basename(file_path)
    return send_file(abs_file_path, as_attachment=True, attachment_filename=parse.quote(file_name), cache_timeout=0)

if __name__ == '__main__':
    init()
    # debug = True时会导致__main__所在的进程反复重启
    # 而程序参数信息会在重启的时候得不到保存而丢失
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8080)
    args = parser.parse_args()
    show_addr_msg(get_host_ips(), args.port)

    app.run('0.0.0.0', args.port, debug=False)