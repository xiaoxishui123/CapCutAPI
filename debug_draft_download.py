#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试草稿下载脚本
检查下载的草稿文件内容
"""

import os
import zipfile
import tempfile
import requests

def debug_draft_download(draft_url):
    """调试草稿下载"""
    print(f"正在下载草稿: {draft_url}")
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    draft_zip_path = os.path.join(temp_dir, "draft.zip")
    
    try:
        # 下载草稿文件
        response = requests.get(draft_url, stream=True)
        response.raise_for_status()
        
        with open(draft_zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✓ 草稿文件下载完成: {draft_zip_path}")
        print(f"文件大小: {os.path.getsize(draft_zip_path)} 字节")
        
        # 检查ZIP文件内容
        try:
            with zipfile.ZipFile(draft_zip_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                print(f"\nZIP文件内容:")
                for file in file_list:
                    print(f"  - {file}")
                
                # 检查是否有草稿文件夹
                draft_folders = [f for f in file_list if f.startswith('dfd_')]
                if draft_folders:
                    print(f"\n✓ 找到草稿文件夹: {draft_folders}")
                else:
                    print(f"\n❌ 未找到草稿文件夹")
                    print("文件列表:")
                    for file in file_list:
                        print(f"  {file}")
        
        except zipfile.BadZipFile:
            print("❌ 下载的文件不是有效的ZIP文件")
            
            # 检查文件内容
            with open(draft_zip_path, 'rb') as f:
                content = f.read(1024)
                print(f"文件前1024字节: {content}")
                
                # 检查是否是HTML错误页面
                if b'<html' in content.lower() or b'<!doctype' in content.lower():
                    print("❌ 下载的是HTML页面，可能是错误页面")
                    
                    # 读取完整内容
                    with open(draft_zip_path, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                        print(f"HTML内容: {html_content[:500]}...")
        
    except Exception as e:
        print(f"❌ 下载失败: {str(e)}")
    finally:
        # 清理临时文件
        import shutil
        shutil.rmtree(temp_dir)

def main():
    """主函数"""
    # 您提供的草稿URL
    draft_url = "http://zdaigfpt.oss-cn-wuhan-lr.aliyuncs.com/dfd_cat_1753754237_75267d20.zip?OSSAccessKeyId=LTAI5tLhTQGk2Di25ArrkgGG&Expires=1753840685&Signature=RK%2Bzp7ZvezNN%2FFw5mMUc9DQPBdY%3D"
    
    print("🔍 调试草稿下载")
    print("=" * 50)
    
    debug_draft_download(draft_url)

if __name__ == "__main__":
    main() 