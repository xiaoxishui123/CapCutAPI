#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
服务器端草稿文件直接修改脚本
在服务器上直接修改草稿文件，无需重新创建
"""

import os
import json
import shutil
import requests
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ServerSideDraftFixer:
    def __init__(self, draft_id, server_base_url="http://8.148.70.18:9000"):
        self.draft_id = draft_id
        self.server_base_url = server_base_url
        self.draft_path = None
        
    def find_draft_directory(self):
        """在服务器上查找草稿目录"""
        logger.info(f"查找草稿目录: {self.draft_id}")
        
        # 可能的草稿目录位置
        possible_paths = [
            f"./{self.draft_id}",
            f"./tmp/{self.draft_id}",
            f"./drafts/{self.draft_id}",
            f"/tmp/{self.draft_id}",
            f"/home/CapCutAPI/{self.draft_id}"
        ]
        
        for path in possible_paths:
            if os.path.exists(path) and os.path.isdir(path):
                self.draft_path = path
                logger.info(f"✓ 找到草稿目录: {path}")
                return True
        
        logger.error(f"❌ 未找到草稿目录: {self.draft_id}")
        return False
    
    def analyze_draft_structure(self):
        """分析草稿结构"""
        if not self.draft_path:
            logger.error("草稿路径未设置")
            return False
        
        logger.info(f"分析草稿结构: {self.draft_path}")
        
        # 检查关键文件
        key_files = ["draft_info.json", "draft_content.json", "draft_meta_info.json"]
        for file_name in key_files:
            file_path = os.path.join(self.draft_path, file_name)
            if os.path.exists(file_path):
                logger.info(f"  ✓ {file_name}")
            else:
                logger.warning(f"  ❌ {file_name} (缺失)")
        
        # 检查assets目录
        assets_dir = os.path.join(self.draft_path, "assets")
        if os.path.exists(assets_dir):
            logger.info(f"  ✓ assets目录")
            for asset_type in ["video", "audio", "image"]:
                asset_dir = os.path.join(assets_dir, asset_type)
                if os.path.exists(asset_dir):
                    files = os.listdir(asset_dir)
                    logger.info(f"    {asset_type}: {len(files)} 个文件")
                    for file in files:
                        logger.info(f"      - {file}")
                else:
                    logger.warning(f"    {asset_type}: 目录不存在")
        else:
            logger.warning("  ❌ assets目录不存在")
        
        return True
    
    def fix_media_files_in_place(self):
        """在服务器上直接修复媒体文件"""
        logger.info("🔧 直接修复媒体文件...")
        
        # 读取draft_content.json
        content_path = os.path.join(self.draft_path, "draft_content.json")
        if not os.path.exists(content_path):
            logger.error("draft_content.json 不存在")
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
                            logger.warning(f"  ⚠️  媒体文件缺失: {material_name}")
                            if self._download_media_file_in_place(media["remote_url"], local_path):
                                fixed_count += 1
                                logger.info(f"    ✓ 已修复: {material_name}")
                            else:
                                logger.error(f"    ❌ 修复失败: {material_name}")
        
        logger.info(f"  📊 修复统计: {fixed_count} 个媒体文件已修复")
        return True
    
    def _download_media_file_in_place(self, remote_url, local_path):
        """在服务器上直接下载媒体文件"""
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
            logger.error(f"    ❌ 下载失败: {str(e)}")
            return False
    
    def fix_platform_info_in_place(self):
        """在服务器上直接修复平台信息"""
        logger.info("🔧 直接修复平台信息...")
        
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
            logger.info("  ✓ 修复draft_content.json平台信息")
        
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
            logger.info("  ✓ 修复draft_info.json平台信息")
    
    def create_backup(self):
        """创建备份"""
        if not self.draft_path:
            return False
        
        backup_path = f"{self.draft_path}_backup_{int(time.time())}"
        try:
            shutil.copytree(self.draft_path, backup_path)
            logger.info(f"✓ 备份已创建: {backup_path}")
            return True
        except Exception as e:
            logger.error(f"❌ 备份失败: {str(e)}")
            return False
    
    def fix_draft_in_place(self):
        """在服务器上直接修复草稿"""
        try:
            logger.info("🎬 服务器端直接修改草稿文件")
            logger.info("=" * 50)
            
            # 1. 查找草稿目录
            if not self.find_draft_directory():
                return False
            
            # 2. 创建备份
            self.create_backup()
            
            # 3. 分析草稿结构
            self.analyze_draft_structure()
            
            # 4. 直接修复媒体文件
            self.fix_media_files_in_place()
            
            # 5. 直接修复平台信息
            self.fix_platform_info_in_place()
            
            logger.info("\n✅ 服务器端直接修复完成！")
            logger.info(f"修复后的草稿目录: {self.draft_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ 修复失败: {str(e)}")
            return False

def fix_draft_on_server(draft_id):
    """在服务器上修复指定草稿"""
    fixer = ServerSideDraftFixer(draft_id)
    return fixer.fix_draft_in_place()

def main():
    """主函数"""
    # 测试草稿ID
    draft_id = "dfd_cat_1753754237_75267d20"
    
    print("🎬 服务器端草稿直接修改工具")
    print("=" * 50)
    
    # 执行服务器端修复
    success = fix_draft_on_server(draft_id)
    
    if success:
        print("\n✅ 服务器端修复完成！")
        print("\n💡 优势:")
        print("- 直接在服务器上修改文件")
        print("- 无需重新创建整个文件结构")
        print("- 保留原始文件的完整性")
        print("- 修复过程更高效")
        print("- 减少文件传输开销")
    else:
        print("\n❌ 服务器端修复失败！")
        print("请检查草稿ID和文件权限。")

if __name__ == "__main__":
    import time
    main() 