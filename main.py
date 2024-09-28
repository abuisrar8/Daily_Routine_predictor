import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import speech_recognition as sr
from datetime import datetime
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

# Data file path
data_file = "mydailyroutine.csv"

# ------------------------------------------------------------------------------
# Initialize the CSV file if it doesn't exist
if not os.path.exists(data_file):
    pd.DataFrame(columns=['Day', 'Start Time', 'End Time', 'Activity']).to_csv(data_file, index=False)

# ------------------------------------------------------------------------------
# Activity Tracker Class
class ActivityTracker:
    def __init__(self, master):
        self.master = master
        master.title("Activity Tracker")

        # Buttons for different functionalities
        self.add_activity_button = tk.Button(master, text="Add Activity", command=self.add_activity)
        self.add_activity_button.pack()

        self.predict_rf_button = tk.Button(master, text="Predict Activity (Random Forest)", command=self.predict_activity_rf)
        self.predict_rf_button.pack()

        self.predict_xgb_button = tk.Button(master, text="Predict Activity (XGBoost)", command=self.predict_activity_xgb)
        self.predict_xgb_button.pack()

        self.visualize_button = tk.Button(master, text="Visualize Activities", command=self.visualize_activities)
        self.visualize_button.pack()

        self.analyze_button = tk.Button(master, text="Analyze Trends", command=self.analyze_trends)
        self.analyze_button.pack()

        self.suggest_button = tk.Button(master, text="Suggest New Activity", command=self.suggest_new_activity)
        self.suggest_button.pack()

        self.speech_button = tk.Button(master, text="Add Activity via Speech", command=self.speech_to_text)
        self.speech_button.pack()

    # ------------------------------------------------------------------------------
    # Add activity method
    def add_activity(self):
        day = simpledialog.askstring("Input", "Enter the day (YYYY-MM-DD):")
        start_time = simpledialog.askstring("Input", "Enter the start time (HH:MM):")
        end_time = simpledialog.askstring("Input", "Enter the end time (HH:MM):")
        description = simpledialog.askstring("Input", "Enter the activity description:")

        # Parse the activity description
        activity = self.parse_activity(description)

        # Add new activity to the DataFrame and save it
        new_row = {'Day': day, 'Start Time': start_time, 'End Time': end_time, 'Activity': activity}
        df = pd.read_csv(data_file)
        df = df.append(new_row, ignore_index=True)
        df.to_csv(data_file, index=False)
        messagebox.showinfo("Success", "Activity added successfully.")

    # ------------------------------------------------------------------------------
    # Predict activity using Random Forest
    def predict_activity_rf(self):
        df = pd.read_csv(data_file)
        accuracy = self.train_model(df, model_type="RandomForest")
        messagebox.showinfo("Prediction Result", f"Prediction accuracy using Random Forest: {accuracy * 100:.2f}%")

    # ------------------------------------------------------------------------------
    # Predict activity using XGBoost
    def predict_activity_xgb(self):
        df = pd.read_csv(data_file)
        accuracy = self.train_model(df, model_type="XGBoost")
        messagebox.showinfo("Prediction Result", f"Prediction accuracy using XGBoost: {accuracy * 100:.2f}%")

    # ------------------------------------------------------------------------------
    # Visualize activities
    def visualize_activities(self):
        df = pd.read_csv(data_file)
        activity_counts = df['Activity'].value_counts()

        # Plot the data
        plt.bar(activity_counts.index, activity_counts.values)
        plt.xlabel("Activities")
        plt.ylabel("Frequency")
        plt.title("Activity Distribution")
        plt.xticks(rotation=45)
        plt.show()

    # ------------------------------------------------------------------------------
    # Analyze trends
    def analyze_trends(self):
        df = pd.read_csv(data_file)
        daily_summary = df.groupby('Day').size()
        daily_summary.plot(kind='line', title="Number of Activities Over Time", ylabel="Activities", xlabel="Date")
        plt.show()

    # ------------------------------------------------------------------------------
    # Suggest new activity
    def suggest_new_activity(self):
        df = pd.read_csv(data_file)
        common_activities = df['Activity'].value_counts()
        least_frequent = common_activities.idxmin()  # Get the least frequent activity
        messagebox.showinfo("Suggestion", f"Try something new today! How about {least_frequent}?")

    # ------------------------------------------------------------------------------
    # Speech-to-text activity entry
    def speech_to_text(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            print("You said: " + text)
            day = datetime.now().strftime('%Y-%m-%d')
            start_time = datetime.now().strftime('%H:%M')
            end_time = simpledialog.askstring("Input", "Enter the end time (HH:MM):")

            # Parse the spoken activity description
            activity = self.parse_activity(text)

            # Add the recognized activity
            new_row = {'Day': day, 'Start Time': start_time, 'End Time': end_time, 'Activity': activity}
            df = pd.read_csv(data_file)
            df = df.append(new_row, ignore_index=True)
            df.to_csv(data_file, index=False)
            messagebox.showinfo("Success", "Activity added successfully based on speech input.")
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Could not understand audio")
        except sr.RequestError:
            messagebox.showerror("Error", "Could not request results")

    # ------------------------------------------------------------------------------
    # Model training function
    def train_model(self, df, model_type="RandomForest"):
        # Split data into features and labels
        X = df[['Day', 'Start Time', 'End Time']]
        y = df['Activity']

        # Split into training and test data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train model
        if model_type == "RandomForest":
            model = RandomForestClassifier(n_estimators=100, random_state=42)
        else:
            model = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # Output the accuracy
        accuracy = accuracy_score(y_test, y_pred)
        return accuracy

    # ------------------------------------------------------------------------------
    # Parse activity description
    def parse_activity(self, description):
        if "exercise" in description.lower():
            return "Exercise"
        elif "work" in description.lower():
            return "Work"
        elif "read" in description.lower():
            return "Reading"
        else:
            return "Other"

# ------------------------------------------------------------------------------
# Main function
if __name__ == "__main__":
    root = tk.Tk()
    tracker = ActivityTracker(root)
    root.mainloop()
