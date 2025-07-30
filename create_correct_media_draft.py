#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""
创建使用正确媒体类型的剪映草稿文件
解决音频和视频文件识别问题
"""

import os
import sys
import json
import uuid
import zipfile
import shutil
from datetime import datetime

def create_correct_media_draft():
    """创建一个使用正确媒体类型的剪映草稿文件"""
    print("🎬 创建使用正确媒体类型的剪映草稿文件")
    print("=" * 50)
    
    # 生成草稿ID
    timestamp = int(datetime.now().timestamp())
    draft_id = f"dfd_cat_{timestamp}_{uuid.uuid4().hex[:8]}"
    print(f"📝 草稿ID: {draft_id}")
    
    # 创建草稿目录结构
    draft_dir = f"./correct_media_{draft_id}"
    os.makedirs(draft_dir, exist_ok=True)
    
    # 创建assets目录结构
    assets_dir = os.path.join(draft_dir, "assets")
    os.makedirs(os.path.join(assets_dir, "audio"), exist_ok=True)
    os.makedirs(os.path.join(assets_dir, "video"), exist_ok=True)
    os.makedirs(os.path.join(assets_dir, "image"), exist_ok=True)
    
    print("📁 目录结构已创建")
    
    # 生成唯一ID
    draft_uuid = str(uuid.uuid4()).upper()
    audio_id = str(uuid.uuid4()).replace("-", "")[:32]
    video_id = str(uuid.uuid4()).replace("-", "")[:32]
    text_id = str(uuid.uuid4()).replace("-", "")[:32]
    
    # 使用相对路径，但确保路径格式正确
    audio_path = "assets/audio/audio_9869932344c1c9d3.mp3"
    video_path = "assets/video/sample_video.mp4"  # 使用视频文件路径
    image_path = "assets/image/image_81fa0547ac2dcba5.png"
    
    print(f"🔗 音频路径: {audio_path}")
    print(f"🔗 视频路径: {video_path}")
    print(f"🔗 图片路径: {image_path}")
    
    # 创建草稿内容 - 使用正确的媒体类型
    draft_content = {
        "canvas_config": {
            "width": 1080,
            "height": 1920,
            "ratio": "original"
        },
        "color_space": -1,
        "config": {
            "adjust_max_index": 1,
            "attachment_info": [],
            "combination_max_index": 1,
            "export_range": None,
            "extract_audio_last_index": 1,
            "lyrics_recognition_id": "",
            "lyrics_sync": True,
            "lyrics_taskinfo": [],
            "maintrack_adsorb": True,
            "material_save_mode": 0,
            "multi_language_current": "none",
            "multi_language_list": [],
            "multi_language_main": "none",
            "multi_language_mode": "none",
            "original_sound_last_index": 1,
            "record_audio_last_index": 1,
            "sticker_max_index": 1,
            "subtitle_keywords_config": None,
            "subtitle_recognition_id": "",
            "subtitle_sync": True,
            "subtitle_taskinfo": [],
            "system_font_list": [],
            "video_mute": False,
            "zoom_info_params": None
        },
        "cover": None,
        "create_time": timestamp,
        "duration": 5000000,
        "extra_info": None,
        "fps": 30.0,
        "free_render_index_mode_on": False,
        "group_container": None,
        "id": draft_uuid,
        "keyframe_graph_list": [],
        "keyframes": {
            "adjusts": [],
            "audios": [],
            "effects": [],
            "filters": [],
            "handwrites": [],
            "stickers": [],
            "texts": [],
            "videos": []
        },
        "last_modified_platform": {
            "app_id": 3704,
            "app_source": "lv",
            "app_version": "8.7.0",
            "device_id": str(uuid.uuid4()).replace("-", "")[:32],
            "hard_disk_id": str(uuid.uuid4()).replace("-", "")[:32],
            "mac_address": str(uuid.uuid4()).replace("-", "")[:32],
            "os": "windows",
            "os_version": "10.0.19045"
        },
        "materials": {
            "ai_translates": [],
            "audio_balances": [],
            "audio_effects": [],
            "audio_fades": [],
            "audio_track_indexes": [],
            "audios": [
                {
                    "app_id": 0,
                    "category_id": "",
                    "category_name": "local",
                    "check_flag": 1,
                    "copyright_limit_type": "none",
                    "duration": 2325333,
                    "effect_id": "",
                    "formula_id": "",
                    "id": audio_id,
                    "intensifies_path": "",
                    "is_ai_clone_tone": False,
                    "is_text_edit_overdub": False,
                    "is_ugc": False,
                    "local_material_id": audio_id,
                    "music_id": audio_id,
                    "name": "audio_9869932344c1c9d3.mp3",
                    "path": audio_path,
                    "remote_url": "",
                    "query": "",
                    "request_id": "",
                    "resource_id": "",
                    "search_id": "",
                    "source_from": "",
                    "source_platform": 0,
                    "team_id": "",
                    "text_id": "",
                    "tone_category_id": "",
                    "tone_category_name": "",
                    "tone_effect_id": "",
                    "tone_effect_name": "",
                    "tone_id": "",
                    "tone_name": "",
                    "type": "audio",
                    "update_time": timestamp,
                    "user_id": "",
                    "video_id": ""
                }
            ],
            "beats": [],
            "canvases": [],
            "chromas": [],
            "color_curves": [],
            "color_gradings": [],
            "color_wheels": [],
            "effects": [],
            "filters": [],
            "handwrites": [],
            "images": [
                {
                    "app_id": 0,
                    "category_id": "",
                    "category_name": "local",
                    "check_flag": 1,
                    "copyright_limit_type": "none",
                    "duration": 3000000,
                    "effect_id": "",
                    "formula_id": "",
                    "id": video_id,
                    "intensifies_path": "",
                    "is_ai_clone_tone": False,
                    "is_text_edit_overdub": False,
                    "is_ugc": False,
                    "local_material_id": video_id,
                    "music_id": "",
                    "name": "image_81fa0547ac2dcba5.png",
                    "path": image_path,
                    "remote_url": "",
                    "query": "",
                    "request_id": "",
                    "resource_id": "",
                    "search_id": "",
                    "source_from": "",
                    "source_platform": 0,
                    "team_id": "",
                    "text_id": "",
                    "tone_category_id": "",
                    "tone_category_name": "",
                    "tone_effect_id": "",
                    "tone_effect_name": "",
                    "tone_id": "",
                    "tone_name": "",
                    "type": "image",
                    "update_time": timestamp,
                    "user_id": "",
                    "video_id": ""
                }
            ],
            "luts": [],
            "masks": [],
            "motions": [],
            "particles": [],
            "shapes": [],
            "stickers": [],
            "texts": [
                {
                    "app_id": 0,
                    "category_id": "",
                    "category_name": "local",
                    "check_flag": 1,
                    "copyright_limit_type": "none",
                    "duration": 3000000,
                    "effect_id": "",
                    "formula_id": "",
                    "id": text_id,
                    "intensifies_path": "",
                    "is_ai_clone_tone": False,
                    "is_text_edit_overdub": False,
                    "is_ugc": False,
                    "local_material_id": text_id,
                    "music_id": "",
                    "name": "欢迎使用CapCutAPI!",
                    "path": image_path,  # 文本使用图片作为背景
                    "remote_url": "",
                    "query": "",
                    "request_id": "",
                    "resource_id": "",
                    "search_id": "",
                    "source_from": "",
                    "source_platform": 0,
                    "team_id": "",
                    "text_id": text_id,
                    "tone_category_id": "",
                    "tone_category_name": "",
                    "tone_effect_id": "",
                    "tone_effect_name": "",
                    "tone_id": "",
                    "tone_name": "",
                    "type": "text",
                    "update_time": timestamp,
                    "user_id": "",
                    "video_id": ""
                }
            ],
            "videos": []
        },
        "platform": "windows",
        "ratio": "original",
        "resolution": "original",
        "speed": 1.0,
        "tracks": [
            {
                "id": "main_track",
                "type": "video",
                "segments": [
                    {
                        "id": "segment_1",
                        "material_id": video_id,
                        "start": 0,
                        "end": 3000000,
                        "duration": 3000000,
                        "type": "image"
                    },
                    {
                        "id": "segment_2",
                        "material_id": text_id,
                        "start": 0,
                        "end": 3000000,
                        "duration": 3000000,
                        "type": "text"
                    }
                ]
            },
            {
                "id": "audio_track",
                "type": "audio",
                "segments": [
                    {
                        "id": "audio_segment_1",
                        "material_id": audio_id,
                        "start": 0,
                        "end": 2325333,
                        "duration": 2325333,
                        "type": "audio"
                    }
                ]
            }
        ],
        "update_time": timestamp,
        "version": "8.7.0"
    }
    
    # 创建草稿信息文件 - 与draft_content.json相同
    draft_info = draft_content.copy()
    
    # 创建草稿元信息文件
    draft_meta_info = {
        "draft_id": draft_id,
        "draft_name": f"CapCutAPI正确媒体类型草稿_{timestamp}",
        "create_time": timestamp,
        "update_time": timestamp,
        "version": "8.7.0",
        "platform": "windows"
    }
    
    # 保存文件
    print("💾 保存配置文件...")
    with open(os.path.join(draft_dir, "draft_content.json"), "w", encoding="utf-8") as f:
        json.dump(draft_content, f, ensure_ascii=False, indent=4)
    
    with open(os.path.join(draft_dir, "draft_info.json"), "w", encoding="utf-8") as f:
        json.dump(draft_info, f, ensure_ascii=False, indent=4)
    
    with open(os.path.join(draft_dir, "draft_meta_info.json"), "w", encoding="utf-8") as f:
        json.dump(draft_meta_info, f, ensure_ascii=False, indent=4)
    
    print("✓ 配置文件已保存")
    
    # 复制媒体文件到正确位置
    print("📁 复制媒体文件...")
    
    # 复制音频文件
    if os.path.exists("assets/audio/audio_9869932344c1c9d3.mp3"):
        shutil.copy2("assets/audio/audio_9869932344c1c9d3.mp3", 
                     os.path.join(assets_dir, "audio", "audio_9869932344c1c9d3.mp3"))
        print("✓ 音频文件已复制: audio_9869932344c1c9d3.mp3")
    else:
        print("⚠️  音频文件不存在: assets/audio/audio_9869932344c1c9d3.mp3")
    
    # 复制图片文件到image目录（作为图片使用）
    if os.path.exists("assets/image/image_81fa0547ac2dcba5.png"):
        shutil.copy2("assets/image/image_81fa0547ac2dcba5.png", 
                     os.path.join(assets_dir, "image", "image_81fa0547ac2dcba5.png"))
        print("✓ 图片文件已复制: image_81fa0547ac2dcba5.png")
    else:
        print("⚠️  图片文件不存在: assets/image/image_81fa0547ac2dcba5.png")
    
    # 创建一个简单的视频文件（使用ffmpeg生成）
    print("🎥 创建示例视频文件...")
    try:
        # 使用ffmpeg创建一个简单的测试视频
        video_output = os.path.join(assets_dir, "video", "sample_video.mp4")
        ffmpeg_cmd = f'ffmpeg -f lavfi -i testsrc=duration=3:size=640x480:rate=30 -f lavfi -i sine=frequency=1000:duration=3 -c:v libx264 -c:a aac -shortest {video_output} -y'
        os.system(ffmpeg_cmd)
        
        if os.path.exists(video_output):
            print("✓ 示例视频文件已创建: sample_video.mp4")
        else:
            print("⚠️  视频文件创建失败，使用图片文件代替")
            # 如果ffmpeg失败，复制图片文件到video目录
            if os.path.exists("assets/image/image_81fa0547ac2dcba5.png"):
                shutil.copy2("assets/image/image_81fa0547ac2dcba5.png", 
                             os.path.join(assets_dir, "video", "sample_video.mp4"))
                print("✓ 使用图片文件代替视频文件")
    except Exception as e:
        print(f"⚠️  视频文件创建失败: {e}")
        # 使用图片文件代替
        if os.path.exists("assets/image/image_81fa0547ac2dcba5.png"):
            shutil.copy2("assets/image/image_81fa0547ac2dcba5.png", 
                         os.path.join(assets_dir, "video", "sample_video.mp4"))
            print("✓ 使用图片文件代替视频文件")
    
    # 创建ZIP文件
    print("📦 创建ZIP文件...")
    zip_filename = f"{draft_id}.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(draft_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, draft_dir)
                zipf.write(file_path, arcname)
    
    print(f"✓ ZIP文件已创建: {zip_filename}")
    
    # 显示文件结构
    print("\n📋 文件结构:")
    for root, dirs, files in os.walk(draft_dir):
        level = root.replace(draft_dir, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f"{subindent}{file}")
    
    # 清理临时目录
    shutil.rmtree(draft_dir)
    print("🧹 临时目录已清理")
    
    return zip_filename

def main():
    """主函数"""
    try:
        print("🎬 开始创建使用正确媒体类型的剪映草稿文件...")
        zip_filename = create_correct_media_draft()
        
        print(f"\n✅ 正确媒体类型草稿文件创建完成!")
        print(f"📁 文件名: {zip_filename}")
        print(f"📊 文件大小: {os.path.getsize(zip_filename) / 1024:.1f} KB")
        
        print("\n📋 使用说明:")
        print("1. 将生成的ZIP文件解压到: F:\\jianyin\\cgwz\\JianyingPro Drafts\\")
        print("2. 重启剪映专业版软件")
        print("3. 在剪映中打开草稿，音频和图片应该能正确识别")
        
        print("\n💡 正确媒体类型草稿的优势:")
        print("- ✅ 使用正确的媒体文件类型")
        print("- ✅ 音频文件使用MP3格式")
        print("- ✅ 图片文件使用PNG格式")
        print("- ✅ 尝试创建真正的视频文件")
        print("- ✅ 相对路径格式正确")
        
        print(f"\n🎉 草稿文件已准备就绪: {zip_filename}")
        
    except Exception as e:
        print(f"❌ 创建草稿文件失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    main()