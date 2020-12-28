# Built-in imports
from unittest import TestCase
import warnings
import os

# Local imports
from maven_iuvs.files.files import Files
from maven_iuvs.get_module_path import get_module_path


class TestFiles(TestCase):
    def setUp(self):
        self._path = os.path.join(os.path.dirname(os.path.abspath(
            os.path.realpath(__file__))), 'test_filenames')
        self.files = Files(os.path.join(get_module_path(), self._path), '*')


class TestFilesInit(TestFiles):
    def test_files_has_absolute_paths_attribute(self):
        self.assertTrue(hasattr(self.files, 'absolute_paths'))

    def test_files_has_filenames_attribute(self):
        self.assertTrue(hasattr(self.files, 'filenames'))

    def test_files_has_exactly_two_attributes(self):
        self.assertTrue(len(self.files.__dict__.keys()), 2)

    def test_absolute_paths_is_list(self):
        self.assertTrue(isinstance(self.files.absolute_paths, list))

    def test_filenames_is_list(self):
        self.assertTrue(isinstance(self.files.filenames, list))

    def test_nonexistent_path_raises_os_error(self):
        with self.assertRaises(OSError):
            Files('/lBGduwfTwq', '*')

    def test_int_path_raises_type_error(self):
        with self.assertRaises(TypeError):
            Files(1, '*')

    def test_int_pattern_raises_type_error(self):
        with self.assertRaises(TypeError):
            Files(get_module_path(), 1)

    def test_nonexistent_files_raises_value_error(self):
        with self.assertRaises(ValueError):
            Files(get_module_path(), '*.foo')

    def test_files_found_13_files(self):
        self.assertEqual(13, len(self.files.filenames))

    def test_all_filenames_are_in_absolute_paths(self):
        filename_in_abs_paths = [f for f in self.files.filenames if f in
                                 self.files.absolute_paths]
        self.assertTrue(all(filename_in_abs_paths))


class TestDownselectAbsoluteFiles(TestFiles):
    def test_int_input_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.files.downselect_absolute_paths(1)

    def test_nonexistent_files_raises_warning(self):
        with warnings.catch_warnings(record=True) as warning:
            warnings.simplefilter("always")
            self.files.downselect_absolute_paths('*.foo')
            self.assertEqual(1, len(warning))
            self.assertEqual(warning[-1].category, UserWarning)

    def test_nonexistent_files_output_empty_list(self):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            output = self.files.downselect_absolute_paths('*.foo')
            self.assertEqual([], output)

    def test_pattern_matches_manual_result(self):
        output = self.files.downselect_absolute_paths('mars*')
        self.assertEqual([os.path.join(self._path, 'mars_map.png')], output)


class TestDownselectFilenames(TestFiles):
    def test_int_input_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.files.downselect_filenames(1)

    def test_nonexistent_files_raises_warning(self):
        with warnings.catch_warnings(record=True) as warning:
            warnings.simplefilter("always")
            self.files.downselect_filenames('*.foo')
            self.assertEqual(1, len(warning))
            self.assertEqual(warning[-1].category, UserWarning)

    def test_nonexistent_files_output_empty_list(self):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            output = self.files.downselect_filenames('*.foo')
            self.assertEqual([], output)

    def test_pattern_matches_manual_result(self):
        output = self.files.downselect_absolute_paths('*database*')
        self.assertEqual([os.path.join(
            self._path, 'mvn_iuv_apoapse-database.csv')], output)
