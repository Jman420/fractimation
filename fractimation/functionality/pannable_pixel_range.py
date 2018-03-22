import numpy

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

# NOTE : THIS FUNCTIONALITY WILL ONLY WORK WITH LINEAR SPACED Z & C VALUES
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
        horizontal_z_range_params = ComplexRangeParams()
        horizontal_c_range_params = ComplexRangeParams()
        vertical_z_range_params = ComplexRangeParams()
        vertical_c_range_params = ComplexRangeParams()
        if real_pixel_diff < 0:
            horizontal_z_range_params.min_real_number = z_first_real_num - z_real_range_diff
            horizontal_z_range_params.max_real_number = z_values_range.real_number_values[0][real_pixel_diff]
            vertical_z_range_params.min_real_number = horizontal_z_range_params.min_real_number
            vertical_z_range_params.max_real_number = z_values_range.real_number_values[real_pixel_diff][0]

            horizontal_c_range_params.min_real_number = c_first_real_num - c_real_range_diff
            horizontal_c_range_params.max_real_number = c_values_range.real_number_values[0][real_pixel_diff]
            vertical_c_range_params.min_real_number = horizontal_c_range_params.min_real_number
            vertical_c_range_params.max_real_number = z_values_range.real_number_values[real_pixel_diff][0]

            ### NEED TO ALSO SET IMAGINARY RANGE (all of this needs to be outsourced to a clever method; just swap parameters)
        elif real_pixel_diff > 0:
            z_last_real_num = z_values_range.real_number_values[-1][-1]
            horizontal_z_range_params.min_real_number = z_values_range.real_number_values[0][-1]
            horizontal_z_range_params.max_real_number = z_last_real_num + z_real_range_diff
            vertical_z_range_params.min_real_number = z_values_range.real_number_values[-1][real_pixel_diff]
            vertical_z_range_params.max_real_number = horizontal_z_range_params.max_real_number

            c_last_real_num = c_values_range.real_number_values[-1][-1]
            horizontal_c_range_params.min_real_number = c_values_range.real_number_values[0][-1]
            horizontal_c_range_params.max_real_number = c_last_real_num + c_real_range_diff
            vertical_c_range_params.min_real_number = c_values_range.real_number_values[-1][real_pixel_diff]
            vertical_c_range_params.max_real_number = horizontal_c_range_params.max_real_number

            ### NEED TO ALSO SET IMAGINARY RANGE (all of this needs to be outsourced to a clever method; just swap parameters)
        if imaginary_pixel_diff > 0:
            horizontal_z_range_params.max_real_number = z_values_range[-imaginary_pixel_diff][0]

        elif imaginary_pixel_diff < 0:
            pass

        # determine complex range for newly exposed area (modify current ranges from iterable)
        orig_z_range_params = fractal_iterable.get_z_values_range_params()
        orig_c_range_params = fractal_iterable.get_c_values_range_params()
        dimension_params = fractal_iterable.get_dimension_params()
        
        new_z_range_params = ComplexRangeParams(orig_z_range_params.min_real_number, orig_z_range_params.max_real_number,
                                                orig_z_range_params.min_imaginary_number, orig_z_range_params.max_imaginary_number,
                                                orig_z_range_params.spacing_func)
        new_c_range_params = ComplexRangeParams(orig_c_range_params.min_real_number, orig_c_range_params.max_real_number,
                                                orig_c_range_params.min_imaginary_number, orig_c_range_params.max_imaginary_number,
                                                orig_c_range_params.spacing_func)
        if real_pixel_diff > 0:
            new_z_range_params.min_real_number = orig_z_range_params.max_real_number
            new_z_range_params.max_real_number = orig_z_range_params.max_real_number + (real_pixel_diff * z_real_num_step)
            new_c_range_params.min_real_number = orig_c_range_params.max_real_number
            new_c_range_params.max_real_number = orig_c_range_params.max_real_number + (real_pixel_diff * c_real_num_step)

            remaining_columns_slice = slice(imaginary_pixel_diff, dimension_params.get_height())
        elif real_pixel_diff < 0:
            new_z_range_params.min_real_number = orig_z_range_params.min_real_number + (real_pixel_diff * z_real_num_step)
            new_z_range_params.max_real_number = orig_z_range_params.min_real_number
            new_c_range_params.min_real_number = orig_c_range_params.min_real_number + (real_pixel_diff * c_real_num_step)
            new_c_range_params.max_real_number = orig_c_range_params.min_real_number

            remaining_columns_slice = slice(0, dimension_params.get_height() + imaginary_pixel_diff)

        if imaginary_pixel_diff > 0:
            new_z_range_params.min_imaginary_number = orig_z_range_params.max_imaginary_number
            new_z_range_params.max_imaginary_number = orig_z_range_params.max_imaginary_number + (imaginary_pixel_diff * z_imaginary_num_step)
            new_c_range_params.min_imaginary_number = orig_c_range_params.max_imaginary_number
            new_c_range_params.max_imaginary_number = orig_c_range_params.max_imaginary_number + (imaginary_pixel_diff * c_imaginary_num_step)

            remaining_rows_slice = slice(real_pixel_diff, dimension_params.get_width())
        else:
            new_z_range_params.min_imaginary_number = orig_z_range_params.min_imaginary_number + (imaginary_pixel_diff * z_imaginary_num_step)
            new_z_range_params.max_imaginary_number = orig_z_range_params.min_imaginary_number
            new_c_range_params.min_imaginary_number = orig_c_range_params.min_imaginary_number + (imaginary_pixel_diff * c_imaginary_num_step)
            new_c_range_params.max_imaginary_number = orig_c_range_params.min_imaginary_number

            remaining_rows_slice = slice(0, dimension_params.get_width() + real_pixel_diff)
            
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
            # get new area frame from new area renderer
            new_area_frame = new_area_renderer.render(frameCounter)

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
