from flask import Flask, Response, jsonify, request
from time import time
from key_val_store import KeyValStore, TTL

app = Flask(__name__)
key_val_store = KeyValStore()


# GET /values
@app.route('/values', methods=['GET'])
def get_values():
    key_val_store.remove_expired_keys()
    
    if 'keys' not in request.args:
        return jsonify(key_val_store.get_keys())
    else:
        keys = request.args.get('keys').split(',')
        return get_specific_values(keys)


# GET /values?keys=key1,key2
def get_specific_values(keys):
    if keys == ['']:
        return jsonify({'error': 'No keys provided'}), 400
    
    conflicting_keys = find_conflicting_keys(keys)

    if len(conflicting_keys) != len(keys):
        missing_keys = get_missing_keys(keys, conflicting_keys)

        return jsonify({'error': f'The following keys do not exist: {", ".join(missing_keys)}'}), 404
    else:
        return jsonify(key_val_store.get_keys(keys))


# POST /values
@app.route('/values', methods=['POST'])
def save_values():
    data = request.json

    if not isinstance(data, dict):
            return jsonify({'error': 'Invalid JSON data supplied'}), 400
    
    key_val_store.remove_expired_keys()
    conflicting_keys = find_conflicting_keys(data)

    if conflicting_keys:
        return jsonify({'error': f'The following keys already exist: {", ".join(conflicting_keys)}'}), 409
    
    save_data_to_store(data)
        
    return jsonify({'message': 'Items successfully added'}), 201


# PATCH /values
@app.route('/values', methods=['PATCH'])
def update_values():
    data = request.json

    if not isinstance(data, dict):
            return jsonify({'error': 'Invalid JSON data supplied'}), 400
    
    key_val_store.remove_expired_keys()
    keys = list(data.keys())
    conflicting_keys = find_conflicting_keys(data)

    if len(conflicting_keys) != len(keys):
        missing_keys = get_missing_keys(keys, conflicting_keys)

        return jsonify({'error': f'The following keys do not exist: {", ".join(missing_keys)}'}), 404
    
    save_data_to_store(data)
        
    return Response(status=204)


def save_data_to_store(data):
    ttl = time() + TTL

    for key, value in data.items():        
        key_val_store.set_key(key, value, ttl)


def find_conflicting_keys(data):
    conflicting_keys = []

    for key in data:
        if key_val_store.check_key(key):
            conflicting_keys.append(key)

    return conflicting_keys


def get_missing_keys(list1, list2):
    set1 = set(list1)
    set2 = set(list2)

    return list(set1.symmetric_difference(set2))


if __name__ == '__main__':
    # Run the Flask application
    app.run(debug=True)