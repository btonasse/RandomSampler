import logging
import types

level_map = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

def add_separator(self: logging.Logger, level: str, message: str = '') -> None:
    '''
    Create a log record with a given string without the default formatting.
    Useful for creating separator lines in the log
    '''
    for handler in self.handlers:
        handler.setFormatter(self.naked_formatter)

    self.log(level_map[level], message)

    for handler in self.handlers:
        handler.setFormatter(self.formatter)

def logger_setup(name: str, file: str) -> logging.Logger:
    '''
    Encapsulate logger set-up and add a method called 'sep', which logs a naked string instead of the default format.
    '''  
    # Create logger
    logger = logging.getLogger(name)    
    logger.setLevel(logging.DEBUG)

    # Formatters
    formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s: %(message)s")
    naked_formatter = logging.Formatter("%(message)s")

    # Handlers
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.WARNING)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(filename=file, mode='w', encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    # Extend functionality with extra formatter
    logger.handlers = [console_handler, file_handler]
    logger.formatter = formatter
    logger.naked_formatter = naked_formatter
    logger.sep = types.MethodType(add_separator, logger)

    return logger

if __name__ == '__main__':
    logger = logger_setup('Sampler', 'test.log')
    logger.debug('Debugging...')
    logger.info('Infoing...')
    logger.sep(logging.WARNING, '*'*10)
    logger.warning('Warning...')
    logger.error('Ooopsie..')
    logger.critical('Ooopsie even more..')    


