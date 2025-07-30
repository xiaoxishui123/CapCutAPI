#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试修复器的远程下载功能
"""

import sys
import os
sys.path.append('.')

from smart_draft_fixer import SmartDraftFixer

def test_remote_download():
    """测试远程文件下载功能"""
    print("🎯 直接测试修复器远程下载功能")
    print("=" * 50)
    
    # 创建修复器实例
    draft_url = "http://zdaigfpt.oss-cn-wuhan-lr.aliyuncs.com/dfd_cat_1753754237_75267d20.zip?OSSAccessKeyId=LTAI5tLhTQGk2Di25ArrkgGG&Expires=1753840685&Signature=RK%2Bzp7ZvezNN%2FFw5mMUc9DQPBdY%3D"
    fixer = SmartDraftFixer(draft_url)
    
    try:
        # 下载并解压
        print("📥 下载并解压草稿...")
        if not fixer.download_and_extract():
            print("❌ 下载失败")
            return
        
        # 测试远程文件下载
        print("🔧 测试远程文件下载...")
        result = fixer._fix_media_paths()
        print(f"📊 修复结果: {result}")
        
        # 检查是否下载了音频文件
        audio_path = os.path.join(fixer.draft_path, "assets/audio/audio_9869932344c1c9d3.mp3")
        if os.path.exists(audio_path):
            print(f"✅ 音频文件已下载: {audio_path}")
            print(f"📏 文件大小: {os.path.getsize(audio_path)} bytes")
        else:
            print(f"❌ 音频文件未下载: {audio_path}")
        
        # 清理
        fixer.cleanup()
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

def main():
    """主函数"""
    test_remote_download()

if __name__ == "__main__":
    main() 