from website import create_app

app = create_app()

# Basic app run code.
if __name__ == "__main__":
    app.run(debug=True) #debug=true means code changes are picked up without restart
    