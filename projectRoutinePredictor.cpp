#include <iostream>
#include <fstream>
#include <time.h>
#include<string.h>
#include<vector>
#include <iomanip>
#include <algorithm>
#include <map>


using namespace std;

class Activity {
public:
    string day;
    string startTime;
    string endTime;
    string description;

    Activity(const string& day, const string& startTime, const string& endTime, const string& description)
        : day(day), startTime(startTime), endTime(endTime), description(description) {}
};

// -----------------------------------------------------------------Reading activities from CSV file
vector<Activity> readActivitiesFromCSV(const string& filename) {
    vector<Activity> activities;

    ifstream file(filename);
    if (file.is_open()) {
        string line;
        getline(file, line); 
        while (getline(file, line)) {
            stringstream ss(line);
            string day, startTime, endTime, description;
            getline(ss, day, ',');
            getline(ss, startTime, ',');
            getline(ss, endTime, ',');
            getline(ss, description, ',');
            activities.push_back(Activity(day, startTime, endTime, description));
        }
        file.close();
    } else {
        cout << "Error: Could not open file " << filename << endl;
    }

    return activities;
}

// ----------------------------------------------------------------------------Writing activities to CSV file
void writeToCSV(const vector<Activity>& activities, const string& filename) {
    ofstream file(filename);
    file << "Day,Start Time,End Time,Activity\n";
    for (const Activity& activity : activities) {
        file << activity.day << "," << activity.startTime << "," << activity.endTime << "," << activity.description << "\n";
    }
    file.close();
}

// ------------------------------------------------------------------------------Predict current activity (simple rule-based approach)
string predictCurrentActivity(const vector<Activity>& activities) {
    // Get current time
    time_t now = time(0);
    tm* localTime = localtime(&now);
    string currentDay = string(asctime(localTime)).substr(0, 3);
    string currentTime = string(asctime(localTime)).substr(11, 5);

    // Find matching activities
    vector<Activity> matchingActivities;
    for (const Activity& activity : activities) {
        if (activity.day == currentDay && activity.startTime <= currentTime) {
            matchingActivities.push_back(activity);
        }
    }

    // Choose the most frequent activity (considering empty end times)
    if (!matchingActivities.empty()) {
        map<string, int> activityCounts;
        for (const Activity& activity : matchingActivities) {
            string matchingEndTime = activity.endTime;
            if (matchingEndTime.empty()) {
                // Find the next activity's start time as end time
                for (const Activity& nextActivity : activities) {
                    if (nextActivity.day == currentDay && nextActivity.startTime > activity.startTime) {
                        matchingEndTime = nextActivity.startTime;
                        break;
                    }
                }
            }
            activityCounts[activity.description]++;
        }

        // Find the activity with the highest count
        string mostFrequentActivity;
        int maxCount = 0;
        for (const auto& pair : activityCounts) {
            if (pair.second > maxCount) {
                maxCount = pair.second;
                mostFrequentActivity = pair.first;
            }
        }

        return mostFrequentActivity;
    } else {
        return "No matching activity found.";
    }
}

int main() {
    // Read activities from CSV file
    vector<Activity> activities = readActivitiesFromCSV("mydailyroutine.csv");

    int choice;
    while (true) {
        cout << "\nChoose an option:\n";
        cout << "1. Add activity\n";
        cout << "2. Predict current activity\n";
        cout << "3. Exit\n";
        cout << "Enter your choice: ";
        cin >> choice;

        if (choice == 1) {
            // Add activity logic
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            string day, startTime, endTime, description;

            // Get date and time (optional manual entry)
            time_t now = time(0);
            tm* localTime = localtime(&now);
            char timeBuffer[80];
            strftime(timeBuffer, sizeof(timeBuffer), "%Y-%m-%d", localTime); // Format for date
            day = timeBuffer; // Use current date by default

            strftime(timeBuffer, sizeof(timeBuffer), "%H:%M", localTime);
            startTime = timeBuffer; // Use current time by default

            cout << "Enter the day (YYYY-MM-DD) (leave blank for today): ";
            getline(cin,day); // Allow manual override for date
            if (day.empty()) {
                day = timeBuffer; // Use current date if left blank
            }

            cout << "Enter the start time (HH:MM) (leave blank for current time): ";
            getline(cin, startTime); // Allow manual override for time
            if (startTime.empty()) {
                startTime = timeBuffer; // Use current time if left blank
            }

            cout << "Enter the end time (HH:MM): ";
            getline(cin, endTime);
            cout << "Enter the activity description: ";
            getline(cin, description);

            // Create and add activity
            Activity activity(day, startTime, endTime, description);
            activities.push_back(activity);

            // Write updated activities to CSV file
            writeToCSV(activities, "mydailyroutine.csv");
            cout << "Activity added to CSV file successfully!\n";
        } else if (choice == 2) {
            // Predict current activity
            string predictedActivity = predictCurrentActivity(activities);
            cout << "Predicted activity: " << predictedActivity << endl;

            char confirm;
            cout << "Are you satisfied with this prediction? (y/n): ";
            cin >> confirm;

            if (confirm == 'y') {
                // Get current time
                time_t now = time(0);
                tm* localTime = localtime(&now);
                string currentDay = string(asctime(localTime)).substr(0, 3);
                string currentTime = string(asctime(localTime)).substr(11, 5);

                // Create an Activity object with the predicted activity
                Activity activity(currentDay, currentTime, currentTime, predictedActivity);
                activities.push_back(activity);

                // Write updated activities to CSV file
                writeToCSV(activities, "mydailyroutine.csv");
                cout << "Activity added to CSV file successfully!\n";
            }
        } else if (choice == 3) {
            break;
        } else {
            cout << "Invalid choice. Please try again.\n";
        }
    }

    return 0;
}
