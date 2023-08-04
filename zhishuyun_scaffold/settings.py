import environs

env = environs.Env()
env.read_env()

HTTP_HOST = env.str('HTTP_HOST', '0.0.0.0')
HTTP_PORT = env.int('HTTP_PORT', 8000)


ERROR_CODE_API_ERROR = 'api_error'
ERROR_CODE_UNKNOWN = 'unknown'
ERROR_CODE_CONNECTION_RESET = 'connection_reset'
ERROR_CODE_NOT_FOUND = 'not_found'

ERROR_DETAIL_API_ERROR = 'api internal error, please contact admin'
ERROR_DETAIL_UNKNOWN = 'unknown internal server error, please contact admin'
ERROR_DETAIL_CONNECTION_RESET = 'connection reset error, this usually caused by client closed connection'
ERROR_DETAIL_NOT_FOUND = 'not found'
