#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""
创建包含所有媒体文件的完整工作草稿
基于正常工作的草稿文件格式，包含音频、视频、图片
"""

import os
import sys
import json
import uuid
import zipfile
import shutil
from datetime import datetime

def create_complete_working_draft():
    """创建包含所有媒体文件的完整工作草稿"""
    print("🎬 创建包含所有媒体文件的完整工作草稿")
    print("=" * 50)
    
    # 生成草稿ID
    timestamp = int(datetime.now().timestamp())
    draft_id = f"dfd_cat_{timestamp}_{uuid.uuid4().hex[:8]}"
    print(f"📝 草稿ID: {draft_id}")
    
    # 创建草稿目录结构
    draft_dir = f"./complete_draft_{draft_id}"
    os.makedirs(draft_dir, exist_ok=True)
    
    # 创建.res目录结构
    res_dir = os.path.join(draft_dir, ".res")
    os.makedirs(res_dir, exist_ok=True)
    
    print("📁 目录结构已创建")
    
    # 生成唯一ID
    draft_uuid = str(uuid.uuid4()).upper()
    audio_id = str(uuid.uuid4()).upper()
    video_id = str(uuid.uuid4()).upper()
    image_id = str(uuid.uuid4()).upper()
    
    # 使用绝对路径格式
    user_draft_path = f"F:\\jianyin\\cgwz\\JianyingPro Drafts\\{draft_id}"
    audio_path = f"{user_draft_path}\\.res\\audio_9869932344c1c9d3.mp3"
    video_path = f"{user_draft_path}\\.res\\sample_video.mp4"
    image_path = f"{user_draft_path}\\.res\\image_81fa0547ac2dcba5.png"
    
    print(f"🔗 用户草稿路径: {user_draft_path}")
    print(f"🔗 音频路径: {audio_path}")
    print(f"🔗 视频路径: {video_path}")
    print(f"🔗 图片路径: {image_path}")
    
    # 创建草稿内容 - 包含所有媒体类型
    draft_content = {
        "canvas_config": {
            "width": 1920,
            "height": 1080,
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
            "original_sound_last_index": 1,
            "record_audio_last_index": 1,
            "sticker_max_index": 1,
            "subtitle_recognition_id": "",
            "subtitle_sync": True,
            "subtitle_taskinfo": [],
            "system_font_list": [],
            "video_mute": False,
            "zoom_info_params": None
        },
        "cover": None,
        "create_time": timestamp,
        "duration": 8000000,  # 8秒
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
            "app_version": "4.4.0",
            "device_id": str(uuid.uuid4()).replace("-", "")[:32],
            "hard_disk_id": str(uuid.uuid4()).replace("-", "")[:32],
            "mac_address": str(uuid.uuid4()).replace("-", "")[:32],
            "os": "windows",
            "os_version": "10.0.22621"
        },
        "materials": {
            "audio_balances": [],
            "audio_effects": [],
            "audio_fades": [],
            "audios": [
                {
                    "app_id": 0,
                    "category_id": "",
                    "category_name": "local",
                    "check_flag": 1,
                    "copyright_limit_type": "none",
                    "duration": 5000000,  # 5秒
                    "effect_id": "",
                    "formula_id": "",
                    "id": audio_id,
                    "intensifies_path": "",
                    "is_ai_clone_tone": False,
                    "is_text_edit_overdub": False,
                    "is_ugc": False,
                    "local_material_id": audio_id,
                    "music_id": "",
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
            "canvases": [
                {
                    "album_image": "",
                    "blur": 0.0,
                    "color": "",
                    "id": str(uuid.uuid4()).upper(),
                    "image": "",
                    "image_id": "",
                    "image_name": "",
                    "source_platform": 0,
                    "team_id": "",
                    "type": "canvas_color"
                }
            ],
            "chromas": [],
            "color_curves": [],
            "digital_humans": [],
            "drafts": [],
            "effects": [],
            "green_screens": [],
            "handwrites": [],
            "hsl": [],
            "images": [
                {
                    "app_id": 0,
                    "category_id": "",
                    "category_name": "local",
                    "check_flag": 1,
                    "copyright_limit_type": "none",
                    "duration": 3000000,  # 3秒
                    "effect_id": "",
                    "formula_id": "",
                    "height": 1080,
                    "id": image_id,
                    "intensifies_path": "",
                    "is_ai_clone_tone": False,
                    "is_text_edit_overdub": False,
                    "is_ugc": False,
                    "local_material_id": image_id,
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
                    "video_id": "",
                    "width": 1920
                }
            ],
            "log_color_wheels": [],
            "manual_deformations": [],
            "masks": [],
            "material_animations": [],
            "material_colors": [],
            "placeholders": [],
            "plugin_effects": [],
            "primary_color_wheels": [],
            "realtime_denoises": [],
            "shapes": [],
            "smart_crops": [],
            "sound_channel_mappings": [
                {
                    "audio_channel_mapping": 0,
                    "id": str(uuid.uuid4()).upper(),
                    "is_config_open": False,
                    "type": "none"
                }
            ],
            "speeds": [
                {
                    "curve_speed": None,
                    "id": str(uuid.uuid4()).upper(),
                    "mode": 0,
                    "speed": 1.0,
                    "type": "speed"
                }
            ],
            "stickers": [],
            "tail_leaders": [],
            "text_templates": [],
            "texts": [],
            "transitions": [],
            "video_effects": [],
            "video_trackings": [],
            "videos": [
                {
                    "audio_fade": None,
                    "cartoon_path": "",
                    "category_id": "",
                    "category_name": "local",
                    "check_flag": 63487,
                    "crop": {
                        "lower_left_x": 0.0,
                        "lower_left_y": 1.0,
                        "lower_right_x": 1.0,
                        "lower_right_y": 1.0,
                        "upper_left_x": 0.0,
                        "upper_left_y": 0.0,
                        "upper_right_x": 1.0,
                        "upper_right_y": 0.0
                    },
                    "crop_ratio": "free",
                    "crop_scale": 1.0,
                    "duration": 3000000,  # 3秒
                    "extra_type_option": 0,
                    "formula_id": "",
                    "freeze": None,
                    "gameplay": None,
                    "has_audio": True,
                    "height": 1080,
                    "id": video_id,
                    "intensifies_audio_path": "",
                    "intensifies_path": "",
                    "is_ai_generate_content": False,
                    "is_unified_beauty_mode": False,
                    "local_id": "",
                    "local_material_id": video_id,
                    "material_id": "",
                    "material_name": "sample_video",
                    "material_url": "",
                    "matting": {
                        "flag": 0,
                        "has_use_quick_brush": False,
                        "has_use_quick_eraser": False,
                        "interactiveTime": [],
                        "path": "",
                        "strokes": []
                    },
                    "media_path": "",
                    "object_locked": None,
                    "origin_material_id": "",
                    "path": video_path,
                    "picture_from": "none",
                    "picture_set_category_id": "",
                    "picture_set_category_name": "",
                    "request_id": "",
                    "reverse_intensifies_path": "",
                    "reverse_path": "",
                    "smart_motion": None,
                    "source": 0,
                    "source_platform": 0,
                    "stable": None,
                    "team_id": "",
                    "type": "video",
                    "video_algorithm": {
                        "algorithms": [],
                        "deflicker": None,
                        "motion_blur_config": None,
                        "noise_reduction": None,
                        "path": "",
                        "time_range": None
                    },
                    "width": 1920
                }
            ]
        },
        "mutable_config": None,
        "name": "",
        "new_version": "79.0.0",
        "platform": {
            "app_id": 3704,
            "app_source": "lv",
            "app_version": "4.4.0",
            "device_id": str(uuid.uuid4()).replace("-", "")[:32],
            "hard_disk_id": str(uuid.uuid4()).replace("-", "")[:32],
            "mac_address": str(uuid.uuid4()).replace("-", "")[:32],
            "os": "windows",
            "os_version": "10.0.22621"
        },
        "relationships": [],
        "render_index_track_mode_on": False,
        "retouch_cover": None,
        "source": "default",
        "static_cover_image_path": "",
        "tracks": [
            {
                "attribute": 0,
                "flag": 0,
                "id": str(uuid.uuid4()).upper(),
                "segments": [
                    {
                        "cartoon": False,
                        "clip": {
                            "alpha": 1.0,
                            "flip": {
                                "horizontal": False,
                                "vertical": False
                            },
                            "rotation": 0.0,
                            "scale": {
                                "x": 1.0,
                                "y": 1.0
                            },
                            "transform": {
                                "x": 0.0,
                                "y": 0.0
                            }
                        },
                        "common_keyframes": [],
                        "enable_adjust": True,
                        "enable_color_curves": True,
                        "enable_color_wheels": True,
                        "enable_lut": True,
                        "enable_smart_color_adjust": False,
                        "extra_material_refs": [],
                        "group_id": "",
                        "hdr_settings": {
                            "intensity": 1.0,
                            "mode": 1,
                            "nits": 1000
                        },
                        "id": str(uuid.uuid4()).upper(),
                        "intensifies_audio": False,
                        "is_placeholder": False,
                        "is_tone_modify": False,
                        "keyframe_refs": [],
                        "last_nonzero_volume": 1.0,
                        "material_id": video_id,
                        "render_index": 0,
                        "reverse": False,
                        "source_timerange": {
                            "duration": 3000000,
                            "start": 0
                        },
                        "speed": 1.0,
                        "target_timerange": {
                            "duration": 3000000.0,
                            "start": 0
                        },
                        "template_id": "",
                        "template_scene": "default",
                        "track_attribute": 0,
                        "track_render_index": 0,
                        "uniform_scale": {
                            "on": True,
                            "value": 1.0
                        },
                        "visible": True,
                        "volume": 1.0
                    }
                ],
                "type": "video"
            },
            {
                "attribute": 1,  # 音频轨道
                "flag": 0,
                "id": str(uuid.uuid4()).upper(),
                "segments": [
                    {
                        "cartoon": False,
                        "clip": {
                            "alpha": 1.0,
                            "flip": {
                                "horizontal": False,
                                "vertical": False
                            },
                            "rotation": 0.0,
                            "scale": {
                                "x": 1.0,
                                "y": 1.0
                            },
                            "transform": {
                                "x": 0.0,
                                "y": 0.0
                            }
                        },
                        "common_keyframes": [],
                        "enable_adjust": True,
                        "enable_color_curves": True,
                        "enable_color_wheels": True,
                        "enable_lut": True,
                        "enable_smart_color_adjust": False,
                        "extra_material_refs": [],
                        "group_id": "",
                        "hdr_settings": {
                            "intensity": 1.0,
                            "mode": 1,
                            "nits": 1000
                        },
                        "id": str(uuid.uuid4()).upper(),
                        "intensifies_audio": False,
                        "is_placeholder": False,
                        "is_tone_modify": False,
                        "keyframe_refs": [],
                        "last_nonzero_volume": 1.0,
                        "material_id": audio_id,
                        "render_index": 0,
                        "reverse": False,
                        "source_timerange": {
                            "duration": 5000000,
                            "start": 0
                        },
                        "speed": 1.0,
                        "target_timerange": {
                            "duration": 5000000.0,
                            "start": 0
                        },
                        "template_id": "",
                        "template_scene": "default",
                        "track_attribute": 1,
                        "track_render_index": 0,
                        "uniform_scale": {
                            "on": True,
                            "value": 1.0
                        },
                        "visible": True,
                        "volume": 1.0
                    }
                ],
                "type": "audio"
            }
        ],
        "update_time": timestamp,
        "version": 360000
    }
    
    # 创建草稿信息文件
    draft_info = draft_content.copy()
    
    # 创建草稿元信息文件
    draft_meta_info = {
        "draft_cloud_capcut_purchase_info": "",
        "draft_cloud_last_action_download": False,
        "draft_cloud_materials": [],
        "draft_cloud_purchase_info": "",
        "draft_cloud_template_id": "",
        "draft_cloud_tutorial_info": "",
        "draft_cloud_videocut_purchase_info": "",
        "draft_cover": "draft_cover.jpg",
        "draft_deeplink_url": "",
        "draft_enterprise_info": {
            "draft_enterprise_extra": "",
            "draft_enterprise_id": "",
            "draft_enterprise_name": ""
        },
        "draft_fold_path": f"C:/Users/Administrator/AppData/Local/JianyingPro/User Data/Projects/com.lveditor.draft/{draft_id}",
        "draft_id": draft_uuid,
        "draft_is_article_video_draft": False,
        "draft_is_from_deeplink": "false",
        "draft_materials": [
            {
                "type": 0,  # 视频
                "value": [
                    {
                        "create_time": timestamp,
                        "duration": 3000000,
                        "extra_info": "sample_video",
                        "file_Path": video_path,
                        "height": 1080,
                        "id": video_id,
                        "import_time": timestamp,
                        "import_time_ms": timestamp * 1000,
                        "md5": "",
                        "metetype": "video",
                        "roughcut_time_range": {
                            "duration": 0,
                            "start": 0
                        },
                        "sub_time_range": {
                            "duration": -1,
                            "start": -1
                        },
                        "type": 0,
                        "width": 1920
                    }
                ]
            },
            {
                "type": 1,  # 音频
                "value": [
                    {
                        "create_time": timestamp,
                        "duration": 5000000,
                        "extra_info": "audio_9869932344c1c9d3",
                        "file_Path": audio_path,
                        "height": 0,
                        "id": audio_id,
                        "import_time": timestamp,
                        "import_time_ms": timestamp * 1000,
                        "md5": "",
                        "metetype": "audio",
                        "roughcut_time_range": {
                            "duration": 0,
                            "start": 0
                        },
                        "sub_time_range": {
                            "duration": -1,
                            "start": -1
                        },
                        "type": 1,
                        "width": 0
                    }
                ]
            },
            {
                "type": 2,  # 图片
                "value": [
                    {
                        "create_time": timestamp,
                        "duration": 3000000,
                        "extra_info": "image_81fa0547ac2dcba5",
                        "file_Path": image_path,
                        "height": 1080,
                        "id": image_id,
                        "import_time": timestamp,
                        "import_time_ms": timestamp * 1000,
                        "md5": "",
                        "metetype": "image",
                        "roughcut_time_range": {
                            "duration": 0,
                            "start": 0
                        },
                        "sub_time_range": {
                            "duration": -1,
                            "start": -1
                        },
                        "type": 2,
                        "width": 1920
                    }
                ]
            },
            {"type": 3, "value": []},
            {"type": 6, "value": []},
            {"type": 7, "value": []},
            {"type": 8, "value": []}
        ],
        "draft_materials_copied_info": [],
        "draft_name": f"CapCutAPI完整草稿_{timestamp}",
        "draft_new_version": "",
        "draft_removable_storage_device": f"C:\\Users\\Administrator\\AppData\\Local\\JianyingPro\\User Data\\Projects\\com.lveditor.draft",
        "draft_root_path": f"C:\\Users\\Administrator\\AppData\\Local\\JianyingPro\\User Data\\Projects\\com.lveditor.draft",
        "draft_segment_extra_info": [],
        "draft_timeline_materials_size_": 7540,
        "tm_draft_cloud_completed": "",
        "tm_draft_cloud_modified": 0,
        "tm_draft_create": timestamp * 1000000,
        "tm_draft_modified": timestamp * 1000000,
        "tm_duration": 8000000.0,
        "id": str(uuid.uuid4()).upper(),
        "draft_timeline_metetyperials_size_": 0
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
    
    # 复制媒体文件到.res目录
    print("📁 复制媒体文件到.res目录...")
    
    # 复制音频文件
    if os.path.exists("assets/audio/audio_9869932344c1c9d3.mp3"):
        shutil.copy2("assets/audio/audio_9869932344c1c9d3.mp3", 
                     os.path.join(res_dir, "audio_9869932344c1c9d3.mp3"))
        print("✓ 音频文件已复制: audio_9869932344c1c9d3.mp3")
    else:
        print("⚠️  音频文件不存在: assets/audio/audio_9869932344c1c9d3.mp3")
    
    # 复制图片文件
    if os.path.exists("assets/image/image_81fa0547ac2dcba5.png"):
        shutil.copy2("assets/image/image_81fa0547ac2dcba5.png", 
                     os.path.join(res_dir, "image_81fa0547ac2dcba5.png"))
        print("✓ 图片文件已复制: image_81fa0547ac2dcba5.png")
    else:
        print("⚠️  图片文件不存在: assets/image/image_81fa0547ac2dcba5.png")
    
    # 创建视频文件
    print("🎥 创建示例视频文件...")
    try:
        video_output = os.path.join(res_dir, "sample_video.mp4")
        ffmpeg_cmd = f'ffmpeg -f lavfi -i testsrc=duration=3:size=1920x1080:rate=30 -f lavfi -i sine=frequency=1000:duration=3 -c:v libx264 -c:a aac -shortest {video_output} -y'
        os.system(ffmpeg_cmd)
        
        if os.path.exists(video_output):
            print("✓ 示例视频文件已创建: sample_video.mp4")
        else:
            print("⚠️  视频文件创建失败")
    except Exception as e:
        print(f"⚠️  视频文件创建失败: {e}")
    
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
        print("🎬 开始创建包含所有媒体文件的完整工作草稿...")
        zip_filename = create_complete_working_draft()
        
        print(f"\n✅ 完整工作草稿创建完成!")
        print(f"📁 文件名: {zip_filename}")
        print(f"📊 文件大小: {os.path.getsize(zip_filename) / 1024:.1f} KB")
        
        print("\n📋 使用说明:")
        print("1. 将生成的ZIP文件解压到: F:\\jianyin\\cgwz\\JianyingPro Drafts\\")
        print("2. 重启剪映专业版软件")
        print("3. 在剪映中打开草稿，所有媒体文件应该能正确识别")
        
        print("\n💡 完整草稿的优势:")
        print("- ✅ 包含音频、视频、图片所有媒体类型")
        print("- ✅ 使用正常工作的草稿文件格式")
        print("- ✅ 使用.res目录结构")
        print("- ✅ 使用绝对路径格式")
        print("- ✅ 包含音频轨道配置")
        print("- ✅ 完整的媒体材料配置")
        
        print(f"\n🎉 完整草稿文件已准备就绪: {zip_filename}")
        
    except Exception as e:
        print(f"❌ 创建完整草稿文件失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    main()