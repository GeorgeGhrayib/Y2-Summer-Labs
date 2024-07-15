def create_youtube_video(title,description):
    return {"title":title,"description":description,"likes":0,"dislikes":0,"comments":{},"hashtag":[]}

def like(dic):
    if "likes" in dic:
        dic["likes"]+=1
        return dic
        
def dislike(dic):
    if "dislikes" in dic:
        dic["dislikes"]+=1
        return dic
        
def add_comment(youtubevideo,username,comment_text):
    if "comments" in youtubevideo:
        youtubevideo[username]=comment_text
        return youtubevideo
    
vid = create_youtube_video("cool name","----")
for i in range(495):
    vid = like(vid)
vid = dislike(vid)
vid = add_comment(vid,"cool name","cool vid")
vid["hashtag"]=["1","2","3"]

g = create_youtube_video("cosdfgol name","----")
for i in range(45):
    g = like(g)
g = dislike(g)
g = add_comment(g,"coolsdf name","cool vweid")
g["hashtag"]=["13","2","3","34"]

def similarity_to_video(vid1,vid2):
    c=0
    for i in vid1["hashtag"]:
        for j in vid2["hashtag"]:
            if(i==j):
                c+=1
    return c

print("similar: ",similarity_to_video(vid,g)*20,"%")

def istrending(dic):
    return dic["likes"] > 20 and dic["likes"]> dic["dislikes"]

print("is trending: ",istrending(vid))
print(vid)
print(g)
    
    
    
    
    