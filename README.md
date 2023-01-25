This project makes use of Youtube API to fetch video information from Youtube channels. Data analysis and plots notebook is also added for fun.

Notebook Version 1
-- function get_video_details (input: video_id, output: view_count, like_count, dislike_count, comment_count) 
-- function get_videos (input: empty dataframe with 8 fields, output: dataframe with data) 
Video information items are listed explicitly, and fetched one by one from the API call response.

Notebook Version 2
-- function get_channel_stats (input: resource object, channel_ids, output: dataframe with channel stats) 
-- function get_video_ids (input: resource object, playlist_id, output: video_ids) 
-- function get_video_details (input: resouce object, video_ids, output: dataframe with 10 fields)
Instead of looping through video ID one by one, version 2 bundles 50 video IDs into each API call, and use dictionary to hold video list part, then fetch information from reponse. 

Python file format Extract_Video_Info_Youtube_API (same as Version 2)

Thanks Thu Vu for a tutorial doing all kinds plots listed below and how to use NLTK. The wordcloud is stunning :-)
Notebook Video_Info_Analysis_Plots
-- convert columns with count to numeric
-- add new field publishDayName (apply lambda function)
-- convert video duration to seconds
-- plots: most/less popular videos, violin plot, Views vs. Likes, Views vs. Comments, video duration, upload schedule
-- customize matplotlib runtime configuration parameters to show Chinese characters on plots
-- create wordcloud using NLTK
