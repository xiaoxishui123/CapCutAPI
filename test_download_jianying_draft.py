#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import requests
import zipfile
import tempfile
import json
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_and_check_jianying_draft():
    """下载并检查剪映中文版草稿文件结构"""
    print("=== 剪映中文版草稿下载和检查测试 ===")
    
    # 新的draft_url
    draft_url = "http://zdaigfpt.oss-cn-wuhan-lr.aliyuncs.com/dfd_cat_1752795632_1ec07103.zip?OSSAccessKeyId=LTAI5tLhTQGk2Di25ArrkgGG&Expires=1752882032&Signature=OCSl6NZmBKTq5idwSDH95xbdbFo%3D"
    
    try:
        # 步骤1：下载草稿文件
        print(f"\n📥 步骤1：下载草稿文件...")
        print(f"URL: {draft_url}")
        
        response = requests.get(draft_url, stream=True)
        response.raise_for_status()
        
        # 创建临时目录
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, "draft.zip")
        
        # 保存zip文件
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅ 下载成功，文件大小: {os.path.getsize(zip_path)} 字节")
        
        # 步骤2：解压文件
        print(f"\n📁 步骤2：解压文件...")
        extract_dir = os.path.join(temp_dir, "extracted")
        os.makedirs(extract_dir, exist_ok=True)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # 获取解压后的文件夹名
        extracted_folders = [f for f in os.listdir(extract_dir) if os.path.isdir(os.path.join(extract_dir, f))]
        if not extracted_folders:
            print("❌ 解压后没有找到文件夹")
            return
        
        draft_folder = extracted_folders[0]
        draft_path = os.path.join(extract_dir, draft_folder)
        print(f"✅ 解压成功，草稿文件夹: {draft_folder}")
        
        # 步骤3：检查文件结构
        print(f"\n📋 步骤3：检查文件结构...")
        files = os.listdir(draft_path)
        print(f"文件列表: {files}")
        
        # 检查关键文件
        key_files = ['draft_content.json', 'draft_info.json', 'draft_meta_info.json']
        for key_file in key_files:
            file_path = os.path.join(draft_path, key_file)
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                print(f"✅ {key_file} 存在 (大小: {size} 字节)")
                
                # 检查文件内容
                if key_file == 'draft_content.json':
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = json.load(f)
                        print(f"   - canvas_config: {content.get('canvas_config', 'N/A')}")
                        print(f"   - tracks数量: {len(content.get('tracks', []))}")
                        print(f"   - materials数量: {len(content.get('materials', {}))}")
            else:
                print(f"❌ {key_file} 不存在")
        
        # 步骤4：检查draft_info.json内容
        print(f"\n📄 步骤4：检查draft_info.json内容...")
        draft_info_path = os.path.join(draft_path, 'draft_info.json')
        if os.path.exists(draft_info_path):
            with open(draft_info_path, 'r', encoding='utf-8') as f:
                draft_info = json.load(f)
                print(f"✅ draft_info.json 解析成功")
                print(f"   - canvas_config: {draft_info.get('canvas_config', 'N/A')}")
                print(f"   - version: {draft_info.get('version', 'N/A')}")
                print(f"   - app_source: {draft_info.get('platform', {}).get('app_source', 'N/A')}")
        else:
            print("❌ draft_info.json 不存在")
        
        # 步骤5：检查是否包含draft_content.json
        print(f"\n🔍 步骤5：检查draft_content.json内容...")
        draft_content_path = os.path.join(draft_path, 'draft_content.json')
        if os.path.exists(draft_content_path):
            with open(draft_content_path, 'r', encoding='utf-8') as f:
                draft_content = json.load(f)
                print(f"✅ draft_content.json 解析成功")
                print(f"   - canvas_config: {draft_content.get('canvas_config', 'N/A')}")
                print(f"   - tracks数量: {len(draft_content.get('tracks', []))}")
                print(f"   - materials数量: {len(draft_content.get('materials', {}))}")
                print(f"   - version: {draft_content.get('version', 'N/A')}")
        else:
            print("❌ draft_content.json 不存在")
        
        print(f"\n🎯 测试完成！")
        print(f"📁 草稿文件夹路径: {draft_path}")
        print(f"📋 文件总数: {len(files)}")
        
        # 清理临时文件
        import shutil
        shutil.rmtree(temp_dir)
        print(f"🧹 临时文件已清理")
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        logger.error(f"测试失败: {str(e)}", exc_info=True)

if __name__ == "__main__":
    download_and_check_jianying_draft() 