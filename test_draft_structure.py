#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from create_draft import create_draft
from save_draft_impl import save_draft_impl
import logging
import time
import shutil

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_draft_structure():
    """测试草稿文件结构"""
    print("=== 草稿文件结构测试 ===")
    
    try:
        # 步骤1：创建草稿
        print("\n📝 步骤1：创建草稿...")
        script, draft_id = create_draft(width=1080, height=1920)
        print(f"✅ 草稿创建成功! draft_id: {draft_id}")
        
        # 步骤2：检查草稿文件夹结构（在保存之前）
        print(f"\n📁 步骤2：检查草稿文件夹结构...")
        if os.path.exists(draft_id):
            print(f"草稿文件夹存在: {draft_id}")
            files = os.listdir(draft_id)
            print(f"文件列表: {files}")
            
            # 检查关键文件
            key_files = ['draft_content.json', 'draft_info.json', 'draft_meta_info.json']
            for key_file in key_files:
                file_path = os.path.join(draft_id, key_file)
                if os.path.exists(file_path):
                    print(f"✅ {key_file} 存在")
                    # 显示文件大小
                    size = os.path.getsize(file_path)
                    print(f"   大小: {size} 字节")
                else:
                    print(f"❌ {key_file} 不存在")
        else:
            print(f"❌ 草稿文件夹不存在: {draft_id}")
        
        # 步骤3：保存草稿（但不清理临时文件）
        print(f"\n💾 步骤3：保存草稿...")
        
        # 临时禁用清理，以便检查文件
        original_upload_draft = None
        try:
            from settings.local import IS_UPLOAD_DRAFT
            original_upload_draft = IS_UPLOAD_DRAFT
            
            # 临时设置为False，避免清理文件
            import settings.local
            settings.local.IS_UPLOAD_DRAFT = False
            
            result = save_draft_impl(draft_id)
            
            if result.get("success"):
                print("✅ 草稿保存成功!")
                
                # 再次检查文件结构
                print(f"\n📁 步骤4：保存后的文件结构...")
                if os.path.exists(draft_id):
                    files = os.listdir(draft_id)
                    print(f"文件列表: {files}")
                    
                    # 检查关键文件
                    key_files = ['draft_content.json', 'draft_info.json', 'draft_meta_info.json']
                    for key_file in key_files:
                        file_path = os.path.join(draft_id, key_file)
                        if os.path.exists(file_path):
                            print(f"✅ {key_file} 存在")
                            size = os.path.getsize(file_path)
                            print(f"   大小: {size} 字节")
                            
                            # 如果是draft_content.json，显示部分内容
                            if key_file == 'draft_content.json':
                                try:
                                    with open(file_path, 'r', encoding='utf-8') as f:
                                        content = f.read(200)
                                        print(f"   内容预览: {content[:100]}...")
                                except Exception as e:
                                    print(f"   读取失败: {e}")
                        else:
                            print(f"❌ {key_file} 不存在")
                else:
                    print(f"❌ 草稿文件夹不存在: {draft_id}")
            else:
                print(f"❌ 草稿保存失败: {result.get('error', '未知错误')}")
                
        finally:
            # 恢复原始设置
            if original_upload_draft is not None:
                settings.local.IS_UPLOAD_DRAFT = original_upload_draft
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        logger.error(f"测试失败", exc_info=True)

if __name__ == "__main__":
    print("开始草稿文件结构测试...\n")
    test_draft_structure() 