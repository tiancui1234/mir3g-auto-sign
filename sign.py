
import requests
import os
from requests.exceptions import RequestException

# 固定配置（从HTML提取，已精准配置，无需修改）
SIGN_URL = "http://115.190.97.157/?sessionid="  # 表单提交地址
REQUEST_METHOD = "POST"  # 表单提交方式
# 表单参数（name与HTML输入框完全一致）
FORM_DATA = {
    "userid": os.getenv("GAME_ACCOUNT"),  # 游戏账号（对应userid）
    "charname": os.getenv("ROLE_NAME")    # 角色名（对应charname）
}
# 必要请求头（模拟浏览器，避免被拦截）
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "http://115.190.97.157/?sessionid=",
    "Origin": "http://115.190.97.157",
    "Content-Type": "application/x-www-form-urlencoded"
}

def auto_sign():
    """自动签到核心函数"""
    try:
        # 发送POST签到请求
        response = requests.post(
            url=SIGN_URL,
            data=FORM_DATA,
            headers=HEADERS,
            timeout=15,
            allow_redirects=True  # 允许重定向（部分网站签到后跳转）
        )
        # 验证请求是否成功
        response.raise_for_status()
        print(f"✅ 签到请求发送成功，HTTP状态码：{response.status_code}")
        print(f"📝 响应内容预览：{response.text[:500]}")  # 打印前500字符，方便排查

        # 通用签到成功判断（适配大部分简单表单）
        if response.status_code in [200, 302]:
            print("🎉 今日签到操作完成！（页面无明确成功提示，按状态码判定）")
        else:
            print("⚠️ 签到状态未知，HTTP状态码非200/302")

    except RequestException as e:
        print(f"❌ 签到失败，错误信息：{str(e)}")
        raise SystemExit(1)  # 抛出错误，GitHub Actions标记为失败

if __name__ == "__main__":
    # 校验环境变量是否配置（防止漏填账号/角色名）
    game_account = os.getenv("GAME_ACCOUNT")
    role_name = os.getenv("ROLE_NAME")
    if not game_account or not role_name:
        print("❌ 错误：未配置GAME_ACCOUNT或ROLE_NAME环境变量")
        raise SystemExit(1)
    # 执行签到
    auto_sign()
