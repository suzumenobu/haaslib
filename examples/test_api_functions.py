import importlib
import inspect
import os
import sys
from haaslib.examples.config import config
from haaslib.simple_executor import SimpleExecutor
import time

def run_api_function(module, func_name, executor, *args, **kwargs):
    try:
        func = getattr(module, func_name)
        if inspect.isfunction(func):
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_dir = "test_outputs"
            os.makedirs(output_dir, exist_ok=True)
            output_filename = os.path.join(output_dir, f"{func_name}_{timestamp}.txt")
            with open(output_filename, "w") as f:
                start_time = time.time()
                result = func(executor, *args, **kwargs)
                end_time = time.time()
        else:
            pass
    except Exception as e:
        pass

def main():
    executor = SimpleExecutor(
        host="127.0.0.1",
        port=8090,
        email="garrypotterr@gmail.com",
        password="IQYTCQJIQYTCQJ",
    )
    executor.authenticate()

    examples_dir = "examples"
    for filename in os.listdir(examples_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"{examples_dir}.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name)
                for name, member in inspect.getmembers(module):
                    if inspect.isclass(member):
                        for func_name, func in inspect.getmembers(member, inspect.isfunction):
                            if func_name != "__init__":
                                run_api_function(member, func_name, executor)
            except Exception as e:
                pass

if __name__ == "__main__":
    main()
