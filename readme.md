OLA Recorder UI
This project provides a web-based user interface for recording and playing back lighting data using the Open Lighting Architecture (OLA).

Overview:

The ui_server.py script is the main server for the web UI. It leverages Flask to provide a simple web interface where users can control and monitor the recording of DMX data.

Features:
Start and stop recording of DMX data.
View real-time status updates of the recording process.
Manage saved recordings.
Prerequisites
To run this project, you will need:

Python 3.x
Flask
OLA (Open Lighting Architecture)
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/trigx300/OLA-recorder-ui.git
cd OLA-recorder-ui
Install the required Python packages:

bash
Copy code
pip install Flask
Ensure OLA is installed and configured on your system. You can find installation instructions for OLA here.

Usage
Start the server:

bash
Copy code
python ui_server.py
Open your web browser and navigate to http://localhost:5000.

Use the web interface to start and stop recording, and to manage your recordings.

Script Details
ui_server.py
This script sets up a Flask server with the following routes:

/: Serves the main web interface.
/start_recording: Starts recording DMX data.
/stop_recording: Stops the current recording session.
/status: Provides the current status of the recording process.
/recordings: Lists all saved recordings.
The server communicates with OLA to handle the recording and playback of DMX data.

Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
For questions or support, please open an issue in the repository or contact the project maintainer.
