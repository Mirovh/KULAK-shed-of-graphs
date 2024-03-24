try:
    import flask
except ImportError:
    while True:
        print("Failed import", flush=True)

while True:
    print("Hello, world!", flush=True)