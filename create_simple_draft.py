#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

import os
import sys
import json
import uuid
import zipfile
import shutil
from datetime import datetime

def create_simple_draft():
    """创建一个简单的剪映草稿文件"""
    print("=== 创建简单剪映草稿 ===")
    
    # 生成草稿ID
    draft_id = f"dfd_cat_{int(datetime.now().timestamp())}_{uuid.uuid4().hex[:8]}"
    print(f"📝 草稿ID: {draft_id}")
    
    # 创建草稿目录
    draft_dir = f"./simple_draft_{draft_id}"
    os.makedirs(draft_dir, exist_ok=True)
    
    # 基础草稿信息
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
        "duration": 0,
        "extra_info": None,
        "fps": 30.0,
        "free_render_index_mode_on": False,
        "group_container": None,
        "id": str(uuid.uuid4()).upper(),
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
            "audios": [],
            "beats": [],
            "canvases": [],
            "chromas": [],
            "color_curves": [],
            "color_gradings": [],
            "color_wheels": [],
            "effects": [],
            "filters": [],
            "handwrites": [],
            "image_sequences": [],
            "images": [],
            "luts": [],
            "masks": [],
            "motions": [],
            "shapes": [],
            "stickers": [],
            "texts": [],
            "transitions": [],
            "videos": [],
            "vocal_separations": []
        },
        "mutable_config": None,
        "name": "",
        "new_version": "110.0.0",
        "platform": {
            "app_id": 3704,
            "app_source": "lv",
            "app_version": "5.9.0",
            "device_id": str(uuid.uuid4()).replace("-", "")[:32],
            "hard_disk_id": str(uuid.uuid4()).replace("-", "")[:32],
            "mac_address": str(uuid.uuid4()).replace("-", "")[:32],
            "os": "windows",
            "os_version": "10.0.19045"
        },
        "relationships": [],
        "render_index_track_mode_on": True,
        "static_cover_image_path": "",
        "time_marks": None,
        "tracks": [],
        "update_time": int(datetime.now().timestamp()),
        "version": 360000
    }
    
    # 写入草稿文件
    with open(f"{draft_dir}/draft_info.json", "w", encoding="utf-8") as f:
        json.dump(draft_info, f, ensure_ascii=False, indent=4)
    
    # 复制必要的模板文件
    template_files = [
        "attachment_pc_common.json",
        "draft_agency_config.json", 
        "draft_biz_config.json",
        "draft_cover.jpg",
        "draft_settings",
        "attachment_editing.json",
        "performance_opt_info.json"
    ]
    
    for file_name in template_files:
        src_path = f"template_jianying/{file_name}"
        dst_path = f"{draft_dir}/{file_name}"
        if os.path.exists(src_path):
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dst_path)
            else:
                shutil.copy2(src_path, dst_path)
            print(f"✅ 复制文件: {file_name}")
        else:
            print(f"⚠️ 文件不存在: {file_name}")
    
    # 特殊处理draft_meta_info.json，更新路径为Windows系统
    meta_info_src = "template_jianying/draft_meta_info.json"
    if os.path.exists(meta_info_src):
        with open(meta_info_src, 'r', encoding='utf-8') as f:
            meta_info = json.load(f)
        
        # 更新路径为Windows系统路径
        meta_info["draft_root_path"] = "C:\\Users\\Administrator\\AppData\\Local\\JianyingPro\\User Data\\Projects\\com.lveditor.draft"
        meta_info["draft_fold_path"] = "C:\\Users\\Administrator\\AppData\\Local\\JianyingPro\\User Data\\Projects\\com.lveditor.draft\\草稿"
        meta_info["draft_id"] = draft_info["id"]
        meta_info["draft_name"] = f"草稿_{draft_id}"
        meta_info["tm_draft_create"] = int(datetime.now().timestamp() * 1000000)
        meta_info["tm_draft_modified"] = int(datetime.now().timestamp() * 1000000)
        
        with open(f"{draft_dir}/draft_meta_info.json", "w", encoding="utf-8") as f:
            json.dump(meta_info, f, ensure_ascii=False, separators=(',', ':'))
        print("✅ 复制并更新文件: draft_meta_info.json")
    else:
        print("⚠️ 文件不存在: draft_meta_info.json")
    
    # 复制common_attachment目录
    if os.path.exists("template_jianying/common_attachment"):
        shutil.copytree("template_jianying/common_attachment", f"{draft_dir}/common_attachment")
        print("✅ 复制目录: common_attachment")
    
    # 创建zip文件
    zip_path = f"./tmp/zip/{draft_id}.zip"
    os.makedirs("./tmp/zip", exist_ok=True)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(draft_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, draft_dir)
                zipf.write(file_path, arcname)
    
    print(f"✅ 草稿文件创建完成: {zip_path}")
    
    # 清理临时目录
    shutil.rmtree(draft_dir)
    
    # 生成下载URL
    draft_url = f"https://www.install-ai-guider.top/draft/downloader?draft_id={draft_id}"
    
    print(f"\n📋 草稿信息:")
    print(f"草稿ID: {draft_id}")
    print(f"下载URL: {draft_url}")
    print(f"本地文件: {zip_path}")
    
    return draft_id, draft_url

if __name__ == "__main__":
    draft_id, draft_url = create_simple_draft()
    print(f"\n🎉 简单草稿创建完成！")
    print(f"请在剪映中测试: {draft_url}")