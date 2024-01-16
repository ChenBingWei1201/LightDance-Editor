from . import animation, async_core, auth, editor, pos_editor, setup, slider


def register():
    async_core.register()
    setup.register()
    auth.register()
    editor.register()
    slider.register()
    animation.register()
    pos_editor.register()


def unregister():
    async_core.unregister()
    setup.unregister()
    auth.unregister()
    editor.unregister()
    slider.unregister()
    animation.unregister()
    pos_editor.unregister()
