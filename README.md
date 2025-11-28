📚 Personalized Book Recommendation System

This project is a data science application that provides personalized book recommendations. It uses a combination of popularity-based filtering and collaborative filtering techniques to suggest the top 5 most similar and highly-rated books based on a user-inputted title.

The entire application is deployed as an interactive web page using Streamlit.

✨ Features

Book Search: Users can input the name of a book they have read or enjoyed.

Top 5 Recommendations: The system returns a list of 5 highly-rated books that are most similar to the search query.

Detailed Information: Each recommendation includes the book title, author, and an associated cover image (if available in the dataset).

Interactive UI: A user-friendly web interface built with Streamlit for seamless interaction.

🛠️ Tech Stack

Component

Technology

Role

Data Processing

Python, Pandas, NumPy

Data cleaning, merging, and feature engineering.

Model Building

Scikit-learn (e.g., cosine_similarity)

Calculating book similarity scores.

Web Interface

Streamlit

Creating the interactive front-end application.

Serialization

Pickle

Saving the processed data and similarity matrix for quick loading.

🚀 Getting Started

Follow these steps to set up and run the Book Recommendation System locally.

Prerequisites

You will need Python 3.x installed on your machine.


Install Dependencies

Create a virtual environment (recommended) and install the necessary libraries.

# Create environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install Python packages
pip install pandas numpy scikit-learn streamlit


Data & Model Files

This project relies on pre-processed data and the similarity matrix generated in the Google Colab notebook.

popular.pkl: Contains a DataFrame of the top 50 most popular and highly-rated books (based on initial analysis in Colab).

pt.pkl: The pivot table used for similarity calculation.

books.pkl: The master book data frame (including image URLs).

similarity_scores.pkl: The matrix containing the cosine similarity scores between books.

Ensure these files (or the code to generate them) are present in your project directory.

💻 Project Structure

The core functionality of the project is split into two main parts:

Data Preprocessing and Model Training

The book_recommender.ipynb (Google Colab file) handles all the heavy lifting:

Loading Books.csv, Ratings.csv, and Users.csv.

Filtering users with sufficient ratings and books with sufficient votes to remove noise.

Creating the Popularity-Based Recommender by aggregating ratings and calculating the mean rating for the top books.

Building the pivot table (pt) and calculating the Cosine Similarity matrix for the Collaborative Filtering approach.

Dumping the essential objects (popular_df, pt, books, similarity_scores) using pickle.

Streamlit Web Application

The main Streamlit file (e.g., app.py or main.py) loads the pickled files and implements the recommendation logic into an interactive web interface.

Running the Streamlit App

Execute the Streamlit command from your project root directory:

streamlit run app.py  # or the name of your Streamlit file


The application will open in your default web browser (usually at http://localhost:8501).

🤝 Contribution

Feel free to open issues or submit pull requests to improve the system, add more filtering techniques, or enhance the UI!
