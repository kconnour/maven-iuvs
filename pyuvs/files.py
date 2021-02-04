"""The files module contains tools for getting IUVS data files from one's
computer.
"""
import os
from typing import Any
import numpy as np
from pyuvs.misc import orbit_code


# TODO: Most of the logic here could go into a higher class like IUVSFilename
#  so that it could work on .xml files or quicklooks
# TODO: pylint says I have too many instance variables (20 / 7)
class DataFilename:
    """DataFilename is a data structure containing info from IUVS filenames.

    DataFilename accepts a string of an IUVS data filename and extracts all
    information related to the observation and processing pipeline from the
    input.

    """

    def __init__(self, filename: str) -> None:
        """
        Parameters
        ----------
        filename: str
            The IUVS data filename.

        Raises
        ------
        TypeError
            Raised if the input is not a str.
        ValueError
            Raised if the input is not an IUVS data filename.

        """
        self.__filename = filename

        self.__raise_error_if_input_is_bad()

        self.__spacecraft = self.__extract_spacecraft_from_filename()
        self.__instrument = self.__extract_instrument_from_filename()
        self.__level = self.__extract_level_from_filename()
        self.__description = self.__extract_description_from_filename()
        self.__segment = self.__extract_segment_from_description()
        self.__orbit = self.__extract_orbit_from_description()
        self.__channel = self.__extract_channel_from_description()
        self.__timestamp = self.__extract_timestamp_from_filename()
        self.__date = self.__extract_date_from_timestamp()
        self.__year = self.__extract_year_from_date()
        self.__month = self.__extract_month_from_date()
        self.__day = self.__extract_day_from_date()
        self.__time = self.__extract_time_from_timestamp()
        self.__hour = self.__extract_hour_from_time()
        self.__minute = self.__extract_minute_from_time()
        self.__second = self.__extract_second_from_time()
        self.__version = self.__extract_version_from_filename()
        self.__revision = self.__extract_revision_from_filename()
        self.__extension = self.__extract_extension_from_filename()

    def __raise_error_if_input_is_bad(self) -> None:
        self.__raise_type_error_if_input_is_not_str()
        self.__raise_value_error_if_input_is_not_iuvs_data_filename()

    def __raise_type_error_if_input_is_not_str(self) -> None:
        if not isinstance(self.__filename, str):
            raise TypeError('filename must be a str.')

    def __raise_value_error_if_input_is_not_iuvs_data_filename(self) -> None:
        checks = self.__make_filename_checks()
        if not all(checks):
            raise ValueError('The input file is not an IUVS data file.')

    def __make_filename_checks(self) -> list[bool]:
        return [self.__check_file_begins_with_mvn_iuv(),
                self.__check_filename_has_fits_extension(),
                self.__check_filename_contains_6_underscores(),
                self.__check_filename_contains_orbit()]

    def __check_file_begins_with_mvn_iuv(self) -> bool:
        return self.__filename.startswith('mvn_iuv_')

    def __check_filename_has_fits_extension(self) -> bool:
        return self.__filename.endswith('fits') or \
               self.__filename.endswith('fits.gz')

    def __check_filename_contains_6_underscores(self) -> bool:
        return self.__filename.count('_') == 6

    def __check_filename_contains_orbit(self) -> bool:
        return 'orbit' in self.__filename

    def __extract_spacecraft_from_filename(self) -> str:
        return self.__split_filename_on_underscore()[0]

    def __extract_instrument_from_filename(self) -> str:
        return self.__split_filename_on_underscore()[1]

    def __extract_level_from_filename(self) -> str:
        return self.__split_filename_on_underscore()[2]

    def __extract_description_from_filename(self) -> str:
        return self.__split_filename_on_underscore()[3]

    def __extract_segment_from_description(self) -> str:
        orbit_index = self.__get_split_index_containing_orbit()
        segments = self.__split_description()[:orbit_index]
        return '-'.join(segments)

    def __extract_orbit_from_description(self) -> int:
        orbit_index = self.__get_split_index_containing_orbit()
        orbit = self.__split_description()[orbit_index].removeprefix('orbit')
        return int(orbit)

    # TODO: In 3.10 change this to str | type(None)
    def __extract_channel_from_description(self) -> str:
        orbit_index = self.__get_split_index_containing_orbit()
        try:
            return self.__split_description()[orbit_index + 1]
        except IndexError:
            return None

    def __extract_timestamp_from_filename(self) -> str:
        return self.__split_filename_on_underscore()[4]

    def __extract_date_from_timestamp(self) -> str:
        return self.__split_timestamp()[0]

    def __extract_year_from_date(self) -> int:
        return int(self.__date[:4])

    def __extract_month_from_date(self) -> int:
        return int(self.date[4:6])

    def __extract_day_from_date(self) -> int:
        return int(self.date[6:])

    def __extract_time_from_timestamp(self) -> str:
        return self.__split_timestamp()[1]

    def __extract_hour_from_time(self) -> int:
        return int(self.__time[:2])

    def __extract_minute_from_time(self) -> int:
        return int(self.__time[2:4])

    def __extract_second_from_time(self) -> int:
        return int(self.__time[4:])

    def __extract_version_from_filename(self) -> str:
        return self.__split_filename_on_underscore()[5]

    def __extract_revision_from_filename(self) -> str:
        return self.__split_filename_on_underscore()[6]

    def __extract_extension_from_filename(self) -> str:
        return self.__split_stem_from_extension()[1]

    def __split_filename_on_underscore(self) -> list[str]:
        stem = self.__split_stem_from_extension()[0]
        return stem.split('_')

    def __split_stem_from_extension(self) -> list[str]:
        extension_index = self.__filename.find('.')
        stem = self.__filename[:extension_index]
        extension = self.__filename[extension_index + 1:]
        return [stem, extension]

    def __split_timestamp(self) -> list[str]:
        return self.__timestamp.split('T')

    def __split_description(self) -> list[str]:
        return self.__description.split('-')

    def __get_split_index_containing_orbit(self) -> int:
        return [c for c, f in enumerate(self.__split_description())
                if 'orbit' in f][0]

    def __str__(self) -> str:
        return self.__filename

    @property
    def filename(self) -> str:
        """Get the input filename.

        Returns
        -------
        str
            The input filename.

        """
        return self.__filename

    @property
    def spacecraft(self) -> str:
        """Get the spacecraft code from the filename.

        Returns
        -------
        str
            The spacecraft code.

        """
        return self.__spacecraft

    @property
    def instrument(self) -> str:
        """Get the instrument code from the filename.

        Returns
        -------
        str
            The instrument code.

        """
        return self.__instrument

    @property
    def level(self) -> str:
        """Get the data product level from the filename.

        Returns
        -------
        str
            The data product level.

        """
        return self.__level

    @property
    def description(self) -> str:
        """Get the description from the filename.

        Returns
        -------
        str
            The observation description.

        """
        return self.__description

    @property
    def segment(self) -> str:
        """Get the observation segment from the filename.

        Returns
        -------
        str
            The observation segment.

        """
        return self.__segment

    @property
    def orbit(self) -> int:
        """Get the orbit number from the filename.

        Returns
        -------
        orbit: int
            The orbit number.

        """
        return self.__orbit

    @property
    def channel(self) -> str:
        """Get the observation channel from the filename.

        Returns
        -------
        str
            The observation channel.

        """
        return self.__channel

    @property
    def timestamp(self) -> str:
        """Get the timestamp of the observation from the filename.

        Returns
        -------
        str
            The timestamp of the observation.

        """
        return self.__timestamp

    @property
    def date(self) -> str:
        """Get the date of the observation from the filename.

        Returns
        -------
        str
            The date of the observation.

        """
        return self.__date

    @property
    def year(self) -> int:
        """Get the year of the observation from the filename.

        Returns
        -------
        int
            The year of the observation.

        """
        return self.__year

    @property
    def month(self) -> int:
        """Get the month of the observation from the filename.

        Returns
        -------
        int
            The month of the observation.

        """
        return self.__month

    @property
    def day(self) -> int:
        """Get the day of the observation from the filename.

        Returns
        -------
        int
            The day of the observation.

        """
        return self.__day

    @property
    def time(self) -> str:
        """Get the time of the observation from the filename.

        Returns
        -------
        str
            The time of the observation.

        """
        return self.__time

    @property
    def hour(self) -> int:
        """Get the hour of the observation from the filename.

        Returns
        -------
        int
            The hour of the observation.

        """
        return self.__hour

    @property
    def minute(self) -> int:
        """Get the minute of the observation from the filename.

        Returns
        -------
        int
            The minute of the observation.

        """
        return self.__minute

    @property
    def second(self) -> int:
        """Get the second of the observation from the filename.

        Returns
        -------
        int
            The second of the observation.

        """
        return self.__second

    @property
    def version(self) -> str:
        """Get the version code from the filename.

        Returns
        -------
        str
            The version code.

        """
        return self.__version

    @property
    def revision(self) -> str:
        """Get the revision code from the filename.

        Returns
        -------
        rstr
            The revision code.

        """
        return self.__revision

    @property
    def extension(self) -> str:
        """Get the extension of filename.

        Returns
        -------
        str
            The extension.

        """
        return self.__extension


class DataPath:
    """A DataPath object creates absolute paths to where data products reside.

    DataPath contains methods to create strings of absolute paths to where data
    products reside, given a set of assumptions.

    """

    def __init__(self, path: str) -> None:
        """
        Parameters
        ----------
        path: str
            Absolute path of the IUVS data root location.

        Raises
        ------
        IsADirectoryError
            Raised if path does not point to a valid directory.
        TypeError
            Raised if path is not a str.

        """
        self.__path = path

        self.__raise_error_if_input_is_bad()

    def __raise_error_if_input_is_bad(self) -> None:
        self.__raise_type_error_if_input_is_not_string()
        self.__raise_is_a_directory_error_if_path_does_not_exist()

    def __raise_type_error_if_input_is_not_string(self) -> None:
        if not isinstance(self.__path, str):
            raise TypeError('path must be a str.')

    def __raise_is_a_directory_error_if_path_does_not_exist(self) -> None:
        if not os.path.exists(self.__path):
            raise IsADirectoryError('path must point to a valid directory.')

    def block(self, orbit: int) -> str:
        """Make the path to an orbit, assuming orbits are organized in blocks
        of 100 orbits.

        Parameters
        ----------
        orbit: int
            The orbit number.

        Returns
        -------
        str
            The path with orbit block appended corresponding to the input
            orbit.

        Raises
        ------
        TypeError
            Raised if orbit is not an int.

        Examples
        --------
        >>> path = DataPath('/foo/bar')
        >>> path.block(7777)
        '/foo/bar/orbit07700'

        """
        self.__raise_type_error_if_input_is_not_int(orbit, 'orbit')
        return os.path.join(self.__path, self.__block_folder_name(orbit))

    def block_paths(self, orbits: list[int]) -> list[str]:
        """Make paths to a series of orbits, assuming orbits are organized in
        blocks of 100 orbits.

        Parameters
        ----------
        orbits: list[int]
            The orbit numbers.

        Returns
        -------
        list[str]
            The path with orbit block appended corresponding to the input
            orbits.

        Raises
        ------
        TypeError
            Raised if orbits is not a list.
        ValueError
            Raised if any of the values in orbits are not ints.

        Examples
        --------
        >>> path = DataPath('/foo/bar')
        >>> path.block_paths([3495, 3500, 3505])
        ['/foo/bar/orbit03400', '/foo/bar/orbit03500', '/foo/bar/orbit03500']

        """
        self.__raise_type_error_if_input_is_not_list(orbits, 'orbits')
        try:
            return [self.block(f) for f in orbits]
        except TypeError:
            raise ValueError('Each value in orbits must be an int.') from None

    @staticmethod
    def __raise_type_error_if_input_is_not_int(quantity: Any, name: str) \
            -> None:
        if not isinstance(quantity, int):
            raise TypeError(f'{name} must be an int.')

    def __block_folder_name(self, orbit: int) -> str:
        orbit_block = self.__orbit_block(orbit)
        return f'orbit{orbit_code(orbit_block)}'

    @staticmethod
    def __orbit_block(orbit: int) -> int:
        return int(np.floor(orbit / 100) * 100)

    @staticmethod
    def __raise_type_error_if_input_is_not_list(quantity: Any, name: str) \
            -> None:
        if not isinstance(quantity, list):
            raise TypeError(f'{name} must be a list.')