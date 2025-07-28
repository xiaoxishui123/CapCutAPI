#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from create_draft import create_draft
from add_text_impl import add_text_impl
from save_draft_impl import save_draft_impl
import json
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_debug_content():
    """调试文本内容添加和保存"""
    print("=== 调试文本内容测试 ===")
    
    try:
        # 步骤1：创建草稿
        print("\n📝 步骤1：创建草稿...")
        script, draft_id = create_draft(width=1080, height=1920)
        print(f"✅ 草稿创建成功! draft_id: {draft_id}")
        
        # 检查初始草稿内容
        print(f"\n🔍 检查初始草稿内容...")
        print(f"轨道数量: {len(script.tracks)}")
        print(f"素材数量: {len(script.materials.texts)}")
        
        # 步骤2：添加文本内容
        print("\n📝 步骤2：添加文本内容...")
        text_result = add_text_impl(
            text="Hello World!",
            draft_id=draft_id,
            start=0,
            end=3,  # 3秒显示时间
            font="HarmonyOS_Sans_SC_Regular",
            font_color="#FF0000",
            font_size=30.0,
            track_name="main"
        )
        
        if text_result.get("draft_id"):
            print("✅ 文本添加成功!")
            print(f"草稿ID: {text_result.get('draft_id')}")
        else:
            print(f"❌ 文本添加失败: {text_result}")
            return False
        
        # 检查添加文本后的草稿内容
        print(f"\n🔍 检查添加文本后的草稿内容...")
        print(f"轨道数量: {len(script.tracks)}")
        print(f"文本素材数量: {len(script.materials.texts)}")
        
        # 打印轨道信息
        for track_name, track in script.tracks.items():
            print(f"轨道: {track_name}, 类型: {track.track_type}, 片段数量: {len(track.segments)}")
            for i, segment in enumerate(track.segments):
                print(f"  片段 {i}: {type(segment).__name__}")
                if hasattr(segment, 'text'):
                    print(f"    文本内容: {segment.text}")
        
        # 步骤3：保存草稿
        print("\n💾 步骤3：保存草稿...")
        result = save_draft_impl(draft_id)
        
        if result.get("success"):
            print("✅ 草稿保存成功!")
            print(f"📁 草稿文件夹: {draft_id}")
            
            # 检查保存后的文件内容
            print(f"\n🔍 检查保存后的文件内容...")
            draft_content_path = f"{draft_id}/draft_content.json"
            if os.path.exists(draft_content_path):
                with open(draft_content_path, 'r', encoding='utf-8') as f:
                    content = json.load(f)
                    print(f"轨道数量: {len(content.get('tracks', []))}")
                    print(f"文本素材数量: {len(content.get('materials', {}).get('texts', []))}")
                    print(f"草稿时长: {content.get('duration', 0)}")
                    
                    # 打印轨道详情
                    tracks = content.get('tracks', [])
                    for track in tracks:
                        print(f"轨道: {track.get('name', 'unknown')}, 片段数量: {len(track.get('segments', []))}")
            else:
                print(f"❌ 草稿内容文件不存在: {draft_content_path}")
            
            return True
        else:
            print(f"❌ 草稿保存失败: {result.get('error', '未知错误')}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        logger.error(f"测试失败", exc_info=True)
        return False

if __name__ == "__main__":
    test_debug_content() 