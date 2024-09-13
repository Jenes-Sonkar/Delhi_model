from flask import Flask ,jsonify,request
from joblib import load

app = Flask("__name__")

model=load('MLmodel.joblib')


# def graph_data(input_day,input_month):
#     list1=[]
#     list2=["Chanakyapuri", "Civil Lines", "Connaught Place", "Daryaganj", "Defence Colony",
#                      "Delhi Cantonment", "Gandhi Nagar",
#                      "Hauz Khas", "Kalkaji", "Karol Bagh", "Kotwali", "Model Town", "Najafgarh", "Narela", "Paharganj",
#                      "Parliament Street", "Patel Nagar",
#                      "Preet Vihar", "Punjabi Bagh", "Rajouri Garden", "Sadar Bazaar", "Saraswati Vihar", "Seelampur",
#                      "Seemapuri", "Shahdara", "Vasant Vihar",
#                      "Vivek Vihar"]
#     for i in range (27):
#         list1.append()




def model_input(input_day, input_district, input_month):
    sub_districts = ["Chanakyapuri", "Civil Lines", "Connaught Place", "Daryaganj", "Defence Colony",
                     "Delhi Cantonment", "Gandhi Nagar",
                     "Hauz Khas", "Kalkaji", "Karol Bagh", "Kotwali", "Model Town", "Najafgarh", "Narela", "Paharganj",
                     "Parliament Street", "Patel Nagar",
                     "Preet Vihar", "Punjabi Bagh", "Rajouri Garden", "Sadar Bazaar", "Saraswati Vihar", "Seelampur",
                     "Seemapuri", "Shahdara", "Vasant Vihar",
                     "Vivek Vihar"]
    month = ["Month_1", "Month_2", "Month_3", "Month_4", "Month_5", "Month_6", "Month_7", "Month_8", "Month_9",
             "Month_10", "Month_11",
             "Month_12"]
    day = ["Day_1", "Day_2", "Day_3", "Day_4", "Day_5", "Day_6", "Day_7", "Day_8", "Day_9", "Day_10", "Day_11",
           "Day_12", "Day_13", "Day_14",
           "Day_15", "Day_16", "Day_17", "Day_18", "Day_19", "Day_20", "Day_21", "Day_22", "Day_23", "Day_24", "Day_25",
           "Day_26", "Day_27"
        , "Day_28", "Day_29", "Day_30", "Day_31"]

    inputDistrict = []
    inputMonth = []
    inputDay = []

    for district in sub_districts:
        if district == input_district:
            inputDistrict.append(True)
        else:
            inputDistrict.append(False)

    for days in day:
        if days == input_day:
            inputDay.append(True)
        else:
            inputDay.append(False)

    for months in month:
        if months == input_month:
            inputMonth.append(True)
        else:
            inputMonth.append(False)

    merged_input = inputDistrict + inputMonth + inputDay
    return merged_input


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Json format me data le lia hai
        data = request.get_json()
        input_day = data.get('day')
        input_district = data.get('district')
        input_month = data.get('month')

        if not all([input_day, input_district, input_month]):
            return jsonify({"error": "Missing data. Ensure 'day', 'district', and 'month' are provided."}), 400


        ml_input = model_input(input_day, input_district, input_month) # yeh input lekr model ko call krke data de dega

        #
        prediction = model.predict([ml_input])# predicting


        return jsonify({"prediction": prediction.tolist()}) # predicted array ko json format mai dega

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)