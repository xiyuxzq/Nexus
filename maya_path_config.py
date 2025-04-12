#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Maya路径配置工具 - 用于配置Maya路径
"""

import os
import sys
import yaml
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class MayaPathConfig:
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "environments.yaml")
        self.environments = []
        self.load_config()
        
        # 创建UI
        self.root = tk.Tk()
        self.root.title("Maya路径配置")
        self.root.geometry("600x400")
        self.root.minsize(600, 400)
        
        self.create_widgets()
        self.update_environment_list()
    
    def load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.environments = yaml.safe_load(f) or []
            except Exception as e:
                print(f"加载配置文件失败: {str(e)}")
                self.environments = []
        else:
            print(f"配置文件不存在: {self.config_file}")
            self.environments = []
    
    def save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(self.environments, f, default_flow_style=False, allow_unicode=True)
            return True
        except Exception as e:
            print(f"保存配置文件失败: {str(e)}")
            return False
    
    def create_widgets(self):
        """创建控件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左侧列表
        list_frame = ttk.LabelFrame(main_frame, text="环境列表")
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 环境列表
        self.env_listbox = tk.Listbox(list_frame)
        self.env_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.env_listbox.bind('<<ListboxSelect>>', self.on_select_environment)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.env_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.env_listbox.configure(yscrollcommand=scrollbar.set)
        
        # 右侧详情
        details_frame = ttk.LabelFrame(main_frame, text="环境详情")
        details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 详情控件
        ttk.Label(details_frame, text="名称:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(details_frame, textvariable=self.name_var, state="readonly").grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(details_frame, text="软件:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.software_var = tk.StringVar()
        ttk.Entry(details_frame, textvariable=self.software_var, state="readonly").grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(details_frame, text="版本:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.version_var = tk.StringVar()
        ttk.Entry(details_frame, textvariable=self.version_var, state="readonly").grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(details_frame, text="部门:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.department_var = tk.StringVar()
        ttk.Entry(details_frame, textvariable=self.department_var, state="readonly").grid(row=3, column=1, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(details_frame, text="可执行文件路径:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.exec_path_var = tk.StringVar()
        exec_frame = ttk.Frame(details_frame)
        exec_frame.grid(row=4, column=1, sticky=tk.EW, padx=5, pady=5)
        self.exec_entry = ttk.Entry(exec_frame, textvariable=self.exec_path_var)
        self.exec_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(exec_frame, text="浏览...", command=self.browse_executable).pack(side=tk.RIGHT)
        
        ttk.Label(details_frame, text="启动脚本:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.startup_script_var = tk.StringVar()
        ttk.Entry(details_frame, textvariable=self.startup_script_var, state="readonly").grid(row=5, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # 按钮区域
        button_frame = ttk.Frame(details_frame)
        button_frame.grid(row=6, column=0, columnspan=2, sticky=tk.EW, padx=5, pady=10)
        ttk.Button(button_frame, text="保存", command=self.save_executable_path).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="检测路径", command=self.detect_maya_path).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="退出", command=self.root.destroy).pack(side=tk.RIGHT, padx=5)
        
        # 设置列权重
        details_frame.columnconfigure(1, weight=1)
    
    def update_environment_list(self):
        """更新环境列表"""
        self.env_listbox.delete(0, tk.END)
        
        # 过滤只显示Maya环境
        maya_environments = [env for env in self.environments if env.get("software") == "Maya"]
        
        for env in maya_environments:
            name = env.get("name", "未命名环境")
            self.env_listbox.insert(tk.END, name)
    
    def on_select_environment(self, event):
        """选择环境时的处理"""
        selection = self.env_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        
        # 过滤只显示Maya环境
        maya_environments = [env for env in self.environments if env.get("software") == "Maya"]
        
        if index >= len(maya_environments):
            return
        
        env = maya_environments[index]
        
        # 更新UI
        self.name_var.set(env.get("name", ""))
        self.software_var.set(env.get("software", ""))
        self.version_var.set(env.get("version", ""))
        self.department_var.set(env.get("department", ""))
        self.exec_path_var.set(env.get("executable_path", ""))
        self.startup_script_var.set(env.get("startup_script", ""))
        
        # 允许编辑可执行文件路径
        self.exec_entry.config(state="normal")
    
    def browse_executable(self):
        """浏览选择可执行文件"""
        file_path = filedialog.askopenfilename(
            title="选择Maya可执行文件",
            filetypes=[("可执行文件", "*.exe"), ("所有文件", "*.*")]
        )
        
        if file_path:
            self.exec_path_var.set(file_path)
    
    def save_executable_path(self):
        """保存可执行文件路径"""
        selection = self.env_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个环境")
            return
        
        index = selection[0]
        
        # 过滤只显示Maya环境
        maya_environments = [env for env in self.environments if env.get("software") == "Maya"]
        
        if index >= len(maya_environments):
            return
        
        # 获取所选环境在原始列表中的索引
        env_name = maya_environments[index].get("name")
        original_index = next((i for i, env in enumerate(self.environments) if env.get("name") == env_name), -1)
        
        if original_index == -1:
            messagebox.showerror("错误", "找不到所选环境")
            return
        
        # 更新路径
        new_path = self.exec_path_var.get()
        
        # 检查路径是否存在
        if not os.path.exists(new_path):
            result = messagebox.askyesno("警告", f"路径不存在: {new_path}\n是否仍要保存?")
            if not result:
                return
        
        self.environments[original_index]["executable_path"] = new_path
        
        # 保存配置
        if self.save_config():
            messagebox.showinfo("成功", "路径已保存")
        else:
            messagebox.showerror("错误", "保存配置失败")
    
    def detect_maya_path(self):
        """自动检测Maya路径"""
        # 常见的Maya安装路径
        common_paths = [
            "C:/Program Files/Autodesk/Maya2019/bin/maya.exe",
            "C:/Program Files/Autodesk/Maya2020/bin/maya.exe",
            "C:/Program Files/Autodesk/Maya2022/bin/maya.exe",
            "C:/Program Files/Autodesk/Maya2023/bin/maya.exe",
            "C:/Autodesk/Maya2019/bin/maya.exe",
            "C:/Autodesk/Maya2020/bin/maya.exe",
            "C:/Autodesk/Maya2022/bin/maya.exe",
            "C:/Autodesk/Maya2023/bin/maya.exe"
        ]
        
        # 尝试查找Maya路径
        found_paths = []
        for path in common_paths:
            if os.path.exists(path):
                found_paths.append(path)
        
        if not found_paths:
            messagebox.showinfo("提示", "未找到Maya路径，请手动选择")
            self.browse_executable()
            return
        
        # 如果只找到一个路径，直接使用
        if len(found_paths) == 1:
            self.exec_path_var.set(found_paths[0])
            messagebox.showinfo("成功", f"已检测到Maya路径: {found_paths[0]}")
            return
        
        # 如果找到多个路径，让用户选择
        self.show_path_selection_dialog(found_paths)
    
    def show_path_selection_dialog(self, paths):
        """显示路径选择对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("选择Maya路径")
        dialog.geometry("500x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="选择要使用的Maya路径:").pack(padx=10, pady=10)
        
        # 创建列表框
        path_listbox = tk.Listbox(dialog)
        path_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 添加路径
        for path in paths:
            path_listbox.insert(tk.END, path)
        
        # 选择按钮
        def on_select():
            selection = path_listbox.curselection()
            if selection:
                index = selection[0]
                self.exec_path_var.set(paths[index])
                dialog.destroy()
        
        ttk.Button(dialog, text="选择", command=on_select).pack(side=tk.RIGHT, padx=10, pady=10)
        ttk.Button(dialog, text="取消", command=dialog.destroy).pack(side=tk.RIGHT, padx=10, pady=10)
    
    def run(self):
        """运行应用"""
        self.root.mainloop()

if __name__ == "__main__":
    app = MayaPathConfig()
    app.run()