from flask import Flask, render_template, send_file
import sys
import hashlib
import os

file_info_list= []
file_info_dict = {}

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

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', file_info_list = file_info_list)

@app.route('/<file_hash>')
def get_file(file_hash):
    file_path= file_info_dict.get(file_hash)
    if not file_path:
        return 'file not found', 404
    print('access path: {}'.format(file_path))
    if not os.path.isfile(file_path):
        return 'file not found', 404
    file_name = os.path.basename(file_path)
    return send_file(file_path, as_attachment=True, attachment_filename=file_name, cache_timeout=0)

if __name__ == '__main__':
    init()
    print(file_info_list)
    # debug = True时会导致__main__所在的进程反复重启
    # 而程序参数信息会在重启的时候得不到保存而丢失
    app.run('0.0.0.0', 8081, debug=False)