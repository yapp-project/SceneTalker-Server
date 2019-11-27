import datetime
import os


def set_filename_format(filename, now):
    """
    file format setting
    e.g)
        {username}-{date}-{microsecond}{extension}
        hjh-2016-07-12-158859.png
    """
    return "{microsecond}-{original_name}".format(
        microsecond=now.microsecond,
        original_name=filename,
    )


def user_directory_path(instance, filename):
    """
     image upload directory setting
     e.g)
        images/{year}/{month}/{day}/{username}/{filename}
        images/2016/7/12/hjh/hjh-2016-07-12-158859.png
    """

    now = datetime.datetime.now()
    path = "upload-image/{year}/{month}/{day}/{hour}/{minute}/{second}/{username}/{filename}".format(
        year=now.year,
        month=now.month,
        day=now.day,
        hour=now.hour,
        minute=now.minute,
        second=now.second,
        username=instance.author.username,
        filename=set_filename_format(filename, now),
    )
    return path
