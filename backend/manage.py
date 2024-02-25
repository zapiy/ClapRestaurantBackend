import os, sys, logging, asyncio
from settings.settings import BASE_DIR
from django import setup


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
async def main():
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] - %(name)s - [%(filename)s(%(lineno)d) in %(funcName)s] => %(message)s",
        handlers=[
            logging.FileHandler(BASE_DIR / "conf" / "logs.log"),
            logging.StreamHandler()
        ]
    )
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    
    # from cdn.cleaner import cleaner
    # asyncio.create_task(cleaner())
    
    args = sys.argv
        
    if len(args) <= 1:
        setup()
        args.append('runserver')
        args.append('0.0.0.0:8000')
        
    execute_from_command_line(args)


if __name__ == '__main__':
    asyncio.run(main())
else:
    setup()
