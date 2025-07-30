#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""
直接创建正确的剪映草稿文件
确保媒体文件路径配置正确，避免后续修复
"""

import os
import sys
import json
import uuid
import zipfile
import shutil
from datetime import datetime

def create_correct_draft():
    """创建一个包含正确媒体文件路径的剪映草稿文件"""
    print("=== 创建正确的剪映草稿文件 ===")
    
    # 生成草稿ID
    draft_id = f"dfd_cat_{int(datetime.now().timestamp())}_{uuid.uuid4().hex[:8]}"
    print(f"📝 草稿ID: {draft_id}")
    
    # 创建草稿目录结构
    draft_dir = f"./correct_draft_{draft_id}"
    os.makedirs(draft_dir, exist_ok=True)
    
    # 创建assets目录结构
    assets_dir = os.path.join(draft_dir, "assets")
    os.makedirs(os.path.join(assets_dir, "audio"), exist_ok=True)
    os.makedirs(os.path.join(assets_dir, "video"), exist_ok=True)
    os.makedirs(os.path.join(assets_dir, "image"), exist_ok=True)
    
    # 生成唯一ID
    draft_uuid = str(uuid.uuid4()).upper()
    
    # 创建正确的草稿内容
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
        "create_time": int(datetime.now().timestamp()),
        "duration": 5000000,  # 5秒时长
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
            "app_version": "5.9.0",
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
                    "id": "1be9555d8ac23b32ab271d356849b1f7",
                    "intensifies_path": "",
                    "is_ai_clone_tone": False,
                    "is_text_edit_overdub": False,
                    "is_ugc": False,
                    "local_material_id": "1be9555d8ac23b32ab271d356849b1f7",
                    "music_id": "1be9555d8ac23b32ab271d356849b1f7",
                    "name": "audio_9869932344c1c9d3.mp3",
                    # 使用正确的相对路径，相对于草稿文件夹
                    "path": "assets/audio/audio_9869932344c1c9d3.mp3",
                    "remote_url": "https://www.soundjay.com/misc/sounds/bell-ringing-05.wav",
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
                    "update_time": int(datetime.now().timestamp()),
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
            "images": [],
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
                    "id": "2ce9555d8ac23b32ab271d356849b1f8",
                    "intensifies_path": "",
                    "is_ai_clone_tone": False,
                    "is_text_edit_overdub": False,
                    "is_ugc": False,
                    "local_material_id": "2ce9555d8ac23b32ab271d356849b1f8",
                    "music_id": "",
                    "name": "欢迎使用CapCutAPI!",
                    "path": "assets/video/image_81fa0547ac2dcba5.png",
                    "remote_url": "",
                    "query": "",
                    "request_id": "",
                    "resource_id": "",
                    "search_id": "",
                    "source_from": "",
                    "source_platform": 0,
                    "team_id": "",
                    "text_id": "2ce9555d8ac23b32ab271d356849b1f8",
                    "tone_category_id": "",
                    "tone_category_name": "",
                    "tone_effect_id": "",
                    "tone_effect_name": "",
                    "tone_id": "",
                    "tone_name": "",
                    "type": "text",
                    "update_time": int(datetime.now().timestamp()),
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
                        "material_id": "2ce9555d8ac23b32ab271d356849b1f8",
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
                        "material_id": "1be9555d8ac23b32ab271d356849b1f7",
                        "start": 0,
                        "end": 2325333,
                        "duration": 2325333,
                        "type": "audio"
                    }
                ]
            }
        ],
        "update_time": int(datetime.now().timestamp()),
        "version": "5.9.0"
    }
    
    # 创建草稿信息文件
    draft_info = {
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
        "create_time": int(datetime.now().timestamp()),
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
            "app_version": "5.9.0",
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
                    "id": "1be9555d8ac23b32ab271d356849b1f7",
                    "intensifies_path": "",
                    "is_ai_clone_tone": False,
                    "is_text_edit_overdub": False,
                    "is_ugc": False,
                    "local_material_id": "1be9555d8ac23b32ab271d356849b1f7",
                    "music_id": "1be9555d8ac23b32ab271d356849b1f7",
                    "name": "audio_9869932344c1c9d3.mp3",
                    # 使用正确的相对路径
                    "path": "assets/audio/audio_9869932344c1c9d3.mp3",
                    "remote_url": "https://www.soundjay.com/misc/sounds/bell-ringing-05.wav",
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
                    "update_time": int(datetime.now().timestamp()),
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
            "images": [],
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
                    "id": "2ce9555d8ac23b32ab271d356849b1f8",
                    "intensifies_path": "",
                    "is_ai_clone_tone": False,
                    "is_text_edit_overdub": False,
                    "is_ugc": False,
                    "local_material_id": "2ce9555d8ac23b32ab271d356849b1f8",
                    "music_id": "",
                    "name": "欢迎使用CapCutAPI!",
                    "path": "assets/video/image_81fa0547ac2dcba5.png",
                    "remote_url": "",
                    "query": "",
                    "request_id": "",
                    "resource_id": "",
                    "search_id": "",
                    "source_from": "",
                    "source_platform": 0,
                    "team_id": "",
                    "text_id": "2ce9555d8ac23b32ab271d356849b1f8",
                    "tone_category_id": "",
                    "tone_category_name": "",
                    "tone_effect_id": "",
                    "tone_effect_name": "",
                    "tone_id": "",
                    "tone_name": "",
                    "type": "text",
                    "update_time": int(datetime.now().timestamp()),
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
                        "material_id": "2ce9555d8ac23b32ab271d356849b1f8",
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
                        "material_id": "1be9555d8ac23b32ab271d356849b1f7",
                        "start": 0,
                        "end": 2325333,
                        "duration": 2325333,
                        "type": "audio"
                    }
                ]
            }
        ],
        "update_time": int(datetime.now().timestamp()),
        "version": "5.9.0"
    }
    
    # 创建草稿元信息文件
    draft_meta_info = {
        "draft_id": draft_id,
        "draft_name": f"CapCutAPI草稿_{int(datetime.now().timestamp())}",
        "create_time": int(datetime.now().timestamp()),
        "update_time": int(datetime.now().timestamp()),
        "version": "5.9.0",
        "platform": "windows"
    }
    
    # 保存文件
    with open(os.path.join(draft_dir, "draft_content.json"), "w", encoding="utf-8") as f:
        json.dump(draft_content, f, ensure_ascii=False, indent=4)
    
    with open(os.path.join(draft_dir, "draft_info.json"), "w", encoding="utf-8") as f:
        json.dump(draft_info, f, ensure_ascii=False, indent=4)
    
    with open(os.path.join(draft_dir, "draft_meta_info.json"), "w", encoding="utf-8") as f:
        json.dump(draft_meta_info, f, ensure_ascii=False, indent=4)
    
    # 复制媒体文件到正确位置
    if os.path.exists("assets/audio/audio_9869932344c1c9d3.mp3"):
        shutil.copy2("assets/audio/audio_9869932344c1c9d3.mp3", 
                     os.path.join(assets_dir, "audio", "audio_9869932344c1c9d3.mp3"))
        print("✓ 音频文件已复制")
    
    if os.path.exists("assets/video/image_81fa0547ac2dcba5.png"):
        shutil.copy2("assets/video/image_81fa0547ac2dcba5.png", 
                     os.path.join(assets_dir, "video", "image_81fa0547ac2dcba5.png"))
        print("✓ 图片文件已复制")
    
    # 创建ZIP文件
    zip_filename = f"{draft_id}.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(draft_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, draft_dir)
                zipf.write(file_path, arcname)
    
    print(f"✓ 草稿文件已创建: {zip_filename}")
    print(f"📁 草稿目录: {draft_dir}")
    
    # 清理临时目录
    shutil.rmtree(draft_dir)
    print("🧹 临时目录已清理")
    
    return zip_filename

def main():
    """主函数"""
    try:
        zip_filename = create_correct_draft()
        print(f"\n✅ 正确的草稿文件创建完成: {zip_filename}")
        print("\n📋 使用说明:")
        print("1. 将生成的ZIP文件复制到剪映的草稿目录")
        print("2. 重启剪映软件")
        print("3. 在剪映中打开草稿，媒体文件应该能正常显示")
        print("\n💡 优势:")
        print("- 直接生成正确的文件结构")
        print("- 媒体文件路径配置正确")
        print("- 无需后续修复")
        print("- 剪映可以直接识别和使用")
        
    except Exception as e:
        print(f"❌ 创建草稿文件失败: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    main()