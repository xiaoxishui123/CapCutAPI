#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from settings.local import IS_UPLOAD_DRAFT
from create_draft import create_draft
from save_draft_impl import save_draft_impl
import logging
import time

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_complete_workflow():
    """测试完整的工作流程：创建草稿 -> 保存草稿 -> 生成draft_url"""
    print("=== 完整工作流程测试 ===")
    print(f"IS_UPLOAD_DRAFT: {IS_UPLOAD_DRAFT}")
    
    if IS_UPLOAD_DRAFT:
        print("✅ OSS上传已启用，将创建草稿并上传到OSS")
    else:
        print("⚠️  OSS上传已禁用，将只创建本地草稿文件")
    
    try:
        # 步骤1：创建草稿
        print("\n📝 步骤1：创建草稿...")
        script, draft_id = create_draft(width=1080, height=1920)
        print(f"✅ 草稿创建成功! draft_id: {draft_id}")
        
        # 步骤2：保存草稿
        print("\n💾 步骤2：保存草稿...")
        result = save_draft_impl(draft_id)
        
        if result.get("success"):
            draft_url = result.get("draft_url", "")
            if draft_url:
                print(f"✅ 草稿保存成功!")
                print(f"📎 draft_url: {draft_url}")
                print(f"🔗 可以直接在剪映中打开此链接")
                return True
            else:
                print("✅ 草稿保存成功! (本地模式，无draft_url)")
                return True
        else:
            print(f"❌ 草稿保存失败: {result.get('error', '未知错误')}")
            return False
            
    except Exception as e:
        print(f"❌ 工作流程测试失败: {str(e)}")
        logger.error(f"工作流程测试失败", exc_info=True)
        return False

if __name__ == "__main__":
    print("开始完整工作流程测试...\n")
    
    success = test_complete_workflow()
    
    if success:
        print("\n🎉 完整工作流程测试通过！")
        if IS_UPLOAD_DRAFT:
            print("💡 草稿文件已上传到OSS，draft_url可以直接在剪映中使用")
        else:
            print("💡 当前为本地模式，草稿文件保存在本地")
    else:
        print("\n❌ 完整工作流程测试失败") 