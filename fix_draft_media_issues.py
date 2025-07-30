#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复剪映草稿媒体文件问题的脚本

主要解决以下问题：
1. 媒体文件下载失败
2. 草稿文件中的媒体文件引用不正确
3. OSS模式下的文件路径问题
"""

import os
import json
import shutil
import zipfile
import tempfile
import requests
from urllib.parse import urlparse
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DraftMediaFixer:
    def __init__(self, draft_url, output_dir="./fixed_drafts"):
        """
        初始化修复器
        
        :param draft_url: 草稿下载URL
        :param output_dir: 输出目录
        """
        self.draft_url = draft_url
        self.output_dir = output_dir
        self.temp_dir = None
        self.draft_id = None
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
    
    def download_draft(self):
        """下载草稿文件"""
        try:
            logger.info(f"正在下载草稿: {self.draft_url}")
            
            # 创建临时目录
            self.temp_dir = tempfile.mkdtemp()
            draft_zip_path = os.path.join(self.temp_dir, "draft.zip")
            
            # 下载草稿文件
            response = requests.get(self.draft_url, stream=True)
            response.raise_for_status()
            
            with open(draft_zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info("草稿文件下载完成")
            return draft_zip_path
            
        except Exception as e:
            logger.error(f"下载草稿失败: {str(e)}")
            return None
    
    def extract_draft(self, draft_zip_path):
        """解压草稿文件"""
        try:
            extract_dir = os.path.join(self.temp_dir, "extracted")
            os.makedirs(extract_dir, exist_ok=True)
            
            with zipfile.ZipFile(draft_zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # 获取草稿ID（文件夹名）
            draft_folders = [f for f in os.listdir(extract_dir) if f.startswith('dfd_')]
            if draft_folders:
                self.draft_id = draft_folders[0]
                draft_path = os.path.join(extract_dir, self.draft_id)
                logger.info(f"草稿ID: {self.draft_id}")
                return draft_path
            else:
                logger.error("未找到草稿文件夹")
                return None
                
        except Exception as e:
            logger.error(f"解压草稿失败: {str(e)}")
            return None
    
    def analyze_draft_structure(self, draft_path):
        """分析草稿文件结构"""
        try:
            logger.info("分析草稿文件结构...")
            
            # 检查关键文件
            key_files = [
                "draft_info.json",
                "draft_content.json", 
                "draft_meta_info.json"
            ]
            
            for file_name in key_files:
                file_path = os.path.join(draft_path, file_name)
                if os.path.exists(file_path):
                    logger.info(f"✓ 找到文件: {file_name}")
                else:
                    logger.warning(f"✗ 缺少文件: {file_name}")
            
            # 检查assets目录
            assets_dir = os.path.join(draft_path, "assets")
            if os.path.exists(assets_dir):
                logger.info("✓ 找到assets目录")
                for asset_type in ["video", "audio", "image"]:
                    asset_dir = os.path.join(assets_dir, asset_type)
                    if os.path.exists(asset_dir):
                        files = os.listdir(asset_dir)
                        logger.info(f"  {asset_type}: {len(files)} 个文件")
                    else:
                        logger.warning(f"  {asset_type}: 目录不存在")
            else:
                logger.warning("✗ assets目录不存在")
            
            return True
            
        except Exception as e:
            logger.error(f"分析草稿结构失败: {str(e)}")
            return False
    
    def fix_media_references(self, draft_path):
        """修复媒体文件引用"""
        try:
            logger.info("修复媒体文件引用...")
            
            # 读取draft_content.json
            content_path = os.path.join(draft_path, "draft_content.json")
            if not os.path.exists(content_path):
                logger.error("draft_content.json 文件不存在")
                return False
            
            with open(content_path, 'r', encoding='utf-8') as f:
                content_data = json.load(f)
            
            # 检查materials部分
            materials = content_data.get("materials", {})
            
            # 修复视频文件引用
            videos = materials.get("videos", [])
            for video in videos:
                if "remote_url" in video and video["remote_url"]:
                    # 检查本地文件是否存在
                    material_name = video.get("material_name", "")
                    if material_name:
                        local_path = os.path.join(draft_path, "assets", "video", material_name)
                        if not os.path.exists(local_path):
                            logger.warning(f"视频文件不存在: {material_name}")
                            # 尝试下载文件
                            self.download_media_file(video["remote_url"], local_path)
            
            # 修复音频文件引用
            audios = materials.get("audios", [])
            for audio in audios:
                if "remote_url" in audio and audio["remote_url"]:
                    material_name = audio.get("material_name", "")
                    if material_name:
                        local_path = os.path.join(draft_path, "assets", "audio", material_name)
                        if not os.path.exists(local_path):
                            logger.warning(f"音频文件不存在: {material_name}")
                            # 尝试下载文件
                            self.download_media_file(audio["remote_url"], local_path)
            
            # 修复图片文件引用
            images = materials.get("images", [])
            for image in images:
                if "remote_url" in image and image["remote_url"]:
                    material_name = image.get("material_name", "")
                    if material_name:
                        local_path = os.path.join(draft_path, "assets", "image", material_name)
                        if not os.path.exists(local_path):
                            logger.warning(f"图片文件不存在: {material_name}")
                            # 尝试下载文件
                            self.download_media_file(image["remote_url"], local_path)
            
            logger.info("媒体文件引用修复完成")
            return True
            
        except Exception as e:
            logger.error(f"修复媒体文件引用失败: {str(e)}")
            return False
    
    def download_media_file(self, remote_url, local_path):
        """下载媒体文件"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            logger.info(f"正在下载: {remote_url} -> {local_path}")
            
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
            
            logger.info(f"文件下载完成: {local_path}")
            return True
            
        except Exception as e:
            logger.error(f"下载文件失败 {remote_url}: {str(e)}")
            return False
    
    def fix_platform_info(self, draft_path):
        """修复平台信息"""
        try:
            logger.info("修复平台信息...")
            
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
            
            logger.info("平台信息修复完成")
            return True
            
        except Exception as e:
            logger.error(f"修复平台信息失败: {str(e)}")
            return False
    
    def create_fixed_draft(self, draft_path):
        """创建修复后的草稿文件"""
        try:
            logger.info("创建修复后的草稿文件...")
            
            # 创建输出文件名
            output_filename = f"{self.draft_id}_fixed.zip"
            output_path = os.path.join(self.output_dir, output_filename)
            
            # 创建ZIP文件
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(draft_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, draft_path)
                        zipf.write(file_path, arcname)
            
            logger.info(f"修复后的草稿文件已创建: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"创建修复后的草稿文件失败: {str(e)}")
            return None
    
    def cleanup(self):
        """清理临时文件"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            logger.info("临时文件已清理")
    
    def fix_draft(self):
        """执行完整的草稿修复流程"""
        try:
            logger.info("开始修复草稿文件...")
            
            # 1. 下载草稿
            draft_zip_path = self.download_draft()
            if not draft_zip_path:
                return False
            
            # 2. 解压草稿
            draft_path = self.extract_draft(draft_zip_path)
            if not draft_path:
                return False
            
            # 3. 分析草稿结构
            if not self.analyze_draft_structure(draft_path):
                return False
            
            # 4. 修复媒体文件引用
            if not self.fix_media_references(draft_path):
                return False
            
            # 5. 修复平台信息
            if not self.fix_platform_info(draft_path):
                return False
            
            # 6. 创建修复后的草稿文件
            fixed_draft_path = self.create_fixed_draft(draft_path)
            if not fixed_draft_path:
                return False
            
            logger.info("草稿修复完成！")
            logger.info(f"修复后的草稿文件: {fixed_draft_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"修复草稿失败: {str(e)}")
            return False
        finally:
            self.cleanup()

def main():
    """主函数"""
    # 测试用的草稿URL
    draft_url = "http://zdaigfpt.oss-cn-wuhan-lr.aliyuncs.com/dfd_cat_1753754237_75267d20.zip?OSSAccessKeyId=LTAI5tLhTQGk2Di25ArrkgGG&Expires=1753840685&Signature=RK%2Bzp7ZvezNN%2FFw5mMUc9DQPBdY%3D"
    
    # 创建修复器
    fixer = DraftMediaFixer(draft_url)
    
    # 执行修复
    success = fixer.fix_draft()
    
    if success:
        print("\n✅ 草稿修复成功！")
        print("请将修复后的草稿文件复制到剪映的草稿目录中进行测试。")
    else:
        print("\n❌ 草稿修复失败！")
        print("请检查网络连接和文件权限。")

if __name__ == "__main__":
    main() 