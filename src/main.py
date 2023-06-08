from api.app import create_app, add_logging_to_file

if __name__ == '__main__':
    app = create_app()
    add_logging_to_file()

    app.run(host="0.0.0.0", port=80, debug=True)
