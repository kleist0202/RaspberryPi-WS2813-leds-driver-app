from website import create_app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, threaded=False, host="0.0.0.0", processes=1)
