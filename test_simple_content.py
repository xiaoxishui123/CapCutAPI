#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from create_draft import create_draft
from add_text_impl import add_text_impl
from save_draft_impl import save_draft_impl
import logging
import time

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_simple_content():
    """测试添加简单文本内容到草稿"""
    print("=== 添加简单内容测试 ===")
    
    try:
        # 步骤1：创建草稿
        print("\n📝 步骤1：创建草稿...")
        script, draft_id = create_draft(width=1080, height=1920)
        print(f"✅ 草稿创建成功! draft_id: {draft_id}")
        
        # 步骤2：添加文本内容
        print("\n📝 步骤2：添加文本内容...")
        text_result = add_text_impl(
            text="Hello World!",
            draft_id=draft_id,
            start=0,
            end=3,  # 3秒显示时间
            font="HarmonyOS_Sans_SC_Regular",
            font_color="#FF0000",
            font_size=30.0,
            track_name="main"
        )
        
        if text_result.get("success"):
            print("✅ 文本添加成功!")
        else:
            print(f"❌ 文本添加失败: {text_result.get('error', '未知错误')}")
            return False
        
        # 步骤3：保存草稿
        print("\n💾 步骤3：保存草稿...")
        result = save_draft_impl(draft_id)
        
        if result.get("success"):
            print("✅ 草稿保存成功!")
            print(f"📁 草稿文件夹: {draft_id}")
            print(f"📋 请将 {draft_id} 文件夹复制到剪映草稿目录")
            return True
        else:
            print(f"❌ 草稿保存失败: {result.get('error', '未知错误')}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        logger.error(f"测试失败", exc_info=True)
        return False

if __name__ == "__main__":
    test_simple_content() 