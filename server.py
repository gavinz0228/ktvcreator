from flask import Flask, request, send_file
from os import path
from processor import remove_video_vocal, download_yt_video
app = Flask(__name__)

working_dir = path.abspath(r"./working/")

@app.route("/", methods=['GET'])
def hello_world():
    args = request.args
    if "url" not in args:
        return "url param is not presented in the url!"
    yt_url = args["url"].strip()
    if not yt_url:
        return "youtube url is not presented, please paste your youtube url after ?url="
    video_path = download_yt_video(yt_url, working_dir)
    final_output = remove_video_vocal(video_path)
    print(final_output)
    return send_file(final_output)

if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run("0.0.0.0", port=8080)