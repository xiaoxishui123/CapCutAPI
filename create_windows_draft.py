#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from create_draft import create_draft
from save_draft_impl import save_draft_impl
import json
import uuid
import platform

def create_windows_draft(width=1080, height=1920):
    """创建专门为Windows系统优化的草稿"""
    print("=== 创建Windows系统草稿 ===")
    
    try:
        # 1. 创建基础草稿
        print("📝 创建基础草稿...")
        script, draft_id = create_draft(width=width, height=height)
        print(f"✅ 草稿创建成功: {draft_id}")
        
        # 2. 修改平台信息为Windows
        print("🖥️ 修改平台信息为Windows...")
        
        # 生成Windows平台信息
        windows_platform = {
            "app_id": 3704,
            "app_source": "lv",
            "app_version": "5.9.0",
            "device_id": str(uuid.uuid4()).replace("-", "")[:32],
            "hard_disk_id": str(uuid.uuid4()).replace("-", "")[:32],
            "mac_address": str(uuid.uuid4()).replace("-", "")[:32],
            "os": "windows",
            "os_version": "10.0.19045"  # Windows 10 版本
        }
        
        # 修改草稿内容
        script.content["last_modified_platform"] = windows_platform
        script.content["platform"] = windows_platform
        
        # 3. 保存草稿
        print("💾 保存Windows草稿...")
        result = save_draft_impl(draft_id)
        
        if result.get("success"):
            draft_url = result.get("draft_url", "")
            print(f"✅ Windows草稿保存成功!")
            print(f"📎 下载URL: {draft_url}")
            
            # 4. 验证平台信息
            print("🔍 验证平台信息...")
            zip_path = f"./tmp/zip/{draft_id}.zip"
            if os.path.exists(zip_path):
                import zipfile
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    draft_info = json.loads(zip_ref.read('draft_info.json'))
                    platform_info = draft_info.get('platform', {})
                    print(f"✅ 平台信息: {platform_info.get('os')} {platform_info.get('os_version')}")
            
            return draft_id, draft_url
        else:
            print(f"❌ 草稿保存失败: {result.get('error', '未知错误')}")
            return None, None
            
    except Exception as e:
        print(f"❌ 创建Windows草稿失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None

def create_windows_draft_with_content():
    """创建带内容的Windows草稿"""
    print("=== 创建带内容的Windows草稿 ===")
    
    try:
        # 1. 创建Windows草稿
        draft_id, draft_url = create_windows_draft()
        if not draft_id:
            return None, None
        
        # 2. 添加文本内容
        print("📝 添加文本内容...")
        import requests
        
        text_data = {
            "draft_id": draft_id,
            "text": "Windows系统测试文本",
            "start": 0,
            "end": 5.0,
            "font_size": 60,
            "color": "#FFFFFF",
            "position_x": 0,
            "position_y": -0.5
        }
        
        response = requests.post("http://localhost:9000/add_text", json=text_data)
        if response.status_code == 200:
            print("✅ 文本添加成功")
        else:
            print(f"❌ 文本添加失败: {response.text}")
        
        # 3. 重新保存草稿
        print("💾 重新保存草稿...")
        result = save_draft_impl(draft_id)
        
        if result.get("success"):
            new_draft_url = result.get("draft_url", "")
            print(f"✅ 带内容的Windows草稿保存成功!")
            print(f"📎 下载URL: {new_draft_url}")
            
            return draft_id, new_draft_url
        else:
            print(f"❌ 草稿保存失败: {result.get('error', '未知错误')}")
            return None, None
            
    except Exception as e:
        print(f"❌ 创建带内容的Windows草稿失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None

if __name__ == "__main__":
    print("选择草稿类型:")
    print("1. 空草稿")
    print("2. 带内容的草稿")
    
    choice = input("请输入选择 (1 或 2): ").strip()
    
    if choice == "1":
        draft_id, draft_url = create_windows_draft()
    elif choice == "2":
        draft_id, draft_url = create_windows_draft_with_content()
    else:
        print("❌ 无效选择")
        sys.exit(1)
    
    if draft_id:
        print(f"\n🎉 Windows草稿创建完成！")
        print(f"草稿ID: {draft_id}")
        print(f"下载URL: {draft_url}")
        print(f"本地文件: ./tmp/zip/{draft_id}.zip")
        print(f"\n请在Windows剪映中测试此草稿文件")