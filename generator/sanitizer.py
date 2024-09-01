import json

def get_json(filepath: str):
    with open(filepath, 'r') as file:
        return json.load(file)
    
if __name__ == '__main__':
    print(get_json('tests/simple_filter.json'))