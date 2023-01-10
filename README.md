
# AI That Reads My Face

This application prompts you with a randomly generated social media post, then using a webcam looks at your
face and determines how you reacted and interacts with the post accordingly.

This is a general overview of the project. If yo uwish to read how I accomplished this project you can check out my article on medium [HERE](https://medium.com/@csharpseth/my-face-liked-your-post-36af4c545df3)

#### Example:
You are prompted with a post of a cat, but you hate cats, so your demeanor is negative. The Computer Vision recognizes this, dislikes the post, then prompts you with the next post.

## Additional Information
I am currently using OpenCV for the facial detection and recognition. I am also using NodeJS w/ Express for the webapp to interact with the Computer Vision model. You could potentially integrate this with actual social media websites. However, when I tried this initially I got stuch on determining when I was looking at a new post. If you can accomplish this I would love to see a fork of this project and how you did it.

## Screenshots

<img src="https://miro.medium.com/max/1100/1*sBZi1B_mHlnegArdRsw4aQ.gif" alt="My Project GIF" width="500" height="600">
<img src="https://miro.medium.com/max/1100/1*wfOh9gFRTM00hApSEqmRFw.webp" alt="My Project GIF" width="500" height="600">

## References
 - [OpenCV](https://opencv.org/)
 - [freeCodeCamp Video](https://youtu.be/oXlwWbU8l2o)
