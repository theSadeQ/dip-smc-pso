"""
hello_world.py - Your First Python Program

This script demonstrates basic Python concepts:
- Variables and data types
- String formatting
- Functions
- Control flow

Run: python hello_world.py
"""


def greet(name, language="English"):
    """
    Greet someone in different languages.

    Args:
        name: Person's name
        language: Language for greeting (default: English)

    Returns:
        Greeting string
    """
    greetings = {
        "English": "Hello",
        "Spanish": "Hola",
        "French": "Bonjour",
        "German": "Guten Tag",
    }

    greeting = greetings.get(language, "Hello")
    return f"{greeting}, {name}!"


def calculate_age_in_days(age_years):
    """Calculate approximate age in days."""
    days_per_year = 365.25  # Account for leap years
    return int(age_years * days_per_year)


def main():
    """Main entry point."""
    print("=" * 50)
    print("Welcome to Python!")
    print("=" * 50)

    # Variables
    name = "Alice"
    age = 25
    is_student = True

    # String formatting
    print(f"\nName: {name}")
    print(f"Age: {age} years")
    print(f"Student: {is_student}")

    # Function calls
    print(f"\n{greet(name)}")
    print(f"{greet(name, 'Spanish')}")
    print(f"{greet(name, 'French')}")

    # Calculations
    days = calculate_age_in_days(age)
    print(f"\n{name} has lived approximately {days:,} days!")

    # Control flow
    print("\n" + "-" * 50)
    print("Age category:")
    if age < 18:
        category = "Minor"
    elif age < 65:
        category = "Adult"
    else:
        category = "Senior"
    print(f"{name} is an {category}")

    # Lists and loops
    print("\n" + "-" * 50)
    print("Languages I can greet in:")
    languages = ["English", "Spanish", "French", "German"]
    for i, lang in enumerate(languages, 1):
        print(f"  {i}. {lang}: {greet(name, lang)}")

    print("\n" + "=" * 50)
    print("Program complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
