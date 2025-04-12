/*
Nexus - 3ds Max武器部门启动脚本
为3ds Max配置武器制作环境
*/

-- 设置环境变量和路径
fn setupEnvironment = (
    -- 获取Nexus主目录
    nexusHome = getEnvironmentVariable "NEXUS_HOME"
    if nexusHome == undefined do (
        -- 如果环境变量未设置，尝试从脚本路径推断
        scriptPath = getFilenamePath (getThisScriptFilename())
        nexusHome = scriptPath + "\\..\\.."
    )
    
    -- 将路径转换为绝对路径
    nexusHome = pathConfig.convertPathToAbsolute nexusHome
    
    -- 添加脚本路径
    maxScriptsPath = nexusHome + "\\scripts\\max"
    weaponScriptsPath = maxScriptsPath + "\\weapon"
    
    -- 将路径添加到3ds Max的脚本路径
    scriptPaths = pathConfig.getScriptPaths()
    if findString scriptPaths maxScriptsPath == undefined do (
        pathConfig.appendScriptPath maxScriptsPath
    )
    if findString scriptPaths weaponScriptsPath == undefined do (
        pathConfig.appendScriptPath weaponScriptsPath
    )
    
    -- 返回Nexus主目录
    print "已设置3ds Max武器环境"
    return nexusHome
)

-- 创建武器工具菜单
fn createWeaponMenu = (
    -- 如果菜单已存在，先删除
    if menuMan.findMenu "武器工具" != undefined do (
        weaponMenu = menuMan.findMenu "武器工具"
        menuMan.unRegisterMenu weaponMenu
    )
    
    -- 创建主菜单
    weaponMainMenu = menuMan.createMenu "武器工具"
    
    -- 创建菜单项
    weaponSubmenu1 = menuMan.createSubMenu "建模工具"
    weaponSubmenu2 = menuMan.createSubMenu "UV工具"
    weaponSubmenu3 = menuMan.createSubMenu "纹理工具"
    
    -- 添加命令到菜单
    -- 建模工具子菜单
    modelingAction1 = menuMan.createActionItem "fileIn (getScriptPath() + \"\\weapon\\modeling\\create_weapon_base.ms\")" "Nexus.Weapon.Modeling"
    modelingAction1.setTitle "创建武器基础结构"
    weaponSubmenu1.addItem modelingAction1 -1
    
    modelingAction2 = menuMan.createActionItem "fileIn (getScriptPath() + \"\\weapon\\modeling\\optimize_mesh.ms\")" "Nexus.Weapon.Modeling"
    modelingAction2.setTitle "优化模型"
    weaponSubmenu1.addItem modelingAction2 -1
    
    -- 添加分隔线
    weaponSubmenu1.addItem (menuMan.createSeparatorItem()) -1
    
    modelingAction3 = menuMan.createActionItem "fileIn (getScriptPath() + \"\\weapon\\modeling\\export_model.ms\")" "Nexus.Weapon.Modeling"
    modelingAction3.setTitle "导出模型"
    weaponSubmenu1.addItem modelingAction3 -1
    
    -- UV工具子菜单
    uvAction1 = menuMan.createActionItem "fileIn (getScriptPath() + \"\\weapon\\uv\\auto_unwrap.ms\")" "Nexus.Weapon.UV"
    uvAction1.setTitle "自动展UV"
    weaponSubmenu2.addItem uvAction1 -1
    
    uvAction2 = menuMan.createActionItem "fileIn (getScriptPath() + \"\\weapon\\uv\\pack_uvs.ms\")" "Nexus.Weapon.UV"
    uvAction2.setTitle "UV排列"
    weaponSubmenu2.addItem uvAction2 -1
    
    -- 纹理工具子菜单
    textureAction1 = menuMan.createActionItem "fileIn (getScriptPath() + \"\\weapon\\texture\\create_texture_template.ms\")" "Nexus.Weapon.Texture"
    textureAction1.setTitle "创建纹理模板"
    weaponSubmenu3.addItem textureAction1 -1
    
    textureAction2 = menuMan.createActionItem "fileIn (getScriptPath() + \"\\weapon\\texture\\batch_assign_materials.ms\")" "Nexus.Weapon.Texture"
    textureAction2.setTitle "批量设置材质"
    weaponSubmenu3.addItem textureAction2 -1
    
    -- 将子菜单添加到主菜单
    weaponMainMenu.addItem weaponSubmenu1 -1
    weaponMainMenu.addItem weaponSubmenu2 -1
    weaponMainMenu.addItem weaponSubmenu3 -1
    
    -- 添加分隔线
    weaponMainMenu.addItem (menuMan.createSeparatorItem()) -1
    
    -- 添加加载插件选项
    pluginAction = menuMan.createActionItem "fileIn (getScriptPath() + \"\\plugin_loader.ms\")" "Nexus.Weapon"
    pluginAction.setTitle "加载插件"
    weaponMainMenu.addItem pluginAction -1
    
    -- 创建菜单栏项并注册
    weaponMenuItem = menuMan.createMainMenuItem "武器" "Nexus武器工具"
    weaponMenuItem.setSubMenu weaponMainMenu
    menuMan.registerMenu weaponMenuItem
    
    -- 更新菜单栏
    menuMan.updateMenuBar()
    
    print "已创建武器工具菜单"
    true
)

-- 加载武器相关的3ds Max插件
fn loadWeaponPlugins = (
    -- 获取Nexus主目录
    nexusHome = getEnvironmentVariable "NEXUS_HOME"
    if nexusHome == undefined do (
        -- 如果环境变量未设置，尝试从脚本路径推断
        scriptPath = getFilenamePath (getThisScriptFilename())
        nexusHome = scriptPath + "\\..\\.."
    )
    
    -- 插件目录
    pluginsDir = nexusHome + "\\plugins\\max"
    
    -- 如果目录存在，添加到3ds Max的插件路径
    if doesFileExist pluginsDir do (
        pluginPaths = pathConfig.getPluginPaths()
        if findString pluginPaths pluginsDir == undefined do (
            pathConfig.appendPluginPath pluginsDir
        )
    )
    
    -- 加载常用插件
    weaponPlugins = #(
        "UnwrapPro.dlu",     -- 假设的UV展开插件
        "ModelOptimizer.dlu" -- 假设的模型优化插件
    )
    
    for plugin in weaponPlugins do (
        try (
            pluginPath = pluginsDir + "\\" + plugin
            if doesFileExist pluginPath do (
                loadPlugin pluginPath
                print ("已加载插件: " + plugin)
            )
        ) catch (
            print ("警告: 无法加载插件 " + plugin)
        )
    )
    
    true
)

-- 初始化武器环境
fn initialize = (
    try (
        -- 设置环境
        nexusHome = setupEnvironment()
        
        -- 加载插件
        loadWeaponPlugins()
        
        -- 创建菜单
        createWeaponMenu()
        
        -- 打印欢迎信息
        print "=================================================="
        print "欢迎使用Nexus 3ds Max武器环境"
        print "版本: 1.0.0"
        print "=================================================="
        
        true
    ) catch (
        messageBox ("初始化武器环境失败: " + (getCurrentException()))
        false
    )
)

-- 调用初始化函数
initialize()