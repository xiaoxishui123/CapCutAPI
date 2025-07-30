#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接修改草稿文件修复脚本
在原始文件基础上直接修改，不重新创建文件
"""

import os
import json
import zipfile
import tempfile
import requests
import shutil
from urllib.parse import urlparse

class DirectDraftFixer:
    def __init__(self, draft_url):
        self.draft_url = draft_url
        self.temp_dir = None
        self.draft_id = None
        self.draft_path = None
    
    def download_and_extract(self):
        """下载并解压草稿文件"""
        print(f"正在下载草稿: {self.draft_url}")
        
        # 创建临时目录
        self.temp_dir = tempfile.mkdtemp()
        draft_zip_path = os.path.join(self.temp_dir, "draft.zip")
        
        try:
            # 下载草稿文件
            response = requests.get(self.draft_url, stream=True)
            response.raise_for_status()
            
            with open(draft_zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print("✓ 草稿文件下载完成")
            
            # 解压文件
            extract_dir = os.path.join(self.temp_dir, "extracted")
            os.makedirs(extract_dir, exist_ok=True)
            
            with zipfile.ZipFile(draft_zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # 检查文件结构
            file_list = zip_ref.namelist()
            print(f"ZIP文件内容: {file_list}")
            
            # 确定草稿路径
            draft_folders = [f for f in os.listdir(extract_dir) if f.startswith('dfd_')]
            
            if draft_folders:
                # 正常的草稿文件夹结构
                self.draft_id = draft_folders[0]
                self.draft_path = os.path.join(extract_dir, self.draft_id)
                print(f"✓ 找到草稿ID: {self.draft_id}")
            else:
                # 直接包含草稿文件的结构
                print("⚠️  检测到直接包含草稿文件的结构")
                self.draft_id = "dfd_cat_1753754237_75267d20"  # 从URL提取
                self.draft_path = os.path.join(extract_dir, self.draft_id)
                
                # 创建草稿文件夹并移动文件
                os.makedirs(self.draft_path, exist_ok=True)
                for item in os.listdir(extract_dir):
                    item_path = os.path.join(extract_dir, item)
                    if os.path.isfile(item_path):
                        shutil.move(item_path, os.path.join(self.draft_path, item))
                    elif os.path.isdir(item_path) and item != self.draft_id:
                        shutil.move(item_path, os.path.join(self.draft_path, item))
                
                print(f"✓ 创建草稿文件夹: {self.draft_id}")
            
            return True
            
        except Exception as e:
            print(f"❌ 下载或解压失败: {str(e)}")
            return False
    
    def analyze_current_structure(self):
        """分析当前草稿结构"""
        print("\n📋 当前草稿结构分析:")
        print(f"  草稿路径: {self.draft_path}")
        
        # 检查关键文件
        key_files = ["draft_info.json", "draft_content.json", "draft_meta_info.json"]
        for file_name in key_files:
            file_path = os.path.join(self.draft_path, file_name)
            if os.path.exists(file_path):
                print(f"  ✓ {file_name}")
            else:
                print(f"  ❌ {file_name} (缺失)")
        
        # 检查assets目录
        assets_dir = os.path.join(self.draft_path, "assets")
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
    
    def fix_media_files_directly(self):
        """直接修复媒体文件"""
        print("\n🔧 直接修复媒体文件...")
        
        # 读取draft_content.json
        content_path = os.path.join(self.draft_path, "draft_content.json")
        if not os.path.exists(content_path):
            print("  ❌ draft_content.json 不存在")
            return False
        
        with open(content_path, 'r', encoding='utf-8') as f:
            content_data = json.load(f)
        
        materials = content_data.get("materials", {})
        fixed_count = 0
        
        # 修复各种媒体文件
        for media_type in ["videos", "audios", "images"]:
            media_list = materials.get(media_type, [])
            for media in media_list:
                if "remote_url" in media and media["remote_url"]:
                    material_name = media.get("material_name", "")
                    if material_name:
                        local_path = os.path.join(self.draft_path, "assets", media_type[:-1], material_name)
                        if not os.path.exists(local_path):
                            print(f"  ⚠️  媒体文件缺失: {material_name}")
                            if self._download_media_file_directly(media["remote_url"], local_path):
                                fixed_count += 1
                                print(f"    ✓ 已修复: {material_name}")
                            else:
                                print(f"    ❌ 修复失败: {material_name}")
        
        print(f"  📊 修复统计: {fixed_count} 个媒体文件已修复")
        return True
    
    def _download_media_file_directly(self, remote_url, local_path):
        """直接下载媒体文件"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
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
            
            return True
            
        except Exception as e:
            print(f"    ❌ 下载失败: {str(e)}")
            return False
    
    def fix_platform_info_directly(self):
        """直接修复平台信息"""
        print("\n🔧 直接修复平台信息...")
        
        # 修复draft_content.json
        content_path = os.path.join(self.draft_path, "draft_content.json")
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
        info_path = os.path.join(self.draft_path, "draft_info.json")
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
    
    def create_fixed_zip_directly(self):
        """直接创建修复后的ZIP文件"""
        print("\n📦 创建修复后的ZIP文件...")
        
        # 创建输出目录
        output_dir = "./fixed_drafts"
        os.makedirs(output_dir, exist_ok=True)
        
        # 创建修复后的ZIP文件
        output_filename = f"{self.draft_id}_direct_fixed.zip"
        output_path = os.path.join(output_dir, output_filename)
        
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.draft_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, self.draft_path)
                    zipf.write(file_path, arcname)
        
        print(f"✓ 修复后的草稿文件已创建: {output_path}")
        return output_path
    
    def cleanup(self):
        """清理临时文件"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            print("🧹 临时文件已清理")
    
    def fix_draft_directly(self):
        """直接修复草稿文件"""
        try:
            print("🎬 直接修改草稿文件修复工具")
            print("=" * 50)
            
            # 1. 下载并解压
            if not self.download_and_extract():
                return None
            
            # 2. 分析当前结构
            self.analyze_current_structure()
            
            # 3. 直接修复媒体文件
            self.fix_media_files_directly()
            
            # 4. 直接修复平台信息
            self.fix_platform_info_directly()
            
            # 5. 创建修复后的ZIP文件
            fixed_draft_path = self.create_fixed_zip_directly()
            
            print("\n✅ 直接修复完成！")
            print(f"修复后的草稿文件: {fixed_draft_path}")
            
            return fixed_draft_path
            
        except Exception as e:
            print(f"❌ 修复失败: {str(e)}")
            return None
        finally:
            self.cleanup()

def main():
    """主函数"""
    # 您提供的草稿URL
    draft_url = "http://zdaigfpt.oss-cn-wuhan-lr.aliyuncs.com/dfd_cat_1753754237_75267d20.zip?OSSAccessKeyId=LTAI5tLhTQGk2Di25ArrkgGG&Expires=1753840685&Signature=RK%2Bzp7ZvezNN%2FFw5mMUc9DQPBdY%3D"
    
    # 创建直接修复器
    fixer = DirectDraftFixer(draft_url)
    
    # 执行直接修复
    fixed_draft_path = fixer.fix_draft_directly()
    
    if fixed_draft_path:
        print("\n📋 使用说明:")
        print("1. 将修复后的草稿文件复制到剪映的草稿目录")
        print("2. 重启剪映软件")
        print("3. 在剪映中打开修复后的草稿")
        print("4. 检查媒体文件是否正常显示")
        print("\n💡 优势:")
        print("- 直接在原始文件基础上修改")
        print("- 不重新创建整个文件结构")
        print("- 保留原始文件的完整性")
        print("- 修复过程更高效")
    else:
        print("\n❌ 修复失败！")
        print("请检查网络连接和文件权限。")

if __name__ == "__main__":
    main() 