import sys

import panda3d.core as p3d
from direct.showbase.DirectObject import DirectObject
from direct.interval import IntervalGlobal as intervals

from .skybox import Skybox

class MainMenu(DirectObject):
    def __init__(self):
        super().__init__()

        self.root = base.loader.load_model('models/mainMenu.bam')
        self.root.reparent_to(base.render)
        self.root.set_y(10)

        self.skybox = Skybox(self.root)
        self.skybox.root.set_hpr(90,-20,-65)
        self.traverser = p3d.CollisionTraverser()
        self.ray = p3d.CollisionRay()
        picker = p3d.CollisionNode('picker')
        picker.add_solid(self.ray)
        picker.set_from_collide_mask(1)
        picker.set_into_collide_mask(0)
        self.picker = self.root.attach_new_node(picker)
        self.picker_handler = p3d.CollisionHandlerQueue()
        self.traverser.add_collider(self.picker, self.picker_handler)

        scene_camera = self.root.find('**/-Camera')
        campos = scene_camera.get_pos(self.root)
        base.camera.set_pos(campos)
        self.picker.reparent_to(base.camera)

        self.accept('escape', sys.exit)
        self.accept('q', sys.exit)
        self.accept('mouse1-up', self.handle_click)

        base.transitions.fadeIn()
        base.set_bgm('credits')

    def cleanup(self):
        self.root.remove_node()
        self.picker.remove_node()
        self.ignore_all()

    def handle_click(self):
        if not base.mouseWatcherNode.has_mouse():
            return

        mpos = base.mouseWatcherNode.get_mouse()
        self.ray.set_from_lens(base.cam.node(), *mpos)

        self.traverser.traverse(self.root)

        self.picker_handler.sort_entries()
        for entry in self.picker_handler.entries:
            npname = entry.getIntoNodePath().name

            if npname == 'StartSignSign':
                ival = base.transitions.getFadeOutIval()
                ival.append(intervals.Func(base.change_state, 'IntroCutscene', ['Universe']))
                ival.start()
                break
            elif npname == 'OptionSignSign':
                ival = base.transitions.getFadeOutIval()
                ival.append(intervals.Func(base.change_state, 'OptionMenu'))
                ival.start()
                break
            elif npname == 'QuitSignSign':
                sys.exit()

    def update(self, dt):
        pass
