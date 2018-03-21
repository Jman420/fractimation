from .base.fractimation_functionality import FractimationFunctionality

class PannablePixelRange(FractimationFunctionality):

    def pan_pixels(self, real_pixel_diff, imaginary_pixel_diff):
        ## OPTION 1
        # get renderer & iterator
        # determine complex range for newly exposed area
        # get iterator for newly exposed area
        # create image array for newly exposed area
        
        # get render cache
        # for each frame in render cache up to current frame
        #   get exploded indexes from newly exposed iterator
        #   update the newly exposed image array
        #   slice frame for remaining image
        #   inject newly exposed image array into slice
        #   replace render cache entry

        # inject final z & c values from newly exposed iterator into renderer's iterator

        ## OPTION 2  *****
        # get original renderer & iterable
        # determine complex range for newly exposed area (modify current ranges from iterable)
        # get iterator for newly exposed area (tweak iterable via initialize(), then use __iter__()?)
        # create renderer for newly exposed area

        # get original render cache
        # for each original frame in original render cache up to current frame
        #   get new area frame from new area renderer
        #   slice original frame for remaining image
        #   append new area frame to slice
        #   replace original render cache entry

        # inject final z & c values from newly exposed iterator into renderer's iterator
        # update original iterable to reflect full image's range
        return
