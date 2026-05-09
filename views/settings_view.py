import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime, timedelta
import os
from styles import Styles


class SettingsViewMixin:
    """GUI 视图混入类"""

    def system_management(self):
        """系统管理界面 - 现代化设计"""
        self.clear_window()
        
        # 调整窗口高度，增加200
        self.root.geometry(f"{Styles.WINDOW_WIDTH}x{Styles.WINDOW_HEIGHT + 200}")
        
        # 主容器
        main_container = tk.Frame(self.root, bg=Styles.BACKGROUND_COLOR)
        main_container.pack(fill=tk.BOTH, expand=True, padx=Styles.SPACING_XL)
        
        # 页面标题
        self._create_page_header(main_container, "系统管理", "备份、同步和日志管理")
        
        # 按钮区域容器
        buttons_container = tk.Frame(main_container, bg=Styles.BACKGROUND_COLOR)
        buttons_container.pack(fill=tk.BOTH, expand=True)
        
        # 按钮网格
        buttons = [
            ("数据备份管理", self.backup_management, "💾"),
            ("云端同步管理", self.cloud_sync_management, "☁️"),
            ("操作日志查询", self.log_management, "📝")
        ]
        self._create_button_grid(buttons_container, buttons, columns=2)
        
        # 分隔线
        ttk.Separator(buttons_container, orient='horizontal').pack(fill='x', pady=Styles.SPACING_LG)
        
        # 退出按钮
        exit_frame = tk.Frame(buttons_container, bg=Styles.BACKGROUND_COLOR)
        exit_frame.pack(pady=Styles.SPACING_MD)
        ttk.Button(
            exit_frame,
            text="退出系统",
            command=self.root.quit,
            style="Danger.TButton"
        ).pack()
        
        # 返回按钮
        self._create_back_button(main_container, self.create_main_menu)

    def backup_management(self):
        """数据备份管理界面"""
        top = self._create_toplevel_with_size("backup_management", "large")
        top.title("数据备份管理")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_SMALL, fill=tk.X)
        
        tk.Label(
            title_frame, 
            text="数据备份管理", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack(padx=Styles.PADX_MEDIUM, anchor=tk.W)
        
        btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        btn_frame.pack(pady=Styles.PADY_SMALL)
        
        def create_backup():
            """创建备份"""
            description = simpledialog.askstring("备份描述", "请输入备份描述（可选）：", parent=top)
            try:
                backup_path = self.backup_manager.create_backup(description or "")
                messagebox.showinfo("成功", f"备份创建成功！\n备份文件：{backup_path}")
                self.operation_logger.log_operation(
                    operation_type="备份",
                    module="系统管理",
                    details=f"创建数据备份: {backup_path}"
                )
                refresh_list()
            except Exception as e:
                messagebox.showerror("错误", f"备份创建失败：{e}")
        
        def refresh_list():
            """刷新备份列表"""
            for item in tree.get_children():
                tree.delete(item)
            
            backups = self.backup_manager.list_backups()
            for backup in backups:
                tree.insert("", tk.END, values=(
                    backup['filename'],
                    backup['size_formatted'],
                    backup['created_time'].strftime('%Y-%m-%d %H:%M:%S')
                ))
        
        def restore_backup():
            """恢复备份"""
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("提示", "请先选择一个备份文件！")
                return
            
            item = tree.item(selected[0])
            filename = item['values'][0]
            
            backups = self.backup_manager.list_backups()
            backup_info = next((b for b in backups if b['filename'] == filename), None)
            
            if not backup_info:
                messagebox.showerror("错误", "备份文件不存在！")
                return
            
            confirm = messagebox.askyesno(
                "确认恢复",
                f"确定要恢复备份吗？\n\n备份文件：{filename}\n\n注意：当前数据将被覆盖！"
            )
            
            if confirm:
                try:
                    success = self.backup_manager.restore_backup(backup_info['path'])
                    if success:
                        messagebox.showinfo("成功", "数据恢复成功！")
                        self.operation_logger.log_operation(
                            operation_type="恢复",
                            module="系统管理",
                            details=f"恢复数据备份: {filename}"
                        )
                    else:
                        messagebox.showerror("错误", "数据恢复失败！")
                except Exception as e:
                    messagebox.showerror("错误", f"恢复失败：{e}")
        
        def delete_backup():
            """删除备份"""
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("提示", "请先选择一个备份文件！")
                return
            
            item = tree.item(selected[0])
            filename = item['values'][0]
            
            confirm = messagebox.askyesno(
                "确认删除",
                f"确定要删除备份吗？\n\n备份文件：{filename}"
            )
            
            if confirm:
                backups = self.backup_manager.list_backups()
                backup_info = next((b for b in backups if b['filename'] == filename), None)
                
                if backup_info:
                    try:
                        success = self.backup_manager.delete_backup(backup_info['path'])
                        if success:
                            messagebox.showinfo("成功", "备份删除成功！")
                            refresh_list()
                        else:
                            messagebox.showerror("错误", "备份删除失败！")
                    except Exception as e:
                        messagebox.showerror("错误", f"删除失败：{e}")
        
        tk.Button(
            btn_frame, 
            text="创建备份", 
            font=Styles.BUTTON_FONT,
            width=15,
            command=create_backup,
            bg=Styles.SUCCESS_COLOR,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame, 
            text="恢复备份", 
            font=Styles.BUTTON_FONT,
            width=15,
            command=restore_backup,
            bg=Styles.PRIMARY_COLOR,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame, 
            text="删除备份", 
            font=Styles.BUTTON_FONT,
            width=15,
            command=delete_backup,
            bg=Styles.ERROR_COLOR,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame, 
            text="刷新列表", 
            font=Styles.BUTTON_FONT,
            width=15,
            command=refresh_list,
            bg=Styles.SECONDARY_COLOR,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        table_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        table_frame.pack(padx=Styles.PADX_MEDIUM, pady=Styles.PADY_SMALL, fill=tk.BOTH, expand=True)
        
        tree = ttk.Treeview(table_frame, style="Treeview", columns=("filename", "size", "time"), show="headings")
        tree.heading("filename", text="备份文件")
        tree.heading("size", text="文件大小")
        tree.heading("time", text="创建时间")
        tree.column("filename", width=300, anchor=tk.W)
        tree.column("size", width=100, anchor=tk.CENTER)
        tree.column("time", width=180, anchor=tk.CENTER)
        
        scrollbar_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_y.set)
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        refresh_list()
        
        tk.Button(
            top, 
            text="关闭", 
            font=Styles.BUTTON_FONT,
            width=Styles.BUTTON_WIDTH,
            height=Styles.BUTTON_HEIGHT,
            command=top.destroy,
            bg=Styles.PRIMARY_COLOR,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(pady=Styles.PADY_MEDIUM)

    def log_management(self):
        """操作日志管理界面"""
        top = self._create_toplevel_with_size("log_management", "large")
        top.title("操作日志查询")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_SMALL, fill=tk.X)
        
        tk.Label(
            title_frame, 
            text="操作日志查询", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack(padx=Styles.PADX_MEDIUM, anchor=tk.W)
        
        filter_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        filter_frame.pack(pady=Styles.PADY_SMALL, padx=Styles.PADX_MEDIUM, fill=tk.X)
        
        tk.Label(filter_frame, text="操作类型:", bg=Styles.BACKGROUND_COLOR, font=Styles.LABEL_FONT).pack(side=tk.LEFT, padx=5)
        type_var = tk.StringVar()
        type_combo = ttk.Combobox(filter_frame, textvariable=type_var, state="readonly", width=15)
        type_combo['values'] = ["全部", "新增", "修改", "删除", "查询", "导入", "导出", "备份", "恢复", "其他"]
        type_combo.current(0)
        type_combo.pack(side=tk.LEFT, padx=5)
        
        tk.Label(filter_frame, text="模块:", bg=Styles.BACKGROUND_COLOR, font=Styles.LABEL_FONT).pack(side=tk.LEFT, padx=5)
        module_var = tk.StringVar()
        module_combo = ttk.Combobox(filter_frame, textvariable=module_var, state="readonly", width=15)
        module_combo['values'] = ["全部"]
        module_combo.current(0)
        module_combo.pack(side=tk.LEFT, padx=5)
        
        tk.Label(filter_frame, text="记录数:", bg=Styles.BACKGROUND_COLOR, font=Styles.LABEL_FONT).pack(side=tk.LEFT, padx=5)
        limit_var = tk.StringVar(value="100")
        limit_entry = tk.Entry(filter_frame, textvariable=limit_var, width=10)
        limit_entry.pack(side=tk.LEFT, padx=5)
        
        def refresh_logs():
            """刷新日志列表"""
            for item in tree.get_children():
                tree.delete(item)
            
            op_type = type_var.get()
            module = module_var.get()
            limit = int(limit_var.get()) if limit_var.get().isdigit() else 100
            
            op_type_param = None if op_type == "全部" else op_type
            module_param = None if module == "全部" else module
            
            logs = self.operation_logger.get_logs(
                operation_type=op_type_param,
                module=module_param,
                limit=limit
            )
            
            for _, row in logs.iterrows():
                tree.insert("", tk.END, values=(
                    row['日志编号'],
                    row['操作时间'],
                    row['操作类型'],
                    row['操作模块'],
                    row['操作详情'],
                    row['操作人']
                ))
        
        tk.Button(
            filter_frame, 
            text="查询", 
            font=Styles.BUTTON_FONT,
            command=refresh_logs,
            bg=Styles.PRIMARY_COLOR,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=2
        ).pack(side=tk.LEFT, padx=10)
        
        table_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        table_frame.pack(padx=Styles.PADX_MEDIUM, pady=Styles.PADY_SMALL, fill=tk.BOTH, expand=True)
        
        tree = ttk.Treeview(table_frame, style="Treeview", 
                            columns=("id", "time", "type", "module", "detail", "operator"), 
                            show="headings")
        tree.heading("id", text="日志编号")
        tree.heading("time", text="操作时间")
        tree.heading("type", text="操作类型")
        tree.heading("module", text="操作模块")
        tree.heading("detail", text="操作详情")
        tree.heading("operator", text="操作人")
        tree.column("id", width=150, anchor=tk.W)
        tree.column("time", width=150, anchor=tk.CENTER)
        tree.column("type", width=80, anchor=tk.CENTER)
        tree.column("module", width=120, anchor=tk.W)
        tree.column("detail", width=300, anchor=tk.W)
        tree.column("operator", width=100, anchor=tk.CENTER)
        
        scrollbar_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        refresh_logs()
        
        tk.Button(
            top, 
            text="关闭", 
            font=Styles.BUTTON_FONT,
            width=Styles.BUTTON_WIDTH,
            height=Styles.BUTTON_HEIGHT,
            command=top.destroy,
            bg=Styles.PRIMARY_COLOR,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(pady=Styles.PADY_MEDIUM)

    def cloud_sync_management(self):
        """云端同步管理界面 - SFTP 版本"""
        top = self._create_toplevel_with_size("cloud_sync_management", "large")
        top.title("云端同步管理 - SFTP")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_SMALL, fill=tk.X)
        
        tk.Label(
            title_frame, 
            text="云端同步管理 - SFTP", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack(padx=Styles.PADX_MEDIUM, anchor=tk.W)
        
        # 状态信息区域
        status_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        status_frame.pack(pady=Styles.PADY_SMALL, padx=Styles.PADX_MEDIUM, fill=tk.X)
        
        status_label = tk.Label(
            status_frame, 
            text="同步状态: 未启用",
            font=Styles.LABEL_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.TEXT_COLOR
        )
        status_label.pack(anchor=tk.W)
        
        # 服务器配置区域
        config_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR, relief=tk.SOLID, bd=1)
        config_frame.pack(pady=Styles.PADY_SMALL, padx=Styles.PADX_MEDIUM, fill=tk.X)
        
        tk.Label(
            config_frame,
            text="服务器配置",
            font=("微软雅黑", 12, "bold"),
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky=tk.W)
        
        # 主机地址
        tk.Label(config_frame, text="主机地址:", bg=Styles.BACKGROUND_COLOR, font=Styles.LABEL_FONT).grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        host_var = tk.StringVar(value="27.tcp.cpolar.top")
        host_entry = tk.Entry(config_frame, textvariable=host_var, width=25, font=Styles.TEXT_FONT)
        host_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # 端口
        tk.Label(config_frame, text="端口:", bg=Styles.BACKGROUND_COLOR, font=Styles.LABEL_FONT).grid(row=1, column=2, padx=10, pady=5, sticky=tk.E)
        port_var = tk.StringVar(value="11007")
        port_entry = tk.Entry(config_frame, textvariable=port_var, width=10, font=Styles.TEXT_FONT)
        port_entry.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)
        
        # 用户名
        tk.Label(config_frame, text="用户名:", bg=Styles.BACKGROUND_COLOR, font=Styles.LABEL_FONT).grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        username_var = tk.StringVar()
        username_entry = tk.Entry(config_frame, textvariable=username_var, width=25, font=Styles.TEXT_FONT)
        username_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        # 密码
        tk.Label(config_frame, text="密码:", bg=Styles.BACKGROUND_COLOR, font=Styles.LABEL_FONT).grid(row=2, column=2, padx=10, pady=5, sticky=tk.E)
        password_var = tk.StringVar()
        password_entry = tk.Entry(config_frame, textvariable=password_var, width=25, font=Styles.TEXT_FONT, show="*")
        password_entry.grid(row=2, column=3, padx=5, pady=5, sticky=tk.W)
        
        # 远程路径
        tk.Label(config_frame, text="远程路径:", bg=Styles.BACKGROUND_COLOR, font=Styles.LABEL_FONT).grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        remote_path_var = tk.StringVar(value="/mnt/sda/ljw/Code/Tea/")
        remote_path_entry = tk.Entry(config_frame, textvariable=remote_path_var, width=50, font=Styles.TEXT_FONT)
        remote_path_entry.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky=tk.W)
        
        def update_status():
            """更新状态显示"""
            sync_status = self.cloud_sync_manager.get_sync_status()
            if sync_status['enabled']:
                status_text = f"同步状态: 已启用 | 服务器: {sync_status['host']}:{sync_status['port']} | 用户: {sync_status['username']}"
                if sync_status['last_sync_time']:
                    status_text += f" | 最后同步: {sync_status['last_sync_time'][:19]}"
                status_label.config(text=status_text, fg=Styles.SUCCESS_COLOR)
            elif not sync_status['paramiko_available']:
                status_label.config(text="同步状态: paramiko 库未安装，请运行: pip install paramiko", fg=Styles.ERROR_COLOR)
            else:
                status_label.config(text="同步状态: 未启用", fg=Styles.ERROR_COLOR)
        
        def load_existing_config():
            """加载现有配置"""
            sync_status = self.cloud_sync_manager.get_sync_status()
            if sync_status['host']:
                host_var.set(sync_status['host'])
            if sync_status['port']:
                port_var.set(str(sync_status['port']))
            if sync_status['username']:
                username_var.set(sync_status['username'])
            remote_path_var.set(sync_status['remote_path'])
        
        def save_server_config():
            """保存服务器配置"""
            try:
                host = host_var.get().strip()
                port = int(port_var.get().strip())
                username = username_var.get().strip()
                password = password_var.get().strip()
                remote_path = remote_path_var.get().strip()
                
                if not host or not username:
                    messagebox.showwarning("提示", "主机地址和用户名不能为空！")
                    return
                
                success = self.cloud_sync_manager.set_server_config(host, port, username, password, remote_path)
                if success:
                    messagebox.showinfo("成功", "服务器配置已保存！")
                    self.operation_logger.log_operation(
                        operation_type="设置",
                        module="云端同步",
                        details=f"配置 SFTP 服务器: {host}:{port}"
                    )
                    update_status()
                    refresh_cloud_list()
                else:
                    messagebox.showerror("错误", "保存配置失败！")
            except ValueError:
                messagebox.showerror("错误", "端口必须是数字！")
        
        def test_connection():
            """测试服务器连接"""
            result = self.cloud_sync_manager.test_connection()
            if result['success']:
                messagebox.showinfo("成功", result['message'])
            else:
                messagebox.showerror("错误", result['message'])
        
        def upload_to_cloud():
            """上传数据到云端"""
            if not self.cloud_sync_manager.is_enabled():
                messagebox.showwarning("提示", "请先配置并保存服务器连接！")
                return
            
            data_files = ["tea_inventory.xlsx", "config.json", "operation_logs.xlsx", "cloud_sync_config.json"]
            result = self.cloud_sync_manager.upload_to_cloud(data_files)
            
            if result['success']:
                uploaded_str = ", ".join(result.get('uploaded_files', []))
                messagebox.showinfo("成功", f"{result['message']}\n上传文件: {uploaded_str}")
                self.operation_logger.log_operation(
                    operation_type="上传",
                    module="云端同步",
                    details=f"上传数据到 SFTP 服务器，版本: {result['version']}"
                )
                update_status()
                refresh_cloud_list()
            else:
                messagebox.showerror("错误", result['message'])
        
        def download_from_cloud():
            """从云端下载数据"""
            if not self.cloud_sync_manager.is_enabled():
                messagebox.showwarning("提示", "请先配置并保存服务器连接！")
                return
            
            confirm = messagebox.askyesno(
                "确认下载",
                "确定要从云端下载数据吗？\n\n本地文件会被备份后覆盖！"
            )
            
            if not confirm:
                return
            
            result = self.cloud_sync_manager.download_from_cloud(".")
            
            if result['success']:
                restored_str = ", ".join(result.get('restored_files', []))
                messagebox.showinfo("成功", f"{result['message']}\n恢复文件: {restored_str}")
                self.operation_logger.log_operation(
                    operation_type="下载",
                    module="云端同步",
                    details=f"从 SFTP 服务器恢复数据"
                )
                self.system.excel_manager.clear_cache()
                update_status()
                refresh_cloud_list()
            else:
                messagebox.showerror("错误", result['message'])
        
        def refresh_cloud_list():
            """刷新云端文件列表"""
            for item in tree_cloud.get_children():
                tree_cloud.delete(item)
            
            packages = self.cloud_sync_manager.list_cloud_packages()
            for pkg in packages:
                tree_cloud.insert("", tk.END, values=(
                    pkg.get('filename', ''),
                    pkg.get('size_formatted', ''),
                    pkg.get('modified_time_str', '')
                ))
        
        # 配置操作按钮
        config_btn_frame = tk.Frame(config_frame, bg=Styles.BACKGROUND_COLOR)
        config_btn_frame.grid(row=4, column=0, columnspan=4, pady=10)
        
        tk.Button(
            config_btn_frame, 
            text="保存配置", 
            font=Styles.BUTTON_FONT,
            width=12,
            command=save_server_config,
            bg=Styles.PRIMARY_COLOR,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            config_btn_frame, 
            text="测试连接", 
            font=Styles.BUTTON_FONT,
            width=12,
            command=test_connection,
            bg=Styles.SECONDARY_COLOR,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        # 操作按钮区域
        btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        btn_frame.pack(pady=Styles.PADY_SMALL)
        
        tk.Button(
            btn_frame, 
            text="上传到云端", 
            font=Styles.BUTTON_FONT,
            width=18,
            command=upload_to_cloud,
            bg=Styles.SUCCESS_COLOR,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame, 
            text="从云端下载", 
            font=Styles.BUTTON_FONT,
            width=18,
            command=download_from_cloud,
            bg=Styles.PRIMARY_COLOR,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame, 
            text="刷新列表", 
            font=Styles.BUTTON_FONT,
            width=18,
            command=refresh_cloud_list,
            bg=Styles.SECONDARY_COLOR,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        # 使用说明
        help_frame = tk.Frame(top, bg="#E8F4FD", relief=tk.SOLID, bd=1)
        help_frame.pack(pady=Styles.PADY_SMALL, padx=Styles.PADX_MEDIUM, fill=tk.X)
        
        help_text = """使用说明：
1. 本系统通过 SFTP 协议直接连接远程服务器进行数据同步
2. 请在上方填写服务器信息（已预填您提供的配置）
3. 点击\"保存配置\"保存服务器连接信息
4. 点击\"测试连接\"验证服务器连接是否正常
5. 点击\"上传到云端\"将本地数据上传到服务器
6. 点击\"从云端下载\"从服务器下载最新数据到本地
7. 点击\"刷新列表\"查看服务器上的数据文件"""
        
        tk.Label(
            help_frame,
            text=help_text,
            font=Styles.TEXT_FONT,
            bg="#E8F4FD",
            fg="#333333",
            justify=tk.LEFT
        ).pack(padx=10, pady=10, anchor=tk.W)
        
        # 云端文件列表
        table_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        table_frame.pack(padx=Styles.PADX_MEDIUM, pady=Styles.PADY_SMALL, fill=tk.BOTH, expand=True)
        
        tree_cloud = ttk.Treeview(
            table_frame, 
            style="Treeview", 
            columns=("filename", "size", "time"), 
            show="headings"
        )
        tree_cloud.heading("filename", text="文件名")
        tree_cloud.heading("size", text="文件大小")
        tree_cloud.heading("time", text="修改时间")
        tree_cloud.column("filename", width=300, anchor=tk.W)
        tree_cloud.column("size", width=120, anchor=tk.CENTER)
        tree_cloud.column("time", width=180, anchor=tk.CENTER)
        
        scrollbar_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree_cloud.yview)
        tree_cloud.configure(yscrollcommand=scrollbar_y.set)
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_cloud.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 加载现有配置并初始化
        load_existing_config()
        update_status()
        refresh_cloud_list()
        
        tk.Button(
            top, 
            text="关闭", 
            font=Styles.BUTTON_FONT,
            width=Styles.BUTTON_WIDTH,
            height=Styles.BUTTON_HEIGHT,
            command=top.destroy,
            bg=Styles.PRIMARY_COLOR,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(pady=Styles.PADY_MEDIUM)


def main():
    root = tk.Tk()
    app = TeaInventoryGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
