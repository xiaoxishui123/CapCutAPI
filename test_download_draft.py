#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from create_draft import create_draft
from save_draft_impl import save_draft_impl
import logging
import time
import requests
import zipfile
import tempfile

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_and_check_draft():
    """创建草稿，下载并检查文件结构"""
    print("=== 草稿下载和检查测试 ===")
    
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
                
                # 步骤3：下载草稿文件
                print("\n⬇️ 步骤3：下载草稿文件...")
                try:
                    response = requests.get(draft_url, timeout=30)
                    response.raise_for_status()
                    
                    # 保存到临时文件
                    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as f:
                        f.write(response.content)
                        zip_path = f.name
                    
                    print(f"✅ 下载成功，保存到: {zip_path}")
                    
                    # 步骤4：解压并检查文件结构
                    print("\n📁 步骤4：解压并检查文件结构...")
                    extract_dir = f"./extracted_{draft_id}"
                    
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(extract_dir)
                    
                    print(f"✅ 解压成功，目录: {extract_dir}")
                    
                    # 检查文件结构
                    if os.path.exists(extract_dir):
                        files = os.listdir(extract_dir)
                        print(f"📋 文件列表: {files}")
                        
                        # 检查关键文件
                        key_files = ['draft_content.json', 'draft_info.json', 'draft_meta_info.json']
                        missing_files = []
                        
                        for key_file in key_files:
                            file_path = os.path.join(extract_dir, key_file)
                            if os.path.exists(file_path):
                                size = os.path.getsize(file_path)
                                print(f"✅ {key_file} 存在 (大小: {size} 字节)")
                                
                                # 如果是draft_content.json，显示内容
                                if key_file == 'draft_content.json':
                                    try:
                                        with open(file_path, 'r', encoding='utf-8') as f:
                                            content = f.read(500)
                                            print(f"   内容预览: {content[:200]}...")
                                    except Exception as e:
                                        print(f"   读取失败: {e}")
                            else:
                                print(f"❌ {key_file} 不存在")
                                missing_files.append(key_file)
                        
                        if missing_files:
                            print(f"\n⚠️ 缺少关键文件: {missing_files}")
                            print("这可能是剪映无法识别草稿的原因")
                        else:
                            print(f"\n✅ 所有关键文件都存在，草稿结构完整")
                            
                        # 清理临时文件
                        os.unlink(zip_path)
                        shutil.rmtree(extract_dir)
                        
                    else:
                        print(f"❌ 解压目录不存在: {extract_dir}")
                        
                except Exception as e:
                    print(f"❌ 下载或解压失败: {str(e)}")
                    logger.error(f"下载或解压失败", exc_info=True)
            else:
                print("✅ 草稿保存成功! (本地模式，无draft_url)")
        else:
            print(f"❌ 草稿保存失败: {result.get('error', '未知错误')}")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        logger.error(f"测试失败", exc_info=True)

if __name__ == "__main__":
    import shutil
    print("开始草稿下载和检查测试...\n")
    download_and_check_draft() 