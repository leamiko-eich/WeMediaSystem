import logging


def set_my_log(path_log="logs/dev.log"):
    # 配置日志记录器
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        handlers=[
            logging.FileHandler(path_log),
            logging.StreamHandler()
        ])


    # 配置 logging
#    logger = logging.getLogger(__name__)
#    logger.setLevel(logging.INFO)
#
#    # 定义控制台处理程序
#    # console_handler = logging.StreamHandler()
#    # console_handler.setLevel(logging.DEBUG)
#    # console_handler.setFormatter(formatter)
#    # logger.addHandler(console_handler)
#
#    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#
#    file_handler = logging.FileHandler(path_log, mode='a')
#    file_handler.setLevel(logging.INFO)
#    file_handler.setFormatter(formatter)
#    logger.addHandler(file_handler)
#
#
#    logger.info("Init ")
#    logger.info("中国")
#    return logger
#