from flask import Flask, render_template, request
import pandas as pd
from database import conn_to_db, sql_query

# build database connection

conn, engine = conn_to_db()


# get Activities and Amenities
activities = sql_query("select * from wanderwisely.activity_related_parks", conn)
activities = activities["name"].unique()
amenities = sql_query("select * from wanderwisely.amenity_related_parks", conn)
amenities = amenities["name"].unique()

# record user's selection
user_selection = {"activities":[], "amenities":[]}


def update_selection(selection, select_type):
    if selection in user_selection[select_type]:
        user_selection[select_type].remove(selection)
    else:
        user_selection[select_type].append(selection)
    

app = Flask(__name__)

@app.route('/ActivitiesAndAmenities')
def ActivitiesAndAmenities():
    return render_template('ActivitiesAndAmenities.html',activities = activities, amenities = amenities)

@app.route('/record_button', methods=['POST'])
def record_button():
    data = request.get_json()
    update_selection(data["input"], data["type"])
    # Record the button click in the database or perform any other action
    return '', 204


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/park',methods=['GET', 'POST'])
def park():# put application's code here
    if request.method == 'GET':
        #this is for testing
        #value={"my_dict": {"amenity": ["4E4D076A-6866-46C8-A28B-A129E2B8F3DB","04D29064-B9A1-4031-AD0E-98E31EF69604"],"activity": ["13A57703-BB1A-41A2-94B8-53B692EB7238","5F723BAD-7359-48FC-98FA-631592256E35"]}}
        value = request.get_json()
        my_dict = value['my_dict'] 
        amenity_ids=my_dict['amenity']
        activity_ids=my_dict['activity']
        print('amenity_id: ', amenity_ids)
        print('activity_id: ', activity_ids)
        df_amenity = sql_query("select * from wanderwisely.amenity_related_parks", conn)
        df_activity = sql_query("select * from wanderwisely.activity_related_parks", conn)
        parks_df = pd.merge(df_amenity, df_activity, on='parkCode', how='outer')
        parks_df = parks_df.rename(columns={'id_x': 'amenity_id',
                                        'name_x': 'amenity_name',
                                        'designation_x': 'amenity_designation',
                                        'state_x': 'amenity_state',
                                        'parkName_x': 'amenity_parkName',
                                        'id_y': 'activity_id',
                                        'name_y': 'activity_name',
                                        'designation_y': 'activity_designation',
                                        'state_y': 'activity_state',
                                        'parkName_y': 'activity_parkName'})
        parks_df=parks_df.drop(columns=['index_x','index_y'])

    
        if amenity_ids is not None and activity_ids is not None and len(amenity_ids) > 0 and len(activity_ids) > 0:
            condition = (parks_df['amenity_id'].isin(amenity_ids)) & (parks_df['activity_id'].isin(activity_ids))
            parks_df = parks_df[condition]
            parks_df['activity_parkName_count'] = parks_df['activity_parkName'].apply(lambda x: parks_df['activity_parkName'].value_counts()[x])
            top_parks = parks_df.groupby(['activity_parkName', 'parkCode']).size().reset_index(name='count').sort_values('count', ascending=False).head(3)
            data = top_parks['activity_parkName'].values.tolist()

            return render_template('park.html',data=data)
        return render_template('park.html')
    else:
        park_selected = request.form['park_selected']
        hour_selected = request.form['dropdown_selected']
        return redirect(url_for('next_page', park=park_selected, hour=hour_selected))



@app.route('/contact')
def contact():
    return render_template('contact.html')
  
if __name__ == "__main__":
  app.run(debug = True)
