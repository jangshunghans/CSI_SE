from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import anthropic
import os

load_dotenv()  # .env 파일 자동 로드

app = Flask(__name__, static_folder='static')
CORS(app)

# API 키는 환경변수에서 읽음 (Render.com에서 설정)
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'api_key_set': bool(ANTHROPIC_API_KEY)})


@app.route('/api/generate', methods=['POST'])
def generate():
    if not ANTHROPIC_API_KEY:
        return jsonify({'error': '서버에 API 키가 설정되지 않았습니다.'}), 500

    data = request.get_json()
    system_prompt = data.get('system', '')
    user_message = data.get('message', '')

    if not user_message:
        return jsonify({'error': '문제 내용이 없습니다.'}), 400

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        response = client.messages.create(
            model='claude-sonnet-4-20250514',
            max_tokens=4000,
            system=system_prompt,
            messages=[{'role': 'user', 'content': user_message}]
        )

        return jsonify({
            'answer': response.content[0].text,
            'input_tokens': response.usage.input_tokens,
            'output_tokens': response.usage.output_tokens
        })

    except anthropic.AuthenticationError:
        return jsonify({'error': 'API 키가 올바르지 않습니다.'}), 401
    except anthropic.RateLimitError:
        return jsonify({'error': '요청이 너무 많습니다. 잠시 후 다시 시도해주세요.'}), 429
    except anthropic.APIError as e:
        return jsonify({'error': f'API 오류: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'서버 오류: {str(e)}'}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
