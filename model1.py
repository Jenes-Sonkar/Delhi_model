from flask import Flask, jsonify, request
from joblib import load
from datetime import datetime, timedelta

app = Flask(__name__)

# Load the pre-trained model
model = load('MLmodel.joblib')

list2 = []

# Define a mapping from month code to month name
month_mapping = {
    "Month_1": "January",
    "Month_2": "February",
    "Month_3": "March",
    "Month_4": "April",
    "Month_5": "May",
    "Month_6": "June",
    "Month_7": "July",
    "Month_8": "August",
    "Month_9": "September",
    "Month_10": "October",
    "Month_11": "November",
    "Month_12": "December"
}

def model_input(input_day, input_district, input_month):
    sub_districts = ["Chanakyapuri", "Civil Lines", "Connaught Place", "Daryaganj", "Defence Colony",
                     "Delhi Cantonment", "Gandhi Nagar", "Hauz Khas", "Kalkaji", "Karol Bagh", "Kotwali",
                     "Model Town", "Najafgarh", "Narela", "Paharganj", "Parliament Street", "Patel Nagar",
                     "Preet Vihar", "Punjabi Bagh", "Rajouri Garden", "Sadar Bazaar", "Saraswati Vihar",
                     "Seelampur", "Seemapuri", "Shahdara", "Vasant Vihar", "Vivek Vihar"]

    month = ["Month_1", "Month_2", "Month_3", "Month_4", "Month_5", "Month_6", "Month_7", "Month_8",
             "Month_9", "Month_10", "Month_11", "Month_12"]

    day = ["Day_1", "Day_2", "Day_3", "Day_4", "Day_5", "Day_6", "Day_7", "Day_8", "Day_9", "Day_10",
           "Day_11", "Day_12", "Day_13", "Day_14", "Day_15", "Day_16", "Day_17", "Day_18", "Day_19",
           "Day_20", "Day_21", "Day_22", "Day_23", "Day_24", "Day_25", "Day_26", "Day_27", "Day_28",
           "Day_29", "Day_30", "Day_31"]

    inputDistrict = [district == input_district for district in sub_districts]
    inputMonth = [month_item == input_month for month_item in month]
    inputDay = [day_item == input_day for day_item in day]

    merged_input = inputDistrict + inputMonth + inputDay
    return merged_input

def format_date(day, month):
    day = int(day)
    month_name = month_mapping.get(month, "Unknown Month")
    return f"{day} {month_name}"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Parse JSON request
        data = request.get_json()
        input_day = data.get('day')
        input_district = data.get('district')
        input_month = data.get('month')

        if not all([input_day, input_district, input_month]):
            return jsonify({"error": "Missing data. Ensure 'day', 'district', and 'month' are provided."}), 400

        # Define the list of districts
        districts = ["Chanakyapuri", "Civil Lines", "Connaught Place", "Daryaganj", "Defence Colony",
                     "Delhi Cantonment", "Gandhi Nagar", "Hauz Khas", "Kalkaji", "Karol Bagh", "Kotwali",
                     "Model Town", "Najafgarh", "Narela", "Paharganj", "Parliament Street", "Patel Nagar",
                     "Preet Vihar", "Punjabi Bagh", "Rajouri Garden", "Sadar Bazaar", "Saraswati Vihar",
                     "Seelampur", "Seemapuri", "Shahdara", "Vasant Vihar", "Vivek Vihar"]

        predictions = {}

        for district in districts:
            ml_input = model_input(input_day, district, input_month)  # Prepare the input
            prediction = model.predict([ml_input])  # Get the prediction
            predictions[district] = prediction.tolist()  # Store the prediction for the district
            list2.append(str(predictions[district][0]))

        # Find the prediction for the input_district
        if input_district in districts:
            index = districts.index(input_district)
            result = list2[index]
        else:
            return jsonify({"error": "District not found in the list."}), 400
        print(list2)
        return jsonify({"prediction": result})  # Return the prediction for the input district

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/list2", methods=["GET"])
def get_list2():
    try:
        return jsonify({"list2": list2})  # Return list2 as JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/compare", methods=["POST"])
def compare_districts():
    try:
        # Parse JSON request
        data = request.get_json()
        input_day = int(data.get('day'))
        input_month = data.get('month')
        district1 = data.get('district1')
        district2 = data.get('district2')

        if not all([input_day, input_month, district1, district2]):
            return jsonify({"error": "Missing data. Ensure 'day', 'month', 'district1', and 'district2' are provided."}), 400

        # Define the list of districts
        districts = ["Chanakyapuri", "Civil Lines", "Connaught Place", "Daryaganj", "Defence Colony",
                     "Delhi Cantonment", "Gandhi Nagar", "Hauz Khas", "Kalkaji", "Karol Bagh", "Kotwali",
                     "Model Town", "Najafgarh", "Narela", "Paharganj", "Parliament Street", "Patel Nagar",
                     "Preet Vihar", "Punjabi Bagh", "Rajouri Garden", "Sadar Bazaar", "Saraswati Vihar",
                     "Seelampur", "Seemapuri", "Shahdara", "Vasant Vihar", "Vivek Vihar"]

        if district1 not in districts or district2 not in districts:
            return jsonify({"error": "One or both districts not found in the list."}), 400

        # Calculate the date range
        start_date = datetime(year=2024, month=int(input_month.split('_')[1]), day=input_day)
        predictions1 = []
        predictions2 = []

        for i in range(15):
            current_date = start_date + timedelta(days=i)
            formatted_date = current_date.strftime("%d %B")
            formatted_month = f"Month_{current_date.month}"
            day_str = f"Day_{current_date.day}"

            # Get predictions for both districts
            ml_input1 = model_input(day_str, district1, formatted_month)
            prediction1 = model.predict([ml_input1])[0]

            ml_input2 = model_input(day_str, district2, formatted_month)
            prediction2 = model.predict([ml_input2])[0]

            predictions1.append({"date": formatted_date, "prediction": prediction1})
            predictions2.append({"date": formatted_date, "prediction": prediction2})

        # Compare predictions
        comparison_result = {
            "district1": {
                "name": district1,
                "predictions": predictions1
            },
            "district2": {
                "name": district2,
                "predictions": predictions2
            }
        }

        return jsonify(comparison_result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/last_three_days", methods=["POST"])
def last_three_days():
    try:
        # Parse JSON request
        data = request.get_json()
        input_day = int(data.get('day'))
        input_month = data.get('month')
        input_district = data.get('district')

        if not all([input_day, input_month, input_district]):
            return jsonify({"error": "Missing data. Ensure 'day', 'month', and 'district' are provided."}), 400

        # Define the list of districts
        districts = ["Chanakyapuri", "Civil Lines", "Connaught Place", "Daryaganj", "Defence Colony",
                     "Delhi Cantonment", "Gandhi Nagar", "Hauz Khas", "Kalkaji", "Karol Bagh", "Kotwali",
                     "Model Town", "Najafgarh", "Narela", "Paharganj", "Parliament Street", "Patel Nagar",
                     "Preet Vihar", "Punjabi Bagh", "Rajouri Garden", "Sadar Bazaar", "Saraswati Vihar",
                     "Seelampur", "Seemapuri", "Shahdara", "Vasant Vihar", "Vivek Vihar"]

        if input_district not in districts:
            return jsonify({"error": "District not found in the list."}), 400

        # Calculate the date range
        start_date = datetime(year=2024, month=int(input_month.split('_')[1]), day=input_day)
        predictions = []

        for i in range(3):
            current_date = start_date - timedelta(days=2-i)
            formatted_date = current_date.strftime("%d %B")
            formatted_month = f"Month_{current_date.month}"
            day_str = f"Day_{current_date.day}"

            # Get prediction for the district
            ml_input = model_input(day_str, input_district, formatted_month)
            prediction = model.predict([ml_input])[0]

            predictions.append({"date": formatted_date, "prediction": prediction})

        return jsonify({"district": input_district, "predictions": predictions})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    app.run(debug=True)
