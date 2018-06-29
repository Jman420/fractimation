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
        remaining_rows_slice = slice(0, -1)
        remaining_columns_slice = slice(0, -1)
        if real_pixel_diff < 0:
            horizontal_z_range_params.min_real_number = z_first_real_num - z_real_range_diff
            horizontal_z_range_params.max_real_number = z_values_range.real_number_values[0][real_pixel_diff]
            vertical_z_range_params.min_real_number = horizontal_z_range_params.min_real_number
            vertical_z_range_params.max_real_number = z_values_range.real_number_values[0][-1]

            horizontal_c_range_params.min_real_number = c_first_real_num - c_real_range_diff
            horizontal_c_range_params.max_real_number = c_values_range.real_number_values[0][real_pixel_diff]
            vertical_c_range_params.min_real_number = horizontal_c_range_params.min_real_number
            vertical_c_range_params.max_real_number = z_values_range.real_number_values[0][-1]

            remaining_columns_slice = slice(0, real_pixel_diff)
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

            remaining_columns_slice = slice(real_pixel_diff, -1)

        if imaginary_pixel_diff < 0:
            horizontal_z_range_params.max_imaginary_number = z_values_range.imaginary_number_values[imaginary_pixel_diff][0]
            vertical_z_range_params.min_imaginary_number = z_first_imaginary_num - z_imaginary_range_diff
            vertical_z_range_params.max_imaginary_number = z_values_range.imaginary_number_values[0][imaginary_pixel_diff]

            horizontal_c_range_params.max_imaginary_number = c_values_range.imaginary_number_values[imaginary_pixel_diff][0]
            vertical_c_range_params.min_imaginary_number = c_first_imaginary_num - c_imaginary_range_diff
            vertical_c_range_params.max_imaginary_number = z_values_range.imaginary_number_values[0][imaginary_pixel_diff]

            remaining_rows_slice = slice(0, imaginary_pixel_diff)
        elif imaginary_pixel_diff > 0:
            z_last_imaginary_num = z_values_range.imaginary_number_values[-1][-1]
            horizontal_z_range_params.min_imaginary_number = z_values_range.imaginary_number_values[imaginary_pixel_diff][-1]
            vertical_z_range_params.min_imaginary_number = z_values_range.imaginary_number_values[-1][imaginary_pixel_diff]
            vertical_z_range_params.max_imaginary_number = z_last_imaginary_num + z_imaginary_range_diff

            c_last_imaginary_num = c_values_range.imaginary_number_values[-1][-1]
            horizontal_c_range_params.min_imaginary_number = c_values_range.imaginary_number_values[imaginary_pixel_diff][-1]
            vertical_c_range_params.min_imaginary_number = c_values_range.imaginary_number_values[-1][imaginary_pixel_diff]
            vertical_c_range_params.max_imaginary_number = c_last_imaginary_num + c_imaginary_range_diff

            remaining_rows_slice = slice(imaginary_pixel_diff, -1)
            
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

        for frame_counter in range(len(orig_render_cache)):
            # get renders for new areas
            horizontal_frame = horizontal_area_renderer.render(frame_counter)
            vertical_frame = vertical_area_renderer.render(frame_counter)
            
            # slice original frame for remaining image
            orig_frame = render_cache[frame_counter]
            remaining_image = orig_frame[remaining_rows_slice, remaining_columns_slice]

            # construct new image frame
            new_frame = numpy.copy(orig_frame)
            if real_pixel_diff < 0:
                new_frame = _append_array_2d(horizontal_frame, new_frame, 0)
            elif real_pixel_diff > 0:
                new_frame = _append_array_2d(new_frame, horizontal_frame, 0)

            if imaginary_pixel_diff < 0:
                new_frame = _append_array_2d(vertical_frame, new_frame, imaginary_pixel_diff)
            elif imaginary_pixel_diff > 0:
                new_frame = _append_array_2d(new_frame, vertical_frame, imaginary_pixel_diff)

            # replace original render cache entry
            render_cache[frame_counter] = new_frame

        # split renderer's iterator z & c values into 2d arrays along image dimensions
        fractal_iterator = self._renderer.get_fractal_iterator()
        orig_z_values = fractal_iterator.get_z_values()
        orig_c_values = fractal_iterator.get_c_values()
        remaining_z_values = orig_z_values[remaining_rows_slice, remaining_columns_slice]
        remaining_c_values = orig_c_values[remaining_rows_slice, remaining_columns_slice]

        # get new area iterators
        horizontal_iterator = horizontal_area_renderer.get_fractal_iterator()
        horizontal_iterator_z_values = horizontal_iterator.get_z_values()
        horizontal_iterator_c_values = horizontal_iterator.get_c_values()

        vertical_iterator = vertical_area_renderer.get_fractal_iterator()
        vertical_iterator_z_values = vertical_iterator.get_z_values()
        vertical_iterator_c_values = vertical_iterator.get_c_values()

        # inject final z & c values from new areas iterators into z & c value 2d arrays
        new_z_values = orig_z_values
        new_c_values = orig_c_values
        if real_pixel_diff < 0:
            new_z_values = _append_array_2d(horizontal_iterator_z_values, new_z_values, 0)
            new_c_values = _append_array_2d(horizontal_iterator_c_values, new_c_values, 0)
        elif real_pixel_diff > 0:
            new_z_values = _append_array_2d(new_z_values, horizontal_iterator_z_values, 0)
            new_c_values = _append_array_2d(new_c_values, horizontal_iterator_c_values, 0)

        if imaginary_pixel_diff < 0:
            new_z_values = _append_array_2d(vertical_iterator_z_values, new_z_values, imaginary_pixel_diff)
            new_c_values = _append_array_2d(vertical_iterator_c_values, new_c_values, imaginary_pixel_diff)
        elif imaginary_pixel_diff > 0:
            new_z_values = _append_array_2d(new_z_values, vertical_iterator_z_values, imaginary_pixel_diff)
            new_c_values = _append_array_2d(new_c_values, vertical_iterator_c_values, imaginary_pixel_diff)

        # replace renderer's iterator z & c values
        fractal_iterator.set_z_values(new_z_values)
        fractal_iterator.set_c_values(new_c_values)

        # update original iterable to reflect full image's range
        new_z_range_params = copy(orig_z_range_params)
        new_z_range_params.min_real_number += z_real_range_diff
        new_z_range_params.max_real_number += z_real_range_diff
        new_z_range_params.min_imaginary_number += z_imaginary_range_diff
        new_z_range_params.max_imaginary_number += z_imaginary_range_diff

        new_c_range_params = copy(orig_c_range_params)
        new_c_range_params.min_real_number += c_real_range_diff
        new_c_range_params.max_real_number += c_real_range_diff
        new_c_range_params.min_imaginary_number += c_imaginary_range_diff
        new_c_range_params.max_imaginary_number += c_imaginary_range_diff

        fractal_iterable.initialize(new_z_range_params, new_c_range_params, dimension_params,
                                    formula_params, max_iterations)
