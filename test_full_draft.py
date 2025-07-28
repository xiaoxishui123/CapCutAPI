#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from settings.local import IS_UPLOAD_DRAFT
from save_draft_impl import save_draft_impl
import logging
import time

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_full_draft_creation():
    """测试完整的草稿创建功能（包含OSS上传）"""
    print("=== 完整草稿创建测试 ===")
    print(f"IS_UPLOAD_DRAFT: {IS_UPLOAD_DRAFT}")
    
    if IS_UPLOAD_DRAFT:
        print("✅ OSS上传已启用，将创建草稿并上传到OSS")
    else:
        print("⚠️  OSS上传已禁用，将只创建本地草稿文件")
    
    # 创建一个测试草稿ID
    test_draft_id = "test_draft_" + str(int(time.time()))
    
    try:
        print(f"开始创建测试草稿: {test_draft_id}")
        result = save_draft_impl(test_draft_id)
        
        if result.get("success"):
            draft_url = result.get("draft_url", "")
            if draft_url:
                print(f"✅ 草稿创建成功!")
                print(f"📎 draft_url: {draft_url}")
                print(f"🔗 可以直接在剪映中打开此链接")
            else:
                print("✅ 草稿创建成功! (本地模式，无draft_url)")
            return True
        else:
            print(f"❌ 草稿创建失败: {result.get('error', '未知错误')}")
            return False
            
    except Exception as e:
        print(f"❌ 草稿创建测试失败: {str(e)}")
        logger.error(f"草稿创建测试失败", exc_info=True)
        return False

if __name__ == "__main__":
    print("开始完整草稿创建功能测试...\n")
    
    success = test_full_draft_creation()
    
    if success:
        print("\n🎉 草稿创建功能测试通过！")
        if IS_UPLOAD_DRAFT:
            print("💡 草稿文件已上传到OSS，draft_url可以直接在剪映中使用")
        else:
            print("💡 当前为本地模式，草稿文件保存在本地")
    else:
        print("\n❌ 草稿创建功能测试失败") 