from flask import Flask,render_template,request, jsonify
import pickle
import numpy as np
import os
from flask_cors import CORS

current_dir = os.path.dirname(os.path.abspath(__file__))

# Tạo đường dẫn tới file "popular.pkl"
popular_path = os.path.join(current_dir, "popular.pkl")

pt_path = os.path.join(current_dir ,"pt.pkl")
books_path = os.path.join(current_dir ,"books.pkl")
similarity_scores_path = os.path.join(current_dir ,"similarity_scores.pkl")
popular_df = pickle.load(open(popular_path,'rb'))
pt = pickle.load(open(pt_path,'rb'))
books = pickle.load(open(books_path,'rb'))
similarity_scores = pickle.load(open(similarity_scores_path,'rb'))

app = Flask(__name__)
CORS(app)

@app.route('/all', methods=['get'])
def index():
    # return render_template('index.html',
    #                        book_name = list(popular_df['Book-Title'].values),
    #                        author=list(popular_df['Book-Author'].values),
    #                        image=list(popular_df['Image-URL-M'].values),
    #                        votes=list(popular_df['num_ratings'].values),
    #                        rating=list(popular_df['avg_rating'].values)
    #                        )
    data = []
    similar_items = list(enumerate(popular_df['Book-Title'].values))

    for i in similar_items:
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item = {
            'title': ', '.join(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values)),
            'author': ', '.join(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values)),
            'url': ', '.join(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        }
        data.append(item)
    print(data)
    return jsonify({'data': data})
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
@cross_origin()
def recommend():
    user_input = request.form.get('user_input')
    print(user_input)
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]
    
    data = []
    for i in similar_items:
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item = {
            'title': ', '.join(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values)),
            'author': ', '.join(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values)),
            'url': ', '.join(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        }
        data.append(item)
    print(data)
    return jsonify({'data': data})

if __name__ == '__main__':
    app.run(debug=True)