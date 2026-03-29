import requests
import os
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

# ==================== 固定配置区（无需修改）====================
# 签到接口配置
SIGN_URL = "http://115.190.97.157/?sessionid="
FORM_DATA = {
    "userid": os.getenv("GAME_ACCOUNT"),  # 游戏账号（GitHub Secrets）
    "charname": os.getenv("ROLE_NAME")    # 角色名（GitHub Secrets）
}
# 请求头（模拟浏览器，防止拦截）
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "http://115.190.97.157/?sessionid=",
    "Origin": "http://115.190.97.157",
    "Content-Type": "application/x-www-form-urlencoded"
}
# Server酱配置（从GitHub Secrets读取）
SERVER_CHAN_KEY = os.getenv("SERVER_CHAN_KEY")
# ==============================================================

def send_server_chan(title, content):
    """Server酱（方糖）微信推送函数"""
    if not SERVER_CHAN_KEY:
        print("⚠️ 未配置Server酱SEND_KEY，跳过微信推送")
        return
    try:
        # Server酱官方接口
        url = f"https://sctapi.ftqq.com/{SERVER_CHAN_KEY}.send"
        # 推送参数（title标题，desp正文，支持换行）
        data = {
            "title": title,
            "desp": f"【传奇3G自动签到】\n{content}\n📅 推送时间：{os.popen('date').read().strip()}"
        }
        requests.post(url, data=data, timeout=10)
        print("📤 微信推送成功！消息已发送至你的微信")
    except Exception as e:
        print(f"⚠️ 微信推送失败：{str(e)}")

def auto_sign():
    """核心签到函数"""
    try:
        # 发送签到POST请求
        response = requests.post(
            url=SIGN_URL,
            data=FORM_DATA,
            headers=HEADERS,
            timeout=15,
            allow_redirects=True
        )
        response.raise_for_status()  # 抛出HTTP请求错误（如404/500）
        print(f"✅ 签到请求发送成功，HTTP状态码：{response.status_code}")

        # 解析页面HTML，判断签到状态
        soup = BeautifulSoup(response.text, "html.parser")
        sign_card = soup.find("div", id="signCard")

        # 核心判定规则：success/info都算成功，其他全失败
        if sign_card:
            card_classes = sign_card.get("class", [])
            if "success" in card_classes:
                push_title = "✅ 传奇3G签到成功"
                push_content = "首次签到完成！豪礼已领取～"
                print(f"🎉 {push_content}")
                send_server_chan(push_title, push_content)
                return
            elif "info" in card_classes:
                push_title = "✅ 传奇3G签到成功"
                push_content = "今日已签到，无需重复操作～"
                print(f"🎉 {push_content}")
                send_server_chan(push_title, push_content)
                return

        # 未检测到success/info，判定为失败
        push_title = "❌ 传奇3G签到失败"
        push_content = "未识别到有效签到状态，可能参数错误/页面异常！"
        print(push_content)
        send_server_chan(push_title, push_content)
        raise SystemExit(1)  # 标记Actions运行失败

    # 捕获网络/请求异常（如连接失败、超时）
    except RequestException as e:
        push_title = "❌ 传奇3G签到异常"
        push_content = f"网络/请求错误：{str(e)}"
        print(push_content)
        send_server_chan(push_title, push_content)
        raise SystemExit(1)

if __name__ == "__main__":
    # 校验账号/角色名是否配置
    if not os.getenv("GAME_ACCOUNT") or not os.getenv("ROLE_NAME"):
        print("❌ 错误：未在GitHub Secrets配置GAME_ACCOUNT/ROLE_NAME")
        raise SystemExit(1)
    # 执行签到
    auto_sign()
