#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
角色蒙皮工具 - 提供角色蒙皮相关功能
"""

import maya.cmds as cmds
import maya.mel as mel

def skin_tools_ui():
    """显示蒙皮工具UI"""
    # 创建窗口
    if cmds.window("nexusSkinToolsWindow", exists=True):
        cmds.deleteUI("nexusSkinToolsWindow")
    
    window = cmds.window("nexusSkinToolsWindow", title="蒙皮工具", widthHeight=(400, 300))
    main_layout = cmds.columnLayout(adjustableColumn=True, rowSpacing=5, columnOffset=["both", 10])
    
    # 标题
    cmds.text(label="Nexus 角色蒙皮工具", font="boldLabelFont")
    cmds.separator(height=10, style="in")
    
    # 蒙皮操作区域
    cmds.frameLayout(label="蒙皮操作", collapsable=True, collapse=False)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
    
    cmds.button(label="创建平滑蒙皮", command=lambda x: create_smooth_skin())
    cmds.button(label="创建刚性蒙皮", command=lambda x: create_rigid_skin())
    cmds.button(label="复制蒙皮权重", command=lambda x: copy_skin_weights())
    
    cmds.setParent(main_layout)
    
    # 权重编辑区域
    cmds.frameLayout(label="权重编辑", collapsable=True, collapse=False)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
    
    cmds.button(label="打开组件编辑器", command=lambda x: mel.eval("ComponentEditor"))
    cmds.button(label="打开绘制权重工具", command=lambda x: mel.eval("ArtPaintSkinWeightsTool"))
    cmds.button(label="均匀权重分布", command=lambda x: cmds.skinPercent(transformValue=[(0.25, 0.25, 0.25, 0.25)], normalize=True))
    
    cmds.setParent(main_layout)
    
    # 导入导出区域
    cmds.frameLayout(label="导入导出", collapsable=True, collapse=False)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
    
    cmds.button(label="导出蒙皮权重", command=lambda x: export_skin_weights())
    cmds.button(label="导入蒙皮权重", command=lambda x: import_skin_weights())
    
    cmds.setParent(main_layout)
    
    # 底部按钮
    cmds.separator(height=10, style="in")
    cmds.button(label="关闭", command=lambda x: cmds.deleteUI(window))
    
    # 显示窗口
    cmds.showWindow(window)

def create_smooth_skin():
    """创建平滑蒙皮"""
    selection = cmds.ls(selection=True)
    
    if not selection:
        cmds.confirmDialog(
            title="错误",
            message="请先选择模型和骨骼！",
            button=["确定"],
            defaultButton="确定"
        )
        return
    
    # 检查选择中是否有网格和骨骼
    meshes = cmds.ls(selection=True, type="mesh")
    if not meshes:
        meshes = cmds.listRelatives(selection, shapes=True, type="mesh")
    
    joints = cmds.ls(selection=True, type="joint")
    
    if not meshes or not joints:
        cmds.confirmDialog(
            title="错误",
            message="请同时选择模型和骨骼！",
            button=["确定"],
            defaultButton="确定"
        )
        return
    
    # 创建平滑蒙皮
    mesh_transform = cmds.listRelatives(meshes[0], parent=True)[0] if meshes[0] != selection[0] else meshes[0]
    
    try:
        cmds.skinCluster(joints, mesh_transform, tsb=True, name=f"{mesh_transform}_skinCluster")
        cmds.inViewMessage(
            amg="已创建平滑蒙皮",
            pos="midCenter",
            fade=True,
            fadeOutTime=2.0
        )
    except Exception as e:
        cmds.confirmDialog(
            title="错误",
            message=f"创建蒙皮失败: {str(e)}",
            button=["确定"],
            defaultButton="确定"
        )

def create_rigid_skin():
    """创建刚性蒙皮"""
    selection = cmds.ls(selection=True)
    
    if not selection:
        cmds.confirmDialog(
            title="错误",
            message="请先选择模型和骨骼！",
            button=["确定"],
            defaultButton="确定"
        )
        return
    
    # 检查选择中是否有网格和骨骼
    meshes = cmds.ls(selection=True, type="mesh")
    if not meshes:
        meshes = cmds.listRelatives(selection, shapes=True, type="mesh")
    
    joints = cmds.ls(selection=True, type="joint")
    
    if not meshes or not joints:
        cmds.confirmDialog(
            title="错误",
            message="请同时选择模型和骨骼！",
            button=["确定"],
            defaultButton="确定"
        )
        return
    
    # 创建刚性蒙皮
    mesh_transform = cmds.listRelatives(meshes[0], parent=True)[0] if meshes[0] != selection[0] else meshes[0]
    
    try:
        cmds.skinCluster(joints, mesh_transform, toSelectedBones=True, bindMethod=0, skinMethod=0, normalizeWeights=0, name=f"{mesh_transform}_rigidSkin")
        cmds.inViewMessage(
            amg="已创建刚性蒙皮",
            pos="midCenter",
            fade=True,
            fadeOutTime=2.0
        )
    except Exception as e:
        cmds.confirmDialog(
            title="错误",
            message=f"创建蒙皮失败: {str(e)}",
            button=["确定"],
            defaultButton="确定"
        )

def copy_skin_weights():
    """复制蒙皮权重"""
    selection = cmds.ls(selection=True)
    
    if len(selection) < 2:
        cmds.confirmDialog(
            title="错误",
            message="请选择源模型和目标模型！",
            button=["确定"],
            defaultButton="确定"
        )
        return
    
    # 获取源模型和目标模型
    source = selection[0]
    targets = selection[1:]
    
    # 检查源模型是否有蒙皮
    source_skin = mel.eval(f'findRelatedSkinCluster("{source}")')
    
    if not source_skin:
        cmds.confirmDialog(
            title="错误",
            message="源模型没有蒙皮！",
            button=["确定"],
            defaultButton="确定"
        )
        return
    
    try:
        # 复制权重到每个目标模型
        for target in targets:
            # 检查目标是否有蒙皮
            target_skin = mel.eval(f'findRelatedSkinCluster("{target}")')
            
            if not target_skin:
                # 获取源模型的骨骼
                source_joints = cmds.skinCluster(source_skin, query=True, influence=True)
                
                # 为目标创建蒙皮
                target_skin = cmds.skinCluster(source_joints, target, tsb=True, name=f"{target}_skinCluster")[0]
            
            # 复制权重
            cmds.copySkinWeights(
                sourceSkin=source_skin,
                destinationSkin=target_skin,
                noMirror=True,
                surfaceAssociation="closestPoint",
                influenceAssociation=["name", "closestJoint"]
            )
        
        cmds.inViewMessage(
            amg="已复制蒙皮权重",
            pos="midCenter",
            fade=True,
            fadeOutTime=2.0
        )
    except Exception as e:
        cmds.confirmDialog(
            title="错误",
            message=f"复制权重失败: {str(e)}",
            button=["确定"],
            defaultButton="确定"
        )

def mirror_weights():
    """镜像权重"""
    selection = cmds.ls(selection=True)
    
    if not selection:
        cmds.confirmDialog(
            title="错误",
            message="请先选择要镜像权重的模型！",
            button=["确定"],
            defaultButton="确定"
        )
        return
    
    # 创建窗口
    if cmds.window("mirrorWeightsWindow", exists=True):
        cmds.deleteUI("mirrorWeightsWindow")
    
    window = cmds.window("mirrorWeightsWindow", title="镜像权重", widthHeight=(300, 200))
    cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnOffset=["both", 10])
    
    cmds.text(label="镜像权重设置")
    cmds.separator(height=5, style="in")
    
    cmds.radioButtonGrp("mirrorDirection", label="镜像方向", labelArray3=["X轴", "Y轴", "Z轴"], numberOfRadioButtons=3, select=1)
    
    cmds.checkBox("mirrorInfluences", label="镜像骨骼", value=True)
    cmds.textFieldGrp("searchReplace", label="骨骼名称替换", text="l_:r_")
    
    cmds.separator(height=10, style="in")
    
    cmds.button(label="镜像", command=lambda x: _mirror_weights_cmd())
    cmds.button(label="关闭", command=lambda x: cmds.deleteUI(window))
    
    cmds.showWindow(window)

def _mirror_weights_cmd():
    """执行镜像权重操作"""
    selection = cmds.ls(selection=True)
    
    if not selection:
        cmds.confirmDialog(
            title="错误",
            message="请先选择要镜像权重的模型！",
            button=["确定"],
            defaultButton="确定"
        )
        return
    
    # 获取镜像设置
    mirror_direction = cmds.radioButtonGrp("mirrorDirection", query=True, select=True)
    mirror_influences = cmds.checkBox("mirrorInfluences", query=True, value=True)
    search_replace = cmds.textFieldGrp("searchReplace", query=True, text=True).split(":")
    
    # 设置镜像方向
    mirror_x = (mirror_direction == 1)
    mirror_y = (mirror_direction == 2)
    mirror_z = (mirror_direction == 3)
    
    try:
        # 对每个选中的模型执行镜像
        for obj in selection:
            # 检查是否有蒙皮
            skin_cluster = mel.eval(f'findRelatedSkinCluster("{obj}")')
            
            if not skin_cluster:
                cmds.warning(f"{obj} 没有蒙皮，跳过")
                continue
            
            # 执行镜像
            cmds.copySkinWeights(
                sourceSkin=skin_cluster,
                destinationSkin=skin_cluster,
                mirrorMode="YZ" if mirror_x else ("XZ" if mirror_y else "XY"),
                mirrorInverse=False,
                surfaceAssociation="closestPoint",
                influenceAssociation=["label", "name", "oneToOne"],
                normalize=True
            )
            
            # 如果需要镜像骨骼影响
            if mirror_influences and len(search_replace) == 2:
                search, replace = search_replace
                cmds.copySkinWeights(
                    sourceSkin=skin_cluster,
                    destinationSkin=skin_cluster,
                    noMirror=True,
                    surfaceAssociation="closestPoint",
                    influenceAssociation=["name", "closestJoint"],
                    normalize=True,
                    influenceSearchAndReplace=[search, replace]
                )
        
        cmds.inViewMessage(
            amg="权重镜像完成",
            pos="midCenter",
            fade=True,
            fadeOutTime=2.0
        )
    except Exception as e:
        cmds.confirmDialog(
            title="错误",
            message=f"镜像权重失败: {str(e)}",
            button=["确定"],
            defaultButton="确定"
        )
    
    # 关闭窗口
    if cmds.window("mirrorWeightsWindow", exists=True):
        cmds.deleteUI("mirrorWeightsWindow")

def export_skin_weights():
    """导出蒙皮权重"""
    selection = cmds.ls(selection=True)
    
    if not selection:
        cmds.confirmDialog(
            title="错误",
            message="请先选择要导出权重的模型！",
            button=["确定"],
            defaultButton="确定"
        )
        return
    
    # 获取导出路径
    export_path = cmds.fileDialog2(
        fileFilter="权重文件 (*.xml);;所有文件 (*.*)",
        dialogStyle=2,
        caption="导出权重文件",
        fileMode=0
    )
    
    if not export_path:
        return
    
    export_path = export_path[0]
    
    try:
        # 对于每个选中的对象
        for obj in selection:
            # 检查是否有蒙皮
            skin_cluster = mel.eval(f'findRelatedSkinCluster("{obj}")')
            
            if not skin_cluster:
                cmds.warning(f"{obj} 没有蒙皮，跳过")
                continue
            
            # 导出权重
            cmds.deformerWeights(
                f"{obj}_weights.xml",
                path=os.path.dirname(export_path),
                deformer=skin_cluster,
                export=True
            )
        
        cmds.inViewMessage(
            amg="权重导出完成",
            pos="midCenter",
            fade=True,
            fadeOutTime=2.0
        )
    except Exception as e:
        cmds.confirmDialog(
            title="错误",
            message=f"导出权重失败: {str(e)}",
            button=["确定"],
            defaultButton="确定"
        )

def import_skin_weights():
    """导入蒙皮权重"""
    selection = cmds.ls(selection=True)
    
    if not selection:
        cmds.confirmDialog(
            title="错误",
            message="请先选择要导入权重的模型！",
            button=["确定"],
            defaultButton="确定"
        )
        return
    
    # 获取导入路径
    import_path = cmds.fileDialog2(
        fileFilter="权重文件 (*.xml);;所有文件 (*.*)",
        dialogStyle=2,
        caption="导入权重文件",
        fileMode=1
    )
    
    if not import_path:
        return
    
    import_path = import_path[0]
    
    try:
        # 对于每个选中的对象
        for obj in selection:
            # 检查是否有蒙皮
            skin_cluster = mel.eval(f'findRelatedSkinCluster("{obj}")')
            
            if not skin_cluster:
                cmds.warning(f"{obj} 没有蒙皮，跳过")
                continue
            
            # 导入权重
            cmds.deformerWeights(
                os.path.basename(import_path),
                path=os.path.dirname(import_path),
                deformer=skin_cluster,
                import=True
            )
        
        cmds.inViewMessage(
            amg="权重导入完成",
            pos="midCenter",
            fade=True,
            fadeOutTime=2.0
        )
    except Exception as e:
        cmds.confirmDialog(
            title="错误",
            message=f"导入权重失败: {str(e)}",
            button=["确定"],
            defaultButton="确定"
        )

# 当脚本被直接执行时的入口点
if __name__ == "__main__":
    skin_tools_ui()