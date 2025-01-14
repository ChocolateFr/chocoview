from flask import Flask, render_template, request, jsonify
import uuid
import watchdict
import threading
import ai
app = Flask(__name__)
db = watchdict.WatchDict('db.json')

@app.route('/caption', methods=['POST'])
def caption():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image_file = request.files['image']
    
    
    request_id = uuid.uuid4().hex
    image_file.save(f'tmp/{request_id}')
    threading.Thread(target=lambda:ai.generate_caption(f'tmp/{request_id}',request_id, db)).start()
    return jsonify({"id": request_id})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/response', methods=['GET'])
def response():
    request_id = request.args.get('id')
    
    # Simulate response generation
    if request_id in db:
        return jsonify({"caption":db[request_id]})
    return jsonify({"error": "Response is not ready."}), 400

if __name__ == '__main__':
    app.run(debug=True)
