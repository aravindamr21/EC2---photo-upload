[11:27 am, 22/04/2024] ~Ʌ𝐌𝐑 > 🥷: from flask import Flask, render_template, request, redirect, url_for
import boto3
from botocore.exceptions import NoCredentialsError
import os

# AWS credentials
AWS_ACCESS_KEY_ID = 'your access key'
AWS_SECRET_ACCESS_KEY = 'your secret access key'
S3_BUCKET_NAME = 'your bucket name'

# Configure Flask
app = Flask(_name_)

# Configure Boto3 S3 client
s3 = boto3.client('s3',
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# Function to upload image to S3
def upload_to_s3(file, bucket_name, acl='public-read'):
    try:
        s3.upload_fileobj(file, bucket_name, file.filename, ExtraArgs={'ACL': acl})
        return True
    except NoCredentialsError:
        return False

# Route to render upload form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle image upload
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        upload_to_s3(file, S3_BUCKET_NAME)
        return redirect(url_for('show_image', filename=file.filename))

# Route to display the uploaded image
@app.route('/show/<filename>')
def show_image(filename):
    url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{filename}"
    return render_template('show.html', url=url)

if _name_ == '_main_':
    app.run(debug=True)
[11:28 am, 22/04/2024] ~Ʌ𝐌𝐑 > 🥷: <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Upload Image to S3</title>
</head>
<body>
    <h1>Upload Image to S3</h1>
    <form action="/upload" method="POST" enctype="multipart/form-data">
        <input type="file" name="file">
        <button type="submit">Upload</button>
    </form>
</body>
</html>
