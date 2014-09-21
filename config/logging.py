import logging

LOGGING_SETTING = dict(
    file_logger = dict(
        dump_file = "logs/production.log",
        logging_level = logging.DEBUG,
        # @see http://docs.python.jp/2.6/library/logging.html#formatter
        fomatter = "'%(asctime)s - [%(levelname)s] -%(name)s %(module)s, $(filename)s,  %(lineno)s - %(message)s'",
        )
    )
