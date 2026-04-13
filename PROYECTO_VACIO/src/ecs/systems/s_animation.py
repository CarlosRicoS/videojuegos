import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface

def system_animation(world: esper.World, delta_time: float) -> None:
    components = world.get_components(CAnimation, CSurface)
    
    for _, (c_a, c_s) in components:
        
        # disminuir cur_time
        c_a.current_animation_time -= delta_time
        # cuando cur time <= cambio de frame
        
        if (c_a.current_animation_time < 0):
            # restaurar tiempo
            c_a.current_animation_time = c_a.animation_list[c_a.curr_anim].framerate
            # cambio de frame
            c_a.current_frame += 1
        # limitar frame con start y end
            if c_a.current_frame > c_a.animation_list[c_a.curr_anim].end:
                c_a.current_frame = c_a.animation_list[c_a.curr_anim].start
            
        # calcular nueva area del rect
        rect_surf = c_s.surface.get_rect()
        c_s.area.width = rect_surf.width / c_a.number_frames
        c_s.area.x = c_s.area.width * c_a.current_frame
        