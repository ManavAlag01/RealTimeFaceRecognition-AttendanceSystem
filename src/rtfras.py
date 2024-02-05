import os.path
import datetime
import subprocess
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error
import traceback

import util

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1100x520")
        self.main_window.title('Real-time Face Recognition Attendance System')

        self.login_button_main_window = util.get_button(self.main_window, 'Login', 'green', self.login)
        self.login_button_main_window.place(x=750, y=300)

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'Register new user', 'gray',
                                                                    self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=400)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'

        self.mysql_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '123456',
            'database': 'rtfrasdb'
        }

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()    

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def login(self):
         unknown_img_path = './.tmp.jpg'
         cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)
         output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
         name = output.split(',')[1][:-5]

         if name in ['unknown_person', 'no_persons_found']:
             util.msg_box('Oops..', 'Unknown user. Please register a new user or try again')
         else:
             util.msg_box('Welcome back!', 'Welcome, {}'.format(name))

            # Log the login time in the regulardays table
             self.log_login_time(name)

         os.remove(unknown_img_path)

    def log_login_time(self, username):
         sql_insert = "INSERT INTO regulardays (user_id, username, login_date, login_time) VALUES (%s, %s, %s, %s)"
         current_datetime = datetime.datetime.now()
         user_id = self.get_user_id_by_username(username)

         values = (
            user_id,
            username,
            current_datetime.date(),
            current_datetime.strftime("%I:%M:%S %p")  # Format time in 12-hour format
         )

         try:
             connection = mysql.connector.connect(**self.mysql_config)
             cursor = connection.cursor()

             cursor.execute(sql_insert, values)
             connection.commit()
             print(f"Login time recorded in the regulardays table for the user {username}")

         except Exception as e:
             traceback.print_exc()
             print(f"Error: {e}")

         finally:
             if cursor:
                 cursor.close()

             if connection and connection.is_connected():
                 connection.close()

    def get_user_id_by_username(self, username):
        sql_select = "SELECT user_id FROM myinfo WHERE username = %s"
        value = (username,)

        try:
            connection = mysql.connector.connect(**self.mysql_config)
            cursor = connection.cursor()

            cursor.execute(sql_select, value)
            result = cursor.fetchall()

            if result:
                return result[0][0]

        except Exception as e:
            traceback.print_exc()
            print(f"Error: {e}")

        finally:
            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

        return None

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1100x520")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green',
                                                                      self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try again',
                                                                         'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        # Label and Text field for entering username
        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window,
                                                                'Please, input username:')
        self.text_label_register_new_user.place(x=750, y=10)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=50)

        # Label and Text field for entering ID
        self.text_label_register_new_user_id = util.get_text_label(self.register_new_user_window, 'Enter Your ID:')
        self.text_label_register_new_user_id.place(x=750, y=150)

        self.entry_text_register_new_user_id = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user_id.place(x=750, y=190)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def start(self):
        self.main_window.mainloop()

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c").strip()
        user_id = self.entry_text_register_new_user_id.get(1.0, "end-1c").strip()

        # Check if the user ID is already used
        if self.is_user_id_exists(user_id):
            util.msg_box('Error', 'ID already exists. Please enter a unique ID.')
            return

        if not name or not user_id:
            util.msg_box('Error', 'Please enter your details first.')
            return

        # Save the image file to disk
        image_filename = '{}.jpg'.format(name)
        image_path = os.path.join(self.db_dir, image_filename)

        # Debugging: Print the image path before saving
        print(f"Saving image to: {image_path}")

        cv2.imwrite(image_path, self.register_new_user_capture)

        # Debugging: Print a message after saving the image
        print("Image saved successfully")

        # Insert user information into the database
        sql_insert = "INSERT INTO myinfo (username, user_id, image_path, date, time) VALUES (%s, %s, %s, %s, %s)"

        current_datetime = datetime.datetime.now()
        values = (
            name,
            int(user_id),
            image_path,
            current_datetime.strftime("%Y-%m-%d"),
            current_datetime.strftime("%I:%M:%S %p")  # Format time in 12-hour format with AM/PM
        )

        try:
            connection = mysql.connector.connect(**self.mysql_config)
            cursor = connection.cursor()

            cursor.execute(sql_insert, values)
            connection.commit()
            print("User information inserted into the database")

            # Debugging: Print a message after successful insertion
            print("Image path, date, and time updated in the database")

        except Exception as e:
            traceback.print_exc()  # Printing the full exception traceback for debugging
            print(f"Error: {e}")

        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

        util.msg_box('Success!', 'User was registered successfully!')
        self.register_new_user_window.destroy()

    def is_user_id_exists(self, user_id):
        # Check if the user ID already exists in the myinfo table
        sql_check_user_id = "SELECT COUNT(*) FROM myinfo WHERE user_id = %s"
        value = (user_id,)

        try:
            connection = mysql.connector.connect(**self.mysql_config)
            cursor = connection.cursor()

            cursor.execute(sql_check_user_id, value)
            result = cursor.fetchone()

            return result[0] > 0

        except Exception as e:
            traceback.print_exc()
            print(f"Error: {e}")

        finally:
            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()
                
        return False
    
if __name__ == "__main__":
    app = App()
    app.start()
