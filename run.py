from app import create_app

app = create_app()

if __name__ == '__main__':
    # Running locally, change host/port as needed
    app.run(debug=True, host='127.0.0.1', port=5000)
