import bpy

from . import utilities_color


class op(bpy.types.Operator):
	bl_idname = "uv.textools_color_clear"
	bl_label = "Clear Colors"
	bl_description = "Clears the materials or vertex colors on the active object"
	bl_options = {'REGISTER', 'UNDO'}
	

	@classmethod
	def poll(cls, context):
		if not bpy.context.active_object:
			return False

		if bpy.context.active_object not in bpy.context.selected_objects:
			return False

		if bpy.context.active_object.type != 'MESH':
			return False

		#Only in UV editor mode
		if bpy.context.area.type != 'IMAGE_EDITOR':
			return False

		return True
	
	def execute(self, context):
		clear_colors(self, context)
		return {'FINISHED'}



def clear_colors(self, context):
	obj = bpy.context.active_object
	
	if bpy.context.scene.texToolsSettings.color_assign_mode == 'MATERIALS':
		previous_mode = bpy.context.active_object.mode
		bpy.ops.object.mode_set(mode='OBJECT')
		# Clear material slots
		count = len(obj.material_slots)
		for i in range(count):
			bpy.ops.object.material_slot_remove()
		# Delete materials if not used
		for material in bpy.data.materials:
			if utilities_color.material_prefix in material.name:
				if material.users == 0:
					bpy.data.materials.remove(material, do_unlink=True)
		bpy.ops.object.mode_set(mode=previous_mode)
	
	else:	#mode == VERTEXCOLORS
		vclsNames = [vcl.name for vcl in obj.data.vertex_colors]
		if 'TexTools' in vclsNames :
			if obj.data.vertex_colors['TexTools'].active == False :
				obj.data.vertex_colors['TexTools'].active = True
			bpy.ops.mesh.vertex_color_remove()


	# Show Material or Data Tab
	utilities_color.update_properties_tab()

	#Change View mode
	utilities_color.update_view_mode()


bpy.utils.register_class(op)
