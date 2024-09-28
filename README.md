
1. Project Overview
   The Activity Tracker Project is designed to help users manage and analyze their daily activities. 
   It allows users to log activities, predict future activities using machine learning models, 
   visualize their activity patterns, and receive suggestions for new activities. 
   The project combines data management, machine learning, and a user-friendly interface.

2. Key Features
   2.1 Add Activity:
       Users can enter activities through a dialog box, including the day, start time, end time, 
       and a description of the activity. This information is stored in a CSV file for later retrieval and analysis.

   2.2 Predict Activity:
       Users can predict activities based on the logged data using two different machine learning models:
       - Random Forest: A popular ensemble learning method that constructs multiple decision trees.
       - XGBoost: An optimized gradient boosting framework that is highly effective for classification tasks.
       The accuracy of each model is calculated and displayed to the user.

   2.3 Visualize Activities:
       Users can visualize the distribution of activities using a bar chart. This feature helps users 
       understand how often they perform different activities.

   2.4 Analyze Trends:
       Users can analyze trends over time by plotting the number of activities performed each day. 
       This feature provides insights into how the user's routine changes.

   2.5 Suggest New Activity:
       The application suggests an activity that the user may not have done recently, encouraging them 
       to try something new based on their logged activities.

   2.6 Speech-to-Text Activity Entry:
       Users can add activities using voice input. The application utilizes the SpeechRecognition library 
       to convert speech into text, allowing for hands-free activity logging.

3. Components
   3.1 Data Storage:
       Activities are stored in a CSV file (mydailyroutine.csv). The data includes columns for the 
       day, start time, end time, and description of the activity. If the file doesn't exist when 
       the application starts, it is created with appropriate headers.

   3.2 User Interface (UI):
       The UI is built using the Tkinter library, providing a straightforward and intuitive way 
       for users to interact with the application. The interface includes buttons for each functionality 
       and uses dialog boxes to gather user input.

   3.3 Machine Learning:
       The project utilizes scikit-learn for implementing the Random Forest model and XGBoost for 
       the XGBoost model. The models are trained on historical activity data to predict future 
       activities based on the logged information.

   3.4 Data Visualization:
       Matplotlib is used for visualizing activity data through bar charts and line plots. 
       This helps users quickly grasp their activity patterns and trends over time.

4. How It Works
   4.1 Starting the Application:
       When the application starts, the main window is displayed with buttons for different functionalities.

   4.2 Adding an Activity:
       When the "Add Activity" button is clicked, a series of dialog boxes prompt the user for the 
       day, start time, end time, and activity description. The new activity is appended to the CSV file.

   4.3 Predicting Activities:
       Clicking on either the "Predict Activity (Random Forest)" or "Predict Activity (XGBoost)" button 
       trains the selected model on the logged activity data and displays the prediction accuracy.

   4.4 Visualizing Data:
       Clicking the "Visualize Activities" button generates a bar chart showing how many times each 
       activity has been logged.

   4.5 Analyzing Trends:
       The "Analyze Trends" button generates a line plot showing the number of activities performed 
       each day, allowing users to see their engagement over time.

   4.6 Suggestions:
       The application can suggest a new activity that the user might enjoy but hasn't logged recently.

   4.7 Speech Recognition:
       Clicking the "Add Activity via Speech" button allows users to log activities by speaking. 
       The spoken input is converted to text, and the user is prompted to provide the end time for the activity.

5. Technologies Used
   - Python: The main programming language used for the implementation.
   - Tkinter: For creating the GUI.
   - Pandas: For data manipulation and CSV file handling.
   - Matplotlib: For data visualization.
   - Scikit-learn: For implementing machine learning models (Random Forest).
   - XGBoost: For implementing the XGBoost classification model.
   - SpeechRecognition: For converting speech to text.

6. Potential Enhancements
   - User Authentication: Implement user accounts to store activities separately for different users.
   - Mobile/Web Versions: Extend the application to mobile or web platforms for better accessibility.
   - Reminders and Notifications: Add a feature to set reminders for activities.
   - Integrate Fitness Tracker: Sync with fitness trackers to log physical activities automatically.
   - Mood/Stress Tracking: Include features for users to log their mood or stress levels associated with different activities.

