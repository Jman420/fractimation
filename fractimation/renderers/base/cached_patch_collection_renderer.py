from abc import ABC, abstractmethod

from .cached_renderer import CachedRenderer

class CachedPatchCollectionRenderer(CachedRenderer, ABC):
    """Base class for Fratal Renderers using Matpotlib PatchCollections for rendering"""

    _cache_added_to_axes = False

    def initialize(self):
        super().initialize()

        self._cache_added_to_axes = False

    @abstractmethod
    def iterate(self):
        super().iterate()

    @abstractmethod
    def preheat_render_cache(self, max_iterations):
        super().preheat_render_cache(max_iterations)

        self._cache_added_to_axes = False

    def render(self, frame_num, axes):
        if not self._cache_added_to_axes:
            for frame_counter in range(0, len(self._render_cache)):
                frame_patches = self._render_cache[frame_counter]
                axes.add_collection(frame_patches)
            self._cache_added_to_axes = True

        if not frame_num in self._render_cache:
            for frame_counter in range(self._next_iteration_index, frame_num + 1):
                self.iterate()

                frame_patches = self._render_cache[frame_counter]
                axes.add_collection(frame_patches)

        for frame_counter in range(0, len(self._render_cache)):
            frame_patches = self._render_cache[frame_counter]
            frame_patches.set_visible(frame_counter <= frame_num)
