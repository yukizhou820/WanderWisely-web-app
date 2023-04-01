
def get_park(amenity_ids,activity_ids):
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
             return data
   
