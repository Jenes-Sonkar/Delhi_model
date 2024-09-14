from flask import Flask, jsonify, request
from joblib import load
from datetime import datetime, timedelta

app = Flask(__name__)

# Load the pre-trained model
model = load('MLmodel.joblib')


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


def generate_date_range(start_day, start_month, num_days):
    # Convert month name to month number
    month_mapping = {f"Month_{i + 1}": i + 1 for i in range(12)}
    start_month_number = month_mapping[start_month]

    # Define the start date
    start_date = datetime(year=2023, month=start_month_number, day=start_day)

    # Generate a list of dates
    date_range = [start_date + timedelta(days=i) for i in range(num_days)]

    return date_range


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
            predictions[district] = prediction.tolist()

        # Find the prediction for the input_district
        if input_district in predictions:
            result = predictions[input_district][0]
        else:
            return jsonify({"error": "District not found in the list."}), 400

        return jsonify({"prediction": result})

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
            return jsonify(
                {"error": "Missing data. Ensure 'day', 'month', 'district1', and 'district2' are provided."}), 400

        # Define the list of districts
        districts = ["Chanakyapuri", "Civil Lines", "Connaught Place", "Daryaganj", "Defence Colony",
                     "Delhi Cantonment", "Gandhi Nagar", "Hauz Khas", "Kalkaji", "Karol Bagh", "Kotwali",
                     "Model Town", "Najafgarh", "Narela", "Paharganj", "Parliament Street", "Patel Nagar",
                     "Preet Vihar", "Punjabi Bagh", "Rajouri Garden", "Sadar Bazaar", "Saraswati Vihar",
                     "Seelampur", "Seemapuri", "Shahdara", "Vasant Vihar", "Vivek Vihar"]

        if district1 not in districts or district2 not in districts:
            return jsonify({"error": "One or both districts not found in the list."}), 400

        # Get the predictions for both districts for the next 15 days from the given input date
        def get_predictions(district):
            date_range = generate_date_range(input_day, input_month, 15)
            predictions = []
            for date in date_range:
                day_str = f"Day_{date.day}"
                month_str = f"Month_{date.month}"
                ml_input = model_input(day_str, district, month_str)
                prediction = model.predict([ml_input])
                predictions.append({
                    "date": f"{month_str} {date.day}",
                    "prediction": prediction[0]
                })
            return predictions

        # Get predictions for both districts
        district1_predictions = get_predictions(district1)
        district2_predictions = get_predictions(district2)

        # Prepare the result with district names and predictions
        comparison_result = {
            "district1": {
                "name": district1,
                "predictions": district1_predictions
            },
            "district2": {
                "name": district2,
                "predictions": district2_predictions
            }
        }

        return jsonify(comparison_result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
