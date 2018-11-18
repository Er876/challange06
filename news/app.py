#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import json
from flask import Flask, render_template, abort

app = Flask(__name__)

class Files(object):

    directory = os.path.normpath(os.path.join(
        os.path.dirname(__file__), '..', 'files'))

    def __init__(self):
        self._files = self._read_all_files()

    def _read_all_files(self):
        result = {}
        for filename in os.listdir(self.directory):
            file_path = os.path.join(self.directory, filename)
            with open(file_path) as f:
                result[filename[:-5]] = json.load(f)
        return result

    def get_title_list(self):
        return [item['title'] for item in self._files.values()]

    def get_by_filename(self, filename):
        return self._files.get(filename)

files = Files()

@app.route('/')
def index():
    # 显示文章名称的列表
    return render_template('index.html', title_list=files.get_title_list())
    # 也就是 /home/shiyanlou/files/ 目录下所有 json 文件中的 'title' 信息列表

@app.route('/files/<filename>')
def file(filename):
    # 读取并显示 filename.json 中的文章内容
    file_item = files.get_by_filename(filename)
    if not file_item:
        abort(404)
    return render_template('file.html', file_item=file_item)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
    # 例如 filename='helloworld' 的时候显示 helloworld.json 中的内容
    # 如果 filename 不存在，则显示包含字符串 'shiyanlou 404' 的错误页面

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=True)
