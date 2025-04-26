# streamlit app
import streamlit as st
import mysql.connector
from datetime import datetime

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

# Helper function to display images with reliable fallback
def display_image(image_path):
    """Display image with built-in fallback to placeholder"""
    try:
        st.image(image_path, use_container_width=True)
    except Exception:
        # Create a movie-themed placeholder with emojis and markdown
        st.markdown("""
        <div style="background: linear-gradient(45deg, #2c3e50, #4a69bd); padding: 20px; border-radius: 10px; text-align: center; color: white;">
            <h2>🎬 Movie Magic 🍿</h2>
            <p style="font-size: 18px;"></p>
            <p style="font-size: 36px;">🎥 🎞️ 🎭 🎪</p>
        </div>
        """, unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Login/Register", "Movies", "Theatre", "Seats", "Payment"])

# Session state to store customer ID
if "custId" not in st.session_state:
    st.session_state.custId = None

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 42px;
        font-weight: bold;
        color: #1e3799;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    .sub-header {
        font-size: 30px;
        font-weight: bold;
        color: #0c2461;
        margin-bottom: 10px;
    }
    .info-text {
        font-size: 18px;
        margin-bottom: 5px;
    }
    .success-message {
        padding: 10px;
        background-color: #d4edda;
        color: #155724;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .error-message {
        padding: 10px;
        background-color: #f8d7da;
        color: #721c24;
        border-radius: 5px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Single Login/Register page logic
if page == "Login/Register":
    if st.session_state.custId is None:
        # Display login or registration based on user selection
        login_or_register = st.radio("Choose an option", ["Login", "Register"])
        
        if login_or_register == "Login":
            st.markdown("<h1 class='main-header'>Cinema Booking - Login</h1>", unsafe_allow_html=True)
            display_image("movie_ticket_booking_poster.png")

            with st.container():
                st.markdown("<h2 class='sub-header'>Sign In</h2>", unsafe_allow_html=True)
                email = st.text_input("Email Id")
                password = st.text_input("Password", type="password")
                col1, col2 = st.columns([1,1])
                with col1:
                    if st.button("LOGIN", use_container_width=True):
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
                            st.session_state.username = result[1]  # Store username
                            st.success(f"Welcome back, {result[1]}!")
                            st.rerun()
                with col2:
                    if st.button("Go to Register", use_container_width=True):
                        login_or_register = "Register"
                        st.experimental_rerun()

        elif login_or_register == "Register":
            st.markdown("<h1 class='main-header'>Cinema Booking - Registration</h1>", unsafe_allow_html=True)
            display_image("movie_ticket_booking_poster.png")

            with st.container():
                st.markdown("<h2 class='sub-header'>Create Account</h2>", unsafe_allow_html=True)
                username = st.text_input("Username")
                email = st.text_input("Email Address")
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                
                if st.button("REGISTER", use_container_width=True):
                    if not username or not email or not password:
                        st.error("All fields are required")
                    elif password != confirm_password:
                        st.error("Passwords do not match")
                    else:
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
                            st.session_state.username = result[1]  # Store username
                            st.success(f"Welcome, {username}! Your account has been created successfully.")
                            st.rerun()

# Movies page
elif page == "Movies":
    if st.session_state.custId is None:
        st.warning("Please login first to browse movies")
        if st.button("Go to Login"):
            page = "Login"
            st.rerun()
    else:
        st.markdown("<h1 class='main-header'>Select a Movie</h1>", unsafe_allow_html=True)
        display_image("popcornandstuff.jpeg")
        
        # Create a grid layout for movies
        mycursor.execute('SELECT ID, name FROM movie')
        movies = mycursor.fetchall()
        
        # Display movies in a more visual format
        movie_options = {str(movie[1]): movie[0] for movie in movies}
        selected_movie = st.selectbox("Choose a movie", options=list(movie_options.keys()))
        
        # Show movie details
        if selected_movie:
            movie_id = movie_options[selected_movie]
            mycursor.execute("SELECT * FROM movie WHERE ID = %s", (movie_id,))
            movie_details = mycursor.fetchone()
            
            # Display movie details if available
            if movie_details:
                st.subheader(f"About '{selected_movie}'")
                # Add any additional details if your movie table has them
                # For example: st.write(f"Genre: {movie_details[2]}")
                # st.write(f"Duration: {movie_details[3]} minutes")
            
            if st.button("Select This Movie", use_container_width=True):
                st.session_state.movie_id = movie_options[selected_movie]
                st.success(f"Selected: {selected_movie}")
                st.rerun()

# Theatre page
elif page == "Theatre":
    if st.session_state.custId is None:
        st.warning("Please login first to book theatres")
        if st.button("Go to Login"):
            page = "Login"
            st.rerun()
    elif "movie_id" not in st.session_state:
        st.warning("Please select a movie first")
        if st.button("Go to Movies"):
            page = "Movies"
            st.rerun()
    else:
        st.markdown("<h1 class='main-header'>Select Theatre & Showtime</h1>", unsafe_allow_html=True)
        
        # Get movie name for display
        mycursor.execute("SELECT name FROM movie WHERE ID = %s", (st.session_state.movie_id,))
        movie_name = mycursor.fetchone()[0]
        st.subheader(f"Selected Movie: {movie_name}")
        
        # Try to display movie-specific image
        display_image(f"{st.session_state.movie_id}.jpg")
        
        # Get available shows
        mycursor.execute('''SELECT s.ID, t.name, start_time, show_date, hall_ID
                           FROM shows s, theatre t
                           WHERE s.movie_ID=%s AND s.theatre_ID=t.ID
                           ORDER BY show_date, start_time''', (st.session_state.movie_id,))
        shows = mycursor.fetchall()
        
        if not shows:
            st.info("No showtimes available for this movie at the moment.")
        else:
            # Group shows by date
            show_dates = list(set([show[3] for show in shows]))
            show_dates.sort()  # Sort dates
            
            selected_date = st.selectbox("Select Date", options=show_dates)
            
            # Filter shows for selected date
            date_shows = [show for show in shows if show[3] == selected_date]
            
            # Create more user-friendly options
            show_options = {f"{row[1]} | {row[2].strftime('%I:%M %p') if isinstance(row[2], datetime) else row[2]} | Hall {row[4]}": row[0] for row in date_shows}
            
            selected_show = st.selectbox("Select Showtime", options=list(show_options.keys()))
            
            if st.button("Continue to Seat Selection", use_container_width=True):
                st.session_state.show_id = show_options[selected_show]
                st.success("Showtime selected! Let's choose your seats.")
                st.rerun()

# Seats page
elif page == "Seats":
    if st.session_state.custId is None:
        st.warning("Please login first to select seats")
        if st.button("Go to Login"):
            page = "Login"
            st.rerun()
    elif "show_id" not in st.session_state:
        st.warning("Please select a showtime first")
        if st.button("Go to Theatre Selection"):
            page = "Theatre"
            st.rerun()
    else:
        st.markdown("<h1 class='main-header'>Select Your Seats</h1>", unsafe_allow_html=True)
        display_image("popcornandstuff.jpeg")
        
        show_id = st.session_state.show_id
        
        # Get show details for display
                # Get show details for seat availability
        mycursor.execute('''SELECT ID, seat_ID, book_date, book_time 
                    FROM seatinline 
                    WHERE show_ID = %s 
                    ORDER BY seat_ID''', (show_id,))

        seats = mycursor.fetchall()
        
        # Display seats in rows (like A1 to A10, B1 to B10...)
        available_seats = [seat for seat in seats if not seat[2]]
        seat_labels = [seat[1] for seat in available_seats]

        st.markdown("<h2 class='sub-header'>Available Seats</h2>", unsafe_allow_html=True)
        selected_seats = st.multiselect("Choose your seats", seat_labels)

        if st.button("Confirm Seats", use_container_width=True):
            if not selected_seats:
                st.error("Please select at least one seat.")
            else:
                # Save selected seat IDs to session
                seat_ids = [seat[0] for seat in available_seats if seat[1] in selected_seats]
                st.session_state.seat_ids = seat_ids
                st.session_state.selected_seat_labels = selected_seats
                st.success(f"You have selected: {', '.join(selected_seats)}")
                st.rerun()

# Payment page
elif page == "Payment":
    if st.session_state.custId is None:
        st.warning("Please login first to make payment")
        if st.button("Go to Login"):
            page = "Login"
            st.rerun()
    elif "selected_seat_labels" not in st.session_state:
        st.warning("Please select seats first")
        if st.button("Go to Seat Selection"):
            page = "Seats"
            st.rerun()
    else:
        st.markdown("<h1 class='main-header'>Complete Your Booking</h1>", unsafe_allow_html=True)
        display_image("popcornandstuff.jpeg")
        
        show_id = st.session_state.show_id
        new_booked = st.session_state.selected_seats_labels
        
        # Get show details
        mycursor.execute('''SELECT * FROM shows WHERE ID=%s''', (show_id,))
        show_info = mycursor.fetchall()[0]
        mycursor.execute('''SELECT name FROM movie WHERE ID=%s''', (show_info[1],))
        movie_name = mycursor.fetchall()[0][0]
        mycursor.execute('''SELECT name FROM theatre WHERE ID=%s''', (show_info[3],))
        theatre_name = mycursor.fetchall()[0][0]
        fl_amt = int(show_info[7]) * len(new_booked)
        
        # Booking summary
        st.markdown("<h3>Booking Summary</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h4 style="margin-top: 0;">{movie_name}</h4>
            <p><strong>Theatre:</strong> {theatre_name}</p>
            <p><strong>Hall:</strong> {show_info[2]}</p>
            <p><strong>Date & Time:</strong> {show_info[6]} at {show_info[4]}</p>
            <p><strong>Seat(s):</strong> {', '.join(map(str, new_booked))}</p>
            <p><strong>Price per seat:</strong> ${show_info[7]}</p>
            <h4>Total: ${fl_amt}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Payment method selection
        payment_method = st.selectbox("Select Payment Method", ["Credit Card", "Debit Card", "PayPal"])
        
        # Payment form based on method
        if payment_method in ["Credit Card", "Debit Card"]:
            col1, col2 = st.columns(2)
            with col1:
                card_number = st.text_input("Card Number", placeholder="XXXX XXXX XXXX XXXX")
                card_name = st.text_input("Name on Card")
            with col2:
                expiry = st.text_input("Expiry (MM/YY)")
                cvv = st.text_input("CVV", type="password", max_chars=3)
        elif payment_method == "PayPal":
            st.text_input("PayPal Email")
            st.text_input("PayPal Password", type="password")
        
        # Complete payment button
        if st.button("Complete Payment", type="primary", use_container_width=True):
            # Process booking in database
            try:
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
                
                # Display success message and ticket
                st.balloons()
                st.success("Payment successful! Here's your booking confirmation.")
                
                # Display ticket
                st.markdown("""
                <div style="background: linear-gradient(to right, #0f0c29, #302b63, #24243e); color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
                    <h2 style="text-align: center; text-transform: uppercase; border-bottom: 1px solid #fff; padding-bottom: 10px;">Movie Ticket</h2>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div style="padding: 10px 0;">
                        <h3 style="margin: 0;">{movie_name}</h3>
                        <p style="opacity: 0.8; margin: 5px 0;">{theatre_name} | Hall {show_info[2]}</p>
                        <p style="opacity: 0.8; margin: 5px 0;">Date: {show_info[6]}</p>
                        <p style="opacity: 0.8; margin: 5px 0;">Time: {show_info[4]} - {show_info[5]}</p>
                        <p style="opacity: 0.8; margin: 5px 0;">Seat(s): {', '.join(map(str, new_booked))}</p>
                        <p style="opacity: 0.8; margin: 5px 0;">Booking ID: BOOK-{pay_id}</p>
                    </div>
                    <div style="text-align: center; margin-top: 15px;">
                        <p style="font-size: 14px;">Enjoy your movie! Please arrive 15 minutes before showtime.</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Clear session variables except user ID
                for key in list(st.session_state.keys()):
                    if key not in ["custId", "username"]:
                        del st.session_state[key]
                
                if st.button("Book Another Movie"):
                    page = "Movies"
                    st.rerun()
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.error("Please try again or contact customer support.")

# Run the app
if __name__ == "__main__":
    if st.session_state.custId is not None:
        username = getattr(st.session_state, 'username', f"User {st.session_state.custId}")
        st.sidebar.markdown(f"### Welcome, {username}!")
        if st.sidebar.button("Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    st.stop()
