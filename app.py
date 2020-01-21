# GEN HACKATON 2020
# 9:30PM - 3:09AM
# PROJECT: BOOKLOG

from flask import Flask, render_template, request, redirect, url_for
from datetime import date
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect("books.db", check_same_thread=False)
try:
    conn.execute(
        """CREATE TABLE BOOKS
                (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                TITLE   TEXT    NOT NULL,
                AUTHOR  TEXT    NOT NULL,
                PAGES   INT     NOT NULL,
                STARTDATE TEXT NOT NULL,
                ENDDATE TEXT NOT NULL,
                STATUS  TEXT    NOT NULL);"""
    )
except:
    pass


@app.route("/bookentry")
def home():
    return render_template("entry.html")


@app.route("/")
@app.route("/home")
@app.route("/viewbooks")
def viewbooks():
    bookList = []
    cursor = conn.execute("SELECT ID, TITLE, AUTHOR, PAGES, STATUS, STARTDATE, ENDDATE FROM BOOKS")
    for row in cursor:
        book = [row[0], row[1], row[2], row[3], row[4], row[5], row[6]]
        bookList.append(book)

    return render_template("viewbooks.html", bookList=bookList)


@app.route("/addbook", methods=["POST"])
def addBook():
    bookTitle = request.form.get("title")
    bookAuthor = request.form.get("author")
    bookPages = request.form.get("pages")
    startDate = date.today()

    if not bookTitle or not bookAuthor or not bookPages:
        return render_template("fail.html")
    else:
        conn.execute(
            f'INSERT INTO BOOKS (TITLE, AUTHOR, PAGES, STATUS, STARTDATE, ENDDATE)VALUES ("{bookTitle}", "{bookAuthor}", "{bookPages}", "True", "{startDate}", "");'
        )
        conn.commit()
        return render_template("success.html")


@app.route("/setbookstatus", methods=["POST", "GET"])
def setBookStatus():
    bookId = request.args.get("bookid")
    currentStatus = request.args.get("currentstatus")
    endDate = date.today()

    if currentStatus == "True":
        conn.execute(f'UPDATE BOOKS SET STATUS = "False" WHERE ID = {bookId}')
        conn.execute(f'UPDATE BOOKS SET ENDDATE = "{endDate}" WHERE ID = {bookId}')

    elif currentStatus == "False":
        conn.execute(f'UPDATE BOOKS SET STATUS = "True" WHERE ID = {bookId}')

    conn.commit()
    return redirect("/viewbooks")


@app.route("/deletebook", methods=["GET"])
def deleteBook():
    bookId = request.args.get("bookid")
    conn.execute(f"DELETE FROM BOOKS WHERE ID = {bookId}")
    conn.commit()
    return redirect("/viewbooks")


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=4000)
