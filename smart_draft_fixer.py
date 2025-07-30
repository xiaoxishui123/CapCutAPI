#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能草稿修复脚本
只修复需要修复的部分，避免不必要的重新创建
"""

import os
import json
import zipfile
import tempfile
import requests
import shutil
import hashlib
import time
from urllib.parse import urlparse

class SmartDraftFixer:
    def __init__(self, draft_url):
        self.draft_url = draft_url
        self.temp_dir = None
        self.draft_id = None
        self.draft_path = None
        self.original_files = {}
        self.fixed_files = {}
    
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
    
    def analyze_and_detect_issues(self):
        """分析并检测问题"""
        print("\n🔍 智能分析草稿问题...")
        
        issues = []
        
        # 检查关键文件
        key_files = ["draft_info.json", "draft_content.json", "draft_meta_info.json"]
        for file_name in key_files:
            file_path = os.path.join(self.draft_path, file_name)
            if os.path.exists(file_path):
                print(f"  ✓ {file_name}")
            else:
                print(f"  ❌ {file_name} (缺失)")
                issues.append(f"缺失文件: {file_name}")
        
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
                    issues.append(f"缺失目录: assets/{asset_type}")
        else:
            print("  ❌ assets目录不存在")
            issues.append("缺失目录: assets")
        
        # 检查平台信息
        platform_issues = self._check_platform_info()
        issues.extend(platform_issues)
        
        # 检查媒体文件
        media_issues = self._check_media_files()
        issues.extend(media_issues)
        
        return issues
    
    def _check_platform_info(self):
        """检查平台信息"""
        issues = []
        
        # 检查draft_content.json
        content_path = os.path.join(self.draft_path, "draft_content.json")
        if os.path.exists(content_path):
            with open(content_path, 'r', encoding='utf-8') as f:
                content_data = json.load(f)
            
            if "platform" in content_data:
                platform = content_data["platform"]
                if platform.get("os") != "windows":
                    issues.append("平台信息不匹配: draft_content.json")
        
        # 检查draft_info.json
        info_path = os.path.join(self.draft_path, "draft_info.json")
        if os.path.exists(info_path):
            with open(info_path, 'r', encoding='utf-8') as f:
                info_data = json.load(f)
            
            if "platform" in info_data:
                platform = info_data["platform"]
                if platform.get("os") != "windows":
                    issues.append("平台信息不匹配: draft_info.json")
        
        return issues
    
    def _check_media_files(self):
        """检查媒体文件"""
        issues = []
        
        content_path = os.path.join(self.draft_path, "draft_content.json")
        if not os.path.exists(content_path):
            return issues
        
        with open(content_path, 'r', encoding='utf-8') as f:
            content_data = json.load(f)
        
        materials = content_data.get("materials", {})
        
        # 检查各种媒体文件
        for media_type in ["videos", "audios", "images"]:
            media_list = materials.get(media_type, [])
            for media in media_list:
                if "remote_url" in media and media["remote_url"]:
                    material_name = media.get("material_name", "")
                    if material_name:
                        local_path = os.path.join(self.draft_path, "assets", media_type[:-1], material_name)
                        if not os.path.exists(local_path):
                            issues.append(f"媒体文件缺失: {material_name}")
        
        return issues
    
    def fix_only_necessary_parts(self, issues):
        """只修复必要的部分"""
        print(f"\n🔧 检测到 {len(issues)} 个问题，开始智能修复...")
        
        fixed_count = 0
        
        # 1. 修复媒体文件路径
        if self._fix_media_paths():
            fixed_count += 1
        
        # 2. 创建draft_meta_info.json文件
        if self._create_draft_meta_info():
            fixed_count += 1
        
        # 3. 修复缺失的媒体文件
        for issue in issues:
            if "媒体文件缺失" in issue:
                material_name = issue.split(": ")[1]
                if self._fix_single_media_file(material_name):
                    fixed_count += 1
                    print(f"  ✓ 已修复: {material_name}")
                else:
                    print(f"  ❌ 修复失败: {material_name}")
            
            elif "平台信息不匹配" in issue:
                file_name = issue.split(": ")[1]
                if self._fix_platform_info_for_file(file_name):
                    fixed_count += 1
                    print(f"  ✓ 已修复: {file_name}")
                else:
                    print(f"  ❌ 修复失败: {file_name}")
        
        print(f"  📊 修复统计: {fixed_count} 个问题已修复")
        return fixed_count
    
    def _fix_single_media_file(self, material_name):
        """修复单个媒体文件"""
        content_path = os.path.join(self.draft_path, "draft_content.json")
        if not os.path.exists(content_path):
            return False
        
        with open(content_path, 'r', encoding='utf-8') as f:
            content_data = json.load(f)
        
        materials = content_data.get("materials", {})
        
        # 查找对应的媒体文件
        for media_type in ["videos", "audios", "images"]:
            media_list = materials.get(media_type, [])
            for media in media_list:
                if media.get("material_name") == material_name:
                    remote_url = media.get("remote_url")
                    if remote_url:
                        local_path = os.path.join(self.draft_path, "assets", media_type[:-1], material_name)
                        return self._download_media_file_smart(remote_url, local_path)
        
        return False
    
    def _download_media_file_smart(self, remote_url, local_path):
        """智能下载媒体文件"""
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
    
    def _fix_platform_info_for_file(self, file_name):
        """修复指定文件的平台信息 - 基于原始CapCutAPI项目的逻辑"""
        file_path = os.path.join(self.draft_path, file_name)
        if not os.path.exists(file_path):
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 基于原始项目的Windows平台信息格式
            import uuid
            windows_platform = {
                "app_id": 3704,
                "app_source": "lv",
                "app_version": "5.9.0",
                "device_id": str(uuid.uuid4()).replace("-", "")[:32],
                "hard_disk_id": str(uuid.uuid4()).replace("-", "")[:32],
                "mac_address": str(uuid.uuid4()).replace("-", "")[:32],
                "os": "windows",
                "os_version": "10.0.19045"
            }
            
            # 更新平台信息
            if "platform" in data:
                data["platform"] = windows_platform
            
            if "last_modified_platform" in data:
                data["last_modified_platform"] = windows_platform
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            return True
            
        except Exception as e:
            print(f"    ❌ 修复失败: {str(e)}")
            return False
    
    def _download_remote_file(self, url, local_path):
        """下载远程文件"""
        try:
            print(f"    📥 下载远程文件: {url}")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # 确保目录存在
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            # 保存文件
            with open(local_path, 'wb') as f:
                f.write(response.content)
            
            print(f"    ✓ 下载完成: {os.path.basename(local_path)}")
            return True
        except Exception as e:
            print(f"    ❌ 下载失败: {str(e)}")
            return False

    def _fix_media_paths(self):
        """修复媒体文件路径问题 - 基于原始CapCutAPI项目的逻辑"""
        print("  🔧 修复媒体文件路径...")
        
        content_path = os.path.join(self.draft_path, "draft_content.json")
        if not os.path.exists(content_path):
            return False
        
        try:
            with open(content_path, 'r', encoding='utf-8') as f:
                content_data = json.load(f)
            
            materials = content_data.get("materials", {})
            fixed_count = 0
            
            # 修复各种媒体类型的路径
            for media_type in ["videos", "audios", "images"]:
                media_list = materials.get(media_type, [])
                for media in media_list:
                    material_name = media.get("material_name") or media.get("name", "")
                    if material_name:
                        # 检查是否有远程URL需要下载
                        remote_url = media.get("remote_url", "")
                        current_path = media.get("path", "")
                        current_replace_path = media.get("replace_path", "")
                        
                        if remote_url and not current_path and not current_replace_path:
                            # 下载远程文件
                            media_type_single = media_type[:-1]  # videos -> video
                            local_path = os.path.join(self.draft_path, f"assets/{media_type_single}/{material_name}")
                            
                            if self._download_remote_file(remote_url, local_path):
                                # 基于原始项目，使用replace_path字段，并设置为相对路径
                                new_replace_path = f"assets/{media_type_single}/{material_name}"
                                media["replace_path"] = new_replace_path
                                # 同时设置path字段为空，让剪映使用replace_path
                                media["path"] = ""
                                fixed_count += 1
                                print(f"    ✓ 下载并修复路径: {material_name} -> {new_replace_path}")
                        
                        elif current_path.startswith("/tmp/") or current_path.startswith("/var/"):
                            # 修复绝对路径为相对路径
                            media_type_single = media_type[:-1]  # videos -> video
                            new_replace_path = f"assets/{media_type_single}/{material_name}"
                            media["replace_path"] = new_replace_path
                            media["path"] = ""
                            fixed_count += 1
                            print(f"    ✓ 修复路径: {material_name} -> {new_replace_path}")
            
            # 保存修复后的内容
            with open(content_path, 'w', encoding='utf-8') as f:
                json.dump(content_data, f, ensure_ascii=False, indent=4)
            
            print(f"  📊 路径修复统计: {fixed_count} 个媒体文件路径已修复")
            return fixed_count > 0
            
        except Exception as e:
            print(f"    ❌ 路径修复失败: {str(e)}")
            return False
    
    def _create_draft_meta_info(self):
        """创建draft_meta_info.json文件"""
        print("  📝 创建draft_meta_info.json...")
        
        meta_info = {
            "platform": {
                "os": "windows",
                "os_version": "10.0.19045"
            },
            "version": "1.0.0",
            "create_time": int(time.time() * 1000),
            "update_time": int(time.time() * 1000)
        }
        
        meta_path = os.path.join(self.draft_path, "draft_meta_info.json")
        try:
            with open(meta_path, 'w', encoding='utf-8') as f:
                json.dump(meta_info, f, ensure_ascii=False, indent=4)
            print("    ✓ draft_meta_info.json 已创建")
            return True
        except Exception as e:
            print(f"    ❌ 创建失败: {str(e)}")
            return False
    
    def create_smart_fixed_zip(self):
        """创建智能修复后的ZIP文件"""
        print("\n📦 创建智能修复后的ZIP文件...")
        
        # 创建输出目录
        output_dir = "./fixed_drafts"
        os.makedirs(output_dir, exist_ok=True)
        
        # 创建修复后的ZIP文件
        output_filename = f"{self.draft_id}_smart_fixed.zip"
        output_path = os.path.join(output_dir, output_filename)
        
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.draft_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, self.draft_path)
                    zipf.write(file_path, arcname)
        
        print(f"✓ 智能修复后的草稿文件已创建: {output_path}")
        return output_path
    
    def cleanup(self):
        """清理临时文件"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            print("🧹 临时文件已清理")
    
    def smart_fix_draft(self):
        """智能修复草稿文件"""
        try:
            print("🎬 智能草稿修复工具")
            print("=" * 50)
            
            # 1. 下载并解压
            if not self.download_and_extract():
                return None
            
            # 2. 分析并检测问题
            issues = self.analyze_and_detect_issues()
            
            if not issues:
                print("\n✅ 草稿文件无需修复！")
                result = self.create_smart_fixed_zip()
                self.cleanup()
                return result
            
            # 3. 只修复必要的部分
            fixed_count = self.fix_only_necessary_parts(issues)
            
            # 4. 创建修复后的ZIP文件
            fixed_draft_path = self.create_smart_fixed_zip()
            
            print(f"\n✅ 智能修复完成！")
            print(f"修复了 {fixed_count} 个问题")
            print(f"修复后的草稿文件: {fixed_draft_path}")
            
            self.cleanup()
            return fixed_draft_path
            
        except Exception as e:
            print(f"❌ 修复失败: {str(e)}")
            self.cleanup()
            return None
    
    def download_draft(self):
        """仅下载草稿"""
        try:
            if not self.download_and_extract():
                return {"success": False, "error": "下载失败"}
            
            # 获取文件信息
            file_list = []
            file_size = 0
            for root, dirs, files in os.walk(self.draft_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.draft_path)
                    file_list.append(rel_path)
                    file_size += os.path.getsize(file_path)
            
            return {
                "success": True,
                "message": "草稿下载成功",
                "file_size": file_size,
                "file_count": len(file_list),
                "file_list": file_list
            }
        except Exception as e:
            return {"success": False, "error": f"下载失败: {str(e)}"}
        finally:
            self.cleanup()
    
    def fix_draft(self):
        """仅修复草稿"""
        try:
            result = self.smart_fix_draft()
            if result:
                return {
                    "success": True,
                    "message": "草稿修复成功",
                    "fixed_file": result
                }
            else:
                return {"success": False, "error": "修复失败"}
        except Exception as e:
            return {"success": False, "error": f"修复失败: {str(e)}"}
    
    def download_and_fix_draft(self):
        """下载并修复草稿"""
        try:
            # 下载并解压
            if not self.download_and_extract():
                return {"success": False, "error": "下载失败"}
            
            # 获取文件信息
            file_list = []
            file_size = 0
            for root, dirs, files in os.walk(self.draft_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.draft_path)
                    file_list.append(rel_path)
                    file_size += os.path.getsize(file_path)
            
            download_result = {
                "success": True,
                "message": "草稿下载成功",
                "file_size": file_size,
                "file_count": len(file_list),
                "file_list": file_list
            }
            
            # 修复
            result = self.smart_fix_draft()
            if result:
                fix_result = {
                    "success": True,
                    "message": "草稿修复成功",
                    "fixed_file": result
                }
            else:
                fix_result = {"success": False, "error": "修复失败"}
            
            return {
                "success": True,
                "message": "下载并修复成功",
                "download_info": download_result,
                "fix_info": fix_result
            }
        except Exception as e:
            return {"success": False, "error": f"下载并修复失败: {str(e)}"}
        finally:
            self.cleanup()

def main():
    """主函数"""
    # 您提供的草稿URL
    draft_url = "http://zdaigfpt.oss-cn-wuhan-lr.aliyuncs.com/dfd_cat_1753754237_75267d20.zip?OSSAccessKeyId=LTAI5tLhTQGk2Di25ArrkgGG&Expires=1753840685&Signature=RK%2Bzp7ZvezNN%2FFw5mMUc9DQPBdY%3D"
    
    # 创建智能修复器
    fixer = SmartDraftFixer(draft_url)
    
    # 执行智能修复
    fixed_draft_path = fixer.smart_fix_draft()
    
    if fixed_draft_path:
        print("\n📋 使用说明:")
        print("1. 将修复后的草稿文件复制到剪映的草稿目录")
        print("2. 重启剪映软件")
        print("3. 在剪映中打开修复后的草稿")
        print("4. 检查媒体文件是否正常显示")
        print("\n💡 智能修复优势:")
        print("- 只修复需要修复的部分")
        print("- 避免不必要的重新创建")
        print("- 保留原始文件的完整性")
        print("- 修复过程更高效")
        print("- 减少处理时间和资源消耗")
    else:
        print("\n❌ 修复失败！")
        print("请检查网络连接和文件权限。")

if __name__ == "__main__":
    main() 