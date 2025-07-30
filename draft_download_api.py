#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
草稿下载和修复API接口
提供下载草稿、修复草稿等功能
"""

import os
import json
import tempfile
import zipfile
import requests
import shutil
from flask import Flask, request, jsonify
from flask_cors import CORS
from smart_draft_fixer import SmartDraftFixer
from direct_draft_fixer import DirectDraftFixer
import simple_draft_fixer
from server_side_draft_fixer import ServerSideDraftFixer

app = Flask(__name__)
CORS(app)  # 启用CORS支持

class DraftDownloadAPI:
    def __init__(self):
        self.base_url = "http://8.148.70.18:9000"
        self.output_dir = "./fixed_drafts"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def download_draft(self, draft_url):
        """仅下载草稿文件"""
        try:
            print(f"开始下载草稿: {draft_url}")
            
            # 创建临时目录
            temp_dir = tempfile.mkdtemp()
            draft_zip_path = os.path.join(temp_dir, "draft.zip")
            
            # 下载草稿文件
            response = requests.get(draft_url, stream=True)
            response.raise_for_status()
            
            with open(draft_zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # 获取文件信息
            file_size = os.path.getsize(draft_zip_path)
            
            # 检查ZIP文件内容
            with zipfile.ZipFile(draft_zip_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
            
            # 清理临时文件
            shutil.rmtree(temp_dir)
            
            return {
                "success": True,
                "message": "草稿下载成功",
                "file_size": file_size,
                "file_count": len(file_list),
                "file_list": file_list[:10],  # 只返回前10个文件
                "draft_url": draft_url
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"下载失败: {str(e)}",
                "draft_url": draft_url
            }
    
    def fix_draft(self, draft_url, fix_method="smart"):
        """仅修复草稿文件"""
        try:
            print(f"开始修复草稿: {draft_url}, 方法: {fix_method}")
            
            # 根据修复方法选择修复器
            if fix_method == "smart":
                fixer = SmartDraftFixer(draft_url)
                result = fixer.smart_fix_draft()
            elif fix_method == "direct":
                fixer = DirectDraftFixer(draft_url)
                result = fixer.fix_draft_directly()
            elif fix_method == "traditional":
                result = simple_draft_fixer.download_and_fix_draft(draft_url)
            elif fix_method == "server":
                # 从URL中提取草稿ID
                draft_id = draft_url.split('/')[-1].split('.')[0]
                fixer = ServerSideDraftFixer(draft_id)
                result = fixer.fix_draft_in_place()
            else:
                return {
                    "success": False,
                    "error": f"不支持的修复方法: {fix_method}"
                }
            
            if result:
                return {
                    "success": True,
                    "message": f"草稿修复成功 (方法: {fix_method})",
                    "fixed_file": result,
                    "fix_method": fix_method,
                    "draft_url": draft_url
                }
            else:
                return {
                    "success": False,
                    "error": f"修复失败 (方法: {fix_method})",
                    "draft_url": draft_url
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"修复失败: {str(e)}",
                "draft_url": draft_url,
                "fix_method": fix_method
            }
    
    def download_and_fix_draft(self, draft_url, fix_method="smart"):
        """下载并修复草稿文件"""
        try:
            print(f"开始下载并修复草稿: {draft_url}, 方法: {fix_method}")
            
            # 先下载
            download_result = self.download_draft(draft_url)
            if not download_result["success"]:
                return download_result
            
            # 再修复
            fix_result = self.fix_draft(draft_url, fix_method)
            if not fix_result["success"]:
                return fix_result
            
            return {
                "success": True,
                "message": "下载并修复成功",
                "download_info": download_result,
                "fix_info": fix_result,
                "draft_url": draft_url,
                "fix_method": fix_method
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"下载并修复失败: {str(e)}",
                "draft_url": draft_url,
                "fix_method": fix_method
            }

# 创建API实例
api = DraftDownloadAPI()

@app.route('/download_draft', methods=['POST'])
def download_draft_endpoint():
    """仅下载草稿API"""
    try:
        data = request.get_json()
        draft_url = data.get('draft_url')
        
        if not draft_url:
            return jsonify({
                "success": False,
                "error": "缺少draft_url参数"
            })
        
        result = api.download_draft(draft_url)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"API调用失败: {str(e)}"
        })

@app.route('/fix_draft', methods=['POST'])
def fix_draft_endpoint():
    """仅修复草稿API"""
    try:
        data = request.get_json()
        draft_url = data.get('draft_url')
        fix_method = data.get('fix_method', 'smart')
        
        if not draft_url:
            return jsonify({
                "success": False,
                "error": "缺少draft_url参数"
            })
        
        result = api.fix_draft(draft_url, fix_method)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"API调用失败: {str(e)}"
        })

@app.route('/download_and_fix_draft', methods=['POST'])
def download_and_fix_draft_endpoint():
    """下载并修复草稿API"""
    try:
        data = request.get_json()
        draft_url = data.get('draft_url')
        fix_method = data.get('fix_method', 'smart')
        
        if not draft_url:
            return jsonify({
                "success": False,
                "error": "缺少draft_url参数"
            })
        
        result = api.download_and_fix_draft(draft_url, fix_method)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"API调用失败: {str(e)}"
        })

@app.route('/get_fix_methods', methods=['GET'])
def get_fix_methods_endpoint():
    """获取可用的修复方法"""
    return jsonify({
        "success": True,
        "methods": [
            {
                "value": "smart",
                "name": "智能修复",
                "description": "只修复需要修复的部分，处理时间最短",
                "recommended": True
            },
            {
                "value": "direct",
                "name": "直接修改",
                "description": "在原始文件基础上直接修改，保留文件完整性"
            },
            {
                "value": "traditional",
                "name": "传统修复",
                "description": "完全重建文件结构，适用于严重损坏的草稿"
            },
            {
                "value": "server",
                "name": "服务器端修复",
                "description": "直接在服务器上修改文件，无需文件传输"
            }
        ]
    })

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        "success": True,
        "message": "草稿下载API服务正常运行",
        "version": "1.0.0"
    })

if __name__ == '__main__':
    print("🎬 草稿下载API服务启动中...")
    print("=" * 50)
    print("可用接口:")
    print("- POST /download_draft - 仅下载草稿")
    print("- POST /fix_draft - 仅修复草稿")
    print("- POST /download_and_fix_draft - 下载并修复草稿")
    print("- GET /get_fix_methods - 获取修复方法")
    print("- GET /health - 健康检查")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=9001, debug=True) 