import json

class Checker():

    async def check_logs_no_log():
        with open('data/logs/logs.json', 'r', encoding='utf-8') as f1:
            data = json.load(f1)

        from cogs import add_item

        


        