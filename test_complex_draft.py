#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from create_draft import create_draft
from save_draft_impl import save_draft_impl
import requests
import json

def test_complex_draft():
    """测试创建带内容的复杂草稿"""
    print("=== 复杂草稿测试 ===")
    
    try:
        # 1. 创建草稿
        print("📝 创建草稿...")
        script, draft_id = create_draft(width=1080, height=1920)
        print(f"✅ 草稿创建成功: {draft_id}")
        
        # 2. 添加文本内容
        print("📝 添加文本内容...")
        text_data = {
            "draft_id": draft_id,
            "text": "这是一个测试文本",
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
        
        # 3. 保存草稿
        print("💾 保存草稿...")
        result = save_draft_impl(draft_id)
        
        if result.get("success"):
            draft_url = result.get("draft_url", "")
            print(f"✅ 草稿保存成功!")
            print(f"📎 下载URL: {draft_url}")
            
            # 4. 显示草稿信息
            print("\n📋 草稿信息:")
            print(f"草稿ID: {draft_id}")
            print(f"下载URL: {draft_url}")
            print(f"本地文件: ./tmp/zip/{draft_id}.zip")
            
            return draft_id, draft_url
        else:
            print(f"❌ 草稿保存失败: {result.get('error', '未知错误')}")
            return None, None
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None

if __name__ == "__main__":
    draft_id, draft_url = test_complex_draft()
    if draft_id:
        print(f"\n🎉 测试完成！")
        print(f"请在剪映中测试草稿: {draft_url}") 