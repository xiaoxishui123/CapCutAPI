import requests
import json

# 服务器基础URL
BASE_URL = "http://8.148.70.18:9000"

def test_create_draft():
    """测试创建草稿功能"""
    print("测试创建草稿...")
    url = f"{BASE_URL}/create_draft"
    data = {"draft_name": "测试草稿"}
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            print(f"✓ 草稿创建成功！")
            print(f"  草稿ID: {result['output']['draft_id']}")
            print(f"  草稿URL: {result['output']['draft_url']}")
            return result['output']['draft_id']
        else:
            print(f"✗ 草稿创建失败: {result.get('error')}")
    else:
        print(f"✗ 请求失败，状态码: {response.status_code}")
    return None

def test_add_text(draft_id):
    """测试添加文本功能"""
    print("\n测试添加文本...")
    url = f"{BASE_URL}/add_text"
    data = {
        "draft_id": draft_id,
        "text": "Hello CapCutAPI!",
        "start": 0,
        "end": 3,
        "font": "HarmonyOS_Sans_SC_Regular",
        "font_color": "#FF0000",
        "font_size": 30.0,
        "track_name": "test_text"
    }
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            print("✓ 文本添加成功！")
        else:
            print(f"✗ 文本添加失败: {result.get('error')}")
    else:
        print(f"✗ 请求失败，状态码: {response.status_code}")

def main():
    """主测试函数"""
    print("CapCutAPI 基础功能测试")
    print("=" * 40)
    
    # 测试创建草稿
    draft_id = test_create_draft()
    
    if draft_id:
        # 测试添加文本
        test_add_text(draft_id)
        
        print(f"\n测试完成！")
        print(f"草稿ID: {draft_id}")
        print("您可以使用这个草稿ID进行更多操作。")
    else:
        print("测试失败：无法创建草稿")

if __name__ == "__main__":
    main() 