class AppError(Exception):
    pass

class ValidationError(AppError):
    pass

class DataSourceError(AppError):
    pass

class StudentNotFoundError(AppError):
    pass

class DuplicateIdError(AppError):
    pass