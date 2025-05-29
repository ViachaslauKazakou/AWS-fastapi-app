import asyncio
import json
import os
from starlette.concurrency import run_in_threadpool
import time
import logging
from fastapi import HTTPException

from fastapi import HTTPException
from asyncio import FIRST_EXCEPTION

logging.basicConfig(
    level=logging.INFO,  # or DEBUG for more verbosity
    format="[%(asctime)s %(levelname)s %(name)s: %(message)s]"
)


logger = logging.getLogger("Manager")

# from fastapi.concurrency import run_in_threadpool


def sync_wrapper(task):
    """Wrapper to run a synchronous function in a thread pool"""
    return asyncio.run(task)


class ItemsManager:
    def __init__(self):
        self.items = []
        self.json_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "item.json")
        self._load_items()
    
    def _load_items(self):
        """Load items from the JSON file if it exists"""
        if os.path.exists(self.json_file_path):
            try:
                with open(self.json_file_path, 'r') as file:
                    self.items = json.load(file)
            except json.JSONDecodeError:
                self.items = []
        else:
            # Initialize with empty list if file doesn't exist
            self._save_items()
    
    def _save_items(self):
        """Save items to the JSON file"""
        with open(self.json_file_path, 'w') as file:
            json.dump(self.items, file, indent=2)

    def add_item(self, item: dict):
        self._load_items()  # Refresh from file before adding
        self.items.append(item)
        self._save_items()
        logger.info(f"Item '{item}' added and saved to item.json.")
        
    def get_item_by_id(self, item_id: int):
        """Return all items with the specified id"""
        self._load_items()  # Refresh from file before searching
        raise HTTPException(status_code=410, detail="Item not found.")
        raise HTTPException(
            status_code=400,
            detail="Bad Request: Invalid item ID."
        )
        matching_items = [
            item for item in self.items
            if item.get("id") == item_id
        ]
        return matching_items

    def remove_item(self, item):
        self._load_items()  # Refresh from file before removing
        if item in self.items:
            self.items.remove(item)
            self._save_items()
            logger.info(f"Item '{item}' removed.")
        else:
            logger.info(f"Item '{item}' not found.")

    def list_items(self):
        self._load_items()  # Refresh from file before listing
        if self.items:
            logger.info("Items in the manager:")
            for item in self.items:
                logger.info(f"- {item}")
        else:
            logger.info("No items in the manager.")

    async def parse_items_async(self, count=1, pool_size=10):
        """Parse items from the JSON file and return a list of dictionaries"""
        tasks = []
        for task in range(count):
            # Simulate some processing
            search_result = self.fake_task(task)
            tasks.append(search_result)
             
        running_tasks = [asyncio.create_task(run_in_threadpool(sync_wrapper, task)) for task in tasks]
        logger.info(f"Running tasks: {len(running_tasks)}")
        
        try:
            result = await asyncio.gather(*running_tasks)
            return result
        except Exception as e:
            for t in running_tasks:
                if not t.done():  # and t.exception():
                    # logger.error(f"Task {t} failed ")  # with exception: {t.exception()}")
                    # Log only the task id (use t.get_name() if available, else id(t))
                    task_id = getattr(t, "get_name", None)
                    if callable(task_id):
                        logger.error(f"Task {t.get_name()} failed")
                    else:
                        logger.error(f"Task id {id(t)} failed")
                    t.cancel() 
                    logger.error(f"Task id {t.get_name()} cancelled")   
            raise HTTPException(status_code=422, detail="Task failed.")
            logger.info(f"Exception: {e}")
        # if result
        # logger.info(f"Tasks completed: {result}")
        # return result
    
    async def parse_items_async2(self, count=1, pool_size=10):
        """Parse items from the JSON file and return a list of dictionaries"""
        tasks = []
        for task in range(count):
            # Schedule the synchronous fake_task in the thread pool
            tasks.append(run_in_threadpool(self.fake_task, task))
        logger.info(f"Running tasks: {len(tasks)}")
        
        try:
            result = await asyncio.gather(*tasks)
            return result
        except Exception as e:
            for t in tasks:
                if not t.done():  # and t.exception():
                    # logger.error(f"Task {t} failed ")  # with exception: {t.exception()}")
                    # Log only the task id (use t.get_name() if available, else id(t))
                    task_id = getattr(t, "get_name", None)
                    if callable(task_id):
                        logger.error(f"Task {t.get_name()} failed")
                    else:
                        logger.error(f"Task id {id(t)} failed")
                    t.cancel() 
                    logger.error(f"Task id {t.get_name()} cancelled") 
            logger.error(f"Exception: {e}")
            raise HTTPException(status_code=422, detail="Task failed.")
    
    async def parse_items(self, count=1):
        """Parse items from the JSON file and return a list of dictionaries"""
        tasks = []
        for task in range(count):
            # Simulate some processing
            search_result = self.fake_task(task)
            tasks.append(search_result)
             
        running_tasks = [asyncio.create_task(task) for task in tasks]
        logger.info(f"Running tasks: {len(running_tasks)}")
        
        result = await asyncio.gather(*running_tasks, return_exceptions=True)
        
        return result
    
    async def parse_items3(self, count=1):
        """Parse items from the JSON file and return a list of dictionaries (async version)"""
        tasks = [asyncio.create_task(self.fake_task(i)) for i in range(count)]
        logger.info(f"Running tasks: {len(tasks)}")

        try:
            done, pending = await asyncio.wait(tasks, return_when=FIRST_EXCEPTION)
            # Check for exceptions in completed tasks
            for task in done:
                if task.exception():
                    logger.error(f"Task failed with exception: {task.exception()}")
                    # Cancel all pending tasks
                    for p in pending:
                        p.cancel()
                        logger.info(f"Task {p} is cancelled")
                    # raise task.exception()
            # If no exceptions, return results
            results = [task.result() for task in done]
            return results
        except Exception as e:
            logger.error(f"Exception: {e}")
            raise HTTPException(status_code=422, detail="Task failed.")
    
    async def parse_items2(self, count=1, pool_size=10) -> list[str | BaseException]:
        """Запускает задачи пулом с ограничением по pool_size"""
        semaphore = asyncio.Semaphore(pool_size)

        async def sem_task(task_num):
            async with semaphore:
                return await self.fake_task(task_num)

        tasks = [sem_task(i) for i in range(count)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results
    
    async def fake_task(self, count):
        """Fake task to demonstrate functionality"""
        logger.info(f"Performing a fake task...{count}")
        # Simulate some processing
        await asyncio.sleep(delay=5)
        # time.sleep(2)
        if count == 5:
            logger.error("[ERROR]Fake task %s failed." % str(count))
            raise ValueError(f"Fake task {count} failed.")
        logger.info("Fake task %s completed." % str(count))
        return f"Fake task {count} completed."
    
    
if __name__ == "__main__":
    manager = ItemsManager()
    count = 30
    time_start = time.time()
    asyncio.run(manager.parse_items_async(count=count))
    time_end = time.time()
    logger.info(f"Time taken: {time_end - time_start} seconds")
    
    # logger.info("="*30)
    # time_start = time.time()
    # asyncio.run(manager.parse_items(count=count))
    # time_end = time.time()
    # logger.info(f"Time taken: {time_end - time_start} seconds")
