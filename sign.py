import requests
import os
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

# 固定配置（已适配传奇3G签到系统）
SIGN_URL = "http://115.190.97.157/?sessionid="
FORM_DATA = {
    "userid": os.getenv("GAME_ACCOUNT"),
    "charname": os.getenv("ROLE_NAME")
}
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "http://115.190.97.157/?sessionid=",
    "Origin": "http://115.190.97.157",
    "Content-Type": "application/x-www-form-urlencoded"
}

def auto_sign():
    try:
        # 发送签到请求
        response = requests.post(
            url=SIGN_URL,
            data=FORM_DATA,
            headers=HEADERS,
            timeout=15,
            allow_redirects=True
        )
        response.raise_for_status()
        print(f"✅ 请求发送成功，状态码：{response.status_code}")

        # 解析页面
        soup = BeautifulSoup(response.text, "html.parser")
        sign_card = soup.find("div", id="signCard")

        # ======================================
        # 核心判定：只要出现 success 或 info 都算成功
        # ======================================
        if sign_card:
            classes = sign_card.get("class", [])
            if "success" in classes:
                print("🎉 签到成功：首次签到完成！")
                return
            elif "info" in classes:
                print("🎉 签到成功：今日已签到，无需重复操作！")
                return

        # 不满足上面2种 → 一律判定失败
        print("❌ 签到失败：未识别到有效签到状态！")
        print("📄 页面内容预览：", response.text[:1500])
        raise SystemExit(1)

    except RequestException as e:
        print(f"❌ 签到失败：网络/请求异常 → {str(e)}")
        raise SystemExit(1)

if __name__ == "__main__":
    acc = os.getenv("GAME_ACCOUNT")
    role = os.getenv("ROLE_NAME")
    if not acc or not role:
        print("❌ 错误：未配置账号或角色名")
        raise SystemExit(1)
    auto_sign()
