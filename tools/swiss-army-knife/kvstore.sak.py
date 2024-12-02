import argparse
import sys
import json
from pathlib import Path

class KeyValueStore:
    def __init__(self, filename="kvstore.json"):
        self.filename = Path(filename)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not self.filename.exists():
            with open(self.filename, 'w') as f:
                json.dump({}, f)

    def get(self, key):
        with open(self.filename, 'r') as f:
            data = json.load(f)
            return data.get(key)

    def set(self, key, value):
        with open(self.filename, 'r+') as f:
            data = json.load(f)
            data[key] = value
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()

    def delete(self, key):
        with open(self.filename, 'r+') as f:
            data = json.load(f)
            if key in data:
                del data[key]
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()
                return True
            return False

    def list_all(self):
        with open(self.filename, 'r') as f:
            return json.load(f)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--info', action='store_true', help='Show script information')
    parser.add_argument('action', nargs='?', choices=['get', 'set', 'delete', 'list'],
                        help='Action to perform')
    parser.add_argument('key', nargs='?', help='Key to operate on')
    parser.add_argument('value', nargs='?', help='Value to set (for set action)')
    args = parser.parse_args()

    if args.info:
        print("""
Tool Name: Key-Value Store
Description: Simple persistent key-value store
Usage: swiss-army-knife kvstore action [key] [value]
Actions:
  get <key>: Get value for key
  set <key> <value>: Set key to value
  delete <key>: Delete key
  list: Show all keys and values
Example:
  swiss-army-knife kvstore set mykey myvalue
  swiss-army-knife kvstore get mykey
        """)
        return

    store = KeyValueStore()

    if args.action == 'get':
        if not args.key:
            print("Error: Key required for get action")
            return
        value = store.get(args.key)
        if value is not None:
            print(value)
        else:
            print(f"Key '{args.key}' not found")

    elif args.action == 'set':
        if not args.key or not args.value:
            print("Error: Both key and value required for set action")
            return
        store.set(args.key, args.value)
        print(f"Set {args.key} = {args.value}")

    elif args.action == 'delete':
        if not args.key:
            print("Error: Key required for delete action")
            return
        if store.delete(args.key):
            print(f"Deleted key '{args.key}'")
        else:
            print(f"Key '{args.key}' not found")

    elif args.action == 'list':
        data = store.list_all()
        if data:
            for key, value in data.items():
                print(f"{key}: {value}")
        else:
            print("Store is empty")

if __name__ == '__main__':
    main()