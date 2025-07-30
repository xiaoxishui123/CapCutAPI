#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from create_draft import create_draft
from add_video_track import add_video_track
from save_draft_impl import save_draft_impl
import logging
import time

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_add_content():
    """测试添加内容到草稿"""
    print("=== 添加内容测试 ===")
    
    try:
        # 步骤1：创建草稿
        print("\n📝 步骤1：创建草稿...")
        script, draft_id = create_draft(width=1080, height=1920)
        print(f"✅ 草稿创建成功! draft_id: {draft_id}")
        
        # 步骤2：添加视频内容
        print("\n🎬 步骤2：添加视频内容...")
        video_result = add_video_track(
            video_url="https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4",
            draft_id=draft_id,
            start=0,
            end=5,  # 5秒视频
            target_start=0,
            track_name="main"
        )
        
        if video_result.get("success"):
            print("✅ 视频添加成功!")
        else:
            print(f"❌ 视频添加失败: {video_result.get('error', '未知错误')}")
            return False
        
        # 步骤3：保存草稿
        print("\n💾 步骤3：保存草稿...")
        result = save_draft_impl(draft_id)
        
        if result.get("success"):
            print("✅ 草稿保存成功!")
            print(f"📁 草稿文件夹: {draft_id}")
            print(f"📋 请将 {draft_id} 文件夹复制到剪映草稿目录")
            return True
        else:
            print(f"❌ 草稿保存失败: {result.get('error', '未知错误')}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        logger.error(f"测试失败", exc_info=True)
        return False

if __name__ == "__main__":
    test_add_content() 