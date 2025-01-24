import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.properties import DictProperty, StringProperty
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
import requests
import sqlite3
from sql import create_db # type: ignore

# Main screen of the app
class MainScreen(Screen):
    pass


# Function to fetch all currencies from the SQLite database
def fetch_all_currencies():
    conn = sqlite3.connect('currencies.db')
    cursor = conn.cursor()

    cursor.execute("SELECT code, name FROM currencies")
    currencies = cursor.fetchall()

    conn.close()

    return {code: name for code, name in currencies}


class FromCurrencyScreen(Screen):
    def on_enter(self):
        """Populate the grid with currency buttons when the screen is shown."""
        grid = self.ids.from_currency_grid
        grid.clear_widgets()  # Clear any existing widgets

        # Add a search bar to the top of the screen
        search_bar = TextInput(
            hint_text="Search currencies",
            size_hint_y=None,
            height=40,
            multiline=False,
            on_text_validate=self.filter_currencies,
            background_color=(1, 1, 1, 1),  # White background for search bar
            foreground_color=(0, 0, 0, 1),  # Black text color for search bar
        )
        grid.add_widget(search_bar)

        self.populate_currency_buttons(grid)

    def populate_currency_buttons(self, grid):
        """Populate the grid with currency buttons."""
        for code, name in App.get_running_app().currencies.items():
            button = Button(
                text=f"{code} - {name}",
                size_hint_y=None,
                height=50,
                background_normal="",  # Disable default background
                background_color=(0.1, 0.67, 0.13, 1),  # #1AAD21 (greenish)
                color=(1, 1, 1, 1),  # White text color
                on_release=lambda btn, c=code: App.get_running_app().set_currency("from", c),
            )
            grid.add_widget(button)

    def filter_currencies(self, instance):
        """Filter the currencies based on the search input."""
        grid = self.ids.from_currency_grid  # This will be the from currency grid, adjust as needed
        query = instance.text.lower()
        grid.clear_widgets()  # Clear the existing buttons

        # Add the search bar again to keep it visible
        search_bar = TextInput(
            hint_text="Search currencies",
            size_hint_y=None,
            height=40,
            multiline=False,
            on_text_validate=self.filter_currencies,
            background_color=(1, 1, 1, 1),  # White background for search bar
            foreground_color=(0, 0, 0, 1),  # Black text color for search bar
        )
        grid.add_widget(search_bar)

        # Now add the filtered currency buttons
        for code, name in App.get_running_app().currencies.items():
            if query in name.lower() or query in code.lower():
                # Only add buttons that match the query
                button = Button(
                    text=f"{code} - {name}",
                    size_hint_y=None,
                    height=50,
                    background_normal="",  # Disable default background
                    background_color=(0.1, 0.67, 0.13, 1),  # #1AAD21 (greenish)
                    color=(1, 1, 1, 1),  # White text color
                    on_release=lambda btn, c=code: App.get_running_app().set_currency("from", c),
                )
                grid.add_widget(button)


class ToCurrencyScreen(Screen):
    def on_enter(self):
        """Populate the grid with currency buttons when the screen is shown."""
        grid = self.ids.to_currency_grid
        grid.clear_widgets()  # Clear any existing widgets

        # Add a search bar to the top of the screen
        search_bar = TextInput(
            hint_text="Search currencies",
            size_hint_y=None,
            height=40,
            multiline=False,
            on_text_validate=self.filter_currencies,
            background_color=(1, 1, 1, 1),  # White background for search bar
            foreground_color=(0, 0, 0, 1),  # Black text color for search bar
        )
        grid.add_widget(search_bar)

        self.populate_currency_buttons(grid)

    def populate_currency_buttons(self, grid):
        """Populate the grid with currency buttons."""
        for code, name in App.get_running_app().currencies.items():
            button = Button(
                text=f"{code} - {name}",
                size_hint_y=None,
                height=50,
                background_normal="",  # Disable default background
                background_color=(0.1, 0.67, 0.13, 1),  # #1AAD21 (greenish)
                color=(1, 1, 1, 1),  # White text color
                on_release=lambda btn, c=code: App.get_running_app().set_currency("to", c),
            )
            grid.add_widget(button)

    def filter_currencies(self, instance):
        """Filter the currencies based on the search input."""
        grid = self.ids.to_currency_grid  # This will be the to currency grid, adjust as needed
        query = instance.text.lower()
        grid.clear_widgets()  # Clear the existing buttons

        # Add the search bar again to keep it visible
        search_bar = TextInput(
            hint_text="Search currencies",
            size_hint_y=None,
            height=40,
            multiline=False,
            on_text_validate=self.filter_currencies,
            background_color=(1, 1, 1, 1),  # White background for search bar
            foreground_color=(0, 0, 0, 1),  # Black text color for search bar
        )
        grid.add_widget(search_bar)

        # Now add the filtered currency buttons
        for code, name in App.get_running_app().currencies.items():
            if query in name.lower() or query in code.lower():
                # Only add buttons that match the query
                button = Button(
                    text=f"{code} - {name}",
                    size_hint_y=None,
                    height=50,
                    background_normal="",  # Disable default background
                    background_color=(0.1, 0.67, 0.13, 1),  # #1AAD21 (greenish)
                    color=(1, 1, 1, 1),  # White text color
                    on_release=lambda btn, c=code: App.get_running_app().set_currency("to", c),
                )
                grid.add_widget(button)




class MyApp(App):
    currencies = DictProperty({})  # Dictionary to store currency codes and their names
    from_currency = StringProperty("USD")  # Default "From" currency
    to_currency = StringProperty("EUR")  # Default "To" currency

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(FromCurrencyScreen(name="from_currency"))
        sm.add_widget(ToCurrencyScreen(name="to_currency"))
        return sm

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.from_label_value = ""  # Initialize the input value
        self.load_currencies()  # Fetch the currency list from the database at startup

    def load_currencies(self):
        """Fetch the list of currencies from the SQLite database."""
        self.currencies = fetch_all_currencies()

    def set_currency(self, currency_type, code):
        """Set the selected currency."""
        if currency_type == "from":
            self.from_currency = code
        elif currency_type == "to":
            self.to_currency = code
        self.root.current = "main"  # Go back to the main screen

    def update_label(self, label_id, value):
        label = self.root.get_screen("main").ids.get(label_id)
        if label:
            # Remove commas from the label text before converting to an integer
            current_value = label.text.replace(",", "")
            
            # If the label text is "0", reset the value, otherwise append the new value
            if current_value == "0":
                label.text = value
            else:
                # Append the new value and format with commas
                label.text += value

            # Format the text to have commas for thousands separators
            label.text = f"{int(label.text.replace(',', '') or 0):,}"


    def remove_last_digit(self, label_id):
        label = self.root.get_screen("main").ids.get(label_id)
        if label:
            # Remove commas before processing the number
            current_value = label.text.replace(",", "")
            
            print(f"Current value before removing last digit: {current_value}")  # Add debug
            
            if len(current_value) > 1:
                # Remove the last digit
                current_value = current_value[:-1]
            else:
                # If only one digit is left, reset it to "0"
                current_value = "0"
            
            print(f"Updated value after removing last digit: {current_value}")  # Add debug
            
            # Update the label with the new value and format with commas
            label.text = f"{int(current_value):,}"
            self.from_label_value = label.text  # Update the stored value

            print(f"from_label_value after removing digit: '{self.from_label_value}'")  # Add debug


    def exchange(self):
        """Fetch the conversion rate and update the result label."""
        label = self.root.get_screen("main").ids.get("from_label")
        self.from_label_value = label.text
        
        raw_input_value = self.from_label_value.strip()
        
        # If the input is empty, print an error and exit
        if not raw_input_value:
            print("Invalid input: empty value")
            self.update_to_label("Invalid input")
            return

        # Remove commas after checking for the empty string
        raw_input_value = raw_input_value.replace(",", "")
        
        try:
            # Check if the cleaned input is a valid number (allowing decimal points)
            value = float(raw_input_value)
            print(f"Input value as float: {value}")

        except ValueError:
            # If the value is not a valid number, print and show error
            print(f"Invalid input value: {raw_input_value}")
            self.update_to_label("Invalid input")
            return

        try:
            # API call to fetch the conversion rates
            url = f"https://v6.exchangerate-api.com/v6/00a812453d987aa4b6f56d7f/latest/{self.from_currency}"
            response = requests.get(url)
            response.raise_for_status()  # Will raise an error for bad responses (non-200 status)
            
            data = response.json()  # Convert response to JSON
            
            if data.get("result") == "success":
                rate = data["conversion_rates"].get(self.to_currency)
                
                # Check if conversion rate is found
                if rate is not None:
                    # Convert the raw input value (without commas) to a float and apply the rate
                    converted_value = value * rate
                    
                    # Format the converted value with commas (while keeping the decimal part)
                    self.update_to_label(f"{converted_value:,.2f}")
                else:
                    print("Error: Conversion rate not found")
                    self.update_to_label("Rate not found")
            else:
                print("API Error:", data.get("error-type", "Unknown error"))
                self.update_to_label("API Error")
        
        except requests.RequestException as e:
            print(f"Request Error: {e}")
            self.update_to_label("Request Error")
        
        except Exception as e:
            print(f"Unexpected error: {e}")
            self.update_to_label("Unexpected error")



    def update_to_label(self, message):
        """Update the 'To' label on the main screen with a formatted value or error message."""
        to_label = self.root.get_screen("main").ids.get("to_label")
        if to_label:
            to_label.text = message




    def clear_label(self, label_id):
        """Clear the label."""
        label = self.root.get_screen("main").ids.get(label_id)
        if label:
            label.text = "0"
            self.from_label_value = ""  # Clear stored value



if __name__ == '__main__':
    create_db()  # Ensure the database is created
    MyApp().run()
