from fastapi.responses import JSONResponse
import logging

logging.basicConfig(format='%(name)s-%(levelname)s|%(lineno)d:  %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

def RESPONSE_BAD_REQUEST(message:str = "Bad request", **kwargs):
    log.info(f'Returning 400 Response: {message}')
    return JSONResponse({'body': message, **kwargs}, status_code=400)
    
def RESPONSE_OK(message:str = "OK", **kwargs):
    log.info(f'Returning 200 Response: {message}')
    return JSONResponse({'body': message, **kwargs}, status_code=200)

def RESPONSE_CREATED(message:str = "Created", **kwargs):
    log.info(f'Returning 201 Response: {message}')
    return JSONResponse({'body': message, **kwargs}, status_code=201)

def RESPONSE_SERVER_ERROR(message:str = "Internal Server Error", **kwargs):
    log.info(f'Returning 500 Response: {message}')
    return JSONResponse({'body': message, **kwargs}, status_code=500)