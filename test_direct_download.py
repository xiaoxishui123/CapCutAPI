#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试直接下载功能
"""

import requests
import json

def test_direct_download():
    """测试直接下载功能"""
    print("🎯 测试直接下载功能")
    print("=" * 50)
    
    # API端点
    api_url = "http://8.148.70.18:9000/api/download_and_fix_draft"
    
    # 测试数据
    data = {
        "draft_url": "http://zdaigfpt.oss-cn-wuhan-lr.aliyuncs.com/dfd_cat_1753754237_75267d20.zip?OSSAccessKeyId=LTAI5tLhTQGk2Di25ArrkgGG&Expires=1753840685&Signature=RK%2Bzp7ZvezNN%2FFw5mMUc9DQPBdY%3D",
        "fix_method": "smart"
    }
    
    try:
        print("📡 正在调用修复API...")
        response = requests.post(api_url, json=data, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get("success"):
            print("✅ 修复成功！")
            print(f"📋 修复结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            # 检查是否有下载链接
            if result.get("download_url"):
                print(f"\n🎉 直接下载链接: {result['download_url']}")
                print("💡 您可以直接点击此链接下载修复后的草稿文件！")
                
                # 测试下载链接是否有效
                try:
                    download_response = requests.head(result["download_url"])
                    if download_response.status_code == 200:
                        print("✅ 下载链接有效！")
                    else:
                        print(f"⚠️  下载链接状态码: {download_response.status_code}")
                except Exception as e:
                    print(f"⚠️  下载链接测试失败: {str(e)}")
            else:
                print("❌ 未生成下载链接")
                
        else:
            print(f"❌ 修复失败: {result.get('error', '未知错误')}")
            
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")

def main():
    """主函数"""
    test_direct_download()

if __name__ == "__main__":
    main() 