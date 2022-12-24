from flask import Flask, request, send_file, render_template
from os import path
from processor import remove_video_vocal, download_yt_video
from pathlib import Path

app = Flask(__name__, template_folder = "templates")

working_dir = path.abspath(r"./working/")

@app.route("/", methods=['GET'])
def home():
    return render_template("index.html", title = 'Home')

@app.route("/process", methods=['GET'])
def process():
    args = request.args
    if "url" not in args:
        return "url param is not presented in the url!"
    yt_url = args["url"].strip()
    if not yt_url:
        return "youtube url is not presented, please paste your youtube url after ?url="
    video_path = download_yt_video(yt_url, working_dir)
    final_output = remove_video_vocal(video_path)
    return Path(final_output).name.split(".")[0]
    
@app.route("/download/<file_name>", methods=['GET'])
def download(file_name):
    return send_file(working_dir + "/" + file_name)

if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run("0.0.0.0", port=8000, debug=True)