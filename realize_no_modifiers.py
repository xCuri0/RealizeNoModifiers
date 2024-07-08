import bpy

bl_info = {
    'name': 'Realize Instances (no modifiers)',
    'author': 'Curi0',
    'version': (0, 1),
    'blender': (2, 80, 3),
    'location': 'Object > Apply > Make Instances Real (no modifiers)',
    'description': 'Make Instances Real without copying modifiers, this avoids Blender crashing from running out of memory with large setups.',
    'doc_url': 'https://github.com/xCuri0/RealizeNoModifiers',
    'tracker_url': 'https://github.com/xCuri0/RealizeNoModifiers/issues',
    'category': 'Object',
}

class RealizeNoModifiers(bpy.types.Operator):
    bl_label = 'Make Instances Real (no modifiers)'
    bl_description = 'Make instanced objects attached to this object real without copying modifiers'
    bl_idname = 'object.realize_no_modifier'
    bl_options = {'REGISTER', 'UNDO'}
    parent: bpy.props.BoolProperty(name='Parent', default=False, description="Parent newly created objects to the original instancer")


    def is_object_instance_from_selected(self, object_instance):
        # For instanced objects we check selection of their instancer (more accurately: check
        # selection status of the original object corresponding to the instancer).
        if object_instance.parent:
            return object_instance.parent.original.select_get()
        # For non-instanced objects we check selection state of the original object.
        return object_instance.object.original.select_get()


    # Function to create a linked duplicate of an object without modifiers
    def linked_duplicate_without_modifiers(self, obj, matrix_world):
        # Create a new object with the same mesh data
        mesh_data = obj.data
        new_obj = bpy.data.objects.new(obj.name, mesh_data)

        if self.parent:
            new_obj.parent = obj

        # Link the new object to the same collection as the original object
        for collection in obj.users_collection:
            collection.objects.link(new_obj)

        # Set the location, rotation, and scale of the new object to match the original object
        new_obj.location = obj.location
        new_obj.rotation_euler = obj.rotation_euler
        new_obj.scale = obj.scale
        new_obj.matrix_world = matrix_world

        return new_obj


    def execute(self, context):
        depsgraph = bpy.context.evaluated_depsgraph_get()
        for object_instance in depsgraph.object_instances:
            if not object_instance.is_instance or not self.is_object_instance_from_selected(object_instance):
                continue

            # Duplicate and transform
            self.linked_duplicate_without_modifiers(object_instance.object.original, object_instance.matrix_world)
          
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(RealizeNoModifiers.bl_idname, text='Make Instances Real (no modifiers)')


def register():
    bpy.utils.register_class(RealizeNoModifiers)
    bpy.types.VIEW3D_MT_object_apply.append(menu_func)


def unregister():
    bpy.utils.unregister_class(RealizeNoModifiers)
    bpy.types.VIEW3D_MT_object_apply.remove(menu_func)


if __name__ == "__main__":
    register()
