import omni.ext
import omni.ui as ui
import omni.kit.commands
# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class MyExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[Spawn.Cube] MyExtension startup")

        self._window = ui.Window("Spawn Cube", width=300, height=300)
        with self._window.frame:
            with ui.VStack():
                ui.Label("Some Label")

                def on_click():
                    print("clicked!")

                    omni.kit.commands.execute('CreatePrimWithDefaultXform',
	                    prim_type='Cube',
	                    attributes={'size': 100, 'extent': [(-50, -50, -50), (50, 50, 50)]})


                ui.Button("Spawn Cube", clicked_fn=lambda: on_click())

    def on_shutdown(self):
        print("[Spawn.Cube] MyExtension shutdown")
