from flask import Flask, render_template, request, jsonify, redirect
import requests

app = Flask(__name__)

# 🔥 FORCE HTTPS LOGIC (Naya Code) 🔥
# Isse har user automatic Secure (Green Lock) wale link par chala jayega
@app.before_request
def before_request():
    scheme = request.headers.get('X-Forwarded-Proto')
    if scheme and scheme == 'http':
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_video():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'success': False, 'message': 'Please enter a valid URL'})

    api_url = "https://www.tikwm.com/api/"
    payload = {'url': url, 'count': 12, 'cursor': 0, 'web': 1, 'hd': 1}
    
    try:
        response = requests.post(api_url, data=payload)
        json_data = response.json()

        if 'data' in json_data:
            video_data = json_data['data']
            base_url = "https://www.tikwm.com"
            
            play_url = video_data.get('hdplay')
            if not play_url:
                play_url = video_data.get('play')

            if play_url and not play_url.startswith('http'):
                play_url = base_url + play_url

            cover_url = video_data.get('cover')
            if cover_url and not cover_url.startswith('http'):
                cover_url = base_url + cover_url

            return jsonify({
                'success': True,
                'title': video_data.get('title', 'TikTok Video'),
                'author': video_data.get('author', {}).get('nickname', 'Unknown'),
                'thumbnail': cover_url,
                'download_url': play_url
            })
        else:
            return jsonify({'success': False, 'message': 'Video not found or Private'})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': 'Server Error'})

if __name__ == '__main__':
    app.run(debug=True)