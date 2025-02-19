import os
from flask import Flask, send_file, render_template_string, abort
from markupsafe import escape
import logging

# 配置日志
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
# 假设 HTML 文件所在的文件夹名为 html_folder，你可以根据实际情况修改
html_folder = os.getenv('HTML_FOLDER', '.')


def is_safe_path(basedir, path):
    abs_basedir = os.path.abspath(basedir)
    abs_path = os.path.abspath(os.path.join(basedir, path))
    return abs_path.startswith(abs_basedir)


@app.route('/')
def list_html_files():  
    try:
        html_files = [f for f in os.listdir(html_folder) if f.endswith('.html')]
        html_links = [f'<a href="/{escape(file)}">{escape(file)}</a><br>' for file in html_files]
        page_content = '<h1>Available HTML Files</h1>' + ''.join(html_links)
        return page_content
    except OSError as e:
        logging.error(f"Error listing files: {str(e)}")
        abort(500, f"Error listing files: {str(e)}")


@app.route('/<filename>')
def serve_html_file(filename):
    if filename.endswith('.html'):
        file_path = os.path.join(html_folder, filename)
        if is_safe_path(html_folder, file_path) and os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    html_content = file.read()
                return render_template_string(html_content)
            except OSError as e:
                logging.error(f"Error reading file: {str(e)}")
                abort(500, f"Error reading file: {str(e)}")
    return "File not found", 404


@app.errorhandler(500)
def internal_error(error):
    logging.error(f"Internal Server Error: {error}")
    return "Internal Server Error", 500


if __name__ == '__main__':
    # 监听所有网络接口，使用 8080 端口
    app.run(host='0.0.0.0', port=8080, debug=True)