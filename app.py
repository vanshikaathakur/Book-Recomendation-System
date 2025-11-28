import streamlit as st
import pickle
import numpy as np

# --- 1. Data Loading and Caching ---
# @st.cache_data ensures these large files are loaded into memory only once, 
# making the app much faster on subsequent runs and interactions.
@st.cache_data
def load_data():
    try:
        # NOTE: Ensure all these .pkl files are in the same directory as this streamlit_app.py file.
        popular_df = pickle.load(open('popular.pkl', 'rb'))
        pt = pickle.load(open('pt.pkl', 'rb'))
        books = pickle.load(open('books.pkl', 'rb'))
        similarity_scores = pickle.load(open('similarity_score.pkl', 'rb'))
        return popular_df, pt, books, similarity_scores
    except FileNotFoundError as e:
        st.error(f"Data file not found: {e.filename}. Please ensure all .pkl files are in the same directory.")
        return None, None, None, None

popular_df, pt, books, similarity_scores = load_data()

# Exit if data loading failed
if popular_df is None:
    st.stop()


# --- 2. Recommendation Logic (Reused from Flask) ---
def recommend(book_name, pt_df, similarity_matrix, book_data):
    """Calculates top 5 similar books based on the input book name."""
    
    # Check if the book exists in the pivot table index
    if book_name not in pt_df.index:
        return []
    
    # Find the index of the input book
    index = np.where(pt_df.index == book_name)[0][0]
    
    # Get 5 similar items (skipping the book itself at index 0)
    similar_items = sorted(list(enumerate(similarity_matrix[index])), key=lambda x: x[1], reverse=True)[1:6]
    
    data = []
    for i in similar_items:
        # Get the recommended book title
        recommended_book_title = pt_df.index[i[0]]
        
        # Retrieve book details
        temp_df = book_data[book_data['Book-Title'] == recommended_book_title].drop_duplicates('Book-Title')
        
        item = {}
        item['Title'] = list(temp_df['Book-Title'].values)[0]
        item['Author'] = list(temp_df['Book-Author'].values)[0]
        item['Image'] = list(temp_df['Image-URL-S'].values)[0]
        data.append(item)
        
    return data


# --- 3. Streamlit UI Design ---

st.set_page_config(layout="wide")

st.title('📚 Book Recommender System')
st.markdown("---")


# --- RECOMMENDATION SECTION ---
st.header("Find Your Next Read")

# Get a list of all unique book titles for the selectbox
all_book_titles = list(pt.index)
selected_book = st.selectbox(
    'Type or select a book title:',
    all_book_titles
)

if st.button('Show Recommendations'):
    st.markdown("---")
    
    # Get recommendations
    recommendation_results = recommend(selected_book, pt, similarity_scores, books)
    
    if recommendation_results:
        st.subheader(f"Recommended Books for: **{selected_book}**")
        
        # Create 5 columns for displaying 5 books
        cols = st.columns(len(recommendation_results))
        
        for i, book_data in enumerate(recommendation_results):
            with cols[i]:
                st.image(
                    book_data['Image'],
                    caption=book_data['Title'],
                    width=150
                )
                st.markdown(f"**{book_data['Title']}**")
                st.write(f"Author: {book_data['Author']}")
    else:
        st.warning(f"Could not find recommendations for '{selected_book}'. Try another book.")


st.markdown("---")

# --- TOP 50 BOOKS SECTION ---
st.header("Top 50 Popular Books")

# Create 5 columns for the Top 50 display (5 books per row)
num_books_to_show = 50
books_per_row = 5
num_rows = num_books_to_show // books_per_row

for row in range(num_rows):
    start_index = row * books_per_row
    end_index = start_index + books_per_row
    
    # Get the books for the current row
    row_books = popular_df.iloc[start_index:end_index]
    
    # Create a column layout for the row
    cols = st.columns(books_per_row)
    
    for i, col in enumerate(cols):
        # Get the actual index in the popular_df
        df_index = start_index + i
        
        with col:
            # Display image
            col.image(
                row_books.iloc[i]['Image-URL-S'],
                caption=row_books.iloc[i]['Book-Title'],
                width=120
            )
            # Display text details
            col.markdown(f"**{row_books.iloc[i]['Book-Title']}**")
            col.caption(f"Author: {row_books.iloc[i]['Book-Author']}")
            col.write(f"Avg Rating: **{round(row_books.iloc[i]['avg_ratings'], 2)}**")
            col.write(f"Votes: {int(row_books.iloc[i]['num_ratings'])}")