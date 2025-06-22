# Development-of-a-Chess-Problem-Composition-Program
Requirements

- Python 3.8 or higher
- The [Stockfish chess engine](https://stockfishchess.org/download/) installed on your system

Setting the Stockfish Path

This program uses the "Stockfish" engine for chess analysis. You need to manually specify the path to the Stockfish executable on your machine.

1. Download Stockfish from: https://stockfishchess.org/download/

2. Extract the downloaded file and locate the executable:
   - Windows, something like: "C:\Users\YourName\Downloads\stockfish\stockfish-windows-x86-64.exe"

   - Linux/macOS, something like: "/home/yourname/Downloads/stockfish/stockfish"

3. Open the Python files ("genetic_algorithm.py", "GAT_Compositions.py") and find this line:

STOCKFISH_PATH = r""  # Add your Stockfish path here

Replace it with your own path. It should look something like this:

STOCKFISH_PATH = r"C:\Users\YourName\Downloads\stockfish\stockfish-windows-x86-64.exe"
or
STOCKFISH_PATH = "/home/yourname/Downloads/stockfish/stockfish"
