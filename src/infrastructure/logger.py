import logging


def configure_logging(level=logging.INFO):
    handlers = [
        logging.StreamHandler(),
        logging.FileHandler("sync_ad.log")
    ]

    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s",
        handlers=handlers,
    )
