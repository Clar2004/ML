from flask import Flask, request, jsonify
from model import load_data, preprocess_data, train_model, get_recommendations

app = Flask(__name__)

df = load_data()
df = preprocess_data(df)
model = train_model(df)

@app.route('/recommend', methods=['POST'])
def recommend():
    user_data = request.json
    store_location = user_data['store_location']
    product_category = user_data['product_category']
    product_type = user_data['product_type']
    unit_price = user_data['unit_price']

    new_data_point = [store_location, product_category, product_type, unit_price]
    recommendations = get_recommendations(model, df, new_data_point)
    
    # Ensure unique and non-duplicate recommendations
    recommendations = recommendations.drop_duplicates(subset=['product_detail'])
    
    result = recommendations.to_dict(orient='records')
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
