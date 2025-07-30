#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进草稿创建脚本
解决CapCutAPI中媒体文件丢失的问题
"""

import os
import json
import shutil
import requests
import subprocess
from pathlib import Path

class DraftCreator:
    def __init__(self):
        self.base_url = "http://8.148.70.18:9000"
        self.draft_id = None
        self.draft_folder = None
    
    def create_draft(self, draft_name="测试草稿", width=1080, height=1920):
        """创建草稿"""
        print(f"创建草稿: {draft_name}")
        
        url = f"{self.base_url}/create_draft"
        data = {
            "draft_name": draft_name,
            "width": width,
            "height": height
        }
        
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            result = response.json()
            
            if result.get("success"):
                self.draft_id = result["output"]["draft_id"]
                print(f"✓ 草稿创建成功: {self.draft_id}")
                return True
            else:
                print(f"❌ 草稿创建失败: {result.get('error')}")
                return False
                
        except Exception as e:
            print(f"❌ 创建草稿时发生错误: {str(e)}")
            return False
    
    def add_text(self, text="欢迎使用CapCutAPI！", font_size=30, font_color="#FF0000"):
        """添加文本"""
        if not self.draft_id:
            print("❌ 请先创建草稿")
            return False
        
        print(f"添加文本: {text}")
        
        url = f"{self.base_url}/add_text"
        data = {
            "draft_id": self.draft_id,
            "text": text,
            "start": 0,
            "end": 5,
            "font": "HarmonyOS_Sans_SC_Regular",
            "font_color": font_color,
            "font_size": font_size,
            "track_name": "test_text"
        }
        
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            result = response.json()
            
            if result.get("success"):
                print("✓ 文本添加成功")
                return True
            else:
                print(f"❌ 文本添加失败: {result.get('error')}")
                return False
                
        except Exception as e:
            print(f"❌ 添加文本时发生错误: {str(e)}")
            return False
    
    def add_image(self, image_url="https://picsum.photos/800/600", duration=3):
        """添加图片"""
        if not self.draft_id:
            print("❌ 请先创建草稿")
            return False
        
        print(f"添加图片: {image_url}")
        
        url = f"{self.base_url}/add_image"
        data = {
            "draft_id": self.draft_id,
            "image_url": image_url,
            "start": 0,
            "end": duration,
            "track_name": "test_image"
        }
        
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            result = response.json()
            
            if result.get("success"):
                print("✓ 图片添加成功")
                return True
            else:
                print(f"❌ 图片添加失败: {result.get('error')}")
                return False
                
        except Exception as e:
            print(f"❌ 添加图片时发生错误: {str(e)}")
            return False
    
    def add_audio(self, audio_url="https://www.soundjay.com/misc/sounds/bell-ringing-05.wav", volume=1.0):
        """添加音频"""
        if not self.draft_id:
            print("❌ 请先创建草稿")
            return False
        
        print(f"添加音频: {audio_url}")
        
        url = f"{self.base_url}/add_audio"
        data = {
            "draft_id": self.draft_id,
            "audio_url": audio_url,
            "start": 0,
            "end": 5,
            "target_start": 0,
            "volume": volume,
            "track_name": "test_audio"
        }
        
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            result = response.json()
            
            if result.get("success"):
                print("✓ 音频添加成功")
                return True
            else:
                print(f"❌ 音频添加失败: {result.get('error')}")
                return False
                
        except Exception as e:
            print(f"❌ 添加音频时发生错误: {str(e)}")
            return False
    
    def save_draft(self, save_path="/tmp/capcut_drafts"):
        """保存草稿"""
        if not self.draft_id:
            print("❌ 请先创建草稿")
            return False
        
        print(f"保存草稿到: {save_path}")
        
        url = f"{self.base_url}/save_draft"
        data = {
            "draft_id": self.draft_id,
            "draft_folder": save_path
        }
        
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            result = response.json()
            
            if result.get("success"):
                draft_url = result["output"]["draft_url"]
                print(f"✓ 草稿保存成功")
                print(f"草稿下载URL: {draft_url}")
                return draft_url
            else:
                print(f"❌ 草稿保存失败: {result.get('error')}")
                return None
                
        except Exception as e:
            print(f"❌ 保存草稿时发生错误: {str(e)}")
            return None
    
    def fix_draft_media_issues(self, draft_url):
        """修复草稿媒体文件问题"""
        print(f"修复草稿媒体文件: {draft_url}")
        
        # 下载草稿文件
        try:
            response = requests.get(draft_url, stream=True)
            response.raise_for_status()
            
            # 保存到临时文件
            temp_file = f"/tmp/draft_{self.draft_id}.zip"
            with open(temp_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✓ 草稿文件下载完成: {temp_file}")
            
            # 解压并修复
            import zipfile
            import tempfile
            
            temp_dir = tempfile.mkdtemp()
            extract_dir = os.path.join(temp_dir, "extracted")
            os.makedirs(extract_dir, exist_ok=True)
            
            with zipfile.ZipFile(temp_file, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # 检查文件结构
            file_list = zip_ref.namelist()
            print(f"ZIP文件内容: {file_list}")
            
            # 创建正确的草稿文件夹结构
            draft_folder = os.path.join(extract_dir, self.draft_id)
            os.makedirs(draft_folder, exist_ok=True)
            
            # 移动文件到草稿文件夹
            for item in os.listdir(extract_dir):
                item_path = os.path.join(extract_dir, item)
                if os.path.isfile(item_path):
                    shutil.move(item_path, os.path.join(draft_folder, item))
                elif os.path.isdir(item_path) and item != self.draft_id:
                    shutil.move(item_path, os.path.join(draft_folder, item))
            
            # 修复媒体文件
            self._fix_media_files(draft_folder)
            
            # 修复平台信息
            self._fix_platform_info(draft_folder)
            
            # 创建修复后的草稿文件
            fixed_draft_path = f"./fixed_drafts/{self.draft_id}_improved.zip"
            os.makedirs("./fixed_drafts", exist_ok=True)
            
            with zipfile.ZipFile(fixed_draft_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(draft_folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, draft_folder)
                        zipf.write(file_path, arcname)
            
            print(f"✓ 修复后的草稿文件: {fixed_draft_path}")
            
            # 清理临时文件
            shutil.rmtree(temp_dir)
            os.remove(temp_file)
            
            return fixed_draft_path
            
        except Exception as e:
            print(f"❌ 修复草稿失败: {str(e)}")
            return None
    
    def _fix_media_files(self, draft_path):
        """修复媒体文件"""
        content_path = os.path.join(draft_path, "draft_content.json")
        if not os.path.exists(content_path):
            return
        
        with open(content_path, 'r', encoding='utf-8') as f:
            content_data = json.load(f)
        
        materials = content_data.get("materials", {})
        
        # 修复各种媒体文件
        for media_type in ["videos", "audios", "images"]:
            media_list = materials.get(media_type, [])
            for media in media_list:
                if "remote_url" in media and media["remote_url"]:
                    material_name = media.get("material_name", "")
                    if material_name:
                        local_path = os.path.join(draft_path, "assets", media_type[:-1], material_name)
                        if not os.path.exists(local_path):
                            print(f"  下载缺失的媒体文件: {material_name}")
                            self._download_media_file(media["remote_url"], local_path)
    
    def _download_media_file(self, remote_url, local_path):
        """下载媒体文件"""
        try:
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
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
    
    def _fix_platform_info(self, draft_path):
        """修复平台信息"""
        # 修复draft_content.json
        content_path = os.path.join(draft_path, "draft_content.json")
        if os.path.exists(content_path):
            with open(content_path, 'r', encoding='utf-8') as f:
                content_data = json.load(f)
            
            if "platform" in content_data:
                content_data["platform"]["os"] = "windows"
                content_data["platform"]["os_version"] = "10.0.19045"
            
            with open(content_path, 'w', encoding='utf-8') as f:
                json.dump(content_data, f, ensure_ascii=False, indent=4)
        
        # 修复draft_info.json
        info_path = os.path.join(draft_path, "draft_info.json")
        if os.path.exists(info_path):
            with open(info_path, 'r', encoding='utf-8') as f:
                info_data = json.load(f)
            
            if "platform" in info_data:
                info_data["platform"]["os"] = "windows"
                info_data["platform"]["os_version"] = "10.0.19045"
            
            with open(info_path, 'w', encoding='utf-8') as f:
                json.dump(info_data, f, ensure_ascii=False, indent=4)

def main():
    """主函数"""
    print("🎬 改进的CapCutAPI草稿创建工具")
    print("=" * 50)
    
    creator = DraftCreator()
    
    # 1. 创建草稿
    if not creator.create_draft("改进测试草稿"):
        return
    
    # 2. 添加文本
    creator.add_text("欢迎使用改进的CapCutAPI！", 40, "#FF0000")
    
    # 3. 添加图片
    creator.add_image("https://picsum.photos/800/600", 3)
    
    # 4. 添加音频
    creator.add_audio("https://www.soundjay.com/misc/sounds/bell-ringing-05.wav", 1.0)
    
    # 5. 保存草稿
    draft_url = creator.save_draft()
    if not draft_url:
        return
    
    # 6. 修复草稿媒体文件问题
    fixed_draft_path = creator.fix_draft_media_issues(draft_url)
    
    if fixed_draft_path:
        print("\n✅ 改进的草稿创建完成！")
        print(f"修复后的草稿文件: {fixed_draft_path}")
        print("\n📋 使用说明:")
        print("1. 将修复后的草稿文件复制到剪映的草稿目录")
        print("2. 重启剪映软件")
        print("3. 在剪映中打开修复后的草稿")
        print("4. 检查媒体文件是否正常显示")
    else:
        print("\n❌ 草稿创建或修复失败！")

if __name__ == "__main__":
    main() 