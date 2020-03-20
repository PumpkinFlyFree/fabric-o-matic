import os
import bpy
import bpy.utils.previews

bl_info = {
    'name': "Fabric-o-matic",
    'description': "Library of nodes to generate various woven fabric patterns",
    'author': "qwiglydee@gmail.com",
    'version': (0, 1),
    'warning': "Beta release. Please, provide feedback to make it better",
    'blender': (2, 81, 0),
    'category': "Material",
    'location': "NodeEditor > Add > Fabric-o-matic"
}


class MenuBase(bpy.types.Menu):
    def draw_node_item(self, node_class):
        adding = self.layout.operator('node.add_node', text=node_class.bl_label)
        adding.type = node_class.bl_idname
        adding.use_transform = True


class AddNodeMenu(MenuBase, bpy.types.Menu):
    bl_idname = "NODE_MT_add_fabricomatic_component"
    bl_label = "Weaving components"

    def draw(self, _context):
        pass


class AddUtilMenu(MenuBase, bpy.types.Menu):
    bl_idname = "NODE_MT_add_fabricomatic_util"
    bl_label = "Utils"

    def draw(self, _context):
        pass


class AddMenu(MenuBase, bpy.types.Menu):
    bl_idname = "NODE_MT_add_fabricomatic"
    bl_label = "Fabric-o-matic"

    def draw(self, _context):
        layout = self.layout
        layout.menu(AddNodeMenu.bl_idname)
        layout.menu(AddUtilMenu.bl_idname)


def extend_add_menu(self, context):
    if context.area.ui_type != 'ShaderNodeTree':
        return
    self.layout.menu(AddMenu.bl_idname)


classes = (
    AddNodeMenu,
    AddUtilMenu,
    AddMenu,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.NODE_MT_add.append(extend_add_menu)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.NODE_MT_add.remove(extend_add_menu)
