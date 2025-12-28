import logging

from agent_sdk.agent import create_sheet

def on_crawl_complete(crawl_result):
    # Example stub: create a sheet listing URLs found
    title = f"Crawl Results - {crawl_result.get('seed','unknown')}"
        logging.info('Created sheet', sid)
        sid = create_sheet('sheets-agent@infinity-x-one-systems.iam.gserviceaccount.com', title=title)
        logging.info('Created sheet', sid)
    except Exception as e:
        logging.info('Failed to create sheet', e)
