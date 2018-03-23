import numpy

from copy import copy

from .base.fractimation_functionality import FractimationFunctionality
from ..data_models.complex_range_params import ComplexRangeParams
from ..data_models.dimension_params import DimensionParams
from ..renderers.cached_image_renderer import CachedImageRenderer

def _append_array_2d(orig_array, values, start_index):
    new_array = numpy.copy(orig_array)
    if start_index < 0:
        for new_rows_counter in range(start_index, 0):
            new_array.insert(0, [])

    if start_index + len(values) > len(new_array):
        for new_rows_counter in range(len(new_array), start_index + len(values)):
            new_array.append([])

    for row_counter in range(0, len(values)):
        orig_row = new_array[start_index + row_counter]
        new_array[start_index + row_counter] = orig_row.append(values[row_counter])

    return new_array

# NOTE : THIS FUNCTIONALITY WILL ONLY WORK WITH LINEAR SPACED Z & C VALUES (need to outsource diff calc/map to iterable)
class PannablePixelRange(FractimationFunctionality):

    # NOTE: THIS WHOLE THING NEEDS REWRITING; ITS FAR TOO CONVOLUTED
    def pan(self, real_pixel_diff, imaginary_pixel_diff):
        # get original renderer & iterable
        fractal_iterable = self._renderer.get_fractal_iterable()

        # calculate new areas' dimensions
        dimension_params = fractal_iterable.get_dimension_params()
        horizontal_dimensions = DimensionParams(dimension_params.width, imaginary_pixel_diff)
        vertical_dimensions = DimensionParams(real_pixel_diff, dimension_params.height - imaginary_pixel_diff)

        # calculate linear diff amounts
        z_values_range = fractal_iterable.get_z_values_range()
        z_first_real_num = z_values_range.real_number_values[0][0]
        z_real_range_diff = z_values_range.real_number_values[0][abs(real_pixel_diff)] - z_first_real_num
        z_first_imaginary_num = z_values_range.imaginary_number_values[0][0]
        z_imaginary_range_diff = z_values_range.imaginary_number_values[0][abs(imaginary_pixel_diff)] - z_first_imaginary_num

        c_values_range = fractal_iterable.get_c_values_range()
        c_first_real_num = c_values_range.real_number_values[0][0]
        c_real_range_diff = c_values_range.real_number_values[0][abs(real_pixel_diff)] - c_first_real_num
        c_first_imaginary_num = c_values_range.imaginary_number_values[0][0]
        c_imaginary_range_diff = c_values_range.imaginary_number_values[0][abs(imaginary_pixel_diff)] - c_first_imaginary_num
        
        # calculate new areas' complex ranges
        orig_z_range_params = fractal_iterable.get_z_values_range_params()
        orig_c_range_params = fractal_iterable.get_c_values_range_params()

        horizontal_z_range_params = copy(orig_z_range_params)
        horizontal_c_range_params = copy(orig_c_range_params)
        vertical_z_range_params = copy(orig_z_range_params)
        vertical_c_range_params = copy(orig_c_range_params)
        if real_pixel_diff < 0:
            horizontal_z_range_params.min_real_number = z_first_real_num - z_real_range_diff
            horizontal_z_range_params.max_real_number = z_values_range.real_number_values[0][real_pixel_diff]
            vertical_z_range_params.min_real_number = horizontal_z_range_params.min_real_number
            vertical_z_range_params.max_real_number = z_values_range.real_number_values[0][-1]

            horizontal_c_range_params.min_real_number = c_first_real_num - c_real_range_diff
            horizontal_c_range_params.max_real_number = c_values_range.real_number_values[0][real_pixel_diff]
            vertical_c_range_params.min_real_number = horizontal_c_range_params.min_real_number
            vertical_c_range_params.max_real_number = z_values_range.real_number_values[0][-1]

            # calculate remaining slices
        elif real_pixel_diff > 0:
            z_last_real_num = z_values_range.real_number_values[-1][-1]
            horizontal_z_range_params.min_real_number = z_values_range.real_number_values[0][real_pixel_diff]
            horizontal_z_range_params.max_real_number = z_last_real_num + z_real_range_diff
            vertical_z_range_params.min_real_number = z_values_range.real_number_values[0][-1]
            vertical_z_range_params.max_real_number = horizontal_z_range_params.max_real_number

            c_last_real_num = c_values_range.real_number_values[-1][-1]
            horizontal_c_range_params.min_real_number = c_values_range.real_number_values[0][real_pixel_diff]
            horizontal_c_range_params.max_real_number = c_last_real_num + c_real_range_diff
            vertical_c_range_params.min_real_number = c_values_range.real_number_values[0][-1]
            vertical_c_range_params.max_real_number = horizontal_c_range_params.max_real_number

            # calculate remaining slices

        if imaginary_pixel_diff < 0:
            horizontal_z_range_params.max_imaginary_number = z_values_range.imaginary_number_values[imaginary_pixel_diff][0]
            vertical_z_range_params.min_imaginary_number = z_first_imaginary_num - z_imaginary_range_diff
            vertical_z_range_params.max_imaginary_number = z_values_range.imaginary_number_values[0][imaginary_pixel_diff]

            horizontal_c_range_params.max_imaginary_number = c_values_range.imaginary_number_values[imaginary_pixel_diff][0]
            vertical_c_range_params.min_imaginary_number = c_first_imaginary_num - c_imaginary_range_diff
            vertical_c_range_params.max_imaginary_number = z_values_range.imaginary_number_values[0][imaginary_pixel_diff]

            # calculate remaining slices
        elif imaginary_pixel_diff > 0:
            z_last_imaginary_num = z_values_range.imaginary_number_values[-1][-1]
            horizontal_z_range_params.min_imaginary_number = z_values_range.imaginary_number_values[imaginary_pixel_diff][-1]
            vertical_z_range_params.min_imaginary_number = z_values_range.imaginary_number_values[-1][imaginary_pixel_diff]
            vertical_z_range_params.max_imaginary_number = z_last_imaginary_num + z_imaginary_range_diff

            c_last_imaginary_num = c_values_range.imaginary_number_values[-1][-1]
            horizontal_c_range_params.min_imaginary_number = c_values_range.imaginary_number_values[imaginary_pixel_diff][-1]
            vertical_c_range_params.min_imaginary_number = c_values_range.imaginary_number_values[-1][imaginary_pixel_diff]
            vertical_c_range_params.max_imaginary_number = c_last_imaginary_num + c_imaginary_range_diff

            # calculate remaining slices
            
        # get renderers for newly exposed areas
        vertical_area = DimensionParams(dimension_params.get_width(), abs(imaginary_pixel_diff))
        horizontal_area = DimensionParams(abs(real_pixel_diff), dimension_params.get_height() - abs(imaginary_pixel_diff))
        
        formula_params = fractal_iterable.get_formula_params()
        max_iterations = fractal_iterable.get_max_iterations()
        image_params = self._renderer.get_image_params()

        fractal_iterable.initialize(new_z_range_params, new_c_range_params, vertical_area,
                                    formula_params, max_iterations)
        vertical_area_renderer = CachedImageRenderer(fractal_iterable, vertical_area, image_params)

        fractal_iterable.initialize(new_z_range_params, new_c_range_params, horizontal_area_area,
                                    formula_params, max_iterations)
        horizontal_area_renderer = CachedImageRenderer(fractal_iterable, horizontal_area_area, image_params)

        # get original render cache
        render_cache = self._renderer.get_render_cache()

        for frameCounter in range(len(orig_render_cache)):
            # get renders for new areas and append them appropriately
            
            # slice original frame for remaining image
            orig_frame = render_cache[frameCounter]
            remaining_image = orig_frame[remaining_rows_slice, remaining_columns_slice]

            # append new area and remaining image
            if sign > 0:
                new_image = _append_array_2d(new_area_renderer, remaining_image, -imaginary_pixel_diff)

            # replace original render cache entry

        # inject final z & c values from newly exposed iterator into renderer's iterator
        # update original iterable to reflect full image's range
        return
