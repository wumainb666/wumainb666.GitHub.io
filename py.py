import http.server
import socketserver

# 定义服务器端口
PORT = 8080

# 创建一个简单的 HTTP 请求处理程序
Handler = http.server.SimpleHTTPRequestHandler

# 启动服务器
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"服务器正在运行，监听地址为 127.0.0.1:{PORT}，公网访问地址为 http://likjhfqwlkjfqajp.w1.luyouxia.net")
    httpd.serve_forever()