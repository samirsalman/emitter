import logging
import logging.handlers


def set_level(
    level: int = logging.DEBUG,
):
    logging.getLogger().setLevel(level)


def add_log_file(
    level: int = logging.DEBUG,
    dirpath: str = "logs",
    file_prefix: str = "emitter",
):
    import datetime
    import os

    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    filename = f"{file_prefix}-{datetime.datetime.now().strftime('%Y-%m-%d')}.log"
    filepath = os.path.join(dirpath, filename)

    # add a rotating handler
    handler = logging.handlers.RotatingFileHandler(
        filepath,
        maxBytes=1024 * 1024,
        backupCount=3,
    )

    handler.setLevel(level)
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )

    logging.getLogger().addHandler(handler)
    logging.getLogger().info(f"Logging to: {filepath}")
