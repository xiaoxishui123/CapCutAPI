#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from settings.local import OSS_CONFIG
from oss import upload_to_oss
import tempfile
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_oss_config():
    """测试OSS配置是否正常"""
    print("=== OSS配置测试 ===")
    print(f"Bucket名称: {OSS_CONFIG.get('bucket_name')}")
    print(f"Access Key ID: {OSS_CONFIG.get('access_key_id')}")
    print(f"Access Key Secret: {'*' * len(OSS_CONFIG.get('access_key_secret', ''))}")
    print(f"Endpoint: {OSS_CONFIG.get('endpoint')}")
    
    # 检查配置完整性
    required_fields = ['bucket_name', 'access_key_id', 'access_key_secret', 'endpoint']
    missing_fields = [field for field in required_fields if not OSS_CONFIG.get(field)]
    
    if missing_fields:
        print(f"❌ 缺少必要配置: {missing_fields}")
        return False
    
    print("✅ OSS配置完整")
    return True

def test_oss_upload():
    """测试OSS上传功能"""
    print("\n=== OSS上传测试 ===")
    
    try:
        # 创建临时测试文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("这是一个OSS上传测试文件")
            temp_file_path = f.name
        
        print(f"创建测试文件: {temp_file_path}")
        
        # 尝试上传
        print("开始上传测试...")
        upload_url = upload_to_oss(temp_file_path)
        
        if upload_url:
            print(f"✅ 上传成功! URL: {upload_url}")
            
            # 清理临时文件
            os.unlink(temp_file_path)
            return True
        else:
            print("❌ 上传失败，未返回URL")
            return False
            
    except Exception as e:
        print(f"❌ 上传测试失败: {str(e)}")
        logger.error(f"OSS上传测试失败", exc_info=True)
        return False

if __name__ == "__main__":
    print("开始OSS配置和连接测试...\n")
    
    # 测试配置
    config_ok = test_oss_config()
    
    if config_ok:
        # 测试上传
        upload_ok = test_oss_upload()
        
        if upload_ok:
            print("\n🎉 所有测试通过！OSS配置正常工作")
        else:
            print("\n❌ 上传测试失败，请检查网络连接和权限")
    else:
        print("\n❌ 配置测试失败，请检查OSS配置") 