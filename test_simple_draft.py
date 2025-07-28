#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from create_draft import create_draft
from save_draft_impl import save_draft_impl
import json
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_simple_draft():
    """测试生成一个简单的空草稿"""
    print("=== 测试简单草稿生成 ===")
    
    try:
        # 步骤1：创建草稿
        print("\n📝 步骤1：创建草稿...")
        script, draft_id = create_draft(width=1080, height=1920)
        print(f"✅ 草稿创建成功! draft_id: {draft_id}")
        
        # 检查初始草稿内容
        print(f"\n🔍 检查初始草稿内容...")
        print(f"轨道数量: {len(script.tracks)}")
        print(f"素材数量: {len(script.materials.texts)}")
        
        # 步骤2：保存草稿（不添加任何内容）
        print("\n💾 步骤2：保存草稿...")
        save_result = save_draft_impl(draft_id=draft_id)
        
        if save_result.get("success"):
            print("✅ 草稿保存成功!")
            print(f"📁 草稿文件夹: {draft_id}")
            print(f"🔗 draft_url: {save_result.get('draft_url')}")
            return save_result.get('draft_url')
        else:
            print(f"❌ 草稿保存失败: {save_result}")
            return None
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    draft_url = test_simple_draft()
    if draft_url:
        print(f"\n🎉 测试完成! 新的draft_url: {draft_url}")
    else:
        print("\n❌ 测试失败!") 