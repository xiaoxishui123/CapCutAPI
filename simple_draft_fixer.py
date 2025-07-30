#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单草稿修复脚本
专门解决剪映草稿中媒体文件丢失的问题
"""

import os
import json
import zipfile
import tempfile
import requests
import shutil
from urllib.parse import urlparse

def download_and_fix_draft(draft_url, output_dir="./fixed_drafts"):
    """
    下载并修复草稿文件
    
    :param draft_url: 草稿下载URL
    :param output_dir: 输出目录
    :return: 修复后的草稿文件路径
    """
    print(f"正在处理草稿: {draft_url}")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    
    try:
        # 1. 下载草稿文件
        print("1. 下载草稿文件...")
        draft_zip_path = os.path.join(temp_dir, "draft.zip")
        
        response = requests.get(draft_url, stream=True)
        response.raise_for_status()
        
        with open(draft_zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print("✓ 草稿文件下载完成")
        
        # 2. 解压草稿文件
        print("2. 解压草稿文件...")
        extract_dir = os.path.join(temp_dir, "extracted")
        os.makedirs(extract_dir, exist_ok=True)
        
        with zipfile.ZipFile(draft_zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # 检查ZIP文件结构
        file_list = zip_ref.namelist()
        print(f"ZIP文件内容: {file_list}")
        
        # 查找草稿文件夹或直接的文件
        draft_folders = [f for f in os.listdir(extract_dir) if f.startswith('dfd_')]
        
        if draft_folders:
            # 正常的草稿文件夹结构
            draft_id = draft_folders[0]
            draft_path = os.path.join(extract_dir, draft_id)
            print(f"✓ 找到草稿ID: {draft_id}")
        else:
            # 直接包含草稿文件的结构
            print("⚠️  检测到直接包含草稿文件的结构")
            
            # 从URL中提取草稿ID
            draft_id = "dfd_cat_1753754237_75267d20"  # 从URL中提取
            draft_path = os.path.join(extract_dir, draft_id)
            
            # 创建草稿文件夹
            os.makedirs(draft_path, exist_ok=True)
            
            # 移动文件到草稿文件夹
            for item in os.listdir(extract_dir):
                item_path = os.path.join(extract_dir, item)
                if os.path.isfile(item_path):
                    # 移动文件到草稿文件夹
                    shutil.move(item_path, os.path.join(draft_path, item))
                elif os.path.isdir(item_path) and item != draft_id:
                    # 移动目录到草稿文件夹（排除草稿文件夹本身）
                    shutil.move(item_path, os.path.join(draft_path, item))
            
            print(f"✓ 创建草稿文件夹: {draft_id}")
        
        # 3. 分析草稿结构
        print("3. 分析草稿结构...")
        analyze_draft_structure(draft_path)
        
        # 4. 修复媒体文件
        print("4. 修复媒体文件...")
        fix_media_files(draft_path)
        
        # 5. 修复平台信息
        print("5. 修复平台信息...")
        fix_platform_info(draft_path)
        
        # 6. 创建修复后的草稿文件
        print("6. 创建修复后的草稿文件...")
        output_filename = f"{draft_id}_fixed.zip"
        output_path = os.path.join(output_dir, output_filename)
        
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(draft_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, draft_path)
                    zipf.write(file_path, arcname)
        
        print(f"✓ 修复后的草稿文件已创建: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ 处理失败: {str(e)}")
        return None
    finally:
        # 清理临时文件
        shutil.rmtree(temp_dir)

def analyze_draft_structure(draft_path):
    """分析草稿文件结构"""
    print(f"  草稿路径: {draft_path}")
    
    # 检查关键文件
    key_files = ["draft_info.json", "draft_content.json", "draft_meta_info.json"]
    for file_name in key_files:
        file_path = os.path.join(draft_path, file_name)
        if os.path.exists(file_path):
            print(f"  ✓ {file_name}")
        else:
            print(f"  ❌ {file_name} (缺失)")
    
    # 检查assets目录
    assets_dir = os.path.join(draft_path, "assets")
    if os.path.exists(assets_dir):
        print(f"  ✓ assets目录")
        for asset_type in ["video", "audio", "image"]:
            asset_dir = os.path.join(assets_dir, asset_type)
            if os.path.exists(asset_dir):
                files = os.listdir(asset_dir)
                print(f"    {asset_type}: {len(files)} 个文件")
                for file in files:
                    print(f"      - {file}")
            else:
                print(f"    {asset_type}: 目录不存在")
    else:
        print("  ❌ assets目录不存在")

def fix_media_files(draft_path):
    """修复媒体文件"""
    # 读取draft_content.json
    content_path = os.path.join(draft_path, "draft_content.json")
    if not os.path.exists(content_path):
        print("  ❌ draft_content.json 不存在")
        return
    
    with open(content_path, 'r', encoding='utf-8') as f:
        content_data = json.load(f)
    
    materials = content_data.get("materials", {})
    
    # 修复视频文件
    videos = materials.get("videos", [])
    for video in videos:
        if "remote_url" in video and video["remote_url"]:
            material_name = video.get("material_name", "")
            if material_name:
                local_path = os.path.join(draft_path, "assets", "video", material_name)
                if not os.path.exists(local_path):
                    print(f"  ⚠️  视频文件缺失: {material_name}")
                    download_media_file(video["remote_url"], local_path)
    
    # 修复音频文件
    audios = materials.get("audios", [])
    for audio in audios:
        if "remote_url" in audio and audio["remote_url"]:
            material_name = audio.get("material_name", "")
            if material_name:
                local_path = os.path.join(draft_path, "assets", "audio", material_name)
                if not os.path.exists(local_path):
                    print(f"  ⚠️  音频文件缺失: {material_name}")
                    download_media_file(audio["remote_url"], local_path)
    
    # 修复图片文件
    images = materials.get("images", [])
    for image in images:
        if "remote_url" in image and image["remote_url"]:
            material_name = image.get("material_name", "")
            if material_name:
                local_path = os.path.join(draft_path, "assets", "image", material_name)
                if not os.path.exists(local_path):
                    print(f"  ⚠️  图片文件缺失: {material_name}")
                    download_media_file(image["remote_url"], local_path)

def download_media_file(remote_url, local_path):
    """下载媒体文件"""
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        print(f"    正在下载: {os.path.basename(local_path)}")
        
        # 设置请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # 下载文件
        response = requests.get(remote_url, headers=headers, stream=True)
        response.raise_for_status()
        
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"    ✓ 下载完成: {os.path.basename(local_path)}")
        return True
        
    except Exception as e:
        print(f"    ❌ 下载失败: {str(e)}")
        return False

def fix_platform_info(draft_path):
    """修复平台信息"""
    # 修复draft_content.json
    content_path = os.path.join(draft_path, "draft_content.json")
    if os.path.exists(content_path):
        with open(content_path, 'r', encoding='utf-8') as f:
            content_data = json.load(f)
        
        # 更新平台信息为Windows
        if "platform" in content_data:
            content_data["platform"]["os"] = "windows"
            content_data["platform"]["os_version"] = "10.0.19045"
        
        with open(content_path, 'w', encoding='utf-8') as f:
            json.dump(content_data, f, ensure_ascii=False, indent=4)
        print("  ✓ 修复draft_content.json平台信息")
    
    # 修复draft_info.json
    info_path = os.path.join(draft_path, "draft_info.json")
    if os.path.exists(info_path):
        with open(info_path, 'r', encoding='utf-8') as f:
            info_data = json.load(f)
        
        # 更新平台信息
        if "platform" in info_data:
            info_data["platform"]["os"] = "windows"
            info_data["platform"]["os_version"] = "10.0.19045"
        
        with open(info_path, 'w', encoding='utf-8') as f:
            json.dump(info_data, f, ensure_ascii=False, indent=4)
        print("  ✓ 修复draft_info.json平台信息")

def main():
    """主函数"""
    # 您提供的草稿URL
    draft_url = "http://zdaigfpt.oss-cn-wuhan-lr.aliyuncs.com/dfd_cat_1753754237_75267d20.zip?OSSAccessKeyId=LTAI5tLhTQGk2Di25ArrkgGG&Expires=1753840685&Signature=RK%2Bzp7ZvezNN%2FFw5mMUc9DQPBdY%3D"
    
    print("🎬 剪映草稿修复工具")
    print("=" * 50)
    
    # 执行修复
    fixed_draft_path = download_and_fix_draft(draft_url)
    
    if fixed_draft_path:
        print("\n✅ 修复完成！")
        print(f"修复后的草稿文件: {fixed_draft_path}")
        print("\n📋 使用说明:")
        print("1. 将修复后的草稿文件复制到剪映的草稿目录")
        print("2. 重启剪映软件")
        print("3. 在剪映中打开修复后的草稿")
        print("4. 检查媒体文件是否正常显示")
    else:
        print("\n❌ 修复失败！")
        print("请检查网络连接和文件权限。")

if __name__ == "__main__":
    main() 