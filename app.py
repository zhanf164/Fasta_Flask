from flask import Flask, render_template, request, redirect, url_for, session
import os
import secrets
from Fasta_file import Fasta_file
import math

secret = secrets.token_urlsafe(32)



app = Flask(__name__, template_folder="templates/")
app.secret_key = secret

def Generate_fasta_stats(fasta):
    fasta_info = {}
    fasta_info["filename"] = fasta.filename
    fasta_info["seq_number"] = fasta.number_seqs
    fasta_info["average_length"] = fasta.average_lengths
    fasta_info["lengths"] = fasta.lengths
    fasta_info["max_length"] = fasta.max_length
    fasta_info["min_length"] = fasta.min_length
    fasta_info["average_masked"] = fasta.average_masked * 100
    fasta_info["masked"] = fasta.masked
    fasta_info["average_GC"] = fasta.average_GC * 100
    fasta_info["GC"] = fasta.GC
    fasta_info["average_gaps"] = fasta.average_gaps * 100
    fasta_info["gaps"] = fasta.gaps
    return fasta_info

def Bucketize(list):
    buckets = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    intervals = ['0-10', '10-20', '20-30','30-40','40-50','50-60','60-70','70-80','80-90','90-100']
    for i in range(len(list)):
        ind = math.floor(list[i]*100/10)
        if ind == 10:
            buckets[-1] += 1
        else: 
            buckets[ind] += 1
    return intervals, buckets

def CleanUp(filepath):
    os.remove(filepath)

@app.route("/Fasta_Home", methods=["GET", "POST"])
def Home():
    if request.method == 'POST':
        upload = request.files['fasta']
        if upload.filename != '':
            upload.save("./static/{}".format(upload.filename))
            uploaded_file = {'file': str(upload.filename)}
            static_files = os.path.join(os.getcwd(), 'static/')
            filepath = os.path.join(static_files, upload.filename)
            session["filename"] = uploaded_file
            session["filepath"] = filepath
            return redirect(url_for("Results"))
    return render_template("Homepage.html")
    


@app.route("/Fasta_Home/Bad_submission", methods=["GET", "POST"])
def Bad_submission():
    if request.method == 'POST':
        upload = request.files['fasta']
        if upload.filename != '':
            upload.save("./static/{}".format(upload.filename))
            uploaded_file = {'file': str(upload.filename)}
            static_files = os.path.join(os.getcwd(), 'static/')
            filepath = os.path.join(static_files, upload.filename)
            session["filename"] = uploaded_file
            session["filepath"] = filepath
            return redirect(url_for("Results"))
    return render_template("Bad_submission.html")

@app.route("/Fasta_Results", methods=["GET", "POST"])
def Results():
    fasta_info = {}
    path = session.get("filepath")
    files = session.get("filename")
    fasta = Fasta_file(path)
    fasta_info = Generate_fasta_stats(fasta)
    intervals, test_buckets = Bucketize(fasta.GC)
    intervals2, test_buckets_2 = Bucketize(fasta.masked)
    print(test_buckets)
    print(test_buckets_2)
    if fasta.isfasta:
        CleanUp(path)
        return render_template("result.html", fasta_info=fasta_info, test_buckets=test_buckets, intervals=intervals, intervals2=intervals2, test_buckets_2=test_buckets_2)    
    else:
        CleanUp(path)
        return redirect(url_for("Bad_submission"))
    


if __name__ == 'main':
    app.run()
