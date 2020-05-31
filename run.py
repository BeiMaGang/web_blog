# coding = utf8
import sys
from app import create_app

if __name__ == '__main__':
    port = 5000
    if len(sys.argv) > 1:
        port = sys.argv[1]
    app = create_app()
    app.run(host='0.0.0.0', port=port)