# import streamlit as st
# import mysql.connector
# from datetime import datetime

# # Database connection
# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     passwd="1234",
#     database="cinema"
# )
# mycursor = mydb.cursor()

# # Set page configuration
# st.set_page_config(page_title="Movie Booking System", layout="wide")

# # Sidebar for navigation
# st.sidebar.title("Navigation")
# page = st.sidebar.radio("Go to", ["Login", "Register", "Movies", "Theatre", "Seats", "Payment"])

# # Session state to store customer ID
# if "custId" not in st.session_state:
#     st.session_state.custId = None

# # Login page
# if page == "Login" and st.session_state.custId is None:
#     st.title("Login")
#     try:
#         st.image("movie_ticket_booking_poster.png", use_column_width=True)
#     except FileNotFoundError:
#         st.warning("movie_ticket_booking_poster.png not found!")
#         st.image("https://via.placeholder.com/900x600", use_column_width=True)  # Fallback image
#     email = st.text_input("Email Id")
#     password = st.text_input("Password", type="password")
#     if st.button("LOGIN"):
#         mycursor.execute('''SELECT CASE WHEN (%s IN (SELECT DISTINCT email FROM customer) AND 
#                                     %s IN (SELECT DISTINCT password FROM customer)) THEN 1 ELSE 0 END AS val''',
#                         (email, password))
#         sql_qry = mycursor.fetchone()
#         if sql_qry[0] == 0:
#             st.error("Invalid Credentials! Please Try Again...")
#         else:
#             mycursor.execute('''SELECT ID FROM customer WHERE email=%s AND password=%s''', (email, password))
#             st.session_state.custId = mycursor.fetchall()[0][0]
#             st.success("Logged in successfully!")
#             st.rerun()

#     if st.button("Go to Register"):
#         st.rerun()

# # Register page
# elif page == "Register" and st.session_state.custId is None:
#     st.title("Register")
#     try:
#         st.image("movie_ticket_booking_poster.png", use_column_width=True)
#     except FileNotFoundError:
#         st.warning("movie_ticket_booking_poster.png not found!")
#         st.image("https://via.placeholder.com/900x600", use_column_width=True)  # Fallback image
#     username = st.text_input("Create Username")
#     email = st.text_input("Email Address")
#     password = st.text_input("Set Password", type="password")
#     if st.button("REGISTER"):
#         mycursor.execute('''SELECT CASE WHEN EXISTS(SELECT email FROM customer WHERE email=%s) THEN 0 ELSE 1 END AS val''', (email,))
#         sql_query = mycursor.fetchall()[0][0]
#         if sql_query == 0:
#             st.error("Email already in use, please use another")
#         else:
#             mycursor.execute("INSERT INTO customer(name, email, password) VALUES (%s, %s, %s)", (username, email, password))
#             mydb.commit()
#             mycursor.execute('''SELECT MAX(ID) FROM customer''')
#             st.session_state.custId = mycursor.fetchall()[0][0]
#             st.success("Registered successfully! Please log in.")
#             st.rerun()

# # Movies page (placeholder)
# elif page == "Movies" and st.session_state.custId:
#     st.title("Select Movie")
#     try:
#         st.image("popcornandstuff.jpeg", use_column_width=True)
#     except FileNotFoundError:
#         st.warning("popcornandstuff.jpeg not found!")
#         st.image("https://via.placeholder.com/900x600", use_column_width=True)  # Fallback image
#     mycursor.execute('SELECT ID, name FROM movie')
#     movies = mycursor.fetchall()
#     movie_options = {str(movie[1]): movie[0] for movie in movies}
#     selected_movie = st.selectbox("Choose a movie", options=list(movie_options.keys()))
#     if st.button("Select"):
#         st.session_state.movie_id = movie_options[selected_movie]
#         st.rerun()

# # Theatre page (placeholder)
# elif page == "Theatre" and st.session_state.custId and "movie_id" in st.session_state:
#     st.title("Theatre Booking")
#     try:
#         st.image(f"{st.session_state.movie_id}.jpg", use_column_width=True)
#     except FileNotFoundError:
#         st.warning(f"{st.session_state.movie_id}.jpg not found!")
#         st.image("https://via.placeholder.com/900x600", use_column_width=True)  # Fallback image
#     mycursor.execute('''SELECT s.ID, t.name, start_time, show_date, hall_ID
#                        FROM shows s, theatre t
#                        WHERE s.movie_ID=%s AND s.theatre_ID=t.ID
#                        ORDER BY show_date, start_time''', (st.session_state.movie_id,))
#     shows = mycursor.fetchall()
#     show_options = {f"{row[1]} - {row[2]} - {row[3]} (Hall {row[4]})": row[0] for row in shows}
#     selected_show = st.selectbox("Choose a show", options=list(show_options.keys()))
#     if st.button("Proceed"):
#         st.session_state.show_id = show_options[selected_show]
#         st.rerun()

# # Seats page (placeholder)
# elif page == "Seats" and st.session_state.custId and "show_id" in st.session_state:
#     st.title("Seat Booking")
#     try:
#         st.image("popcornandstuff.jpeg", use_column_width=True)
#     except FileNotFoundError:
#         st.warning("popcornandstuff.jpeg not found!")
#         st.image("https://via.placeholder.com/900x600", use_column_width=True)  # Fallback image
#     show_id = st.session_state.show_id
#     mycursor.execute('''SELECT hall_ID, theatre_ID FROM shows WHERE ID=%s''', (show_id,))
#     info = mycursor.fetchall()
#     h_id, t_id = info[0]
#     mycursor.execute('''SELECT capacity FROM hall WHERE ID=%s AND theatre_ID=%s''', (h_id, t_id))
#     capacity = mycursor.fetchall()[0][0]
#     mycursor.execute('''SELECT seat_ID FROM books WHERE show_ID=%s''', (show_id,))
#     booked = [row[0] for row in mycursor.fetchall()]
#     mycursor.execute('''SELECT seat_ID FROM seatinline WHERE show_ID=%s AND book_date=CURDATE()
#                        AND (CAST(CURTIME() AS TIME) - CAST(book_time AS TIME)) <= 1000''', (show_id,))
#     booked.extend(row[0] for row in mycursor.fetchall())
#     seats = [i + 1 for i in range(capacity) if i + 1 not in booked]
#     selected_seats = st.multiselect("Select Seats", options=seats)
#     if st.button("Proceed"):
#         if selected_seats:
#             st.session_state.selected_seats = selected_seats
#             st.rerun()
#         else:
#             st.error("Please select at least one seat")

# # Payment page (placeholder)
# elif page == "Payment" and st.session_state.custId and "selected_seats" in st.session_state:
#     st.title("Payment")
#     try:
#         st.image("popcornandstuff.jpeg", use_column_width=True)
#     except FileNotFoundError:
#         st.warning("popcornandstuff.jpeg not found!")
#         st.image("https://via.placeholder.com/900x600", use_column_width=True)  # Fallback image
#     show_id = st.session_state.show_id
#     new_booked = st.session_state.selected_seats
#     mycursor.execute('''SELECT * FROM shows WHERE ID=%s''', (show_id,))
#     show_info = mycursor.fetchall()
#     mycursor.execute('''SELECT name FROM movie WHERE ID=%s''', (show_info[0][1],))
#     movie_name = mycursor.fetchall()[0][0]
#     mycursor.execute('''SELECT name FROM theatre WHERE ID=%s''', (show_info[0][3],))
#     theatre_name = mycursor.fetchall()[0][0]
#     fl_amt = int(show_info[0][7]) * len(new_booked)
#     st.write(f"Movie: {movie_name}")
#     st.write(f"Hall: {show_info[0][2]}")
#     st.write(f"Theatre: {theatre_name}")
#     st.write(f"Start Time: {show_info[0][4]}")
#     st.write(f"End Time: {show_info[0][5]}")
#     st.write(f"Date: {show_info[0][6]}")
#     st.write(f"Price: {fl_amt}")
#     st.write(f"Seat numbers: {' '.join(map(str, new_booked))}")
#     if st.button("Pay"):
#         for i in new_booked:
#             mycursor.execute('''INSERT INTO seatinline(seat_ID, show_ID, book_time, book_date) VALUES
#                               (%s, %s, CURTIME(), CURDATE())''', (i, show_id))
#         mydb.commit()
#         mycursor.execute('''INSERT INTO payment(amt, pay_time, pay_date) VALUES (%s, CURTIME(), CURDATE())''', (fl_amt,))
#         mydb.commit()
#         mycursor.execute('''SELECT MAX(ID) FROM payment''')
#         pay_id = mycursor.fetchall()[0][0]
#         for i in new_booked:
#             mycursor.execute('''INSERT INTO books VALUES (%s, %s, %s, %s)''', (st.session_state.custId, i, show_id, pay_id))
#         mydb.commit()
#         for i in new_booked:
#             mycursor.execute('''DELETE FROM seatinline WHERE seat_ID=%s AND show_ID=%s''', (i, show_id))
#         mydb.commit()
#         st.success("Payment successful!")
#         st.session_state.custId = None  # Log out after payment
#         st.rerun()

# # Run the app
# if __name__ == "__main__":
#     if st.session_state.custId:
#         st.sidebar.write(f"Welcome, User ID: {st.session_state.custId}")
#     st.stop()


import streamlit as st
import mysql.connector

# Database connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1234",
    database="cinema"
)
mycursor = mydb.cursor()

# Set page configuration
st.set_page_config(page_title="Movie Booking System", layout="wide")

# Session state to store customer ID and username
if "custId" not in st.session_state:
    st.session_state.custId = None
if "username" not in st.session_state:
    st.session_state.username = None

# Custom CSS for background image
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('movie_ticket_booking_poster.png');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .stCard {
        background-color: rgba(0, 0, 0, 0.7); /* Semi-transparent black overlay */
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Main content with tabs for Login and Register
st.title("Movie Booking System")

# Create a card-like container for the form
with st.container():
    st.markdown('<div class="stCard">', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    # Login tab
    with tab1:
        st.subheader("Login")
        email = st.text_input("Email Id")
        password = st.text_input("Password", type="password")
        if st.button("LOGIN"):
            mycursor.execute('''SELECT CASE WHEN (%s IN (SELECT DISTINCT email FROM customer) AND 
                                        %s IN (SELECT DISTINCT password FROM customer)) THEN 1 ELSE 0 END AS val''',
                            (email, password))
            sql_qry = mycursor.fetchone()
            if sql_qry[0] == 0:
                st.error("Invalid Credentials! Please Try Again...")
            else:
                mycursor.execute('''SELECT ID, name FROM customer WHERE email=%s AND password=%s''', (email, password))
                result = mycursor.fetchall()[0]
                st.session_state.custId = result[0]
                st.session_state.username = result[1]  # Store the username
                st.success("Logged in successfully!")
                st.rerun()

    # Register tab
    with tab2:
        st.subheader("Sign Up")
        username = st.text_input("Create Username")
        email = st.text_input("Email Address")
        password = st.text_input("Set Password", type="password")
        if st.button("REGISTER"):
            mycursor.execute('''SELECT CASE WHEN EXISTS(SELECT email FROM customer WHERE email=%s) THEN 0 ELSE 1 END AS val''', (email,))
            sql_query = mycursor.fetchall()[0][0]
            if sql_query == 0:
                st.error("Email already in use, please use another")
            else:
                mycursor.execute("INSERT INTO customer(name, email, password) VALUES (%s, %s, %s)", (username, email, password))
                mydb.commit()
                mycursor.execute('''SELECT MAX(ID), name FROM customer''')
                result = mycursor.fetchall()[0]
                st.session_state.custId = result[0]
                st.session_state.username = result[1]  # Store the username
                st.success("Registered successfully! Please log in.")
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# Conditional navigation for authenticated users
if st.session_state.custId:
    st.sidebar.title("Navigation")
    st.sidebar.write(f"Welcome, {st.session_state.username}")  # Display username once
    page = st.sidebar.radio("Go to", ["Movies", "Theatre", "Seats", "Payment", "Logout"])
    
    # Movies page
    if page == "Movies":
        st.title("Select Movie")
        try:
            st.image("popcornandstuff.jpg", use_container_width=True)  # Updated to use_container_width
        except FileNotFoundError:
            st.warning("popcornandstuff.jpg not found!")
            st.image("https://via.placeholder.com/900x600", use_container_width=True)  # Fallback image
        mycursor.execute('SELECT ID, name FROM movie')
        movies = mycursor.fetchall()
        movie_options = {str(movie[1]): movie[0] for movie in movies}
        selected_movie = st.selectbox("Choose a movie", options=list(movie_options.keys()))
        if st.button("Select"):
            st.session_state.movie_id = movie_options[selected_movie]
            st.rerun()

    # Theatre page
    elif page == "Theatre" and "movie_id" in st.session_state:
        st.title("Theatre Booking")
        try:
            st.image(f"{st.session_state.movie_id}.jpg", use_container_width=True)  # Updated to use_container_width
        except FileNotFoundError:
            st.warning(f"{st.session_state.movie_id}.jpg not found!")
            st.image("https://via.placeholder.com/900x600", use_container_width=True)  # Fallback image
        mycursor.execute('''SELECT s.ID, t.name, start_time, show_date, hall_ID
                           FROM shows s, theatre t
                           WHERE s.movie_ID=%s AND s.theatre_ID=t.ID
                           ORDER BY show_date, start_time''', (st.session_state.movie_id,))
        shows = mycursor.fetchall()
        show_options = {f"{row[1]} - {row[2]} - {row[3]} (Hall {row[4]})": row[0] for row in shows}
        selected_show = st.selectbox("Choose a show", options=list(show_options.keys()))
        if st.button("Proceed"):
            st.session_state.show_id = show_options[selected_show]
            st.rerun()

    # Seats page
    elif page == "Seats" and "show_id" in st.session_state:
        st.title("Seat Booking")
        try:
            st.image("popcornandstuff.jpg", use_container_width=True)  # Updated to use_container_width
        except FileNotFoundError:
            st.warning("popcornandstuff.jpg not found!")
            st.image("https://via.placeholder.com/900x600", use_container_width=True)  # Fallback image
        show_id = st.session_state.show_id
        mycursor.execute('''SELECT hall_ID, theatre_ID FROM shows WHERE ID=%s''', (show_id,))
        info = mycursor.fetchall()
        h_id, t_id = info[0]
        mycursor.execute('''SELECT capacity FROM hall WHERE ID=%s AND theatre_ID=%s''', (h_id, t_id))
        capacity = mycursor.fetchall()[0][0]
        mycursor.execute('''SELECT seat_ID FROM books WHERE show_ID=%s''', (show_id,))
        booked = [row[0] for row in mycursor.fetchall()]
        mycursor.execute('''SELECT seat_ID FROM seatinline WHERE show_ID=%s AND book_date=CURDATE()
                           AND (CAST(CURTIME() AS TIME) - CAST(book_time AS TIME)) <= 1000''', (show_id,))
        booked.extend(row[0] for row in mycursor.fetchall())
        seats = [i + 1 for i in range(capacity) if i + 1 not in booked]
        selected_seats = st.multiselect("Select Seats", options=seats)
        if st.button("Proceed"):
            if selected_seats:
                st.session_state.selected_seats = selected_seats
                st.rerun()
            else:
                st.error("Please select at least one seat")

    # Payment page
    elif page == "Payment" and "selected_seats" in st.session_state:
        st.title("Payment")
        try:
            st.image("popcornandstuff.jpg", use_container_width=True)  # Updated to use_container_width
        except FileNotFoundError:
            st.warning("popcornandstuff.jpg not found!")
            st.image("https://via.placeholder.com/900x600", use_container_width=True)  # Fallback image
        show_id = st.session_state.show_id
        new_booked = st.session_state.selected_seats
        mycursor.execute('''SELECT * FROM shows WHERE ID=%s''', (show_id,))
        show_info = mycursor.fetchall()
        mycursor.execute('''SELECT name FROM movie WHERE ID=%s''', (show_info[0][1],))
        movie_name = mycursor.fetchall()[0][0]
        mycursor.execute('''SELECT name FROM theatre WHERE ID=%s''', (show_info[0][3],))
        theatre_name = mycursor.fetchall()[0][0]
        fl_amt = int(show_info[0][7]) * len(new_booked)
        st.write(f"Movie: {movie_name}")
        st.write(f"Hall: {show_info[0][2]}")
        st.write(f"Theatre: {theatre_name}")
        st.write(f"Start Time: {show_info[0][4]}")
        st.write(f"End Time: {show_info[0][5]}")
        st.write(f"Date: {show_info[0][6]}")
        st.write(f"Price: {fl_amt}")
        st.write(f"Seat numbers: {' '.join(map(str, new_booked))}")
        if st.button("Pay"):
            for i in new_booked:
                mycursor.execute('''INSERT INTO seatinline(seat_ID, show_ID, book_time, book_date) VALUES
                                  (%s, %s, CURTIME(), CURDATE())''', (i, show_id))
            mydb.commit()
            mycursor.execute('''INSERT INTO payment(amt, pay_time, pay_date) VALUES (%s, CURTIME(), CURDATE())''', (fl_amt,))
            mydb.commit()
            mycursor.execute('''SELECT MAX(ID) FROM payment''')
            pay_id = mycursor.fetchall()[0][0]
            for i in new_booked:
                mycursor.execute('''INSERT INTO books VALUES (%s, %s, %s, %s)''', (st.session_state.custId, i, show_id, pay_id))
            mydb.commit()
            for i in new_booked:
                mycursor.execute('''DELETE FROM seatinline WHERE seat_ID=%s AND show_ID=%s''', (i, show_id))
            mydb.commit()
            st.success("Payment successful!")
            st.session_state.custId = None
            st.session_state.username = None
            st.rerun()

    # Logout
    elif page == "Logout":
        st.session_state.custId = None
        st.session_state.username = None
        st.success("Logged out successfully!")
        st.rerun()

# Run the app
if __name__ == "__main__":
    if st.session_state.custId:
        st.sidebar.write(f"Welcome, {st.session_state.username}")  # Fallback display
    st.stop()