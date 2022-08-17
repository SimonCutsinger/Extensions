import omni.ext
import omni.ui as ui
from .utils import get_selection
import omni.usd
import omni.kit.commands
from pxr import Gf, UsdGeom

# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.


class MyExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.

    def on_startup(self, ext_id):
        print("[casual5.super.snap] MyExtension startup")
        # Models
        self._source_prim_model_one = ui.SimpleStringModel()
        self._source_prim_model_two = ui.SimpleStringModel()

        self._window = ui.Window("Super Snap", width=300, height=200)
        with self._window.frame:
            with ui.VStack():
                with ui.HStack():
                    ui.Label("Prim 1", name="attribute_name", width=0, height=0)
                    ui.StringField(model=self._source_prim_model_one, height=0),
                    # Button that puts the selection to the string field
                    ui.Button(
                        " S ",
                        width=0,
                        height=0,
                        clicked_fn=self._on_get_selection_one,
                        tooltip="Get From Selection",
                    )
                with ui.HStack():
                    ui.Label("Prim 2", name="attribute_name", width=20, height=0)
                    ui.StringField(model=self._source_prim_model_two, height=0)
                    # Button that puts the selection to the string field
                    ui.Button(
                        " S ",
                        width=0,
                        height=0,
                        clicked_fn=self._on_get_selection_two,
                        tooltip="Get From Selection",
                    )

                def on_click_snap_3d():
                    print("clicked!")
                    self.move_to_snap_point()

                def on_click_snap(delta):
                    print("clicked!")
                    self.move_to_snap_point(delta)
                ui.Label("Alignment tools")
                with ui.HStack():
                    ui.Button("SNAP!", style={
                        "background_color": 0xff000000,
                        "font_size": 20}, clicked_fn=lambda: on_click_snap(Gf.Vec3d(1, 1, 1)))
                    ui.Button("X", style={
                        "background_color": 0x990000FF,
                        "color": 0xFF000000,
                        "font_size": 20,
                        "border_color": 0xFF000000,
                        "border_width": 2}, clicked_fn=lambda: on_click_snap(Gf.Vec3d(1, 0, 0)))
                    ui.Button("Y", style={
                        "background_color": 0x9900FF00,
                        "color": 0xFF000000,
                        "font_size": 20,
                        "border_color": 0xFF000000,
                        "border_width": 2}, clicked_fn=lambda: on_click_snap(Gf.Vec3d(0, 1, 0)))
                    ui.Button("Z", style={
                        "background_color": 0x99FF1223,
                        "color": 0xFF000000,
                        "font_size": 20,
                        "border_color": 0xFF000000,
                        "border_width": 2}, clicked_fn=lambda: on_click_snap(Gf.Vec3d(0, 0, 1)))

    def on_shutdown(self):
        print("[casual5.snap.dot] MyExtension shutdown")

    def _on_get_selection_one(self):
        """Called when the user presses the "Get From Selection" button"""
        self._source_prim_model_one.as_string = ", ".join(get_selection())

    def _on_get_selection_two(self):
        """Called when the user presses the "Get From Selection" button"""
        self._source_prim_model_two.as_string = ", ".join(get_selection())

    def move_to_snap_point(self, translate):
        stage = omni.usd.get_context().get_stage()
        path_one = self._source_prim_model_one.as_string
        path_two = self._source_prim_model_two.as_string
        prim_one = stage.GetPrimAtPath(path_one)
        prim_two = stage.GetPrimAtPath(path_two)

        snap_point = omni.usd.utils.get_world_transform_matrix(prim_one)

        prim_two_xform = UsdGeom.Xformable(prim_two)
        prim_two_world_point = omni.usd.utils.get_world_transform_matrix(prim_two)

        prim_two_world_point_location = prim_two_world_point.ExtractTranslation()

        snap_point_location = snap_point.ExtractTranslation()

        print(snap_point_location)

        delta = snap_point_location - prim_two_world_point_location
        delta = Gf.Vec3d(delta[0]*translate[0], delta[1]*translate[1], delta[2]*translate[2])

        scale, rotation, rotation_order, prim_two_local_translation = omni.usd.utils.get_local_transform_SRT(prim_two)

        xform_api = UsdGeom.XformCommonAPI(prim_two_xform)
        xform_api.SetTranslate(prim_two_local_translation+delta)

        # xform.ClearXformOpOrder()
        # Set the pose of prim_two to that of prim_one
        # xform_op = prim_two_xform.AddXformOp(UsdGeom.XformOp.TypeTransform, UsdGeom.XformOp.PrecisionDouble, "")
        # xform_op.Set(snap_point)
