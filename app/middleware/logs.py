from fastapi import Request
from fastapi.routing import APIRoute
import time
from app.logger import logger

class LoggingRoute(APIRoute):
    def get_route_handler(self):
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request):
            start_time = time.time()
            response = await original_route_handler(request)
            process_time = time.time() - start_time
            formatted_process_time = '{0:.2f}'.format(process_time * 1000)
            logger.info(
                f"method={request.method} url={request.url.path} status_code={response.status_code} "
                f"response_time={formatted_process_time}ms"
            )
            return response

        return custom_route_handler