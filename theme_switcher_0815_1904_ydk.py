# 代码生成时间: 2025-08-15 19:04:40
#!/usr/bin/env python

"""
主题切换功能实现
使用Bottle框架实现一个简单的Web应用程序，允许用户切换主题。
"""

from bottle import route, run, request, response, template

# 定义主题列表
themes = ["light", "dark", "blue"]

@route('/')
def index():
    """
    主页路由，显示当前主题和切换选项。
    """
    current_theme = request.get_cookie("theme", "light")  # 默认主题为light
    return template(
        "Switch theme: {{theme}}

<a href="/set_theme/{{theme}}">Switch to {theme}</a>",
        {
            "theme": current_theme
        }
    )

@route('/set_theme/<theme:"light|dark|blue">')
def set_theme(theme):
    """
    设置主题的路由，接受一个主题参数并设置cookie。
    """
    if theme in themes:
        response.set_cookie("theme", theme)
        return f"Theme set to {theme}"
    else:
        return "Invalid theme", 400  # 返回400错误

if __name__ == '__main__':
    # 运行服务器在localhost:8080
    run(host='localhost', port=8080, debug=True)
