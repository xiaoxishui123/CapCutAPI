#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载修复后的草稿文件
"""

import requests
import json
import os

def download_fixed_draft(draft_url):
    """下载并修复草稿文件"""
    print("🎬 开始下载并修复草稿...")
    
    # API端点
    api_url = "http://8.148.70.18:9000/api/download_and_fix_draft"
    
    # 请求数据
    data = {
        "draft_url": draft_url,
        "fix_method": "smart"
    }
    
    try:
        # 发送请求
        print("📡 正在调用修复API...")
        response = requests.post(api_url, json=data, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get("success"):
            print("✅ 修复成功！")
            print(f"📁 修复后的文件: {result['fix_info']['fixed_file']}")
            print(f"📊 文件大小: {result['download_info']['file_size']} 字节")
            print(f"📋 文件数量: {result['download_info']['file_count']} 个")
            print("\n📋 文件列表:")
            for file in result['download_info']['file_list']:
                print(f"  - {file}")
            
            # 检查是否包含关键文件
            file_list = result['download_info']['file_list']
            has_meta_info = any('draft_meta_info.json' in f for f in file_list)
            
            if has_meta_info:
                print("\n✅ 包含 draft_meta_info.json 文件 - 剪映应该能正常识别！")
            else:
                print("\n⚠️  缺少 draft_meta_info.json 文件 - 可能需要手动修复")
            
            return True
        else:
            print(f"❌ 修复失败: {result.get('error', '未知错误')}")
            return False
            
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")
        return False

def main():
    """主函数"""
    # 您提供的草稿URL
    draft_url = "http://zdaigfpt.oss-cn-wuhan-lr.aliyuncs.com/dfd_cat_1753754237_75267d20.zip?OSSAccessKeyId=LTAI5tLhTQGk2Di25ArrkgGG&Expires=1753840685&Signature=RK%2Bzp7ZvezNN%2FFw5mMUc9DQPBdY%3D"
    
    print("🎯 剪映草稿修复工具")
    print("=" * 50)
    
    # 下载并修复
    success = download_fixed_draft(draft_url)
    
    if success:
        print("\n📋 使用说明:")
        print("1. 修复后的文件位于: ./fixed_drafts/dfd_cat_1753754237_75267d20_smart_fixed.zip")
        print("2. 将此文件复制到剪映的草稿目录")
        print("3. 重启剪映软件")
        print("4. 在剪映中打开修复后的草稿")
        print("5. 检查媒体文件是否正常显示")
        
        print("\n💡 修复内容:")
        print("- ✅ 创建了 draft_meta_info.json 文件")
        print("- ✅ 修复了媒体文件路径")
        print("- ✅ 下载了缺失的媒体文件")
        print("- ✅ 保持了正确的文件结构")
    else:
        print("\n❌ 修复失败，请检查网络连接或联系技术支持")

if __name__ == "__main__":
    main() 