from googleapiclient.discovery import build
import requests
import pandas as pd

def get_channel_stats(youtube_resource, channel_ids):
    # input: youtube_api, channel_ids
    # output: dataframe with channel stats
    all_data = []
    request = youtube_resource.channels().list(part="snippet,contentDetails,statistics", id=','.join(channel_ids))
    response = request.execute()
    
    # loop through items
    for items in response['items']:
        data = {'channelName': items['snippet']['title'],
                'subscribers': items['statistics']['subscriberCount'],
                'views': items['statistics']['viewCount'],
                'totalVideos': items['statistics']['videoCount'],
                'playlistId': items['contentDetails']['relatedPlaylists']['uploads']
        }
        
        all_data.append(data)
        
    return(pd.DataFrame(all_data))

def get_video_ids(youtube_resource, playlist_id):
    # input: youtube_api, playlist_id
    # output: a list containing video ids
    video_ids = []
    
    request = youtube_resource.playlistItems().list(part="snippet,contentDetails", playlistId=playlist_id, maxResults = 50)
    response = request.execute()
    
    for item in response['items']:
        video_ids.append(item['contentDetails']['videoId'])
    
    next_page_token = response.get('nextPageToken')
    while response.get('nextPageToken') is not None: #if none, it means it reached the last page and break out of it
        request = youtube_resource.playlistItems().list(part='contentDetails', playlistId=playlist_id, maxResults = 50, pageToken=next_page_token)
        response = request.execute()

        for item in response['items']:
            video_ids.append(item['contentDetails']['videoId'])

        next_page_token = response.get('nextPageToken')
        
    return video_ids

def get_video_details(youtube_resource,video_ids):
    # input: youtube_api, video_ids
    # output: dataframe with video information
    all_video_info = []
    
    for i in range(0, len(video_ids), 50): # step = 50
        request = youtube_resource.videos().list(part="snippet,contentDetails,statistics", id=','.join(video_ids[i:i+50]))
        response = request.execute()

        for video_item in response['items']:
            item_list = {'snippet': ['channelTitle', 'title', 'description', 'publishedAt'],
                         'statistics': ['viewCount', 'likeCount', 'dislikeCount', 'commentCount'],
                         'contentDetails': ['duration', 'caption']
                         }
            video_info = {}
            video_info['video_id'] = video_item['id']
            for key in item_list.keys():
                for value in item_list[key]:
                    try:
                        video_info[value] = video_item[key][value]
                    except:
                        video_info[value] = None

            all_video_info.append(video_info)
    
    return pd.DataFrame(all_video_info)

def main():
	# keys
    api_key = "xxxxxx"
    api_service_name = "youtube"
    api_version = "v3"

    # create an API client
    youtube_resource = build(api_service_name, api_version, developerKey=api_key) #Construct a Resource for interacting with an API.
    channel_ids = ["UCCKlp1JI9Yg3-cUjKPdD3mw" # magic ingredients
                  ]
    #build dataframe
    channel_stats = get_channel_stats(youtube_resource, channel_ids)
    video_ids = get_video_ids(youtube_resource, channel_stats['playlistId'][0])
    
    video_df = pd.DataFrame(columns=["video_id", "channel_title", "video_title", "upload_date", "view_count", "like_count", "dislike_count", "comment_count"]);
    video_df = get_video_details(youtube_resource, video_ids)
    
    # remove duplicates
    video_df = video_df.drop_duplicates()
    print('dimension: ' + video_df.shape)
    
    video_df.to_csv('Magic_Ingredients_Videos_Stats_V2.csv', index=False)
    
    
if __name__ == "_main_":
    main()

