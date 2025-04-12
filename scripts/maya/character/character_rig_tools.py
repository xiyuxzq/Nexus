#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
角色绑定工具 - 提供角色绑定相关功能
"""

import maya.cmds as cmds
import maya.mel as mel

def create_skeleton():
    """创建基础骨架"""
    # 显示一个简单的UI窗口
    if cmds.window("createSkeletonWindow", exists=True):
        cmds.deleteUI("createSkeletonWindow")
    
    window = cmds.window("createSkeletonWindow", title="创建骨架", widthHeight=(300, 200))
    cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnOffset=["both", 10])
    
    cmds.text(label="选择骨架类型:")
    cmds.radioButtonGrp("skeletonType", label="骨架类型", labelArray3=["人形", "四足", "自定义"], numberOfRadioButtons=3, select=1)
    
    cmds.separator(height=10, style="in")
    
    cmds.button(label="创建", command=lambda x: _create_skeleton_cmd())
    cmds.button(label="关闭", command=lambda x: cmds.deleteUI(window))
    
    cmds.showWindow(window)

def _create_skeleton_cmd():
    """创建骨架的具体命令"""
    skeleton_type = cmds.radioButtonGrp("skeletonType", query=True, select=True)
    
    # 根据选择的类型创建不同的骨架
    if skeleton_type == 1:  # 人形
        # 创建一个简单的人形骨架
        cmds.select(clear=True)
        root = cmds.joint(p=(0, 0, 0), name="root")
        spine1 = cmds.joint(p=(0, 5, 0), name="spine1")
        spine2 = cmds.joint(p=(0, 10, 0), name="spine2")
        neck = cmds.joint(p=(0, 15, 0), name="neck")
        head = cmds.joint(p=(0, 20, 0), name="head")
        
        # 返回到spine2
        cmds.select("spine2")
        
        # 创建左臂
        cmds.joint(p=(5, 10, 0), name="l_clavicle")
        l_shoulder = cmds.joint(p=(10, 10, 0), name="l_shoulder")
        l_elbow = cmds.joint(p=(15, 10, 0), name="l_elbow")
        l_wrist = cmds.joint(p=(20, 10, 0), name="l_wrist")
        
        # 返回到spine2
        cmds.select("spine2")
        
        # 创建右臂
        cmds.joint(p=(-5, 10, 0), name="r_clavicle")
        r_shoulder = cmds.joint(p=(-10, 10, 0), name="r_shoulder")
        r_elbow = cmds.joint(p=(-15, 10, 0), name="r_elbow")
        r_wrist = cmds.joint(p=(-20, 10, 0), name="r_wrist")
        
        # 返回到root
        cmds.select("root")
        
        # 创建左腿
        cmds.joint(p=(2, 0, 0), name="l_hip")
        l_knee = cmds.joint(p=(2, -10, 0), name="l_knee")
        l_ankle = cmds.joint(p=(2, -20, 0), name="l_ankle")
        l_foot = cmds.joint(p=(2, -20, 5), name="l_foot")
        
        # 返回到root
        cmds.select("root")
        
        # 创建右腿
        cmds.joint(p=(-2, 0, 0), name="r_hip")
        r_knee = cmds.joint(p=(-2, -10, 0), name="r_knee")
        r_ankle = cmds.joint(p=(-2, -20, 0), name="r_ankle")
        r_foot = cmds.joint(p=(-2, -20, 5), name="r_foot")
        
        cmds.select(clear=True)
        
    elif skeleton_type == 2:  # 四足
        # 创建一个简单的四足骨架
        cmds.select(clear=True)
        root = cmds.joint(p=(0, 10, 0), name="root")
        spine1 = cmds.joint(p=(0, 10, 5), name="spine1")
        spine2 = cmds.joint(p=(0, 10, 10), name="spine2")
        spine3 = cmds.joint(p=(0, 10, 15), name="spine3")
        neck = cmds.joint(p=(0, 12, 20), name="neck")
        head = cmds.joint(p=(0, 15, 25), name="head")
        
        # 前腿
        cmds.select("spine1")
        
        # 创建左前腿
        cmds.joint(p=(5, 10, 5), name="l_frontLeg1")
        l_frontLeg2 = cmds.joint(p=(5, 5, 5), name="l_frontLeg2")
        l_frontFoot = cmds.joint(p=(5, 0, 5), name="l_frontFoot")
        
        # 创建右前腿
        cmds.select("spine1")
        cmds.joint(p=(-5, 10, 5), name="r_frontLeg1")
        r_frontLeg2 = cmds.joint(p=(-5, 5, 5), name="r_frontLeg2")
        r_frontFoot = cmds.joint(p=(-5, 0, 5), name="r_frontFoot")
        
        # 后腿
        cmds.select("spine3")
        
        # 创建左后腿
        cmds.joint(p=(5, 10, 15), name="l_backLeg1")
        l_backLeg2 = cmds.joint(p=(5, 5, 15), name="l_backLeg2")
        l_backFoot = cmds.joint(p=(5, 0, 15), name="l_backFoot")
        
        # 创建右后腿
        cmds.select("spine3")
        cmds.joint(p=(-5, 10, 15), name="r_backLeg1")
        r_backLeg2 = cmds.joint(p=(-5, 5, 15), name="r_backLeg2")
        r_backFoot = cmds.joint(p=(-5, 0, 15), name="r_backFoot")
        
        # 尾巴
        cmds.select("spine3")
        tail1 = cmds.joint(p=(0, 10, 20), name="tail1")
        tail2 = cmds.joint(p=(0, 10, 25), name="tail2")
        tail3 = cmds.joint(p=(0, 10, 30), name="tail3")
        
        cmds.select(clear=True)
        
    else:  # 自定义
        # 显示提示信息
        cmds.confirmDialog(
            title="自定义骨架",
            message="暂不支持自定义骨架，请手动创建或联系技术支持。",
            button=["确定"],
            defaultButton="确定"
        )
    
    # 关闭窗口
    if cmds.window("createSkeletonWindow", exists=True):
        cmds.deleteUI("createSkeletonWindow")
    
    # 显示创建完成的提示
    cmds.inViewMessage(
        amg="骨架创建完成",
        pos="midCenter",
        fade=True,
        fadeOutTime=2.0
    )

def mirror_skeleton():
    """镜像骨骼"""
    # 显示一个简单的UI窗口
    if cmds.window("mirrorSkeletonWindow", exists=True):
        cmds.deleteUI("mirrorSkeletonWindow")
    
    window = cmds.window("mirrorSkeletonWindow", title="镜像骨骼", widthHeight=(300, 200))
    cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnOffset=["both", 10])
    
    cmds.text(label="请选择要镜像的根骨骼，然后选择镜像方向")
    
    cmds.separator(height=10, style="in")
    
    cmds.radioButtonGrp("mirrorPlane", label="镜像平面", labelArray3=["YZ (X轴)", "XZ (Y轴)", "XY (Z轴)"], numberOfRadioButtons=3, select=1)
    cmds.checkBox("mirrorBehavior", label="镜像行为", value=True)
    
    cmds.separator(height=10, style="in")
    
    cmds.button(label="镜像", command=lambda x: _mirror_skeleton_cmd())
    cmds.button(label="关闭", command=lambda x: cmds.deleteUI(window))
    
    cmds.showWindow(window)

def _mirror_skeleton_cmd():
    """镜像骨骼的具体命令"""
    # 获取选中的骨骼
    selection = cmds.ls(selection=True, type="joint")
    
    if not selection:
        cmds.confirmDialog(
            title="错误",
            message="请先选择要镜像的根骨骼！",
            button=["确定"],
            defaultButton="确定"
        )
        return
    
    # 获取镜像设置
    mirror_plane = cmds.radioButtonGrp("mirrorPlane", query=True, select=True)
    mirror_behavior = cmds.checkBox("mirrorBehavior", query=True, value=True)
    
    # 设置镜像平面
    if mirror_plane == 1:
        mirror_across = "YZ"
    elif mirror_plane == 2:
        mirror_across = "XZ"
    else:
        mirror_across = "XY"
    
    # 执行镜像操作
    try:
        cmds.select(selection[0])
        cmds.mirrorJoint(
            mirrorYZ=(mirror_across=="YZ"),
            mirrorXZ=(mirror_across=="XZ"),
            mirrorXY=(mirror_across=="XY"),
            mirrorBehavior=mirror_behavior,
            searchReplace=["l_", "r_"]
        )
        
        # 显示成功消息
        cmds.inViewMessage(
            amg="骨骼镜像完成",
            pos="midCenter",
            fade=True,
            fadeOutTime=2.0
        )
    except Exception as e:
        # 显示错误消息
        cmds.confirmDialog(
            title="错误",
            message=f"镜像骨骼失败: {str(e)}",
            button=["确定"],
            defaultButton="确定"
        )
    
    # 关闭窗口
    if cmds.window("mirrorSkeletonWindow", exists=True):
        cmds.deleteUI("mirrorSkeletonWindow")

# 当脚本被直接执行时的入口点
if __name__ == "__main__":
    create_skeleton()