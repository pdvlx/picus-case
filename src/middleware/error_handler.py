from flask import jsonify
import botocore

def handle_errors(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        response = {
            "status": "error",
            "message": "An internal error occurred. Please try again later."
        }
        status_code = 500

        if isinstance(e, botocore.exceptions.ClientError):
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']

            app.logger.error(f"DynamoDB ClientError occurred: {error_code} - {error_message}")

            if error_code == 'ProvisionedThroughputExceededException':
                response['message'] = "Request rate is too high. Reduce the frequency of requests."
                status_code = 429
            elif error_code == 'ResourceNotFoundException':
                response['message'] = "The requested resource could not be found."
                status_code = 404
            elif error_code == 'ConditionalCheckFailedException':
                response['message'] = "A conditional check failed."
                status_code = 400
            elif error_code == 'ValidationException':
                response['message'] = "Invalid input parameters."
                status_code = 400
            elif error_code == 'AccessDeniedException':
                response['message'] = "Access denied to the requested resource."
                status_code = 403
            else:
                response['message'] = error_message
                status_code = 500

        else:
            app.logger.error(f"An error occurred: {str(e)}")

        return jsonify(response), status_code