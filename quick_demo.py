#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CapCutAPI 快速演示脚本
这个脚本展示了如何使用CapCutAPI创建一个简单的视频项目
"""

import requests
import json
import time

# API配置
BASE_URL = "http://8.148.70.18:9000"

def print_step(step_num, description):
    """打印步骤信息"""
    print(f"\n🔸 步骤 {step_num}: {description}")
    print("=" * 50)

def make_api_request(endpoint, data=None, method='POST'):
    """发送API请求"""
    url = f"{BASE_URL}/{endpoint}"
    
    try:
        if method == 'GET':
            response = requests.get(url)
        else:
            response = requests.post(url, json=data)
        
        response.raise_for_status()
        result = response.json()
        
        if result.get('success', True):
            print(f"✅ {endpoint} 调用成功")
            return result
        else:
            print(f"❌ {endpoint} 调用失败: {result.get('error', '未知错误')}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求失败: {e}")
        return None
    except json.JSONDecodeError:
        print(f"❌ 响应解析失败")
        return None

def demo_basic_workflow():
    """演示基础工作流程"""
    print("🎬 CapCutAPI 快速演示")
    print("本演示将创建一个包含文本和图片的简单视频项目")
    print("-" * 60)
    
    # 步骤1: 检查API状态
    print_step(1, "检查API服务状态")
    api_info = make_api_request("", method='GET')
    if not api_info:
        print("❌ API服务不可用，请检查服务器状态")
        return False
    
    print(f"📍 服务地址: {api_info.get('base_url', BASE_URL)}")
    print(f"📊 服务状态: {api_info.get('status', '未知')}")
    
    # 步骤2: 创建草稿
    print_step(2, "创建视频草稿")
    draft_data = {
        "draft_name": "演示项目_" + str(int(time.time())),
        "width": 1080,
        "height": 1920  # 竖屏格式
    }
    
    draft_result = make_api_request("create_draft", draft_data)
    if not draft_result:
        return False
    
    draft_id = draft_result["output"]["draft_id"]
    draft_url = draft_result["output"]["draft_url"]
    
    print(f"📝 草稿ID: {draft_id}")
    print(f"🔗 草稿URL: {draft_url}")
    
    # 步骤3: 添加标题文本
    print_step(3, "添加标题文本")
    title_data = {
        "draft_id": draft_id,
        "text": "欢迎使用CapCutAPI！",
        "start": 0,
        "end": 3,
        "font": "HarmonyOS_Sans_SC_Bold",
        "font_color": "#FF4444",
        "font_size": 42.0,
        "track_name": "title_text"
    }
    
    text_result = make_api_request("add_text", title_data)
    if text_result:
        print("✨ 标题文本添加成功")
    
    # 步骤4: 添加内容文本
    print_step(4, "添加内容文本")
    content_data = {
        "draft_id": draft_id,
        "text": "这是一个由API自动生成的视频项目\n支持多行文本显示\n功能强大且易于使用",
        "start": 3,
        "end": 8,
        "font": "HarmonyOS_Sans_SC_Regular",
        "font_color": "#333333",
        "font_size": 28.0,
        "track_name": "content_text"
    }
    
    content_result = make_api_request("add_text", content_data)
    if content_result:
        print("📝 内容文本添加成功")
    
    # 步骤5: 添加背景图片
    print_step(5, "添加背景图片")
    image_data = {
        "draft_id": draft_id,
        "image_url": "https://picsum.photos/1080/1920?random=1",
        "start": 0,
        "end": 10,
        "track_name": "background_image"
    }
    
    image_result = make_api_request("add_image", image_data)
    if image_result:
        print("🖼️ 背景图片添加成功")
    
    # 步骤6: 保存草稿
    print_step(6, "保存草稿到本地")
    save_data = {
        "draft_id": draft_id,
        "draft_folder": "/tmp/capcut_demo"
    }
    
    save_result = make_api_request("save_draft", save_data)
    if save_result:
        print("💾 草稿保存成功")
        print(f"📁 保存位置: /tmp/capcut_demo")
    
    # 完成
    print("\n" + "=" * 60)
    print("🎉 演示完成！")
    print(f"📋 项目摘要:")
    print(f"   - 草稿ID: {draft_id}")
    print(f"   - 包含: 标题文本 + 内容文本 + 背景图片")
    print(f"   - 总时长: 10秒")
    print(f"   - 格式: 竖屏 1080x1920")
    print(f"📂 草稿文件已保存到: /tmp/capcut_demo")
    print(f"🌐 您可以访问 {BASE_URL}/comprehensive-test 进行更多测试")
    
    return True

def demo_get_resources():
    """演示获取可用资源"""
    print("\n🎨 获取可用资源演示")
    print("-" * 30)
    
    # 获取字体列表
    print("📝 获取可用字体列表...")
    fonts_result = make_api_request("get_font_types", method='GET')
    if fonts_result and 'fonts' in fonts_result:
        fonts = fonts_result['fonts']
        print(f"✅ 共找到 {len(fonts)} 种字体")
        print("前10种字体:")
        for font in fonts[:10]:
            print(f"   - {font}")
        if len(fonts) > 10:
            print(f"   ... 还有 {len(fonts) - 10} 种字体")
    
    # 获取转场效果
    print("\n🎬 获取转场效果类型...")
    transition_result = make_api_request("get_transition_types", method='GET')
    if transition_result:
        print("✅ 转场效果获取成功")

def main():
    """主函数"""
    print("🚀 CapCutAPI 快速演示程序")
    print("这个程序将展示CapCutAPI的基本功能")
    
    # 选择演示模式
    print("\n请选择演示模式:")
    print("1. 完整工作流程演示 (推荐)")
    print("2. 获取可用资源演示")
    print("3. 两者都运行")
    
    try:
        choice = input("\n请输入选择 (1-3): ").strip()
        
        if choice == "1":
            demo_basic_workflow()
        elif choice == "2":
            demo_get_resources()
        elif choice == "3":
            success = demo_basic_workflow()
            if success:
                demo_get_resources()
        else:
            print("❌ 无效选择，运行默认演示")
            demo_basic_workflow()
            
    except KeyboardInterrupt:
        print("\n\n👋 演示已取消")
    except Exception as e:
        print(f"\n❌ 演示过程中发生错误: {e}")

if __name__ == "__main__":
    main() 