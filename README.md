# Rating Rivals

Rating Rivals is a web application that allows disc golfers to compare their PDGA ratings with their peers. It scrapes data responsibly from the PDGA website, specifically the player history pages, to provide up-to-date and accurate comparisons based on the PDGA numbers provided in the search bar.

## Features

- Compare up to 8 players at a time
- Visualize player ratings over time
- View detailed player summaries
- Responsive design with a clean and intuitive interface

## Prerequisites

- Python 3.x
- Django
- Requests
- BeautifulSoup
- Matplotlib
- dotenv

## Setup

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/PDGA_Player_Data.git
   cd PDGA_Player_Data

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`

3. **Install dependencies:**

    ```sh
    pip install -r requirements.txt

4. **Set up environment variables:**

    Create a .env file in the root of the project and add your secret key:
    SECRET_KEY=your-new-secret-key

    You can generate a new Django secret key using the following Python script:
    
    ```sh
    from django.core.management.utils import get_random_secret_key
    print(get_random_secret_key())

5. **Apply migrations:**

    ```sh
    python manage.py migrate

6. **Run the development server:**

    ```sh
    python manage.py runserver

7. **Access the application:**

    Open your web browser and go to http://127.0.0.1:8000.

## Usage
1. Enter up to 8 PDGA player numbers separated by commas in the search bar.
2. Click "Get Player Data" to fetch and compare the player ratings.
3. The application will display a summary of each player and a plot of their ratings over time.

## FAQ
1. **Why is the search limited to 8 players?**

The search is limited to 8 players to help ensure a responsible use of the PDGA website's resources. Each player search involves sending a request to the PDGA site to retrieve and display up-to-date player data. By limiting the number of players that can be searched at once, we reduce the number of simultaneous requests sent to the PDGA site, thereby minimizing server load and ensuring that the service remains fast and reliable for all users. This limit helps us maintain good performance and avoid potential issues related to excessive traffic or server overloading.

2. **Is this project affiliated with the PDGA?**

No, this project is not affiliated with the PDGA. The data is responsibly pulled from the PDGA website, specifically the player history pages, to provide up-to-date and accurate comparisons based on the PDGA numbers provided in the search bar. This tool is only meant to be used as a data visualizer tool and does not store PDGA data about players. We do not sell or distribute any player data.

## Contributing
We welcome contributions! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## Support
If you enjoy using Rating Rivals, consider leaving a tip by <a href="https://buymeacoffee.com/chadwoodard" target="_blank">buying me a coffee</a>. Enjoy!