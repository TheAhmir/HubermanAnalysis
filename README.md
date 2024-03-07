# HubermanAnalysis
<img src="https://github.com/TheAhmir/HubermanAnalysis/assets/100968856/782ca0ff-aba5-4d94-9c42-c226fe97c4bf">

## Scatterplot
<img width="707" alt="Screenshot 2023-09-25 at 3 36 54 AM" src="https://github.com/TheAhmir/HubermanAnalysis/assets/100968856/383c4e78-74a1-4936-adfd-51ca5b103194">

I found out that the way the data was extracted originally was essential in chronilogical order, so i wanted to use that to make a visualization.

I created Scatterplots displaying the number of comments recieved for each video in chronilogical order as well as the number of views recieved for each video in chronilogical order. The size of each dot correlates to the number of characters used in the title of each video.

This idea behind this was to determine overall success from the Huberman's first video to the most current video in my data. I chose to visualize this using a scatterplot because I felt that it might be too much data to visualize all of it in a legible way using a line plot.

I wasn't able to come to many conclusions using this scatterplot. It seems that Huberman has recieved the same amount of interaction as far as comments go throughout his videos and the length of his titles doesn't seem to have an affect of the number of comments.

## Bar Plot 1

<img width="815" alt="Screenshot 2023-09-25 at 3 38 15 AM" src="https://github.com/TheAhmir/HubermanAnalysis/assets/100968856/4a0f45c0-611c-49f4-8815-dac07b3d43ae">

This is a bar plot showing the average number of views is video with a guest star as compared to videos without a guest star. I chose a bar plot because I felt it was a readable way to effectively display the difference between two numeric values.

This visualization was unexpected. My data shows that Huberman's solo videos get more comments than his videos with guest stars. I expected guest star videos to introduce a professionals perspective and cause more viewers to leave comments. 

This could potentially be because he has more videos solo than with guess stars.

## Bar Plot 2
<img width="638" alt="Screenshot 2023-09-25 at 3 40 34 AM" src="https://github.com/TheAhmir/HubermanAnalysis/assets/100968856/754e46ac-8b74-4214-8e89-cdc0aaac0604">

I chose to use bar plots to determine if correlations existed within the data. I felt that this was the most visually apealing and offers the best ease of understanding for me to draw conclusions from.

This plot depics the top 10 videos by view count from left to right with the y-axis being the number of comments. It is one of three seperate graphs that I used in my analysis within my python notebooks.

This plot had an expected result. The videos with more views seem to get more comments.

## PyVis Network
<a href="https://theahmir.github.io/HubermanAnalysis/visualizations/topic_analyses_communities(size_by_views).html">
  <img src="https://github.com/TheAhmir/HubermanAnalysis/assets/100968856/6f84306b-8bef-4093-9aea-3a68d06fa22e"/>
</a>

I believe this was the best way for me to visualize the different communities of relationships within the data. I felt it offered an interesting look into how topics and view count interact within my data.

This visualization shows a network of the the videos with the largest connections between other videos regarding topic. Each unique color shows a network of videos that share a similar topic and the size of each node is based on how many views that video has. This visualization is also interactable. Nodes can be moved and the html can be zoomed in and out to display the names of the videos for each node.

My most interesting observations were in regards to the node sizes by view. Huberman's data showed a lot of close connections around the topic of the brain. These videos also recieve a significant amount of views and comments. The same can be said about videos pertaining to sleep and habit forming.

Lastly, I noticed a larger interconnectedness in videos about hormones. However, these video seem to get less views than his other more common topics. In this case, to increase performance, I would advise less videos about hormones and more about the topics that get more interaction.
