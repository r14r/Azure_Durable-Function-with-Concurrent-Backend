import logging
import azure.functions as func
import azure.durable_functions as df

import requests
import asyncio

myApp = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@myApp.route(route="orchestrators/{functionName}")
@myApp.durable_client_input(client_name="client")
async def http_start(req: func.HttpRequest, client):
    function_name = req.route_params.get('functionName')
    instance_id = await client.start_new(function_name)
    
    logging.info(f"Started orchestration with ID = '{instance_id}'.")
    return client.create_check_status_response(req, instance_id)

@myApp.orchestration_trigger(context_name="context")
def the_orchestrator(context: df.DurableOrchestrationContext):
    tasks = []

    # Replace 'website_url1', 'website_url2', etc., with the actual URLs you want to request
    websites = ['web.de', 'github.com', 'microsoft.com']

    for website in websites:
        tasks.append(context.call_activity('WebRequestActivity', website))

    # Wait for all tasks to complete in parallel
    results = yield context.task_all(tasks)

    return results

    # tasks = [context.call_activity('WebRequestActivity', website) for website in websites]

    # results = await asyncio.gather(*tasks)

    # return results


async def make_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        logging.info(f"Request to {url} succeeded with status code {response.status_code}")

        return {
            'url': url,
            'status_code': response.status_code,
            'content': response.text
        }
    except requests.exceptions.RequestException as e:
        logging.error(f"Request to {url} failed. {e}")

        return {
            'url': url,
            'error': str(e),
            'status_code': None,
            'content': None
        }


@myApp.activity_trigger(input_name="city")
async def web_request_activity(context: df.DurableActivityContext, url):
    return await context.call_activity('MakeRequest', url)
