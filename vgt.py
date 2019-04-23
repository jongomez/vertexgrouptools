bl_info = {
    'name': 'Vertex Group Tools',
    'author': 'Jon Gomez',
    'version': (0,1),
    'blender': (2, 80, 0),
    'location': "N Panel > Vertex Group Tools",
    'description': 'Filter vertices based on the number of vertex groups they\'re on.',
    'category': 'Vertex Group Tools'}

import bpy

class ListItem(bpy.types.PropertyGroup):
    id: bpy.props.IntProperty()

class OBJECT_OT_vertex_group_limit(bpy.types.Operator):
    bl_idname = "object.vertex_group_limit"
    bl_label = "Filter Vertices"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        #print('Influence Range:', context.scene.vg_num)
        # Nice! https://caretdashcaret.com/2014/10/15/selecting-deselecting-vertices-and-edges-with-the-blender-api/
        if bpy.context.active_object.mode == "EDIT":
            bpy.ops.mesh.select_all(action = 'DESELECT')
            
            bpy.ops.object.mode_set(mode="OBJECT")
            
            currently_selected_mesh = bpy.context.object.data
            
            #from pprint import pprint
            #pprint(dir(bpy.context))
            
            for v in currently_selected_mesh.vertices:
                if len(v.groups) >= context.scene.vg_num:
                    v.select = True
             
            # Change to back to EDIT mode.
            bpy.ops.object.mode_set(mode="EDIT")

        return {'FINISHED'}
    
class OBJECT_OT_find_vertex_groups(bpy.types.Operator):
    bl_idname = "object.find_vertex_groups"
    bl_label = "Find Vertex Groups"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Nice! https://blender.stackexchange.com/questions/28235/how-can-i-get-the-names-of-the-vertex-groups-these-vertices-are-in
        ob = bpy.context.object
        ob.my_list.clear()
        
        if bpy.context.active_object.mode == "EDIT":
            vgroup_names = {vgroup.index: vgroup.name for vgroup in context.object.vertex_groups}
            
            bpy.ops.object.mode_set(mode="OBJECT")
            
            currently_selected_mesh = bpy.context.object.data
            
            my_groups = set()    
            for v in currently_selected_mesh.vertices:
                if v.select:
                    for g in v.groups:
                        #from pprint import pprint
                        #pprint(dir(g))
                        my_groups.add(vgroup_names[g.group])

            #print("The selected groups are {}".format(my_groups))
            for unique_g in list(my_groups):
                item = ob.my_list.add()
                item.id = len(ob.my_list)
                item.name = unique_g
                    
            bpy.ops.object.mode_set(mode="EDIT")
        
        return {'FINISHED'}

class OBJECT_PT_Vertex_Tools_Main(bpy.types.Panel):
    bl_idname = "object_PT_Vertex_Tools_Main"
    bl_label = "VG Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Vertex Group Tools"

    def draw(self, context):
        layout = self.layout
        ob = context.object
        scn = context.scene

        row = layout.row()
        row.prop(scn, "vg_num")
        
        row = layout.row()
        row.operator("object.vertex_group_limit")
        
        layout.separator()

        row = layout.row()
        row.operator("object.find_vertex_groups")

        row = layout.row()
        row.template_list("UI_UL_list", "my_list_id", ob, "my_list", 
            ob, "active_list_index", rows=8)

        

def register():
    # List stuff.
    bpy.utils.register_class(ListItem)
    bpy.types.Object.my_list = bpy.props.CollectionProperty(type=ListItem)
    bpy.types.Object.active_list_index = bpy.props.IntProperty()
    
    # Main functionality.
    bpy.types.Scene.vg_num = bpy.props.IntProperty(min = 0, max = 999)
    bpy.utils.register_class(OBJECT_OT_vertex_group_limit)
    bpy.utils.register_class(OBJECT_OT_find_vertex_groups)
    bpy.utils.register_class(OBJECT_PT_Vertex_Tools_Main)

def unregister():
    bpy.utils.unregister_class(OBJECT_PT_Vertex_Tools_Main)
    bpy.utils.unregister_class(OBJECT_OT_find_vertex_groups)
    bpy.utils.unregister_class(OBJECT_OT_vertex_group_limit)
    bpy.utils.unregister_class(ListItem)

if __name__ == "__main__":
    register()