class Settings():
    class path:
        SCRIPTS: str = './scripts'
        FILE_STORE: str = './tmp'

    class files:
        FILENAME_PATTERN: str = r"[A-Za-z0-9.-_]+"

    class error_msg:
        FILENAME_NOT_VALID: str = "Filename not valid."
        FILE_NOT_EXISTS: str = "File not exists."
        INVALID_FILE_CONTENT: str = "Data file not valid."

        BAD_RANGE: str = "Range max value must be bigger than min value."

    class response_msg:
        FILE_OVERWRITEEN: str = 'File overwriteen.'
        FILE_STORED: str = 'File stored.'

settings = Settings()