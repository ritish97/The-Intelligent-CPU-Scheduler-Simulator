import sys
import os

# Ensure we can import from src directory when running main.py directly
sys.path.append(os.path.dirname(__file__))

from gui import SimulatorGUI

def main():
    app = SimulatorGUI()
    app.mainloop()

if __name__ == "__main__":
    main()
