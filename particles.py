"""
This file contains two classes: AnimationPlayer and ParticleEffects. AnimationPlayer
initializes a dictionary of particle effects for magic, attacks, monster death, 
and is also responsible for flipping the particle frames and creating the particles. 
"""

import pygame
from support import import_folder
from random import choice


class AnimationPlayer:

	def __init__(self):
		self.frames = {
			# magic
			'flame': import_folder('graphics/particles/flame/frames'),
			'aura': import_folder('graphics/particles/aura'),
			'heal': import_folder('graphics/particles/heal/frames'),
			
			# attacks 
			'claw': import_folder('graphics/particles/claw'),
			'slash': import_folder('graphics/particles/slash'),
			'sparkle': import_folder('graphics/particles/sparkle'),
			'leaf_attack': import_folder('graphics/particles/leaf_attack'),
			'thunder': import_folder('graphics/particles/thunder'),

			# monster deaths
			'squid': import_folder('graphics/particles/bone_death'),
			'raccoon': import_folder('graphics/particles/bone_death'),
			'spirit': import_folder('graphics/particles/bone_death'),
			'bamboo': import_folder('graphics/particles/bone_death'),
	        'OgreSkull': import_folder('graphics/particles/bone_death'),		
            'CyclopSkull': import_folder('graphics/particles/bone_death'),
            'EvilSkull': import_folder('graphics/particles/bone_death'),
            'OxSkull': import_folder('graphics/particles/bone_death'),

            # TODO: add leafs death particles later.
			}
	
	def reflect_images(self, frames):
		new_frames = []
		for frame in frames:
			flipped_frame = pygame.transform.flip(frame, True, False)
			new_frames.append(flipped_frame)
		return new_frames

	def create_particles(self,animation_type, pos, groups):
		animation_frames = self.frames[animation_type]
		ParticleEffect(pos,animation_frames,groups)


class ParticleEffect(pygame.sprite.Sprite):

    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
