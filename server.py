import argparse
from flask import Flask, render_template, request, jsonify
import pymorphy2
from isv_nlp_utils.constants import create_analyzers_for_every_alphabet
from isv_nlp_utils.spellcheck import perform_spellcheck
import time

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

abecedas = create_analyzers_for_every_alphabet()

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/koriguj', methods=['POST'])
def korigovanje():
    start = time.time()
    text = request.json['text']
    selected_morph = abecedas[request.json["abeceda"]]
    text, spans, proposed_corrections = perform_spellcheck(text, request.json['abeceda'], selected_morph)
    end = time.time()
    print((end - start)/60)

    resp = {
        'text': "<p>" + text.replace("\n", "<p> </p>") + '</p>',
        'spans': spans,
        'corrections': proposed_corrections
    }
    return jsonify(resp)
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
           '--port', type=int, default=666,
           help='The port to listen on (defaults to 666).')
    args = parser.parse_args()
    app.run(host='localhost', port=args.port, debug=True)

